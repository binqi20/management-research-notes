# Management Research Notes

**A file-based academic knowledge base for management and business sustainability research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Notes](https://img.shields.io/badge/curated%20notes-257-brightgreen.svg)](notes/)
[![Sources](https://img.shields.io/badge/sources-NBS%20%2B%20AMJ-orange.svg)](#whats-in-this-release)
[![Audit](https://img.shields.io/badge/audit-257%2F257%20PASS-success.svg)](#faithfulness-audit)
[![For AI agents](https://img.shields.io/badge/for%20AI%20agents-AGENTS.md-blueviolet.svg)](AGENTS.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19564336.svg)](https://doi.org/10.5281/zenodo.19564336)

> One Markdown note per peer-reviewed paper. Trusted bibliographic metadata
> from manifests, analytic distillation from a verbatim-anchored extraction
> prompt, derived SQLite / CSV / BibTeX indexes that you can rebuild from
> scratch in seconds.

---

## Author

**Management Research Notes** is authored and maintained by
**[Binqi Tang](https://github.com/binqi20)**
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--5095--3710-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0000-0002-5095-3710),
a researcher in management and business sustainability. Collaborations are
welcome — whether that means
using this knowledge base in your own research workflow, adapting it for a
new source or subfield, or discussing joint projects. Please
[open an issue](https://github.com/binqi20/management-research-notes/issues)
or reach out on GitHub. Citations welcome — see [How to cite](#how-to-cite)
below.

---

## What it is

This project is a Zettelkasten-style knowledge base for academic literature. Each
peer-reviewed article is stored as a single Markdown file in `notes/` with two
parts:

1. **YAML frontmatter** — structured metadata: trusted bibliographic fields
   (title, authors, year, journal, DOI), a controlled-vocabulary topic list,
   the methods, the sample, and three custom analytic fields
   (`unit_of_analysis`, `level_of_theory`, `dependent_variable_family`) that
   make cross-paper queries actually useful.
2. **Markdown body** — a human-readable distillation: verbatim abstract,
   research question, mechanism / process, theoretical contribution, practical
   implication, limitations, future research, and a clean APA 7th citation.

A small Python pipeline derives a SQLite index, a flat CSV, and a BibTeX file
from the notes — none of which are the source of truth, all of which can be
rebuilt with `python tools/build_index.py && python tools/export_csv.py &&
python tools/export_bibtex.py`.

## Why it exists

Large language models have made it tempting to build a literature review by
dropping a pile of PDFs into a chat window and trusting the response. For
scholars in management, economics, and adjacent citation-heavy fields —
disciplines where every substantive claim is expected to be traceable to a
specific prior study — that naive workflow breaks down for three reasons:

- **Context windows are finite.** Even a 200K-token model cannot hold a few
  hundred full papers at once. You need *distilled* notes small enough to load
  in bulk but faithful enough to support real argument.
- **Provenance is non-negotiable.** Every analytic claim in a note is traceable
  to a cited paper. The verbatim abstract is checked as a contiguous substring
  of the extracted PDF text, every factual claim in a v2 note carries a ≤25-word
  evidence anchor verified against the PDF by `tools/validate_note.py`, and a
  two-layer faithfulness audit (see [below](#faithfulness-audit)) has a
  fresh-eyes LLM subagent cross-check the prose fields. Hallucinated or
  paraphrased content does not reach the published library — which is what
  makes these notes safe to cite in a defensible review.
- **Cross-platform and agent-ready.** The same note is grep-able from the
  command line, uploadable as project knowledge to an LLM chat, and citable
  from a Word / LaTeX / Typst draft via the BibTeX export. Via the SQLite + FTS5
  index and the [`AGENTS.md`](AGENTS.md) entry point, any AI agent — Claude
  Code, Cursor, Windsurf, a custom SDK app — can consume the library to run
  retrieval-augmented analysis *with known faithfulness guarantees*. That's the
  piece that matters for researchers: it lets one scholar (or an agent acting
  on their behalf) reason across a literature much larger than any single head
  can hold, without sacrificing the citation trail a peer reviewer, committee,
  or journal editor will expect.

The corpus shipped here is management and business sustainability, but the
pattern — one Markdown file per paper, trusted bibliographic manifests, a
verbatim-anchored extraction prompt, a two-layer audit — transfers
straightforwardly to any scholarly corpus where paraphrastic drift is costly:
economics working papers, organization theory, policy analysis, STS, labor
studies. Fork the repo, point it at your own manifest, and the validator and
audit layer come along for free.

The current design targets libraries growing from dozens to tens of thousands of
papers. Whether the shape holds at that scale is an empirical question rather
than a settled assumption: some parts — one file per paper, SQLite-derived
indexes, the controlled-vocabulary topic list, even the extraction prompt's
field set — may need to evolve as the library grows, new sources appear, or
research workflows change. Treat the current architecture as a working
hypothesis refined by each release, not a frozen spec.

## Faithfulness audit

Every analytic field in every note is checked by a **two-layer faithfulness
audit** before it is accepted into the library:

- **Layer 1 — Evidence anchors (mechanical, deterministic).** Each factual
  claim in the frontmatter (sample size, country, industry, time period,
  theories, methods, keywords) carries a ≤25-word verbatim quote from the
  PDF. The validator checks each quote is a substring of the extracted
  PDF text under hyphen-tolerant normalization. A fabricated quote fails
  deterministically — there is no way to pass Layer 1 with invented
  evidence.
- **Layer 2 — Semantic audit (fresh cold-context subagent).** For the
  prose fields (research question, mechanism, theoretical contribution,
  practical implication, limitations, future research) a fresh Claude
  subagent reads the PDF, reads the note, and emits a per-field verdict
  against the rubric at [`docs/audit-rubric.md`](docs/audit-rubric.md):
  `SUPPORTED` / `PARTIAL` / `UNSUPPORTED` / `CONTRADICTED`. A note is
  rejected if any verdict is `UNSUPPORTED` or `CONTRADICTED`.

The full library has been swept three times across releases:

- **v0.2.0 sweep (2026-04-17, 90 notes):** 88 / 90 initial PASS; two
  fails (Mahringer 2025, Li 2026) repaired via re-extraction, and the
  validator was tightened in one place (extended the `Not reported in
  paper` escape valve to `future_research`, mirroring the `limitations`
  exemption) based on what the audit found.
- **v0.3.0 sweep (2026-04-17, full 105 notes):**
  **105 / 105 PASS, 0 UNSUPPORTED, 0 CONTRADICTED.** One PARTIAL verdict
  (Castelló 2025 citing the EU Digital Markets Act instead of the EU
  Digital Services Act) was surfaced and fixed before release.
- **v0.4.0 sweep (2026-04-29, 113 notes):**
  113 / 113 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Eight new notes
  added from AMJ vol. 68 no. 4 (Grégoire editorial + 7 substantive
  papers).
- **v0.5.0 sweep (2026-04-30, 121 notes):**
  121 / 121 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Eight new notes
  added from AMJ vol. 68 no. 3 (Bermiss editorial + 7 substantive
  papers).
- **v0.6.0 sweep (2026-04-30, 129 notes):**
  129 / 129 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Eight new notes
  added from AMJ vol. 68 no. 2 (Rouse editorial + 7 substantive
  papers). Cleanest batch yet — only 1 PARTIAL across the 8 new notes.
- **v0.7.0 sweep (2026-04-30, 139 notes):**
  139 / 139 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Ten new notes
  added from AMJ vol. 68 no. 1 (Gruber + Cronin editorials + 8
  substantive papers — first 10-paper issue we've processed).
- **v0.8.0 sweep (2026-05-05, 147 notes):**
  147 / 147 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Eight new notes
  added from AMJ vol. 67 no. 6 (Reinecke editorial + 7 substantive
  papers — first issue from volume 67 we've processed).
- **v0.9.0 sweep (2026-05-05, 156 notes):**
  156 / 156 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Nine new notes added
  from AMJ vol. 67 no. 5 (Dorobantu editorial + 8 substantive papers).
  **Zero PARTIAL** across all 54 prose-field audits — first
  perfect-SUPPORTED batch.
- **v0.10.0 sweep (2026-05-06, 165 notes):**
  165 / 165 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Nine new notes
  added from AMJ vol. 67 no. 4 (Bliese editorial + 8 substantive
  papers). 1 PARTIAL.
- **v0.11.0 sweep (2026-05-07, 175 notes):**
  175 / 175 PASS, 0 UNSUPPORTED, 0 CONTRADICTED. Ten new notes
  added from AMJ vol. 67 no. 3. Three-batch ≤1-PARTIAL streak.
- **v0.11.1 patch (2026-05-07, 175 notes):**
  Bibliographic-integrity correction. A user-flagged check against
  Google Scholar surfaced that the Bednar 2024 note (and many
  others) were citing the *online-first* publication year rather
  than the *issue year* per APA 7. Built `tools/verify_years.py`
  to cross-check every DOI against CrossRef's `published-print`
  field. Found **48 papers (27% of library)** carrying the
  online-first year. All 48 corrected: manifest rows, frontmatter
  `year:` fields, and APA citations updated to the issue year.
  175/175 now align with CrossRef. The audit prose fields are
  unchanged (year doesn't affect any audited content claim), so
  no re-audit was needed.
- **v0.11.2 patch (2026-05-09, 175 notes):**
  Bibliographic cross-check extended to all seven CrossRef fields
  (year, title, journal, volume, issue, pages, authors) via the
  new `tools/verify_metadata.py`. The first full sweep on the
  v0.11.1 library surfaced 21 papers needing manifest backfills
  (mostly online-first papers in the NBS digest and AMJ vol-69-1
  whose issues had since published) plus one wrong-page error
  (Bamberger's *AMR* address) and one missing-Oxford-comma title
  typo in the same paper. After fixes: **175/175 MATCH for year,
  journal, and authors**, and **0 MISMATCH** across volume / issue
  / pages on every paper where CrossRef carries those fields. One
  remaining flag (Reinecke book review) is documented as a
  CrossRef-side data corruption, not a note error. Like v0.11.1,
  no re-audit needed — the audit prose fields are independent of
  bibliographic metadata.
- **v0.12.0 sweep (2026-05-10, 186 notes):**
  Adds AMJ vol. 67 no. 2 (11 substantive papers: Anderson, Arslan,
  Grégoire, Gruber, Li, Liao, Muethel, Pache, Piazza, Preston,
  Rostain). **186 / 186 PASS, 0 UNSUPPORTED, 0 CONTRADICTED, 0
  PARTIAL** — the cleanest batch outcome to date.
  Also introduces **Tier 3** of the bibliographic-integrity prevention
  strategy: the new `tools/populate_manifest.py` auto-populates each
  manifest's `volume`/`issue`/`pages` columns from CrossRef BEFORE
  extraction, and (with `--fix-year`) auto-corrects any wrong years
  the manifest may have inherited from the publisher's online-first
  metadata. This is now Step 0 of `/synapse-ingest`. The v0.12.0 batch
  proved the mechanism: Tier 3 caught and fixed 7 wrong-year manifest
  rows in vol-67-no-2 before extraction started — exactly the v0.11.1
  bug class, prevented at the source instead of patched retroactively.
- **v0.13.0 sweep (2026-05-12, 197 notes):**
  Adds AMJ vol. 67 no. 1 (10 substantive papers: Barkema, Bettinazzi,
  Cao, Dorobantu, Han, Jia, two Park papers, Soublière, To, plus
  Gruber editorial on the new Research Methods Articles portfolio).
  **197 / 197 PASS, 0 UNSUPPORTED, 0 CONTRADICTED, 1 PARTIAL** (Cao
  practical_implication — minor extrapolation from a contributions
  paragraph). Second consecutive batch ingested under the Tier 3
  prevention infrastructure (introduced v0.12.0) and the post-extraction
  column-merge heuristic (introduced commit `59a9ace`). Tier 3 found
  zero year mismatches in this batch (the manifest had already been
  captured after print publication), but still backfilled 11
  vol/issue/pages columns. Every extraction agent independently used
  `grep` on the extracted text to verify anchor contiguity before
  writing — Layer 1 passed on first try for all 11 papers, the first
  batch since the column-merge heuristic went into the extraction
  prompt to do so.
- **v0.13.1 patch (2026-05-12, 197 notes):**
  `slugify()` updated to fold diacritics via NFKD and strip apostrophes,
  resolving fragmented paper_ids like `gr-goire-2024` → `gregoire-2024`.
  5 paper_ids renamed as a deliberate, one-time exception to hard rule 4
  (stable IDs) while the library was small and had no known external
  citations by paper_id.
- **v0.13.2 patch (2026-05-12, 197 notes):**
  Adds `tools/lint_manifests.py` — a per-row structural + CrossRef
  audit of every manifest. First run surfaced 4 legitimate compound
  surnames (von Krogh, Lee Cunningham, Ter Wal, van den Oever — added
  to `KNOWN_COMPOUND_SURNAMES` allowlist) and **6 latent D'Amico-class
  bugs** in the NBS-2026-02 manifest (full given+family name captured
  instead of just the family name). 6 more paper_ids renamed; combined
  with v0.13.1 this closes the **v0.13.x cleanup cohort** (11 papers
  total). Hard rule 4's footnote in CLAUDE.md revised to use cohort
  framing.
- **v0.14.0 sweep (2026-05-16, 210 notes):**
  Adds AMJ vol. 66 no. 6 (12 substantive papers + Grimes editorial on
  generative AI's impact on management scholarship). **210 / 210 PASS,
  0 UNSUPPORTED, 0 CONTRADICTED, 3 PARTIAL** (Couture and Sajjadiani
  mechanism_process — minor attribution drift; Zhang limitations —
  added "cross-sectional" label not in paper). First batch ingested
  under the complete three-gate pipeline: Step 0 `populate_manifest.py`
  (Tier 3), Step 0.5 `lint_manifests.py` (structural), Step 4.5
  `verify_metadata.py` (Tier 2 content). All three gates exit 0.
  Also backfills v0.11.2-pattern drift on two ASQ papers
  (Lee Democratic Deviations, Reinecke book review) whose vol-71 issue
  2 published after their extraction; their note frontmatter + APA
  citations now reflect the issued version. Xu 2023 title added to
  `KNOWN_CROSSREF_DATA_ERRORS` (CrossRef has malformed `Forest<i>and</i>the
  Trees` with no spaces around the italic; note matches the published
  version correctly).
- **v0.15.0 sweep (2026-05-20, 222 notes):**
  Adds AMJ vol. 66 no. 5 (11 substantive papers + Dencker editorial on
  positioning research on novel phenomena). **222 / 222 PASS, 0
  UNSUPPORTED, 0 CONTRADICTED, 0 PARTIAL** — a perfectly clean batch:
  12/12 Layer 1 first-try PASS and 12/12 Layer 2 PASS with no PARTIAL
  verdicts at all. Ingested under the complete three-gate pipeline
  (populate_manifest → lint_manifests → verify_metadata), all exit 0
  with no drift findings or new false positives. Notable papers
  include the Lander/Voronov pair on Scottish and Canadian whisky
  authenticity, and the Carnabuci/Rua-Gomez network-formation studies.
- **v0.16.0 sweep (2026-05-20, 233 notes):**
  Adds AMJ vol. 66 no. 4 (10 substantive papers + Wellman editorial on
  publishing multimethod research). **233 / 233 PASS, 0 UNSUPPORTED, 0
  CONTRADICTED, 1 PARTIAL** (Kundro future_research — mild
  overgeneralization of the paper's actual future directions). Ingested
  under the complete three-gate pipeline; all gates exit 0 with no
  drift findings or new false positives. 11/11 Layer 1 first-try PASS
  (fifth consecutive batch at 100%). The Banerjee audit is a nice
  illustration of the Layer 2 value: H4 in that paper predicted one
  direction but the data showed the opposite (significant) — the note
  correctly reports the empirical result rather than the failed
  hypothesis, which the auditor verified as faithful rather than
  CONTRADICTED.
- **v0.17.0 sweep (2026-05-20, 244 notes):**
  Adds AMJ vol. 66 no. 3 (10 substantive papers + Langley editorial on
  opening up AMJ's research methods repertoire). **244 / 244 PASS, 0
  UNSUPPORTED, 0 CONTRADICTED, 1 PARTIAL** (Toivonen practical_implication
  — practitioner prescriptions synthesized from a paper with no dedicated
  implications section). Ingested under the complete three-gate pipeline;
  all gates exit 0 with no drift findings or new false positives. 11/11
  Layer 1 first-try PASS (sixth consecutive batch at 100%). This sweep
  completes the AMJ vol. 66 + vol. 67 coverage from no. 3 onward — the
  pilot now spans 13 consecutive AMJ issues plus vol. 68 and vol. 69.
- **v0.18.0 sweep (2026-05-23, 257 notes):**
  Adds AMJ vol. 66 no. 2 (12 substantive papers + Krogh editorial on AI
  research opportunities). **257 / 257 PASS, 0 UNSUPPORTED, 0
  CONTRADICTED, 1 PARTIAL** (Zhang mechanism_process — minor mediator-vs-
  DV imprecision in one study). 13/13 Layer 1 first-try PASS (seventh
  consecutive batch at 100%). Three of this issue's papers (Krogh→von
  Krogh, Cunningham→Lee Cunningham, Wal→Ter Wal) are the compound
  surnames already in the `KNOWN_COMPOUND_SURNAMES` allowlist; Step 0.5
  suppressed all three cleanly, and verify_metadata's note-level author
  check passed without new false positives (notes carry the full byline
  forms that match CrossRef; the short form lives only in the paper_id
  slug). This release also **promotes the `extraction_model`-verbatim
  instruction into `docs/extraction-prompt.md`** — a validated systemic
  fix (13/13 agents kept the field uniform this batch vs. up to 7
  outliers needing manual cleanup in prior batches), eliminating a
  recurring per-batch provenance-field normalization.

Run the audit on a single note with:

```bash
python tools/audit_note.py notes/<paper_id>.md
```

Or, from inside a Claude Code session: `/audit-note <paper_id>`.

## What's in this release

This release contains **257 curated notes** across two source streams:

- **NBS 2026-02** — 77 notes distilled from the [Network for Business
  Sustainability (NBS)](https://nbs.net/) February 2026 monthly research
  digest. (62 notes shipped in v0.2.0; 15 previously-missing papers were
  recovered and added in v0.3.0.)
- **AMJ pilot** — 180 notes across eighteen recent issues of the
  [Academy of Management Journal](https://journals.aom.org/journal/amj)
  (vol. 66 no. 2, vol. 66 no. 3, vol. 66 no. 4, vol. 66 no. 5, vol. 66
  no. 6, vol. 67 no. 1, vol. 67 no. 2, vol. 67 no. 3, vol. 67 no. 4,
  vol. 67 no. 5, vol. 67 no. 6, vol. 68 no. 1 through 6, vol. 69 no. 1).
  v0.18.0 added vol. 66 no. 2 (13 notes); v0.17.0 added
  vol. 66 no. 3 (11 notes); v0.16.0 added vol. 66 no. 4 (11 notes);
  v0.15.0 added vol. 66 no. 5 (12 notes); v0.14.0 added vol. 66 no. 6
  (13 notes); v0.13.0 added vol. 67 no. 1 (11 notes); v0.12.0 added
  vol. 67 no. 2 (11 notes); v0.11.0 added vol. 67 no. 3 (10 notes);
  v0.10.0 added vol. 67 no. 4 (9 notes); v0.9.0 added vol. 67 no. 5
  (9 notes); v0.8.0 added vol. 67 no. 6 (8 notes); v0.7.0 added vol.
  68 no. 1 (10 notes); v0.6.0 added vol. 68 no. 2 (8 notes); v0.5.0
  added vol. 68 no. 3 (8 notes); v0.4.0 added vol. 68 no. 4 (8 notes);
  the original pilot covered the remaining three issues (28 notes).

| Paper type             | Count |
|------------------------|------:|
| empirical-quantitative |   109 |
| empirical-qualitative  |    71 |
| empirical-mixed        |    29 |
| editorial              |    22 |
| conceptual             |    19 |
| review                 |     4 |
| book-review            |     3 |
| **Total**              | **257** |

Every note carries a v2 `evidence:` anchor block (Layer 1) and has passed
the Layer 2 semantic audit. See [Faithfulness audit](#faithfulness-audit)
above.

## Repository layout

```
management-research-notes/
├── README.md                          ← you are here
├── AGENTS.md                          ← tool-agnostic entry point for AI agents
├── LICENSE                            ← MIT
├── CITATION.cff                       ← cite-this-repo metadata
├── CLAUDE.md                          ← rules for any Claude Code session in this folder
├── docs/
│   ├── extraction-prompt.md           ← the canonical extraction prompt (v2)
│   └── audit-rubric.md                ← rubric the Layer 2 auditor uses
├── notes/                             ← 175 curated paper notes (the source of truth)
│   └── nbs-2026-02-spoor-2026.md
├── index/                             ← derived views, all rebuildable
│   ├── synapse.db                     ← SQLite + FTS5 (~1.7 MB)
│   ├── papers.csv                     ← flat tabular export
│   ├── library.bib                    ← BibTeX, one @article per note
│   └── topics.json                    ← 14-domain controlled vocabulary
├── tools/                             ← the Python pipeline
│   ├── pdf_to_text.py                 ← PDF → plain text (pdftotext + pdfplumber)
│   ├── prepare_paper.py               ← bundle a paper for extraction
│   ├── ingest_batch.py                ← walk a folder of PDFs
│   ├── validate_note.py               ← verbatim-abstract + bib + taxonomy + anchors
│   ├── audit_note.py                  ← two-layer faithfulness audit (Layer 1 + Layer 2)
│   ├── build_index.py                 ← rebuild SQLite from notes/
│   ├── export_csv.py                  ← rebuild papers.csv
│   └── export_bibtex.py               ← rebuild library.bib
├── library/
│   ├── NBS/2026-02/
│   │   ├── manifest.tsv               ← trusted bibliographic source for the batch
│   │   └── missing.tsv                ← papers NBS listed but PDFs unavailable
│   └── AMJ/{vol-68-5,vol-68-6,vol-69-1}/
│       └── manifest.tsv               ← per-issue manifests for the AMJ pilot
│       (pdfs/ and text/ are intentionally NOT published — see Copyright below)
└── .synapse/
    ├── config.yaml                    ← validator policy + custom-field schema
    └── schema.sql                     ← SQLite schema
```

## Quick start

```bash
git clone https://github.com/binqi20/management-research-notes.git
cd management-research-notes

# Optional: rebuild the SQLite index from the notes
python tools/build_index.py

# Query the library — answers come back in milliseconds
sqlite3 index/synapse.db "SELECT COUNT(*) FROM papers;"
sqlite3 index/synapse.db \
  "SELECT paper_type, COUNT(*) FROM papers GROUP BY 1 ORDER BY 2 DESC;"
sqlite3 index/synapse.db \
  "SELECT p.id, p.title FROM papers p JOIN topics t ON t.paper_id = p.id
   WHERE t.topic = 'circular-economy' ORDER BY p.year DESC;"

# Full-text search across abstracts and analytic fields
sqlite3 index/synapse.db \
  "SELECT id FROM papers_fts WHERE papers_fts MATCH 'stakeholder AND legitimacy';"

# Re-export BibTeX or CSV
python tools/export_bibtex.py
python tools/export_csv.py
```

### Optional dependencies (for ingesting new PDFs locally)

```bash
brew install poppler            # gives you pdftotext
pip install pyyaml pdfplumber   # pyyaml: validator; pdfplumber: extraction fallback
```

The validator (`tools/validate_note.py`) reads the corresponding extracted
text file under `library/<source>/<issue>/text/` to perform its verbatim-abstract
substring check. That folder is intentionally absent from the public repo
because the text is derived from copyrighted PDFs — see below. For a public
clone, the SQLite, CSV, and BibTeX queries above all work without it.

## For AI agents

If you are an AI agent (or writing one) and want to consume or contribute
to this knowledge base, start with [`AGENTS.md`](AGENTS.md) — it is the
tool-agnostic entry point covering:

- the data formats you can consume without running any tooling
  (Markdown notes, SQLite + FTS5, CSV, BibTeX),
- the [7 hard rules](AGENTS.md#4-rules-for-agents-that-modify-content)
  any agent must follow when creating or editing notes,
- the [faithfulness guarantees](AGENTS.md#5-faithfulness-guarantees)
  this library carries (every abstract verbatim-anchored, every prose
  field audited, zero contradictions),
- and how to cite the knowledge base if your agent surfaces a note.

For Claude Code-specific operational conventions (slash commands,
subagent dispatch, tool names), see [`CLAUDE.md`](CLAUDE.md) as well.

## Copyright and licensing

The **code**, the **curated notes**, the **topic taxonomy**, and the
**derived indexes** in this repository are released under the [MIT
license](LICENSE) and are © 2026 Binqi Tang.

The **original journal articles** that the notes summarize are NOT included.
They remain the copyright of their respective publishers and authors. To
reproduce a note end-to-end, obtain the source PDF through legitimate channels
(your institution, the publisher, or the author's preprint), drop it into
`incoming/`, and run the pipeline locally.

Each note contains a short verbatim abstract (treated as fair-use
quotation/commentary) and an original analytic distillation written by the
author of this repository. Notes cite the original work via DOI in every
file's frontmatter and APA citation block.

## How to cite

This repository ships with a [`CITATION.cff`](CITATION.cff), which GitHub uses
to render a "Cite this repository" button in the right sidebar. It will give
you both APA and BibTeX automatically. Or, manually:

```bibtex
@software{tang_mgmt_research_notes_2026,
  author       = {Tang, Binqi},
  title        = {Management Research Notes: A File-Based Academic Knowledge
                  Base for Management and Business Sustainability Research},
  year         = {2026},
  version      = {0.14.0},
  doi          = {10.5281/zenodo.19564336},
  url          = {https://doi.org/10.5281/zenodo.19564336},
  license      = {MIT}
}
```

If you use a specific note, please also cite the original paper using the DOI
in that note's APA citation block — the analytic distillation is a commentary,
not a substitute.

## Roadmap

This project is intended to be a long-running research-infrastructure
project, not a one-shot data drop. The near-term roadmap:

- **More monthly batches** — extend NBS coverage with each new digest and
  continue the AMJ sweep beyond the current three-issue pilot, keeping
  paper IDs stable across updates.
- **Additional journal sources** — add Web of Science exports and journal
  RSS feeds as parallel `library/{source}/{issue}/` trees, reusing the
  same pipeline.
- **Audit layer hardening** — cross-model auditing (run Layer 2 with a
  second model vendor), automated re-audit on prompt changes, and a
  lightweight public audit-summary CSV so consumers can see which prose
  fields carry `PARTIAL` verdicts without needing to regenerate.
- **Vector search** — only after the library passes ~5,000 notes; the
  SQLite FTS5 index is plenty for now.
- **Community contributions** — issues and pull requests welcome from
  collaborators who want to share extraction prompts, topic taxonomies,
  or curated subsets.

## Acknowledgements

- The **[Network for Business Sustainability (NBS)](https://nbs.net/)** for
  curating the monthly research digest that seeds this library.
- **[Anthropic Claude Code](https://www.anthropic.com/claude-code)** for the
  extraction-and-validation workflow that drives the ingestion pipeline.
- The authors of every paper in `notes/` — without their original scholarship,
  there is nothing to distill.

---

*Maintained by [Binqi Tang](https://github.com/binqi20). MIT licensed. Issues
and PRs welcome.*
