# Management Research Notes

**A file-based academic knowledge base for management and business sustainability research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Notes](https://img.shields.io/badge/curated%20notes-121-brightgreen.svg)](notes/)
[![Sources](https://img.shields.io/badge/sources-NBS%20%2B%20AMJ-orange.svg)](#whats-in-this-release)
[![Audit](https://img.shields.io/badge/audit-121%2F121%20PASS-success.svg)](#faithfulness-audit)
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
- **v0.5.0 sweep (2026-04-30, full 121 notes):**
  **121 / 121 PASS, 0 UNSUPPORTED, 0 CONTRADICTED.** Eight new notes
  added from AMJ vol. 68 no. 3 (Bermiss editorial + 7 substantive
  papers). Across four release cycles the library has now produced
  zero CONTRADICTED verdicts.

Run the audit on a single note with:

```bash
python tools/audit_note.py notes/<paper_id>.md
```

Or, from inside a Claude Code session: `/audit-note <paper_id>`.

## What's in this release

This release contains **121 curated notes** across two source streams:

- **NBS 2026-02** — 77 notes distilled from the [Network for Business
  Sustainability (NBS)](https://nbs.net/) February 2026 monthly research
  digest. (62 notes shipped in v0.2.0; 15 previously-missing papers were
  recovered and added in v0.3.0.)
- **AMJ pilot** — 44 notes across five recent issues of the
  [Academy of Management Journal](https://journals.aom.org/journal/amj)
  (vol. 68 no. 3, vol. 68 no. 4, vol. 68 no. 5, vol. 68 no. 6, vol. 69
  no. 1). v0.5.0 added vol. 68 no. 3 (8 notes); v0.4.0 added vol. 68
  no. 4 (8 notes); the previous pilot covered the other three issues
  (28 notes).

| Paper type             | Count |
|------------------------|------:|
| empirical-quantitative |    46 |
| empirical-qualitative  |    33 |
| conceptual             |    19 |
| empirical-mixed        |     8 |
| editorial              |     8 |
| review                 |     4 |
| book-review            |     3 |
| **Total**              | **121** |

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
├── notes/                             ← 121 curated paper notes (the source of truth)
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
  version      = {0.5.0},
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
