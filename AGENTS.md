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
sustainability research. The current v0.69.0 main-branch snapshot contains 272
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

**Current main-branch audit state (2026-09-13, v0.69.0): 1,167 / 1,167 stored official reports PASS, 0 UNSUPPORTED, 0 CONTRADICTED.**

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
acceptance. The v0.69.0 official reports contain no remaining `UNSUPPORTED` or
`CONTRADICTED` verdicts. A CONTRADICTED verdict was returned on a batch-28
draft and repaired before that release; v0.68.0 repaired Kotha’s published
contradiction, and v0.69.0 repaired the contradictions disclosed above. Audit
outcomes do not establish that all undetected errors are absent.

Agents querying the data can rely on the following:

- **Every abstract is a verbatim substring of the source PDF.** If your agent quotes an abstract from a note, it is quoting the paper.
- **Every factual claim in v2 note frontmatter is anchored.** If your agent cites a sample size or a theory from v2 frontmatter, there is a verbatim PDF quote behind it in the `evidence:` block.
- **Every prose field has passed a semantic audit.** If your agent summarizes a research question, mechanism, or theoretical contribution from a note, it's quoting a claim that was independently cross-checked against the PDF.
- **Zero current `CONTRADICTED` verdicts in v0.69.0.** This describes the stored audit results, not an absolute guarantee that every source contradiction has been detected.

**Caveats:**
- Notes are a snapshot, not a live database. The current v0.69.0 main-branch audit state was checked locally on 2026-09-13.
- The audit can identify hallucinations and direction-reversals, but does not resolve inconsistencies in the source paper itself. Always cite the original paper for any claim of substance.
- `PARTIAL` verdicts can indicate minor paraphrastic drift, compression, or missing source context in the fitted audit input; they are listed in the per-paper audit JSONs but those JSONs are not published to the repo (they contain per-paper reasoning that is better regenerated on demand).

---

## 6. How to cite when your agent surfaces a note

- **Citing the underlying paper:** Use the APA citation block at the bottom of each note's body. That's the canonical citation; the DOI is in the frontmatter and is machine-verifiable via CrossRef.
- **Citing this knowledge base as a research tool:** If your agent or application uses Management Research Notes as a retrieval source, please cite the repository itself:

> Tang, B. (2026). *Management Research Notes: A File-Based Academic Knowledge Base for Management and Business Sustainability Research* (Version 0.69.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.19564336

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
