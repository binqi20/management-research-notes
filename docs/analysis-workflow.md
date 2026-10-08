# Analysis and publication workflow

Current method: **v0.71.0, 2026-10-05**. This consolidates the October 4–5 review lessons without changing the v3 note schema, rubric-v3 verdict definitions, fitted-source algorithm or budgets. The [runbook](pipeline-runbook.md) governs execution; this document explains how to read, extract, check and close a paper. A new batch still needs an explicit assignment.

## Purpose and standard of evidence

The library supports literature discovery, comparison and return to the original paper. It is a research aid, not a substitute for reading the source when a claim matters to an argument. Its publication standard is a completed, traceable review of a specific version, with material errors corrected and remaining interpretive limits disclosed. It is not a claim of flawless accuracy.

Mechanical validation establishes format, hash currency and quotation membership. Independent readers assess meaning through different tasks. Parent adjudication resolves disagreements against the source. Agreement among these checks is useful evidence, but neither agreement nor a PASS label estimates corpus accuracy. The small historical samples also confound model era with pipeline maturity, rubric changes and paper mix; they do not establish a causal model ranking.

## 1. Freeze the assignment and source

Record the exact paper IDs, public baseline, note and immutable source hashes, paper/version identity, known retraction status, permitted fields, prompt/rubric/tool revisions, actual runtime model and required reader configuration. Keep corpus, cohort, wave and publication-subset counts distinct. Do not silently substitute a paper, model, source or interpretation when preflight fails. Obtain bibliographic metadata from the trusted manifest and use the existing metadata checks.

Do not regenerate existing extracted text to make a quote or number match. Check complete raw lines and adjacent columns; inspect the local PDF read-only if an equation, table header, footnote or layout remains ambiguous. Record the resolution and source location. A zero-hit text search is not evidence of absence.

## 2. Extract evidence before compressing it

Use a short private working record, sized to the paper; it is not a new public note schema. Before drafting, record:

| Evidence item | Required distinction |
|---|---|
| Study and sample | Study ID; recruited versus retained sample; people, observations, organizations, interviews, rounds and hours; dates and waves |
| Construct and measure | Definition, operationalization, scale, denominator, unit, data source; distinguish the focal construct from its proxy |
| Formula | Ordered operations and aggregation index: what is differenced, logged, standardized, multiplied, summed or averaged, and when |
| Design | Unit of analysis versus theory level; treatment/association; timing and identification assumptions; controls and mediators by study |
| Hypothesis and result | Prediction versus reported result; estimate, direction, uncertainty/significance, outcome, table/model and time window |
| Qualification | Comparator, dimension, direction and condition; which studies, tests, groups or cycles an “all” or robustness statement covers |
| Interpretation | Author argument versus empirical finding; proposed mechanism versus tested mediation; explicit recommendation versus analyst inference |

Read the reporting tables with their labels and footnotes, and the authors' prose. If they conflict, preserve and explain the discrepancy; do not silently choose one or invent a reconciliation. A theory paper needs propositions and scope, not an invented empirical sample. A qualitative count must retain the unit the paper actually counts.

## 3. Draft a faithful, concise note

Use the canonical [extraction prompt](extraction-prompt.md) or [augmentation prompt](augmentation-prompt.md). Keep per-study attribution, signed quantities, temporal meaning and result qualifications during compression. A nonsignificant result is not a reversal; marginal support is not unqualified confirmation. Do not imply causal identification beyond the design. Keep practical implications, audiences, limitations and future directions within what the paper states. Use the prescribed missing-information sentinel when warranted.

Before handing off, check cross-field consistency and every proper name, number, formula, direction and generalization. A broad evidence anchor supports traceability but does not certify every clause in its field. Preserve frontmatter, anchors and historical stamps during repairs unless their exact change is authorized.

## 4. Run mechanical checks, then blind readers

Validate the note and run `tools/check_numbers.py`. Resolve every zero-hit token and every `requires_raw_verification` item against raw lines, recording unit, referent and disposition. A glyph candidate is a lead, never a literal hit. Numeric presence cannot establish the correct study or meaning. Retain unresolved findings for adjudication rather than deleting a number solely to satisfy the checker.

For abstract extraction-layout conflicts, the optional [PDF-derived abstract check](abstract-evidence.md) reproduces hash-bound evidence from the original PDF. This exception applies only to the abstract; preserve the original source text, fitter, evidence-anchor checks and claims-quotation checks. Confirm complete abstract boundaries visually. Book reviews without standalone abstracts keep the heading with `Not reported in paper`.

Generate both prompts parent-side from the frozen note and the same standard fitted source. The writer/repairer, holistic reader and claims reader use distinct contexts. Record actual runtime metadata, not self-reported model names. The source is the final PDF-text block, not an identically worded heading quoted in the task. Read the supplied prompt completely in bounded chunks and recover truncated displays; loading bytes or reporting a line count does not prove reading.

The holistic reader applies rubric v3. The claims reader inventories atomic claims and explicitly judges qualifiers and comparisons. Match the inventory to clause occurrences, not merely unique words: a sentence mapped to a row can still have an unchecked tail. Serialization helpers may serialize judgments already made, never manufacture SUPPORTED rows, claim types or repeated placeholders. Preserve complete raw returns. Record each return before the next dispatch; use at most three workers with the current four-slot runtime and a lower cap if necessary.

The calibrated one-holistic-reader configuration remains specific to Stage 1 first-pass retrospective audits. Every newly written, augmented or repaired note requires both readers. Historical, user-approved retry/model/parent-coverage exceptions remain scoped to their original wave; this consolidation does not make them general waivers.

## 5. Adjudicate and stop at a defined boundary

The parent reads raw evidence for every disagreement, non-supported claim, doubtful SUPPORTED field and identified coverage gap. Bind the decision to note/source/reader hashes and exact field or row, record raw locations, and distinguish source-faithful compression, framing latitude, source-internal discrepancy, missing fitted evidence and a real defect. Parent coverage judgments stay visibly separate from reader judgments; never relabel the original reader output. An unresolved gap blocks publication unless the user authorizes a specifically documented exception.

Assemble all first-pass reports in the assigned wave before any repair. Follow the assignment's stop rules for UNSUPPORTED/CONTRADICTED and systemic failures; only the user may authorize continuation or change constants, protected fields or rules. Make the smallest authorized source-verified correction and obtain both fresh full-note readers on the repaired bytes. Grade each changed field substantive or precision, preserving initial findings separately from later discoveries.

Freeze the required checks before dispatch. Correct schema/provenance failures, but do not rerun valid audits merely to obtain unanimous SUPPORTED labels. Once prescribed readers, raw adjudications, current hashes and release checks are complete, close that version unless concrete new evidence creates a blocker. Faithful framing can be accepted with reasons; known factual errors cannot be waived in pursuit of closure. Retain unresolved notes outside a completed publication subset.

## 6. Check release evidence and publish only its scope

An official PASS is necessary but not sufficient. Use the read-only [publication-readiness checker](publication-readiness.md) with a hash-bound parent review. It checks recorded prerequisites, not semantic truth or runtime authenticity. The parent must verify the recorded assertions and the current pending-correction registry.

For a selective release, freeze an explicit list of eligible notes and a held list. Build SQLite, then CSV, then BibTeX from a clean public baseline plus only the selected note bytes. Never let incomplete worktree notes enter derived indexes. Reconcile parsed counts, verify selected diffs and unchanged bibliographic fields, preserve BibTeX when no exported field changed, and validate the selected notes. Skip CrossRef only with the unchanged-bibliography proof and a stated reason. Stage explicit public paths, inspect the staged diff, then verify the pushed commit, annotated tag and public release.

Disclose each corrected published clause, its source location and severity; distinguish repaired operations, fields and notes. Record residual judgments and coverage exceptions. The release explains what passed and what remains outside scope, without turning historical PASS totals into an accuracy guarantee.

## 7. Preserve work in the appropriate repository

| Destination | Contents |
|---|---|
| Public `management-research-notes` | Eligible notes and derived indexes; reusable code and synthetic tests; canonical methods, correction disclosures and release rationale |
| Private `synapse-codex-handoff` | Curated operating guidance, dated decisions, current queue and review summaries |
| Private `synapse-private-archive` | Filtered recovery evidence, ledgers, failed attempts, hashes and review records |

Keep full-paper sources, fitted prompts, credentials and raw runtime logs local. Private visibility does not remove copyright or secret-handling obligations. Inspect content as well as extensions: JSON diagnostics can embed long source text. Use a reviewed allowlist/manifest for a targeted backup, or the separately authorized snapshot procedure after inspecting its exclusions; verify uploaded hashes. Never erase failed attempts or rewrite history to make the record look cleaner. A checkpoint is preservation, not a completed audit or release.
