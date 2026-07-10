# AGENTS.md

**How AI agents can use this repository.**

This file is the tool-agnostic entry point for any AI agent (Claude, GPT,
Gemini, Cursor, Windsurf, a custom SDK app, or a future framework we
haven't heard of yet) that wants to read, query, or contribute to the
Management Research Notes knowledge base. A companion file,
[`CLAUDE.md`](CLAUDE.md), contains Claude-Code-specific operational
conventions (slash commands, subagent dispatch, tool names); this file
focuses on what's portable across agents.

---

## 1. What this repository is

**Management Research Notes** is a file-based academic knowledge base of
**1,141 curated notes** on peer-reviewed papers in management and business
sustainability research. The current main-branch snapshot contains 272
Network for Business Sustainability notes (2025-12, 2026-01, 2026-02)
and 869 Academy of Management Journal pilot notes across 68 recent issues
(vol. 57 no. 1, plus vol. 58 no. 1 through vol. 69 no. 1). Every note is a single Markdown
file with YAML frontmatter and a structured Markdown body. The repository
is MIT licensed; individual PDFs are not redistributed.

**Why it exists for agents specifically.** Raw PDFs are expensive to load
in bulk and their text layers vary in quality. These notes are a
distilled, uniform, verbatim-anchored representation that fits in a
context window, supports structured querying, and carries strong
faithfulness guarantees (see §5). An agent can load the whole library
into a 200K-context model, or query SQL/FTS5 for specific slices, without
worrying about whether a claim was hallucinated.

---

## 2. Recommended reading order for an agent

Before acting on the data or contributing to it, an agent should read in
this order:

1. This file (`AGENTS.md`) — entry point, data formats, faithfulness guarantees.
2. [`CLAUDE.md`](CLAUDE.md) — the 7 hard rules for anyone modifying content (Claude-Code-flavored but content is tool-agnostic).
3. [`docs/extraction-prompt.md`](docs/extraction-prompt.md) — the canonical prompt used to produce each note, including the required `evidence:` anchor schema.
4. [`docs/audit-rubric.md`](docs/audit-rubric.md) — the verdict rubric the faithfulness auditor uses.
5. [`docs/pipeline-runbook.md`](docs/pipeline-runbook.md) — **if you are ingesting or publishing:** the vendor-neutral step-by-step procedure (gate order, parallel-wave caps, systemic-failure stop conditions, SSH publish).
6. Any single note, e.g. [`notes/nbs-2026-02-spoor-2026.md`](notes/nbs-2026-02-spoor-2026.md), to see the schema in practice.

---

## 3. How to consume the data

The notes are the source of truth. Everything in `index/` is derived and
can be regenerated with `python tools/build_index.py`.

### 3.1 Markdown notes (`notes/*.md`) — primary

- One file per paper, named by stable `paper_id` (e.g. `nbs-2026-02-spoor-2026`).
- Every `paper_id` is permanent — agents may safely use it as a citation target.
- Two parts:
  - **YAML frontmatter:** bibliographic metadata (title, authors, year, journal, DOI, volume, issue, pages), paper type, controlled-vocabulary `topics:`, methods, sample (N, country, industry, time period), three custom analytic fields (`unit_of_analysis`, `level_of_theory`, `dependent_variable_family`), and (on v2/v3 notes) an `evidence:` block of ≤25-word verbatim PDF quotes anchoring each factual claim.
  - **Markdown body:** verbatim abstract (always a substring of the source PDF), research question, mechanism/process, theoretical contribution, practical implication, limitations, future research, and an APA 7th citation block. **v3 notes add three empirical sections — hypotheses / propositions, data & measures, and key findings** — so the note records not just what a paper studied but what it found.
- **Good for:** grep / full-text search, loading into context, human reading.
- **Example query:** `grep -l "stakeholder theory" notes/*.md`.

### 3.2 SQLite index (`index/synapse.db`) — derived

- Standard SQLite 3, readable from any language. Tables include `papers`, `authors`, `topics`, `theories`, `methods`, plus FTS5 virtual tables over the abstracts and analytic prose.
- **Good for:** structured queries, counts, filters, joins.
- **Example query:**
  ```sql
  SELECT p.id, p.title, p.year
  FROM papers p
  JOIN topics t ON t.paper_id = p.id
  WHERE t.topic = 'circular-economy'
  ORDER BY p.year DESC;
  ```
- **FTS5 example:**
  ```sql
  SELECT id FROM papers_fts WHERE papers_fts MATCH 'stakeholder AND legitimacy';
  ```

### 3.3 Flat CSV (`index/papers.csv`) — derived

- One row per paper, the most-queried fields flattened.
- **Good for:** pandas, spreadsheets, quick joins with external data.

### 3.4 BibTeX (`index/library.bib`) — derived

- One `@article` per note, DOI-keyed.
- **Good for:** LaTeX, Zotero, Word citation managers. Drop it into your bibliography file and the notes' APA citations round-trip.

### 3.5 Controlled vocabulary (`index/topics.json`) — derived

- The 14-domain taxonomy behind the `topics:` field on each note.
- **Good for:** vocabulary alignment when an agent extracts topics for a new paper. Do not invent topics — reuse this list.

---

## 4. Rules for agents that modify content

If your agent is creating new notes, editing existing ones, or submitting
a pull request, it must follow these 7 rules (paraphrased tool-agnostically
from [`CLAUDE.md`](CLAUDE.md)):

1. **Never invent bibliographic fields.** Title, authors, year, journal, DOI, volume/issue/pages come only from `library/.../manifest.tsv` or a CrossRef lookup by DOI. Unknown → `Not reported in paper`. Never guess.
2. **Verbatim means verbatim.** When the extraction prompt says "extract the abstract verbatim," the result must be a contiguous substring of the extracted PDF text (modulo whitespace/hyphen normalization).
3. **Notes are the source of truth.** Never edit `index/synapse.db`, `index/papers.csv`, or `index/library.bib` by hand — they are rebuilt from `notes/`. To fix a paper's metadata, re-run the ingestion script and let the derived index rebuild.
4. **Stable paper IDs.** Every paper has a `paper_id` of the form `{source-slug}-{year-month}-{first-author-slug}-{year}`. Once assigned, it never changes.
5. **Validate before committing.** After producing or editing a note, run the validator (`python tools/validate_note.py notes/<id>.md`). On fail, fix the note or move it to `incoming/_flagged/` with a `.reason.txt` explaining why.
6. **One paper, one note.** Never split a paper across multiple notes. Never merge two papers into one note.
7. **Faithfulness is checked, not assumed.** Every v2 note carries an `evidence:` frontmatter block whose quotes are verbatim substrings of the PDF text. A two-layer audit (`python tools/audit_note.py notes/<id>.md`) runs this check mechanically (Layer 1) and then uses a fresh, independent auditor context to score the prose fields semantically against the rubric at [`docs/audit-rubric.md`](docs/audit-rubric.md) (Layer 2). The auditor must not be the same agent/session that wrote the note. Codex-style external auditors must provide provenance-checked Layer 2 JSON via `--layer-2-json`. Both layers must pass.

---

## 4.1 Parallel agent slot policy

For issue-level ingestion with parallel agents, Synapse uses a conservative
Codex operating cap rather than a claimed platform limit. Keep at most **6
active extraction agents** or **6 active audit agents** per wave. Do not attempt
larger waves unless the user explicitly changes this policy after a new cap
test.

Use separate waves for extraction and audit. Extraction agents may write only
`notes/<paper_id>.md`. Audit agents may write only
`incoming/_audits/<paper_id>.layer2.json`. The parent session assembles official
audit reports, handles repairs, and rebuilds SQLite/CSV/BibTeX indexes.

After any worker returns, record its result and close the completed agent thread
before spawning another. If an active-agent cap, timeout, or coordination
problem appears even at 6, fall back to 5, then 3, then serial execution while
keeping extraction and audit roles independent.

---

## 5. Faithfulness guarantees

Every note in this repository has been through a **two-layer faithfulness
audit**:

- **Layer 1 — Evidence anchors (mechanical).** For v2/v3 notes, each factual claim (sample size, country, industry, time period, theories, methods, keywords — and, on v3, hypotheses, measures, and key findings) carries a ≤25-word verbatim quote from the PDF. The validator checks each quote is a substring of the extracted PDF text under hyphen-tolerant normalization. Fabricated quotes fail deterministically. Earlier v1 notes predate the evidence-anchor schema and are exempt from this layer.
- **Layer 2 — Semantic audit (fresh independent auditor).** A fresh auditor context reads the PDF, reads the note, and emits a per-field verdict for the six prose fields (research question, mechanism, theoretical contribution, practical implication, limitations, future research — v3 notes add three more: hypotheses, data & measures, key findings) from the set: `SUPPORTED` / `PARTIAL` / `UNSUPPORTED` / `CONTRADICTED`. The auditor cannot be the same agent/session that generated the note. A note is rejected if any verdict is `UNSUPPORTED` or `CONTRADICTED`.

**Current main-branch audit state (2026-07-10):
1,141 / 1,141 notes PASS, 0 UNSUPPORTED, 0 CONTRADICTED.** The 13 new
vol-57-no-1 notes (the first extraction-v3 issue) audited at 117/117
prose-field verdicts SUPPORTED under rubric v2; the prior 1,128 notes are
unchanged from the v0.29.0 audit sweep. The corpus contains 88 legacy v1
notes, 1,040 v2 notes, and 13 v3 notes with evidence anchors; new notes are
produced at extraction **v3**, which adds hypotheses, data & measures, and key
findings (see [`docs/pipeline-runbook.md`](docs/pipeline-runbook.md)). `PARTIAL`
verdicts (stylistic compressions that don't rise to a faithfulness failure)
are flagged for human review but do not block publication. The library has
never produced a `CONTRADICTED` verdict — no claim in any note actively
contradicts its source paper.

Agents querying the data can rely on the following:

- **Every abstract is a verbatim substring of the source PDF.** If your agent quotes an abstract from a note, it is quoting the paper.
- **Every factual claim in v2 note frontmatter is anchored.** If your agent cites a sample size or a theory from v2 frontmatter, there is a verbatim PDF quote behind it in the `evidence:` block.
- **Every prose field has passed a semantic audit.** If your agent summarizes a research question, mechanism, or theoretical contribution from a note, it's quoting a claim that was independently cross-checked against the PDF.
- **Zero `CONTRADICTED` verdicts.** No note in the library makes a claim the source PDF actively refutes.

**Caveats:**
- Notes are a snapshot, not a live database. The current main-branch audit state was checked locally on 2026-07-07.
- The audit catches hallucinations and direction-reversals, but cannot catch issues in the source paper itself. Always cite the original paper for any claim of substance.
- `PARTIAL` verdicts indicate minor paraphrastic drift or compression; they are listed in the per-paper audit JSONs but those JSONs are not published to the repo (they contain per-paper reasoning that is better regenerated on demand).

---

## 6. How to cite when your agent surfaces a note

- **Citing the underlying paper:** Use the APA citation block at the bottom of each note's body. That's the canonical citation; the DOI is in the frontmatter and is machine-verifiable via CrossRef.
- **Citing this knowledge base as a research tool:** If your agent or application uses Management Research Notes as a retrieval source, please cite the repository itself:

> Tang, B. (2026). *Management Research Notes: A File-Based Academic Knowledge Base for Management and Business Sustainability Research* (Version 0.31.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.19564336

Or see [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

---

## 7. What this repository is NOT

- **Not a live database.** It's a Git-versioned snapshot. Each commit is a reproducible state; tagged releases are archived on Zenodo with DOIs.
- **Not a replacement for reading the papers.** Notes are a distillation, not a substitute. For any claim of academic substance, cite the original.
- **Not the trusted source for bibliographic metadata.** `library/.../manifest.tsv` is the trusted source (populated from journal TOCs, publisher APIs, and CrossRef). Notes derive from the manifest; if they disagree, the manifest wins.
- **Not a Python package.** There's no PyPI install; the pipeline ships as scripts in `tools/`. Clone the repo to use it locally.
- **Not a search engine.** No hosted query endpoint. Agents that want low-latency search should load `index/synapse.db` locally or into a hosted SQLite service of their choice.

---

## Contact and contribution

- Open an issue at https://github.com/binqi20/management-research-notes/issues
- Pull requests welcome — please pass `tools/validate_note.py` and `tools/audit_note.py` before submission.
- The maintainer is [Binqi Tang](https://github.com/binqi20) ([ORCID](https://orcid.org/0000-0002-5095-3710)).
