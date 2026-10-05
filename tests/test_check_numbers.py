"""Synthetic fixtures only: presence checks must never be semantic verdicts."""
from pathlib import Path
import json
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_numbers as checker


@pytest.fixture
def make_note(tmp_path):
    def make(content, raw, section="Key Findings", extra=""):
        source = tmp_path / "source.txt"
        source.write_text(raw, encoding="utf-8")
        note = tmp_path / "note.md"
        note.write_text(
            f"---\ntext_path: {json.dumps(str(source))}\n---\n"
            f"**{section}**\n\n{content}\n\n{extra}", encoding="utf-8"
        )
        return note
    return make


def test_thousands_separator_equivalence(make_note):
    report = checker.analyze_note(make_note("N = 1,234 and 2345.", "N=1234; N=2,345.", "Data & Measures"))
    assert [row["hit_count"] for row in report["tokens"]] == [1, 1]
    assert report["totals"] == {"tokens": 2, "tokens_with_hits": 2, "zero_hits": 0}


def test_contextual_pdf_glyphs(make_note):
    report = checker.analyze_note(make_note("b=-0.27, p<.01", "b 5 2.27, p , .01"))
    assert [row["normalized_token"] for row in report["tokens"]] == ["-0.27", "0.01"]
    assert [row["artifact_hit_count"] for row in report["tokens"]] == [1, 1]
    assert not report["zero_hits"]


def test_leading_zero_equivalence(make_note):
    report = checker.analyze_note(make_note("b = 0.27, r = .45", "b=.27; r=0.45"))
    assert [row["hit_count"] for row in report["tokens"]] == [1, 1]


def test_percentages_keep_units(make_note):
    report = checker.analyze_note(make_note("15% responded; 20 percent completed.", "15 % responded, 20% completed; 15 people."))
    assert [row["normalized_token"] for row in report["tokens"]] == ["15%", "20%"]
    assert [row["hit_count"] for row in report["tokens"]] == [1, 1]
    assert checker.analyze_note(make_note("15% responded", "15 people"))["totals"]["zero_hits"] == 1


def test_invented_number_reports_verbatim_clause_and_exit(make_note, capsys):
    note = make_note("The sample included 987 respondents; the effect was positive.", "N = 123")
    report = checker.analyze_note(note)
    assert report["zero_hits"][0]["clause"] == "The sample included 987 respondents;"
    assert checker.main([str(note)]) == 1
    output = capsys.readouterr().out
    assert "Zero-hit tokens" in output
    assert "Key Findings | 987 | The sample included 987 respondents;" in output


def test_citation_years_ignored_but_study_years_retained(make_note):
    note = make_note(
        "Following Smith (1999), Jones et al. (2000), and (Doe & Roe, 2001), "
        "data cover 2010–2012. In 2013, N = 400.",
        "2010 2012 2013 400", "Data & Measures"
    )
    assert [row["token"] for row in checker.analyze_note(note)["tokens"]] == ["2010", "2012", "2013", "400"]


def test_list_labels_dois_and_unselected_sections_ignored(make_note):
    note = make_note(
        "1. H1 predicts an effect.\n2) H2 predicts 25% improvement. "
        "See https://doi.org/10.1234/example.2020.99",
        "25%", "Hypotheses / Propositions",
        "**Theoretical Contribution**\nA separate number 777.\n"
    )
    report = checker.analyze_note(note)
    assert [row["token"] for row in report["tokens"]] == ["25%"]
    assert report["sections_present"] == ["Hypotheses / Propositions"]


def test_no_partial_numeric_matches_or_uncontextualized_minus_repair(make_note):
    report = checker.analyze_note(make_note("27, -0.27, 234, 5", "127 27.5 .27 2.27 1,234 15"))
    assert report["totals"]["zero_hits"] == 4


def test_signs_ranges_thresholds_and_repeated_occurrences(make_note):
    report = checker.analyze_note(make_note("Years 2010-2012; b=−.27; p≤.05; b=+.27; .27 again.", "2010–2012 −0.27 .05 +0.27"))
    assert [r["normalized_token"] for r in report["tokens"]] == ["2010", "2012", "-0.27", "0.05", "0.27", "0.27"]
    assert [r["hit_count"] for r in report["tokens"]] == [1] * 6


def test_signed_literal_not_reinterpreted_as_glyph(make_note):
    report = checker.analyze_note(make_note("b=-.27", "b=2.27; ordinary value 2.27"))
    assert report["totals"]["zero_hits"] == 1


def test_json_cli_and_duplicate_counts(make_note, capsys):
    note = make_note("N=123", "123 participants; 123 responses")
    assert checker.main([str(note), "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["tokens"][0]["hit_count"] == 2
    assert "referent" in report["advisory"]


def test_missing_source_is_input_error(make_note, capsys):
    note = make_note("N=123", "123")
    (note.parent / "source.txt").unlink()
    assert checker.main([str(note)]) == 2
    assert "check_numbers:" in capsys.readouterr().err


def test_relative_source_path_uses_repository_root(make_note, monkeypatch):
    note = make_note("N=123", "123")
    note.write_text("---\ntext_path: source.txt\n---\n**Data & Measures**\nN=123\n", encoding="utf-8")
    monkeypatch.setattr(checker, "SYNAPSE_ROOT", note.parent)
    assert checker.analyze_note(note)["tokens"][0]["hit_count"] == 1


@pytest.mark.parametrize("raw,positive,negative", [
    ("M 5 21.87", "21.87", "-1.87"),
    ("b 5 2.27", "2.27", "-0.27"),
])
def test_ambiguous_minus_glyph_keeps_literal_and_artifact(make_note, raw, positive, negative):
    report = checker.analyze_note(make_note(f"Values {positive} and {negative}.", raw))
    literal, artifact = report["tokens"]
    assert literal["hit_count"] == literal["literal_hit_count"] == 1
    assert literal["artifact_hit_count"] == 0
    assert artifact["hit_count"] == artifact["artifact_hit_count"] == 1
    assert artifact["literal_hit_count"] == 0
    assert not report["zero_hits"]
    assert "heuristic" in report["advisory"]


def test_identical_glyph_and_literal_value_not_double_counted(make_note):
    report = checker.analyze_note(make_note("M=10.18; p<.01", "M 5 10.18, p , .01"))
    assert [row["hit_count"] for row in report["tokens"]] == [1, 1]


@pytest.mark.parametrize("label,value,negative", [
    ("B", "2.17", "-0.17"), ("g", "2.04", "-0.04"),
    ("γ", "2.08", "-0.08"), ("gamma", "2.09", "-0.09"),
    ("estimate", "20.323", "-0.323"), ("effect", "21.25", "-1.25"),
])
def test_new_statistic_glyphs_are_candidates_not_hits(make_note, label, value, negative):
    report = checker.analyze_note(make_note(f"{negative}; {value}", f"{label} 5 {value}"))
    missing, literal = report["tokens"]
    assert missing["hit_count"] == 0
    assert missing["requires_raw_verification"] is True
    assert report["totals"]["zero_hits"] == 1
    assert literal["literal_hit_count"] == 1
    candidate, = missing["candidates"]
    assert candidate["statistic_label"] == label
    assert candidate["reasons"] == ["minus_as_2", "contextual_statistic"]
    assert candidate["literal_interpretation"] == value
    assert candidate["candidate_interpretation"] == negative
    assert candidate["ambiguous"] and candidate["requires_raw_verification"]


def test_candidate_raw_offsets_lines_and_ci_table_hints(make_note):
    raw = "Unicode α header\n95% CI [2.17, 20.323]\nrow    21    2.17    .04\n"
    report = checker.analyze_note(make_note("-.17; -.323; -1", raw))
    rows = report["tokens"]
    assert report["totals"]["zero_hits"] == 3
    assert [len(row["candidates"]) for row in rows] == [2, 1, 1]
    for row in rows:
        for candidate in row["candidates"]:
            start, end = candidate["raw_start"], candidate["raw_end"]
            assert raw[start:end] == candidate["raw_token"]
            assert candidate["raw_line"] == raw.count("\n", 0, start) + 1
            assert candidate["raw_column"] == start - raw.rfind("\n", 0, start)
            assert candidate["raw_end_line"] == candidate["raw_line"]
    assert "ci_location_hint" in rows[0]["candidates"][0]["reasons"]
    assert "table_location_hint" in rows[0]["candidates"][1]["reasons"]
    assert rows[2]["candidates"][0]["literal_interpretation"] == "21"


@pytest.mark.parametrize("glyph", list(checker.ALTERNATE_MINUS))
def test_alternate_minus_candidates_and_range_safeguard(make_note, glyph):
    raw = f"effect {glyph}.27; years 2010{glyph}2012; CI [{glyph} .40, .20]"
    report = checker.analyze_note(make_note("-.27; -2012; -.40", raw))
    a, year, b = report["tokens"]
    assert report["totals"]["zero_hits"] == 3
    assert a["candidates"][0]["raw_token"] == glyph + ".27"
    assert a["candidates"][0]["reasons"] == ["alternate_minus", "ci_location_hint"]
    assert not year["candidates"]
    assert b["candidates"][0]["raw_token"] == glyph + " .40"


@pytest.mark.parametrize("text,expected", [
    ("Survey, 2007-2015", ["2007", "2015"]),
    ("ProQuest, 2011–2019", ["2011", "2019"]),
    ("Almanac (1857–1921)", ["1857", "1921"]),
    ("Thomson Financial, 1990–2016", ["1990", "2016"]),
    ("Post (2014–2017 = 1)", ["2014", "2017", "1"]),
    ("McKinsey Quarterly, 2012–2014", ["2012", "2014"]),
    ("Survey, 2007 -2015", ["2007", "2015"]),
    ("Survey (2007 — 2015)", ["2007", "2015"]),
])
def test_empirical_source_name_ranges_preserve_both_years(make_note, text, expected):
    report = checker.analyze_note(make_note(text, " ".join(expected), "Data & Measures"))
    assert [row["normalized_token"] for row in report["tokens"]] == expected
    assert not report["zero_hits"]


def test_ordinary_author_citations_stay_masked_beside_ranges(make_note):
    text = "Smith (1999, 2001); Doe & Roe, 2003; Survey, 2007-2015; Jones (2004a)."
    report = checker.analyze_note(make_note(text, "2007 2015"))
    assert [row["normalized_token"] for row in report["tokens"]] == ["2007", "2015"]


def test_positive_two_prefixed_values_never_globally_replaced(make_note):
    report = checker.analyze_note(make_note("2; 21; 20.323; 2.27; 234", "2 21 20.323 2.27 234"))
    assert [r["literal_hit_count"] for r in report["tokens"]] == [1] * 5
    assert all(not r["candidates"] for r in report["tokens"])
    assert all(not r["requires_raw_verification"] for r in report["tokens"])


def test_candidate_numeric_boundaries_units_and_explicit_signs(make_note):
    raw = "12.27 2.275 .227 2.27x x2.27 2,270 2.27% +2.27 https://doi.org/10.1234/2.27"
    report = checker.analyze_note(make_note("-.27", raw))
    assert report["totals"]["zero_hits"] == 1
    assert not report["tokens"][0]["candidates"]
    report = checker.analyze_note(make_note("-.27%", "2.27%"))
    assert report["tokens"][0]["candidates"][0]["candidate_interpretation"] == "-0.27%"
    assert report["tokens"][0]["hit_count"] == 0


def test_legacy_glyph_only_hit_still_requires_raw_verification(make_note):
    report = checker.analyze_note(make_note("-.27; 2.27", "b 5 2.27"))
    glyph, literal = report["tokens"]
    assert glyph["artifact_hit_count"] == 1
    assert glyph["requires_raw_verification"]
    assert glyph["candidates"][0]["reasons"] == ["minus_as_2", "contextual_statistic"]
    assert literal["literal_hit_count"] == 1
    assert not report["zero_hits"]


@pytest.mark.parametrize("raw,negative,positive", [
    ("2010 -2,012", "-2,012", "2,012"),
    ("Year  Net income\n2010 -2012", "-2012", "2012"),
    ("2010 -2012e-3", "-2012e-3", "2012e-3"),
    ("2010 -2012%", "-2012%", "2012%"),
    ("2010\n-2012", "-2012", "2012"),
])
def test_year_shaped_table_values_preserve_source_sign(make_note, raw, negative, positive):
    report = checker.analyze_note(make_note(f"Net income was {negative}; not {positive}.", raw))
    signed, unsigned = report["tokens"]
    assert signed["literal_hit_count"] == signed["hit_count"] == 1
    assert not signed["requires_raw_verification"]
    assert unsigned["hit_count"] == 0
    assert unsigned["requires_raw_verification"]
    assert report["totals"]["zero_hits"] == 1


@pytest.mark.parametrize("content,negative", [
    ("Year  Net income\n2010 -2012", "-2012"),
    ("Survey, 2010 -2,012", "-2012"),
    ("Survey, 2010 -2012e-3", "-2012e-3"),
    ("Survey, 2010 -2012%", "-2012%"),
    ("Years 2010\n-2012", "-2012"),
])
def test_note_range_cue_does_not_erase_signed_non_years(make_note, content, negative):
    report = checker.analyze_note(make_note(content, f"2010 {negative}"))
    signed = report["tokens"][-1]
    assert signed["normalized_token"] == negative
    assert signed["literal_hit_count"] == 1


def test_ambiguous_spaced_source_range_requires_verification(make_note):
    report = checker.analyze_note(make_note("Years 2010 -2012", "2010 -2012"))
    assert [row["normalized_token"] for row in report["tokens"]] == ["2010", "2012"]
    assert report["tokens"][1]["hit_count"] == 0
    assert report["tokens"][1]["requires_raw_verification"]
