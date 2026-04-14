---
description: Ingest a new monthly batch of academic papers into Synapse — runs the full pipeline (pdf_to_text → prepare_paper → parallel extraction → validate_note → build_index → export) on a folder of PDFs, honoring every hard rule in CLAUDE.md.
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
> `notes/<PAPER_ID>.md`. Then run:
>
>     python tools/validate_note.py notes/<PAPER_ID>.md
>
> **Report one of three outcomes, under 150 words each:**
> - **OK** — the note was written and `validate_note.py` exited zero.
> - **FAIL** — validator reported errors. Quote the validator's error list
>   verbatim. Do NOT try to "fix" a structural problem by inventing content —
>   that violates the no-invention rule.
> - **STOP** — you hit a hard-rule trigger: the trusted bib block contradicts
>   what the PDF text clearly says, the paper isn't scholarly (dataset,
>   website snapshot, book chapter without a DOI, etc.), or the text block
>   in the bundle is a different paper than the one named in the bib block.
>   Write a short `.reason.txt` file at `incoming/_flagged/<PAPER_ID>.reason.txt`
>   explaining what went wrong. Do NOT write a `notes/` file.

## Step 3 — Aggregate outcomes

As each batch returns, log one line per paper: `OK <paper_id>`, `FAIL <paper_id>`,
or `STOP <paper_id>`. After all batches complete, compile:

- **OK count**, **FAIL count**, **STOP count**.
- The list of flagged paper IDs and the first line of each `.reason.txt`.
- **Systemic-failure check**: if ≥3 papers fail for the same root-cause error
  (e.g., "topic slug X not in index/topics.json", or "abstract is not a
  verbatim substring"), **stop and ask** the user — this signals that the
  extraction prompt or the topic vocabulary needs tightening, not that the
  notes need individual fixing.

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
