# Management Research Notes

**A management and business sustainability research library for literature discovery, comparison and return to the original papers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/binqi20/management-research-notes)](https://github.com/binqi20/management-research-notes/releases/latest)
[![For AI agents](https://img.shields.io/badge/for%20AI%20agents-AGENTS.md-blueviolet.svg)](AGENTS.md)

The library provides one structured Markdown note per scholarly publication, with searchable SQLite data and CSV/BibTeX exports. Notes combine bibliographic metadata, analytic summaries and links back to the sources. They are produced through an AI-assisted workflow with documented source checks, independent reviews and corrections.

[Browse the notes](notes/) · [Read a V3 example](notes/amj-vol-69-no-5-hymer-2026.md) · [Quick start](#quick-start) · [Latest release](https://github.com/binqi20/management-research-notes/releases/latest) · [For AI agents](#for-ai-agents)

## What it is

Each note has YAML frontmatter for bibliographic fields, topics, methods, sample information and analytic classifications, followed by a readable account of the research question, mechanism, contribution, implications and limitations. V3 notes also include **Hypotheses / Propositions, Data & Measures, and Key Findings**. Editorials, conceptual papers and reviews are represented alongside empirical studies; fields without applicable source content follow the documented conventions.

The notes are the primary records. The SQLite database, CSV and BibTeX are derived views that can be rebuilt from them. Stable paper IDs connect these formats, while the topic vocabulary supports comparison across papers. This is a file-based library: there is no hosted search service or package to install just to read it.

## Why it exists

Reading and comparing a large literature requires more than collecting PDFs. This library makes it easier to locate relevant studies, compare constructs, samples and findings, and return to the original evidence when developing an argument.

Plain text and standard exports let researchers and developers use the same material in different ways: browse Markdown, filter data in a spreadsheet, query SQLite, import citations or retrieve selected notes for an AI-assisted research task. Source references, review disclosures and version history support checking that work. The notes remain a research aid; substantive claims should be verified against the original publications.

## What's in this snapshot

**v0.82.0 · 20 October 2026 · 1,248 notes**

**Most notes cover publications in UTD24 journals**, the [24 leading business journals](https://jsom.utdallas.edu/the-utd-top-100-business-school-research-rankings/list-of-journals) used in The University of Texas at Dallas’s business school research rankings. Coverage is especially deep in the *Academy of Management Journal*.

| Source collection | Notes | Coverage |
|---|---:|---|
| Network for Business Sustainability (NBS) digests | 272 | December 2025, January 2026 and February 2026 |
| Academy of Management Journal (AMJ) issue batches | 976 | 78 issues: Volume 56 Issue 6; all issues of Volumes 57–68; Volume 69 Issues 1–5 |

Seven NBS-source notes also cover AMJ papers, bringing the total to **983 distinct AMJ publications** without duplicate analyses. The corpus contains **61 V1, 210 V2 and 977 V3 notes**. These version labels describe note formats, not accuracy ratings.

The latest release adds all 13 AMJ Volume 56 Issue 6 notes, including the editorial. See the [v0.82.0 release record](docs/releases/v0.82.0.md) for corrections, retained judgments, approved exceptions and publication checks, and [earlier release records](docs/releases/) for their respective scopes.

## Quick start

**Browse without installing anything:** open a [Markdown note](notes/amj-vol-69-no-5-hymer-2026.md), download [papers.csv](index/papers.csv), or use [library.bib](index/library.bib) in a bibliography manager. The [topic vocabulary](index/topics.json) describes available categories.

**Query locally:** clone the repository and use the committed database with a SQLite installation that supports FTS5. No source PDFs, Python environment or index rebuild is needed for these queries.

```bash
git clone https://github.com/binqi20/management-research-notes.git
cd management-research-notes

sqlite3 -readonly index/synapse.db "SELECT COUNT(*) FROM papers;"

sqlite3 -readonly index/synapse.db \
  "SELECT p.id, p.title, p.year FROM papers p
   JOIN topics t ON t.paper_id = p.id
   WHERE t.topic = 'circular-economy' ORDER BY p.year DESC;"

sqlite3 -readonly index/synapse.db \
  "SELECT id FROM papers_fts
   WHERE papers_fts MATCH 'stakeholder AND legitimacy';"
```

**Optional rebuild:** use Python 3.10+ and PyYAML in a virtual environment. Run the three commands sequentially; they replace the derived database and exports in your clone.

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux; on Windows use .venv\Scripts\activate
python -m pip install pyyaml
python tools/build_index.py
python tools/export_csv.py
python tools/export_bibtex.py
```

Ingesting or validating against original publications is a separate task. PDFs, extracted paper text and full local review evidence are not distributed in this public repository. Those operations require the matching source material and the additional dependencies and checks in the [pipeline runbook](docs/pipeline-runbook.md).

## Faithfulness audit

The current workflow combines mechanical checks, independent holistic and claims reviews, and source-based adjudication. A quotation match establishes membership in the checked source text; it does not certify the meaning of every statement. Required fresh reviews follow repairs, and original reader judgments remain separate from parent adjudications.

Review coverage and exceptions vary by version. A passing report records a specified review outcome; it does not guarantee error-free notes. Published release records disclose corrections, retained reservations and approved exceptions. Verify substantive claims against the original publications before relying on or citing them.

- [Current analysis workflow](docs/analysis-workflow.md)
- [Publication-readiness requirements](docs/publication-readiness.md)
- [Complete preserved audit history through v0.80.0](FAITHFULNESS-AUDIT.md)
- [Detailed release records](docs/releases/)

## For AI agents

Start with [AGENTS.md](AGENTS.md) for data formats, query examples, stable identifiers, modification rules and citation guidance. Retrieve the notes relevant to the task and follow their source references when checking substantive claims. The [current analysis workflow](docs/analysis-workflow.md) distinguishes mechanical validation, independent readers and source adjudication.

Agents modifying content must also follow [CLAUDE.md](CLAUDE.md), the project's working rules under its historical filename, and the [pipeline runbook](docs/pipeline-runbook.md). Current production and reader settings are documented in the [claims guide](docs/claims-verification.md); historical model stamps remain unchanged. Reading the library does not require a particular model or vendor.

## Repository layout

```text
notes/                  Primary Markdown notes with YAML frontmatter
index/synapse.db         Derived SQLite database with FTS5 search
index/papers.csv         Derived tabular export
index/library.bib        Derived bibliography
index/topics.json       Controlled topic vocabulary
tools/                  Ingestion, validation, indexing and export scripts
library/                Public source manifests; PDFs and text stay local
docs/                   Workflow, prompts, review guides and release records
AGENTS.md               Entry point for agents using or modifying the library
CLAUDE.md               Working rules, retained under the historical filename
FAITHFULNESS-AUDIT.md    Preserved homepage audit history through v0.80.0
CITATION.cff             Machine-readable citation metadata
LICENSE                 MIT license
```

## Copyright and licensing

Project-created code, note commentary, taxonomy and index structure are provided under the [MIT license](LICENSE), © 2026 Binqi Tang. Quoted abstracts and evidence excerpts remain subject to the rights of their respective authors and publishers; the project license does not grant rights to third-party material.

Original journal PDFs and extracted full texts are not redistributed here. Notes use AI-assisted analysis and maintainer curation, with attribution to the underlying publications. Where a publication has no standalone abstract, the note records that absence. Reproducing source-dependent checks requires legitimate access to the matching source version; a different manuscript or preprint may not reproduce those checks.

## How to cite

Use [CITATION.cff](CITATION.cff) or GitHub’s **Cite this repository** control to cite this library. For the current corpus release:

```bibtex
@software{tang_mgmt_research_notes_2026,
  author  = {Tang, Binqi},
  title   = {Management Research Notes: A File-Based Academic Knowledge Base
             for Management and Business Sustainability Research},
  year    = {2026},
  version = {0.82.0},
  url     = {https://github.com/binqi20/management-research-notes/releases/tag/v0.82.0}
}
```

The [original v0.1.0 Zenodo archive](https://doi.org/10.5281/zenodo.19564336) has its own DOI; it is not an archive of v0.82.0. Later Zenodo deposits remain paused. When using a note’s substantive content, also cite the original publication using its bibliographic metadata and APA citation block.

## Author

Authored and maintained by **[Binqi Tang](https://github.com/binqi20)**, a researcher in management and business sustainability. [ORCID: 0000-0002-5095-3710](https://orcid.org/0000-0002-5095-3710).

Questions, correction reports and collaboration proposals are welcome through [GitHub issues](https://github.com/binqi20/management-research-notes/issues). For a correction, identify the note, passage and supporting source location. Contributions must follow the documented source and review requirements.

## Roadmap

The current priorities are extending coverage through selected journal issues and research digests, maintaining stable identifiers, and documenting source checks and corrections. Further source integrations or search capabilities will be considered when there is a demonstrated need. There is no automatic re-audit schedule or note-count trigger for changing the architecture.

## Acknowledgements

Thanks to the [Network for Business Sustainability](https://nbs.net/) for the research digests that seeded the library, and to the authors of the underlying scholarship. Claude Code supported the early extraction and validation workflow; OpenAI Codex supports the current analysis and independent-review orchestration. Historical provenance is retained in the notes and release records.
