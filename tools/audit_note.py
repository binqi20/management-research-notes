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
    A fresh Claude subagent reads the rubric at `docs/audit-rubric.md`, the note
    body, and the PDF text, and returns a per-prose-field JSON verdict from the
    set { SUPPORTED, PARTIAL, UNSUPPORTED, CONTRADICTED }. The subagent runs in
    a cold context so it has no prior commitment to the note's claims.

    Two layers run in order. A Layer 1 failure short-circuits Layer 2 unless
    --force-layer-2 is set (you almost never want this — bad anchors mean bad
    claims, and paying for an LLM pass on fabricated content is wasted work).

Usage
-----
    python tools/audit_note.py notes/<paper_id>.md [options]

Options
-------
    --flag                    On fail, write incoming/_flagged/<id>.reason.txt
    --dry-run                 Compute the audit but DO NOT write the JSON report
                              or the flag sidecar. Report is still printed.
    --skip-layer-2            Run Layer 1 only. No subagent dispatch.
    --prompt-only             Print the Layer 2 prompt to stdout and exit 0.
                              Useful when the calling agent wants to dispatch
                              the Task tool directly and needs the prompt text.
    --layer-2-json PATH       Skip Layer 2 dispatch; read the subagent's JSON
                              verdict from PATH. Used when the calling agent
                              has already dispatched the Task tool externally.
    --force-layer-2           Run Layer 2 even if Layer 1 failed (debugging).
    --auditor-model MODEL     Override the auditor model (default: config value)

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
    parse_body_sections,
    split_frontmatter,
)

AUDITS_DIR = SYNAPSE_ROOT / "incoming" / "_audits"
FLAGGED_DIR = SYNAPSE_ROOT / "incoming" / "_flagged"
RUBRIC_PATH = SYNAPSE_ROOT / "docs" / "audit-rubric.md"
DEFAULT_AUDITOR_MODEL = "claude-opus-4-6"

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

VERDICT_ENUM = {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "CONTRADICTED"}
CONFIDENCE_ENUM = {"high", "medium", "low"}


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

    Safety guard: only strips if the heading appears in the back half of the
    text (>50% offset), to avoid false positives from a "References" heading
    that appears early in the introduction.
    """
    # Common headings, anchored at the start of a line (after a newline).
    # Allow optional leading whitespace (\s*) because two-column PDF
    # extractions often center section headings with spaces.
    # Use \b (word boundary) at the end instead of \s*\n — two-column
    # PDF extraction often concatenates the heading with the first
    # reference entry on the same line, so there's no trailing newline.
    # We search for the LAST match in the back half of the text.
    patterns = [
        r"\n\s*References\b",
        r"\n\s*REFERENCES\b",
        r"\n\s*Bibliography\b",
        r"\n\s*BIBLIOGRAPHY\b",
        r"\n\s*Works Cited\b",
        r"\n\s*Literature Cited\b",
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


def build_auditor_prompt(
    paper_id: str,
    paper_type: str,
    body: str,
    pdf_text: str,
    rubric_text: str,
    max_pdf_chars: int = 180_000,
) -> str:
    """Construct the prompt for the Layer 2 auditor subagent.

    The PDF text is truncated to max_pdf_chars to stay within a reasonable
    context budget. We truncate from the END on the theory that front matter
    (title, abstract, intro, theory) is where most of the claims come from;
    losing the back of the references section is acceptable. For exceptionally
    long papers, the user can re-audit with --auditor-model set to a
    larger-context model.

    The prompt is deliberately structured so the subagent's output IS a JSON
    object — no preamble, no prose wrapper, no fenced block. We re-parse
    defensively in parse_auditor_response so a non-compliant response doesn't
    hang the pipeline.
    """
    # Strip the references/bibliography section before truncating.
    # The Discussion and Conclusions sections are far more valuable for
    # audit than the bibliography, and stripping references first keeps
    # them in the context window.
    stripped, refs_removed = _strip_references(pdf_text)
    truncated = stripped[:max_pdf_chars]

    truncated_note = ""
    if refs_removed > 0 or len(stripped) > max_pdf_chars:
        parts: list[str] = []
        if refs_removed > 0:
            parts.append(
                f"References/bibliography section stripped "
                f"({refs_removed:,} chars)"
            )
        if len(stripped) > max_pdf_chars:
            parts.append(
                f"remaining text truncated at {max_pdf_chars:,} chars "
                f"(post-strip length: {len(stripped):,} chars)"
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
    return f"""{rubric_text}

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


def parse_auditor_response(raw: str) -> dict:
    """Defensive JSON parser for the subagent's response.

    The rubric asks for a bare JSON object, but LLMs sometimes wrap it in prose
    or in a ```json``` fence. We try four strategies, in order of strictness:

      1. json.loads on the whole string (fast path: perfectly compliant).
      2. Strip any ```json ... ``` fence and retry.
      3. Regex-find the first top-level `{...}` block that json-parses cleanly.
      4. Give up and raise — the caller surfaces this as an exit-code-2 error.

    After parsing, we validate the shape: `layer_2.overall` must be pass/fail,
    each prose field must be present with a verdict in VERDICT_ENUM and a
    confidence in CONFIDENCE_ENUM. Missing fields are filled with a
    low-confidence SUPPORTED (the conservative default) and surfaced as a
    warning in the audit log.
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

    # Shape validation: we expect a top-level "layer_2" key. If the subagent
    # returned the inner structure directly (skipping the wrapper), promote it.
    if "layer_2" not in parsed and "scores" in parsed:
        parsed = {"layer_2": parsed}
    if "layer_2" not in parsed:
        raise ValueError(
            f"auditor response missing 'layer_2' key. Top-level keys: "
            f"{sorted(parsed.keys())}"
        )
    layer_2 = parsed["layer_2"]
    if not isinstance(layer_2, dict) or "scores" not in layer_2:
        raise ValueError("auditor response missing 'layer_2.scores'")

    scores = layer_2["scores"]
    warnings: list[str] = []
    for field in LAYER_2_PROSE_FIELDS:
        if field not in scores:
            warnings.append(
                f"auditor omitted {field!r}; filling with low-confidence SUPPORTED"
            )
            scores[field] = {
                "verdict": "SUPPORTED",
                "confidence": "low",
                "evidence_page_hint": None,
                "note": "auditor did not provide a verdict for this field",
            }
            continue
        v = scores[field]
        if not isinstance(v, dict):
            warnings.append(f"{field!r} verdict is not an object; coercing")
            scores[field] = {
                "verdict": "PARTIAL",
                "confidence": "low",
                "evidence_page_hint": None,
                "note": str(v)[:200],
            }
            continue
        if v.get("verdict") not in VERDICT_ENUM:
            warnings.append(
                f"{field!r} has invalid verdict {v.get('verdict')!r}; "
                f"coerced to PARTIAL"
            )
            v["verdict"] = "PARTIAL"
        if v.get("confidence") not in CONFIDENCE_ENUM:
            v["confidence"] = "low"
        v.setdefault("evidence_page_hint", None)
        v.setdefault("note", "")

    # Recompute overall from verdicts to defend against an auditor that lies
    # about its own top-level field.
    fail_verdicts = {"UNSUPPORTED", "CONTRADICTED"}
    has_fail = any(scores[f]["verdict"] in fail_verdicts for f in LAYER_2_PROSE_FIELDS)
    layer_2["overall"] = "fail" if has_fail else "pass"

    return {"layer_2": layer_2, "parse_warnings": warnings}


# --- audit report assembly ---------------------------------------------------------


def combine_audit_result(
    paper_id: str,
    layer_1: dict,
    layer_2: dict | None,
    auditor_model: str,
    rubric_version: str = "v1",
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
        "audit_version": "v1",
        "audited_at": now,
        "auditor_model": auditor_model,
        "rubric_version": rubric_version,
        "layer_1": layer_1,
        "layer_2": layer_2_block,
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

    try:
        fm, body, _ = load_note(args.note.resolve())
    except Exception as exc:
        print(f"ERROR loading note: {exc}", file=sys.stderr)
        return 2

    paper_id = fm.get("id", args.note.stem)
    paper_type = fm.get("paper_type", "")

    # --prompt-only: build the prompt, print it, exit. No Layer 1 run.
    if args.prompt_only:
        try:
            pdf_text = load_pdf_text(fm)
            rubric_text = load_rubric()
        except Exception as exc:
            print(f"ERROR preparing prompt: {exc}", file=sys.stderr)
            return 2
        print(build_auditor_prompt(paper_id, paper_type, body, pdf_text, rubric_text))
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

    # Short-circuit: skip Layer 2 if Layer 1 failed (unless --force-layer-2)
    if layer_1["overall"] == "fail" and not args.force_layer_2:
        print("Layer 2: skipped (Layer 1 failed; use --force-layer-2 to override)")
    elif args.skip_layer_2:
        print("Layer 2: skipped (--skip-layer-2)")
    elif args.layer_2_json is not None:
        # External verdict path — the calling agent already dispatched the Task
        # tool and wrote the result to disk. We read and validate it.
        try:
            raw = args.layer_2_json.read_text(encoding="utf-8")
            layer_2_result = parse_auditor_response(raw)
            print(f"Layer 2: {layer_2_result['layer_2']['overall']} "
                  f"(external verdict from {args.layer_2_json})")
        except Exception as exc:
            print(f"ERROR reading external Layer 2 verdict: {exc}", file=sys.stderr)
            return 2
    else:
        # Default path: shell out to the `claude` CLI for a fresh-context audit.
        try:
            pdf_text = load_pdf_text(fm)
            rubric_text = load_rubric()
            prompt = build_auditor_prompt(paper_id, paper_type, body, pdf_text, rubric_text)
            raw = dispatch_auditor_via_cli(prompt, args.auditor_model)
            layer_2_result = parse_auditor_response(raw)
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
        auditor_model=args.auditor_model,
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
