#!/usr/bin/env python3
"""Unit tests for the v2→v3 augmentation diff-guard (tools/verify_augmentation.py).

Each test builds a synthetic v2 note and an augmented variant, then asserts the
guard's verdict. Pure functions — no git, no repo data, no network.

Run directly:
    python3 tests/test_verify_augmentation.py
or via pytest:
    python3 -m pytest tests/test_verify_augmentation.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from verify_augmentation import verify  # noqa: E402


def v2_note(paper_type: str = "empirical-quantitative", evidence: bool = True) -> str:
    ev = """evidence:
  sample_n: "sample of 83 firms"
  sample_country: "throughout the United States"
  sample_industry: "credit unions located throughout"
  sample_time_period: "collected six months after"
  theories_overview: "integrating engagement theory with"
  methods_overview: "we used regression techniques"
  keywords_source: "collective organizational engagement"
""" if evidence else ""
    return f"""---
id: "test-2015"
title: "A Test Paper"
authors:
  - "Author, A."
year: 2015
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.test"
volume: 58
issue: 1
pages: "1-20"
source: "AMJ/vol-58-no-1"
pdf_path: "library/AMJ/vol-58-no-1/pdfs/test.pdf"
text_path: "library/AMJ/vol-58-no-1/text/test.txt"
ingested_at: "2026-07-05"
extraction_model: "gpt-5.5"
extraction_version: "v2"
paper_type: "{paper_type}"
keywords: ["alpha", "beta"]
theory: ["engagement theory"]
topics: ["hr-practices"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Survey study."
sample:
  industry: "Credit unions"
  country: "United States"
  time_period: "2013"
  units: "firms"
  n: "83"
{ev}---

# A Test Paper

**Abstract**
The abstract text stays byte identical.

**Research Question**
What does the test ask?

**Mechanism Process**
- IV(s): X
- DV(s): Y

The mechanism paragraph.

**Theoretical Contribution**
The contribution.

**Practical Implication**
The implication.

**Limitations**
The limitations.

**Future Research**
The future research.

**APA 7th Citation**
Author, A. (2015). A test paper. *AMJ*, 58(1), 1-20. https://doi.org/10.5465/amj.test
"""


def augment(old: str, *, model: str = "claude-opus-4-8", date: str = "2026-07-12",
            bump: bool = True, add_prov: bool = True, add_anchors: bool = True,
            hyp_after: str = "**Research Question**\nWhat does the test ask?\n",
            new_sections: bool = True, key_findings_empty: bool = False,
            editorial: bool = False) -> str:
    new = old
    if bump:
        new = new.replace('extraction_version: "v2"', 'extraction_version: "v3"')
    if add_prov:
        anchor_line = 'extraction_version: "v3"' if bump else 'extraction_version: "v2"'
        new = new.replace(
            anchor_line,
            anchor_line + f'\naugmented_model: "{model}"\naugmented_at: "{date}"',
        )
    if add_anchors and not editorial:
        new = new.replace(
            '  keywords_source: "collective organizational engagement"\n',
            '  keywords_source: "collective organizational engagement"\n'
            '  hypotheses_source: "Hypothesis 1. X is positively related to Y."\n'
            '  measures_overview: "Y was measured using archival ROA"\n'
            '  findings_overview: "Hypothesis 1 was supported"\n',
        )
    if new_sections:
        kf = "" if key_findings_empty else "H1 supported (b = .30, p < .01)."
        nr = "Not reported in paper"
        hyp = nr if editorial else "H1: X is positively related to Y."
        dm = nr if editorial else "Y = archival ROA; X = five-point Likert scale."
        kf = nr if editorial else kf
        new = new.replace(
            hyp_after,
            hyp_after + f"\n**Hypotheses / Propositions**\n{hyp}\n",
        )
        new = new.replace(
            "The mechanism paragraph.\n",
            "The mechanism paragraph.\n"
            f"\n**Data & Measures**\n{dm}\n"
            f"\n**Key Findings**\n{kf}\n",
        )
    return new


# ---- tests -------------------------------------------------------------------------


def test_correct_augmentation_passes():
    old = v2_note()
    assert verify(old, augment(old)) == []


def test_editorial_frozen_evidence_passes():
    old = v2_note(paper_type="editorial", evidence=False)
    new = augment(old, editorial=True)
    assert verify(old, new) == []


def test_modified_original_section_fails():
    old = v2_note()
    new = augment(old).replace("The contribution.", "A reworded contribution.")
    errs = verify(old, new)
    assert any("Theoretical Contribution" in e and "changed" in e for e in errs), errs


def test_changed_original_anchor_fails():
    old = v2_note()
    new = augment(old).replace('"sample of 83 firms"', '"sample of 84 firms"')
    errs = verify(old, new)
    assert any("sample_n" in e and "changed" in e for e in errs), errs


def test_missing_new_section_fails():
    old = v2_note()
    new = augment(old, new_sections=False)
    errs = verify(old, new)
    assert any("not the canonical v3 order" in e for e in errs), errs


def test_wrong_position_fails():
    old = v2_note()
    # Insert Hypotheses after Mechanism instead of after Research Question.
    new = augment(old, hyp_after="The mechanism paragraph.\n")
    errs = verify(old, new)
    assert any("not the canonical v3 order" in e for e in errs), errs


def test_changed_bib_frontmatter_fails():
    old = v2_note()
    new = augment(old).replace("year: 2015", "year: 2016")
    errs = verify(old, new)
    assert any("'year'" in e and "changed" in e for e in errs), errs


def test_missing_provenance_fails():
    old = v2_note()
    new = augment(old, add_prov=False)
    errs = verify(old, new)
    assert any("augmented_model" in e for e in errs), errs
    assert any("augmented_at" in e for e in errs), errs


def test_bad_date_fails():
    old = v2_note()
    new = augment(old, date="July 12, 2026")
    errs = verify(old, new)
    assert any("augmented_at must be YYYY-MM-DD" in e for e in errs), errs


def test_missing_version_bump_fails():
    old = v2_note()
    new = augment(old, bump=False)
    errs = verify(old, new)
    assert any("expected 'v3'" in e for e in errs), errs


def test_v1_base_rejected():
    old = v2_note().replace('extraction_version: "v2"', 'extraction_version: "v1"')
    new = augment(old)  # bump replace won't fire; provenance anchors on v2 line
    errs = verify(old, new)
    assert any("not 'v2'" in e for e in errs), errs


def test_missing_new_anchor_fails():
    old = v2_note()
    new = augment(old, add_anchors=False)
    errs = verify(old, new)
    assert sum("required v3 evidence anchor missing" in e for e in errs) == 3, errs


def test_empty_new_section_fails():
    old = v2_note()
    new = augment(old, key_findings_empty=True)
    errs = verify(old, new)
    assert any("'Key Findings'" in e and "empty" in e for e in errs), errs


def test_evidence_added_to_editorial_fails():
    old = v2_note(paper_type="editorial", evidence=False)
    new = augment(old, editorial=True)
    new = new.replace(
        "---\n\n# A Test Paper",
        'evidence:\n  hypotheses_source: "Not reported in paper"\n---\n\n# A Test Paper',
        1,
    )
    errs = verify(old, new)
    assert any("must be untouched" in e for e in errs), errs


def test_title_line_change_fails():
    old = v2_note()
    new = augment(old).replace("# A Test Paper", "# A Test Paper (Revised)")
    errs = verify(old, new)
    assert any("pre-heading region" in e for e in errs), errs


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
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"ERROR {name}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
