"""Synthetic publication gate checks; never modify corpus or dispatch readers."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_publication_readiness as gate


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    monkeypatch.setattr(gate.audit, "SYNAPSE_ROOT", tmp_path)
    note, source = tmp_path / "note.md", tmp_path / "source.txt"
    note.write_text('---\nid: example\nextraction_version: v3\ntext_path: source.txt\n---\n'
                    '**Research Question**\nThe sample includes 12 firms.\n')
    source.write_text("The sample includes 12 firms.\nSecond source line.\n")
    evidence = tmp_path / "source-review.txt"
    evidence.write_text("Parent independently reviewed source and reader runtime records.")
    audit_path, review_path = tmp_path / "audit.json", tmp_path / "review.json"
    hashes = {"note_sha256": gate.digest(note), "text_sha256": gate.digest(source)}
    provenance = {"paper_id": "example", **hashes, "rubric_version": "v2",
                  "auditor_model": "holistic-model", "generated_at": "2026-10-05T00:00:00Z",
                  "dispatch_mode": "independent", "input_mode": "standard-fitted"}
    report = {
        "paper_id": "example", "input_hashes": hashes, "rubric_version": "v2",
        "auditor_model": "holistic-model", "overall": "pass",
        "flagged_claims": [], "parse_warnings": [],
        "layer_1": {"overall": "pass", "anchors_missing": [], "anchors_not_found_in_pdf": [], "other_errors": []},
        "layer_2": {"overall": "pass", "scores": {f: {"verdict": "SUPPORTED", "confidence": "high"}
                                                    for f in gate.audit.LAYER_2_PROSE_FIELDS_V3}},
        "layer_2_provenance": provenance,
        "layer_2_claims_provenance": {**provenance, "auditor_model": "claims-model", "pass": "claims-v1"},
        "layer_2_claims": [{"field": "research_question", "note_clause": "The sample includes 12 firms.",
                            "claim_type": "number", "status": "SUPPORTED",
                            "source_fragment": "The sample includes 12 firms.", "note": "Count verified."}],
        "audit_context": {"readers": [{"pass": p, "model": m, "dispatch_mode": "independent"}
                                      for p, m in [("layer-2", "holistic-model"), ("claims-v1", "claims-model")]]},
    }
    review = {
        "schema_version": "publication-review-v1", "paper_id": "example", **hashes,
        "coverage_reviewed": True, "numeric_reviewed": True, "pending_corrections": [],
        "writer_contexts": ["writer"],
        "readers": {"layer-2": {"context_id": "reader-a", "model": "holistic-model"},
                    "claims-v1": {"context_id": "reader-b", "model": "claims-model"}},
        "evidence": [{"path": evidence.name, "sha256": gate.digest(evidence)}], "adjudications": {},
    }

    def run(rebind=True):
        audit_path.write_text(json.dumps(report))
        if rebind:
            review["audit_sha256"] = gate.digest(audit_path)
        review_path.write_text(json.dumps(review))
        return gate.check_readiness(note, audit_path, review_path)

    return report, review, run, (note, source, evidence, audit_path, review_path)


def adjudication():
    return {"disposition": "source_faithful", "raw_lines": [[1, 2]],
            "rationale": "Parent reopened the source and resolved the reader's uncertainty."}


def test_current_records_ready_and_historical_rubric_preserved(bundle):
    report, _, run, paths = bundle
    result, code = run()
    assert code == 0 and result["ready"] is True
    before = {p: p.read_bytes() for p in paths}
    assert gate.check_readiness(paths[0], paths[3], paths[4])[1] == 0
    assert all(p.read_bytes() == content for p, content in before.items())
    assert report["rubric_version"] == "v2"


def test_pass_with_unverified_claim_requires_adjudication(bundle):
    report, review, run, _ = bundle
    report["layer_2_claims"][0]["status"] = "UNVERIFIED"
    report["layer_2_claims"][0]["source_fragment"] = ""
    result, code = run()
    assert code == 1 and "claim:0" in result["errors"][0]
    review["adjudications"]["claim:0"] = adjudication()
    assert run()[1] == 0


def test_partial_requires_adjudication(bundle):
    report, review, run, _ = bundle
    report["layer_2"]["scores"]["limitations"]["verdict"] = "PARTIAL"
    assert run()[1] == 1
    review["adjudications"]["layer2:limitations"] = adjudication()
    assert run()[1] == 0


@pytest.mark.parametrize("target", ["note", "source", "evidence", "audit"])
def test_stale_bindings_block(bundle, target):
    _, review, run, paths = bundle
    assert run()[1] == 0
    index = {"note": 0, "source": 1, "evidence": 2, "audit": 3}[target]
    paths[index].write_text(paths[index].read_text() + "\n")
    result, code = gate.check_readiness(paths[0], paths[3], paths[4])
    assert code == 1 and result["ready"] is False


def test_abstract_evidence_reference_must_be_current_and_reproducible(bundle):
    _, review, run, paths = bundle
    evidence_path = paths[0].parent / "abstract-evidence.json"
    evidence_path.write_text('{"schema_version": "invalid"}')
    review["abstract_evidence"] = {"path": evidence_path.name, "sha256": "stale"}
    result, code = run()
    assert code == 1 and "abstract evidence reference is stale" in result["errors"][0]
    review["abstract_evidence"]["sha256"] = gate.digest(evidence_path)
    result, code = run()
    assert code == 1 and "invalid evidence schema" in result["errors"][0]


def test_abstract_missing_from_raw_source_needs_verified_alternative(bundle):
    report, review, run, paths = bundle
    note = paths[0]
    note.write_text(note.read_text() + '\n**Abstract**\nInvented abstract outside the source.\n')
    new_hash = gate.audit.sha256_text(note.read_text())
    report["input_hashes"]["note_sha256"] = new_hash
    review["note_sha256"] = new_hash
    result, code = run()
    assert code == 1 and "Abstract is not a verbatim substring" in result["errors"][0]


def test_publication_gate_replays_valid_pdf_abstract_evidence(bundle):
    import abstract_evidence as ae
    fitz = pytest.importorskip("fitz")
    report, review, run, paths = bundle
    note, source = paths[:2]
    abstract = "This synthetic abstract reports 25 observations. It is not a causal result."
    pdf = note.parent / "paper.pdf"
    with fitz.open() as doc:
        doc.new_page().insert_text((40, 50), abstract)
        doc.save(pdf)
    note.write_text(note.read_text().replace("text_path: source.txt", "text_path: source.txt\npdf_path: paper.pdf")
                    + '\n**Abstract**\n' + abstract + '\n')
    new_hash = gate.audit.sha256_text(note.read_text())
    review["note_sha256"] = report["input_hashes"]["note_sha256"] = new_hash
    for key in ("layer_2_provenance", "layer_2_claims_provenance"):
        report[key]["note_sha256"] = new_hash
    recipe = {"name": "pymupdf-regions", "regions": [{"page": 1, "rect": [30, 30, 590, 65]}]}
    text, version = ae.extract(pdf, recipe)
    record = {
        "schema_version": "pdf-abstract-evidence-v1", "paper_id": "example",
        "pdf_path": "paper.pdf", "text_path": "source.txt",
        "pdf_sha256": gate.digest(pdf), "text_sha256": gate.digest(source),
        "abstract_sha256": ae.digest(abstract.encode()),
        "extractor": {**recipe, "version": version},
        "derived_text_sha256": ae.digest(text.encode()),
        "boundary_review": {"complete": True, "reviewer": "synthetic test",
                            "source_location": "page 1", "rationale": "Complete synthetic abstract."},
    }
    ep = note.parent / "abstract.json"
    ep.write_text(json.dumps(record))
    review["abstract_evidence"] = {"path": ep.name, "sha256": gate.digest(ep)}
    result, code = run()
    assert code == 0, result
    del review["abstract_evidence"]
    result, code = run()
    assert code == 1 and "Abstract is not a verbatim substring" in result["errors"][0]


@pytest.mark.parametrize("mutation", [
    lambda a, r: r.update(schema_version="wrong"),
    lambda a, r: r.pop("coverage_reviewed"),
    lambda a, r: r.update(coverage_reviewed="true"),
    lambda a, r: r.update(numeric_reviewed=1),
    lambda a, r: r.update(pending_corrections=["repair"]),
    lambda a, r: r.update(pending_corrections=False),
    lambda a, r: r.update(writer_contexts=[]),
    lambda a, r: r["readers"].pop("claims-v1"),
    lambda a, r: r["readers"]["claims-v1"].update(context_id="reader-a"),
    lambda a, r: r["readers"]["claims-v1"].update(context_id="writer"),
    lambda a, r: r["readers"]["claims-v1"].update(model="wrong"),
    lambda a, r: a["audit_context"].update(readers=[]),
    lambda a, r: a["audit_context"]["readers"][0].pop("pass"),
    lambda a, r: a["layer_2_provenance"].update(note_sha256="wrong"),
    lambda a, r: a["layer_2_provenance"].update(rubric_version="v3"),
    lambda a, r: a["layer_2_claims_provenance"].pop("pass"),
    lambda a, r: a.update(layer_2_claims=[]),
    lambda a, r: a["layer_2_claims"][0].update(source_fragment="invented source quotation"),
    lambda a, r: a["layer_2"]["scores"].pop("data_measures"),
    lambda a, r: a["layer_2"]["scores"].update(extra={"verdict": "SUPPORTED", "confidence": "high"}),
    lambda a, r: a["layer_2"]["scores"]["limitations"].update(verdict="UNSUPPORTED"),
    lambda a, r: a["layer_2"]["scores"]["limitations"].update(verdict="CONTRADICTED"),
    lambda a, r: a["layer_1"].update(overall="fail"),
    lambda a, r: a["layer_1"].update(other_errors=["bad anchor"]),
    lambda a, r: a.update(parent_review={"publication_ready": False}),
    lambda a, r: a.update(parent_review={"publication_ready": "true"}),
    lambda a, r: a.update(parent_review={"pending_corrections_count": 1}),
    lambda a, r: a.update(parent_review={"pending_corrections": ["repair"]}),
    lambda a, r: r.update(evidence=[]),
    lambda a, r: r["evidence"][0].update(path="missing.txt"),
    lambda a, r: r.pop("adjudications"),
])
def test_fail_closed(bundle, mutation):
    report, review, run, _ = bundle
    mutation(report, review)
    result, code = run()
    assert code == 1 and result["ready"] is False and result["errors"]


@pytest.mark.parametrize("change", [
    {"raw_lines": [[0, 1]]}, {"raw_lines": [[2, 1]]}, {"raw_lines": [[1, 3]]},
    {"raw_lines": [[True, 2]]}, {"raw_lines": []}, {"rationale": " "},
    {"disposition": "ignore"},
])
def test_adjudication_requires_valid_source_record(bundle, change):
    report, review, run, _ = bundle
    report["layer_2_claims"][0]["status"] = "UNVERIFIED"
    review["adjudications"]["claim:0"] = {**adjudication(), **change}
    assert run()[1] == 1


def test_six_field_contract(bundle):
    report, _, run, paths = bundle
    paths[0].write_text(paths[0].read_text().replace("v3", "v2"))
    report["layer_2"]["scores"] = {k: v for k, v in report["layer_2"]["scores"].items()
                                      if k in gate.audit.LAYER_2_PROSE_FIELDS}
    report["input_hashes"]["note_sha256"] = gate.digest(paths[0])
    for key in ["layer_2_provenance", "layer_2_claims_provenance"]:
        report[key]["note_sha256"] = gate.digest(paths[0])
    bundle[1]["note_sha256"] = gate.digest(paths[0])
    assert run()[1] == 0


def test_bad_input_exit_two_and_json_cli(bundle, monkeypatch, capsys):
    _, _, run, paths = bundle
    run()
    paths[3].write_text("not json")
    monkeypatch.setattr(sys, "argv", ["check_publication_readiness.py", str(paths[0]),
                                    "--audit-json", str(paths[3]), "--review-json", str(paths[4])])
    assert gate.main() == 2
    result = json.loads(capsys.readouterr().out)
    assert result["ready"] is False and result["errors"]


def test_missing_cli_arguments_return_json(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["check_publication_readiness.py"])
    assert gate.main() == 2
    assert json.loads(capsys.readouterr().out)["ready"] is False


def test_unknown_note_version_blocks(bundle):
    report, review, run, paths = bundle
    paths[0].write_text(paths[0].read_text().replace("v3", "unknown"))
    current = gate.digest(paths[0])
    review["note_sha256"] = report["input_hashes"]["note_sha256"] = current
    for key in ["layer_2_provenance", "layer_2_claims_provenance"]:
        report[key]["note_sha256"] = current
    assert run()[1] == 1


@pytest.mark.parametrize("raw", [b"The sample includes 12 firms.\r\nSecond source line.\r\n",
                                  b"The sample includes 12 firms.\nInvalid byte: \xff\n"])
def test_source_hash_matches_canonical_audit_decoding(bundle, raw):
    report, review, run, paths = bundle
    paths[1].write_bytes(raw)
    canonical = gate.audit.sha256_text(gate.audit.load_pdf_text({"text_path": paths[1].name}))
    assert canonical != gate.digest(paths[1])
    report["input_hashes"]["text_sha256"] = review["text_sha256"] = canonical
    for key in ["layer_2_provenance", "layer_2_claims_provenance"]:
        report[key]["text_sha256"] = canonical
    assert run()[1] == 0


def test_note_hash_matches_canonical_newlines(bundle):
    report, review, run, paths = bundle
    paths[0].write_bytes(paths[0].read_bytes().replace(b"\n", b"\r\n"))
    assert run()[1] == 0


@pytest.mark.parametrize("field,value", [("parse_warnings", ["warning"]),
                                         ("parse_warnings", False),
                                         ("flagged_claims", "none"),
                                         ("flagged_claims", [{"kind": "unknown"}])])
def test_ignored_report_diagnostics_block(bundle, field, value):
    report, _, run, _ = bundle
    report[field] = value
    assert run()[1] == 1


def test_recognized_partial_flag_requires_and_accepts_adjudication(bundle):
    report, review, run, _ = bundle
    report["layer_2"]["scores"]["limitations"]["verdict"] = "PARTIAL"
    report["flagged_claims"] = [{"layer": 2, "kind": "partial", "field": "limitations", "detail": "Scope."}]
    assert run()[1] == 1
    review["adjudications"]["layer2:limitations"] = adjudication()
    assert run()[1] == 0


@pytest.mark.parametrize("summary", [
    {"claims_total": 2, "supported": 1, "unverified": 0, "contradicted": 0},
    {"claims_total": True, "supported": 1, "unverified": 0, "contradicted": 0},
    {"claims_total": 1}, None,
])
def test_inconsistent_claims_summary_blocks(bundle, summary):
    report, _, run, _ = bundle
    report["layer_2_claims_summary"] = summary
    assert run()[1] == 1


def test_consistent_claims_summary_passes(bundle):
    report, _, run, _ = bundle
    report["layer_2_claims_summary"] = {"claims_total": 1, "supported": 1, "unverified": 0, "contradicted": 0}
    assert run()[1] == 0


@pytest.mark.parametrize("key,value", [("paper_id", "other"), ("note_sha256", "0" * 64),
                                       ("text_sha256", "0" * 64), ("claims_sha256", "0" * 64)])
def test_stale_embedded_parent_review_blocks(bundle, key, value):
    report, _, run, _ = bundle
    report["parent_review"] = {"publication_ready": True, key: value}
    assert run()[1] == 1


def test_embedded_repair_disposition_blocks_without_pending_counter(bundle):
    report, _, run, _ = bundle
    report["parent_review"] = {"publication_ready": True, "adjudications": [
        {"channel": "claims", "claim_index": 0, "disposition": "repair_class_proposed_only"}]}
    assert run()[1] == 1


def test_embedded_claims_hash_needs_current_sidecar_evidence(bundle):
    report, review, run, paths = bundle
    sidecar = paths[0].parent / "claims.json"
    sidecar.write_text(json.dumps({"provenance": report["layer_2_claims_provenance"],
                                   "claims": report["layer_2_claims"]}))
    report["parent_review"] = {"publication_ready": True, "claims_sha256": gate.digest(sidecar)}
    review["evidence"].append({"path": sidecar.name, "sha256": gate.digest(sidecar)})
    assert run()[1] == 0
    report["layer_2_claims"][0]["note"] = "Different reader payload."
    assert run()[1] == 1


@pytest.mark.parametrize("field", ["coverage_sha256", "review_sha256"])
def test_unbound_embedded_reference_blocks(bundle, field):
    report, _, run, _ = bundle
    report["parent_review"] = {"publication_ready": True, field: "0" * 64}
    assert run()[1] == 1


@pytest.mark.parametrize("field", ["coverage_adjudications", "parent_coverage_adjudications"])
def test_embedded_coverage_repair_disposition_blocks(bundle, field):
    report, _, run, _ = bundle
    report["parent_review"] = {"publication_ready": True, field: [
        {"disposition": "repair_class_proposed_only"}]}
    assert run()[1] == 1


@pytest.mark.parametrize("mutation", ["none", "stale_identity", "pending", "repair", "coverage_repair",
                                      "stale_coverage", "wrong_coverage_identity", "wrong_path"])
def test_bound_parent_review_and_coverage_references(bundle, mutation):
    report, review, run, paths = bundle
    identity = {"paper_id": "example", **report["input_hashes"]}
    coverage_path = paths[0].parent / "coverage.json"
    coverage = dict(identity)
    if mutation == "wrong_coverage_identity":
        coverage["paper_id"] = "other"
    coverage_path.write_text(json.dumps(coverage))
    review["evidence"].append({"path": coverage_path.name, "sha256": gate.digest(coverage_path)})
    parent_path = paths[0].parent / "parent.json"
    parent = {**identity, "publication_ready": True, "adjudications": [],
              "coverage_sha256": gate.digest(coverage_path)}
    if mutation == "stale_identity":
        parent["note_sha256"] = "0" * 64
    if mutation == "pending":
        parent["pending_unique_operations"] = 1
    if mutation in ("repair", "coverage_repair"):
        key = "adjudications" if mutation == "repair" else "parent_coverage_adjudications"
        parent[key] = [{"disposition": "repair_class_proposed_only"}]
    if mutation == "stale_coverage":
        parent["coverage_sha256"] = "0" * 64
    parent_path.write_text(json.dumps(parent))
    review["evidence"].append({"path": parent_path.name, "sha256": gate.digest(parent_path)})
    report["parent_review"] = {"review_path": str(parent_path),
                               "review_sha256": gate.digest(parent_path), "publication_ready": True}
    if mutation == "wrong_path":
        report["parent_review"]["review_path"] = str(coverage_path)
    assert run()[1] == (0 if mutation == "none" else 1)
