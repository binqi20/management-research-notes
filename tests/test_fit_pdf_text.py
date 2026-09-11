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
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from audit_note import (  # noqa: E402
    SANDWICH_HEAD_RATIO,
    SANDWICH_SEPARATOR_RESERVE,
    SPLICE_TOTAL_BUDGET_CHARS,
    _strip_references,
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


def test_appendix_retained_under_budget():
    # Batches 09-10 (hersel, lauriano, xu-2022): appendix-sourced claims drew
    # PARTIALs because the reference strip dropped the appendix. The fitter
    # must now re-append it after the removed references block.
    body = filler(10_000)
    refs = filler(6_000, seed="r")
    app = "SENTINEL appendix robustness content " + filler(1_000, seed="a")
    text = body + "\nREFERENCES\n" + refs + "\nAPPENDIX A\n" + app
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert "SENTINEL appendix robustness content" in fitted
    assert "appendix retained below" in fitted
    assert "r100 " not in fitted, "references block must still be stripped"
    assert ctx["appendix_retained_chars"] > 0
    assert 0 < ctx["references_removed_chars"] <= len(refs) + 40
    assert ctx["sandwich_truncated"] is False


def test_appendix_retained_over_budget():
    body = filler(50_000)
    refs = filler(4_000, seed="r")
    app = "APPSENT robustness beta " + filler(2_000, seed="b")
    text = body + "\nREFERENCES\n" + refs + "\nAPPENDIX B\n" + app
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["sandwich_truncated"] is True
    assert "APPSENT robustness beta" in fitted
    assert "appendix retained below" in fitted
    assert "[... middle of paper truncated" in fitted
    assert len(fitted) <= MAX, "appendix retention must not blow the budget"
    assert ctx["appendix_retained_chars"] > 0


def test_table_a_marker_starts_appendix():
    # AMJ appendices that are bare tables open with "TABLE A1", no APPENDIX
    # heading (the lauriano case).
    body = filler(12_000)
    refs = filler(4_000, seed="r")
    app = "TASENT tabled robustness " + filler(500, seed="t")
    text = body + "\nREFERENCES\n" + refs + "\nTABLE A1  Robustness checks\n" + app
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert "TASENT tabled robustness" in fitted
    assert ctx["appendix_retained_chars"] > 0


def test_prose_appendix_mention_not_marker():
    # A reference-section prose line mentioning an appendix must not start
    # retention: title-case "Appendix" requires an A-Z/0-9 designator.
    body = filler(12_000)
    text = (
        body
        + "\nREFERENCES\n"
        + filler(2_000, seed="r")
        + "\nAppendix materials are available from the authors upon request\n"
        + filler(2_000, seed="s")
    )
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["appendix_retained_chars"] == 0
    assert "materials are available" not in fitted
    assert fitted == body.rstrip(), "no retention -> plain stripped body"


def test_suspicious_strip_flagged():
    # Batch 11 (ferns/pamphile): a real REFERENCES heading atop column 2 can
    # leave column-1 Discussion prose inside the stripped region. The fitter
    # can't yet fix the cut, but it must flag a strip that removes an
    # unusually large share of the paper.
    body = filler(36_000)
    refs = filler(24_000, seed="r")  # 40% of the text — far past the threshold
    text = body + "\nREFERENCES\n" + refs
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["references_strip_suspicious"] is True
    assert ctx["references_strip_ratio"] > 0.35


def test_normal_strip_not_suspicious():
    body = filler(50_000)
    refs = filler(5_000, seed="r")  # ~9% — a normal reference list
    text = body + "\nREFERENCES\n" + refs
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["references_strip_suspicious"] is False
    assert 0 < ctx["references_strip_ratio"] < 0.15


def test_suspicious_strip_warns_auditor():
    body = filler(36_000)
    refs = filler(24_000, seed="r")
    text = body + "\nREFERENCES\n" + refs
    prompt, ctx = build_auditor_prompt_and_context(
        "test-paper", "empirical-quantitative", "note body", text, "rubric text", MAX
    )
    assert ctx["references_strip_suspicious"] is True
    assert "suspected strip loss" in prompt, (
        "auditor preamble must carry the suspicious-strip caution"
    )


def reference_rows() -> str:
    # Synthetic bibliography around short source-derived layout fixtures.
    return "".join(
        f"{name}, A. 2015. A reference title.                              Smith, B. 2016. Another title.\n"
        "    Journal of Research, 1: 1–10.                                   Journal of Research, 2: 11–20.\n"
        for name in ("Adams", "Baker", "Clark", "Davis")
    )


def test_real_ferns_interleaved_band_stays_prefix_pure():
    # Ferns (2022), raw lines 1291–1318: right heading, then left prose.
    band = (
        "\n                                                                                       REFERENCES\n"
        "industry also challenged activists’ analogical work,              350.org. 2012. Do the math.\n"
        "particularly by attacking activists’ moral positioning               Retrieved from a reference.\n"
        "proliferate.                                                      350.org. 2015. Another reference.\n"
    )
    text = filler(10_000) + band + reference_rows()
    stripped, removed = _strip_references(text)
    assert stripped == (filler(10_000) + band).rstrip()
    assert text.startswith(stripped) and removed == len(text) - len(stripped)
    assert "industry also challenged activists’ analogical work" in stripped
    assert "Adams, A." not in stripped


def test_real_kim_interleaved_band_below_caution_threshold():
    # Kim (2015), raw lines 1165–1174. Below-15% bands are the same defect.
    band = (
        "\n                                                                                     REFERENCES\n"
        "expect (expectations) (Cyert & March, 1963). Several               Aiken, L. S. 1991. A reference.\n"
        "the role of both aspirations and expectations could                  Reference continuation.\n"
        "add valuable insights to the performance feedback                    Reference continuation.\n"
    )
    text = filler(15_000) + band + reference_rows()
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert "the role of both aspirations and expectations could" in fitted
    assert ctx["references_strip_suspicious"] is False
    assert 0 < ctx["references_strip_ratio"] < 0.15


def test_single_column_reference_heading_keeps_original_cut():
    text = filler(10_000) + "\n\nREFERENCES\n" + reference_rows()
    stripped, removed = _strip_references(text)
    assert stripped == filler(10_000).rstrip()
    assert removed == len(text) - len(stripped)


def test_right_column_without_reference_transition_uses_old_cut():
    text = (
        filler(10_000)
        + "\n                                                                                       REFERENCES\n"
        + "The discussion continues and gives no reliable cut.              A right-column fragment.\n"
    )
    stripped, removed = _strip_references(text)
    assert stripped == filler(10_000).rstrip()
    assert removed == len(text) - len(stripped)


def test_real_eggers_right_column_appendix_precedes_table_marker():
    # Eggers (2015), lines 1093, 1115, 1117, 1123. The former TABLE A1
    # fallback omitted these methods facts above the table.
    text = (
        filler(10_000) + "\nREFERENCES\n" + reference_rows()
        + "       and mode of organizing. Entrepreneurship Theory                                          APPENDIX A\n"
        + "cover all VC-backed ventures through 2009\n"
        + "before 2006\nwe use six industry\n"
        + "\nTABLE A1\nTable contents.\n"
    )
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    for phrase in ("cover all VC-backed ventures through 2009", "before 2006", "we use six industry"):
        assert phrase in fitted
    assert "APPENDIX A" in fitted and "TABLE A1" in fitted
    assert ctx["appendix_truncated_chars"] == 0 and len(fitted) <= MAX


def test_real_reyt_numeric_right_column_appendix():
    # Reyt (2015), line 1193: numeric marker alongside a reference.
    text = (
        filler(10_000) + "\nREFERENCES\n" + reference_rows()
        + "    think they’re doing? Action identification and human                                     APPENDIX 1\n"
        + "Appendix methods content.\n"
    )
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert "APPENDIX 1" in fitted and "Appendix methods content." in fitted
    assert ctx["appendix_retained_chars"] > 0


def test_inline_appendix_prose_does_not_start_retention():
    text = (
        filler(10_000) + "\nREFERENCES\n" + reference_rows()
        + "A reference mentions APPENDIX A in running prose.\n"
        + "Another reference.       APPENDIX materials are elsewhere.\n"
    )
    _fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert ctx["appendix_retained_chars"] == 0


def test_real_moy_indented_reference_transition():
    # Raw 982–1004: left margin 117, right heading 223; bibliography in the
    # left column starts at Alting, after the interleaved body continuation.
    fixture = (ROOT / "tests/fixtures/audit_fitter/moy_indented_references.txt").read_text()
    text = filler(30_000) + "\n" + fixture
    start = text.index("Alting, T.")
    cut = text.rfind("\n", 0, start)
    stripped, removed = _strip_references(text)
    assert stripped == text[:cut].rstrip()
    assert "highlight some factors that may mitigate this concern" in stripped
    assert removed == len(text) - len(stripped)


def test_real_zhang_appendix_over_40k_retained_whole():
    layout = json.loads((ROOT / "tests/fixtures/audit_fitter/zhang_appendix_layout.json").read_text())
    # Preserve the real marker geometry and measured lengths, replacing
    # unneeded article content with deterministic filler.
    app = "\n" + layout["first_marker"] + "\n"
    app += filler(layout["first_to_old_marker_chars"] - len(app), seed="z")
    app += "\n" + layout["old_marker"] + "\n"
    app += filler(layout["appendix_chars"] - len(app) - len(layout["tail_fragment"]), seed="t")
    app += layout["tail_fragment"]
    assert len(app) == 45_399
    text = filler(100_000) + "\nREFERENCES\n" + reference_rows() + app
    fitted, ctx = fit_pdf_text_for_audit(text)
    assert app in fitted
    assert ctx["appendix_retained_chars"] == 45_399
    assert ctx["appendix_truncated_chars"] == 0
    assert layout["tail_fragment"] in fitted


def test_real_sherf_titled_appendix_heading():
    fixture = (ROOT / "tests/fixtures/audit_fitter/sherf_titled_appendix.txt").read_text()
    probes = "The final sample included 202\nThe final sample included 263 managers"
    text = filler(20_000) + "\nREFERENCES\n" + reference_rows() + "\n" + fixture + probes
    for separator in (":", "-", "."):
        fitted, ctx = fit_pdf_text_for_audit(text.replace("A: PILOT", f"A{separator} PILOT"))
        assert probes in fitted
        assert ctx["appendix_retained_chars"] > 0


def test_real_lee_single_column_references():
    fixture = (ROOT / "tests/fixtures/audit_fitter/lee_single_column.txt").read_text()
    text = filler(10_000) + "\n" + fixture
    expected = text[:text.index("\nREFERENCES")].rstrip()
    stripped, removed = _strip_references(text)
    assert stripped == expected
    assert "00018392261421927#supplementary-materials" in stripped
    assert "Abi-Esber" not in stripped
    assert removed == len(text) - len(stripped)


def test_real_simsek_terminal_mixed_band_within_budget():
    fixture = (ROOT / "tests/fixtures/audit_fitter/simsek_terminal_band.txt").read_text()
    text = filler(10_000) + "\n" + fixture
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert fitted == text
    assert "tools, and techniques are needed for probing and" in fitted
    assert ctx["sandwich_truncated"] is False
    assert _strip_references(text, MAX) == (text, 0)


def test_terminal_band_over_budget_uses_old_heading_cut():
    fixture = (ROOT / "tests/fixtures/audit_fitter/simsek_terminal_band.txt").read_text()
    body = filler(18_000)
    text = body + "\n" + fixture
    assert len(text) > MAX
    stripped, removed = _strip_references(text, MAX)
    assert stripped == body.rstrip()
    assert removed == len(text) - len(stripped)
    fitted, ctx = fit_pdf_text_for_audit(text, MAX)
    assert fitted == stripped
    assert ctx["sandwich_truncated"] is False


def test_terminal_exception_rejects_right_column_only_ending():
    fixture = (ROOT / "tests/fixtures/audit_fitter/simsek_terminal_band.txt").read_text()
    body = filler(10_000)
    right_only = " " * 70 + "Zhang, A. 2020. A reference-only final line.\n"
    text = body + "\n" + fixture + "\n" + right_only * 10
    assert len(text) < MAX
    stripped, removed = _strip_references(text, MAX)
    assert stripped == body.rstrip()
    assert removed == len(text) - len(stripped)


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
