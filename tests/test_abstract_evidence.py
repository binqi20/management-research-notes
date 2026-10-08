"""Synthetic PDFs only; matching does not substitute for abstract-boundary review."""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import abstract_evidence as evidence
import validate_note as validator


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    fitz = pytest.importorskip("fitz")
    if not shutil.which("pdftotext"):
        pytest.skip("optional pdftotext executable unavailable")
    monkeypatch.setattr(validator, "SYNAPSE_ROOT", tmp_path)
    abstract = "We studied 123 firms. The effect was not significant in small firms."
    pdf = tmp_path / "paper.pdf"
    with fitz.open() as doc:
        page = doc.new_page()
        page.insert_text((40, 50), abstract)
        page.insert_text((40, 150), "Unrelated publication metadata.")
        doc.save(pdf)
    (tmp_path / "raw.txt").write_text("We studied 123 firms. COPYRIGHT\nThe effect was not significant in small firms.")
    fm = {"id": "synthetic", "pdf_path": "paper.pdf", "text_path": "raw.txt"}
    recipe = {"name": "pdftotext-reading-order", "first_page": 1, "last_page": 1}
    text, version = evidence.extract(pdf, recipe)
    record = {
        "schema_version": "pdf-abstract-evidence-v1", "paper_id": fm["id"],
        "pdf_path": fm["pdf_path"], "text_path": fm["text_path"],
        "pdf_sha256": evidence.digest(pdf.read_bytes()),
        "text_sha256": evidence.digest((tmp_path / "raw.txt").read_bytes()),
        "abstract_sha256": evidence.digest(abstract.encode()),
        "extractor": {**recipe, "version": version},
        "derived_text_sha256": evidence.digest(text.encode()),
        "boundary_review": {"complete": True, "reviewer": "test reviewer",
                            "source_location": "page 1", "rationale": "Synthetic complete abstract."},
    }
    path = tmp_path / "evidence.json"

    def run(candidate=abstract, supplied=record):
        path.write_text(json.dumps(supplied))
        errors = []
        validator.check_abstract_verbatim({"Abstract": candidate}, fm, errors, path)
        return errors

    return tmp_path, fm, abstract, record, run


def test_optional_replay_preserves_originals_and_default_failure(bundle):
    root, fm, abstract, record, run = bundle
    before = {p: p.read_bytes() for p in root.iterdir()}
    errors = []
    validator.check_abstract_verbatim({"Abstract": abstract}, fm, errors)
    assert errors
    assert run() == []
    assert all(p.read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize("field", ["paper_id", "pdf_path", "text_path", "pdf_sha256", "text_sha256",
                                    "abstract_sha256", "derived_text_sha256", "schema_version"])
def test_stale_or_wrong_paper_evidence_fails(bundle, field):
    _, _, _, record, run = bundle
    bad = copy.deepcopy(record)
    bad[field] = "wrong"
    assert run(supplied=bad)


@pytest.mark.parametrize("target", ["paper.pdf", "raw.txt"])
def test_mutated_original_source_fails(bundle, target):
    root, _, _, _, run = bundle
    with (root / target).open("ab") as handle:
        handle.write(b"\nchanged")
    assert run()


@pytest.mark.parametrize("change", [lambda s: s.replace("123", "124"),
                                    lambda s: s.replace("not ", ""),
                                    lambda s: s.split(". ")[0] + "."])
def test_changed_abstract_including_shorter_substring_requires_new_review(bundle, change):
    _, _, abstract, _, run = bundle
    assert "abstract changed" in run(candidate=change(abstract))[0]


@pytest.mark.parametrize("change", [lambda s: s.replace("123", "124"),
                                    lambda s: s.replace("123", "-123"),
                                    lambda s: s.replace("not ", "")])
def test_fabricated_content_fails_even_with_rebound_abstract_hash(bundle, change):
    _, _, abstract, record, run = bundle
    changed = change(abstract)
    bad = {**record, "abstract_sha256": evidence.digest(changed.encode())}
    assert "not an exact match" in run(candidate=changed, supplied=bad)[0]


def test_supplied_stale_evidence_fails_even_when_default_would_pass(bundle):
    root, fm, abstract, record, run = bundle
    (root / fm["text_path"]).write_text(abstract)
    errors = []
    validator.check_abstract_verbatim({"Abstract": abstract}, fm, errors)
    assert errors == []
    assert "stale text_sha256" in run()[0]


@pytest.mark.parametrize("recipe_change", [{"version": "wrong"}, {"name": "shell-command"},
                                          {"first_page": True}, {"last_page": 0},
                                          {"command": "do not execute"}])
def test_invalid_or_changed_extractor_fails(bundle, recipe_change):
    _, _, _, record, run = bundle
    bad = copy.deepcopy(record)
    bad["extractor"].update(recipe_change)
    assert run(supplied=bad)


@pytest.mark.parametrize("review", [None, {}, {"complete": "true"}])
def test_missing_boundary_review_fails(bundle, review):
    _, _, _, record, run = bundle
    assert run(supplied={**record, "boundary_review": review})


def test_unavailable_extractor_fails_clearly(bundle, monkeypatch):
    _, _, _, _, run = bundle
    def missing(*args, **kwargs):
        raise FileNotFoundError("pdftotext unavailable")
    monkeypatch.setattr(evidence.subprocess, "run", missing)
    assert "pdftotext unavailable" in run()[0]


def test_typography_is_narrow_and_does_not_change_shared_normalizer():
    text = "ﬁnd\u00ad\nings and ﬂowers"
    assert evidence.typography(text) == "findings and flowers"
    assert evidence.typography("not significant; -0.5; 1²; micro-level") == "not significant; -0.5; 1²; micro-level"
    assert validator.normalize_ws(text) == "ﬁnd ings and ﬂowers"
    assert evidence.typography("two\nwords") == "two\nwords"


@pytest.mark.parametrize("source,correct,incorrect", [
    ("We studied 10-\n20 firms.", "We studied 10-20 firms.", "We studied 1020 firms."),
    ("The estimate was -\n20.", "The estimate was -20.", "The estimate was 20."),
    ("We studied micro-\nenterprises.", "We studied microenterprises.", "We studied macroenterprises."),
])
def test_wrapped_hyphens_preserve_numbers_and_signs(bundle, source, correct, incorrect):
    root, fm, _, record, run = bundle
    import fitz
    pdf = root / "wrapped.pdf"
    with fitz.open() as doc:
        doc.new_page().insert_text((40, 50), source)
        doc.save(pdf)
    fm["pdf_path"] = pdf.name
    # Poppler itself dehyphenates these synthetic wraps; use the extractor
    # that retains them to exercise the comparator with faithful evidence.
    recipe = {"name": "pymupdf-regions", "regions": [
        {"page": 1, "rect": [35, 30, 350, 100]}]}
    text, version = evidence.extract(pdf, recipe)
    assert "-\n" in text
    rebound = {**record, "pdf_path": pdf.name,
               "pdf_sha256": evidence.digest(pdf.read_bytes()),
               "derived_text_sha256": evidence.digest(text.encode()),
               "extractor": {**recipe, "version": version}}
    assert run(correct, {**rebound, "abstract_sha256": evidence.digest(correct.encode())}) == []
    errors = run(incorrect, {**rebound, "abstract_sha256": evidence.digest(incorrect.encode())})
    assert "not an exact match" in errors[0]


def test_region_replay_joins_pages_without_footer(bundle):
    root, _, _, record, _ = bundle
    import fitz
    pdf = root / "regions.pdf"
    with fitz.open() as doc:
        doc.new_page().insert_text((40, 50), "First part of abstract.")
        doc[0].insert_text((40, 150), "Acknowledgments interrupt the extracted text.")
        doc.new_page().insert_text((40, 50), "Second part of abstract.")
        doc.save(pdf)
    recipe = {"name": "pymupdf-regions", "regions": [
        {"page": 1, "rect": [35, 30, 350, 60]}, {"page": 2, "rect": [35, 30, 350, 60]}]}
    text, _ = evidence.extract(pdf, recipe)
    assert validator.normalize_ws(text) == "First part of abstract. Second part of abstract."
    for regions in [list(reversed(recipe["regions"])), [recipe["regions"][0]] * 2,
                    [{"page": 1, "rect": [-1, 0, 50, 50]}],
                    [{"page": 1, "rect": [0, 0, float("nan"), 50]}],
                    [{"page": 3, "rect": [0, 0, 50, 50]}]]:
        with pytest.raises(evidence.EvidenceError):
            evidence.extract(pdf, {**recipe, "regions": regions})


def test_book_review_abstract_sentinel_keeps_heading_required():
    fm = {"paper_type": "book-review", "extraction_version": "v1"}
    sections = {heading: "A sufficiently detailed synthetic section for this structural check."
                for heading, _ in validator.REQUIRED_HEADINGS}
    sections["Abstract"] = validator.NOT_REPORTED
    errors = []
    validator.check_required_headings(sections, fm, errors)
    assert errors == []
    del sections["Abstract"]
    validator.check_required_headings(sections, fm, errors)
    assert errors


def test_cli_rejects_evidence_for_multiple_notes():
    result = subprocess.run([sys.executable, str(Path(validator.__file__)), "a.md", "b.md",
                             "--abstract-evidence", "evidence.json"], capture_output=True, text=True)
    assert result.returncode == 2
    assert "exactly one note" in result.stderr
