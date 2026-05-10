---
description: Ingest a new monthly batch of academic papers into Synapse — runs the full pipeline (populate_manifest → pdf_to_text → prepare_paper → parallel extraction → validate_note → audit → build_index → export → verify_metadata) on a folder of PDFs, honoring every hard rule in CLAUDE.md.
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

Before doing anything else, re-read `CLAUDE.md` in this project. The five hard
rules there override any instinct to speed through:

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
that paper into a Synapse note. **Batch size: 8 concurrent agents.** Dispatch
a batch, wait for all 8 to return, then dispatch the next batch.

Use the following prompt template for each dispatch, filling in `<PAPER_ID>`:

> You are extracting a single paper for the Synapse knowledge base. This is
> one step in the `/synapse-ingest` workflow — do the extraction and report
> back, nothing more.
>
> **Inputs** (read in this order):
> 1. `CLAUDE.md` — the five hard rules at the top of the file. Especially
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
> `notes/<PAPER_ID>.md`. Then run these two checks, in order, and record
> the exit code plus the printed output of each:
>
>     python tools/audit_note.py    notes/<PAPER_ID>.md --flag
>     python tools/validate_note.py notes/<PAPER_ID>.md --flag
>
> These two tools check **different** things and must **both** pass.
>
> - `audit_note.py` runs the **two-layer faithfulness audit**. Layer 1
>   substring-checks every quote in the note's `evidence:` frontmatter
>   block against the extracted PDF text (same two-pass normalization the
>   abstract check uses). Layer 2 dispatches a fresh Claude subagent in a
>   cold context that reads `docs/audit-rubric.md`, the note body, and
>   the PDF, and returns per-prose-field verdicts
>   (`SUPPORTED` / `PARTIAL` / `UNSUPPORTED` / `CONTRADICTED`) for
>   research question, mechanism, theoretical contribution, practical
>   implication, limitations, and future research. On success writes
>   `incoming/_audits/<PAPER_ID>.audit.json`. On failure also writes
>   `incoming/_flagged/<PAPER_ID>.reason.txt` (because of `--flag`).
>   **Takes roughly 1–5 minutes per paper** — Layer 2 is an LLM call.
> - `validate_note.py` runs the **structural and vocabulary check**:
>   verbatim-abstract substring check, controlled-vocabulary topic slugs,
>   paper-type enum, custom analytic field enums, and the same Layer 1
>   evidence-anchor check (gated on `extraction_version: "v2"` — v1 notes
>   skip it and keep passing). Writes its own `.reason.txt` sidecar on
>   failure. Runs in well under a second.
>
> Run the audit **before** the validator. Both tools use the same `--flag`
> sidecar convention and neither moves the note file, so a note that fails
> the audit can still be validated for a more complete debugging picture.
> Run both unconditionally — don't short-circuit on audit failure.
>
> **Report one of four outcomes, under 150 words each:**
> - **OK** — both `audit_note.py` and `validate_note.py` exited zero.
> - **AUDIT_FAIL** — `audit_note.py` exited non-zero. Quote the audit
>   report's flagged claims verbatim: every Layer 1
>   "anchor not found in PDF" entry, plus every Layer 2
>   `UNSUPPORTED` / `CONTRADICTED` verdict with its `field` name and
>   `note:` text. Do NOT try to "fix" a fabricated anchor by rewriting the
>   note — that just papers over a faithfulness problem.
> - **FAIL** — `validate_note.py` reported errors (and the audit may or
>   may not also have failed; report both if so). Quote the validator's
>   error list verbatim. Do NOT try to "fix" a structural problem by
>   inventing content — that violates the no-invention rule.
> - **STOP** — you hit a hard-rule trigger: the trusted bib block
>   contradicts what the PDF text clearly says, the paper isn't scholarly
>   (dataset, website snapshot, book chapter without a DOI, etc.), or the
>   text block in the bundle is a different paper than the one named in
>   the bib block. Write a short `.reason.txt` file at
>   `incoming/_flagged/<PAPER_ID>.reason.txt` explaining what went wrong.
>   Do NOT write a `notes/` file.

## Step 3 — Aggregate outcomes

As each batch returns, log one line per paper using one of four prefixes:
`OK <paper_id>`, `AUDIT_FAIL <paper_id>`, `FAIL <paper_id>`, or
`STOP <paper_id>`. (A paper that fails BOTH the audit and the validator
gets logged as `AUDIT_FAIL` — the faithfulness failure is the more
important signal. The validator errors go into the summary alongside the
audit errors.) After all batches complete, compile:

- **OK count**, **AUDIT_FAIL count**, **FAIL count**, **STOP count**.
- The list of flagged paper IDs and the first line of each `.reason.txt`.
  Note that `AUDIT_FAIL` and `FAIL` both produce `.reason.txt` sidecars but
  in different shapes — audit sidecars list flagged claims and Layer 2
  verdicts, validator sidecars list error messages. When both tools flag
  the same paper, the audit sidecar overwrites the validator sidecar in
  the filesystem, so also print the validator errors in the batch report.
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

## Step 4 — Rebuild derived indexes

Once the note set is stable (no FAIL entries that can be fixed inline):

```bash
python tools/build_index.py
python tools/export_csv.py
python tools/export_bibtex.py
```

Then run a full-corpus validator sweep as a regression check:

```bash
python tools/validate_note.py notes/*.md
```

Expected: every existing note in `notes/` passes. If anything in the
pre-existing corpus suddenly fails, the new batch has touched something it
shouldn't — stop and investigate before continuing.

## Step 4.5 — Bibliographic-integrity check (mandatory)

Run the CrossRef cross-check on every note's bibliographic metadata. This
catches the class of error that v0.11.1 fixed (extracting the **online-first**
year instead of the **issue year**, which APA 7 requires) plus the broader
class of metadata errors that any manual manifest entry is prone to: typos
in titles, missing Oxford commas, swapped authors, null volume/issue/pages
on online-first papers that have since been issued.

```bash
python tools/verify_metadata.py
```

The tool checks **seven fields per note** against CrossRef (year, title,
journal, volume, issue, pages, authors). Exit code 0 if all selected fields
match for all checked notes; exit code 1 on any mismatch (suitable as a
pipeline gate).

Expected output for a clean batch: `MATCH` for every selected field across
every note, with one possible exception — `MISSING` rows for books / book
reviews / editorials that CrossRef doesn't carry full structured metadata
for. Those are not errors; they're absences.

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

Do NOT commit until verify_metadata returns clean (or you have explicit
notes in the commit message explaining each remaining mismatch as a
known false positive).

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
- CrossRef is free, fast (cached at `/tmp/crossref_cache/` after first run),
  and authoritative — it's the canonical DOI registry. There is no good
  reason to skip the check.

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
