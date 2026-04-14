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
  8. The verbatim Abstract is a substring of the extracted PDF text (whitespace
     normalized). Skipped if abstract is "Not reported in paper".

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
    # Reunite line-wrap hyphenations BEFORE collapsing whitespace, so the
    # comparison is robust to PDF extraction artifacts.
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return re.sub(r"\s+", " ", s).strip()


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
        if content == NOT_REPORTED and key not in optional and key != "limitations":
            # 'limitations' is allowed to be Not reported for any type — many empirical
            # papers don't have an explicit limitations section.
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


def check_abstract_verbatim(body_sections: dict, fm: dict, errors: list[str]) -> None:
    abstract = body_sections.get("Abstract", "")
    if abstract == NOT_REPORTED or not abstract:
        return
    text_path = SYNAPSE_ROOT / fm.get("text_path", "")
    if not text_path.exists():
        errors.append(f"text_path does not exist for verbatim check: {text_path}")
        return
    src = text_path.read_text(encoding="utf-8", errors="replace")
    if normalize_ws(abstract) not in normalize_ws(src):
        errors.append(
            "Abstract is not a verbatim substring of the extracted PDF text "
            "(whitespace-normalized). The LLM may have paraphrased."
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
