#!/usr/bin/env python3
"""
validate_note.py — quality gate for a Synapse note.

Checks (in order, with early exit on fatal frontmatter errors):

  1. File exists and is parseable as Markdown with a YAML frontmatter block.
  2. All required frontmatter keys are present and non-empty.
  3. paper_type is in the allowed list.
  4. The note's bibliographic block matches the trusted manifest row for this paper.
  5. The DOI in the body's APA citation matches the DOI in the frontmatter.
  6. All required body headings are present in the right order.
  7. For each section heading, the content is either non-trivial or exactly
     "Not reported in paper" (with paper-type-aware exemption).
  8. The verbatim Abstract is a substring of the extracted PDF text. Both sides
     are normalized for whitespace, soft hyphens (U+00AD), curly quotes/
     apostrophes (→ ASCII), and stray C0 control characters. A second hyphen-
     agnostic pass tolerates PDF line-wrap concatenation artifacts. Skipped if
     abstract is "Not reported in paper".
  9. Prose drift: any backticked kebab-case token in the body that is within
     edit distance 2 of a real topics.json slug but isn't an exact match is
     flagged as a likely typo (e.g., `unehical-behavior` near `unethical-behavior`).
 10. Evidence anchors (Layer 1 faithfulness audit — v2+ only): each key in the
     'evidence:' frontmatter block must be a verbatim substring of the extracted
     PDF text, or the literal string "Not reported in paper". Skipped for notes
     with extraction_version != "v2" (backward compatibility with the 90 v1 notes
     already in the corpus).

On failure: prints a list of errors to stderr and exits non-zero. With `--flag`,
also moves the note (or, if it isn't there yet, writes a stub) to
incoming/_flagged/<paper_id>.reason.txt.

Usage:
  python tools/validate_note.py notes/nbs-2026-02-spoor-2026.md
  python tools/validate_note.py notes/nbs-2026-02-spoor-2026.md --flag
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml

# --- locate the Synapse root ------------------------------------------------------

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
LIBRARY = SYNAPSE_ROOT / "library"
FLAGGED = SYNAPSE_ROOT / "incoming" / "_flagged"
TOPICS_PATH = SYNAPSE_ROOT / "index" / "topics.json"

REQUIRED_FRONTMATTER = [
    "id", "title", "authors", "year", "journal", "doi",
    "source", "pdf_path", "text_path", "ingested_at",
    "extraction_model", "extraction_version",
    "paper_type", "keywords", "theory", "topics",
    "unit_of_analysis", "level_of_theory", "dependent_variable_family",
    "methods", "sample",
]

ALLOWED_PAPER_TYPES = {
    "empirical-quantitative", "empirical-qualitative", "empirical-mixed",
    "conceptual", "review", "editorial", "book-review", "other",
}

# Custom analytic field allowed values (mirrors .synapse/config.yaml).
ALLOWED_UNIT_OF_ANALYSIS = {
    "individual", "dyad", "team", "organization", "firm",
    "industry", "market", "country", "multi-level", "na",
}
ALLOWED_LEVEL_OF_THEORY = {"micro", "meso", "macro", "cross-level", "na"}
ALLOWED_DV_FAMILY = {"financial", "social", "environmental", "mixed", "na"}

# Mapping from body heading -> canonical key used by the optional_for_type table.
REQUIRED_HEADINGS = [
    ("Abstract",                 "abstract"),
    ("Research Question",        "research_question"),
    ("Mechanism Process",        "mechanism_process"),
    ("Theoretical Contribution", "theoretical_contribution"),
    ("Practical Implication",    "practical_implication"),
    ("Limitations",              "limitations"),
    ("Future Research",          "future_research"),
    ("APA 7th Citation",         "apa_citation"),
]

OPTIONAL_FOR_TYPE = {
    "book-review": {"research_question", "mechanism_process", "sample", "theoretical_contribution"},
    "editorial":   {"research_question", "mechanism_process", "sample"},
    "review":      {"mechanism_process", "sample"},
    "conceptual":  {"mechanism_process", "sample"},
}

NOT_REPORTED = "Not reported in paper"

# ---- Layer 1 evidence anchor schema (added in v2) --------------------------------
#
# Required keys in the frontmatter's `evidence:` block, per paper type. For
# paper types listed with an empty list, the evidence block is optional (the
# note can omit it entirely). For all other types, each required key must
# carry either a verbatim substring of the extracted PDF text (<=25 words) or
# the literal string NOT_REPORTED ("Not reported in paper", case-sensitive).
#
# This gating only applies to notes with extraction_version == "v2" — older
# v1 notes (the 90 existing notes at the time v2 shipped) have no evidence
# block and are exempt for backward compatibility.

EVIDENCE_REQUIRED_KEYS_BY_TYPE: dict[str, list[str]] = {
    "empirical-quantitative": [
        "sample_n", "sample_country", "sample_industry", "sample_time_period",
        "theories_overview", "methods_overview", "keywords_source",
    ],
    "empirical-qualitative": [
        "sample_n", "sample_country", "sample_industry", "sample_time_period",
        "theories_overview", "methods_overview", "keywords_source",
    ],
    "empirical-mixed": [
        "sample_n", "sample_country", "sample_industry", "sample_time_period",
        "theories_overview", "methods_overview", "keywords_source",
    ],
    # Conceptual / review papers have no empirical sample; the four sample_*
    # keys are still required (the LLM writes "Not reported in paper" into
    # them), so the validator can detect a missing block instead of a quietly
    # absent one. Theories / methods / keywords still apply.
    "conceptual": [
        "sample_n", "sample_country", "sample_industry", "sample_time_period",
        "theories_overview", "methods_overview", "keywords_source",
    ],
    "review": [
        "sample_n", "sample_country", "sample_industry", "sample_time_period",
        "theories_overview", "methods_overview", "keywords_source",
    ],
    # Editorials / book reviews / uncategorized: evidence block is optional.
    # The note may omit it entirely without a validation error. If a block is
    # present, its entries are still checked for substring faithfulness.
    "editorial":   [],
    "book-review": [],
    "other":       [],
}

EVIDENCE_ALL_KNOWN_KEYS = {
    "sample_n", "sample_country", "sample_industry", "sample_time_period",
    "theories_overview", "methods_overview", "keywords_source",
}

EVIDENCE_MAX_WORDS = 25  # warning-tier cap; longer quotes emit a warning but don't fail


# --- parsing helpers --------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("note must start with '---' YAML frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("YAML frontmatter is not terminated with '---'")
    fm_text = text[4:end]
    body = text[end + 5 :]
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        raise ValueError("YAML frontmatter must be a mapping at the top level")
    return fm, body


def parse_body_sections(body: str) -> dict[str, str]:
    """Split the body by '**Heading**' markers and return {heading: content}."""
    sections: dict[str, str] = {}
    parts = re.split(r"^\*\*([^*]+)\*\*\s*\n", body, flags=re.MULTILINE)
    # parts[0] is anything before the first heading (the title H1, etc.) — ignore.
    i = 1
    while i + 1 < len(parts):
        heading = parts[i].strip()
        content = parts[i + 1].strip()
        # Cut at the next blank-line + bold marker if regex left it joined
        sections[heading] = content
        i += 2
    return sections


def normalize_ws(s: str) -> str:
    # Strip soft hyphens (U+00AD). pdftotext emits them mid-word as an
    # invisible typography hint — they don't render in editors, but they
    # are real bytes in the file and silently break the verbatim-substring
    # check. Stripping them from both sides of the comparison is safe
    # because soft hyphens carry no semantic content.
    s = s.replace("\u00ad", "")
    # Normalize curly quotes and apostrophes to ASCII equivalents. LLM
    # output and pdftotext output often disagree on quote style even when
    # the underlying characters are "the same" — e.g., an LLM may emit
    # ASCII ' while the PDF contains U+2019 RIGHT SINGLE QUOTATION MARK.
    # Unifying both sides is always safe for substring matching.
    s = (
        s.replace("\u2018", "'")   # left single quote
         .replace("\u2019", "'")   # right single quote / apostrophe
         .replace("\u201A", "'")   # single low-9 quote
         .replace("\u2032", "'")   # prime
         .replace("\u201C", '"')   # left double quote
         .replace("\u201D", '"')   # right double quote
         .replace("\u201E", '"')   # double low-9 quote
         .replace("\u2033", '"')   # double prime
    )
    # Strip C0/C1 control characters (except \t, \n, \r, which get folded
    # into spaces by the whitespace regex below). pdftotext occasionally
    # emits stray U+0001 bytes mid-word when it fails to interpret an
    # encoded glyph, silently defeating the verbatim-substring check.
    s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)
    # Reunite line-wrap hyphenations BEFORE collapsing whitespace, so the
    # comparison is robust to PDF extraction artifacts.
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize_for_verbatim(s: str) -> str:
    """Stricter-tolerance normalization for the abstract verbatim check only.

    On top of normalize_ws, this also strips ASCII hyphens entirely. PDF
    extractors sometimes concatenate line-wrapped words without preserving
    the hyphen ("self-\\ncategorization" → "selfcategorization"), while the
    LLM reconstructs the hyphenated form from context. Neither side is
    wrong, but a plain substring check fails. Dropping hyphens from both
    sides of the comparison recovers the match without weakening any other
    check — this helper is deliberately scoped to the abstract check only
    so the title-match check stays strict.
    """
    return normalize_ws(s).replace("-", "")


def _edit_distance_le(a: str, b: str, k: int) -> bool:
    """True iff Levenshtein distance between a and b is <= k.

    Fast-reject via length difference; otherwise standard DP. Inputs are
    short topic slugs (< 40 chars) so the DP is trivially cheap.
    """
    if a == b:
        return True
    if abs(len(a) - len(b)) > k:
        return False
    la, lb = len(a), len(b)
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        curr = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(
                curr[j - 1] + 1,      # insertion
                prev[j] + 1,          # deletion
                prev[j - 1] + cost,   # substitution
            )
        prev = curr
    return prev[lb] <= k


# --- check functions --------------------------------------------------------------


def check_required_frontmatter(fm: dict, errors: list[str]) -> None:
    for key in REQUIRED_FRONTMATTER:
        if key not in fm:
            errors.append(f"frontmatter missing key: {key}")
            continue
        value = fm[key]
        if value is None:
            errors.append(f"frontmatter key {key!r} is null")
        elif isinstance(value, str) and not value.strip():
            errors.append(f"frontmatter key {key!r} is empty")


def check_paper_type(fm: dict, errors: list[str]) -> None:
    pt = fm.get("paper_type")
    if pt not in ALLOWED_PAPER_TYPES:
        errors.append(
            f"paper_type {pt!r} not in allowed list: {sorted(ALLOWED_PAPER_TYPES)}"
        )


def load_allowed_topics() -> set[str]:
    """Flatten index/topics.json into a set of all allowed tag slugs."""
    if not TOPICS_PATH.exists():
        return set()
    try:
        data = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    allowed: set[str] = set()
    for domain_key, domain in (data.get("domains") or {}).items():
        allowed.add(domain_key)
        for sub in domain.get("subtopics", []):
            allowed.add(sub)
    for tag in (data.get("context_tags") or {}).get("tags", []):
        allowed.add(tag)
    return allowed


def check_custom_fields(fm: dict, errors: list[str]) -> None:
    """Validate unit_of_analysis, level_of_theory, dependent_variable_family, topics."""
    ua = fm.get("unit_of_analysis")
    if ua not in ALLOWED_UNIT_OF_ANALYSIS:
        errors.append(
            f"unit_of_analysis {ua!r} not in allowed list: "
            f"{sorted(ALLOWED_UNIT_OF_ANALYSIS)}"
        )
    lt = fm.get("level_of_theory")
    if lt not in ALLOWED_LEVEL_OF_THEORY:
        errors.append(
            f"level_of_theory {lt!r} not in allowed list: "
            f"{sorted(ALLOWED_LEVEL_OF_THEORY)}"
        )
    dvf = fm.get("dependent_variable_family")
    if dvf not in ALLOWED_DV_FAMILY:
        errors.append(
            f"dependent_variable_family {dvf!r} not in allowed list: "
            f"{sorted(ALLOWED_DV_FAMILY)}"
        )
    topics = fm.get("topics")
    if not isinstance(topics, list) or not topics:
        errors.append("topics must be a non-empty list of controlled-vocabulary slugs")
        return
    if len(topics) > 4:
        errors.append(f"topics has {len(topics)} entries; maximum is 4")
    allowed = load_allowed_topics()
    if not allowed:
        errors.append(f"could not load allowed topics from {TOPICS_PATH}")
        return
    for t in topics:
        if t not in allowed:
            errors.append(
                f"topic {t!r} is not in index/topics.json. Add it there first, or "
                f"pick an existing slug."
            )


def load_manifest_row(fm: dict) -> dict | None:
    source = fm.get("source", "")
    if "/" not in source:
        return None
    src, issue = source.split("/", 1)
    manifest = LIBRARY / src / issue / "manifest.tsv"
    if not manifest.exists():
        return None
    pdf_name = Path(fm.get("pdf_path", "")).name
    with manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("saved_filename") == pdf_name:
                return row
    return None


def check_bibliographic_match(fm: dict, errors: list[str]) -> None:
    row = load_manifest_row(fm)
    if row is None:
        errors.append("could not locate matching manifest row for bibliographic check")
        return
    # Title must match
    if normalize_ws(row.get("title", "")) != normalize_ws(str(fm.get("title", ""))):
        errors.append(
            f"title mismatch:\n  manifest: {row.get('title')!r}\n  note:     {fm.get('title')!r}"
        )
    # Year must match
    try:
        if int(row.get("year", -1)) != int(fm.get("year", -2)):
            errors.append(
                f"year mismatch: manifest={row.get('year')} note={fm.get('year')}"
            )
    except (ValueError, TypeError):
        errors.append("year is not an integer in note or manifest")
    # DOI must match (normalized)
    note_doi = str(fm.get("doi", "")).strip().lower().rstrip("/")
    raw = (row.get("doi") or "").strip().lower().rstrip("/")
    manifest_doi = raw if raw.startswith("http") else f"https://doi.org/{raw}"
    if note_doi != manifest_doi:
        errors.append(
            f"DOI mismatch:\n  manifest: {manifest_doi!r}\n  note:     {note_doi!r}"
        )


def check_required_headings(body_sections: dict, fm: dict, errors: list[str]) -> None:
    pt = fm.get("paper_type", "")
    optional = OPTIONAL_FOR_TYPE.get(pt, set())
    body_keys = list(body_sections.keys())
    expected_keys = [heading for heading, _key in REQUIRED_HEADINGS]
    if body_keys != expected_keys:
        errors.append(
            "body headings out of order or missing:\n"
            f"  expected: {expected_keys}\n"
            f"  found:    {body_keys}"
        )
        return
    for heading, key in REQUIRED_HEADINGS:
        content = body_sections.get(heading, "")
        if not content:
            errors.append(f"section {heading!r} is empty")
            continue
        if content == NOT_REPORTED and key not in optional and key not in {"limitations", "future_research"}:
            # 'limitations' and 'future_research' are allowed to be Not reported for any
            # type — many empirical papers don't have an explicit limitations or future-
            # research section. Forcing extractors to invent content here is exactly what
            # the faithfulness audit layer catches (see the Li 2026 FAIL in audit sweep).
            errors.append(
                f"section {heading!r} is 'Not reported in paper' but the paper_type "
                f"{pt!r} requires it"
            )


def check_apa_citation_doi(body_sections: dict, fm: dict, errors: list[str]) -> None:
    apa = body_sections.get("APA 7th Citation", "")
    note_doi = str(fm.get("doi", "")).strip().lower().rstrip("/")
    if note_doi and note_doi not in apa.lower():
        errors.append(
            f"APA citation does not contain the frontmatter DOI {note_doi!r}"
        )


def check_prose_topic_drift(body: str, errors: list[str]) -> None:
    """Flag backticked kebab-case tokens in the body that look like topic
    slugs but are near-misses to a real entry in index/topics.json.

    This is a narrow backstop against prose drift — the LLM writing e.g.
    `unehical-behavior` (a 1-character typo of `unethical-behavior`) in a
    distillation section, which the current frontmatter-only topic check
    would never catch. We deliberately only flag tokens that are within
    edit distance 2 of a real topic slug, so incidental kebab-case code
    like `pdf-to-text` or `not-reported-in-paper` does NOT trigger false
    positives — they aren't close to any vocabulary term.
    """
    allowed = load_allowed_topics()
    if not allowed:
        return
    # Tokens shaped like a topic slug: lowercase kebab-case with 2-5 segments,
    # enclosed in backticks in the body prose. No dots/slashes/underscores.
    candidates = set(
        re.findall(
            r"`([a-z][a-z0-9]*(?:-[a-z0-9]+){1,4})`",
            body,
        )
    )
    for cand in sorted(candidates):
        if cand in allowed:
            continue
        close = sorted(t for t in allowed if _edit_distance_le(cand, t, 2))
        if close:
            errors.append(
                f"body prose contains backticked topic-like token {cand!r} "
                f"that is not in index/topics.json. Likely typo of: "
                f"{', '.join(close)}"
            )


def check_abstract_verbatim(body_sections: dict, fm: dict, errors: list[str]) -> None:
    abstract = body_sections.get("Abstract", "")
    if abstract == NOT_REPORTED or not abstract:
        return
    text_path = SYNAPSE_ROOT / fm.get("text_path", "")
    if not text_path.exists():
        errors.append(f"text_path does not exist for verbatim check: {text_path}")
        return
    src = text_path.read_text(encoding="utf-8", errors="replace")
    # Two-pass check: first try the strict normalization (whitespace, soft
    # hyphens, curly quotes, control chars); if that fails, fall back to
    # hyphen-agnostic matching to tolerate PDF line-wrap concatenation
    # artifacts. Only if BOTH fail do we report paraphrase.
    if normalize_ws(abstract) not in normalize_ws(src):
        if normalize_for_verbatim(abstract) not in normalize_for_verbatim(src):
            errors.append(
                "Abstract is not a verbatim substring of the extracted PDF text "
                "(whitespace-normalized). The LLM may have paraphrased."
            )


def check_evidence_anchors(fm: dict, errors: list[str]) -> None:
    """Layer 1 faithfulness audit — mechanical substring check of evidence anchors.

    For notes produced by extraction prompt v2+, the frontmatter must contain an
    'evidence:' mapping. Each value in that mapping is either a verbatim <=25-word
    substring of the extracted PDF text OR the literal string 'Not reported in
    paper' (case-sensitive — the only permissible escape valve). Fabricated quotes
    are caught deterministically by the two-pass normalization used for the
    abstract verbatim check.

    This function:
      - Skips v1 (pre-audit) notes entirely, preserving the existing corpus as a
        regression baseline.
      - Fails if a v2 note is missing the 'evidence:' block for a paper type that
        requires one.
      - Fails if a required key is missing or empty.
      - Fails if a quote is not a substring of the PDF text under either
        normalization pass.
      - Emits a stderr warning (not a fatal error) if a quote is longer than
        EVIDENCE_MAX_WORDS. The cap exists to keep anchors short enough that
        whitespace/hyphen normalization can't make a fabricated quote match by
        accident — but we prefer a too-long real quote to a paraphrased short one.
      - Warns (stderr only) about unknown keys present in the evidence block, so
        prompt-drift doesn't silently ship a new required key without a validator
        update.
    """
    # Backward compatibility: only enforce for v2+ notes. The 90 existing notes
    # carry extraction_version == "v1" and have no evidence block.
    if fm.get("extraction_version") != "v2":
        return
    paper_type = fm.get("paper_type", "")
    required_keys = EVIDENCE_REQUIRED_KEYS_BY_TYPE.get(paper_type, [])
    evidence = fm.get("evidence")
    # Paper types with no required keys (editorial, book-review, other) may
    # omit the block entirely. If they include one, still fall through to the
    # per-key checks below so a present-but-malformed block is not silently
    # accepted.
    if not required_keys and evidence is None:
        return
    if evidence is None:
        errors.append(
            f"v2 note is missing the 'evidence:' frontmatter block "
            f"(paper_type={paper_type!r} requires keys: {required_keys})"
        )
        return
    if not isinstance(evidence, dict):
        errors.append(
            f"'evidence' frontmatter must be a mapping, got {type(evidence).__name__}"
        )
        return

    # Load the PDF text once so the per-key loop does no extra I/O.
    text_path = SYNAPSE_ROOT / fm.get("text_path", "")
    if not text_path.exists():
        errors.append(
            f"text_path does not exist for evidence-anchor check: {text_path}"
        )
        return
    src = text_path.read_text(encoding="utf-8", errors="replace")
    src_norm = normalize_ws(src)
    src_norm_hyphen = normalize_for_verbatim(src)

    # Required-key presence check.
    for key in required_keys:
        if key not in evidence:
            errors.append(f"evidence missing required key: {key!r}")

    # Unknown-key warning (stderr only; not a fatal error).
    unknown = set(evidence.keys()) - EVIDENCE_ALL_KNOWN_KEYS
    for key in sorted(unknown):
        print(
            f"  warning: evidence contains unknown key {key!r} — not in the v2 "
            f"schema. Remove it or extend EVIDENCE_ALL_KNOWN_KEYS.",
            file=sys.stderr,
        )

    # Substring check for each present key (required or not — we audit every
    # anchor the note emits).
    for key, quote in evidence.items():
        if not isinstance(quote, str) or not quote.strip():
            errors.append(f"evidence[{key!r}] is empty or not a string")
            continue
        quote = quote.strip()
        # The ONLY acceptable escape valve — case-sensitive, exact match.
        if quote == NOT_REPORTED:
            continue
        # Word-count warning (not fatal).
        word_count = len(quote.split())
        if word_count > EVIDENCE_MAX_WORDS:
            print(
                f"  warning: evidence[{key!r}] is {word_count} words "
                f"(cap is {EVIDENCE_MAX_WORDS}); prefer a shorter anchor quote",
                file=sys.stderr,
            )
        # Two-pass substring check — same machinery as the abstract check.
        if normalize_ws(quote) in src_norm:
            continue
        if normalize_for_verbatim(quote) in src_norm_hyphen:
            continue
        # Fabrication caught. Surface the first 40 chars to help triage.
        preview = quote[:40] + ("…" if len(quote) > 40 else "")
        errors.append(
            f"evidence[{key!r}] is not a verbatim substring of the extracted "
            f"PDF text (first 40 chars: {preview!r}). The LLM may have "
            f"fabricated this anchor, or the extraction prompt failed to "
            f"retrieve the right passage."
        )


# --- main -------------------------------------------------------------------------


def validate(note_path: Path) -> list[str]:
    errors: list[str] = []
    if not note_path.exists():
        return [f"note file does not exist: {note_path}"]
    text = note_path.read_text(encoding="utf-8")
    try:
        fm, body = split_frontmatter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"frontmatter parse error: {exc}"]

    check_required_frontmatter(fm, errors)
    check_paper_type(fm, errors)
    check_custom_fields(fm, errors)
    check_bibliographic_match(fm, errors)

    sections = parse_body_sections(body)
    check_required_headings(sections, fm, errors)
    check_apa_citation_doi(sections, fm, errors)
    check_abstract_verbatim(sections, fm, errors)
    check_prose_topic_drift(body, errors)
    check_evidence_anchors(fm, errors)  # Layer 1 faithfulness audit (v2+ only)
    return errors


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: validate_note.py <note.md> [--flag]", file=sys.stderr)
        return 2
    flag = "--flag" in args
    paths = [Path(a) for a in args if not a.startswith("--")]
    overall = 0
    for p in paths:
        errors = validate(p.resolve())
        if errors:
            overall = 1
            print(f"FAIL  {p}")
            for e in errors:
                print(f"  - {e}")
            if flag:
                FLAGGED.mkdir(parents=True, exist_ok=True)
                reason = FLAGGED / (p.stem + ".reason.txt")
                reason.write_text("\n".join(errors) + "\n", encoding="utf-8")
                print(f"  flagged: {reason.relative_to(SYNAPSE_ROOT)}")
        else:
            print(f"OK    {p}")
    return overall


if __name__ == "__main__":
    sys.exit(main())
