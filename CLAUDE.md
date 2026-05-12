# Working in Management Research Notes

This folder is an academic knowledge base for management / business sustainability
research. Read this file before doing anything in this folder.

## What this project is

- `notes/` is a Zettelkasten-style knowledge base — one Markdown file per academic paper,
  with YAML frontmatter for structured metadata and a markdown body for the analytic
  distillation (research question, mechanism, contribution, limitations, etc.).
- `library/{Source}/{Year-Month}/pdfs/` holds the original PDFs. Each has a sibling
  `text/` folder with the extracted plain text.
- `index/synapse.db` is a SQLite index **derived** from `notes/`. Same for
  `index/papers.csv` and `index/library.bib`. Never edit these by hand — they will be
  overwritten by `tools/build_index.py`.
- The user is a researcher who will use these notes for literature reviews and
  theoretical development. Accuracy matters more than speed.

## Hard rules

1. **Never invent bibliographic fields.** Title, authors, year, journal, DOI,
   volume/issue/pages — these come only from `library/.../manifest.tsv` (the trusted
   source) or, if missing there, from CrossRef looked up by DOI. If a field is unknown,
   write `Not reported in paper`. Never guess. The manifest is the trusted source but
   it is hand-entered and error-prone, so the project uses **two CrossRef-based gates
   that bookend the pipeline**:
   - **Before extraction (Tier 3, mandatory):** run
     `python tools/populate_manifest.py library/<source>/<issue>/manifest.tsv --apply --fix-year`
     to upgrade the manifest with `volume`, `issue`, `pages` columns from CrossRef
     and auto-correct any year mismatches against `published-print` (APA 7 issue
     year). This is Step 0 of `/synapse-ingest` and prevents wrong-year/null-vol
     errors from ever propagating into note frontmatter.
   - **After extraction (Tier 2, mandatory):** run `python tools/verify_metadata.py`
     to cross-check every note's bibliographic fields (year, title, journal,
     volume, issue, pages, authors) against CrossRef. This is Step 4.5 of
     `/synapse-ingest`, the last gating step before commit.

   v0.11.1 fixed 48 issue-year mismatches (27% of the library) where the manifest
   had silently stored the *online-first* year — only an external cross-check
   surfaced this. v0.11.2 fixed 21 papers' missing volume/issue/pages by
   backfilling from CrossRef. v0.12.0 introduced Tier 3 (`populate_manifest.py`)
   so future batches never need this kind of cleanup. A clean `verify_metadata`
   run is a precondition for committing new notes. The legacy `tools/verify_years.py`
   is preserved as a year-only alias and is equivalent to
   `verify_metadata.py --field year`.
2. **Verbatim means verbatim.** When the extraction prompt says "extract the abstract
   verbatim," the text in the note must appear as a contiguous substring of the
   extracted PDF text (modulo whitespace). The validator will check this.
3. **Notes are the source of truth.** If you need to fix a paper's metadata, re-run
   `tools/ingest_paper.py` for that paper. Don't edit `synapse.db` directly. Don't edit
   a note's frontmatter by hand unless you are also planning to rebuild the index.
4. **Stable IDs.** Every paper has a `paper_id` like `nbs-2026-02-spoor-2026` that is
   derived from `{source-slug}-{year-month}-{first-author-slug}-{year}`. Once assigned,
   it never changes. The note file is `notes/{paper_id}.md`.

   *Historical exception — the v0.13.x cleanup cohort (2026-05-12):* 11 paper_ids
   were renamed in a single bounded cleanup pass after `slugify()` was updated
   to fold diacritics and strip apostrophes (so "Soublière" → `soubliere`
   instead of `soubli-re`, "D'Amico" → `damico` instead of `d-amico`, etc.)
   AND after `tools/lint_manifests.py` was built and surfaced 6 additional
   manifest-population bugs of the same class. The cohort closed in two
   releases:

   - **v0.13.1** (5 papers): renames surfaced by manual inspection during
     the slugify migration — Pérezts, Soublière, two Grégoire papers, D'Amico.
   - **v0.13.2** (6 papers): renames surfaced when `lint_manifests.py` was
     built and run for the first time — Anjier Chen, Chang Lu, Yuliya Snihur,
     Stella Seyb, Ahmed Sewaid, Nuno Clara (all had full given+family names
     captured in the manifest's `first_author_last` column instead of just
     the family name).

   This was a **deliberate, bounded one-time cleanup pass** taken when the
   library was small (197 notes) and had no known external citations by
   paper_id. The "cohort" framing matters: the right rule for future agents
   is **"when you build a detector for a known bug class, run it once and fix
   everything it finds before declaring the cohort closed"** — not "fix what
   you happened to notice manually." The 11-paper cohort is closed; future
   renames should be exceptional, well-justified, and explicitly documented.
   The rule's "once assigned, never changes" invariant remains in force for
   all post-v0.13.2 paper_ids.
5. **Validate before committing.** After producing or editing a note, run
   `python tools/validate_note.py notes/<id>.md` and only proceed if it passes (or
   move the note to `incoming/_flagged/` with a `.reason.txt`).
6. **One paper, one note.** Never split a paper across multiple notes. Never merge two
   papers into one note.
7. **Faithfulness is checked, not assumed.** Every v2 note must carry an `evidence:`
   frontmatter block whose quotes are verbatim substrings of the PDF text (same
   two-pass normalization the abstract check uses). The Layer 1 substring check is
   mechanical and deterministic — fabricated anchors will fail `tools/validate_note.py`
   and `tools/audit_note.py` identically. Layer 2 dispatches a fresh cold-context
   Claude subagent that scores the prose fields (research question, mechanism,
   theoretical contribution, practical implication, limitations, future research)
   against the PDF via the rubric at `docs/audit-rubric.md`. Both layers run
   automatically inside `/synapse-ingest`; `/audit-note <paper_id>` re-runs them on
   a single note on demand. v1 notes are exempt via an `extraction_version` gate.

## When the user asks "what's in the library?"

- For aggregate questions ("how many papers use stakeholder theory?"), query the SQLite
  index: `sqlite3 index/synapse.db "SELECT theory, COUNT(*) FROM theories GROUP BY 1"`.
- For specific lookups ("show me the Spoor 2026 paper"), use `Read` on
  `notes/nbs-2026-02-spoor-2026.md`.
- For full-text search across abstracts and analytic fields, use the FTS5 virtual table
  in SQLite, or `Grep` over `notes/`.
- For literature-review work, pull the matching notes into context and synthesize from
  them. Always cite using the APA citation in each note's body — that's the trusted
  citation, with the DOI you can verify.

## When ingesting a new PDF

1. Run `tools/pdf_to_text.py <pdf>` to produce a plain-text version.
2. Run `tools/prepare_paper.py <pdf>` to look up the trusted bibliographic metadata
   from the manifest and produce an extraction bundle (text + bib + the canonical
   extraction prompt) in `incoming/_bundles/`.
3. Read the bundle, apply the extraction prompt to the text, and write the resulting
   note to `notes/{paper_id}.md` using the `Write` tool. The bundle tells you exactly
   what `paper_id` to use and what frontmatter is mandatory.
4. Run `python tools/audit_note.py notes/{paper_id}.md --flag`. This is the
   two-layer faithfulness audit: Layer 1 substring-checks the `evidence:` anchors
   against the PDF text, Layer 2 dispatches a fresh cold-context Claude subagent
   that scores the six prose fields against `docs/audit-rubric.md`. On fail, writes
   `incoming/_audits/{paper_id}.audit.json` and `incoming/_flagged/{paper_id}.reason.txt`.
   Takes roughly 1–5 minutes per paper — the Layer 2 subagent is the dominant cost.
5. Run `python tools/validate_note.py notes/{paper_id}.md`. If it fails, fix the
   note OR move it to `incoming/_flagged/` with a `.reason.txt` and report what
   went wrong.
6. Run `python tools/build_index.py` to update the SQLite index.

## Things that should make you stop and ask the user

- A field in the trusted manifest contradicts what the PDF text clearly says (e.g.,
  the manifest year is 2025 but the PDF cover page says 2026). Don't silently pick one.
- The validator fails for the same reason on more than 3 papers in a single batch —
  this means the prompt or the validator needs to change, not the notes.
- A paper appears to be a dataset, a website snapshot, or otherwise not a peer-reviewed
  scholarly article. The pipeline is for scholarly articles only.

## Things that are allowed without asking

- Re-running ingestion on a paper that already has a note (it should be deterministic;
  the new note replaces the old one, and `extraction_version` is bumped if the prompt
  changed).
- Updating `index/topics.json` to add a new term to the controlled vocabulary, as long
  as the change is consistent with the user's research focus.
- Creating new derived views in `index/` (e.g., a CSV grouped by theory) — these are
  always rebuildable from `notes/`.
