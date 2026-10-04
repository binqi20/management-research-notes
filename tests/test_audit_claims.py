"""Synthetic claims-pass tests; no corpus, network, or auditor CLI access."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import audit_note as audit  # noqa: E402

BODY = "**Research Question**\nThe sample includes 12 firms.\n"
SOURCE = "The sample includes 12 firms. The association was negative."
EXPECTED = {
    "paper_id": "synthetic-paper",
    "note_sha256": audit.sha256_text(BODY),
    "text_sha256": audit.sha256_text(SOURCE),
    "rubric_version": "v3",
}


def payload(status="SUPPORTED"):
    return {
        "provenance": {
            **EXPECTED,
            "auditor_model": "gpt-6-astra",
            "generated_at": "2026-10-04T00:00:00Z",
            "dispatch_mode": "independent-subagent",
            "input_mode": "standard-fitted",
            "pass": "claims-v1",
        },
        "claims": [{
            "field": "research_question",
            "note_clause": "The sample includes 12 firms.",
            "claim_type": "number",
            "status": status,
            "source_fragment": "The sample includes 12 firms.",
            "note": "Verified the count and unit.",
        }],
    }


def parse(data, **kwargs):
    inputs = {
        "expected_provenance": EXPECTED,
        "note_body": BODY,
        "pdf_text": SOURCE,
        "fitted_pdf_text": SOURCE,
    }
    inputs.update(kwargs)
    return audit.parse_claims_response(json.dumps(data), **inputs)


def layer_1():
    return {
        "overall": "pass", "anchors_checked": 1,
        "anchors_not_found_in_pdf": [], "anchors_missing": [], "other_errors": [],
    }


def layer_2(verdict="SUPPORTED"):
    return audit.parse_auditor_response(json.dumps({
        "provenance": {k: v for k, v in payload()["provenance"].items() if k != "pass"},
        "layer_2": {"scores": {
            field: {"verdict": verdict, "confidence": "high"}
            for field in audit.LAYER_2_PROSE_FIELDS
        }},
    }), expected_provenance=EXPECTED, require_provenance=True)


def report(**kwargs):
    inputs = dict(paper_id="synthetic-paper", layer_1=layer_1(), layer_2=layer_2(),
                  auditor_model="gpt-6-astra")
    inputs.update(kwargs)
    return audit.combine_audit_result(**inputs)


def test_valid_claims_and_non_gating_counts():
    data = payload()
    for status in ("UNVERIFIED", "CONTRADICTED"):
        row = copy.deepcopy(data["claims"][0])
        row["status"] = status
        if status == "UNVERIFIED":
            row["source_fragment"] = ""
        data["claims"].append(row)
    result = report(claims=parse(data))
    assert result["overall"] == "pass"
    assert result["layer_2_claims"] == data["claims"]
    assert result["layer_2_claims_provenance"] == data["provenance"]
    assert result["layer_2_claims_summary"] == {
        "claims_total": 3, "supported": 1, "unverified": 1, "contradicted": 1,
    }
    assert report(layer_2=layer_2("UNSUPPORTED"), claims=parse(payload()))["overall"] == "fail"


def test_report_without_claims_is_backward_compatible():
    result = report()
    assert result["overall"] == "pass"
    assert "layer_2_claims" not in result
    assert "layer_2_claims_summary" not in result
    assert result["rubric_version"] == "v3"
    assert report(layer_2=None)["layer_2"]["overall"] == "skipped"
    with pytest.raises(ValueError, match="holistic"):
        report(layer_2=None, claims=parse(payload()))


def test_reader_writer_metadata_and_context_preservation():
    original = {"fitted_pdf_chars": 55}
    result = report(
        claims=parse(payload()), audit_context=original,
        fm={"extraction_model": "legacy-writer", "augmented_model": "augmenter"},
        repair_model="explicit-repair-writer",
    )
    context = result["audit_context"]
    assert original == {"fitted_pdf_chars": 55}
    assert context["fitted_pdf_chars"] == 55
    assert context["readers"] == [
        {"model": "gpt-6-astra", "dispatch_mode": "independent-subagent", "pass": pass_name}
        for pass_name in ("layer-2", "claims-v1")
    ]
    assert context["writer_models"] == {
        "extraction_model": "legacy-writer", "augmented_model": "augmenter",
        "repair_model": "explicit-repair-writer",
    }
    writers = report(writer_models={"extraction_model": "same-reader-family"})["audit_context"]["writer_models"]
    assert writers == {"extraction_model": "same-reader-family", "augmented_model": None}
    assert "repair_model" not in report(fm={"repair_model": "untrusted-inference"})["audit_context"]["writer_models"]


@pytest.mark.parametrize("key,value", [
    ("paper_id", "wrong"), ("note_sha256", "0" * 64),
    ("text_sha256", "0" * 64), ("rubric_version", "v2"), ("pass", "layer-2"),
    ("input_mode", "full-raw-text"),
    ("auditor_model", ""), ("generated_at", None), ("dispatch_mode", []),
])
def test_bad_provenance(key, value):
    data = payload()
    data["provenance"][key] = value
    with pytest.raises(ValueError):
        parse(data)


@pytest.mark.parametrize("key", sorted(audit.EXTERNAL_PROVENANCE_REQUIRED_KEYS | {"input_mode", "pass"}))
def test_missing_provenance_key(key):
    data = payload()
    del data["provenance"][key]
    with pytest.raises(ValueError):
        parse(data)


@pytest.mark.parametrize("key,value", [
    ("field", "unknown_field"), ("field", "key_findings"), ("note_clause", "paraphrase"),
    ("note_clause", ""), ("note_clause", 12), ("claim_type", "causality"),
    ("status", "PARTIAL"), ("source_fragment", ""), ("source_fragment", "invented"),
    ("source_fragment", "word " * 26), ("note", None),
])
def test_bad_claim_fields(key, value):
    data = payload()
    data["claims"][0][key] = value
    with pytest.raises(ValueError):
        parse(data)


@pytest.mark.parametrize("shape", [None, [], {}, {"claims": []}, {"provenance": {}}])
def test_bad_top_level(shape):
    with pytest.raises(ValueError):
        parse(shape)


def test_strict_keys_and_nonempty_array():
    for location in ("top", "provenance", "claim"):
        data = payload()
        target = data if location == "top" else data["provenance"] if location == "provenance" else data["claims"][0]
        target["unexpected"] = "value"
        with pytest.raises(ValueError):
            parse(data)
    for claims in ([], {}, [None], [{}]):
        data = payload()
        data["claims"] = claims
        with pytest.raises(ValueError):
            parse(data)
    for key in payload()["claims"][0]:
        data = payload()
        del data["claims"][0][key]
        with pytest.raises(ValueError):
            parse(data)


def test_source_membership_checks_raw_and_fitted_with_whitespace_tolerance():
    assert parse(payload(), pdf_text="The sample\nincludes 12 firms.")
    for key in ("pdf_text", "fitted_pdf_text"):
        with pytest.raises(ValueError, match="raw and fitted"):
            parse(payload(), **{key: "No matching fragment here."})
    data = payload("UNVERIFIED")
    data["claims"][0]["source_fragment"] = ""
    assert parse(data)
    data["claims"][0]["source_fragment"] = "invented"
    with pytest.raises(ValueError):
        parse(data)


def test_v3_prose_scope_and_note_verbatim():
    data = payload()
    data["claims"][0]["field"] = "key_findings"
    assert parse(data, prose_fields=audit.LAYER_2_PROSE_FIELDS_V3)
    with pytest.raises(ValueError):
        parse(data, prose_fields=["unknown"])
    with pytest.raises(ValueError, match="verbatim"):
        parse(payload(), note_body=BODY.replace("includes 12", "includes\n12"))


@pytest.mark.parametrize("pdf_text", [SOURCE, "intro " * 50000 + "\nREFERENCES\n" + "citation " * 1000])
def test_prompt_modes_preserve_exact_fitted_input_and_cautions(monkeypatch, capsys, tmp_path, pdf_text):
    note = tmp_path / "note.md"
    note.write_text(BODY)
    monkeypatch.setattr(audit, "load_note", lambda path: ({"id": "synthetic-paper"}, BODY, {}))
    monkeypatch.setattr(audit, "load_pdf_text", lambda fm: pdf_text)
    monkeypatch.setattr(audit, "load_rubric", lambda: "HOLISTIC TASK")
    monkeypatch.setattr(audit, "load_claims_task", lambda: "CLAIMS TASK")
    outputs = []
    for mode in ("--prompt-only", "--claims-prompt-only"):
        monkeypatch.setattr(sys, "argv", ["audit_note.py", str(note), mode])
        assert audit.main() == 0
        outputs.append(capsys.readouterr().out)
    assert outputs[0].replace("HOLISTIC TASK", "CLAIMS TASK", 1) == outputs[1]
    expected, context = audit.build_auditor_prompt_and_context(
        "synthetic-paper", "", BODY, pdf_text, "CLAIMS TASK", anchors=[])
    assert outputs[1] == expected + "\n"
    fitted, fitted_context = audit.fit_pdf_text_for_audit(pdf_text, anchors=[])
    assert context == fitted_context
    assert fitted in outputs[1]


@pytest.mark.parametrize("flags", [
    ["--claims-json", "claims.json"],
    ["--claims-json", "claims.json", "--layer-2-json", "holistic.json", "--skip-layer-2"],
    ["--claims-json", "claims.json", "--layer-2-json", "holistic.json", "--prompt-only"],
    ["--claims-json", "claims.json", "--layer-2-json", "holistic.json", "--claims-prompt-only"],
])
def test_claims_flag_cannot_be_silently_discarded(monkeypatch, flags):
    monkeypatch.setattr(sys, "argv", ["audit_note.py", "unused.md", *flags])
    with pytest.raises(SystemExit) as exc:
        audit.main()
    assert exc.value.code == 2


def test_external_assembly_consumes_claims_and_records_writers(monkeypatch, tmp_path):
    note = tmp_path / "note.md"
    note.write_text(BODY)
    holistic_path = tmp_path / "holistic.json"
    holistic_path.write_text(json.dumps(layer_2()))
    claims_path = tmp_path / "claims.json"
    claims_path.write_text(json.dumps(payload()))
    fm = {"id": "synthetic-paper", "extraction_model": "writer"}
    monkeypatch.setattr(audit, "load_note", lambda path: (fm, BODY, {}))
    monkeypatch.setattr(audit, "load_pdf_text", lambda fm: SOURCE)
    monkeypatch.setattr(audit, "run_layer_1", lambda fm: layer_1())
    captured = []
    monkeypatch.setattr(audit, "write_audit_report", lambda paper_id, result: captured.append(result) or audit.AUDITS_DIR / "synthetic.audit.json")
    monkeypatch.setattr(sys, "argv", [
        "audit_note.py", str(note), "--layer-2-json", str(holistic_path),
        "--claims-json", str(claims_path), "--repair-model", "repair-writer",
    ])
    assert audit.main() == 0
    assert captured[0]["layer_2_claims_summary"]["claims_total"] == 1
    assert captured[0]["audit_context"]["writer_models"]["repair_model"] == "repair-writer"
    failed = layer_1()
    failed["overall"] = "fail"
    monkeypatch.setattr(audit, "run_layer_1", lambda fm: failed)
    assert audit.main() == 2
    assert len(captured) == 1
