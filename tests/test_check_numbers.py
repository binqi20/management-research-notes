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
