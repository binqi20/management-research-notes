#!/usr/bin/env python3
"""Read-only publication gate for a current note and hash-bound parent review.

Checks record completeness and hash currency, not semantic coverage, source
judgment, or runtime identity. Those still require independent parent review.
No audit is run, assembled, restamped, or written by this command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# Keep CLI execution read-only even when dependency bytecode caches are absent.
sys.dont_write_bytecode = True
import audit_note as audit
from validate_note import check_abstract_verbatim, parse_body_sections


class Blocked(ValueError):
    """Readable inputs do not establish publication readiness."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Blocked(message)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked(f"{path.name}: expected a JSON object")
    return value


def check_parent_state(record: dict, identity: dict, *, require_identity: bool = False) -> None:
    """Check known parent-review state; this does not adjudicate its substance."""
    require(isinstance(record, dict), "parent_review must be an object")
    for key, value in identity.items():
        if require_identity or key in record:
            require(record.get(key) == value, f"parent_review {key} mismatch")
    dispositions = {"source_faithful", "framing", "accepted_source_faithful", "accepted_framing"}
    for key in ("adjudications", "coverage_adjudications", "parent_coverage_adjudications"):
        if key in record:
            require(isinstance(record[key], list)
                    and all(isinstance(row, dict) and row.get("disposition") in dispositions
                            for row in record[key]),
                    f"parent_review has unresolved or malformed {key}")
    if "publication_ready" in record:
        require(record["publication_ready"] is True, "parent_review blocks publication")
    for key, value in record.items():
        if key.startswith("pending"):
            require((type(value) is int and value == 0)
                    or (isinstance(value, list) and value == []),
                    f"parent_review {key} is pending or malformed")


def _check(note_path: Path, audit_path: Path, review_path: Path) -> str:
    report, review = read_json(audit_path), read_json(review_path)
    fm, body, _ = audit.load_note(note_path)
    require(isinstance(fm, dict), "note frontmatter must be an object")
    paper_id = fm.get("id")
    require(nonempty(paper_id), "note id is missing")
    require(nonempty(fm.get("text_path")), "note text_path is missing")
    source = audit.load_pdf_text(fm)
    # Match audit assembly: universal-newline text, and replacement decoding for source.
    hashes = {"note_sha256": audit.sha256_text(note_path.read_text(encoding="utf-8")),
              "text_sha256": audit.sha256_text(source)}
    require(review.get("schema_version") == "publication-review-v1", "invalid review schema_version")
    require(review.get("paper_id") == report.get("paper_id") == paper_id, "paper identity mismatch")
    require(report.get("input_hashes") == hashes, "official input hashes are stale or malformed")
    for key, value in {**hashes, "audit_sha256": digest(audit_path)}.items():
        require(review.get(key) == value, f"review {key} is stale or missing")
    for key in ("coverage_reviewed", "numeric_reviewed"):
        require(review.get(key) is True, f"{key} must be literal true")
    require(isinstance(review.get("pending_corrections"), list)
            and review["pending_corrections"] == [], "pending_corrections must be an empty list")
    abstract_path = None
    if "abstract_evidence" in review:
        reference = review["abstract_evidence"]
        require(isinstance(reference, dict) and nonempty(reference.get("path")),
                "abstract_evidence needs a path and sha256")
        abstract_path = review_path.parent / reference["path"]
        require(digest(abstract_path) == reference.get("sha256"), "abstract evidence reference is stale")
    abstract_errors = []
    check_abstract_verbatim(parse_body_sections(body), fm, abstract_errors,
                            abstract_path, root=audit.SYNAPSE_ROOT)
    require(not abstract_errors, "; ".join(abstract_errors))
    require(report.get("overall") == "pass", "official overall must pass")
    require(isinstance(report.get("parse_warnings"), list) and not report["parse_warnings"],
            "official parse_warnings must be an empty list")
    require(isinstance(report.get("flagged_claims"), list), "official flagged_claims must be a list")
    layer1 = report.get("layer_1")
    require(isinstance(layer1, dict) and layer1.get("overall") == "pass", "official Layer 1 must pass")
    for key in ("anchors_missing", "anchors_not_found_in_pdf", "other_errors"):
        require(isinstance(layer1.get(key), list) and not layer1[key], f"Layer 1 {key} must be empty")
    identity = {"paper_id": paper_id, **hashes}
    if "parent_review" in report:
        check_parent_state(report["parent_review"], identity)

    require(fm.get("extraction_version") in ("v1", "v2", "v3"), "note extraction_version is missing or unknown")
    fields = audit.prose_fields_for(fm.get("extraction_version"))
    layer2 = report.get("layer_2")
    require(isinstance(layer2, dict) and layer2.get("overall") == "pass", "holistic overall must pass")
    scores = layer2.get("scores")
    require(isinstance(scores, dict) and set(scores) == set(fields), "holistic field set must be exact")
    for field, row in scores.items():
        require(isinstance(row, dict) and row.get("verdict") in ("SUPPORTED", "PARTIAL"),
                f"layer2:{field} is unsupported, contradicted, or malformed")
    rubric = report.get("rubric_version")
    require(nonempty(rubric), "official rubric_version is missing")
    expected = {"paper_id": paper_id, **hashes, "rubric_version": rubric}
    fitted, _ = audit.fit_pdf_text_for_audit(source, anchors=audit.anchor_quotes(fm))
    try:
        holistic = audit.parse_auditor_response(
            json.dumps({"provenance": report.get("layer_2_provenance"), "layer_2": layer2}),
            expected_provenance=expected, require_provenance=True, prose_fields=fields)
        claims = audit.parse_claims_response(
            json.dumps({"provenance": report.get("layer_2_claims_provenance"),
                        "claims": report.get("layer_2_claims")}),
            expected_provenance=expected, note_body=body, pdf_text=source,
            fitted_pdf_text=fitted, prose_fields=fields)
    except (ValueError, TypeError, KeyError) as exc:
        raise Blocked(f"reader evidence validation: {exc}") from exc

    if "layer_2_claims_summary" in report:
        summary = report["layer_2_claims_summary"]
        expected_summary = {"claims_total": len(claims["claims"]),
                            **{label: sum(row["status"] == status for row in claims["claims"])
                               for label, status in (("supported", "SUPPORTED"),
                                                     ("unverified", "UNVERIFIED"),
                                                     ("contradicted", "CONTRADICTED"))}}
        require(isinstance(summary, dict) and set(summary) == set(expected_summary)
                and all(type(value) is int for value in summary.values())
                and summary == expected_summary, "official claims summary disagrees with parsed claims")

    writers, readers = review.get("writer_contexts"), review.get("readers")
    require(isinstance(writers, list) and bool(writers) and all(nonempty(v) for v in writers),
            "writer_contexts must list nonempty context ids")
    require(isinstance(readers, dict) and set(readers) == {"layer-2", "claims-v1"},
            "review must identify both readers")
    context = report.get("audit_context")
    require(isinstance(context, dict), "audit_context missing")
    metadata = context.get("readers")
    require(isinstance(metadata, list) and len(metadata) == 2
            and all(isinstance(v, dict) for v in metadata), "official reader metadata missing")
    require({v.get("pass") for v in metadata} == {"layer-2", "claims-v1"}, "official reader passes missing")
    context_ids = []
    for pass_name, parsed in (("layer-2", holistic), ("claims-v1", claims)):
        reader = readers[pass_name]
        require(isinstance(reader, dict) and nonempty(reader.get("context_id"))
                and nonempty(reader.get("model")), f"{pass_name} reader identity missing")
        meta = next(v for v in metadata if v["pass"] == pass_name)
        provenance = parsed["provenance"]
        require(reader["model"] == provenance["auditor_model"] == meta.get("model"),
                f"{pass_name} model mismatch")
        require(nonempty(meta.get("dispatch_mode"))
                and meta["dispatch_mode"] == provenance["dispatch_mode"], f"{pass_name} dispatch metadata mismatch")
        require(provenance.get("input_mode") == "standard-fitted", f"{pass_name} input_mode missing")
        context_ids.append(reader["context_id"])
    require(context_ids[0] != context_ids[1] and not set(context_ids).intersection(writers),
            "reader contexts must be distinct from each other and all writer contexts")
    require(report.get("auditor_model") == holistic["provenance"]["auditor_model"], "official auditor_model mismatch")

    evidence = review.get("evidence")
    require(isinstance(evidence, list) and bool(evidence), "review evidence is required")
    evidence_paths = {}
    for index, item in enumerate(evidence):
        require(isinstance(item, dict) and nonempty(item.get("path")), f"evidence[{index}] path missing")
        path = Path(item["path"])
        require(not path.is_absolute(), f"evidence[{index}] path must be relative to review file")
        try:
            actual = digest(review_path.parent / path)
        except OSError as exc:
            raise Blocked(f"evidence[{index}] unreadable: {exc}") from exc
        require(item.get("sha256") == actual, f"evidence[{index}] hash mismatch")
        evidence_paths[actual] = review_path.parent / path
    embedded = report.get("parent_review", {})
    parent_records = [(embedded, audit_path.parent)]
    if "review_path" in embedded or "review_sha256" in embedded:
        review_hash = embedded.get("review_sha256")
        require(isinstance(review_hash, str) and review_hash in evidence_paths,
                "embedded review hash requires matching hash-bound parent-review evidence")
        referenced_path = evidence_paths[review_hash]
        if "review_path" in embedded:
            require(nonempty(embedded["review_path"]), "embedded review_path is malformed")
            stated_path = Path(embedded["review_path"])
            if not stated_path.is_absolute():
                stated_path = audit_path.parent / stated_path
            require(stated_path.resolve() == referenced_path.resolve(), "embedded review_path mismatch")
        referenced = read_json(referenced_path)
        check_parent_state(referenced, identity, require_identity=True)
        require("review_path" not in referenced and "review_sha256" not in referenced,
                "nested parent-review references are unsupported")
        parent_records.append((referenced, referenced_path.parent))
    for parent_record, parent_dir in parent_records:
        if "claims_sha256" in parent_record:
            claims_hash = parent_record["claims_sha256"]
            require(isinstance(claims_hash, str) and claims_hash in evidence_paths,
                    "parent claims hash requires matching hash-bound sidecar evidence")
            require(read_json(evidence_paths[claims_hash]) == claims,
                    "parent claims sidecar differs from official reader payload")
        if "coverage_sha256" in parent_record or "coverage_path" in parent_record:
            coverage_hash = parent_record.get("coverage_sha256")
            require(isinstance(coverage_hash, str) and coverage_hash in evidence_paths,
                    "parent coverage hash requires matching hash-bound coverage evidence")
            coverage_path = evidence_paths[coverage_hash]
            if "coverage_path" in parent_record:
                require(nonempty(parent_record["coverage_path"]), "parent coverage_path is malformed")
                stated_path = Path(parent_record["coverage_path"])
                if not stated_path.is_absolute():
                    stated_path = parent_dir / stated_path
                require(stated_path.resolve() == coverage_path.resolve(), "parent coverage_path mismatch")
            check_parent_state(read_json(coverage_path), identity, require_identity=True)

    adjudications = review.get("adjudications")
    require(isinstance(adjudications, dict), "adjudications must be an object")
    required = {f"layer2:{field}" for field, row in scores.items() if row["verdict"] != "SUPPORTED"}
    required.update(f"claim:{i}" for i, row in enumerate(claims["claims"]) if row["status"] != "SUPPORTED")
    valid = {f"layer2:{field}" for field in fields} | {f"claim:{i}" for i in range(len(claims["claims"]))}
    require(required <= set(adjudications), f"missing adjudications: {sorted(required - set(adjudications))}")
    require(set(adjudications) <= valid, "adjudication target is unknown")
    for flag in report["flagged_claims"]:
        require(isinstance(flag, dict) and flag.get("layer") == 2
                and flag.get("kind") == "partial" and flag.get("field") in scores,
                "official flagged_claims contains an unsupported or unrecognized flag")
        field = flag["field"]
        require(scores[field]["verdict"] == "PARTIAL" and f"layer2:{field}" in adjudications,
                "official flagged claim is inconsistent or lacks adjudication")
    for key, item in adjudications.items():
        require(isinstance(item, dict) and item.get("disposition") in ("source_faithful", "framing")
                and nonempty(item.get("rationale")), f"{key}: invalid disposition or rationale")
        ranges = item.get("raw_lines")
        require(isinstance(ranges, list) and bool(ranges), f"{key}: raw source lines required")
        for span in ranges:
            require(isinstance(span, list) and len(span) == 2
                    and all(type(v) is int for v in span)
                    and 1 <= span[0] <= span[1] <= len(source.splitlines()), f"{key}: invalid raw line range")
    return paper_id


def check_readiness(note_path: Path, audit_path: Path, review_path: Path) -> tuple[dict, int]:
    try:
        paper_id = _check(note_path, audit_path, review_path)
    except Blocked as exc:
        return {"ready": False, "errors": [str(exc)]}, 1
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"ready": False, "errors": [f"bad input: {exc}"]}, 2
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return {"ready": False, "errors": [f"malformed input record: {exc}"]}, 1
    return {"ready": True, "paper_id": paper_id, "errors": []}, 0


class ReadinessArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def main() -> int:
    parser = ReadinessArgumentParser(description=__doc__)
    parser.add_argument("note_path", type=Path)
    parser.add_argument("--audit-json", required=True, type=Path)
    parser.add_argument("--review-json", required=True, type=Path)
    try:
        args = parser.parse_args()
    except ValueError as exc:
        print(json.dumps({"ready": False, "errors": [f"bad input: {exc}"]}))
        return 2
    result, code = check_readiness(args.note_path, args.audit_json, args.review_json)
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
