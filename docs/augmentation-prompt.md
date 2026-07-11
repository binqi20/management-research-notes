# Canonical Augmentation Prompt (v2 → v3 backfill)

Version: **aug-v1**

This is the prompt that upgrades one **existing, already-audited v2 note** to the
v3 schema by **adding** the three empirical sections and their evidence anchors —
and changing **nothing else**. It exists so the 2026 v3 backfill can enrich the
pre-v3 corpus without regenerating (and thereby risking) prose that has already
passed the two-layer faithfulness audit.

**This prompt is for v2 notes only.** v1 notes (no `evidence:` block) are never
augmented — they are fully re-extracted with the standard pipeline
(`docs/extraction-prompt.md`); see the runbook's "Backfill batches" section.
If the note you were assigned is not `extraction_version: "v2"`, STOP and report.

The rules for WHAT the three sections and three anchors must contain are defined
once, in [`docs/extraction-prompt.md`](extraction-prompt.md) — the sections
"Hypotheses, Data & Measures, and Key Findings (new in v3)" and "Evidence
anchors", including the scope-discipline rule, the sign/direction-fidelity rule
for Key Findings, the ≤25-word verbatim anchor rule, the two-column grep-verify
procedure, and the `"Not reported in paper"` escape valve. Read that file and
apply those rules exactly. This file defines only the DELTA mechanics.

---

## Inputs (read in this order)

1. `docs/extraction-prompt.md` — the v3 section and anchor rules (canonical).
2. `notes/<paper_id>.md` — the existing v2 note you are augmenting.
3. The paper's extracted text at the note's frontmatter `text_path` — the ONLY
   source for the new content. Never use training-data knowledge of the paper.

## The permitted delta — and nothing else

You may make exactly four kinds of change, all **insertions**, using surgical
edits (never rewrite the file wholesale — untouched regions must stay
byte-identical):

1. **Three new body sections**, each `**Heading**` + content, inserted at these
   exact positions (producing the canonical 11-section v3 order):
   - `**Hypotheses / Propositions**` — immediately after the
     `**Research Question**` section.
   - `**Data & Measures**` — immediately after the `**Mechanism Process**`
     section.
   - `**Key Findings**` — immediately after the new `**Data & Measures**`
     section.
2. **Three new evidence anchors**, appended at the end of the existing
   `evidence:` mapping, in this order:
   `hypotheses_source`, `measures_overview`, `findings_overview`.
   Every anchor value must be grep-verified against the text file BEFORE you
   write it (`grep -F "candidate phrase" "<text_path>"`), or be exactly
   `"Not reported in paper"` where the paper type permits.
3. **Version bump:** `extraction_version: "v2"` → `extraction_version: "v3"`.
4. **Provenance lines**, inserted immediately after the `extraction_version`
   line:
   ```yaml
   augmented_model: "<the model actually running this augmentation>"
   augmented_at: "<YYYY-MM-DD>"
   ```
   Never claim a model that did not run. `extraction_model` stays UNCHANGED —
   it truthfully records who wrote the six original prose fields.

## Paper-type rules for the delta

- `empirical-quantitative`: all three sections substantive; all three anchors
  real quotes (per the extraction-prompt rules).
- `empirical-qualitative` / `empirical-mixed`: Hypotheses / Propositions may be
  `Not reported in paper` (inductive studies); `hypotheses_source` then takes
  the escape valve. Data & Measures and Key Findings substantive.
- `conceptual` / `review`: sections may be `Not reported in paper` per the
  extraction-prompt table; `hypotheses_source` quotes a formal proposition if
  one exists, else escape valve; `measures_overview` and `findings_overview`
  take the escape valve (a review reporting meta-analytic results is the
  exception — see the extraction prompt).
- `editorial` / `book-review`: all three sections are `Not reported in paper`.
  **Leave the `evidence:` block exactly as found** — absent stays absent;
  present stays byte-identical with NO new keys (v3 requires none for these
  types).

## Forbidden

- Modifying, rewording, reformatting, or "improving" ANY existing content:
  the abstract, the six original prose sections, the APA citation, the
  bibliographic frontmatter, keywords/theory/topics, sample, methods, or any
  existing evidence anchor. If you believe an existing field is wrong, do NOT
  fix it — finish the augmentation and report the concern; the independent
  audit adjudicates existing content.
- Adding, removing, or reordering anything not listed in the permitted delta.
- Writing any file other than `notes/<paper_id>.md`.
- Running the Layer 2 audit (a fresh independent auditor does that).

## Verification (run both; one self-fix cycle allowed)

From `/Users/tangbinqi/Claude/Synapse`:

```bash
python3 tools/validate_note.py notes/<paper_id>.md --flag
python3 tools/verify_augmentation.py notes/<paper_id>.md
```

`verify_augmentation.py` mechanically proves the do-not-touch guarantee by
diffing against the git HEAD version of the note. If either check fails on a
mechanical issue (anchor not verbatim, wrong insertion position), you may
repair ONCE — re-selecting anchors from the text or fixing structure, never
inventing content — and re-run both. Two attempts maximum.

## Return contract

Report: `paper_id`; `status` (OK / FAIL / STOP) — STOP only if the note is not
v2 or the text file is missing/mismatched; `root_cause` on FAIL
(anchor_not_verbatim / structure / diff_guard / other); `validation_attempts`
(1 or 2); one short sentence of notes (e.g., which sections took the escape
valve), or a concern about existing content if you saw one.
