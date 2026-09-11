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
**1,167 curated notes** on peer-reviewed papers in management and business
sustainability research. The current v0.68.0 main-branch snapshot contains 272
Network for Business Sustainability notes (2025-12, 2026-01, 2026-02)
and 895 Academy of Management Journal pilot notes across 70 recent issues
(vol. 57 no. 1-3, plus vol. 58 no. 1 through vol. 69 no. 1). Every note is a single Markdown
file with YAML frontmatter and a structured Markdown body. The repository
is MIT licensed; individual PDFs are not redistributed.

**Why it exists for agents specifically.** Raw PDFs are expensive to load
in bulk and their text layers vary in quality. These notes are a
distilled, uniform, verbatim-anchored representation that fits in a
context window, supports structured querying, and carries strong
faithfulness guarantees (see §5). An agent can load the whole library
into a context window when it fits, or query SQL/FTS5 for specific slices,
then verify substantive claims against the original paper.

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

**Current main-branch audit state (2026-09-11, v0.68.0): 1,167 / 1,167
stored official reports PASS, 0 UNSUPPORTED, 0 CONTRADICTED.** The audit
fitter repair was checked against all 1,167 immutable source texts in two
byte-identical sweeps: 528 same, 88 improved, one reference-heading/whitespace
addition, and 550 no-match. Every OLD retained source interval remains
visible in NEW, all 14 victim papers and 42 scoped field proofs pass, and
no paper gains sandwich or appendix truncation. The appendix cap is 60K;
the existing shared 240K budget and anchor-splice allowance are unchanged.

Thirty-one notes received fresh blind full nine-field audits on
`gpt-6-astra` under standard fitted input. Their baseline was 239 SUPPORTED
and 40 PARTIAL. After four source-verified, user-approved repairs, the final
state is **276 SUPPORTED / 3 accepted framing PARTIALs**. All 31 notes
validate, and their official reports and sidecars match the full current
note and source hashes. **39 previously accepted text-loss PARTIALs are
now SUPPORTED.** Fang's Future Research retains a PARTIAL for framing,
with all relevant source visible. Kim and Eggers each pass 9/9 under
standard fitted input; their historical full-raw-text exceptions are
superseded, with all original evidence preserved.

Four already-published fields needed correction: Kotha's Key Findings
reversed the licensing-fee payment direction (CONTRADICTED in first pass);
Foulk's Practical Implication reversed the direction of accountability
feedback; Shea's Key Findings omitted the feedback-task-first condition;
and Fang's Key Findings omitted parental variables from the baseline
controls. All four repaired fields now score SUPPORTED. Their source
passages were visible even before the fitter change. These findings show
why a passing audit is evidence of review, not proof that every claim is
correct. No NBS notes, bibliographic frontmatter, historical provenance,
evidence anchors, or cleanup-queue entries changed.

The **remaining AMJ accepted PARTIAL list in v0.68.0 is 25 fields across
22 notes**. Three are framing verdicts from this session: Sherf (2019),
Future Research (objective field-performance example); Ferns (2022),
Practical Implication (the Occupy explanation is more definite than the
source); and Fang (2022), Future Research (social-capital/personality
examples extend the explicit agenda). Their relevant field text is
unchanged. The other 11 fields within the reviewed ledger inventory are
non-tooling cases retained without fresh audits; Wang (2021), Future
Research was adjudicated from raw text. Another 11 earlier-batch fields
were outside the authorized inventory and remain untouched.

| Note | Remaining PARTIAL fields | Disposition in v0.68.0 |
|---|---|---|
| Deken (2018), AMJ 61-5 | Future Research | Prior non-tooling acceptance |
| Sherf (2019), AMJ 62-2 | Future Research | Framing; source visible |
| Nigam (2019), AMJ 62-4 | Practical Implication | Prior non-tooling acceptance |
| Simsek (2019), AMJ 62-4 | Limitations | Prior non-tooling acceptance |
| Lin (2019), AMJ 62-5 | Future Research | Prior non-tooling acceptance |
| Wang (2021), AMJ 64-6 | Limitations; Future Research | Framing/locality; raw-text adjudication |
| Dushnitsky (2022), AMJ 65-1 | Key Findings | Paper-internal inconsistency |
| Fang (2022), AMJ 65-3 | Future Research | Framing; source visible |
| Ferns (2022), AMJ 65-4 | Practical Implication | Framing; source visible |
| Lazar (2022), AMJ 65-4 | Data & Measures | Paper-internal inconsistency |
| Koppman (2022), AMJ 65-5 | Limitations | Prior non-tooling acceptance |
| Matusik (2022), AMJ 65-5 | Future Research | Prior non-tooling acceptance |
| Williams (2022), AMJ 65-5 | Future Research | Prior non-tooling acceptance |
| Xu (2022), AMJ 65-6 | Data & Measures; Future Research | Earlier batch; outside scope |
| Chan (2023), AMJ 66-1 | Practical Implication | Earlier batch; outside scope |
| Dwertmann (2023), AMJ 66-1 | Mechanism Process; Theoretical Contribution | Earlier batch; outside scope |
| Lauriano (2023), AMJ 66-1 | Data & Measures | Earlier batch; outside scope |
| Hersel (2023), AMJ 66-2 | Data & Measures | Earlier batch; outside scope |
| Toivonen (2023), AMJ 66-3 | Practical Implication | Earlier batch; outside scope |
| Hagtvedt (2024), AMJ 68-1 | Future Research | Earlier batch; outside scope |
| Trzebiatowski (2024), AMJ 68-1 | Data & Measures | Earlier batch; outside scope |
| Li (2025), AMJ 68-4 | Limitations | Earlier batch; outside scope |

The v0.68.0 census remains **61 v1 / 211 v2 / 895 v3**, with all 895 AMJ
notes at v3 across 70 issues; the 272 remaining v1/v2 notes are NBS. All
four repaired notes are reflected in the rebuilt indexes; notes, SQLite,
parsed CSV and BibTeX each contain 1,167 records. BibTeX is byte-identical.
The 272 legacy NBS reports have no stored hash provenance, so their
correspondence to current files cannot be established from those reports;
this is not evidence of unequal hashes. The documented Wiedner (2024)
frontmatter-only hash mismatch remains outside scope. Historical model
era stamps are preserved. Desai (2016), AMJ 59-3, retains its explicit
retraction statement. No later cross-family review result is asserted.

New notes are produced at extraction **v3**, which adds hypotheses, data &
measures, and key findings (see
[`docs/pipeline-runbook.md`](docs/pipeline-runbook.md)). **Augmented** v3
notes carry `augmented_model` / `augmented_at` frontmatter — the six
original prose fields were written by `extraction_model`, the three v3
sections by `augmented_model`, and the whole note passed a fresh full
9-field rubric-v2 audit at augmentation time (a mechanical diff-guard,
`tools/verify_augmentation.py`, proves the original audited content was
untouched before any explicitly documented audit repair). `PARTIAL`
verdicts (minor compression or claims whose supporting source passages are
missing from the fitted audit input) require documented review and do not
block publication when source verification supports the documented
acceptance. The v0.68.0 official reports contain no remaining `UNSUPPORTED` or
`CONTRADICTED` verdicts. A CONTRADICTED verdict was returned on a batch-28
draft and repaired before that release; this session also detected and
repaired a contradiction in the already-published Kotha note. Audit
outcomes do not establish that all undetected errors are absent.

Agents querying the data can rely on the following:

- **Every abstract is a verbatim substring of the source PDF.** If your agent quotes an abstract from a note, it is quoting the paper.
- **Every factual claim in v2 note frontmatter is anchored.** If your agent cites a sample size or a theory from v2 frontmatter, there is a verbatim PDF quote behind it in the `evidence:` block.
- **Every prose field has passed a semantic audit.** If your agent summarizes a research question, mechanism, or theoretical contribution from a note, it's quoting a claim that was independently cross-checked against the PDF.
- **Zero current `CONTRADICTED` verdicts in v0.68.0.** This describes the stored audit results, not an absolute guarantee that every source contradiction has been detected.

**Caveats:**
- Notes are a snapshot, not a live database. The current v0.68.0 main-branch audit state was checked locally on 2026-09-11.
- The audit catches hallucinations and direction-reversals, but cannot catch issues in the source paper itself. Always cite the original paper for any claim of substance.
- `PARTIAL` verdicts can indicate minor paraphrastic drift, compression, or missing source context in the fitted audit input; they are listed in the per-paper audit JSONs but those JSONs are not published to the repo (they contain per-paper reasoning that is better regenerated on demand).

---

## 6. How to cite when your agent surfaces a note

- **Citing the underlying paper:** Use the APA citation block at the bottom of each note's body. That's the canonical citation; the DOI is in the frontmatter and is machine-verifiable via CrossRef.
- **Citing this knowledge base as a research tool:** If your agent or application uses Management Research Notes as a retrieval source, please cite the repository itself:

> Tang, B. (2026). *Management Research Notes: A File-Based Academic Knowledge Base for Management and Business Sustainability Research* (Version 0.68.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.19564336

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
