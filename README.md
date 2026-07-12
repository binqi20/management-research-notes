# Management Research Notes

**A file-based academic knowledge base for management and business sustainability research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Notes](https://img.shields.io/badge/curated%20notes-1167-brightgreen.svg)](notes/)
[![Sources](https://img.shields.io/badge/sources-NBS%20%2B%20AMJ-orange.svg)](#whats-in-this-snapshot)
[![Audit](https://img.shields.io/badge/audit-1167%2F1167%20PASS-success.svg)](#faithfulness-audit)
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
  practical implication, limitations, future research) a fresh independent
  auditor reads the PDF, reads the note, and emits a per-field verdict
  against the rubric at [`docs/audit-rubric.md`](docs/audit-rubric.md):
  `SUPPORTED` / `PARTIAL` / `UNSUPPORTED` / `CONTRADICTED`. A note is
  rejected if any verdict is `UNSUPPORTED` or `CONTRADICTED`.

The full library has been swept across releases:

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
- **v0.19.0 sweep (2026-05-23, 270 notes):**
  Adds AMJ vol. 66 no. 1 (12 substantive papers + Gruber editorial on
  the 23rd editorial term's strategic priorities). **270 / 270 PASS, 0
  UNSUPPORTED, 0 CONTRADICTED, 0 PARTIAL** — the third perfectly-clean
  batch (after v0.12.0 and v0.15.0). This release also served as a
  **standalone validation of two infrastructure fixes from prior
  releases**:
  - **`extraction_model` verbatim** (codified in v0.18.0, commit
    `cc16c71`): extraction agents were deliberately dispatched WITHOUT
    the inline reminder; 13/13 still kept the field uniform purely
    from reading `docs/extraction-prompt.md`. The codified location is
    independently load-bearing.
  - **Editorial-abstract escape** (added in commit `5b4ae81`,
    pre-v0.19.0): Gruber editorial — the first editorial extracted
    after the fix — wrote `"Not reported in paper"` for Abstract
    instead of the sentence-fragment workaround used by all five
    earlier editorials.
  13/13 Layer 1 first-try PASS (eighth consecutive batch at 100%).
  All three gates exit 0; zero post-extraction remediation needed.
- **v0.19.1 patch (2026-05-27, 270 notes):**
  Provenance correction — `extraction_model` field. No content changes;
  no new notes. The v0.18.0 fix had standardized this field to
  `claude-opus-4-6` (the bundle's stale default), but the actual
  extraction model for batches from **2026-04-18 onward** was
  Claude Opus 4.7 (the parent session's model, with 57 notes carrying
  direct agent self-reports as evidence). Updated 108 notes that
  predated my v0.18.0 fix-to-verbatim with the accurate `claude-opus-4-7`
  value; left 105 pre-cutover notes at `claude-opus-4-6` (no direct
  evidence of model identity for those earlier batches). Constant in
  `tools/prepare_paper.py` updated to `claude-opus-4-7` so future
  bundles record the accurate model. Library is now provenance-correct
  for everything where we have direct evidence; pre-cutover notes
  retain their original metadata as historical record. All three gates
  still exit 0 after the sweep (provenance field is not validated or
  audited).

- **v0.20.0 sweep (2026-06-11, 352 notes):**
  Adds the NBS **December 2025** monthly digest — **82 peer-reviewed
  papers** across *Ecological Economics* (including the biodiversity-and-
  finance special issue), AMJ, *Business & Society*, *Review of Finance*,
  *Strategic Management Journal*, and others. **82 / 82 PASS** (Layer 1 +
  Layer 2). Introduced **masthead-based SSRN→published detection** (read the
  page masthead, not the footer DOI, to catch working papers that reached
  their journal version — 9 upgraded to the published DOI/metadata) and a
  **code-orchestrated parallel-dispatch extraction workflow** whose
  `pipeline()` fan-out guarantees the subagent count, eliminating
  hand-dispatch drift. Four incomplete-PDF stubs (Soboleva, Thomas, Willis,
  Zhu) were re-acquired and ingested. A separate commit cleaned CrossRef
  metadata drift in 7 prior-release NBS-2026-02 notes (vol/issue/pages now
  indexed). All three gates exit 0; 6 *Review of Finance* DOIs are valid but
  CrossRef-pending and will verify once indexed.

- **v0.21.0 sweep (2026-06-23, 465 notes):**
  Adds the NBS **January 2026** monthly digest — **113 peer-reviewed
  papers**, led by the *Journal of Business Ethics* (40) with *Research
  Policy* (14), the *Journal of Environmental Economics and Management*,
  *Organization Science*, *Human Relations*, *The Journal of Finance*,
  *MIS Quarterly*, and others. **113 / 113 PASS** (Layer 1 + Layer 2).
  Each batch ran as two ~5–6-paper waves through the `pipeline()`
  extraction workflow to stay under a transient server rate-limit while
  keeping the subagent count code-guaranteed. Surfaced more SSRN working
  papers that had reached their published journal version (upgraded to
  the journal DOI/metadata — e.g. Wang → *Journal of Business Ethics*,
  Duguay → *Journal of Accounting and Economics*) and several
  filename-lossy title restorations (dropped colons / question marks
  repaired against CrossRef). Seven incomplete-PDF stubs were found; six
  were re-acquired and ingested and one (Myers, a special-issue
  editorial) was skipped. A separate commit cleaned CrossRef metadata
  drift in 3 prior-release NBS-2026-02 notes. All three gates exit 0
  (validate, verify_metadata, lint_manifests).

- **v0.22.0 sweep (2026-06-24, 542 notes):**
  Adds **Academy of Management Journal volume 65, issues 1-6** — **77
  peer-reviewed papers** with issue counts **13, 13, 13, 12, 13, 13**.
  This completes AMJ pilot coverage from vol. 65 no. 1 through vol. 69
  no. 1. **77 / 77 PASS** the faithfulness audit for the AMJ volume-65
  batch; the full library now has **542 / 542 PASS**, 0 `UNSUPPORTED`,
  and 0 `CONTRADICTED` verdicts. All six AMJ volume-65 manifests lint
  cleanly, all notes validate, and CrossRef metadata verification exits
  0 with no mismatches. The public indexes were rebuilt from notes:
  SQLite, CSV, and BibTeX all contain 542 records.

- **v0.23.0 sweep (2026-06-27, 617 notes):**
  Adds **Academy of Management Journal volume 64, issues 1-6** — **75
  peer-reviewed papers** with issue counts **12, 12, 13, 12, 13, 13**.
  This completes AMJ pilot coverage from vol. 64 no. 1 through vol. 69
  no. 1. **75 / 75 PASS** the faithfulness audit for the AMJ volume-64
  batch; the full library now has **617 / 617 PASS**, 0 `UNSUPPORTED`,
  and 0 `CONTRADICTED` verdicts. All six AMJ volume-64 manifests lint
  cleanly, all notes validate, and CrossRef metadata verification exits
  0 with no mismatches; remaining notices are documented CrossRef-side
  false positives or lookup warnings. The public indexes were rebuilt from
  notes: SQLite, CSV, and BibTeX all contain 617 records.

- **v0.23.1 patch (2026-06-27, 617 notes):**
  Provenance correction for the AMJ volume-64 Codex batch. The 75 AMJ
  volume-64 notes now record `extraction_model: "gpt-5.5"` instead of the
  stale bundle value `claude-opus-4-8`. Five audit-identified wording issues
  were narrowed: Abdurakhmonov et al. (2021) removed an overbroad
  country-generalization phrase, Jacobs et al. (2021) softened a direct
  practical prescription to a case-grounded association, Lifshitz-Assaf et al.
  (2021) removed an unsupported stage-gate reference, Bain et al. (2021)
  distinguished experimental boundary tests from the Study 3 intervention
  target, and Ji et al. (2021) removed an unstated national/historical-setting
  limitation. Abstracts, evidence anchors, bibliographic metadata, and
  citations are unchanged. The patch also makes GPT-5.5 the
  current Codex extraction/audit default in the workflow docs and sets
  issue-level parallelism to a fixed 6-agent cap with fallback to 5, 3, or
  serial execution if stability degrades.

- **v0.24.0 sweep (2026-06-28, 691 notes):**
  Adds **Academy of Management Journal volume 63, issues 1-6** — **74
  peer-reviewed papers** with issue counts **13, 12, 12, 12, 12, 13**.
  This extends AMJ pilot coverage backward to vol. 63 no. 1, so the AMJ
  pilot now spans vol. 63 no. 1 through vol. 69 no. 1. **74 / 74 PASS**
  the faithfulness audit for the AMJ volume-63 batch; the full library now
  has **691 / 691 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` verdicts.
  All six AMJ volume-63 manifests lint cleanly, all notes validate, and
  CrossRef metadata verification exits 0 with no mismatches; remaining
  notices are documented CrossRef-side false positives or lookup warnings.
  The public indexes were rebuilt from notes: SQLite, CSV, and BibTeX all
  contain 691 records.

- **v0.25.0 sweep (2026-06-30, 767 notes):**
  Adds **Academy of Management Journal volume 62, issues 1-6** — **76
  peer-reviewed papers** with issue counts **12, 12, 13, 13, 12, 14**.
  This extends AMJ pilot coverage backward to vol. 62 no. 1, so the AMJ
  pilot now spans vol. 62 no. 1 through vol. 69 no. 1. **76 / 76 PASS**
  the faithfulness audit for the AMJ volume-62 batch; the full library now
  has **767 / 767 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` verdicts.
  All six AMJ volume-62 manifests lint cleanly, all notes validate, and
  scoped CrossRef metadata verification for all 76 AMJ volume-62 notes exits
  0 with no mismatches. The full-library CrossRef sweep was attempted during
  release preparation but interrupted by a network-level HTTPS handshake stall;
  existing pre-AMJ62 notes were unchanged from the v0.24.0 metadata-verified
  snapshot. The public indexes were rebuilt from notes: SQLite, CSV, and
  BibTeX all contain 767 records.

- **v0.26.0 sweep (2026-07-02, 860 notes):**
  Adds **Academy of Management Journal volume 61, issues 1-6** — **93
  peer-reviewed papers** with issue counts **16, 16, 15, 15, 16, 15**.
  This extends AMJ pilot coverage backward to vol. 61 no. 1, so the AMJ
  pilot now spans vol. 61 no. 1 through vol. 69 no. 1. **93 / 93 PASS**
  the faithfulness audit for the AMJ volume-61 batch; the full library now
  has **860 / 860 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` verdicts.
  All six AMJ volume-61 manifests lint cleanly, all notes validate, and
  scoped CrossRef metadata verification for all 93 AMJ volume-61 notes exits
  0 with no mismatches. The audit sweep has one non-blocking `PARTIAL`
  verdict (Aristidou 2018 limitations), retained as harmless compression
  around scope-boundary wording rather than a faithfulness failure. The
  public indexes were rebuilt from notes: SQLite, CSV, and BibTeX all
  contain 860 records.

- **v0.27.0 sweep (2026-07-03, 955 notes):**
  Adds **Academy of Management Journal volume 60, issues 1-6** — **95
  peer-reviewed papers** with issue counts **16, 16, 16, 17, 15, 15**.
  This extends AMJ pilot coverage backward to vol. 60 no. 1, so the AMJ
  pilot now spans vol. 60 no. 1 through vol. 69 no. 1. **95 / 95 PASS**
  the faithfulness audit for the AMJ volume-60 batch; the full library now
  has **955 / 955 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` verdicts.
  All six AMJ volume-60 manifests lint cleanly, all notes validate, and
  scoped CrossRef metadata verification for all 95 AMJ volume-60 notes exits
  0 with no mismatches; two AMJ volume-60 author-name notices are documented
  as CrossRef-side family-name parsing false positives. Two audit-identified
  future-research fields (Fan 2017 and Katila 2017) were narrowed before
  release; the final AMJ volume-60 audit scan has 570 / 570 prose-field
  verdicts `SUPPORTED`, 0 `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED`.
  The public indexes were rebuilt from notes: SQLite, CSV, and BibTeX all
  contain 955 records.

- **v0.28.0 sweep (2026-07-05, 1,050 notes):**
  Adds **Academy of Management Journal volume 59, issues 1-6** — **95
  peer-reviewed papers** with issue counts **16, 15, 16, 16, 16, 16**.
  This extends AMJ pilot coverage backward to vol. 59 no. 1, so the AMJ
  pilot now spans vol. 59 no. 1 through vol. 69 no. 1. **95 / 95 PASS**
  the faithfulness audit for the AMJ volume-59 batch; the full library now
  has **1,050 / 1,050 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED`
  verdicts. All six AMJ volume-59 manifests lint cleanly, all notes
  validate, and scoped CrossRef metadata verification for all 95 AMJ
  volume-59 notes exits 0 with two documented CrossRef-side title false
  positives in issue 1 (Durand and Zavyalova malformed inline HTML). The
  final AMJ volume-59 audit scan has 570 / 570 prose-field verdicts
  `SUPPORTED`, 0 `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED`. The
  public indexes were rebuilt from notes: SQLite, CSV, and BibTeX all
  contain 1,050 records.

- **v0.29.0 sweep (2026-07-07, 1,128 notes):**
  Adds **Academy of Management Journal volume 58, issues 1-6** — **78
  peer-reviewed papers** with issue counts **13, 13, 13, 13, 13, 13**.
  This extends AMJ pilot coverage backward to vol. 58 no. 1, so the AMJ
  pilot now spans vol. 58 no. 1 through vol. 69 no. 1. **78 / 78 PASS**
  the faithfulness audit for the AMJ volume-58 batch; the full library now
  has **1,128 / 1,128 PASS**, 0 `UNSUPPORTED`, and 0 `CONTRADICTED`
  verdicts. All six AMJ volume-58 manifests lint cleanly, all notes
  validate, and scoped CrossRef metadata verification for all 78 AMJ
  volume-58 notes exits 0 with three documented CrossRef-side false
  positives: Byron title inline-HTML spacing, Little / Smith Major author
  parsing, and Joshi title inline-HTML spacing. Six audit-identified
  prose fields were narrowed before release (Eggers, Gabriel, Gurses,
  Kish-Gephart, Lioukas, and Wo); the final AMJ volume-58 audit scan has
  468 / 468 prose-field verdicts `SUPPORTED`, 0 `PARTIAL`,
  0 `UNSUPPORTED`, and 0 `CONTRADICTED`. The public indexes were rebuilt
  from notes: SQLite, CSV, and BibTeX all contain 1,128 records.

- **v0.30.0 tooling (2026-07-09, 1,128 notes):**
  Schema-and-tooling release — **no new notes**. Introduces extraction
  **v3**, which adds three empirical body sections to every future note —
  **Hypotheses / Propositions**, **Data & Measures**, and **Key
  Findings** — plus three matching Layer 1 evidence anchors
  (`hypotheses_source`, `measures_overview`, `findings_overview`) and
  three new Layer 2 audited prose fields under audit rubric **v2**
  (nine fields for v3 notes; a reversed finding direction is
  `CONTRADICTED`, per the sign-reversal rule). Applied going-forward
  only: the validator, auditor, and indexer are version-gated on
  `extraction_version`, all 1,128 existing v1/v2 notes revalidate
  unchanged (**1,128 / 1,128 OK**), and the rebuilt SQLite/CSV indexes
  carry the three new columns (still 1,128 records; `key_findings` and
  `hypotheses` are FTS5-searchable). Also adds
  `docs/pipeline-runbook.md` — a vendor-neutral ingest/audit/publish
  runbook referenced from `AGENTS.md` — hardens the shared CrossRef
  client (retry-with-backoff, negative 404 caching) used by all three
  metadata gates, and fixes stale documentation references
  (`ingest_batch.py`, the tools list, the audit invocation examples).

- **v0.31.0 sweep (2026-07-10, 1,141 notes):**
  Adds **Academy of Management Journal volume 57, issue 1** — **13
  peer-reviewed papers** — the **first live extraction-v3 issue**: every
  empirical note carries Hypotheses / Propositions, Data & Measures, and
  Key Findings with three additional verbatim evidence anchors, audited
  under rubric v2 (nine prose fields per note). All 13 extractions
  validated on the first attempt; the final audit scan has
  **117 / 117 prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`,
  0 `UNSUPPORTED`, and 0 `CONTRADICTED`. Two audit-loop repairs before
  release: one note narrowing (Marr: per-study status-loss manipulation
  attribution) and one **tooling fix** — the audit prompt's
  references-stripper false-matched a line-initial prose sentence
  ("References to relationships…", Koerner) and cut the Discussion from
  the audit input; the stripper gained a prose-guard plus regression
  tests, and Koerner re-audited cleanly against the full text. The
  release also raises the audit text budget to 240K chars with
  anchor-aware splicing (every evidence anchor's context is guaranteed
  visible to the auditor), migrates both CrossRef false-positive
  registries to JSON data files (`tools/known_crossref_issues.json`,
  `tools/known_compound_surnames.json`), adds a `--model` provenance
  flag to the ingest tools (this issue's notes record
  `claude-fable-5`), and adds anti-overreach scope guidance to the
  extraction prompt. Manifest lint and scoped CrossRef pass 13/13 with
  zero new false-positive entries; SQLite, CSV, and BibTeX all contain
  1,141 records.

- **v0.37.0 v3 backfill batch 04 (2026-07-12, 1,167 notes):**
  Upgrades **AMJ volume 68, issue 1 and volume 67, issue 6, 18 notes total** to
  the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 997 v2, 109 v3. Each touched
  note passed a fresh full independent 9-field rubric-v2 audit: **160 / 162
  prose-field verdicts `SUPPORTED`, 0 `UNSUPPORTED`, 0 `CONTRADICTED`** (all 18
  notes overall pass). These two issues' older v2 notes carried an unusual
  amount of scope drift in their practical-implication and future-research
  fields, so eighteen evidence-based repairs across two rounds narrowed added
  audiences, prescriptions, and examples back to the papers' own scope (and
  fixed three factual slips). Two residual `PARTIAL`s were accepted and
  documented rather than edited: the Hagtvedt future-research note lightly
  extends a stated limitation, and the Trzebiatowski data-measures note carries
  a source-ambiguous turnover lag that is internally consistent with the
  paper's methods — editing either to appease the auditor would violate the
  faithful-note rule.

- **v0.36.0 v3 backfill batch 03 (2026-07-11, 1,167 notes):**
  Upgrades **AMJ volume 68, issue 3 and issue 2, 16 notes total** to the v3
  schema — all v2 augmentations (the AMJ v1 re-extraction tier was cleared in
  batch 02, so batches 03+ are pure augmentation). The **record total is
  unchanged at 1,167**; the version-tier census shifts to 61 v1, 1,015 v2, 91
  v3. Each touched note passed a fresh full independent 9-field rubric-v2
  audit: **144 / 144 prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`,
  0 `UNSUPPORTED`, 0 `CONTRADICTED`, after two evidence-based scope repairs
  (the Fitzsimons and Knight practical implications were narrowed to the
  paper's own stated audience and claims).

- **v0.35.0 v3 backfill batch 02 (2026-07-11, 1,167 notes):**
  Upgrades **AMJ volume 68, issue 5 and issue 4, 19 notes total** to the v3
  schema (11 legacy v1 notes fully re-extracted, 8 v2 notes augmented in
  place). The **record total is unchanged at 1,167**; the version-tier census
  shifts to 61 v1, 1,031 v2, 75 v3, and one re-extracted note (Lazar) was
  reclassified empirical-mixed → empirical-quantitative. Each touched note
  passed a fresh full independent 9-field rubric-v2 audit: **170 / 171
  prose-field verdicts `SUPPORTED`, 0 `UNSUPPORTED`, 0 `CONTRADICTED`**, after
  five evidence-based repairs (per-study support-pattern and scope corrections
  on Chung, Dutta, and Preston). One residual `PARTIAL` remains, on the Li
  note's Limitations: its "30% and 7%" mediation figures are verbatim-faithful
  to the paper, but two-column typesetting splices that sentence into the
  reference list, so the independent auditor could not re-verify the 7% — the
  faithful sentence was left unchanged rather than edited to appease the
  extraction artifact.

- **v0.34.0 v3 backfill batch 01 (2026-07-11, 1,167 notes):**
  Upgrades the two most recent AMJ issues to the v3 schema — **AMJ volume 69,
  issue 1 and volume 68, issue 6, 17 notes total** (16 legacy v1 notes fully
  re-extracted, 1 v2 note augmented in place). This adds Hypotheses /
  Propositions, Data & Measures, and Key Findings to every note in both issues;
  the **record total is unchanged at 1,167** (a backfill adds no papers). Each
  touched note passed a fresh full independent 9-field rubric-v2 audit:
  **153 / 153 prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED`, after three evidence-based repairs (Peng and Lee
  key-findings over-generalizations, and the Mahringer note's practical
  implication narrowed to the paper's own scope). The version-tier census
  shifts accordingly: 72 v1, 1,039 v2, 56 v3.

- **v0.33.0 sweep (2026-07-11, 1,167 notes):**
  Adds **Academy of Management Journal volume 57, issue 3** — **13
  peer-reviewed papers** produced under extraction v3 and independently
  audited under rubric v2. One audit-identified field was repaired from
  PDF evidence before release: Crossland's Theoretical Contribution had
  listed CEO tenure among the constructs the paper's discriminant-validity
  analysis distinguished career variety from (the tests covered openness to
  experience, risk propensity, age, and education, not tenure). A fresh
  re-audit cleared the repair; the final issue scan has **117 / 117
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`, and
  0 `CONTRADICTED`. All 13 notes validate, the manifest lints cleanly, and
  scoped CrossRef verification matches all seven checked bibliographic fields
  for every paper. SQLite, CSV, and BibTeX were rebuilt sequentially and each
  contains 1,167 records.

- **v0.32.0 sweep (2026-07-10, 1,154 notes):**
  Adds **Academy of Management Journal volume 57, issue 2** — **13
  peer-reviewed papers** produced under extraction v3 and independently
  audited under rubric v2. Three audit-identified fields were repaired from
  PDF evidence before release: Beckman's board-measure timing, Rogan's
  agency-level robustness qualification, and Wang's patent-count-mediated
  indirect pathway. Fresh re-audits cleared each repair; the final issue scan
  has **117 / 117 prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`,
  0 `UNSUPPORTED`, and 0 `CONTRADICTED`. All 13 notes validate, the manifest
  lints cleanly, and scoped CrossRef verification matches all seven checked
  bibliographic fields for every paper. SQLite, CSV, and BibTeX were rebuilt
  sequentially and each contains 1,154 records.

Run the audit on a single note. Layer 1 (the mechanical anchor check) runs
standalone; the full two-layer audit reads an independent auditor's verdict:

```bash
# Layer 1 only (mechanical evidence-anchor check):
python tools/audit_note.py notes/<paper_id>.md --skip-layer-2

# Full two-layer audit (Layer 2 verdict supplied by an independent auditor):
python tools/audit_note.py notes/<paper_id>.md \
  --layer-2-json incoming/_audits/<paper_id>.layer2.json
```

Or, from inside a Claude Code session: `/audit-note <paper_id>`.

## What's in this snapshot

This main-branch snapshot contains **1,167 curated notes**:

- **NBS 2026-02** — 77 notes distilled from the [Network for Business
  Sustainability (NBS)](https://nbs.net/) February 2026 monthly research
  digest. (62 notes shipped in v0.2.0; 15 previously-missing papers were
  recovered and added in v0.3.0.)
- **NBS 2025-12** — 82 notes from the NBS **December 2025** monthly digest, spanning the *Ecological Economics* biodiversity-and-finance special issue, AMJ, *Business & Society*, *Review of Finance*, *Strategic Management Journal*, and other journals (added in v0.20.0).
- **NBS 2026-01** — 113 notes from the NBS **January 2026** monthly digest, led by the *Journal of Business Ethics* (40) with *Research Policy* (14), the *Journal of Environmental Economics and Management*, *Organization Science*, *Human Relations*, *The Journal of Finance*, *MIS Quarterly*, and other journals (added in v0.21.0).
- **AMJ pilot** — 895 notes across 70 recent issues of
  the [Academy of Management Journal](https://journals.aom.org/journal/amj)
  (vol. 57 no. 1 through vol. 57 no. 3, vol. 58 no. 1 through vol. 58 no. 6, vol. 59 no. 1 through vol.
  59 no. 6, vol. 60 no. 1 through vol.
  60 no. 6, vol. 61 no. 1 through vol.
  61 no. 6, vol. 62 no. 1 through vol.
  62 no. 6, vol. 63 no. 1 through vol.
  63 no. 6, vol. 64 no. 1 through vol.
  64 no. 6, vol. 65 no. 1 through vol.
  65 no. 6, vol. 66 no. 1 through vol.
  66 no. 6, vol. 67 no. 1 through vol. 67 no. 6, vol. 68 no. 1
  through vol. 68 no. 6, and vol. 69 no. 1).
  v0.33.0 added vol. 57 no. 3 (13 notes);
  v0.32.0 added vol. 57 no. 2 (13 notes); v0.31.0 added vol. 57 no. 1
  (13 notes, the first extraction-v3 issue);
  v0.29.0 added vol. 58 no. 1-6 (78 notes);
  v0.28.0 added vol. 59 no. 1-6 (95 notes);
  v0.27.0 added vol. 60 no. 1-6 (95 notes);
  v0.26.0 added vol. 61 no. 1-6 (93 notes);
  v0.25.0 added vol. 62 no. 1-6 (76 notes);
  v0.24.0 added vol. 63 no. 1-6 (74 notes);
  v0.23.0 added vol. 64 no. 1-6 (75 notes);
  v0.22.0 added vol. 65 no. 1-6 (77 notes);
  v0.19.0 added vol. 66 no. 1 (13 notes); v0.18.0 added vol. 66 no. 2
  (13 notes); v0.17.0 added vol. 66 no. 3 (11 notes); v0.16.0 added
  vol. 66 no. 4 (11 notes); v0.15.0 added vol. 66 no. 5 (12 notes);
  v0.14.0 added vol. 66 no. 6 (13 notes); v0.13.0 added vol. 67 no. 1
  (11 notes); v0.12.0 added vol. 67 no. 2 (11 notes); v0.11.0 added
  vol. 67 no. 3 (10 notes); v0.10.0 added vol. 67 no. 4 (9 notes);
  v0.9.0 added vol. 67 no. 5 (9 notes); v0.8.0 added vol. 67 no. 6
  (8 notes); v0.7.0 added vol. 68 no. 1 (10 notes); v0.6.0 added vol.
  68 no. 2 (8 notes); v0.5.0 added vol. 68 no. 3 (8 notes); v0.4.0
  added vol. 68 no. 4 (8 notes); the original pilot covered the
  remaining three issues (28 notes).

| Paper type             | Count |
|------------------------|------:|
| empirical-quantitative |   668 |
| empirical-qualitative  |   247 |
| empirical-mixed        |   111 |
| editorial              |    72 |
| conceptual             |    54 |
| review                 |     9 |
| book-review            |     6 |
| **Total**              | **1,167** |

All notes have passed the semantic audit. The corpus contains 61 legacy v1
notes, 997 v2 notes, and 109 v3 notes; v2/v3 notes carry an `evidence:` anchor
block checked by Layer 1, and v3 notes add Hypotheses / Propositions, Data &
Measures, and Key Findings. See [Faithfulness audit](#faithfulness-audit) above.

## Repository layout

```
management-research-notes/
├── README.md                          ← you are here
├── AGENTS.md                          ← tool-agnostic entry point for AI agents
├── LICENSE                            ← MIT
├── CITATION.cff                       ← cite-this-repo metadata
├── CLAUDE.md                          ← rules for any Claude Code session in this folder
├── docs/
│   ├── extraction-prompt.md           ← the canonical extraction prompt (v3)
│   └── audit-rubric.md                ← rubric the Layer 2 auditor uses
├── notes/                             ← 1,167 curated paper notes (the source of truth)
│   └── nbs-2026-02-spoor-2026.md
├── index/                             ← derived views, all rebuildable
│   ├── synapse.db                     ← SQLite + FTS5 (~19 MB)
│   ├── papers.csv                     ← flat tabular export
│   ├── library.bib                    ← BibTeX, one @article per note
│   └── topics.json                    ← 14-domain controlled vocabulary
├── tools/                             ← the Python pipeline
│   ├── pdf_to_text.py                 ← PDF → plain text (pdftotext + pdfplumber)
│   ├── populate_manifest.py           ← Tier 3 gate: backfill vol/issue/pages + fix year (CrossRef)
│   ├── lint_manifests.py              ← structural manifest lint (catches name-capture bugs)
│   ├── prepare_paper.py               ← bundle a paper for extraction
│   ├── ingest_batch.py                ← walk a folder of PDFs
│   ├── validate_note.py               ← verbatim-abstract + bib + taxonomy + anchors
│   ├── audit_note.py                  ← two-layer faithfulness audit (Layer 1 + Layer 2)
│   ├── verify_metadata.py             ← Tier 2 gate: cross-check bib fields vs CrossRef (verify_years.py = year-only alias)
│   ├── build_index.py                 ← rebuild SQLite from notes/
│   ├── export_csv.py                  ← rebuild papers.csv
│   └── export_bibtex.py               ← rebuild library.bib
├── library/
│   ├── NBS/2026-02/
│   │   ├── manifest.tsv               ← trusted bibliographic source for the batch
│   │   └── missing.tsv                ← papers NBS listed but PDFs unavailable
│   └── AMJ/vol-58-no-1 ... vol-69-no-1/
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
  version      = {0.37.0},
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
  continue the AMJ backfill into earlier volumes, keeping paper IDs stable
  across updates.
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
- **OpenAI Codex** for the issue-level extraction and independent-audit
  orchestration used in the AMJ volume 64 backfill.
- The authors of every paper in `notes/` — without their original scholarship,
  there is nothing to distill.

---

*Maintained by [Binqi Tang](https://github.com/binqi20). MIT licensed. Issues
and PRs welcome.*
