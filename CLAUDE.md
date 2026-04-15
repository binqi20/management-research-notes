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
   write `Not reported in paper`. Never guess.
2. **Verbatim means verbatim.** When the extraction prompt says "extract the abstract
   verbatim," the text in the note must appear as a contiguous substring of the
   extracted PDF text (modulo whitespace). The validator will check this.
3. **Notes are the source of truth.** If you need to fix a paper's metadata, re-run
   `tools/ingest_paper.py` for that paper. Don't edit `synapse.db` directly. Don't edit
   a note's frontmatter by hand unless you are also planning to rebuild the index.
4. **Stable IDs.** Every paper has a `paper_id` like `nbs-2026-02-spoor-2026` that is
   derived from `{source-slug}-{year-month}-{first-author-slug}-{year}`. Once assigned,
   it never changes. The note file is `notes/{paper_id}.md`.
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
