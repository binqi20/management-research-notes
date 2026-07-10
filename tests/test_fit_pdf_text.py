#!/usr/bin/env python3
"""Unit tests for the anchor-aware audit sandwich (tools/audit_note.py).

Covers the v0.31.0 upgrade: membership-first anchor location, chunk-scan of the
dropped middle, straddle and stripped-References fallbacks, window merge +
budget cap, marker/coalescing rules, and the legacy byte-identical regression
pin. Pure functions only — no network, no repo data.

Run directly (no framework needed):
    python3 tests/test_fit_pdf_text.py
or via pytest:
    python3 -m pytest tests/test_fit_pdf_text.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from audit_note import (  # noqa: E402
    SANDWICH_HEAD_RATIO,
    SANDWICH_SEPARATOR_RESERVE,
    SPLICE_TOTAL_BUDGET_CHARS,
    build_auditor_prompt_and_context,
    fit_pdf_text_for_audit,
)
from validate_note import normalize_ws  # noqa: E402

# Small budget so tests run fast; the machinery is budget-agnostic.
MAX = 20_000


def geometry(max_chars: int = MAX) -> tuple[int, int]:
    available = max_chars - SANDWICH_SEPARATOR_RESERVE
    head = int(available * SANDWICH_HEAD_RATIO)
    return head, available - head


def filler(n: int, seed: str = "w") -> str:
    """Deterministic unique-token filler with no accidental anchor matches."""
    parts: list[str] = []
    total = 0
    i = 0
    while total < n:
        tok = f"{seed}{i} "
        parts.append(tok)
        total += len(tok)
        i += 1
    return "".join(parts)[:n]


def with_inserts(base: str, inserts: dict[int, str]) -> str:
    """Insert sentinel strings at approximate positions (descending order)."""
    text = base
    for pos in sorted(inserts, reverse=True):
        text = text[:pos] + inserts[pos] + text[pos:]
    return text


def legacy_pin(stripped: str, max_chars: int = MAX) -> str:
    """The pre-splice sandwich output, computed independently of audit_note."""
    head, tail = geometry(max_chars)
    dropped = len(stripped) - head - tail
    sep = f"\n\n[... middle of paper truncated ({dropped:,} chars dropped) ...]\n\n"
    return stripped[:head] + sep + stripped[-tail:]


# ---- tests -------------------------------------------------------------------------


def test_under_budget_passthrough():
    text = filler(10_000)
    anchor = "SENTINEL under budget anchor"
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert fitted == text, "under-budget text must pass through unchanged"
    assert ctx["sandwich_truncated"] is False
    assert ctx["windows_spliced"] == 0 and ctx["spliced_chars"] == 0
    assert ctx["fitted_pdf_chars"] == len(text)


def test_legacy_regression_pin_no_anchors():
    text = filler(50_000)
    for anchors in (None, []):
        fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=anchors)
        assert fitted == legacy_pin(text), "no-anchor output must be byte-identical to the legacy sandwich"
        assert ctx["sandwich_truncated"] is True
        assert ctx["windows_spliced"] == 0


def test_head_anchor_no_splice():
    anchor = "ALPHA head resident anchor phrase"
    text = with_inserts(filler(50_000), {5_000: anchor})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["anchors_in_head_tail"] == 1
    assert ctx["windows_spliced"] == 0
    assert fitted == legacy_pin(text), "head-resident anchor must not trigger splicing"


def test_middle_anchor_spliced():
    anchor = "ZEBRA quantum finding beta gamma delta"
    text = with_inserts(filler(50_000), {25_000: anchor})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["anchors_in_dropped_middle"] == 1
    assert ctx["windows_spliced"] == 1
    assert ctx["spliced_chars"] > 0
    assert normalize_ws(anchor) in normalize_ws(fitted), "spliced anchor must survive in fitted text"
    assert "resuming at evidence-anchor context" in fitted
    assert "chars dropped ...]" in fitted


def test_straddle_anchor_at_head_cut():
    head, _ = geometry()
    anchor = "STRADDLE anchor spanning the head cut boundary exactly here"
    text = with_inserts(filler(50_000), {head - 30: anchor})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["anchors_in_dropped_middle"] == 1, "straddle anchor must be located via full-scan fallback"
    assert ctx["windows_spliced"] == 1
    assert normalize_ws(anchor) in normalize_ws(fitted), (
        "window must coalesce with head so the straddled anchor is contiguous again"
    )
    assert "resuming at evidence-anchor context" not in fitted, (
        "no marker may be interposed between head and a head-adjacent window"
    )


def test_nearby_anchors_merge():
    a1 = "MERGE first anchor token stream"
    a2 = "MERGE second anchor token stream"
    text = with_inserts(filler(50_000), {25_000: a1, 26_500: a2})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[a1, a2])
    assert ctx["anchors_in_dropped_middle"] == 2
    assert ctx["windows_spliced"] == 1, "overlapping windows must merge"
    assert normalize_ws(a1) in normalize_ws(fitted)
    assert normalize_ws(a2) in normalize_ws(fitted)


def test_duplicate_anchor_one_window():
    anchor = "DUPLICATE anchor appearing twice mid paper"
    text = with_inserts(filler(50_000), {25_000: anchor, 35_000: anchor})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor, anchor])
    assert ctx["windows_spliced"] == 1, "same anchor text must yield a single window"
    assert normalize_ws(anchor) in normalize_ws(fitted)


def test_refs_tail_anchor():
    anchor = "APPENDIX robustness anchor rho sigma tau"
    body = filler(60_000)
    refs = with_inserts(filler(20_000, seed="r"), {10_000: anchor})
    text = body + "\nReferences\n" + refs
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["references_removed_chars"] > 0, "test setup: references must be stripped"
    assert ctx["anchors_in_stripped_refs"] == 1
    assert "spliced from the removed references/appendix section" in fitted
    assert normalize_ws(anchor) in normalize_ws(fitted)


def test_prose_line_initial_references_not_stripped():
    # AMJ 57(1) Koerner bug class: a sentence beginning "References to ..."
    # at the start of a line in the back half must not be mistaken for the
    # REFERENCES heading. (In the real paper this cut 67,575 chars — the
    # entire Discussion — out of the audit prompt.)
    prose = "\n   References to relationships appeared in 93 percent of accounts\n"
    text = with_inserts(filler(60_000), {45_000: prose})
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["references_removed_chars"] == 0, (
        "line-initial prose 'References to ...' must not trigger the strip"
    )


def test_reference_note_line_not_last_match():
    # Meta-analysis convention: the references section opens with a note like
    # "References marked with an asterisk indicate ...". The last-match rule
    # must land on the true heading above it, not on the prose note below it.
    text = (
        filler(60_000)
        + "\n\nREFERENCES\n"
        + filler(2_000, seed="R")
        + "\nReferences marked with an asterisk indicate included studies\n"
        + filler(10_000, seed="S")
    )
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["references_removed_chars"] >= 12_000, (
        "strip must start at the REFERENCES heading, not at the prose note "
        "inside the references section"
    )


def test_heading_sharing_line_with_column_text_strips():
    # Two-column -layout extraction: the heading legitimately shares its
    # physical line with the OTHER column's lowercase text, separated by a
    # wide space run (the column gap). This must still strip.
    text = (
        filler(60_000)
        + "\nREFERENCES                                        ecological approach to management\n"
        + filler(15_000, seed="R")
    )
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["references_removed_chars"] >= 15_000, (
        "a wide space run after the heading is a column gap, not prose — "
        "the heading must still be recognized"
    )


def test_budget_overflow_deterministic():
    sentinels = [f"OVERFLOW anchor number {i} unique payload" for i in range(4)]
    positions = {20_000: sentinels[0], 32_000: sentinels[1],
                 44_000: sentinels[2], 56_000: sentinels[3]}
    text = with_inserts(filler(80_000), positions)
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=sentinels)
    assert ctx["spliced_chars"] <= SPLICE_TOTAL_BUDGET_CHARS
    assert ctx["windows_dropped_over_budget"] == 1
    assert ctx["windows_spliced"] == 3
    for kept in sentinels[:3]:
        assert normalize_ws(kept) in normalize_ws(fitted), "kept windows are the earliest by offset"
    assert normalize_ws(sentinels[3]) not in normalize_ws(fitted), "over-budget window must be dropped"
    # Determinism: identical call → identical drop decision.
    fitted2, ctx2 = fit_pdf_text_for_audit(text, MAX, anchors=sentinels)
    assert fitted2 == fitted and ctx2 == ctx


def test_long_anchor_dynamic_overlap():
    anchor = "LONGANCHOR " + " ".join(f"lw{i}" for i in range(39))  # 40 words, > 25-word cap
    assert len(anchor.split()) == 40
    text = with_inserts(filler(50_000), {25_000: anchor})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["windows_spliced"] == 1, "over-cap-length anchor must still be located (dynamic overlap)"
    assert normalize_ws(anchor) in normalize_ws(fitted)


def test_hyphenated_linewrap_match():
    embedded = "ZEBRA effi-\nciency HYDRA gamma marker"
    anchor = "ZEBRA efficiency HYDRA gamma marker"
    text = with_inserts(filler(50_000), {25_000: embedded})
    fitted, ctx = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert ctx["anchors_in_dropped_middle"] == 1, "line-wrap hyphenation must not defeat the scan"
    assert normalize_ws(anchor) in normalize_ws(fitted)


def test_determinism_and_prompt_path_context_equality():
    anchor = "EQUALITY anchor for path comparison"
    text = with_inserts(filler(50_000), {25_000: anchor})
    fitted1, ctx1 = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    fitted2, ctx2 = fit_pdf_text_for_audit(text, MAX, anchors=[anchor])
    assert fitted1 == fitted2 and ctx1 == ctx2
    # The prompt-build path must record the SAME audit_context the assembly
    # path computes — this is the provenance-coherence guarantee.
    _prompt, ctx3 = build_auditor_prompt_and_context(
        "test-paper", "empirical-quantitative", "note body", text, "RUBRIC",
        max_pdf_chars=MAX, anchors=[anchor],
    )
    assert ctx3 == ctx1


# ---- runner ------------------------------------------------------------------------


def main() -> int:
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    failures = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {name}: {exc}")
        except Exception as exc:  # noqa: BLE001 — surface unexpected errors per-test
            failures += 1
            print(f"ERROR {name}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
