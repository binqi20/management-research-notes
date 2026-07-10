#!/usr/bin/env python3
"""
audit_note.py — two-layer faithfulness audit for a generated Synapse note.

    Layer 1 (mechanical, deterministic)
    -----------------------------------
    Every value in the note's `evidence:` frontmatter block must be a verbatim
    substring of the extracted PDF text, or the literal string
    "Not reported in paper". This is the same check that lives in
    `tools/validate_note.py:check_evidence_anchors` — we import it directly so
    the two entry points never disagree about what counts as a pass.

    Layer 2 (semantic, LLM-based)
    -----------------------------
    A fresh independent auditor reads the rubric at `docs/audit-rubric.md`, the
    note body, and the PDF text, and returns a per-prose-field JSON verdict from
    the set { SUPPORTED, PARTIAL, UNSUPPORTED, CONTRADICTED }. The auditor runs
    in a cold context so it has no prior commitment to the note's claims.

    Two layers run in order. A Layer 1 failure short-circuits Layer 2 unless
    --force-layer-2 is set (you almost never want this — bad anchors mean bad
    claims, and paying for an LLM pass on fabricated content is wasted work).

Usage
-----
    python tools/audit_note.py notes/<paper_id>.md [options]

    Layer 2 needs an independent verdict: pass --layer-2-json PATH (the Codex
    default) or --auditor-model claude-<model> (legacy CLI dispatcher). A bare
    invocation runs Layer 1 then errors on Layer 2 by design; use --skip-layer-2
    for a Layer-1-only check.

Options
-------
    --flag                    On fail, write incoming/_flagged/<id>.reason.txt
    --dry-run                 Compute the audit but DO NOT write the JSON report
                              or the flag sidecar. Report is still printed.
    --skip-layer-2            Run Layer 1 only. No subagent dispatch.
    --prompt-only             Print the Layer 2 prompt to stdout and exit 0.
                              Useful when the calling agent wants to dispatch
                              the Task tool directly and needs the prompt text.
    --layer-2-json PATH       Skip Layer 2 dispatch; read an independent
                              subagent's JSON verdict from PATH. The JSON must
                              include provenance tying it to the current note,
                              extracted text, rubric, model, timestamp, and
                              dispatch mode.
    --force-layer-2           Run Layer 2 even if Layer 1 failed (debugging).
    --auditor-model MODEL     Override the auditor model recorded in reports.
                              The default is the Codex external-audit model.
                              The legacy Claude CLI path requires an explicit
                              Claude model such as claude-opus-4-6.

Exit codes
----------
    0 — audit passed (or dry-run completed successfully)
    1 — audit failed (Layer 1 or Layer 2)
    2 — error (missing files, parse error, subagent call failed, etc.)

Output files
------------
    incoming/_audits/<paper_id>.audit.json   — the combined audit report
    incoming/_flagged/<paper_id>.reason.txt  — on fail with --flag

Designed to be cheap to re-run. The audit JSON is the source of truth; calling
`audit_note.py` again just overwrites it with a fresh result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- reuse validator internals so the two tools never disagree ---------------------

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
sys.path.insert(0, str(THIS_FILE.parent))

from validate_note import (  # noqa: E402 — path munging above is intentional
    EVIDENCE_ALL_KNOWN_KEYS,
    EVIDENCE_REQUIRED_KEYS_BY_TYPE,
    NOT_REPORTED,
    check_evidence_anchors,
    normalize_for_verbatim,
    normalize_ws,
    parse_body_sections,
    split_frontmatter,
)

AUDITS_DIR = SYNAPSE_ROOT / "incoming" / "_audits"
FLAGGED_DIR = SYNAPSE_ROOT / "incoming" / "_flagged"
RUBRIC_PATH = SYNAPSE_ROOT / "docs" / "audit-rubric.md"
DEFAULT_AUDITOR_MODEL = "gpt-5.5"
AUDIT_VERSION = "v1"
# The single canonical rubric doc (docs/audit-rubric.md) is now v2: it scores the
# original six prose fields plus the three v3 fields (Hypotheses / Propositions,
# Data & Measures, Key Findings), instructing the auditor to score only the fields
# a given note actually contains. New audits of any note therefore read rubric v2;
# historical audit JSONs stamped "v1" remain valid and are not re-checked.
RUBRIC_VERSION = "v2"

# Prose fields the Layer 2 subagent verdicts against. Must match the keys in
# the rubric's output-format example — if the rubric changes, this list must
# move with it. (Validated at parse time by parse_auditor_response.)
LAYER_2_PROSE_FIELDS = [
    "research_question",
    "mechanism_process",
    "theoretical_contribution",
    "practical_implication",
    "limitations",
    "future_research",
]

# v3 notes add three empirical prose fields, scored in note-body order. v1/v2
# notes keep the original six-field contract. The set is chosen per note by
# extraction_version so the existing corpus audits identically and a v3 audit is
# *required* to score Key Findings (the field most exposed to sign reversal).
LAYER_2_PROSE_FIELDS_V3 = [
    "research_question",
    "hypotheses",
    "mechanism_process",
    "data_measures",
    "key_findings",
    "theoretical_contribution",
    "practical_implication",
    "limitations",
    "future_research",
]


def prose_fields_for(extraction_version: str | None) -> list[str]:
    """Return the Layer 2 prose fields the auditor must verdict for a note."""
    if extraction_version == "v3":
        return LAYER_2_PROSE_FIELDS_V3
    return LAYER_2_PROSE_FIELDS


VERDICT_ENUM = {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "CONTRADICTED"}
CONFIDENCE_ENUM = {"high", "medium", "low"}
EXTERNAL_PROVENANCE_REQUIRED_KEYS = {
    "paper_id",
    "note_sha256",
    "text_sha256",
    "rubric_version",
    "auditor_model",
    "generated_at",
    "dispatch_mode",
}

# When the post-strip PDF text exceeds max_pdf_chars, build_auditor_prompt
# uses a "sandwich": keep SANDWICH_HEAD_RATIO of the budget for the front of
# the paper (abstract, intro, theory, methods, results) and the remainder for
# the tail (discussion, practical implications, limitations, future research).
# The middle — typically detailed results — is the safest part to drop because
# the six audited prose fields draw from the front (research_question,
# mechanism_process, theoretical_contribution) and the back (practical_implication,
# limitations, future_research).
#
# This ratio is a tunable knob. If future audit JSONs in incoming/_audits/ show
# new mechanism_process PARTIALs whose notes say the auditor "couldn't find" a
# measure or hypothesis, raise toward 0.65–0.70 (more front context). If
# limitations or future_research PARTIALs reappear with truncation-related
# language, lower toward 0.55–0.50 (more tail context).
SANDWICH_HEAD_RATIO = 0.6
# Bytes reserved for the "[... middle of paper truncated (NNNNN chars dropped) ...]"
# marker inside the sandwich. Generous bound — the actual marker is ~75 chars.
SANDWICH_SEPARATOR_RESERVE = 80

# Audit text budget (v0.31.0: raised from 180K after corpus measurement — raw text
# sizes run p90=204K / p97=234K / p99=278K chars, so 240K leaves only ~1% of papers
# truncated). The single module constant is used by every call site; never override
# per-call, or the prompt-time fitted text and the assembly-time audit_context
# silently desynchronize.
MAX_PDF_CHARS = 240_000

# Anchor-aware splicing (v0.31.0). When the sandwich drops the middle of a long
# paper, any evidence anchor whose only occurrence lies in the dropped region gets
# a context window spliced back in, so the Layer 2 auditor can always see the
# passages backing the note's claims. v3 raised the stakes: Key Findings evidence
# lives mid-paper, and a dropped Results section can turn a faithful Key Findings
# field into a false UNSUPPORTED — an audit FAIL, not just a PARTIAL.
SPLICE_WINDOW_CHARS = 1_000        # context kept on each side of a located anchor chunk
SPLICE_CHUNK_CHARS = 4_000         # scan granularity; >> the longest corpus anchor (~200 chars)
SPLICE_TOTAL_BUDGET_CHARS = 20_000 # cap on total spliced chars per paper


# --- loading helpers ---------------------------------------------------------------


def load_note(note_path: Path) -> tuple[dict, str, dict]:
    """Parse a note and return (frontmatter, body, sections)."""
    if not note_path.exists():
        raise FileNotFoundError(f"note file does not exist: {note_path}")
    text = note_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    sections = parse_body_sections(body)
    return fm, body, sections


def load_pdf_text(fm: dict) -> str:
    """Load the extracted PDF text referenced by the note's text_path."""
    text_path = SYNAPSE_ROOT / fm.get("text_path", "")
    if not text_path.exists():
        raise FileNotFoundError(f"text_path does not exist: {text_path}")
    return text_path.read_text(encoding="utf-8", errors="replace")


def load_rubric() -> str:
    """Load the canonical rubric text so the subagent reads the same instructions."""
    if not RUBRIC_PATH.exists():
        raise FileNotFoundError(f"rubric missing: {RUBRIC_PATH}")
    return RUBRIC_PATH.read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest for UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- Layer 1 -----------------------------------------------------------------------


def run_layer_1(fm: dict) -> dict:
    """Run the mechanical evidence-anchor check and return a structured result.

    We delegate to the validator's check_evidence_anchors — the same function
    that runs inside `validate_note.py`. This means a note that passes
    `validate_note.py` for evidence anchors is guaranteed to pass Layer 1 here,
    and vice versa. The two entry points can never drift.
    """
    errors: list[str] = []
    check_evidence_anchors(fm, errors)

    anchors_checked = 0
    evidence = fm.get("evidence") or {}
    if isinstance(evidence, dict):
        anchors_checked = sum(1 for v in evidence.values() if v != NOT_REPORTED)

    # Partition errors into "missing key" and "not a substring" for structured
    # reporting. The validator emits these as two distinct message shapes.
    missing: list[str] = []
    not_in_pdf: list[str] = []
    other: list[str] = []
    for err in errors:
        if err.startswith("evidence missing required key:"):
            missing.append(err)
        elif "is not a verbatim substring" in err:
            not_in_pdf.append(err)
        else:
            other.append(err)

    return {
        "overall": "fail" if errors else "pass",
        "anchors_checked": anchors_checked,
        "anchors_missing": missing,
        "anchors_not_found_in_pdf": not_in_pdf,
        "other_errors": other,
    }


# --- Layer 2 helpers ----------------------------------------------------------------


def _strip_references(text: str) -> tuple[str, int]:
    """Strip the References/Bibliography section from the end of PDF text.

    Academic papers end with a References section (sometimes followed by
    appendices). For audit purposes, the Discussion and Conclusions sections
    are far more valuable than the bibliography, so stripping references
    before truncation preserves the content the auditor actually needs to
    verify limitations and future-research claims.

    Returns (stripped_text, chars_removed). If no references heading is found,
    returns the original text unchanged with 0 chars removed.

    Safety guards: only strips if the heading appears in the back half of the
    text (>50% offset), to avoid false positives from a "References" heading
    that appears early in the introduction; and a heading followed at prose
    distance (1-2 spaces) by a lowercase word is rejected as sentence text,
    not a heading.
    """
    # Common headings, anchored at the start of a line (after a newline).
    # Allow optional leading whitespace (\s*) because two-column PDF
    # extractions often center section headings with spaces.
    # Use \b (word boundary) at the end instead of \s*\n — two-column
    # PDF extraction often concatenates the heading with the first
    # reference entry on the same line, so there's no trailing newline.
    # The prose guard (?![ \t]{1,2}[a-z]) rejects a heading word followed at
    # prose distance (one or two spaces) by a lowercase word — that's a
    # sentence, not a heading: "References to how the acts of courage
    # would..." (AMJ 57(1) Koerner, where this cut the entire Discussion out
    # of the audit prompt) or the meta-analysis note "References marked with
    # an asterisk indicate...". Wide space runs (3+) must stay matchable: in
    # two-column -layout output they are column gaps, where the OTHER
    # column's lowercase text legitimately shares the heading's physical
    # line ("REFERENCES          ecological approach to management..."). A
    # newline straight after the heading also stays matchable.
    # We search for the LAST match in the back half of the text.
    prose_guard = r"(?![ \t]{1,2}[a-z])"
    patterns = [
        r"\n\s*References\b" + prose_guard,
        r"\n\s*REFERENCES\b" + prose_guard,
        r"\n\s*Bibliography\b" + prose_guard,
        r"\n\s*BIBLIOGRAPHY\b" + prose_guard,
        r"\n\s*Works Cited\b" + prose_guard,
        r"\n\s*Literature Cited\b" + prose_guard,
    ]
    last_pos = -1
    for pat in patterns:
        for m in re.finditer(pat, text):
            if m.start() > last_pos:
                last_pos = m.start()

    if last_pos > 0 and last_pos > len(text) * 0.5:
        stripped = text[:last_pos].rstrip()
        return stripped, len(text) - len(stripped)

    return text, 0


# --- Layer 2 prompt building -------------------------------------------------------


def anchor_quotes(fm: dict) -> list[str]:
    """The note's evidence-anchor quotes (escape-valve entries excluded).

    These are the passages the Layer 2 auditor most needs to see; the
    anchor-aware sandwich guarantees each one survives truncation.
    """
    evidence = fm.get("evidence") or {}
    if not isinstance(evidence, dict):
        return []
    return [
        v.strip()
        for v in evidence.values()
        if isinstance(v, str) and v.strip() and v.strip() != NOT_REPORTED
    ]


def _scan_region_for_anchor(
    q_ws: str, q_vb: str, region: str, base: int, overlap: int
) -> tuple[int, int] | None:
    """Chunk-scan `region` (starting at offset `base` in its parent text) for an
    anchor. Returns (lo, hi) chunk offsets in the parent text, or None.

    Chunks overlap by `overlap` chars, so any occurrence whose raw span is
    shorter than the overlap is fully interior to at least one chunk — the
    normalized substring test then finds it despite offset-shifting artifacts
    (soft hyphens, line-wrap hyphenation, whitespace runs).
    """
    if not region:
        return None
    step = max(SPLICE_CHUNK_CHARS - overlap, 1)
    for s in range(0, max(len(region) - overlap, 1), step):
        chunk = region[s : s + SPLICE_CHUNK_CHARS]
        if q_ws in normalize_ws(chunk) or q_vb in normalize_for_verbatim(chunk):
            return (base + s, base + min(s + SPLICE_CHUNK_CHARS, len(region)))
    return None


def _merge_and_cap_windows(
    windows: list[tuple[int, int]], budget: int
) -> tuple[list[tuple[int, int]], int]:
    """Merge overlapping/adjacent (lo, hi) windows, then cap total size.

    Windows beyond the budget are dropped in ascending offset order
    (deterministic). Returns (kept_windows, dropped_count).
    """
    merged: list[list[int]] = []
    for lo, hi in sorted(windows):
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    kept: list[tuple[int, int]] = []
    total = dropped = 0
    for lo, hi in merged:
        if total + (hi - lo) <= budget:
            kept.append((lo, hi))
            total += hi - lo
        else:
            dropped += 1
    return kept, dropped


def fit_pdf_text_for_audit(
    pdf_text: str,
    max_pdf_chars: int = MAX_PDF_CHARS,
    anchors: list[str] | None = None,
) -> tuple[str, dict]:
    """Fit extracted PDF text into the Layer 2 audit budget.

    Three-step process:
      1. Strip the References/Bibliography section via _strip_references().
      2. If the post-strip text still exceeds max_pdf_chars, apply the
         "sandwich": keep SANDWICH_HEAD_RATIO of the budget from the front
         (abstract, intro, theory, methods) and the remainder from the back
         (discussion, implications, limitations, future research).
      3. Anchor-aware splicing (v0.31.0): for each evidence anchor from the
         note, first test membership in the normalized head/tail; anchors
         found nowhere in the fitted ends get a chunk-scan of the dropped
         middle (with straddle and stripped-References fallbacks) and a
         ±SPLICE_WINDOW_CHARS context window spliced back in, budget-capped.
         This guarantees the auditor sees the passages backing the note's
         claims — critical for v3, whose Key Findings evidence lives in the
         Results section that the plain sandwich used to drop.

    With no anchors (or none missing), the over-budget output is byte-identical
    to the legacy head + separator + tail sandwich.

    Returns (fitted_text, context_metadata). The metadata is persisted in the
    audit report so a later reviewer can see exactly how much source text the
    auditor received and which anchors needed splicing.
    """
    stripped, refs_removed = _strip_references(pdf_text)

    context = {
        "max_pdf_chars": max_pdf_chars,
        "original_pdf_chars": len(pdf_text),
        "post_reference_strip_chars": len(stripped),
        "references_removed_chars": refs_removed,
        "fitted_pdf_chars": len(stripped),
        "sandwich_truncated": False,
        "sandwich_head_chars": 0,
        "sandwich_tail_chars": 0,
        "sandwich_middle_dropped_chars": 0,
        "sandwich_head_ratio": SANDWICH_HEAD_RATIO,
        "anchors_total": len(anchors) if anchors else 0,
        "anchors_in_head_tail": 0,
        "anchors_in_dropped_middle": 0,
        "anchors_in_stripped_refs": 0,
        "anchors_not_located": 0,
        "windows_spliced": 0,
        "spliced_chars": 0,
        "windows_dropped_over_budget": 0,
    }

    if len(stripped) <= max_pdf_chars:
        return stripped, context

    available = max_pdf_chars - SANDWICH_SEPARATOR_RESERVE
    head_chars = int(available * SANDWICH_HEAD_RATIO)
    tail_chars = available - head_chars
    middle_dropped = len(stripped) - head_chars - tail_chars
    mid_lo, mid_hi = head_chars, len(stripped) - tail_chars

    context.update(
        sandwich_truncated=True,
        sandwich_head_chars=head_chars,
        sandwich_tail_chars=tail_chars,
        sandwich_middle_dropped_chars=middle_dropped,
    )

    head = stripped[:head_chars]
    tail = stripped[mid_hi:]

    mid_windows: list[tuple[int, int]] = []
    ref_windows: list[tuple[int, int]] = []
    if anchors:
        head_ws, head_vb = normalize_ws(head), normalize_for_verbatim(head)
        tail_ws, tail_vb = normalize_ws(tail), normalize_for_verbatim(tail)
        # Overlap must exceed any anchor's raw span (raw span > normalized
        # length because hyphenation/whitespace artifacts collapse under
        # normalization); anchors are ≤ ~200 chars corpus-wide, and the
        # 25-word cap is warning-tier only, so scale with the longest.
        overlap = max(400, 2 * max(len(a) for a in anchors))
        for quote in anchors:
            q_ws = normalize_ws(quote)
            q_vb = normalize_for_verbatim(quote)
            if (
                q_ws in head_ws
                or q_ws in tail_ws
                or q_vb in head_vb
                or q_vb in tail_vb
            ):
                context["anchors_in_head_tail"] += 1
                continue
            # Scan the dropped middle first; fall back to the whole stripped
            # text (an anchor can straddle the head/middle or middle/tail cut,
            # where neither membership nor the middle-only scan can see it).
            hit = _scan_region_for_anchor(
                q_ws, q_vb, stripped[mid_lo:mid_hi], mid_lo, overlap
            ) or _scan_region_for_anchor(q_ws, q_vb, stripped, 0, overlap)
            if hit is not None:
                context["anchors_in_dropped_middle"] += 1
                lo = max(hit[0] - SPLICE_WINDOW_CHARS, mid_lo)
                hi = min(hit[1] + SPLICE_WINDOW_CHARS, mid_hi)
                if hi > lo:
                    mid_windows.append((lo, hi))
                continue
            # Layer 1 verified anchors against the FULL text, so the only
            # occurrence may live in the stripped References/appendix tail
            # (AMJ appendices carry robustness results).
            if refs_removed:
                hit = _scan_region_for_anchor(
                    q_ws, q_vb, pdf_text[len(stripped):], len(stripped), overlap
                )
                if hit is not None:
                    context["anchors_in_stripped_refs"] += 1
                    lo = max(hit[0] - SPLICE_WINDOW_CHARS, len(stripped))
                    hi = min(hit[1] + SPLICE_WINDOW_CHARS, len(pdf_text))
                    ref_windows.append((lo, hi))
                    continue
            context["anchors_not_located"] += 1

    mid_windows, dropped_mid = _merge_and_cap_windows(
        mid_windows, SPLICE_TOTAL_BUDGET_CHARS
    )
    ref_budget = SPLICE_TOTAL_BUDGET_CHARS - sum(hi - lo for lo, hi in mid_windows)
    ref_windows, dropped_ref = _merge_and_cap_windows(ref_windows, max(ref_budget, 0))
    context["windows_dropped_over_budget"] = dropped_mid + dropped_ref
    context["windows_spliced"] = len(mid_windows) + len(ref_windows)
    context["spliced_chars"] = sum(hi - lo for lo, hi in mid_windows + ref_windows)

    # Assemble: head + [gap markers / spliced windows] + tail + refs splices.
    # Windows touching the head or tail coalesce with no marker interposed —
    # a marker there would re-break the very anchor the splice preserves.
    parts = [head]
    cursor = mid_lo
    for lo, hi in mid_windows:
        if lo > cursor:
            parts.append(
                f"\n\n[... {lo - cursor:,} chars dropped; resuming at "
                f"evidence-anchor context ...]\n\n"
            )
        parts.append(stripped[lo:hi])
        cursor = hi
    if cursor < mid_hi:
        if mid_windows:
            parts.append(f"\n\n[... {mid_hi - cursor:,} chars dropped ...]\n\n")
        else:
            # Legacy single-separator sandwich — byte-identical to the
            # pre-splice implementation (regression-pinned in tests).
            parts.append(
                f"\n\n[... middle of paper truncated "
                f"({middle_dropped:,} chars dropped) ...]\n\n"
            )
    parts.append(tail)
    for lo, hi in ref_windows:
        parts.append(
            "\n\n[... spliced from the removed references/appendix section "
            "(evidence-anchor context) ...]\n\n"
        )
        parts.append(pdf_text[lo:hi])

    fitted = "".join(parts)
    context["fitted_pdf_chars"] = len(fitted)
    return fitted, context


def build_auditor_prompt_and_context(
    paper_id: str,
    paper_type: str,
    body: str,
    pdf_text: str,
    rubric_text: str,
    max_pdf_chars: int = MAX_PDF_CHARS,
    anchors: list[str] | None = None,
) -> tuple[str, dict]:
    """Construct the prompt for the Layer 2 auditor subagent.

    The prompt is deliberately structured so the subagent's output IS a JSON
    object — no preamble, no prose wrapper, no fenced block. We re-parse
    defensively in parse_auditor_response so a non-compliant response doesn't
    hang the pipeline.
    """
    truncated, context = fit_pdf_text_for_audit(
        pdf_text, max_pdf_chars=max_pdf_chars, anchors=anchors
    )
    refs_removed = context["references_removed_chars"]
    sandwich_middle_dropped = context["sandwich_middle_dropped_chars"]
    sandwich_head_chars = context["sandwich_head_chars"]
    sandwich_tail_chars = context["sandwich_tail_chars"]
    stripped_chars = context["post_reference_strip_chars"]

    truncated_note = ""
    if refs_removed > 0 or sandwich_middle_dropped > 0:
        parts: list[str] = []
        if refs_removed > 0:
            parts.append(
                f"References/bibliography section stripped "
                f"({refs_removed:,} chars)"
            )
        if sandwich_middle_dropped > 0:
            parts.append(
                f"sandwich-truncated to {sandwich_head_chars:,} head + "
                f"{sandwich_tail_chars:,} tail chars "
                f"(post-strip length: {stripped_chars:,} chars; "
                f"{sandwich_middle_dropped:,} chars dropped from middle)"
            )
        truncated_note = (
            f"\n\n[{'; '.join(parts)}. "
            f"Original PDF text: {len(pdf_text):,} chars.]\n"
        )

    # The assembled prompt. Order matters:
    #   1. Rubric (instructions, verdict definitions, output schema)
    #   2. Paper metadata (paper_id, paper_type)
    #   3. Note body (the thing being audited)
    #   4. PDF text (the source of truth)
    # Placing the PDF text LAST minimizes the chance that instructions near the
    # top of the prompt get diluted by a giant text blob.
    prompt = f"""{rubric_text}

---

# Audit task

You are auditing the following note against its source PDF. Follow the rubric
above exactly. Produce ONLY the JSON object defined in the "Output format"
section. No preamble, no fenced code block, no commentary, no Markdown — just
the JSON.

## Paper metadata

- paper_id: {paper_id}
- paper_type: {paper_type}

## Note body (the thing you are auditing)

```
{body.strip()}
```

## PDF text (the source of truth){truncated_note}

```
{truncated}
```

---

Emit the JSON object now.
"""
    return prompt, context


def build_auditor_prompt(
    paper_id: str,
    paper_type: str,
    body: str,
    pdf_text: str,
    rubric_text: str,
    max_pdf_chars: int = MAX_PDF_CHARS,
    anchors: list[str] | None = None,
) -> str:
    """Backward-compatible wrapper returning only the Layer 2 prompt."""
    prompt, _ = build_auditor_prompt_and_context(
        paper_id=paper_id,
        paper_type=paper_type,
        body=body,
        pdf_text=pdf_text,
        rubric_text=rubric_text,
        max_pdf_chars=max_pdf_chars,
        anchors=anchors,
    )
    return prompt


# --- Layer 2 dispatcher ------------------------------------------------------------


def dispatch_auditor_via_cli(prompt: str, auditor_model: str) -> str:
    """Shell out to the `claude` CLI for a cold-context audit pass.

    This is the default dispatcher — it works both standalone and inside an
    agent context, at the cost of a CLI startup per call (~2-3 seconds). The
    calling agent can bypass this function entirely by dispatching the Task
    tool itself, writing the subagent's JSON result to a file, and calling
    audit_note.py with --layer-2-json <path>.

    Design choices:
      - We pipe the prompt via stdin, not via --prompt, because prompts can be
        hundreds of KB (the PDF text dominates) and command-line arg length is
        OS-dependent.
      - We use --print to get non-interactive output.
      - We DO NOT pass --resume or --continue — every invocation must be a
        fresh session with no prompt-cache carryover.
      - stderr is captured separately so we can surface CLI errors to the user
        without polluting the JSON parse.
    """
    if not auditor_model.startswith("claude-"):
        raise RuntimeError(
            "The default Synapse auditor model is now GPT-5.5 and must be run "
            "through an independent Codex external-audit JSON path. To use the "
            "legacy Claude CLI dispatcher, pass an explicit Claude model such "
            "as --auditor-model claude-opus-4-6."
        )

    cmd = ["claude", "--print", "--model", auditor_model]
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            check=False,
            timeout=600,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "`claude` CLI not found on PATH. Either install Claude Code, or run "
            "audit_note.py with --prompt-only and dispatch the Task tool yourself, "
            "or provide an external verdict via --layer-2-json PATH."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"auditor CLI call timed out after 600s: {cmd}"
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"auditor CLI exited with code {result.returncode}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return result.stdout


def validate_external_provenance(provenance: object, expected: dict) -> dict:
    """Validate provenance for externally generated Layer 2 JSON."""
    if not isinstance(provenance, dict):
        raise ValueError("external Layer 2 verdict missing top-level 'provenance' object")

    missing = sorted(EXTERNAL_PROVENANCE_REQUIRED_KEYS - set(provenance))
    if missing:
        raise ValueError(
            "external Layer 2 provenance missing required keys: "
            + ", ".join(missing)
        )

    for key, expected_value in expected.items():
        actual = provenance.get(key)
        if actual != expected_value:
            raise ValueError(
                f"external Layer 2 provenance mismatch for {key}: "
                f"expected {expected_value!r}, got {actual!r}"
            )

    for key in ("auditor_model", "generated_at", "dispatch_mode"):
        if not isinstance(provenance.get(key), str) or not provenance[key].strip():
            raise ValueError(f"external Layer 2 provenance field {key!r} is blank")

    return provenance


def parse_auditor_response(
    raw: str,
    *,
    expected_provenance: dict | None = None,
    require_provenance: bool = False,
    prose_fields: list[str] | None = None,
) -> dict:
    """Defensive JSON parser for the subagent's response.

    The rubric asks for a bare JSON object, but LLMs sometimes wrap it in prose
    or in a ```json``` fence. We try four strategies, in order of strictness:

      1. json.loads on the whole string (fast path: perfectly compliant).
      2. Strip any ```json ... ``` fence and retry.
      3. Regex-find the first top-level `{...}` block that json-parses cleanly.
      4. Give up and raise — the caller surfaces this as an exit-code-2 error.

    After parsing, we validate the shape: `layer_2.overall` must be pass/fail,
    each prose field must be present with a verdict in VERDICT_ENUM and a
    confidence in CONFIDENCE_ENUM. Missing or malformed required fields fail
    closed with exit-code 2 at the caller.
    """
    parsed = None

    # 1. Strict
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 2. Strip a fenced block if present
    if parsed is None:
        stripped = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        stripped = re.sub(r"\s*```$", "", stripped)
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            pass

    # 3. Regex-find the first top-level { ... } block
    if parsed is None:
        # Find the first opening brace and walk to its matching close.
        start = raw.find("{")
        if start != -1:
            depth = 0
            for i in range(start, len(raw)):
                c = raw[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = raw[start : i + 1]
                        try:
                            parsed = json.loads(candidate)
                        except json.JSONDecodeError:
                            pass
                        break

    if parsed is None:
        raise ValueError(
            f"auditor response is not valid JSON. First 200 chars: {raw[:200]!r}"
        )
    if not isinstance(parsed, dict):
        raise ValueError(
            f"auditor response must be a JSON object, got {type(parsed).__name__}"
        )

    provenance = parsed.get("provenance") if isinstance(parsed, dict) else None

    # Shape validation: we expect a top-level "layer_2" key. If the subagent
    # returned the inner structure directly (skipping the wrapper), promote it.
    if "layer_2" not in parsed and "scores" in parsed:
        parsed = {"layer_2": parsed, "provenance": provenance}
    if "layer_2" not in parsed:
        raise ValueError(
            f"auditor response missing 'layer_2' key. Top-level keys: "
            f"{sorted(parsed.keys())}"
        )
    layer_2 = parsed["layer_2"]
    if not isinstance(layer_2, dict) or "scores" not in layer_2:
        raise ValueError("auditor response missing 'layer_2.scores'")

    scores = layer_2["scores"]
    if not isinstance(scores, dict):
        raise ValueError("auditor response 'layer_2.scores' is not an object")
    warnings: list[str] = []
    fields = prose_fields or LAYER_2_PROSE_FIELDS
    for field in fields:
        if field not in scores:
            raise ValueError(f"auditor omitted required Layer 2 field {field!r}")
        v = scores[field]
        if not isinstance(v, dict):
            raise ValueError(f"auditor verdict for {field!r} is not an object")
        if v.get("verdict") not in VERDICT_ENUM:
            raise ValueError(
                f"{field!r} has invalid verdict {v.get('verdict')!r}"
            )
        if v.get("confidence") not in CONFIDENCE_ENUM:
            raise ValueError(
                f"{field!r} has invalid confidence {v.get('confidence')!r}"
            )
        v.setdefault("evidence_page_hint", None)
        v.setdefault("note", "")

    if require_provenance:
        provenance = validate_external_provenance(
            provenance,
            expected_provenance or {},
        )

    # Recompute overall from verdicts to defend against an auditor that lies
    # about its own top-level field.
    fail_verdicts = {"UNSUPPORTED", "CONTRADICTED"}
    has_fail = any(scores[f]["verdict"] in fail_verdicts for f in fields)
    layer_2["overall"] = "fail" if has_fail else "pass"

    return {
        "layer_2": layer_2,
        "parse_warnings": warnings,
        "provenance": provenance if isinstance(provenance, dict) else None,
    }


# --- audit report assembly ---------------------------------------------------------


def combine_audit_result(
    paper_id: str,
    layer_1: dict,
    layer_2: dict | None,
    auditor_model: str,
    rubric_version: str = RUBRIC_VERSION,
    note_sha256: str | None = None,
    text_sha256: str | None = None,
    audit_context: dict | None = None,
) -> dict:
    """Merge Layer 1 and Layer 2 results into the canonical audit JSON shape."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if layer_2 is None:
        layer_2_block = {
            "overall": "skipped",
            "scores": {},
        }
    else:
        layer_2_block = layer_2["layer_2"]

    # Collect all flagged claims for quick human triage — both Layer 1 anchor
    # failures and Layer 2 UNSUPPORTED/CONTRADICTED verdicts.
    flagged: list[dict] = []
    for err in layer_1["anchors_not_found_in_pdf"]:
        flagged.append({"layer": 1, "kind": "anchor_not_in_pdf", "detail": err})
    for err in layer_1["anchors_missing"]:
        flagged.append({"layer": 1, "kind": "anchor_missing", "detail": err})
    if layer_2 is not None:
        for field, v in layer_2_block.get("scores", {}).items():
            if v.get("verdict") in {"UNSUPPORTED", "CONTRADICTED"}:
                flagged.append(
                    {
                        "layer": 2,
                        "kind": v["verdict"].lower(),
                        "field": field,
                        "detail": v.get("note", ""),
                    }
                )

    overall = "pass"
    if layer_1["overall"] == "fail":
        overall = "fail"
    elif layer_2 is not None and layer_2_block.get("overall") == "fail":
        overall = "fail"

    return {
        "paper_id": paper_id,
        "audit_version": AUDIT_VERSION,
        "audited_at": now,
        "auditor_model": auditor_model,
        "rubric_version": rubric_version,
        "input_hashes": {
            "note_sha256": note_sha256,
            "text_sha256": text_sha256,
        },
        "audit_context": audit_context or {},
        "layer_1": layer_1,
        "layer_2": layer_2_block,
        "layer_2_provenance": (layer_2 or {}).get("provenance"),
        "overall": overall,
        "flagged_claims": flagged,
        "parse_warnings": (layer_2 or {}).get("parse_warnings", []),
    }


def write_audit_report(paper_id: str, report: dict) -> Path:
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    path = AUDITS_DIR / f"{paper_id}.audit.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_flag_reason(paper_id: str, report: dict) -> Path:
    FLAGGED_DIR.mkdir(parents=True, exist_ok=True)
    path = FLAGGED_DIR / f"{paper_id}.reason.txt"
    lines: list[str] = []
    lines.append(f"AUDIT FAILED — {paper_id}")
    lines.append(f"audited_at: {report['audited_at']}")
    lines.append(f"auditor_model: {report['auditor_model']}")
    lines.append("")
    lines.append(f"Layer 1 ({report['layer_1']['overall']}): "
                 f"{report['layer_1']['anchors_checked']} anchors checked")
    for err in report["layer_1"].get("anchors_missing", []):
        lines.append(f"  - missing: {err}")
    for err in report["layer_1"].get("anchors_not_found_in_pdf", []):
        lines.append(f"  - fabricated: {err}")
    for err in report["layer_1"].get("other_errors", []):
        lines.append(f"  - other: {err}")
    lines.append("")
    l2 = report["layer_2"]
    lines.append(f"Layer 2 ({l2.get('overall', 'skipped')}):")
    for field, v in (l2.get("scores") or {}).items():
        if v.get("verdict") in {"UNSUPPORTED", "CONTRADICTED", "PARTIAL"}:
            lines.append(
                f"  - {field}: {v['verdict']} ({v.get('confidence', '?')}) "
                f"— {v.get('note', '')}"
            )
    lines.append("")
    lines.append("See the full audit report at:")
    lines.append(f"  incoming/_audits/{paper_id}.audit.json")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --- main --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Two-layer faithfulness audit for a Synapse note.",
    )
    parser.add_argument("note", type=Path, help="path to notes/<paper_id>.md")
    parser.add_argument("--flag", action="store_true",
                        help="on fail, write incoming/_flagged/<id>.reason.txt")
    parser.add_argument("--dry-run", action="store_true",
                        help="compute audit but do not write JSON report or flag sidecar")
    parser.add_argument("--skip-layer-2", action="store_true",
                        help="run Layer 1 only; no subagent dispatch")
    parser.add_argument("--prompt-only", action="store_true",
                        help="print the Layer 2 prompt to stdout and exit")
    parser.add_argument("--layer-2-json", type=Path, default=None,
                        help="read Layer 2 verdict from this JSON file instead of dispatching")
    parser.add_argument("--force-layer-2", action="store_true",
                        help="run Layer 2 even if Layer 1 failed (debugging only)")
    parser.add_argument("--auditor-model", default=DEFAULT_AUDITOR_MODEL,
                        help=f"auditor model (default: {DEFAULT_AUDITOR_MODEL})")
    args = parser.parse_args()

    note_path = args.note.resolve()
    try:
        fm, body, _ = load_note(note_path)
        note_raw = note_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"ERROR loading note: {exc}", file=sys.stderr)
        return 2

    paper_id = fm.get("id", args.note.stem)
    paper_type = fm.get("paper_type", "")
    prose_fields = prose_fields_for(fm.get("extraction_version"))
    note_digest = sha256_text(note_raw)
    text_digest: str | None = None
    audit_context: dict | None = None

    # --prompt-only: build the prompt, print it, exit. No Layer 1 run.
    if args.prompt_only:
        try:
            pdf_text = load_pdf_text(fm)
            rubric_text = load_rubric()
        except Exception as exc:
            print(f"ERROR preparing prompt: {exc}", file=sys.stderr)
            return 2
        print(
            build_auditor_prompt(
                paper_id,
                paper_type,
                body,
                pdf_text,
                rubric_text,
                anchors=anchor_quotes(fm),
            )
        )
        return 0

    # Layer 1.
    layer_1 = run_layer_1(fm)
    print(f"Layer 1: {layer_1['overall']} "
          f"({layer_1['anchors_checked']} anchors checked)")
    for err in layer_1["anchors_missing"]:
        print(f"  - missing: {err}")
    for err in layer_1["anchors_not_found_in_pdf"]:
        print(f"  - fabricated: {err}")
    for err in layer_1["other_errors"]:
        print(f"  - other: {err}")

    layer_2_result: dict | None = None
    effective_auditor_model = args.auditor_model

    # Short-circuit: skip Layer 2 if Layer 1 failed (unless --force-layer-2)
    if layer_1["overall"] == "fail" and not args.force_layer_2:
        print("Layer 2: skipped (Layer 1 failed; use --force-layer-2 to override)")
    elif args.skip_layer_2:
        print("Layer 2: skipped (--skip-layer-2)")
    elif args.layer_2_json is not None:
        # External verdict path — the calling agent already dispatched the Task
        # tool and wrote the result to disk. We read and validate it.
        try:
            pdf_text = load_pdf_text(fm)
            text_digest = sha256_text(pdf_text)
            _, audit_context = fit_pdf_text_for_audit(
                pdf_text, anchors=anchor_quotes(fm)
            )
            expected_provenance = {
                "paper_id": paper_id,
                "note_sha256": note_digest,
                "text_sha256": text_digest,
                "rubric_version": RUBRIC_VERSION,
            }
            raw = args.layer_2_json.read_text(encoding="utf-8")
            layer_2_result = parse_auditor_response(
                raw,
                expected_provenance=expected_provenance,
                require_provenance=True,
                prose_fields=prose_fields,
            )
            effective_auditor_model = (
                layer_2_result.get("provenance", {}).get("auditor_model")
                or args.auditor_model
            )
            print(f"Layer 2: {layer_2_result['layer_2']['overall']} "
                  f"(external verdict from {args.layer_2_json})")
        except Exception as exc:
            print(f"ERROR reading external Layer 2 verdict: {exc}", file=sys.stderr)
            return 2
    else:
        # Default path: shell out to the `claude` CLI for a fresh-context audit.
        try:
            pdf_text = load_pdf_text(fm)
            text_digest = sha256_text(pdf_text)
            rubric_text = load_rubric()
            prompt, audit_context = build_auditor_prompt_and_context(
                paper_id,
                paper_type,
                body,
                pdf_text,
                rubric_text,
                anchors=anchor_quotes(fm),
            )
            raw = dispatch_auditor_via_cli(prompt, args.auditor_model)
            layer_2_result = parse_auditor_response(raw, prose_fields=prose_fields)
            print(f"Layer 2: {layer_2_result['layer_2']['overall']}")
            for field, v in layer_2_result["layer_2"].get("scores", {}).items():
                marker = "  "
                if v.get("verdict") in {"UNSUPPORTED", "CONTRADICTED"}:
                    marker = "!!"
                elif v.get("verdict") == "PARTIAL":
                    marker = " ~"
                print(f"{marker} {field}: {v.get('verdict')} ({v.get('confidence')})")
        except Exception as exc:
            print(f"ERROR during Layer 2 dispatch: {exc}", file=sys.stderr)
            return 2

    # Assemble and (optionally) write.
    report = combine_audit_result(
        paper_id=paper_id,
        layer_1=layer_1,
        layer_2=layer_2_result,
        auditor_model=effective_auditor_model,
        note_sha256=note_digest,
        text_sha256=text_digest,
        audit_context=audit_context,
    )

    if not args.dry_run:
        path = write_audit_report(paper_id, report)
        print(f"audit report: {path.relative_to(SYNAPSE_ROOT)}")

    if report["overall"] == "fail":
        if args.flag and not args.dry_run:
            reason_path = write_flag_reason(paper_id, report)
            print(f"flagged: {reason_path.relative_to(SYNAPSE_ROOT)}")
        print(f"OVERALL: FAIL ({len(report['flagged_claims'])} flagged claims)")
        return 1

    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
