# Publication evidence check

Current tool contract: `publication-review-v1`, introduced in **v0.71.0**, with optional PDF-derived abstract evidence. This is a read-only consistency gate for changed notes that require both readers. It neither runs an audit nor edits an official report. Historical reports are not restamped. It is not the one-reader Stage 1 first-pass gate.

```sh
python3 tools/check_publication_readiness.py notes/<id>.md \
  --audit-json incoming/_audits/<id>.audit.json \
  --review-json incoming/_ledgers/<run>-evidence/publication-reviews/<id>.json
```

Output is JSON: `ready`, `errors`, and `paper_id` on success. Exit codes: **0** recorded prerequisites satisfied; **1** blocked or malformed evidence; **2** unreadable input or invalid command arguments. A successful result is not a semantic accuracy guarantee or publication authorization.

## Parent review record

Keep the review and its evidence private. Populate assertions only after actually checking them against the source and current pending-correction registry. Hash the note and loaded source using `audit_note.py`'s conventions; hash report and evidence files as raw bytes. Retain runtime metadata proving the reader contexts separately.

```json
{
  "schema_version": "publication-review-v1",
  "paper_id": "example-paper-id",
  "note_sha256": "<current audit-compatible note hash>",
  "text_sha256": "<current audit-compatible source hash>",
  "audit_sha256": "<current report byte hash>",
  "coverage_reviewed": true,
  "numeric_reviewed": true,
  "pending_corrections": [],
  "writer_contexts": ["<known writer/repairer context id>"],
  "readers": {
    "layer-2": {"context_id": "<holistic context>", "model": "gpt-6-astra"},
    "claims-v1": {"context_id": "<claims context>", "model": "gpt-5.6-sol"}
  },
  "evidence": [
    {"path": "../numeric-review.json", "sha256": "<byte hash>"},
    {"path": "../source-review.json", "sha256": "<byte hash>"},
    {"path": "../pending-corrections.json", "sha256": "<byte hash>"}
  ],
  "adjudications": {
    "claim:20": {
      "disposition": "source_faithful",
      "raw_lines": [[105, 108], [473, 514]],
      "rationale": "<source-based reason for retaining this exact claim>"
    }
  }
}
```

The example is a schema illustration, not evidence. Supply the actual models and contexts used. Each `evidence.path` is relative to the review file. Include both reader sidecars, numeric dispositions, source/coverage review, applicable authorization and the latest pending registry; the parent verifies their meaning and completeness. The tool requires at least one valid hash-bound evidence entry and validates referenced parent-review/coverage/claims artifacts when those references exist in the official report. It does not discover omitted pending proposals by itself.

When using the optional [PDF-derived abstract check](abstract-evidence.md), add
`"abstract_evidence": {"path": "../abstract-evidence/<id>.json", "sha256": "<file byte hash>"}`
to the parent review. The gate verifies this reference, reproduces the extraction
and checks the abstract. Without this field it uses the original extracted text.
A supplied stale record blocks readiness even if the original-text match passes.
The parent still verifies the complete PDF boundaries and all other note content.

Adjudication keys are `layer2:<field_key>` or `claim:<zero-based row index>`, bound to the report hash. Every non-SUPPORTED result needs a disposition (`source_faithful` or `framing`), nonempty rationale and valid raw-line ranges. These fields record a source judgment; adding a hash or line number does not make the judgment true. Parent-confirmed defects remain repair-class and cannot be waived by choosing an accepted disposition.

## What is checked

- Current paper identity and note/source/report hashes; exact holistic field set, passing mechanical/holistic results, compatible reader provenance and standard fitted input.
- Nonempty claims inventory, valid quotes/clauses through the existing parser, consistent summary and reader metadata; distinct reader contexts separate from declared writer contexts.
- Literal completion booleans, an explicitly empty pending list, current evidence hashes and explicit residual adjudications. Present contradictory diagnostics, unresolved embedded repairs or stale parent/coverage references block readiness.

Actual reading, source fidelity, full semantic coverage, omitted evidence and runtime identity require parent verification. The tool cannot infer them from Boolean assertions. The separate [analysis workflow](analysis-workflow.md) and runbook retain validation, source adjudication, all-reports-before-repair ordering, allowed-path checks, correct index scope and remote readback. Unresolved notes stay outside the selected release.
