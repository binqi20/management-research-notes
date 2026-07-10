---
description: Ingest a new monthly batch of academic papers into Synapse — runs the full pipeline (populate_manifest → lint_manifests → pdf_to_text → prepare_paper → parallel extraction → validate_note → audit → build_index → export → verify_metadata) on a folder of PDFs, honoring every hard rule in CLAUDE.md.
argument-hint: "<library/SOURCE/YYYY-MM/pdfs>"
---

# /synapse-ingest — monthly batch ingestion workflow

You are running the **Synapse monthly ingestion pipeline** on the folder passed
as `$ARGUMENTS`. This command automates everything from raw PDF to validated
note to rebuilt SQLite/CSV/BibTeX indexes, without re-explaining the workflow
each month.

**The target folder is:** `$ARGUMENTS`

If no argument was passed, **stop** and ask the user which `library/<source>/<year-month>/pdfs/`
folder they want to ingest.

---

## Non-negotiable rules (from CLAUDE.md)

Before doing anything else, re-read `CLAUDE.md` in this project. The seven hard
rules there override any instinct to speed through (the most load-bearing for
ingestion are summarized below):

1. **Never invent bibliographic fields.** Use only the manifest or CrossRef
   lookup. `Not reported in paper` is always an acceptable value.
2. **Verbatim means verbatim.** The `Abstract` section must be a contiguous
   substring of the extracted PDF text. `validate_note.py` will check this,
   now with soft-hyphen normalization on both sides.
3. **Stop and ask** when: the trusted manifest contradicts what the PDF text
   clearly says; >3 papers fail for the same reason in one batch; a file
   isn't a scholarly article.
4. **Stable IDs.** `{source-slug}-{year-month}-{first-author-slug}-{year}`,
   assigned once, never changed.
5. **One paper, one note.**

---

## Preconditions

Verify all of these **before** starting extraction. If any fail, stop and report.

1. `$ARGUMENTS` exists and resolves to a path of the form
   `library/<source>/<year-month>/pdfs/`.
2. The sibling `library/<source>/<year-month>/manifest.tsv` exists and has a
   header row containing at least: `title`, `first_author_last`, `year`,
   `saved_filename`, `doi`, `status`.
3. `docs/extraction-prompt.md` exists (canonical extraction prompt).
4. `index/topics.json` exists (controlled vocabulary — enforces topic tags).
5. `pdftotext` is on `PATH` (from the poppler package). Run `which pdftotext`
   to confirm; if missing, tell the user to `brew install poppler` and stop.

---

## Step 0 — Populate manifest from CrossRef (Tier 3, mandatory)

Before extraction, **upgrade the manifest with authoritative bibliographic
metadata from CrossRef**. The manifest's `title`, `first_author_last`, `year`,
`doi` columns are typically populated by hand (from journal TOCs); the
`volume`, `issue`, `pages` columns are usually missing entirely until this
step. Tier 3 fills the gaps and cross-checks existing fields against the
canonical DOI registry.

```bash
python tools/populate_manifest.py library/<source>/<year-month>/manifest.tsv --apply --fix-year
```

This:

1. Queries CrossRef per DOI and **adds `volume`, `issue`, `pages` columns**
   to the manifest (or upgrades them if already present).
2. Cross-checks `year` against CrossRef's `published-print` date (APA 7
   issue year). If `--fix-year` is passed, year mismatches are
   auto-corrected from CrossRef and a warning is emitted for the audit
   trail; without `--fix-year`, mismatches only warn.
3. Cross-checks `title` and `journal`. These are warning-only — title
   variations between manifest and CrossRef are common (smart-quote
   normalization, missing Oxford commas) and need human review.
4. Writes the upgraded manifest back atomically.

**Why this is Step 0 and not deferred to Step 4.5:** if the manifest's
`year` is wrong (the v0.11.1 bug class — manifest stores online-first year
instead of issue year), then prepare_paper.py would build extraction
bundles with the wrong year, and the extraction agent would write the
wrong year into note frontmatter and APA citations. v0.11.1 patched 48
such cases retroactively; Tier 3 catches them BEFORE extraction. Same
logic for null vol/issue/pages — without Step 0, prepare_paper.py would
pass `null` to the extraction agent, which would write `null` into the
note. v0.11.2 cleaned up 21 such cases retroactively.

**Expected output for a clean batch:** "X row(s) have CrossRef-derived
changes to ('volume', 'issue', 'pages')" with no warnings (or only
expected ones — e.g., year auto-corrections from online-first to issue
year, which are exactly what Tier 3 is designed to apply). If there are
unexpected warnings (e.g., title mismatch, journal mismatch), stop and
investigate before continuing.

**If `--fix-year` auto-corrects any years**, the manifest's `year`
column is now authoritative. No manual cleanup needed afterwards;
Step 4.5 (verify_metadata.py) confirms everything round-trips cleanly.

---

## Step 0.5 — Manifest structural lint (mandatory)

After populate_manifest fills in the bibliographic columns, **lint the
manifest's structure** before extraction begins. This catches the class
of bug that v0.13.2 surfaced retroactively: a manifest row that is
*internally consistent but structurally wrong* (e.g., the full given+family
name captured in `first_author_last` instead of just the family name).
Such rows propagate cleanly through every downstream step — they pass
validation, pass audit, pass `verify_metadata` — because no other gate
asks "is the manifest field structurally well-formed?"

```bash
python tools/lint_manifests.py --manifest library/<source>/<year-month>/manifest.tsv
```

The linter runs two tiers of check:

- **Heuristic (fast, no network)**: flags numeric, empty, comma-containing,
  or overly-long `first_author_last` values; out-of-range years; malformed
  DOIs; missing PDF files referenced by `status=downloaded`.
- **Authoritative (CrossRef per-DOI)**: compares manifest `first_author_last`
  against CrossRef's first-author family name (after accent-fold). A
  mismatch is the **D'Amico bug class**: the manifest captured a full
  given+family name instead of just the family.

Expected output for a clean batch: `✓ All checks passed` for the
manifest, exit code 0.

**If the linter flags rows:** stop. Triage by the message:

- **`first_author_last`: contains comma** → manifest has `"Last, First"`
  instead of just `Last`. Fix the manifest row.
- **`first_author_last`: unusually long (X chars)** → likely full-name
  capture. Cross-check with the linter's CrossRef output and the PDF
  byline, then fix the manifest row to just the family name.
- **`crossref:` mismatch** → either a D'Amico-class bug (fix the
  manifest) OR a legitimate compound surname where CrossRef has the
  formal version and the manifest uses the citation short form (add an
  entry to `tools/known_compound_surnames.json` with a dated rationale —
  a data edit, same pattern as `tools/known_crossref_issues.json`).
- **`saved_filename`: file not found** → either rename the PDF to match
  the manifest, or update the manifest to match the actual PDF on disk.

Do NOT proceed to Step 1 until the linter exits 0 (or every remaining
flag is documented as an allowlisted false positive).

**This step is mandatory because:**

- The manifest is the trusted source for bibliographic metadata. If a
  manifest row has a structural anomaly, every downstream step inherits
  it. The lint catches the anomaly at the cheapest possible point.
- `populate_manifest.py` (Step 0) populates fields but does NOT validate
  the structure of pre-existing fields. `verify_metadata.py` (Step 4.5)
  audits notes, not manifest rows. The linter fills the only remaining
  gap.
- v0.13.2 ran this linter for the first time and found 6 latent
  D'Amico-class bugs that had been in the library since the original
  NBS-2026-02 ingestion (v0.2.0). Without the linter, those would have
  remained latent until the next manual cleanup pass — and any new batch
  with similar manifest-population errors would compound the problem.

---

## Step 1 — Prepare all bundles

Run the deterministic first half of the pipeline:

```bash
python tools/ingest_batch.py "$ARGUMENTS"
```

This walks the folder and, for each PDF:

- Runs `tools/pdf_to_text.py` → writes `library/<source>/<year-month>/text/<stem>.txt`
- Runs `tools/prepare_paper.py` → looks up the manifest row and writes
  `incoming/_bundles/<paper_id>.bundle.txt` containing the trusted bib block
  plus the full extracted text.

Expected outcome: one bundle per valid PDF, printed at the end as
`bundles ready: N  failed: M  total PDFs: P`. Any `failed` entries mean the
PDF was unreadable or had no matching manifest row — **stop and show the
failures to the user** before proceeding.

## Step 2 — Extract notes in parallel batches

For every bundle produced in step 1, dispatch one `Agent` subtask to extract
that paper into a Synapse note. **Synapse agent-slot policy: keep at most 6
active extraction agents per wave.** Do not attempt larger waves unless the user
explicitly changes this policy after a new cap test. Dispatch a wave, wait for
workers to return, record each result, close each completed agent thread, then
spawn the next wave.

If spawning hits an agent-cap error, timeout, or coordination problem, fall back
from 6 to 5, then 3, then serial execution. Do not weaken the extraction/audit
separation to recover speed.

Extraction agents write notes only. They must not run the semantic Layer 2 audit
on their own work, and they must not produce the external Layer 2 JSON. The
audit layer is deliberately separated into Step 2.5 so the auditor has fresh
context and no prior commitment to the note's claims.

Use the following prompt template for each dispatch, filling in `<PAPER_ID>`:

> You are extracting a single paper for the Synapse knowledge base. This is
> one step in the `/synapse-ingest` workflow — do the extraction and report
> back, nothing more.
>
> **Inputs** (read in this order):
> 1. `CLAUDE.md` — the seven hard rules at the top of the file. Especially
>    "never invent bibliographic fields" and "verbatim means verbatim."
> 2. `docs/extraction-prompt.md` — the canonical 17-field extraction prompt.
>    Follow it literally; the structure of the output note is non-negotiable.
> 3. `index/topics.json` — the full topic vocabulary. Every tag in the note's
>    frontmatter `topics:` field must be drawn from here (1–4 domain/subtopic
>    tags, plus any number of context tags).
> 4. `incoming/_bundles/<PAPER_ID>.bundle.txt` — trusted bib block + full PDF
>    text + paper_id. Treat the bib block as authoritative.
>
> **Output**: use the `Write` tool to create exactly one file at
> `notes/<PAPER_ID>.md`. Then run this structural check and record the exit
> code plus printed output:
>
>     python tools/validate_note.py notes/<PAPER_ID>.md --flag
>
> - `validate_note.py` runs the **structural and vocabulary check**:
>   verbatim-abstract substring check, controlled-vocabulary topic slugs,
>   paper-type enum, custom analytic field enums, and the same Layer 1
>   evidence-anchor check (gated on `extraction_version: "v2"` — v1 notes
>   skip it and keep passing). Writes its own `.reason.txt` sidecar on
>   failure. Runs in well under a second.
>
> Do not run `tools/audit_note.py` from the extraction agent. The independent
> auditor in Step 2.5 will run Layer 2 and produce the official audit report.
>
> **Report one of four outcomes, under 150 words each:**
> - **OK** — `validate_note.py` exited zero.
> - **FAIL** — `validate_note.py` reported errors. Quote the validator's
>   error list verbatim. Do NOT try to "fix" a structural problem by
>   inventing content — that violates the no-invention rule.
>   - **Common Layer 1 failure pattern: anchors not contiguous in the
>     extracted text**, even though they look contiguous in the PDF.
>     Cause: two-column journal layouts get linearized by `pdftotext` so
>     a sentence wrapping across the column break has unrelated col-2
>     text spliced into it. **Fix**: re-dispatch the extraction agent
>     with the explicit instruction to use the `Grep`/`Read` tools on
>     the extracted text file (`library/<source>/<issue>/text/...`) to
>     verify each candidate anchor is actually a substring before writing
>     it. Prefer anchors that fit within a single physical line — abstract
>     sentences, table cells, captions, intra-paragraph phrases. The
>     extraction prompt's "How to choose anchors that survive validation"
>     section has the full guidance.
> - **STOP** — you hit a hard-rule trigger: the trusted bib block
>   contradicts what the PDF text clearly says, the paper isn't scholarly
>   (dataset, website snapshot, book chapter without a DOI, etc.), or the
>   text block in the bundle is a different paper than the one named in
>   the bib block. Write a short `.reason.txt` file at
>   `incoming/_flagged/<PAPER_ID>.reason.txt` explaining what went wrong.
>   Do NOT write a `notes/` file.

## Step 2.5 — Independent Layer 2 audit

After notes validate structurally, dispatch separate GPT-5.5 auditor agents.
**Keep at most 6 active auditor agents per wave.** Do not attempt larger waves
unless the user explicitly changes this policy after a new cap test. Do not mix
extraction and audit waves for the same issue. As with extraction, record each
returned audit result, close the completed auditor thread, then spawn the next
wave.

If an audit-agent spawn hits an active-agent cap, timeout, or coordination
problem even at 6, fall back to 5, then 3, then serial execution while
preserving auditor independence. Each auditor handles exactly one note. The
preferred input is the self-contained audit prompt:

1. Run `python tools/audit_note.py notes/<PAPER_ID>.md --prompt-only` and read
   its output — it contains the current rubric, the note body, and the
   anchor-aware fitted PDF text (so what the auditor sees is exactly what the
   assembled report's `audit_context` records).
2. `tools/audit_note.py` usage notes for `--layer-2-json` (provenance shape).

(Reading `docs/audit-rubric.md`, the note, and the raw extracted text directly
is a legacy fallback — it can diverge from the recorded `audit_context` on
long papers.)

The auditor must not read the extraction agent's reasoning, drafts, chat
transcript, or self-evaluation. It emits a JSON file at
`incoming/_audits/<PAPER_ID>.layer2.json` with this top-level shape:

```json
{
  "provenance": {
    "paper_id": "<PAPER_ID>",
    "note_sha256": "<sha256 of current note text>",
    "text_sha256": "<sha256 of current extracted PDF text>",
    "rubric_version": "v2",
    "auditor_model": "<model name>",
    "generated_at": "<UTC ISO timestamp>",
    "dispatch_mode": "codex-independent-agent"
  },
  "layer_2": {
    "overall": "pass",
    "scores": {
      "research_question": {
        "verdict": "SUPPORTED",
        "confidence": "high",
        "evidence_page_hint": null,
        "note": "..."
      }
    }
  }
}
```

The `scores` object must include every prose field the note contains, per
`docs/audit-rubric.md` (rubric v2): for **v1/v2 notes**, the six fields
`research_question`, `mechanism_process`, `theoretical_contribution`,
`practical_implication`, `limitations`, `future_research`; for **v3 notes**,
those six plus `hypotheses`, `data_measures`, and `key_findings` (nine total).
Missing fields are an audit error, not an implied pass — assembly rejects the
JSON. `rubric_version` must be `"v2"`; a `"v1"` stamp is rejected.

The parent operator then assembles the official report:

```bash
python tools/audit_note.py notes/<PAPER_ID>.md \
  --layer-2-json incoming/_audits/<PAPER_ID>.layer2.json \
  --auditor-model <model name> \
  --flag
```

This command verifies Layer 1 anchors, validates the external Layer 2 provenance
against the current note/PDF hashes, writes
`incoming/_audits/<PAPER_ID>.audit.json`, and writes
`incoming/_flagged/<PAPER_ID>.reason.txt` only if the audit fails.

## Step 3 — Aggregate outcomes

As each batch returns, log one line per paper using one of four prefixes:
`OK <paper_id>`, `AUDIT_FAIL <paper_id>`, `FAIL <paper_id>`, or
`STOP <paper_id>`. (A paper that fails BOTH the audit and the validator
gets logged as `AUDIT_FAIL` — the faithfulness failure is the more
important signal. The validator errors go into the summary alongside the
audit errors.) After all batches complete, compile:

- **OK count**, **AUDIT_FAIL count**, **FAIL count**, **STOP count**.
- The list of flagged paper IDs and the first line of each `.reason.txt`.
  Audit reports live in `incoming/_audits/<PAPER_ID>.audit.json`; validator
  failures and audit failures may both write a `.reason.txt`, so preserve the
  printed validator output in the batch report instead of relying on one shared
  sidecar to carry every failure detail.
- **Systemic validator-failure check**: if ≥3 papers fail VALIDATION for the
  same root-cause error (e.g., "topic slug X not in index/topics.json", or
  "abstract is not a verbatim substring"), **stop and ask** the user — this
  signals that the extraction prompt or the topic vocabulary needs
  tightening, not that the notes need individual fixing.
- **Systemic audit-failure check**: if ≥3 papers fail the AUDIT for the
  same root-cause reason (e.g., >3 papers have a fabricated `sample_n`
  anchor, or >3 papers have an `UNSUPPORTED` verdict on
  `theoretical_contribution`), **stop and ask** the user — same pattern as
  the validator rule above. A flood of audit failures usually means the
  extraction prompt is drifting in a specific way, or the rubric is
  miscalibrated, or the PDF text is being corrupted by two-column
  concatenation — NOT that the individual notes need hand-editing.

## Step 4 — Issue-level closeout and derived indexes

Once the note set is stable (no FAIL entries that can be fixed inline):

```bash
python tools/build_index.py
python tools/export_csv.py
python tools/export_bibtex.py
```

Run these three commands **sequentially**. Do not export CSV or BibTeX in
parallel with `build_index.py`; the exporters read `index/synapse.db`, so they
must wait until the SQLite rebuild has finished. After the rebuild, verify that
the SQLite paper count, CSV data-row count, and BibTeX `@article` count agree
and that the new issue has the expected number of records.

For an ordinary issue-level ingest where only a bounded set of notes changed,
close out the issue with targeted gates:

- Validate the changed/touched notes, e.g. `python tools/validate_note.py
  notes/<issue-paper-id-prefix>*.md`.
- Scan the issue's official audit reports in `incoming/_audits/` and confirm
  no `PARTIAL`, `UNSUPPORTED`, or `CONTRADICTED` verdict remains unresolved.
- Confirm counts agree: manifest rows = PDFs = extracted text files = bundles =
  notes = official audit reports.
- Run the scoped CrossRef metadata check described in Step 4.5.

Full-library local note validation is useful but not mandatory for every
issue-level run. At the current corpus size it may still be acceptable as
cautious extra assurance:

```bash
python tools/validate_note.py notes/*.md
```

Run this full local note-validation sweep when the run changes schema,
validator behavior, parser/indexer behavior, the extraction prompt, many notes
by batch edit or migration, global metadata, or when prior validation state is
stale/unreliable, a systemic issue is suspected, a volume/release/milestone is
being closed, an official research output is being prepared, or the user
explicitly asks for it. If targeted issue validation already gives equivalent
assurance, do not treat the full local validation sweep as a ritual.

## Step 4.5 — Bibliographic-integrity check (mandatory)

For ordinary issue closeout, identify the changed issue paper IDs from the issue
note filenames, bundle filenames, or private issue ledger, then run the CrossRef
cross-check with `--paper-id` once per note (or an equivalent small loop):

```bash
python tools/verify_metadata.py --quiet --paper-id <PAPER_ID>
```

The tool checks **seven fields per note** against CrossRef (year, title,
journal, volume, issue, pages, authors). Exit code 0 if all selected fields
match for all checked notes; exit code 1 on any mismatch (suitable as a
pipeline gate). For an issue release (or a volume-scope sweep), scoped CrossRef
over the changed notes is sufficient when no global metadata code, schema,
prompt, or indexer change occurred. Full-library CrossRef verification is more expensive
than local note validation, so do not treat it as a ritual. Reserve
`python tools/verify_metadata.py --quiet` for real high-risk triggers:
metadata parsing or comparison logic changed globally, `verify_metadata.py`
comparison behavior changed globally, schema/indexer changes affect metadata
fields, a batch migration or global metadata transformation occurred, systemic
metadata drift is suspected, the prior validation state is stale or unreliable,
the user explicitly requests it, or a major public milestone justifies the
network cost.

A narrow `tools/known_crossref_issues.json` addition for a newly added paper does
not by itself trigger a full-library CrossRef sweep, because it cannot affect
unrelated notes. Treat that as a scoped data exception and rerun the scoped
check for the affected issue or volume. A global change to CrossRef parsing,
normalization, comparison, or field-selection logic is different and should use
the full-library sweep.

Expected output for a clean scoped check: every changed note matches CrossRef,
with one possible exception — `MISSING` rows for books / book reviews /
editorials that CrossRef doesn't carry full structured metadata for. Those are
not errors; they're absences.

**If the script reports MISMATCH:** stop and triage by field:

- **year mismatch** → manifest has the wrong year. Fix manifest's `year`
  column (CrossRef `published-print` is authoritative), re-run extraction
  for the affected notes. This is the v0.11.1 case.
- **title / journal / authors mismatch** → manifest has a typo or wording
  difference. Decide which is correct (CrossRef is usually right but
  occasionally has its own data-quality issues — eyeball before fixing).
- **volume / issue / pages mismatch** with `note: null` → online-first paper
  whose issue assignment came after manifest entry. Backfill the manifest.
- **volume / issue / pages mismatch** with concrete values on both sides →
  real conflict; investigate.

Do NOT commit until the required metadata-verification scope returns clean (or
you have explicit notes in the commit message explaining each remaining
mismatch as a known false positive).

This step is mandatory because:

- The manifest is treated as the trusted source for bibliographic metadata
  (CLAUDE.md hard rule 1), but the manifest itself is not automatically
  validated against any external authority. Without this check, a wrong
  field in the manifest silently propagates through the entire pipeline —
  exactly the bug v0.11.1 patched after a 27%-of-library systematic error
  surfaced from a single user check against Google Scholar.
- The audit layers (Layer 1 anchors, Layer 2 prose) verify content against
  the source PDF. They do NOT cross-check bibliographic metadata. Errors
  in title / authors / volume / etc. are invisible to them.
- For scoped checks, CrossRef is free and usually fast once cached at
  `/tmp/crossref_cache/`; it is also authoritative as the canonical DOI
  registry. There is no good reason to skip the required scoped check.

**Useful flags:**

- `--field year` — check only the year (fastest, used as the v0.11.1 gate)
- `--field year,title,journal` — check a subset
- `--quiet` — suppress per-field summary, only show mismatches
- `--tsv` — machine-readable output for scripting
- `--paper-id <id>` — check a single paper
- `--no-cache` — bypass cache and refetch from CrossRef

The legacy `tools/verify_years.py` is preserved as a year-only alias for
back-compat with v0.11.1 docs and scripts; it is exactly equivalent to
`verify_metadata.py --field year`.

## Step 5 — Sanity checks

Quick database peek to confirm the batch landed:

```bash
sqlite3 index/synapse.db "SELECT COUNT(*) FROM papers;"
sqlite3 index/synapse.db \
  "SELECT paper_type, COUNT(*) FROM papers GROUP BY 1 ORDER BY 2 DESC;"
sqlite3 index/synapse.db \
  "SELECT topic, COUNT(*) FROM topics GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
```

Cross-check the paper count against the manifest row count minus the flagged
papers. If they don't match, identify the delta before continuing.

## Step 6 — Report

Deliver a closing report to the user with:

- Folder processed and paper count.
- OK / FAIL / STOP tally.
- Names of any flagged paper IDs and the one-line reason for each.
- Top 10 topics surfaced in this batch (from the SQLite query above).
- Whether the batch is commit-ready (yes if all notes pass and no STOPs are
  pending user intervention; no otherwise).
- Suggested next command if the user wants to publish this batch (e.g.,
  "`git add notes/ index/ library/.../manifest.tsv && git commit -m ...`").

**Do NOT commit or push on the user's behalf** unless they explicitly ask.
The commit message style lives in git log — follow that style when the user
does ask.

---

## Failure-recovery playbook

If an agent returns **STOP** with a manifest-vs-text contradiction (the
canonical case is "the PDF for Paper X actually contains the text of Paper Y"),
do NOT auto-retry — that would waste a whole agent slot on a file problem.
Surface the paper to the user with:

- The path to the reason file (`incoming/_flagged/<paper_id>.reason.txt`).
- The DOI from the manifest (so they can re-download from the publisher).
- Whether Unpaywall has an open-access copy (run
  `curl -sS "https://api.unpaywall.org/v2/<doi>?email=<user-email>"` and check
  the `is_oa` field).

The user will either replace the PDF (re-run `/synapse-ingest` on just the
affected PDFs), update the manifest, or decide the paper is out of scope.

If a batch has >20% STOPs, something is systemically wrong with the upstream
download pipeline — stop and ask the user to investigate before producing
any notes, because running extractions against bad text wastes agent budget.

---

## What this command does NOT do

- It does not re-download PDFs. The expectation is that PDFs are already on
  disk (via a separate scraper / institutional download workflow).
- It does not modify `index/topics.json`. If a batch would benefit from a new
  topic slug, the user must add it explicitly before ingestion.
- It does not commit or push. Publication is a separate, human-in-the-loop
  decision.
- It does not run on the public clone where `library/*/text/` is absent —
  that tree is gitignored because the PDFs are copyrighted. Run locally only.
