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
  fresh-eyes LLM subagent cross-check the prose fields. Passing audits are
  evidence of review, not proof that every claim is correct. Verify
  substantive claims against the original paper before citing them.
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

- **v0.69.0 second-opinion sample and residual PARTIAL closeout (2026-09-13, 1,167 notes):**
  Forty-five AMJ notes received fresh blind full nine-field gpt-6-astra audits
  under the unchanged standard fitted input: a deterministic random sample of
  36 notes (12 per era) plus nine notes carrying 11 earlier accepted PARTIALs.
  Eligible frames contained 127 claude-opus-4-8, 270 claude-opus-5 and 279
  gpt-5.6-sol notes. Each stratum used random.Random(20260911).sample on its
  sorted eligible IDs, with no redraws or substitutions; editorials, the 31
  v0.68.0 re-audit notes and the residue set were excluded from the random
  frame.

  The frozen first pass returned 370 SUPPORTED / 30 PARTIAL / 0 UNSUPPORTED /
  5 CONTRADICTED across 405 fields. Parent raw-source adjudication identified
  30 distinct repair-class fields in 20 notes: 23 substantive and seven
  precision-grade defects. Five CONTRADICTED fields, 23 PARTIAL fields and two
  parent-flagged SUPPORTED fields needed repair; seven first-pass PARTIALs
  were accepted. The table below preserves this first-pass comparison and
  excludes later discoveries. S/P/U/C are auditor verdicts; defect counts
  include parent verification.

  | Stratum | First pass S / P / U / C | Affected notes, all / substantive only | Defective fields, all / substantive only |
  |---|---:|---|---|
  | claude-opus-4-8 | 90 / 14 / 0 / 4 | 10/12 (83.3%) / 8/12 (66.7%) | 17/108 (15.7%) / 13/108 (12.0%) |
  | claude-opus-5 | 104 / 4 / 0 / 0 | 3/12 (25.0%) / 2/12 (16.7%) | 3/108 (2.8%) / 2/108 (1.9%) |
  | gpt-5.6-sol | 106 / 2 / 0 / 0 | 1/12 (8.3%) / 1/12 (8.3%) | 1/108 (0.9%) / 1/108 (0.9%) |
  | Residue (purposive) | 70 / 10 / 0 / 1 | 6/9 (66.7%) / 6/9 (66.7%) | 9/81 (11.1%) / 7/81 (8.6%) |

  All includes substantive and precision grades. Substantive changes a
  contradicted direction, number, formula, unit, significance or attribution,
  or removes a claim/prescription the paper does not make. Precision preserves
  a supported core claim while correcting wording, coverage, scope or
  qualification. Each field takes its highest clause severity. The omitted but
  explicitly hypothesized Dwertmann mediator is graded precision as completion
  of an otherwise supported list; it remains repair-class. Grades are explicit
  parent judgments, not an independent severity rating. Affected-note rates
  count distinct notes, not defective clauses.

  | Stratum | Field family | Audited fields | Defects, all | Substantive only |
  |---|---|---:|---:|---:|
  | claude-opus-4-8 | Three v3 fields | 36 | 10/36 (27.8%) | 9/36 (25.0%) |
  | claude-opus-4-8 | Six legacy fields | 72 | 7/72 (9.7%) | 4/72 (5.6%) |
  | claude-opus-5 | Three v3 fields | 36 | 3/36 (8.3%) | 2/36 (5.6%) |
  | claude-opus-5 | Six legacy fields | 72 | 0/72 (0.0%) | 0/72 (0.0%) |
  | gpt-5.6-sol | Three v3 fields | 36 | 0/36 (0.0%) | 0/36 (0.0%) |
  | gpt-5.6-sol | Six legacy fields | 72 | 1/72 (1.4%) | 1/72 (1.4%) |
  | Residue (purposive) | Three v3 fields | 27 | 3/27 (11.1%) | 3/27 (11.1%) |
  | Residue (purposive) | Six legacy fields | 54 | 6/54 (11.1%) | 4/54 (7.4%) |

  The three v3 fields are Hypotheses, Data & Measures and Key Findings; the
  other six are legacy fields. These are schema families: native-v3 notes do
  not necessarily have a separate augmenter. No first-pass Hypotheses defect
  was found. Across the random sample, the first pass found 21/324 defective
  fields (6.5%) in 14/36 notes (38.9%); excluding precision, 16/324 fields
  (4.9%) in 11/36 notes (30.6%). First-pass accepted PARTIALs by era were 1,
  1 and 1, plus four in the residue set.

  Repair-round discoveries are separate: Fitzsimons Data & Measures mislabeled
  observation hours as meeting counts (substantive; the field was already
  counted for a different first-pass error); DesJardine Practical Implication
  attributed existing SEC requirements where the paper reported warnings
  (substantive; one additional field); and Fitzsimons Key Findings omitted the
  first-three-cycle qualification (precision; one additional field, found by
  parent sibling-field review despite SUPPORTED verdicts). These are three
  later clauses across two already-affected notes, adding two distinct fields,
  not three. All three clauses existed in the published baseline; the findings
  were not introduced by the first repair wave.

  | Stratum | Cumulative defective fields, all / substantive only | New distinct fields after first pass |
  |---|---|---:|
  | claude-opus-4-8 | 19/108 (17.6%) / 14/108 (13.0%) | 2 |
  | claude-opus-5 | 3/108 (2.8%) / 2/108 (1.9%) | 0 |
  | gpt-5.6-sol | 1/108 (0.9%) / 1/108 (0.9%) | 0 |
  | Residue (purposive) | 9/81 (11.1%) / 7/81 (8.6%) | 0 |

  | Stratum | Cumulative field family | Audited fields | Defects, all | Substantive only |
  |---|---|---:|---:|---:|
  | claude-opus-4-8 | Three v3 fields | 36 | 11 (30.6%) | 9 (25.0%) |
  | claude-opus-4-8 | Six legacy fields | 72 | 8 (11.1%) | 5 (6.9%) |
  | claude-opus-5 | Three v3 fields | 36 | 3 (8.3%) | 2 (5.6%) |
  | claude-opus-5 | Six legacy fields | 72 | 0 (0.0%) | 0 (0.0%) |
  | gpt-5.6-sol | Three v3 fields | 36 | 0 (0.0%) | 0 (0.0%) |
  | gpt-5.6-sol | Six legacy fields | 72 | 1 (1.4%) | 1 (1.4%) |
  | residue | Three v3 fields | 27 | 3 (11.1%) | 3 (11.1%) |
  | residue | Six legacy fields | 54 | 6 (11.1%) | 4 (7.4%) |

  Cumulative repairs cover 32 distinct fields in the same 20 notes: 24
  substantive and eight precision. The random-sample cumulative count is
  23/324 fields (7.1%), or 17/324 substantive fields (5.2%); affected-note
  counts remain 14/36 and 11/36 respectively. Repeat audit exposure was
  selective, so these cumulative counts must not replace the frozen first-pass
  comparison. DesJardine’s formula repeated in two fields counts as two field
  defects with one underlying formula error. The approved Trzebiatowski
  methods-frontmatter repeat is outside all nine-field denominators.

  All 45 first-pass official reports were assembled before the first repair
  wave; all 20 repair-round reports were assembled before the three later
  clauses were changed. Four mandatory stops were followed by explicit user
  continuation approvals. Six interrupted workers were restarted in fresh
  contexts without changing model or input. The final two full-note audits
  returned 17 SUPPORTED / 1 framing PARTIAL. Across all rounds there were 67
  completed full-note audits (603 field verdicts), using at most three workers
  at once.

  Final scoped state: 394 SUPPORTED / 11 accepted PARTIALs, zero UNSUPPORTED
  and zero CONTRADICTED. All 45 official reports and sidecars match current
  full-note and source hashes. Of the 32 repaired fields, 30 now score
  SUPPORTED; Kilduff and DesJardine Key Findings retain PARTIALs for different
  wording nuances, while their corrected results and clauses are supported.
  All relevant source passages were visible throughout; the fitter, source
  texts, extraction/augmentation prompts and historical stamps were unchanged.

  Of v0.68.0’s 11 earlier residue fields, three cleared unchanged (Xu Data &
  Measures and Future Research; Li Limitations), six were repaired and now
  score SUPPORTED (Chan Practical Implication; Dwertmann Mechanism Process and
  Theoretical Contribution; Hersel Data & Measures; Toivonen Practical
  Implication; Trzebiatowski Data & Measures), and two remain accepted
  (Lauriano Data & Measures and Hagtvedt Future Research). Fourteen other
  v0.68.0 PARTIAL fields were outside this authorized residue scope and retain
  their prior acceptances. Nine newly documented framing/paper-internal
  PARTIALs yield a current v0.69.0 AMJ inventory of 25 fields across 23 notes;
  the unchanged total masks this turnover. Both inventories are disclosed
  below.

  Era caveat: the claude-opus-4-8 stratum is backfill batches 01–07, before
  per-study attribution (batch 28), named-entity verification (batch 25) and
  the Limitations scope-boundary rule (batch 31). Stratum differences reflect
  pipeline maturity as well as auditor model and are not a causal model
  comparison. The era key is augmented_model when present, otherwise the
  native-v3 official auditor model; it does not identify the writer of every
  inherited legacy field. Twelve notes per stratum give imprecise rates;
  fields within notes are correlated. Equal allocation across unequal frames
  is not a corpus-weighted estimate, and the purposive residue set is not
  pooled with the random sample. The v0.68.0 comparison—four defects in 31
  notes (12.9%) and 279 fields (1.4%)—was a targeted input-loss sample, not an
  equivalent random control, and was not graded with this severity scheme.

  Recommendation: run a full second-opinion pass before NBS backfill,
  prioritizing batches 01–07 and their Data & Measures and Key Findings, then
  their legacy mechanism and implication fields. Next cover later-era
  measure/result attribution and legacy scope or prescription risks, including
  retained PARTIALs under current policy. Keep full-note audits to catch
  repeated premises across fields. Zero defects in a 12-note cell does not
  justify exempting that era or field family. This release does not start that
  full pass.

  Validation and publication checks: all 20 changed notes validate; SQLite,
  CSV and BibTeX were rebuilt sequentially and their ID sets reconcile with
  all 1,167 notes. BibTeX is byte-identical (no exported bibliographic field
  changed), and CSV retains CRLF. Scoped CrossRef was skipped because
  bibliographic frontmatter is unchanged; the only frontmatter exception is
  the explicitly approved nonbibliographic Trzebiatowski methods timing
  correction. Pytest is not applicable: no tool or test code changed. Census
  stays 61 v1 / 211 v2 / 895 v3, including all 895 AMJ notes at v3. NBS notes
  and the cleanup queue were untouched. All 1,167 stored official reports PASS
  with zero UNSUPPORTED/CONTRADICTED; this is evidence of review, not proof
  that undetected errors are absent. Legacy NBS reports lack hash provenance;
  the documented Wiedner note-only mismatch remains outside scope. Kim/Eggers
  full-raw-text exceptions remain superseded by v0.68.0; none was used here.

  **Every repaired published field (exact clauses; raw extracted-text line numbers):**

  | Published note / field | Severity; discovery | Before → after | Raw lines | Final field verdict |
  |---|---|---|---|---|
  | [amj-vol-68-no-1-desjardine-2024](notes/amj-vol-68-no-1-desjardine-2024.md), Mechanism Process | substantive; First pass | “- IV: Rival-MSCI common institutional ownership (rival-MSCI CIO) — the average product of an investor's ownership in MSCI and in the target firm's industry rivals, summed across common institutional owners with >=1% stakes.” → “- IV: Rival-MSCI common institutional ownership (rival-MSCI CIO) — for each rival-MSCI pair, multiply the summed ownership stakes that qualifying common institutional owners hold in the rival by their summed stakes in MSCI, then average these products across the target firm's industry rivals; qualifying owners hold >=1% in both firms.” | 445–487 | SUPPORTED |
  | [amj-vol-68-no-1-desjardine-2024](notes/amj-vol-68-no-1-desjardine-2024.md), Data & Measures | substantive; First pass | “computed via Equation 1 as the average product of an investor's ownership in MSCI and in the target firm's industry rivals, summed across institutional owners holding at least 1% of both MSCI and a rival (Thomson Reuters 13F Holdings)” → “computed via Equation 1 by summing qualifying common institutional owners' stakes in each rival and separately in MSCI, multiplying the two sums for each rival-MSCI pair, and averaging these products across the target firm's rivals; qualifying owners hold at least 1% of both MSCI and the rival (Thomson Reuters 13F Holdings)” | 445–487 | SUPPORTED |
  | [amj-vol-68-no-1-desjardine-2024](notes/amj-vol-68-no-1-desjardine-2024.md), Key Findings | substantive; First pass | “The main effect and moderators hold across Heckman selection, firm fixed effects, random effects, an alternative (IVA) industry classification, and the KLD and ASSET4 quasi-natural experiments (post-acquisition KLD-score effect b = -0.531, p < .10).” → “The negative main association persists in Heckman selection, firm fixed-effects, random-effects, and alternative (IVA) industry specifications, but moderator support varies: both controversy interactions are nonsignificant in the IVA tests, and several interactions lose significance when entered jointly. The KLD and ASSET4 acquisition analyses support the main relationship without testing the hypothesized reputational moderators (post-acquisition KLD-score coefficient b = -0.531, p < .10).” | 865–887; 1108–1135; 1171–1195; 1233–1255; 1407–1443; 1445–1495 | PARTIAL |
  | [amj-vol-67-no-5-kilduff-2024](notes/amj-vol-67-no-5-kilduff-2024.md), Key Findings | substantive; First pass | “alters successfully hid their ties from those who saw them as rivals.” → “alters successfully hid their ties from those they considered to be rivals.” | 197–204; 781–798 | PARTIAL |
  | [amj-vol-68-no-5-carnabuci-2025](notes/amj-vol-68-no-5-carnabuci-2025.md), Data & Measures | substantive; First pass | “derived from the share of a class’s patents that are cross-classified into other primary classes” → “computed as one minus the class-year mean of each patent’s fraction of subclasses assigned outside its primary class” | 334–354 | SUPPORTED |
  | [amj-vol-68-no-5-carnabuci-2025](notes/amj-vol-68-no-5-carnabuci-2025.md), Key Findings | substantive; First pass | “(Table 7, all six models)” → “(Table 7; five of six models are significant, but the full-sample prior-art-citation coefficient in Model 5 is not)”<br><br>“and class-year aggregation / GLS.” → “and GLS; class-year aggregation yields significance for CD3 and CD5 but not CD1.” | 739–775; 873–883<br><br>739–775; 873–883 | SUPPORTED |
  | [amj-vol-67-no-3-compagni-2023](notes/amj-vol-67-no-3-compagni-2023.md), Practical Implication | substantive; First pass | “Hospitals and other professional organizations should make space for, and legitimate, collegial cross-specialty collaboration and humanistic patient relations as central rather than ancillary practices, recognizing that they can generate positive moral feedback that helps professionals persist amid uncertainty.” → “Collegial cross-specialty collaboration and humanistic patient relations can become central rather than ancillary practices, generating positive moral feedback that helps professionals persist amid uncertainty.” | 1392–1406; 1412–1436 | SUPPORTED |
  | [amj-vol-67-no-4-rapp-2023](notes/amj-vol-67-no-4-rapp-2023.md), Data & Measures | precision; First pass | “independently coded each interview” → “independently coded the vast majority of interviews” | 244–249 | SUPPORTED |
  | [amj-vol-68-no-6-flynn-2025](notes/amj-vol-68-no-6-flynn-2025.md), Limitations | precision; First pass | “and the samples skewed female and White” → “and the Study 3 sample skewed female and White” | 865–882; 359–386; 549–550; 836–837 | SUPPORTED |
  | [amj-vol-68-no-2-fitzsimons-2024](notes/amj-vol-68-no-2-fitzsimons-2024.md), Mechanism Process | precision; First pass | “- Constraints that compel transition to next cycle: isolation, embattlement, alienation, and finally collapse.” → “- Constraints that compel transitions after the first three cycles: isolation, embattlement, and alienation; the fourth cycle ends in collapse.”<br><br>“Each social defense diffuses, deflects, or displaces anxiety while bolstering leaders' power, but creates a constraint that erodes its effectiveness, resurfacing anxiety and compelling the next cycle.” → “Social defenses diffuse, deflect, or displace anxiety while bolstering leaders' power; in the first three cycles, each creates a constraint that erodes its effectiveness, resurfacing anxiety and compelling the next cycle.” | 905–935; 1166–1175<br><br>905–935; 1166–1175 | SUPPORTED |
  | [amj-vol-68-no-2-fitzsimons-2024](notes/amj-vol-68-no-2-fitzsimons-2024.md), Practical Implication | precision; First pass | “condemning the change effort to fail” → “making failure of the change effort more likely” | 1183–1198 | SUPPORTED |
  | [amj-vol-68-no-2-fitzsimons-2024](notes/amj-vol-68-no-2-fitzsimons-2024.md), Data & Measures | substantive; First pass + repair round | “mostly using in vivo codes drawn from informants' language and tracking the ebb and flow of emotional codes (e.g., "performance anxiety") over time. Second, they developed more abstract codes,” → “mostly using in vivo codes drawn from informants' language. Second, they developed more abstract codes and tracked the ebb and flow of emotional codes (e.g., "performance anxiety") over time,”<br><br>“Throughout, they complemented the inductive coding” → “During the second stage, they complemented the inductive coding”<br><br>“760 hours of nonparticipant observation across 385 Leadership Team meetings, 231 project team meetings, and 144 Change Oversight Group meetings;” → “760 hours of nonparticipant observation across Leadership Team meetings (385 hours), project team meetings (231 hours), and Change Oversight Group meetings (144 hours);” | 377–406<br><br>377–406<br><br>251–269; 284–299; 306–315 | SUPPORTED |
  | [amj-vol-68-no-6-lee-2025](notes/amj-vol-68-no-6-lee-2025.md), Data & Measures | substantive; First pass | “reciprocation operationalized behaviorally as interpersonal citizenship behavior (Settoon & Mossholder, 2002) in Study 1 and as incentivized reward-, resource-, time-allocation, and recommendation decisions in Studies 2-3.” → “reciprocation measured through self-reported interpersonal citizenship behavior (Settoon & Mossholder, 2002) in Study 1, incentivized reward-allocation and recommendation decisions in Study 2, and simulated resource- and time-allocation decisions in Study 3.” | 542–554; 796–814; 974–1028 | SUPPORTED |
  | [amj-vol-66-no-6-xu-2023](notes/amj-vol-66-no-6-xu-2023.md), Key Findings | substantive; First pass | “- All three hypotheses received strong support, and results held across fixed-effect Poisson, multilevel modeling, 2SLS, five alternative embeddedness measures, and inflection-point sample splits.” → “- All three hypotheses received support in the main analyses, with checks using fixed-effect Poisson and multilevel modeling. The 2SLS and five alternative embeddedness-measure checks tested H1 only. In the inflection-point split, the below-peak slope was positive, but the above-peak negative slope was not significant (p = .655).” | 560–577; 718–737; 1323–1354; 1395–1427 | SUPPORTED |
  | [amj-vol-67-no-5-kilduff-2024](notes/amj-vol-67-no-5-kilduff-2024.md), Mechanism Process | substantive; First pass | “friendship tie between ego and alter (exploratory moderator that intensifies hiding and seeking effects)” → “friendship tie between ego and alter (exploratory moderator that strengthens seeking; the hiding interaction is marginal, p = .080)”<br><br>“the field study shows these processes operate in a real organization even after controlling for actual structural equivalence, common friendship ties, and direct knowledge-sharing ties.” → “the field study supports predicted relationships in a real organization after controlling for actual structural equivalence, common friendship ties, and direct knowledge-sharing ties, while capturing outcomes of both intentional and unintentional behavior and perception.” | 966–989; 1001–1005<br><br>966–989; 1001–1005 | SUPPORTED |
  | [amj-vol-67-no-5-kilduff-2024](notes/amj-vol-67-no-5-kilduff-2024.md), Future Research | substantive; First pass | “ using longitudinal observational designs” → [deleted] | 1068–1078 | SUPPORTED |
  | [amj-vol-68-no-5-gama-2025](notes/amj-vol-68-no-5-gama-2025.md), Key Findings | substantive; First pass | “Results hold across numerous robustness tests (alternative partnership coding, continuous scandal-intensity measures, alternative fixed-effects and estimation specifications, and sample restrictions).” → “Results generally hold across numerous robustness tests (alternative partnership coding, continuous scandal-intensity measures, alternative fixed-effects and estimation specifications, and sample restrictions), but the political-board-ties interaction becomes positive when industry and year effects replace firm effects (Model 17).” | 883–895 | SUPPORTED |
  | [amj-vol-65-no-3-tang-2022](notes/amj-vol-65-no-3-tang-2022.md), Data & Measures | precision; First pass | “with industriousness (α = .98), job autonomy (α = .88), job demands (α = .91), and tenure with intelligent machines as controls;” → “with tenure with intelligent machines as the primary control and industriousness (α = .98), job autonomy (α = .88), and job demands (α = .91) added in the Appendix K robustness model;” | 1000–1018; 1055–1065 | SUPPORTED |
  | [amj-vol-66-no-2-bianchi-2023](notes/amj-vol-66-no-2-bianchi-2023.md), Data & Measures | substantive; First pass | “obtained as restricted state-level data from the National Opinion Research Center and merged on state of current residence and survey year” → “merged on survey year and respondents’ state of current residence, with the latter obtained as restricted information from the National Opinion Research Center” | 237–247 | SUPPORTED |
  | [amj-vol-66-no-4-belinda-2023](notes/amj-vol-66-no-4-belinda-2023.md), Key Findings | substantive; First pass | “Study 1 (N = 119, standardized estimates):” → “Study 1 (N = 119, standardized direct paths; unstandardized bootstrapped indirect effects):”<br><br>“Study 2 (N = 63, standardized estimates):” → “Study 2 (N = 63, standardized direct paths; unstandardized bootstrapped indirect effects):” | 428–440; 747–764; 790–806<br><br>428–440; 747–764; 790–806 | SUPPORTED |
  | [amj-vol-60-no-6-powell-2017](notes/amj-vol-60-no-6-powell-2017.md), Limitations | substantive; First pass | “They also note that relationships between connected or separate enactments of community and specific structuring patterns may vary across venture contexts, institutional pressures, prior founder ties, paid work arrangements, and large organizing wins.” → “They also note that relationships between connected or separate enactments of community and specific structuring patterns may vary with venture context and institutional pressures; prior founder ties, paid work arrangements, and large organizing wins instead qualify patterns of continued engagement.” | 1540–1552; 1556–1594 | SUPPORTED |
  | [amj-vol-68-no-1-trzebiatowski-2024](notes/amj-vol-68-no-1-trzebiatowski-2024.md), Data & Measures | substantive; First pass | “DVs = one-year-ahead turnover rate of women and racialized non-leaders (associates) and leaders (partners), each the count who departed during a year divided by the count at that year's start.” → “DVs = annual turnover rate of women and racialized non-leaders (associates) and leaders (partners), each the count who departed during a year divided by the count at that year's start; turnover during a given year was reported in the following year's survey and linked to diversity practices reported in April–May of the turnover year.” | 446–456; 469–472 | SUPPORTED |
  | [amj-vol-66-no-1-chan-2023](notes/amj-vol-66-no-1-chan-2023.md), Practical Implication | substantive; First pass | “For professionals whose clients have grown more powerful (career advisers, lawyers, physicians, therapists, consultants), the study suggests cultivating diagnostic skill at reading client values and a repertoire of variably visible value-enactment practices, rather than committing wholesale to either accommodation or resistance.” → “The study shows how career advisers read client values and use a repertoire of variably visible value-enactment practices, rather than committing wholesale to either accommodation or resistance.”<br><br>“Occupational training that emphasizes relational skills and a service-oriented disposition toward heterogeneous clients can help experts protect their jurisdiction without surrendering their professional purpose.” → “The authors suggest these mechanisms may be more likely in occupations where socialization emphasizes relational skills and a collaborative or service-oriented regard for clients.” | 1318–1343; 1179–1185<br><br>1318–1343; 1179–1185 | SUPPORTED |
  | [amj-vol-66-no-1-chan-2023](notes/amj-vol-66-no-1-chan-2023.md), Key Findings | substantive; First pass | “Negative cases establish the same relationship in the opposite direction. When advisers failed to discern accurately and applied value-magnifying practices to students committed to popular careers, students reacted negatively: they refused to return for advice, circulated negative sentiment about advisers among peers, and left negative appointment feedback and low satisfaction ratings that reached bosses and deans, any of which could undercut advisers' legitimate and autonomous hold over their tasks.” → “Negative cases suggest the corresponding risk. When advisers failed to discern accurately and applied value-magnifying practices to students committed to popular careers, students reported negative experiences. Observed and prospective reactions included not returning for advice, discouraging peers from seeking it, and negative appointment feedback; the authors explain that low satisfaction ratings sent to advisers' bosses could undercut advisers' legitimate and autonomous hold over their tasks.” | 1146–1188 | SUPPORTED |
  | [amj-vol-66-no-1-dwertmann-2023](notes/amj-vol-66-no-1-dwertmann-2023.md), Mechanism Process | precision; First pass | “- Mediators: CSR perceptions; competence stereotypes; disability–job fit stereotypes” → “- Mediators: CSR perceptions; competence stereotypes; warmth stereotypes (hypothesized); disability–job fit stereotypes” | 414–431 | SUPPORTED |
  | [amj-vol-66-no-1-dwertmann-2023](notes/amj-vol-66-no-1-dwertmann-2023.md), Theoretical Contribution | substantive; First pass | “determines whether disability-inclusive hiring is interpreted as reputational asset or liability” → “conditions whether disability-inclusive hiring yields a significant positive CSR signal: the benefit is not significant at high egoistic or low sincere motive attributions” | 994–1016 | SUPPORTED |
  | [amj-vol-66-no-2-hersel-2023](notes/amj-vol-66-no-2-hersel-2023.md), Data & Measures | substantive; First pass | “a PRI consistency threshold of 0.70” → “PRI consistency thresholds of 0.70 for favorable reactions and 0.80 for unfavorable reactions” | 338–344; 370–389 | SUPPORTED |
  | [amj-vol-66-no-3-toivonen-2023](notes/amj-vol-66-no-3-toivonen-2023.md), Practical Implication | substantive; First pass | “Autonomous creators and the mentors, accelerators, and coworking communities supporting them should recognize that highly critical, core-directed feedback can trigger an agonizing but generative period rather than mere failure.” → “The study shows that, for autonomous creators, highly critical, core-directed feedback can trigger an agonizing but generative period rather than mere failure.”<br><br>“Supporting creators through the emotional upheaval—via opportunities to reach out to diverse networks and reach in to core values—can help them work through the process of letting go,” → “Creators reappraised their ideas through reaching out to diverse networks or reaching in to core values as they worked through letting go,” | 1313–1345<br><br>1313–1345 | SUPPORTED |
  | [amj-vol-68-no-1-hagtvedt-2024](notes/amj-vol-68-no-1-hagtvedt-2024.md), Mechanism Process | substantive; First pass | “mutually reinforcing” → “potentially self-reinforcing” | 1185–1241; 1350–1353 | SUPPORTED |
  | [amj-vol-68-no-1-trzebiatowski-2024](notes/amj-vol-68-no-1-trzebiatowski-2024.md), Practical Implication | precision; First pass | “organizations must avoid mixed safeguarding signals and pair resource practices with both high non-discrimination and high accountability;” → “organizations must avoid mixed safeguarding signals; the ideal configuration pairs resource practices with both high non-discrimination and high accountability;” | 1090–1111; 1112–1137 | SUPPORTED |
  | [amj-vol-68-no-1-desjardine-2024](notes/amj-vol-68-no-1-desjardine-2024.md), Practical Implication | substantive; Repair round | “requirements of the kind the SEC applies to rating-agency conflicts.” → “requirements, in light of the SEC's warnings about inadequate disclosure and internal controls.” | 323–330; 1705–1723 | SUPPORTED |
  | [amj-vol-68-no-2-fitzsimons-2024](notes/amj-vol-68-no-2-fitzsimons-2024.md), Key Findings | precision; Repair round | “, which in turn creates a constraint that resurfaces anxiety and compels the next cycle.” → “; in the first three cycles, this produces a constraint that resurfaces anxiety and compels the next cycle.” | 905–935; 1166–1175 | SUPPORTED |
  | [amj-vol-68-no-1-trzebiatowski-2024](notes/amj-vol-68-no-1-trzebiatowski-2024.md), Methods frontmatter | substantive; First pass; explicit frontmatter exception | “and predicting one-year-ahead turnover rates of women and racialized associates (non-leaders) and partners (leaders);” → “and predicting turnover rates of women and racialized associates (non-leaders) and partners (leaders) for the year of the practice measures, using turnover reported in the following year's survey;” | 446–456; 469–472 | Validated; Data & Measures SUPPORTED |

  **Disposition of all 25 v0.68.0 accepted PARTIAL fields:**

  | Note | Field | v0.69.0 disposition |
  |---|---|---|
  | [amj-vol-61-no-5-deken-2018](notes/amj-vol-61-no-5-deken-2018.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-62-no-2-sherf-2019](notes/amj-vol-62-no-2-sherf-2019.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-62-no-4-nigam-2019](notes/amj-vol-62-no-4-nigam-2019.md) | Practical Implication | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-62-no-4-simsek-2019](notes/amj-vol-62-no-4-simsek-2019.md) | Limitations | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-62-no-5-lin-2019](notes/amj-vol-62-no-5-lin-2019.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-64-no-6-wang-2021](notes/amj-vol-64-no-6-wang-2021.md) | Limitations | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-64-no-6-wang-2021](notes/amj-vol-64-no-6-wang-2021.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-1-dushnitsky-2022](notes/amj-vol-65-no-1-dushnitsky-2022.md) | Key Findings | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-3-fang-2022](notes/amj-vol-65-no-3-fang-2022.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-4-ferns-2022](notes/amj-vol-65-no-4-ferns-2022.md) | Practical Implication | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-4-lazar-2022](notes/amj-vol-65-no-4-lazar-2022.md) | Data & Measures | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-5-koppman-2022](notes/amj-vol-65-no-5-koppman-2022.md) | Limitations | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-5-matusik-2022](notes/amj-vol-65-no-5-matusik-2022.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-5-williams-2022](notes/amj-vol-65-no-5-williams-2022.md) | Future Research | Prior acceptance retained; outside this re-audit scope |
  | [amj-vol-65-no-6-xu-2022](notes/amj-vol-65-no-6-xu-2022.md) | Data & Measures | Cleared unchanged: SUPPORTED |
  | [amj-vol-65-no-6-xu-2022](notes/amj-vol-65-no-6-xu-2022.md) | Future Research | Cleared unchanged: SUPPORTED |
  | [amj-vol-66-no-1-chan-2023](notes/amj-vol-66-no-1-chan-2023.md) | Practical Implication | Repaired: SUPPORTED |
  | [amj-vol-66-no-1-dwertmann-2023](notes/amj-vol-66-no-1-dwertmann-2023.md) | Mechanism Process | Repaired: SUPPORTED |
  | [amj-vol-66-no-1-dwertmann-2023](notes/amj-vol-66-no-1-dwertmann-2023.md) | Theoretical Contribution | Repaired: SUPPORTED |
  | [amj-vol-66-no-1-lauriano-2023](notes/amj-vol-66-no-1-lauriano-2023.md) | Data & Measures | Remains accepted PARTIAL |
  | [amj-vol-66-no-2-hersel-2023](notes/amj-vol-66-no-2-hersel-2023.md) | Data & Measures | Repaired: SUPPORTED |
  | [amj-vol-66-no-3-toivonen-2023](notes/amj-vol-66-no-3-toivonen-2023.md) | Practical Implication | Repaired: SUPPORTED |
  | [amj-vol-68-no-1-hagtvedt-2024](notes/amj-vol-68-no-1-hagtvedt-2024.md) | Future Research | Remains accepted PARTIAL |
  | [amj-vol-68-no-1-trzebiatowski-2024](notes/amj-vol-68-no-1-trzebiatowski-2024.md) | Data & Measures | Repaired: SUPPORTED |
  | [amj-vol-68-no-4-li-2025](notes/amj-vol-68-no-4-li-2025.md) | Limitations | Cleared unchanged: SUPPORTED |

  **Current v0.69.0 remaining accepted PARTIALs: 25 fields across 23 notes.**

  | Note | Field | Acceptance basis |
  |---|---|---|
  | [amj-vol-59-no-6-heese-2016](notes/amj-vol-59-no-6-heese-2016.md) | Practical Implication | The paper explicitly proposes the three interventions. The note says “may require,” not that they necessarily work or produce a lasting solution. Omitting the separate social-norm discussion is compression rather than a false effectiveness claim. |
  | [amj-vol-61-no-5-deken-2018](notes/amj-vol-61-no-5-deken-2018.md) | Future Research | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-62-no-2-sherf-2019](notes/amj-vol-62-no-2-sherf-2019.md) | Future Research | Framing; source visible; not re-audited in this scope. |
  | [amj-vol-62-no-4-nigam-2019](notes/amj-vol-62-no-4-nigam-2019.md) | Practical Implication | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-62-no-4-simsek-2019](notes/amj-vol-62-no-4-simsek-2019.md) | Limitations | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-62-no-5-lin-2019](notes/amj-vol-62-no-5-lin-2019.md) | Future Research | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-64-no-6-wang-2021](notes/amj-vol-64-no-6-wang-2021.md) | Limitations | Framing/locality; raw-text adjudication; not re-audited in this scope. |
  | [amj-vol-64-no-6-wang-2021](notes/amj-vol-64-no-6-wang-2021.md) | Future Research | Framing/locality; raw-text adjudication; not re-audited in this scope. |
  | [amj-vol-65-no-1-dushnitsky-2022](notes/amj-vol-65-no-1-dushnitsky-2022.md) | Key Findings | Paper-internal inconsistency; not re-audited in this scope. |
  | [amj-vol-65-no-2-foy-2022](notes/amj-vol-65-no-2-foy-2022.md) | Mechanism Process | The paragraph compresses the central theorized pattern rather than claiming an exhaustive case census. The same field identifies six venture types and low-to-high tension, and Key Findings explicitly reports the three low-tension outliers. Aligned founders’ adoption of sociopolitical best practices does not contradict their avoidance of challenging the sociocultural status quo. |
  | [amj-vol-65-no-3-fang-2022](notes/amj-vol-65-no-3-fang-2022.md) | Future Research | Framing; source visible; not re-audited in this scope. |
  | [amj-vol-65-no-4-ferns-2022](notes/amj-vol-65-no-4-ferns-2022.md) | Practical Implication | Framing; source visible; not re-audited in this scope. |
  | [amj-vol-65-no-4-lazar-2022](notes/amj-vol-65-no-4-lazar-2022.md) | Data & Measures | Paper-internal inconsistency; not re-audited in this scope. |
  | [amj-vol-65-no-5-koppman-2022](notes/amj-vol-65-no-5-koppman-2022.md) | Limitations | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-65-no-5-matusik-2022](notes/amj-vol-65-no-5-matusik-2022.md) | Future Research | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-65-no-5-williams-2022](notes/amj-vol-65-no-5-williams-2022.md) | Future Research | Prior non-tooling acceptance; not re-audited in this scope. |
  | [amj-vol-66-no-1-chan-2023](notes/amj-vol-66-no-1-chan-2023.md) | Limitations | The source calls both features boundary conditions, says lengthy interactions may be required and relational socialization makes the mechanisms more likely, and concludes Within these two boundary conditions. The unchanged note uses the hedged likely require and explicitly attributes these two boundaries. It adds no unnamed generalizability target or unsupported practitioner prescription. The compression is somewhat stronger but remains a tentative rendering of the stated boundaries, rather than a categorical necessity claim. |
  | [amj-vol-66-no-1-lauriano-2023](notes/amj-vol-66-no-1-lauriano-2023.md) | Practical Implication | All three recommendations and their audiences are explicitly present. The note makes no claim that the policies necessarily remove stigma or cannot reproduce hetero/cisnormativity. Omission of the additional caution is a nuance/compression PARTIAL, not an invented intervention or false effectiveness claim. |
  | [amj-vol-66-no-1-lauriano-2023](notes/amj-vol-66-no-1-lauriano-2023.md) | Data & Measures | The Methods explicitly says each interview lasted 60–120 minutes, whereas Table A1 lists one 50-minute interview. The note follows the paper’s prose. Figure 1 includes shadowing in the 480-hour total, but the note’s “additionally” introduces a method and does not assert 496 total hours; Methods likewise introduces it with “Furthermore.” |
  | [amj-vol-67-no-3-compagni-2023](notes/amj-vol-67-no-3-compagni-2023.md) | Limitations | The explicit retrospective-interview limitation is faithfully retained. “Possibility of hindsight bias” is a modest, clearly tentative methodological inference, not an invented generalizability target; the paper’s countervailing reflective benefit remains in the same sentence. |
  | [amj-vol-67-no-4-rapp-2023](notes/amj-vol-67-no-4-rapp-2023.md) | Future Research | The complete paragraph on hero-washing transferability explicitly names neurodiverse workers as an example of mixed social evaluations (raw lines 1450–1496, continuing at the top of the right column). Grouping these named extensions is minor framing/compression, not an invented target. The preliminary candidate is preserved but not selected, consistently with approved proposal 04. |
  | [amj-vol-67-no-5-kilduff-2024](notes/amj-vol-67-no-5-kilduff-2024.md) | Key Findings | The repaired rivalry direction is supported. Detailed numerical results, outcome labels and directions are correct. The remaining final-summary shorthand is read in that explicit context; the paper itself labels the boundary p=.050 differently in its table and prose. Do not edit accurate detailed results to satisfy this wording residue. |
  | [amj-vol-68-no-1-desjardine-2024](notes/amj-vol-68-no-1-desjardine-2024.md) | Key Findings | Objective is a stronger shorthand than the paper's reasonable benchmarks. The same clause explicitly identifies ESG risk incidents and ASSET4 evaluations, gives the correct gap coefficients and null benchmark associations, and limits the conclusion to consistent with a rating-bias interpretation. No measure, number, sign or result is misstated by this remaining adjective. After three full audits, retain this subjective wording residue under the convergence rule; disclose that objective is analyst framing, not a source-established guarantee of unbiased measurement. |
  | [amj-vol-68-no-1-hagtvedt-2024](notes/amj-vol-68-no-1-hagtvedt-2024.md) | Future Research | Collective dynamics are an explicitly named unexamined process, and shifting/blended imagining pathways are within the paper’s model. The tentative “could” agenda extends that named process modestly; it does not invent an external generalizability target. |
  | [amj-vol-68-no-4-li-2025](notes/amj-vol-68-no-4-li-2025.md) | Data & Measures | 507 newcomers follows the introduction; 509 appears in Methods and the promotion counts, an internal source discrepancy. The note assigns random intercepts only to performance/mediator regressions, calls promotion a repeated-events Cox model, and does not claim that promotion bootstrapping retained random intercepts. The alternative-model detail is omitted rather than contradicted. |

  Process deviations and exceptions: the four stop/resume approvals and six
  fresh-context restarts are preserved verbatim in the private evidence; the
  only protected-field exception was Trzebiatowski methods. A Lee restart
  dispatch contained one extra character in the operational note hash,
  corrected before return; the verified sidecar has the exact current hash and
  its analytical input never changed. Hayward’s initial first-pass dispatch
  included a path typo corrected in the same dispatch. No sample redraw, model
  substitution, raw-text audit, fitter/prompt change, NBS work or cleanup-
  queue change occurred. The README’s former absolute assurance about error-
  free publication is narrowed to the verified limits of audit evidence.
  Private prompts, raw returns, ledgers and sidecars remain untracked, PDF-
  free and below the 5 MB per-file archive guard.

- **v0.68.0 audit fitter repair and standard-input re-audit (2026-09-11, 1,167 notes):**
  The reference cut now preserves body prose interleaved with a right-column
  bibliography, advancing to a repeated left-column author/year transition
  and falling back to the old heading cut if no transition is found. A
  user-approved exception retains a positively identified terminal prose
  band only when the complete text fits the existing budget. Right-column
  and titled uppercase appendix headings are recognized, and the approved
  appendix cap is **60,000 characters**. Source text files are unchanged.

  Two byte-identical sweeps of all **1,167 texts** found **528 same, 88
  improved, 1 changed-otherwise, and 550 no-match**. The one other change
  adds only a reference heading and whitespace. Every source interval
  retained by the old fitter remains present: **zero regressions**, no new
  sandwich-truncated paper, and no appendix truncation. All **14 victim
  papers / 28 literal probes** and all **42 scoped field-restoration proofs**
  pass. The largest fitted source is 246,024 characters; this includes the
  existing anchor-splice allowance, not an enlarged base budget. The 15%
  strip-ratio caution remains unchanged. Tests: **51 passed**.

  Fresh blind `gpt-6-astra` audits covered **31 notes / 279 fields** under
  standard fitted input. The baseline was 239 SUPPORTED / 40 PARTIAL;
  first pass returned 273 SUPPORTED / 5 PARTIAL / 1 CONTRADICTED. All
  first-pass official reports were assembled before repairs. With explicit
  user authorization, four previously published fields were corrected:
  Kotha (2018) reversed who pays licensing fees; Foulk (2018) reversed the
  direction of accountability feedback; Shea (2019) omitted the
  feedback-task-first qualification on Study 3 comparisons; Fang (2022)
  omitted parental controls from the baseline-model description. These
  passages were already visible to the old fitter. Fresh full-note audits
  after repair returned 35 SUPPORTED / 1 framing PARTIAL across 36 fields.

  Final scoped state: **276 SUPPORTED / 3 accepted framing PARTIALs,
  0 UNSUPPORTED, 0 CONTRADICTED**. **39 of 40** previously accepted
  text-loss fields are now SUPPORTED. Fang's Future Research remains PARTIAL
  for a different reason: examples drawn from the controls discussion
  extend the explicit future agenda; the supporting source is visible.
  The other framing PARTIALs concern Sherf's Future Research example of
  objective field performance and Ferns's more definite explanation of
  Occupy's relative failure. Their wording is unchanged. Kim and Eggers
  each pass **9/9 under standard fitted input**, superseding both historical
  full-raw-text audit exceptions; the original exception evidence is kept.

  At v0.68.0 publication, official reports were **1,167/1,167 PASS**, with zero
  UNSUPPORTED or CONTRADICTED. AMJ has 25 accepted PARTIAL fields across
  22 notes: the three above, 11 non-tooling fields retained without fresh
  audit, and 11 earlier-batch fields outside this session's scope. See
  [AGENTS §5](AGENTS.md#5-faithfulness-guarantees) for the complete list and
  the limits of audit assurance. No NBS notes or cleanup-queue entries
  changed. All 31 scoped notes validate with matching audit hashes;
  bibliographic frontmatter, historical provenance and anchors are
  unchanged. SQLite, parsed CSV and BibTeX reconcile to **1,167**; CSV
  changes exactly four fields and BibTeX is byte-identical. Scoped CrossRef
  was skipped because bibliographic fields did not change. The v0.68.0
  census remains **61 v1 / 211 v2 / 895 v3**. The runbook now requires
  fail-safe fitter changes, real-layout fixtures and repeated containment
  checks before publication.

- **v0.67.0 v3 backfill batch 34 — AMJ v3 backfill complete (2026-09-10, 1,167 notes):**
  Upgrades the final **13 existing v2 notes from AMJ volume 58 issue 1** to
  v3. No new notes, v1 re-extractions, already-v3 skips, calibration
  repairs, or paper-type changes were needed. The total remains **1,167**,
  and the census shifts from 61 v1 / 224 v2 / 882 v3 to **61 v1 / 211 v2 /
  895 v3**.

  This release completes the AMJ v3 backfill: all 895 AMJ notes across 70
  total issues are now v3. The completed backfill covers 67 issues from
  volume 58 issue 1 through volume 69 issue 1; three earlier volume 57
  issues were already native v3. The only remaining v1/v2 notes are the 272
  NBS notes (61 v1 and 211 v2).

  First-pass blind nine-field audits returned **115 SUPPORTED and 2 PARTIAL
  out of 117**, with no UNSUPPORTED or CONTRADICTED. All 13 official reports
  were assembled with current hashes before any repair. Parent source
  verification produced **10 legacy-field repairs across 9 notes**,
  including **8 fields initially scored SUPPORTED**. The repairs correct
  practical and future-research scope, distinguish predictor groups from
  moderators, remove invented limitations, and clarify planned rather than
  observed job return.

  Every repaired note received a fresh blind full-note audit; the nine
  re-audits returned **81/81 SUPPORTED**. The final state is **117/117
  SUPPORTED**, including all 39 new v3 fields, with **0 PARTIAL, 0
  UNSUPPORTED, and 0 CONTRADICTED**. No faithful-PARTIAL acceptance or
  full-raw-text audit exception was needed. All 13 current official
  report/sidecar pairs match the final note and source hashes; all 22 audit
  returns, prompts, and preserved report/sidecar pairs reconcile.

  All 13 notes validate. The augmentation guard passed before repairs and
  now flags exactly the 10 registered legacy fields. Bibliographic YAML
  bytes, historical extraction provenance, original evidence, and paper
  types are unchanged; the new v3 sections and anchors are unchanged during
  repairs. Augmentation provenance records `gpt-6-astra` and 2026-09-10.
  Scoped CrossRef was skipped only after field-by-field proof of
  byte-identical bibliographic frontmatter.

  Sequential SQLite, parsed CSV, and BibTeX rebuilds reconcile to **1,167
  records** with identical record IDs and **byte-identical BibTeX**.
  Full-library validation passed **1,167/1,167**; direct regressions passed
  **22/22** for PDF-text fitting and **15/15** for augmentation. All 13
  writers and 22 auditors have verified `gpt-6-astra` runtime metadata.

  This is the **fifth batch run end-to-end on `gpt-6-astra` (GPT-6 Astra)**.
  Provenance eras are batches 01–07 `claude-opus-4-8`, 08–15
  `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23 `claude-opus-5`, 24–29
  `gpt-5.6-sol`, and 30–34 `gpt-6-astra`. Cross-family calibration scored
  27/27 for batch 16, 27/27 for batch 24, 25/27 for batch 28 (both
  divergences repaired in v0.62.0), 26/27 for batch 30 (the divergence
  adjudicated faithful), and 26/27 for batch 32 (the divergence explained by
  a documented input-mode difference). Batch 34’s workshop review is
  scheduled to run the closing cross-family spot-audit, including a
  pre-repair probe. The original augmented notes and exact first-pass
  prompts are preserved; that review has not yet been performed.

- **v0.66.0 v3 backfill batch 33 (2026-09-07, 1,167 notes):**
  Upgrades **AMJ volume 58 issues 3 and 2, 13 notes each**, from v2 to v3.
  No new notes, v1 re-extractions, already-v3 skips, or calibration
  repairs were needed. The record total remains **1,167**; the census
  shifts from 61 v1 / 250 v2 / 856 v3 to **61 v1 / 224 v2 / 882 v3**.
  Paper types are unchanged.

  All 26 notes validate. All augmentation guards passed before legacy
  repairs; final guard differences match exactly the **15 registered
  legacy fields across 12 notes**. Bibliographic frontmatter, historical
  extraction provenance, and original evidence remain unchanged. The three
  new v3 sections and their anchors are unchanged during repairs;
  augmentation provenance records `gpt-6-astra` and 2026-09-07.

  First-pass blind nine-field audits returned **226 SUPPORTED and 8
  PARTIAL out of 234**, with no UNSUPPORTED or CONTRADICTED. All 26
  first-pass official reports were assembled before any repair. Parent
  source verification produced 15 legacy-field repairs, including **11
  fields initially scored SUPPORTED**, narrowing unsupported practical,
  limitations, and future-research scope, correcting the stage of
  moderation, and qualifying marginal evidence. Every changed note
  received a fresh blind full-note audit; the 12 re-audits returned
  **108/108 SUPPORTED**.

  The **final state is 230 SUPPORTED and 4 accepted PARTIALs out of 234**,
  with **0 UNSUPPORTED and 0 CONTRADICTED**. All 26 notes pass overall
  with matching current full-note and source hashes. Of the 78 new v3
  fields, 77 are SUPPORTED and one is an accepted PARTIAL. All 38 audit
  returns reconcile with their preserved official reports and sidecars; 26
  current official report/sidecar pairs match the final notes.

  The four retained PARTIALs are faithful claims whose supporting passages
  were omitted from fitted audit input: Di Stefano Limitations (14.43%
  strip), Reyt Data & Measures (18.85%, Appendix 1 validation sample and
  discriminant validity), and Zhang Practical Implication and Limitations
  (19.61%, explicit training guidance and sample/common-method
  qualifications). Each acceptance records raw-presence/fitted-absence
  reconstruction and a subsequent reading of the complete recovered
  passage. No faithful text was removed, and no full-raw-text audit
  exception was needed.

  Scoped CrossRef was skipped only after field-by-field proof of
  byte-identical bibliographic YAML. Sequential SQLite, parsed CSV, and
  BibTeX rebuilds reconcile to **1,167 records**, with **byte-identical
  BibTeX**. Full-library validation passed **1,167/1,167**; direct
  regressions passed **22/22** for PDF-text fitting and **15/15** for
  augmentation. All 26 writers and 38 auditors have verified `gpt-6-astra`
  runtime metadata.

  This is the **fourth batch run end-to-end on `gpt-6-astra` (GPT-6
  Astra)**. Provenance eras are batches 01–07 `claude-opus-4-8`, 08–15
  `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23 `claude-opus-5`, 24–29
  `gpt-5.6-sol`, and 30–33 `gpt-6-astra`. Cross-family calibration scored
  **27/27** for batch 16, **27/27** for batch 24, **25/27** for batch 28
  (both divergences repaired in v0.62.0), **26/27** for batch 30 (the
  divergence adjudicated faithful), and **26/27** for batch 32 (the
  divergence explained by a documented input-mode difference). **No
  spot-audit is scheduled for this batch’s review**; final calibration is
  expected at batch 34’s workshop review.

- **v0.65.0 v3 backfill batch 32 (2026-09-07, 1,167 notes):**
  Upgrades **AMJ volume 58 issues 5 and 4, 13 notes each**, from v2 to v3,
  and repairs only Limitations in three already-v3 notes: Shani (2016),
  Ayyagari (2015), and Graffin (2016), following the workshop's batch-31
  review. These calibration repairs remove generalizability targets the
  papers do not state while preserving their design facts and acknowledged
  limitations. The record total remains **1,167**; the census shifts from
  61 v1 / 276 v2 / 830 v3 to **61 v1 / 250 v2 / 856 v3**.

  All 29 touched notes validate. All 26 augmentation guards passed before
  legacy repairs; final guard differences match the 21 registered legacy
  fields across 14 target notes. The three calibration notes independently
  pass Limitations-only and unchanged-frontmatter checks. Bibliographic
  frontmatter and historical provenance remain unchanged; augmentation
  provenance truthfully records `gpt-6-astra` and 2026-09-07.

  First-pass blind nine-field audits returned **251 SUPPORTED, 9 PARTIAL,
  and 1 UNSUPPORTED** out of 261 judgments. All first-pass official reports
  were assembled before audit-driven repairs. Parent raw-source review
  produced **21 further legacy-field repairs across 14 notes**, including
  **12 fields initially scored SUPPORTED**, correcting directional wording,
  variable roles, theoretical versus empirical support, and unsupported
  practical, limitations, and future-research scope. Every repaired note
  received a fresh blind full-note audit. Together with the three assigned
  calibration repairs, this release repairs 24 legacy fields across 17 notes.

  The **final state is 260 SUPPORTED and 1 accepted PARTIAL out of 261**,
  with **0 UNSUPPORTED and 0 CONTRADICTED**. All 29 notes pass overall with
  current note and source hashes. All 78 newly added fields and the nine
  existing v3 fields in the calibration notes are SUPPORTED. Shani and
  Ayyagari returned 9/9 SUPPORTED. Graffin returned 8 SUPPORTED and 1
  accepted PARTIAL: its Limitations sentence about an inexpensive,
  effective tactic and unexplained non-use is explicit in raw text but
  absent from fitted input at 14.15% strip. Reconstruction proof and
  subsequent reading confirm fidelity; the sentence remains unchanged.

  Kim's legacy Future Research field received UNSUPPORTED in two standard
  audits because the fitter omitted the explicitly stated aspirations and
  expectations agenda at 13.88% strip. With explicit per-note user approval,
  a fresh blind auditor received the complete raw source and returned
  **9/9 SUPPORTED**. The official report was assembled with the audit tool's
  own functions, with the input mode, prompt hash, and authorization in both
  provenance and audit context, alongside the standard fitting diagnostic.
  Both original verdicts remain preserved; no faithful note text, tool, or
  workflow document changed for this exception.

  Scoped CrossRef was skipped after field-by-field proof of byte-identical
  bibliographic frontmatter. Sequential SQLite, parsed CSV, and BibTeX
  rebuilds reconcile to **1,167 records**, with unchanged paper types and
  byte-identical BibTeX. Full-library validation passed **1,167/1,167**;
  direct regressions passed **22/22** for PDF-text fitting and **15/15** for
  augmentation. All 44 independent audit returns and preserved official
  reports reconcile, with 29 current official report/sidecar pairs.

  This is the **third batch run end-to-end on `gpt-6-astra` (GPT-6 Astra)**
  for augmentation and audit. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, 24–29 `gpt-5.6-sol`, and 30–32 `gpt-6-astra`.
  Cross-family calibration scored **27/27** for batch 16, **27/27** for
  batch 24, **25/27** for batch 28 (both divergences repaired in v0.62.0),
  and **26/27** for batch 30 (the divergence adjudicated faithful).
  The next cross-family spot-audit runs at **this batch's workshop review**,
  including a **pre-repair probe on preserved baseline prompts**; its result
  is pending. The three batch-31 Limitations repairs described above ride
  in this release following that workshop's review.

- **v0.64.0 v3 backfill batch 31 (2026-09-06, 1,167 notes):**
  Upgrades **AMJ volume 59 issue 1 and volume 58 issue 6, 29 notes total**
  to v3, all through v2 augmentation. The record total remains **1,167**;
  the census shifts from 61 v1 / 305 v2 / 801 v3 to **61 v1 / 276 v2 /
  830 v3**. All 29 notes validate. The initial augmentation guard passed
  all 29; the final guard passes 12 and flags exactly the registered legacy
  sections repaired in 17 notes. Protected frontmatter, historical extraction
  provenance, and the three new v3 sections are unchanged during repairs.

  First-pass blind 9-field audits returned **249 SUPPORTED, 11 PARTIAL,
  and 1 UNSUPPORTED** out of 261 judgments. Parent source review produced
  **24 legacy-field repairs across 17 notes**, including **17 fields
  initially scored SUPPORTED**. Repairs correct variable roles, theoretical
  versus empirical support, and unsupported practical or future-research
  scope. Every repaired note received a fresh blind full-note audit; all
  24 repaired fields are now SUPPORTED. The **final state is 257 SUPPORTED
  and 4 accepted PARTIALs out of 261**, with **0 UNSUPPORTED and 0
  CONTRADICTED**. All 29 notes pass overall with current note and source
  hashes. Graffin's Limitations and Lanzolla's Future Research retain
  faithful claims whose supporting passages are absent from fitted audit
  inputs. Shani's and Ayyagari's Limitations retain source-grounded sample
  scope qualifications after two-round framing disagreements at 0% strip.
  All four acceptances have reconstruction proofs and subsequent source
  readings in the private ledger.

  Eggers's Data & Measures received UNSUPPORTED in two standard audits
  because fitting removed three appendix methods facts at a 12% strip
  ratio. With explicit user approval, a fresh blind auditor received the
  complete raw source and returned **9/9 SUPPORTED**. The official report
  was assembled with the audit tool's functions and explicit unabridged-input
  provenance; the original verdicts remain preserved. The faithful note,
  tools, and workflow documents were unchanged by this exception.

  Bibliographic frontmatter is byte-identical to the HEAD baseline, so
  scoped CrossRef was skipped. Sequential SQLite, CSV, and BibTeX rebuilds
  reconcile to **1,167 records**, with unchanged paper types and byte-identical
  BibTeX. Full-library validation passed **1,167/1,167**; direct regressions
  passed **22/22** for PDF-text fitting and **15/15** for augmentation.

  This is the **second batch run end-to-end on `gpt-6-astra` (GPT-6 Astra)**
  for augmentation and audit. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, 24–29 `gpt-5.6-sol`, and 30–31 `gpt-6-astra`.
  Cross-family calibration scored **27/27** for batch 16, **27/27** for
  batch 24, **25/27** for batch 28 (both divergences repaired in v0.62.0),
  and **26/27** for batch 30 (the divergence adjudicated faithful under
  strip blindness). No spot-audit is scheduled for this batch's review;
  the next calibration runs at **batch 32's workshop review**.

- **v0.63.0 v3 backfill batch 30 (2026-09-05, 1,167 notes):**
  Upgrades **AMJ volume 59 issues 3 and 2, 31 notes total** to the v3
  schema, all through v2 augmentation. The record total remains **1,167**;
  the corpus shifts from 61 v1 / 336 v2 / 770 v3 to **61 v1 / 305 v2 / 801
  v3**. All 31 notes validate. The initial augmentation guard passed all 31;
  the final guard passes 16 and flags exactly the 18 documented legacy-field
  repairs across 15 notes. All three new sections, augmentation provenance,
  and protected frontmatter remain unchanged during those repairs.

  The first full blind 9-field rubric-v2 audit returned **268 SUPPORTED, 10
  PARTIAL, and 1 UNSUPPORTED** out of 279 verdicts. Parent source review
  produced **18 legacy-field repairs across 15 notes**, including 11 fields
  initially scored SUPPORTED: moderator and mediation roles, the
  hypothesized model, an unmeasured cognitive explanation,
  practical-implication audiences and scope, limitations, and inferred
  future-research agendas. Fresh blind full-note re-audits of all 15
  repaired notes returned **134 SUPPORTED and 1 accepted PARTIAL out of
  135**. The **final state is 275 SUPPORTED and 4 accepted PARTIALs out of
  279**, with **0 UNSUPPORTED and 0 CONTRADICTED**; all 31 notes pass
  overall with current note and source hashes. The accepted PARTIALs are
  Bertrand's Future Research and Key Findings, Holloway's Data & Measures,
  and Khanna's Future Research: reconstructed audit inputs omit the relevant
  discussion or appendix passages, while parent reading of the recovered raw
  text confirms that the claims are faithful. Those fields remain unchanged.
  Tracey's initially PARTIAL Limitations was likewise retained after source
  verification and scored SUPPORTED in the full re-audit required by its
  separate Future Research repair.

  **Desai (2016), AMJ 59-3, is retracted.** Its new Key Findings section
  explicitly opens: “This article has been retracted; the following
  summarizes its originally reported findings.” The note is retained as a
  record of the retracted article; see the publisher's [retraction
  notice](https://journals.aom.org/doi/10.5465/amj.635Retraction).
  Bibliographic frontmatter and paper types are unchanged; scoped CrossRef
  was skipped after field-by-field byte comparisons against the baseline.
  Sequential SQLite, CSV, and BibTeX rebuilds reconcile to 1,167 records;
  BibTeX is byte-identical, with only SQLite and CSV changed. Full-library
  validation passed 1,167/1,167, and the direct regressions passed 22/22 for
  PDF-text fitting and 15/15 for augmentation verification.

  This is the **first backfill batch run end-to-end on `gpt-6-astra` (GPT-6
  Astra)** for augmentation and audit, opening stamp era 30. Provenance eras
  are batches 01–07 `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19
  `gpt-5.6-sol`, 20–23 `claude-opus-5`, 24–29 `gpt-5.6-sol`, and 30
  `gpt-6-astra`. Cross-family spot-audits scored 27/27 for batch 16, 27/27
  for batch 24, and 25/27 for batch 28; both batch-28 divergences were
  repaired in v0.62.0. Batch 30's workshop review will run the next
  spot-audit as a new-model calibration; no result is yet available.

- **v0.62.0 v3 backfill batch 29 (2026-09-04, 1,167 notes):**
  Upgrades **AMJ volume 59 issues 5 and 4, 32 notes total** to the v3 schema —
  all v2 augmentations — and carries one calibration-driven repair to the
  already-v3 Luo (2017) note from batch 28. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 336 v2, and 770 v3. All 33
  touched notes passed `validate_note.py`; the final
  `verify_augmentation.py` sweep passes the 28 target notes with no legacy
  repair and flags exactly the four target notes with documented legacy-field
  repairs, plus Luo's two authorized legacy sections. The first full blind
  9-field rubric-v2 audit returned 294/297 `SUPPORTED`, 3 `PARTIAL`, 0
  `UNSUPPORTED`, and 0 `CONTRADICTED`. Source verification produced **four
  scoped legacy repairs across four batch notes**: Argyres's invented founder/
  investor prescription was removed; Bunderson's practical implication was
  narrowed over two repair rounds to the paper's explicit ideal relational
  structure; Eisenhardt's inferred methodological future-research sentence was
  removed; and Martin's manipulated narrative factors were no longer mislabeled
  as moderators despite a first-pass `SUPPORTED` verdict. The first repair
  re-audits returned 35/36 `SUPPORTED` plus one `PARTIAL`; Bunderson's second
  repair returned 9/9 `SUPPORTED`. The **final state is 297 / 297 prose-field
  verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED`
  (all 33 notes overall pass, with zero stale hashes in scope).

  The workshop's batch-28 cross-family spot-audit identified scope drift in
  Luo's Practical Implication and Future Research. Raw-text adjudication showed
  that the paper frames speed-versus-quality decoupling as implications for
  research on regulation and practice diffusion, not practitioner advice, and
  explicitly calls for comparisons in other settings and longer-window or
  priority-change designs, not a mature-market research agenda. Those two
  fields were repaired without changing Luo's frontmatter or provenance and
  passed a fresh blind 9/9 audit. Before batch-note audit dispatch, literal
  named-entity self-checking also corrected one nonliteral proper-name form in
  Krause's draft Data & Measures field. Bibliographic frontmatter and paper
  types are unchanged, scoped CrossRef was therefore skipped, and
  `library.bib` regenerated byte-identically (only SQLite and CSV changed).
  This batch ran end-to-end on **`gpt-5.6-sol`** for augmentation and audit, the
  tenth such backfill batch. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, and 24–29 `gpt-5.6-sol`. Cross-family spot-audits scored
  27/27 for batch 16, 27/27 for batch 24, and 25/27 for batch 28; the two
  batch-28 divergences were repaired in this release, and no spot-audit is
  scheduled for batch 29's review.

- **v0.61.0 v3 backfill batch 28 (2026-08-31, 1,167 notes):**
  Upgrades **AMJ volume 60 issue 1 and volume 59 issue 6, 32 notes total** to
  the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 368 v2, and 738 v3. All
  32 notes passed `validate_note.py`; the final `verify_augmentation.py` sweep
  passes 23 notes and flags exactly the nine notes with documented legacy-
  field repairs. The first full independent 9-field rubric-v2 audit returned
  275/288 `SUPPORTED`, 12 `PARTIAL`, 0 `UNSUPPORTED`, and 1 `CONTRADICTED`.
  Source verification produced **17 scoped repairs across 10 notes**: Desai's
  Study 3 factor and Study 3/4 data; Hajro's effectiveness measure; Wang's
  practical, limitation, and future-research claims; Cobb's moderator scope;
  George's editorial research agenda; Heese's future-research sentinel,
  moderator role, reporting-table count, and limitation scope; Kim's
  limitations and future-research sentinel; Olsen's proposed natural-
  experiment design; Vakili's mediator/moderator roles; and Zhao's categorical-
  inequality wording. The first repair re-audits returned 86/90 `SUPPORTED`
  plus four `PARTIAL`; Heese's three newly surfaced factual nuances were
  repaired in round two and returned 9/9 `SUPPORTED`. The **final state is
  287 / 288 prose-field verdicts `SUPPORTED`**, 1 verified-faithful `PARTIAL`,
  0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 32 notes overall pass, with zero
  stale hashes). The sole accepted `PARTIAL` is Desai's Future Research: exact
  fitted-text reconstruction shows that interleaved-reference stripping
  removed 16.38% of the raw text, including the supporting authenticity and
  strategic-display passage; read-after-proof review confirmed the field is
  faithful, so it was not edited. Before audit dispatch, literal-anchor and
  named-entity checks corrected six formulations across five notes. The three
  repairs in new v3 fields had distinct causes — multi-study attribution,
  measure-role framing, and a narrative-versus-reporting-table count — so the
  repeated-new-field stop rule did not trigger. Bibliographic frontmatter and
  paper types are unchanged, and `library.bib` regenerated byte-identically
  (only SQLite and CSV changed). This batch ran end-to-end on
  **`gpt-5.6-sol`** for augmentation and audit, the ninth such backfill batch.
  Provenance eras are batches 01–07 `claude-opus-4-8`, 08–15
  `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23 `claude-opus-5`, and 24–28
  `gpt-5.6-sol`. This batch's workshop review runs the recurring cross-family
  calibration; the prior batch-16 and batch-24 calibrations both scored 27/27
  agreement.

- **v0.60.0 v3 backfill batch 27 (2026-08-31, 1,167 notes):**
  Upgrades **AMJ volume 60 issues 3 and 2, 32 notes total** to the v3 schema —
  all v2 augmentations. The **record total is unchanged at 1,167**; the
  version-tier census shifts to 61 v1, 400 v2, and 706 v3. All 32 notes passed
  `validate_note.py`; the final `verify_augmentation.py` sweep passes 28 notes
  and flags exactly the four notes with documented legacy-field repairs. Each
  touched note passed a fresh full independent 9-field rubric-v2 audit: the
  final state is **286 / 288 prose-field verdicts `SUPPORTED`**, 2
  verified-faithful `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 32
  notes overall pass, with zero stale hashes). Round 1 returned 281/288
  `SUPPORTED` and 7 `PARTIAL`. Source verification produced five scoped
  repairs: Aranda's practical implication was confined to critical assessment
  of success; Farh's Data & Measures now distinguishes 168 complete individual
  observations from 41 teams; Wiedner's future-research agenda was narrowed to
  the paper's explicit cross-practice and neglected-practice calls; Ellis's
  unsupported mental-model-gap prescription was removed; and Heaphy's
  practical implication now reflects institutionalized mediating capacity
  without claiming shared understandings. All five repaired notes returned
  45/45 `SUPPORTED` in fresh blind full-note re-audits. The two accepted
  `PARTIAL`s are Gomulya's limitations and future-research fields: exact audit-
  input reconstruction proves that interleaved-reference stripping hid the
  supporting passages, and reading the recovered raw text confirms both fields
  are faithful, so neither was edited. Before audit dispatch, literal-anchor
  checks corrected two two-column splice anchors; a per-phase review corrected
  Heaphy's interview counts; and exact named-entity verification narrowed six
  new-field source or scale names to literal raw-text forms. The two splice-
  anchor validation failures shared one cause but remained below the stop-rule
  threshold of three; the Heaphy count issue was distinct, so no stop rule was
  triggered. Bibliographic frontmatter and paper types are unchanged, and
  `library.bib` regenerated byte-identically (only SQLite and CSV changed).
  This batch ran end-to-end on **`gpt-5.6-sol`** for augmentation and audit, the
  eighth such backfill batch. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, and 24–27 `gpt-5.6-sol`. The recurring cross-family spot-
  audit most recently ran at batch 24's workshop review with 27/27 agreement,
  matching batch 16; none is scheduled for batch 27, and the next calibration
  is expected at batch 28's workshop review.

- **v0.59.0 v3 backfill batch 26 (2026-08-29, 1,167 notes):**
  Upgrades **AMJ volume 60 issues 5 and 4, 32 notes total** to the v3 schema —
  all v2 augmentations. The **record total is unchanged at 1,167**; the
  version-tier census shifts to 61 v1, 432 v2, and 674 v3. All 32 notes passed
  `validate_note.py`; the final `verify_augmentation.py` sweep passes 24 notes
  and flags exactly the eight notes with documented legacy-field repairs. Each
  touched note passed a fresh full independent 9-field rubric-v2 audit: the
  final state is **286 / 288 prose-field verdicts `SUPPORTED`**, 2
  verified-faithful `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 32
  notes overall pass, with zero stale hashes). Round 1 returned 283/288
  `SUPPORTED` and 5 `PARTIAL`. Source verification produced nine scoped legacy
  repairs across eight notes: corrections to moderated-path wiring and
  contingency attribution; removal of invented generalizability, future-agenda,
  and practitioner-prescription claims; reversal of a transferability error;
  restoration of the paper's construct wording; and confinement of a practical
  implication to syndicate formation. All eight repaired notes returned 72/72
  `SUPPORTED` in fresh blind full-note re-audits. The two accepted `PARTIAL`s
  are proven interleaved-reference strip-loss cases: the fitted audit text hid
  Lee's managerial guidance about team composition and negotiation conditions,
  and Schaumberg's future-research call concerning women's leadership efficacy;
  reading the recovered raw passages confirmed both note fields were faithful,
  so neither was edited. A pre-audit exact-anchor sweep corrected Lawrence's
  normalized two-column-splice anchor. The independent pre-publication
  provenance review then found that Malesky's interim `2013 PCI survey`
  source-name phrase had zero literal raw-text hits; the wording was narrowed
  to the exact source name `PCI survey`, its prompt was regenerated, and a
  fresh blind full-note audit returned 9/9 `SUPPORTED`. No repeated new-field
  or validation cause reached the stop threshold. Bibliographic frontmatter and
  paper types are unchanged, and `library.bib` regenerated byte-identically
  (only SQLite and CSV changed). This batch ran end-to-end on
  **`gpt-5.6-sol`** for augmentation and audit, the seventh such backfill batch.
  Provenance eras are batches 01–07 `claude-opus-4-8`, 08–15 `claude-opus-5`,
  16–19 `gpt-5.6-sol`, 20–23 `claude-opus-5`, and 24–26 `gpt-5.6-sol`. The
  recurring cross-family spot-audit most recently ran at batch 24's workshop
  review with 27/27 agreement, matching batch 16; none is scheduled for batch
  26's review.

- **v0.58.0 v3 backfill batch 25 (2026-08-29, 1,167 notes):**
  Upgrades **AMJ volume 61 issue 1 and volume 60 issue 6, 31 notes total** to
  the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 464 v2, and 642 v3. All 31
  notes passed `validate_note.py`; the final `verify_augmentation.py` sweep
  passes 27 notes and flags exactly the four notes with documented legacy-field
  repairs. Each touched note passed a fresh full independent 9-field rubric-v2
  audit: the final state is **279 / 279 prose-field verdicts `SUPPORTED`**, 0
  `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 31 notes overall pass,
  with zero stale hashes). Round 1 returned 272/279 `SUPPORTED`, 6 `PARTIAL`,
  and 1 `UNSUPPORTED`. Source verification produced seven initial prose-field
  repairs across six notes; fresh blind re-audits surfaced two further factual
  legacy nuances, both repaired and returned 18/18 `SUPPORTED` in a third
  round. The nine repaired fields corrected survey timing, a cross-study scale,
  moderated-path attribution, invented rigidity and prerequisite claims, an
  implied rather than explicit future agenda, unsupported data-source names,
  and a misidentified boundary condition. A final exact-substring sweep also
  caught one Glaser findings anchor that normalized a two-column splice; it was
  replaced with a four-word literal fragment and the full note re-audited 9/9
  `SUPPORTED`. The three first-round non-SUPPORTED Data & Measures calls had
  distinct causes, and the single anchor defect did not form a repeated
  new-field cluster, so the stop rule was not triggered. Bibliographic
  frontmatter remained field-for-field identical to HEAD, paper types were
  unchanged, and `library.bib` regenerated byte-identically (only SQLite and
  CSV changed). This batch ran end-to-end on **`gpt-5.6-sol`** for augmentation
  and audit, the sixth such backfill batch. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, and 24–25 `gpt-5.6-sol`. The recurring cross-family
  spot-audit most recently ran at batch 24's workshop review with 27/27
  agreement, matching batch 16; none is scheduled for batch 25's review.

- **v0.57.0 v3 backfill batch 24 (2026-08-24, 1,167 notes):**
  Upgrades **AMJ volume 61, issues 3 and 2, 31 notes total** to the v3 schema —
  all v2 augmentations. The **record total is unchanged at 1,167**; the
  version-tier census shifts to 61 v1, 495 v2, and 611 v3. All 31 notes passed
  `validate_note.py` and their initial `verify_augmentation.py` diff-guards.
  Each touched note then passed a fresh full independent 9-field rubric-v2
  audit: the final state is **278 / 279 prose-field verdicts `SUPPORTED`**, 1
  verified-faithful `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 31
  notes overall pass, with zero stale hashes). Round 1 returned 266/279
  `SUPPORTED` with 13 `PARTIAL`s. Source verification produced 14 initial
  scoped legacy-field repairs across 12 notes; fresh blind re-audits surfaced
  three further legacy wording nuances, bringing the total to 17. Each was
  repaired, and the three final
  re-audits returned 27/27 `SUPPORTED`. No repair landed in a new v3 field, so
  the repeated-new-field stop rule was not approached. The sole accepted
  `PARTIAL` is Foulk's `future_research`: exact audit-input reconstruction
  shows that `fit_pdf_text_for_audit` removed 47,339 of 147,118 raw characters
  (32.18%), including the raw-text phrases “motivation and self-monitoring”
  and “narcissism and self-concern.” Reading the recovered passage confirmed
  that it explicitly proposes those moderators, so the note is faithful and
  the auditor was blind to the interleaved-reference tail. Bibliographic
  frontmatter remained field-for-field identical to HEAD, paper types were
  unchanged, and `library.bib` regenerated byte-identically (only SQLite and
  CSV changed). This batch ran end-to-end on **`gpt-5.6-sol`** for augmentation
  and audit, the fifth such backfill batch. Provenance eras are batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, 20–23
  `claude-opus-5`, and 24 `gpt-5.6-sol`; this batch's workshop review includes
  the recurring cross-family spot-audit (the batch-16 calibration scored
  27/27 agreement).

- **v0.56.0 v3 backfill batch 23 (2026-08-12, 1,167 notes):**
  Upgrades **AMJ volume 61, issues 5 and 4, 31 notes total** to the v3 schema —
  all v2 augmentations, and the largest batch of the backfill so far. The
  **record total is unchanged at 1,167**; the version-tier census shifts to 61
  v1, 526 v2, and 580 v3. All 31 notes passed `validate_note.py` and the
  `verify_augmentation.py` diff-guard, 30 of them on the first attempt (one note
  used its single permitted self-fix cycle). Each touched note then passed a
  fresh full independent 9-field rubric-v2 audit: the final state is **275 / 279
  prose-field verdicts `SUPPORTED`**, 4 faithful `PARTIAL`s, 0 `UNSUPPORTED`,
  and 0 `CONTRADICTED` (all 31 notes overall pass). Round 1 returned 272/279
  `SUPPORTED` with 7 `PARTIAL`s; **six fields across six notes were
  source-verified drift and were repaired, and five of the six returned
  `SUPPORTED` in fresh blind re-audits**. Three repairs share the recurring
  legacy class — a limitation or direction the paper never states, in two cases
  against the paper's own text: Baer's Limitations claimed Study 2's laboratory
  scenario limited generalization, where the paper lists that design under
  *Strengths* and says the two studies' consistency gives "more confidence in
  the robustness and generalizability of our findings"; Kotha's Limitations said
  a one-TTO design "limits direct generalization", where the paper speculates
  that "the theoretical principles from our framework will generally apply"; and
  Dumas's Future Research recast an ideal-worker discussion claim as a research
  agenda in place of the paper's own stated call. Deken's Mechanism Process
  conflated the paper's six *periods* with its eight strategic configurations
  (C1–C8) — the note's own new v3 sections already had it right. Gupta's
  Practical Implication addressed "leaders and boards", where "board" appears in
  the paper only as a CEO-duality control variable and in reference entries;
  that field had scored `SUPPORTED` and was repaired under the two-channel rule
  after parent verification against the raw text. Only **one repair landed in a
  new v3 field** — Dai's Data & Measures inverted the paper's stated sign
  convention for change in confidence ("negative values indicated that
  participants became less confident") — so the repeated-new-field stop rule was
  never approached, and no sign or direction reversal appeared anywhere else in
  the batch. The four remaining `PARTIAL`s are accepted, not edited. Three are
  the interleaved-`REFERENCES` class, each proven by reconstructing the exact
  text the auditor received: König's `key_findings` at a 19.8% strip ratio, and
  both of Kotha's at **14.6% — below the 15% caution threshold** — confirming
  for a third consecutive batch that the flag routes attention rather than
  bounding the class. The fourth is different in kind: Deken's `future_research`
  strips **0.0%**, so both auditors saw identical text, yet round 1 scored it
  `SUPPORTED` and round 2 `PARTIAL`, disputing only framing; it was accepted
  under the repair convergence bound. Two writer-channel concerns closed without
  a fix after parent verification, one of which **averted an over-repair** —
  Hubbard's paper does discuss generalizing to "another expert stakeholder
  group". `library.bib` regenerated byte-identical (the all-augmentation
  signature — only SQLite and CSV changed). This batch ran on **`claude-opus-5`
  under Claude Code** for both augmentation and audit, the fourth consecutive
  batch in that stamp era; backfill provenance stamps now span batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, and 20–23
  `claude-opus-5`.

- **v0.55.0 v3 backfill batch 22 (2026-08-06, 1,167 notes):**
  Upgrades **AMJ volume 62 issue 1 and volume 61 issue 6, 27 notes total** to the
  v3 schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 557 v2, and 549 v3. All 27 notes
  passed `validate_note.py` and the `verify_augmentation.py` diff-guard, 26 of
  them on the first attempt (one note used its single permitted self-fix cycle).
  Each touched note then passed a fresh full independent 9-field rubric-v2 audit:
  the final state is **238 / 243 prose-field verdicts `SUPPORTED`**, 5 faithful
  `PARTIAL`s, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 27 notes overall pass).
  Round 1 returned 234/243 `SUPPORTED` with 9 `PARTIAL`s; **four were
  source-verified drift and were repaired, and all four repaired fields came back
  `SUPPORTED` in fresh blind re-audits**. Three repairs share the recurring legacy
  class — a limitation or future direction the paper never states, in all three
  cases against the paper's own text: Jia's Limitations said the findings may not
  generalize to privately owned firms where the paper states its theory "should,
  in principle, be applicable" to them; Schilpzand's Future Research recommended
  actigraphy where the paper raises it only to conclude that "Barnes (2012) even
  recommended self-rated sleep as the most appropriate and useful methodology";
  and Fini's Future Research recast a boundary condition the paper calls "rare"
  and "likely to be met in most settings" as a research agenda. The fourth fixed a
  direction garble: Simsek's Mechanism Process summary said research trails
  practice, where the editorial says "When impact trails research" and "When
  impact leads research" — the note's own bullets already had it right. The five
  remaining `PARTIAL`s are accepted, not edited: all are the
  interleaved-`REFERENCES` class, where a `REFERENCES` heading begins in column 2
  while column 1 is still running Discussion prose, so the fitted audit input
  discards faithful text. Each was proven by reconstructing the exact text the
  auditor received — Wang's three verdicts at the batch's highest 19.3% strip
  ratio, plus Li's and Simsek's at **14.9% and 13.0%, both below the 15% caution
  threshold**, confirming again that the flag routes attention rather than
  bounding the class. All 27 `hypotheses` and 26 of 27 `key_findings` verdicts
  were `SUPPORTED` in round one, with no sign or direction reversal anywhere in
  the batch, and all four repairs landed in legacy fields, so the
  repeated-new-field stop rule was never approached. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV changed).
  This batch ran on **`claude-opus-5` under Claude Code** for both augmentation
  and audit, the third consecutive batch in that stamp era; backfill provenance
  stamps now span batches 01–07 `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19
  `gpt-5.6-sol`, and 20–22 `claude-opus-5`.

- **v0.54.0 v3 backfill batch 21 (2026-08-05, 1,167 notes):**
  Upgrades **AMJ volume 62, issues 3 and 2, 25 notes total** to the v3 schema —
  all v2 augmentations. The **record total is unchanged at 1,167**; the
  version-tier census shifts to 61 v1, 584 v2, and 522 v3. All 25 notes passed
  `validate_note.py` and the `verify_augmentation.py` diff-guard, 24 of them on
  the first attempt (one note used its single permitted self-fix cycle). Each
  touched note then passed a fresh full independent 9-field rubric-v2 audit:
  the final state is **224 / 225 prose-field verdicts `SUPPORTED`**, 1 faithful
  `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 25 notes overall pass).
  Round 1 returned 217/225 `SUPPORTED` with 8 `PARTIAL`s; **seven were
  source-verified drift and were repaired, and all 63 verdicts across the seven
  fresh blind re-audits came back `SUPPORTED`**. Six repairs share one legacy
  class — a limitation, future direction, or audience the paper never states,
  in three cases against the paper's own text: Dutt's Future Research asked
  whether the findings hold in pharmaceuticals, telecoms, and ICT where the
  paper states they *do* apply there; Weber's Limitations claimed the
  experiments cannot reproduce real contract complexity where the paper's
  conclusion touts experimental "precision and control"; and Zuzul's
  Limitations added a prevalence caveat where the paper argues its cases'
  differences "amplify the generalizability". The seventh repair is the batch's
  only new-field content error: Shi's Data & Measures credited the Heckman
  selection model with addressing the non-random assignment of language style
  matching, which the paper assigns to IPTW — its Heckman first stage predicts
  "whether a firm undertakes M&As in a year". The single remaining `PARTIAL` is
  accepted, not edited: Sherf's Data & Measures faithfully reports an
  Appendix A pilot (202 managers via Prolific, 263 via Qualtrics) that is
  present in the raw text but **absent from the fitted audit input**, confirmed
  by reconstructing the exact text the auditor received — the
  interleaved-`REFERENCES` class at the batch's highest 22.3% strip ratio. All
  25 `hypotheses` and all 25 `key_findings` verdicts were `SUPPORTED` in round
  one, with no sign or direction reversal anywhere in the batch, so the
  repeated-new-field stop rule was never approached. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV
  changed). This batch ran on **`claude-opus-5` under Claude Code** for both
  augmentation and audit, the second consecutive batch in that stamp era;
  backfill provenance stamps now span batches 01–07 `claude-opus-4-8`, 08–15
  `claude-opus-5`, 16–19 `gpt-5.6-sol`, and 20–21 `claude-opus-5`.

- **v0.53.0 v3 backfill batch 20 (2026-08-04, 1,167 notes):**
  Upgrades **AMJ volume 62, issues 5 and 4, 25 notes total** to the v3 schema —
  all v2 augmentations. The **record total is unchanged at 1,167**; the
  version-tier census shifts to 61 v1, 609 v2, and 497 v3. All 25 notes passed
  `validate_note.py`, and all 25 augmentation deltas passed the initial
  `verify_augmentation.py` guard on their first attempt, with no self-fix cycle
  used anywhere in the batch. Each touched note then passed a fresh full
  independent 9-field rubric-v2 audit: the final state is **217 / 225
  prose-field verdicts `SUPPORTED`**, 8 faithful `PARTIAL`, 0 `UNSUPPORTED`,
  and 0 `CONTRADICTED` (all 25 notes overall pass). Two evidence-based
  legacy-field repairs cleared fresh blind re-audits at 9/9 `SUPPORTED` each:
  Lee's Mechanism Process had labelled peer learning a same-level mediator
  where the paper's footnote 7 states the model "does not depict mediation
  process at the same level", and Sgourev's Practical Implication had given
  only the threat half of a managerial argument the paper frames as "both the
  opportunities and threats". The 8 remaining `PARTIAL`s are accepted, not
  edited: four (Wang ×2, Shea ×2) are faithful claims verified in raw text that
  the audit input discards where a `REFERENCES` heading occupies column 2 while
  column 1 still runs Discussion prose, and a fifth (De Stefano) is the same
  class at a **13.9% strip ratio, below the 15% suspicion threshold** — a
  reminder that the detector is a routing aid, not a floor. All 75 verdicts on
  the three new v3 fields were `SUPPORTED`, so the repeated-new-field stop rule
  was never approached. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). This batch
  **returns to `claude-opus-5` under Claude Code for both augmentation and
  audit, after four consecutive batches (16–19) run end-to-end on
  `gpt-5.6-sol`**; backfill provenance stamps now span batches 01–07
  `claude-opus-4-8`, 08–15 `claude-opus-5`, 16–19 `gpt-5.6-sol`, and 20
  `claude-opus-5`.

- **v0.52.0 v3 backfill batch 19 (2026-08-03, 1,167 notes):**
  Upgrades **AMJ volume 63, issue 1 and volume 62, issue 6, 27 notes total**
  to the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 634 v2, and 472 v3. All 27
  notes passed `validate_note.py`; all augmentation deltas passed the initial
  `verify_augmentation.py` guard without a gate failure. Each touched note then
  passed a fresh full independent 9-field rubric-v2 audit: the final state is
  **242 / 243 prose-field verdicts `SUPPORTED`**, 1 faithful `PARTIAL`, 0
  `UNSUPPORTED`, and 0 `CONTRADICTED` (all 27 notes overall pass). Four
  evidence-based legacy-field repairs across three notes cleared fresh blind
  re-audits. Lee's founder-succession Limitations remains an accepted `PARTIAL`
  because the fitted audit input cuts the left-column discussion at an
  interleaved `REFERENCES` heading, while the retained raw text at lines
  888–925 directly supports the sample-selection, archival-proxy,
  alternative-explanation, and measurement-error limitations. All 81 verdicts
  on the three new v3 fields were `SUPPORTED`, and the repeated-new-field stop
  rule was not triggered. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). This is the
  **fourth consecutive backfill batch run end-to-end on `gpt-5.6-sol` for both
  augmentation and audit**. The recurring workshop cross-family spot-audit
  applies; the next calibration runs at the batch-20 review.

- **v0.51.0 v3 backfill batch 18 (2026-08-02, 1,167 notes):**
  Upgrades **AMJ volume 63, issues 3 and 2, 24 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 661 v2, and 445 v3. All 24 notes
  passed `validate_note.py`; all augmentation deltas passed the initial
  `verify_augmentation.py` guard without a gate failure. Each touched note
  then passed a fresh full independent 9-field rubric-v2 audit: the final
  state is **215 / 216 prose-field verdicts `SUPPORTED`**, 1 faithful
  `PARTIAL`, 0 `UNSUPPORTED`, and 0 `CONTRADICTED` (all 24 notes overall
  pass). Nine evidence-based edit operations repaired eight note-field pairs
  across six notes in two repair rounds; fresh blind re-audits cleared every
  repair. Beckman's Future Research remains an accepted `PARTIAL` because the
  fitted audit input cuts at an interleaved `REFERENCES` heading, while the
  retained raw text at lines 1248–1260 directly supports the gender-research
  rationale. All 72 verdicts on the three new v3 fields were `SUPPORTED`, and
  the repeated-new-field stop rule was not triggered. `library.bib`
  regenerated byte-identical (the all-augmentation signature — only SQLite
  and CSV changed). This is the **third backfill batch run end-to-end on
  `gpt-5.6-sol` for both augmentation and audit**. The recurring workshop
  cross-family spot-audit applies; the next calibration is due around batch
  20.

- **v0.50.0 v3 backfill batch 17 (2026-08-02, 1,167 notes):**
  Upgrades **AMJ volume 63, issues 5 and 4, 24 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 685 v2, and 421 v3. All 24 notes
  passed `validate_note.py` and the initial `verify_augmentation.py` delta
  guard without a gate failure. Each touched note then passed a fresh full
  independent 9-field rubric-v2 audit: the final state is **216 / 216
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`, and 0
  `CONTRADICTED` (all 24 notes overall pass). Seven evidence-based repairs
  narrowed legacy prose across four notes in one repair round: Ody-Brasier's
  Practical Implication, Limitations, and Future Research; Yi's Limitations;
  Bourgoin's Research Question and Future Research; and Cloutier's Future
  Research. All four notes cleared fresh blind re-audit, so no `PARTIAL` was
  accepted. All 72 verdicts on the three new v3 fields were `SUPPORTED`, and
  the repeated-new-field stop rule was not triggered. `library.bib`
  regenerated byte-identical (the all-augmentation signature — only SQLite
  and CSV changed). This is the **second backfill batch run end-to-end on
  `gpt-5.6-sol` for both augmentation and audit**. The recurring workshop
  cross-family spot-audit applies; batch 16's review scored 27 / 27 agreement.

- **v0.49.0 v3 backfill batch 16 (2026-08-01, 1,167 notes):**
  Upgrades **AMJ volume 64, issue 1 and volume 63, issue 6, 25 notes total** to
  the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 709 v2, and 397 v3. All 25
  augmentations passed `validate_note.py` and the `verify_augmentation.py`
  diff-guard on the first attempt with zero self-fix cycles. Each touched note
  then passed a fresh full independent 9-field rubric-v2 audit: the final state
  is **225 / 225 prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0
  `UNSUPPORTED`, and 0 `CONTRADICTED` (all 25 notes overall pass), after five
  evidence-based legacy-field repairs across four notes in two repair rounds
  and three audit rounds. The round-1 repairs removed inferred practitioner
  directives from Abdurakhmonov, Cappellaro, and Pierce and narrowed
  Taeuscher's Limitations to the paper's stated inability to measure legitimacy
  directly. A fresh auditor then identified one new Cappellaro Future Research
  nuance; it was narrowed to the paper's explicit calls and cleared in round 3.
  No new v3 field drew a non-`SUPPORTED` verdict, so the repeated-new-field stop
  rule was not triggered. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). This is the
  **first backfill batch run end-to-end on `gpt-5.6-sol` for both augmentation
  and audit**; batches 01–07 recorded `claude-opus-4-8`, and batches 08–15
  recorded `claude-opus-5`. A cross-family spot-audit follows at the workshop
  review.

- **v0.48.0 v3 backfill batch 15 (2026-08-01, 1,167 notes):**
  Upgrades **AMJ volume 64, issue 3 and volume 64, issue 2, 25 notes total** to the
  v3 schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 734 v2, 372 v3. The upgrade phase was
  the cleanest of the backfill so far: **all 25 augmentations passed
  `validate_note.py` and the `verify_augmentation.py` diff-guard on the first
  attempt, with zero self-fix cycles.** Each touched note then passed a fresh full
  independent 9-field rubric-v2 audit, and this batch is the **first of the
  backfill to finish spotless — 225 / 225 prose-field verdicts `SUPPORTED`**, 0
  `PARTIAL`, 0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 25 notes overall pass), after
  nineteen evidence-based repairs across ten notes in three repair rounds and four
  audit rounds. No residual `PARTIAL` had to be accepted and documented; every one
  of the thirteen found in round 1 was cleared by repair. Six of those thirteen
  were the recurring no-practice-section scope drift this 2021 cohort keeps
  producing — a pre-scan run before the audits found that **14 of the 25 papers
  contain no practical-implication marker at all**, and five of the six drifted
  fields sat on flagged papers. Jacobs, Jiang, Naumovska, Reinecke and Zhelyazkov
  each prescribed advice to audiences their papers never address; Myers listed
  "clients" as an external learning source when the paper's own five are faculty,
  industry experts, other teams, second-year MBA students and personal network
  contacts, clients being the project sponsors who *rate* team performance. Three
  landed on the new v3 sections and each had a distinct cause: Liu credited the
  China Stock Market and Accounting Research database with ownership information
  when the paper searched it for an alternative political-linkage robustness
  measure; Opper described M8–M12 as uniformly adding planning dummies and their
  interactions when the paper builds them stepwise; and Reinecke misreported two of
  the paper's three "revealing case" reasons, which a page break had split across
  columns. Wolfson presented HR information systems as a practice tool when the
  paper raises them only as a future-research archive, and Zipay grouped moral
  identity under antecedents of leniency when the paper names it as a personality
  trait moderating *reactions* to leniency. Three of round 2's five remaining
  `PARTIAL`s were introduced by the repairs themselves and were caught only because
  every repaired note is re-audited — the strongest case yet for the
  assemble-then-repair-then-re-audit ordering. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV changed).
  This batch ran on `claude-opus-5`, as batches 08 through 14 did.

- **v0.47.0 v3 backfill batch 14 (2026-07-31, 1,167 notes):**
  Upgrades **AMJ volume 64, issue 5 and volume 64, issue 4, 25 notes total** to the
  v3 schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 759 v2, 347 v3. The upgrade phase was
  the fourth consecutive clean one: 24 of 25 augmentations passed `validate_note.py`
  and the `verify_augmentation.py` diff-guard on the first attempt, the single
  self-fix being a cosmetic Cronbach-alpha symbol alignment inside Hill's own newly
  inserted Data & Measures text. Each touched note then passed a fresh full
  independent 9-field rubric-v2 audit: **224 / 225 prose-field verdicts
  `SUPPORTED`**, 1 `PARTIAL`, 0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 25 notes
  overall pass), after seven evidence-based repairs across six notes in three
  repair rounds. **All six of the round-1 `PARTIAL`s fell on legacy prose fields
  and none on the three new v3 sections** — the cleanest new-field result of the
  backfill so far. Tang's Practical Implication prescribed what "firms should"
  and "managers seeking ambidextrous strategy should" do for a paper in which
  none of "practical implication", "implications for practice", "managers should"
  or "firms should" occurs even once; Methot's Future Research recast the paper's
  cross-cultural and expatriate *practice* contribution as a research agenda;
  Dyer's Theoretical Contribution credited exploratory salary-band and equity
  evidence with producing a "zone of misaligned incentives" the paper explicitly
  calls an untested "logical conclusion from the theory"; Ruebottom's Limitations
  inverted a premise, cautioning against generalizing to "all stigmatized
  industries" where the paper states "we expect that all stigmatized industries
  will have opportunities within them"; and Bettinazzi's Mechanism Process both
  labelled four variables "moderators" for a design that estimates no interaction
  terms at all — it compares coefficients across paired models with Wald tests —
  and attributed to selloff cost an argument the paper runs on the cost of
  resolving conflicts internally. The seventh repair did not come from the audit:
  Bain's augmentation agent flagged, under the flag-don't-fix contract, that
  "Across studies, the effects held for promotive and prohibitive voice and for
  both men and women" over-reached, and although the auditor had scored that field
  `SUPPORTED`, source verification upheld the agent — voice type appears eleven
  times in Study 1 and not once in Studies 2 or 3. **One residual `PARTIAL` is
  accepted and documented rather than edited.** It is Sitzmann's Future Research,
  the interleaved-references truncation class: the REFERENCES heading sits atop
  column 2 at line 1340 while column 1 still runs Future Research prose, so the
  strip discarded 24.6% of the paper, and the flagged call for research on how
  "pornography consumption and rape affect the gender wage gap" verifies almost
  verbatim in the raw text. Batch 11's signal held for a fifth consecutive batch:
  wherever a legacy field and a newly written v3 section covered the same fact —
  Dyer and Bettinazzi — the new section was right and the legacy field wrong.
  `library.bib` regenerated byte-identical (the all-augmentation signature — only
  SQLite and CSV changed). This batch ran on `claude-opus-5`, as batches 08
  through 13 did.

- **v0.46.0 v3 backfill batch 13 (2026-07-30, 1,167 notes):**
  Upgrades **AMJ volume 65, issue 1 and volume 64, issue 6, 26 notes total** to the
  v3 schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 784 v2, 322 v3. The upgrade phase was
  the third consecutive clean one: all 26 augmentations passed `validate_note.py`
  and the `verify_augmentation.py` diff-guard on the first attempt, with no
  self-fix cycles. Each touched note then passed a fresh full independent 9-field
  rubric-v2 audit: **229 / 234 prose-field verdicts `SUPPORTED`**, 5 `PARTIAL`,
  0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 26 notes overall pass), after
  twenty-one evidence-based repairs across sixteen notes in three repair rounds —
  the heaviest repair load of the backfill to date. Fifteen of the twenty-one
  repairs fall on legacy prose fields written before the v3 standard.
  Practical-implication scope drift was the dominant legacy class, with six
  instances, three of them on papers that have no practical-implications section
  at all: Lee prescribed that "executives and directors should treat CSR-oriented
  unrest as strongly informative" for a paper in which the phrase "practical
  implication" never appears, Guo advised executives and investor-relations teams
  for a paper that names IR teams only as the authors of the script, and Yu
  addressed "managers and policymakers" and "alliance partners" where neither
  phrase occurs. Post re-attributed to CEOs and boards an instruction the paper
  gives to "female executives invited to join an all-male TMT"; Baba addressed
  "governments and other central actors" where the paper's three crucial points
  address "peripheral actors such as the Crees"; and Wang credited professional
  associations with a broadening of blame the paper attributes to the government.
  The multi-study support-pattern class recurred for the third batch running, in
  Burgess's Mechanism Process ("converge on these linkages" for a design in which
  only Study 1 tested all six hypotheses), and Lee's Limitations inverted a
  premise outright, claiming causal inference rested on 2SLS where the paper
  concludes its tests make "the 2SLS regression unnecessary". Six repairs touched
  new v3 fields, five of them Data & Measures with five distinct causes —
  Dushnitsky mis-explained a sample-size drop that Table 3 attributes to an
  interaction rather than a control present in all six models, Post reversed two
  dictionary credits across a column break under a "respectively", Vuori
  mislabelled Table 1's interview counts as informant counts, Mikolon added an
  unstated temporal-separation inference, and Schaubroeck overlooked the paper's
  explicit "Except for ..." clause on variable overlap. **Five residual
  `PARTIAL`s are accepted and documented rather than edited.** Two are Guo's, and
  are the interleaved-references truncation class: its REFERENCES heading sits
  atop column 2 at line 1357 while column 1 still runs Future Research prose,
  so the strip discarded 16.8% of the paper, and both flagged claims — the
  data-availability constraint and the verbal/nonverbal delivery-attribute list —
  verify verbatim in the raw text. Two are Wang's, one a framing nuance whose
  content the auditor conceded is true, the other an auditor locality error: the
  paper does discuss "the accounting profession in the U.S. and the U.K." in the
  same future-research thread the note compresses. The fifth is Dushnitsky's Key
  Findings, where the paper's own Figure 3B description contradicts itself and
  the note follows the paper's five separate statements that the effect is
  stronger for younger startups. Batch 11's signal held for the third consecutive
  batch and more strongly: in every case where a legacy field and a newly written
  v3 section covered the same fact — Burgess, Kuhnel, Frey and Lee — the new
  section was right and the legacy field wrong. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV changed).
  This batch ran on `claude-opus-5`, as batches 08 through 12 did.

- **v0.45.0 v3 backfill batch 12 (2026-07-30, 1,167 notes):**
  Upgrades **AMJ volume 65, issue 3 and issue 2, 26 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 810 v2, 296 v3. The upgrade phase
  matched batch 11's clean run: all 26 augmentations passed `validate_note.py`
  and the `verify_augmentation.py` diff-guard on the first attempt, with no
  self-fix cycles. Each touched note then passed a fresh full independent
  9-field rubric-v2 audit: **232 / 234 prose-field verdicts `SUPPORTED`**,
  2 `PARTIAL`, 0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 26 notes overall pass),
  after nine evidence-based repairs across seven notes in three repair rounds.
  Issue 2 was the cleanest issue of the backfill to date, arriving at 116 / 117
  `SUPPORTED` with a single flagged field. Seven of the nine repairs fall on
  legacy prose fields written before the v3 standard. Two documented failure
  classes recurred, both as multi-study support-pattern overstatement: Tewfik's
  Mechanism Process said the indirect effect through an other-focused
  orientation "held across all four studies" when Study 1 "did not measure the
  hypothesized mediator", and Semadeni's said GEE models "support all six
  hypotheses" when the paper's own Results describe Hypothesis 5 as receiving
  "partial support" and Table 2 flags the coefficient at p < 0.1. Gibson
  reproduced the batch-10 premise class in reverse, listing the Indigenous
  Australian setting as a limitation where the paper's "Transferability to Other
  Contexts" section argues the framework "likely has applicability to many
  efforts at social change"; Hein attributed a "constrains generalizability"
  framing to a paper whose text contains no form of the word; Lucas extrapolated
  a call to "more directly measure" its authentication processes; and Tewfik's
  Limitations carried two unstated inferences and then, in a third round, an
  over-attribution the paper confines to "ultimate interpersonal evaluations".
  Two repairs touched new v3 fields, with unrelated causes: Fang's Data &
  Measures called both studies cross-sectional where the paper describes the
  NLSY97 as "a longitudinal study of a nationally representative cohort", and
  Martin's attributed the class-perception chi-squares to a within-study check
  when they come from the non-preregistered 267-participant pretest of
  footnote 3. **Two residual `PARTIAL`s are accepted and documented rather than
  edited**, both on Fang and both instances of the interleaved-references
  truncation class identified in batch 11: Fang's REFERENCES heading sits atop
  column 2 at 77.9% while column 1 still runs its Limitations and Future
  Research prose, so the strip discarded 22% of the paper, and every flagged
  claim — omitted-variable bias, the uncontrolled cognitive-ability measure, the
  additional-variables and incumbent-composition future-research calls —
  verifies verbatim in the raw text. Batch 11's signal held again: in each case
  where a legacy field and a newly written v3 section covered the same fact, the
  new section was right and the legacy field wrong — Tewfik's and Semadeni's new
  Key Findings both stated the support pattern correctly while their legacy
  prose overstated it. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). This batch ran on
  `claude-opus-5`, as batches 08 through 11 did.

- **v0.44.0 v3 backfill batch 11 (2026-07-30, 1,167 notes):**
  Upgrades **AMJ volume 65, issue 5 and issue 4, 25 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 836 v2, 270 v3. The upgrade phase
  was the cleanest of the backfill so far: all 25 augmentations passed
  `validate_note.py` and the `verify_augmentation.py` diff-guard on the first
  attempt, with no self-fix cycles. Each touched note then passed a fresh full
  independent 9-field rubric-v2 audit: **218 / 225 prose-field verdicts
  `SUPPORTED`**, 7 `PARTIAL`, 0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 25 notes
  overall pass), after fifteen evidence-based repairs across thirteen notes in
  two repair rounds. Thirteen of the fifteen fall on legacy prose fields
  written before the v3 standard. Both documented Mechanism Process failure
  classes appear again. Matusik misstated what the paper *predicted*, narrating
  the coordination gap as one that "persists across episodes" when H5 predicted
  the gap would *increase* and the results "did not support Hypothesis 5".
  Two misstated how a model is *wired*: Solomon claimed the self-regulatory
  cascade "does not fire" under sustained high accountability, where the paper
  has counterfactual thinking and regret still occurring and only the reversal
  blocked; and Zhang claimed a leader-vision moderation "supported across three
  studies, including a cross-lagged design that rules out reverse causation",
  where Study 1 never measured leader vision and the cross-lagged model itself
  reports a significant reverse path. Raffaelli transposed two names, putting
  Hayek on Breguet's management committee where the paper has "Hayek inviting
  Biver to serve on SMH's board and on Breguet's management committee".
  **Scope drift on Practical Implication was the batch's dominant legacy
  pattern, at four instances** — Koppman, Shepherd, Williams and Mannucci each
  addressed prescriptions to audiences their papers never name (managers, NGOs
  and policymakers, support organizations, practitioners); all four were
  narrowed to the papers' own stated scope. The remaining legacy repairs
  corrected an unstated inference in Awate's Limitations, a cross-study
  misattribution in Zhang's Limitations, a context ("television") absent from
  Koppman's future-research sentence, a gloss in Jin's Practical Implication
  that inverted the paper's magnitude-over-direction finding, and Kumar's
  attachment of the paper's coined term "shadow of the broker" to the wrong
  construct. Two repairs touched new v3 fields, with unrelated causes: Eleazar's
  Data & Measures sourced three lawsuit controls to VentureXpert when they come
  from the Federal Judicial Center database, and Doyle's Key Findings said an
  interaction crossed p < .05 "only when covariates were added" when footnote 10
  reports it also reaching significance under the preregistered exclusion plan.
  **Seven residual `PARTIAL`s are accepted and documented rather than edited.**
  Three are verification artifacts on *faithful* notes caused by a newly
  identified audit-prompt truncation class: in two-column extraction the real
  REFERENCES heading can sit atop column 2 while column 1 still carries
  Discussion prose, so the strip discards the interleaved tail — Ferns lost 25%
  of its text and Pamphile 18%, and both notes' flagged claims verify verbatim
  in the raw text. Lazar's Data & Measures faithfully reproduces the paper's own
  sample statements, the discrepancy the auditor found being the paper's own
  arithmetic. The other three are framing nuances on legacy fields whose
  substance verifies in the source, two of them re-scorings of fields a prior
  independent round passed — all accepted under the repair convergence bound.
  Notably, in every case where a legacy field and a newly written v3 section
  covered the same fact, the new section was right and the legacy field wrong:
  writing Hypotheses, Data & Measures and Key Findings forces a close read of
  the results tables, so the backfill is functioning as a corpus audit of pre-v3
  prose. `library.bib` regenerated byte-identical (the all-augmentation
  signature — only SQLite and CSV changed). This batch ran on `claude-opus-5`,
  as batches 08 through 10 did.

- **v0.43.0 v3 backfill batch 10 (2026-07-29, 1,167 notes):**
  Upgrades **AMJ volume 66, issue 1 and volume 65, issue 6, 26 notes total** to
  the v3 schema — all v2 augmentations, and the largest batch of the backfill so
  far. The **record total is unchanged at 1,167**; the version-tier census
  shifts to 61 v1, 861 v2, 245 v3. Each touched note passed a fresh full
  independent 9-field rubric-v2 audit: **228 / 234 prose-field verdicts
  `SUPPORTED`**, 6 `PARTIAL`, 0 `UNSUPPORTED`, 0 `CONTRADICTED` (all 26 notes
  overall pass), after thirteen evidence-based repairs across eight notes in
  three repair rounds. Twelve of the thirteen fall on legacy prose fields
  written before the v3 standard, and this is the first batch in which **both**
  documented Mechanism Process failure classes appear together. Three repairs
  misstated what the paper *predicted*: Dimotakis narrated "negative incidents
  are unconditionally aversive" as the theory when that is the *result* (H7 and
  H8 predicted the conditionality, which held only for positive incidents); Ong
  presented an unbufferable-demands claim as a prediction where the paper says
  "we posit this as an empirical research question"; and Xu (65-6) called a
  downturn "partially borne out" that occurred in neither study, the paper
  noting "the absence of the predicted negative effects at the very high levels
  of leader perfectionism". Two more misstated how a model is *wired*: Chan
  collapsed two of the three value-moderating practices and lost the paper's
  "covertly using value-driven resources", and Dwertmann attributed causal
  reasoning to stereotype updating (the paper assigns it to the
  employee-to-organization link) and motive moderation to reputation (H5a/H5b
  moderate the service-to-CSR link). The remaining legacy repairs narrowed two
  unstated inferences in Lauriano's Limitations, corrected Aversa's
  "field-configuring events" to the paper's own "literature on events", and
  fixed a temporal/temporary wording slip in Xu's Future Research. One repair
  touched a new v3 field: Kundro's Data & Measures attached recruited-sample
  demographics to post-exclusion analysed Ns across three experiments.
  A second round surfaced a generalizability caveat the paper raises and then
  *rejects* (Dwertmann: "we would anticipate comparable or potentially more
  positive results in other national contexts"), and a third round found the
  same premise had propagated to the sibling Future Research field — a new
  pattern worth noting, since repairing one field left the other wrong.
  **Six residual `PARTIAL`s are accepted and documented rather than edited.**
  Three are verification artifacts on *faithful* notes: Lauriano's and Xu's
  Data & Measures draw on Appendix A1 and Appendix B respectively, which the
  audit tooling trims to fit its context budget, and Xu's Future Research sits
  in the same trimmed region. Chan's Practical Implication draws every
  component from the paper's own Boundary Conditions in a paper with no
  practical-implications section, and Dwertmann's remaining two are re-scorings
  of nuances that two earlier independent audit rounds had explicitly noted and
  passed — both accepted under the repair convergence bound. `library.bib`
  regenerated byte-identical (the all-augmentation signature — only SQLite and
  CSV changed). This batch ran on `claude-opus-5`, as batches 08 and 09 did.

- **v0.42.0 v3 backfill batch 09 (2026-07-28, 1,167 notes):**
  Upgrades **AMJ volume 66, issue 3 and issue 2, 24 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 887 v2, 219 v3. Each touched note
  passed a fresh full independent 9-field rubric-v2 audit: **214 / 216
  prose-field verdicts `SUPPORTED`**, 2 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED` (all 24 notes overall pass), after fourteen evidence-based
  repairs across eight notes. Twelve of the fourteen fall on legacy prose
  fields written before the v3 standard. Three of those form the batch's
  recurring pattern — a Mechanism Process that misstates how the paper's own
  model is *wired*: Ingram's mediator Dyadic Individuation was attributed to
  latent semantic analysis when the paper builds it as "a sum of Uniqueness
  for the two members of the dyad" (LSA generates the *other* mediator); Lee
  (66-2) had self-serving attribution dampening an above-aspiration effect
  the paper says it *steepens* ("will decrease their search for alternatives
  to alliances, making future acquisitions less likely"); and Zhang listed
  mentor engagement as a mediator in Study 2B, where the paper labels it
  "Mentor engagement (dependent variable)". The remaining legacy repairs
  removed a fabricated limitation the paper frames as favourable design
  context (Ingram — the words "limitation" and "generaliz" appear nowhere in
  the text), reversed a generalizability claim the paper argues *against*
  (Lee 66-3: the thesis "could still hold in individualistic countries as
  well"), corrected a causal-language upgrade (Bianchi: the paper claims only
  "a more direct test of causality"), re-scoped a machine-learning direction
  that in the paper refers to Instagram's placement algorithm
  (Roccapriore), and dropped two unstated prescriptions (Toivonen, Lee 66-2).
  Two repairs touched new v3 fields: a wrongly cited case in Toivonen's Key
  Findings (the paper states "Clayton did not substantially change his plans")
  and a cross-study coverage error in Cunningham's Data & Measures. A second
  round surfaced two further Data & Measures slips (Bianchi's observation
  range, Zhang's mentee sample), both repaired; a third round returned all
  eighteen fields `SUPPORTED`. **Two residual `PARTIAL`s are accepted and
  documented rather than edited:** Hersel's Data & Measures is *faithful* —
  its word-list details are stated verbatim in the paper's Appendix A, which
  the audit tooling trims to fit its context budget — and Toivonen's
  Practical Implication rests on anchored components in a paper that has no
  practical-implications section, so it is accepted under the repair
  convergence bound. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). This batch ran
  on `claude-opus-5`, as batch 08 did.

- **v0.41.0 v3 backfill batch 08 (2026-07-28, 1,167 notes):**
  Upgrades **AMJ volume 66, issue 5 and issue 4, 23 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 911 v2, 195 v3. Each touched note
  passed a fresh full independent 9-field rubric-v2 audit: **207 / 207
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED` (all 23 notes overall pass), after ten evidence-based
  repairs across eight notes. Nine of the ten fall on legacy prose fields
  written before the v3 standard, and three of those form the batch's one
  recurring pattern — a Mechanism Process that presents an *empirical outcome
  as the paper's ex ante theory*: Banerjee's demand-side penalty on
  distinctiveness from current competitors was framed as theorized when
  Hypothesis 4 predicted the opposite and the paper reports "the opposite
  directionality than predicted" (p < .001); Lander called a
  countermobilization effect "unexpected" that Hypothesis 4 explicitly
  predicted; and Kim narrowed a moderation the paper hypothesized across all
  three dress dimensions (H4a–H4c) down to the single dimension that survived
  testing. The remaining legacy repairs removed an unstated "cultural
  settings" extension (Carnabuci), four caveats the paper never framed as
  limitations (Dang), a generalizability claim and an effect-size
  characterization the paper argues against (Liao), a dropped "descriptive
  rather than prescriptive" caution plus an added "organizations" audience
  (Hussain, the one repair needing a second round), and generic future
  directions substituted for the paper's own (Kundro). Only one repair touched
  a new v3 field: an unstated "U.S." on Study 1's site in Kundro's Data &
  Measures. Fresh independent re-audits of every changed note returned all
  nine fields `SUPPORTED`. `library.bib` regenerated byte-identical (the
  all-augmentation signature — only SQLite and CSV changed). **Provenance
  note:** this batch ran on `claude-opus-5`, so its 23 notes carry
  `augmented_model: "claude-opus-5"` and their audits `auditor_model:
  claude-opus-5`, where backfill batches 01–07 recorded `claude-opus-4-8`.

- **v0.40.0 v3 backfill batch 07 (2026-07-14, 1,167 notes):**
  Upgrades **AMJ volume 67, issue 1 and volume 66, issue 6, 24 notes total** to
  the v3 schema — all v2 augmentations. The **record total is unchanged at
  1,167**; the version-tier census shifts to 61 v1, 934 v2, 172 v3. Each touched
  note passed a fresh full independent 9-field rubric-v2 audit: **216 / 216
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED` (all 24 notes overall pass), after three evidence-based
  repairs cleared in a single round — all three on legacy prose fields written
  before the v3 standard, each an "applied extension" scope-drift narrowed back
  to the paper's own scope: a practical implication that had added an unstated
  "platform designers / category curators" audience (Soublière), a future-
  research field carrying two unframed added directions (Park, coevolutionary
  lock-in), and a limitation asserting a single-firm generalizability caveat
  that the paper's own Generalizability section argues against (Jia). A fresh
  independent re-audit of the three repaired notes returned every field
  `SUPPORTED`. `library.bib` regenerated byte-identical (the all-augmentation
  signature — only SQLite and CSV changed).

- **v0.39.0 v3 backfill batch 06 (2026-07-12, 1,167 notes):**
  Upgrades **AMJ volume 67, issue 3 and issue 2, 21 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 958 v2, 148 v3. Each touched note
  passed a fresh full independent 9-field rubric-v2 audit: **189 / 189
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED` (all 21 notes overall pass), after two evidence-based
  repairs cleared in a single round — one new-field precision fix to Data &
  Measures (Preston relabeled Study 1's 135/51 White/Black split from
  "predecessors" to the appointed coaches, matching the paper's own count) and
  one legacy-limitations fix (Compagni's invented "Steering Committee meetings",
  a specific absent from the paper text). A fresh re-audit of the two repaired
  notes returned every field `SUPPORTED`. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV changed).

- **v0.38.0 v3 backfill batch 05 (2026-07-12, 1,167 notes):**
  Upgrades **AMJ volume 67, issue 5 and issue 4, 18 notes total** to the v3
  schema — all v2 augmentations. The **record total is unchanged at 1,167**;
  the version-tier census shifts to 61 v1, 979 v2, 127 v3. Each touched note
  passed a fresh full independent 9-field rubric-v2 audit: **162 / 162
  prose-field verdicts `SUPPORTED`**, 0 `PARTIAL`, 0 `UNSUPPORTED`,
  0 `CONTRADICTED` (all 18 notes overall pass), after four evidence-based
  repairs cleared in a single round — two new-field precision fixes to Data &
  Measures (the Hallila fixed-effect-set list and the Marti 260-statement
  attribution) and two legacy future-research scope trims (Bliese's invented
  method-pairing examples and Madsen's measurement call, which the paper frames
  as a limitation, not a stated direction). A fresh re-audit of the four
  repaired notes returned every field `SUPPORTED`. `library.bib` regenerated
  byte-identical (the all-augmentation signature — only SQLite and CSV changed).

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

All notes have passed the semantic audit. The v0.69.0 corpus contains 61 legacy v1
notes, 211 v2 notes, and 895 v3 notes; v2/v3 notes carry an `evidence:` anchor
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
  version      = {0.69.0},
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
  extend AMJ coverage into earlier volumes, keeping paper IDs stable
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
