# Management Research Notes

**A file-based academic knowledge base for management and business sustainability research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Notes](https://img.shields.io/badge/curated%20notes-62-brightgreen.svg)](notes/)
[![Source](https://img.shields.io/badge/source-NBS%202026--02-orange.svg)](https://nbs.net/)
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

Modern LLMs make it tempting to stuff a literature review with PDFs and hope
for the best. That breaks down for three reasons:

- **Context windows are finite.** Even a 200K-token model cannot hold a few
  hundred full papers. You need *distilled* notes that are small enough to load
  in bulk but faithful enough to support real argument.
- **Provenance matters.** Every analytic claim in a note is traceable to a
  cited paper, and the verbatim abstract is checked as a contiguous substring
  of the extracted PDF text by `tools/validate_note.py` — so paraphrased or
  hallucinated abstracts cannot slip through.
- **Cross-platform reuse.** The same note file is grep-able from Claude Code,
  uploadable as project knowledge to Claude.ai, and citable directly from a
  Word / LaTeX / Typst draft via the BibTeX export.

The design assumes the library will grow from dozens of papers to tens of
thousands without changing shape.

## What's in this release

This first public release contains **62 curated notes** distilled from the
[Network for Business Sustainability (NBS)](https://nbs.net/) February 2026
monthly research digest.

| Paper type             | Count |
|------------------------|------:|
| empirical-quantitative |    23 |
| empirical-qualitative  |    14 |
| conceptual             |    14 |
| review                 |     3 |
| editorial              |     3 |
| book-review            |     3 |
| empirical-mixed        |     2 |
| **Total**              | **62** |

**Top topics** (controlled vocabulary, 14 domains): business-ethics (10),
circular-economy (9), decarbonization (8), grand-challenges (8),
stakeholder-engagement (8), sustainable-consumption (7), entrepreneurship (6),
developing-economies (5), …

**Top journals**: Journal of Industrial Ecology (9), Business Ethics Quarterly
(8), Journal of Management (7), Journal of Consumer Marketing (6), Management
Science (6).

## Repository layout

```
management-research-notes/
├── README.md                          ← you are here
├── LICENSE                            ← MIT
├── CITATION.cff                       ← cite-this-repo metadata
├── CLAUDE.md                          ← rules for any Claude session in this folder
├── docs/
│   └── extraction-prompt.md           ← the canonical 17-field extraction prompt
├── notes/                             ← 62 curated paper notes (the source of truth)
│   └── nbs-2026-02-spoor-2026.md
├── index/                             ← derived views, all rebuildable
│   ├── synapse.db                     ← SQLite + FTS5 (~1.2 MB)
│   ├── papers.csv                     ← flat tabular export (~390 KB)
│   ├── library.bib                    ← BibTeX, one @article per note
│   └── topics.json                    ← 14-domain controlled vocabulary
├── tools/                             ← the Python pipeline
│   ├── pdf_to_text.py                 ← PDF → plain text (pdftotext + pdfplumber)
│   ├── prepare_paper.py               ← bundle a paper for extraction
│   ├── ingest_batch.py                ← walk a folder of PDFs
│   ├── validate_note.py               ← verbatim-abstract + bib + taxonomy gate
│   ├── build_index.py                 ← rebuild SQLite from notes/
│   ├── export_csv.py                  ← rebuild papers.csv
│   └── export_bibtex.py               ← rebuild library.bib
├── library/
│   └── NBS/2026-02/
│       ├── manifest.tsv               ← trusted bibliographic source for the batch
│       └── missing.tsv                ← papers NBS listed but PDFs unavailable
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
text file under `library/NBS/<issue>/text/` to perform its verbatim-abstract
substring check. That folder is intentionally absent from the public repo
because the text is derived from copyrighted PDFs — see below. For a public
clone, the SQLite, CSV, and BibTeX queries above all work without it.

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
  version      = {0.1.0},
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

- **More monthly batches** — extend coverage with each new NBS digest, keeping
  paper IDs stable across updates.
- **Non-NBS sources** — add Web of Science exports and journal RSS feeds as
  parallel `library/{source}/{issue}/` trees, reusing the same pipeline.
- **Validator hardening** — soft-hyphen normalization, better 2-column PDF
  text reconstruction, fewer false-positive verbatim failures.
- **Vector search** — only after the library passes ~5,000 notes; the SQLite
  FTS5 index is plenty for now.
- **Community contributions** — issues and pull requests welcome from
  collaborators who want to share extraction prompts, topic taxonomies, or
  curated subsets.

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
