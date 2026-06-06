# NBS ingestion plan — 2025-12 (5 batches, v0.20.0) + 2026-01 (10 batches, v0.21.0)

End-to-end equivalent of the AMJ one-liner
  `Run /synapse-ingest on <folder>, then commit and publish as a GitHub Release`
— but **distributed across sessions** because 82 + 103 papers will not fit a
single token-limited session. Same end state, reached as:

    PREP (once)  →  N batch prompts (any order, separate sessions)  →  FINALIZE (once)  →  PUBLISH (once)
    └─────────────────── this equals `/synapse-ingest` ──────────────────┘   └─ "commit and publish a Release" ─┘

`/synapse-ingest` itself ends at verify_metadata and does NOT commit; that is
PREP + batches + FINALIZE. The commit + version bump + tag + push + GitHub
Release is PUBLISH — one commit per issue, exactly as v0.15.0–v0.19.0 were done.

Run each issue independently:
- **2025-12** → 82 DOI papers → 5 batches → **v0.20.0** (library 270 → 352); 3 doi-missing excluded.
- **2026-01** → 103 DOI papers → 10 batches → **v0.21.0** (library 352 → 455); 18 doi-missing excluded.
- Total: 185 papers, 15 analysis sessions, 2 GitHub Releases.
- (Alternative: fold both into ONE v0.20.0 release — run 2026-01's PUBLISH only,
  with counts 270 → 455. The per-issue split below matches the established cadence.)

MODEL POLICY (model-agnostic): every analysis session runs on Anthropic's current
strongest model — **today that is Claude Opus 4.8** (`/model claude-opus-4-8[1m]`).
If Anthropic ships a stronger model before you finish all 15 batches, switch the
remaining sessions to it AND re-run PREP step 1 with the new model name. Notes
then carry mixed extraction_model values across batches — that is CORRECT
provenance (each note records what analyzed it), not a bug. Only the model string
changes; the workflow does not.

doi-missing rows are marked in PREP and left for a later cleanup pass.


# ════════════════  NBS 2025-12  ·  82 papers  ·  5 batches  ·  v0.20.0  ════════════════

Batch sizes: [17, 17, 16, 16, 16]  (sum 82).  Release target: v0.20.0, library 270 → 352.

## PREP — run ONCE for 2025-12, before Batch 1 (do NOT skip)

Manifest-level + provenance setup. Not a batch; run once, confirm green, then run
the batch prompts in any order. Re-running is harmless.

```bash
cd /Users/tangbinqi/Claude/Synapse

# 1. Provenance: stamp the model you are ACTUALLY analyzing with into every bundle.
#    Today that is Opus 4.8. (See MODEL POLICY at the top — if a stronger Anthropic
#    model has shipped, put ITS name here instead.)
python3 - <<'PY'
import pathlib
p = pathlib.Path("tools/prepare_paper.py"); t = p.read_text()
import re
t2 = re.sub(r'EXTRACTION_MODEL = "claude-opus-4-\d+"',
            'EXTRACTION_MODEL = "claude-opus-4-8"', t)
if t2 != t:
    p.write_text(t2); print("EXTRACTION_MODEL -> claude-opus-4-8")
elif 'EXTRACTION_MODEL = "claude-opus-4-8"' in t:
    print("EXTRACTION_MODEL already claude-opus-4-8 — no change (idempotent)")
else:
    raise SystemExit("EXTRACTION_MODEL constant not found — inspect prepare_paper.py line 42 by hand")
PY

# 2. Tier 3 gate: backfill volume/issue/pages + auto-correct years from CrossRef.
python3 tools/populate_manifest.py library/NBS/2025-12/manifest.tsv --apply --fix-year
#    Exit 1 is EXPECTED on filename-derived manifests: it only means "TITLE differs"
#    warnings (filenames drop ':' and '?'). Step 3 fixes those. What matters here:
#    0 JOURNAL mismatches, and only small (+/-1) year auto-corrections.

# 3. Canonicalize titles from CrossRef. Filename-derived titles are lossy (no ':'
#    or '?'), which would fail the Step-4.5 verify_metadata gate. This upgrades each
#    DOI row's title to the CrossRef canonical form. SAFE: a row is upgraded only
#    when CrossRef's title is highly similar to the current one; a low-similarity
#    row is FLAGGED (possible wrong DOI), never silently changed. Dry-run, eyeball
#    flags (want 0), then --apply.
python3 tools/canonicalize_titles.py library/NBS/2025-12/manifest.tsv            # dry-run
python3 tools/canonicalize_titles.py library/NBS/2025-12/manifest.tsv --apply    # write

# 4. Structural lint gate. Clean for every DOI row. NOTE: doi-missing rows with a
#    filename year-typo or a non-Latin name may STAY flagged — that is fine; they
#    are excluded from the batches and deferred to the DOI-cleanup pass. A real
#    CrossRef compound-surname mismatch on a DOI row goes in KNOWN_COMPOUND_SURNAMES
#    (tools/lint_manifests.py) with a dated rationale, then re-lint.
python3 tools/lint_manifests.py --manifest library/NBS/2025-12/manifest.tsv

# 5. Bookkeeping: mark DOI-less rows status=doi-missing (excluded from all batches).
python3 - <<'PY'
import csv, pathlib
p = pathlib.Path("library/NBS/2025-12/manifest.tsv")
rows = list(csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"))
cols = list(rows[0].keys()); n = 0
for r in rows:
    if not (r.get("doi") or "").strip() and r.get("status") != "doi-missing":
        r["status"] = "doi-missing"; n += 1
with p.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter="\t"); w.writeheader(); w.writerows(rows)
print(f"marked {n} rows doi-missing")
PY
```

Proceed to batches once steps 2–4 are green (lint may keep doi-missing rows
flagged — that's expected). The 3 doi-missing papers for 2025-12 are listed
at the bottom of this section.

### 2025-12 — Batch 1 of 5  (17 papers)

```
CONTEXT — Synapse NBS ingestion · 2025-12 · Batch 1/5 (17 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2025-12 folder. Run
the scoped steps below on EXACTLY the 17 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2025-12/pdfs/.

PRECONDITION: the one-time PREP block for 2025-12 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2025-12/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2025-12/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 17 PDFs in → 17 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 5 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2025-12.

THIS BATCH — 17 PDFs (process exactly these, ignore all others):
Aagaard 2025 More-than-capitalist economies Insights from community supported agriculture, tiny houses and hitchhiking in Denmark.pdf
Akbari 2026 The real effects of protecting biodiversity.pdf
Albrecht 2025 Is a picture worth a thousand words Image usage in ESG reports.pdf
Allen 2026 Do investors care about the rainforest Evidence from voluntary carbon offsets around the world.pdf
Amaral 2025 Practice Paper—AI-Driven Behavioral Nudges for Organizations An Integrative System for Sustainable Resource Management [10.1287_mksc.2024.1154].pdf
Amaral 2025 Siloed Sustainability How Paradox Management Unravels in Integrative Practice Implementation.pdf
Anand 2025 Invisible Inequality in Entrepreneurial Ecosystems The Micro-Foundations of Navigating Marginalization.pdf
Arora 2026 Reaffirming and Renewing Our Declaration of Interdependence.pdf
Berman 2025 Kazakh Sharing Practices A Critical Inquiry Into Sharing Economy Models From the Vantage of Ownership in Collective Societies.pdf
Bocken 2025 Innovating for impact Harnessing business model innovation to tackle grand challenges.pdf
Boman 2025 Ethical trade-offs in fast fashion Exploring social, environmental, and health dimensions in clothing consumption.pdf
Briscoe 2026 Seeking Greener Pastures Employee Turnover Following Corporate Stakeholder Violations.pdf
Bu 2026 Pollution havens versus gates of hell Environmental pollution and multinationals foreign investment.pdf
Cao 2026 Biodiversity entrepreneurship.pdf
Cennamo 2025 Platform Regulation Beyond Power and Size.pdf
Chandon 2026 When and how simplified nutrition labels improve fast-food choices.pdf
Chen 2026 The Aesthetics of Impact Making Impact Beautiful, Not Just Useful.pdf
```

### 2025-12 — Batch 2 of 5  (17 papers)

```
CONTEXT — Synapse NBS ingestion · 2025-12 · Batch 2/5 (17 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2025-12 folder. Run
the scoped steps below on EXACTLY the 17 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2025-12/pdfs/.

PRECONDITION: the one-time PREP block for 2025-12 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2025-12/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2025-12/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 17 PDFs in → 17 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 5 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2025-12.

THIS BATCH — 17 PDFs (process exactly these, ignore all others):
Chevalier 2025 Fixed capital and growth imperatives Is commercial aviation trapped in a treadmill.pdf
Chioatto 2025 “Local Heroes” Construction firms pioneering circular innovation.pdf
Choi 2026 Human Capital Disclosure and Labor Market Outcomes Evidence from Regulation S-K.pdf
Deore 2025 Board gender diversity, innovation ambidexterity, and firm performance.pdf
Duenas 2025 Accounting and post-colonial resistance Affective ambivalence in the international development assemblage.pdf
Dupont 2025 The Unintended Carbon Impacts of Large-Scale Electricity Storage.pdf
Fang 2026 Political Segregation in the Labor Market and the Persistence of Pay Gaps.pdf
Freeman 2025 Linking Multisite Sex Ad Data at the Individual Level to Aid Counter-Trafficking Efforts.pdf
García-Alaminos 2025 Recent global value chain reconfiguration drivers and consequences on EU carbon footprint.pdf
Gardberg 2026 Evaluating Organizations in an Age of Absurdity How Fake News Disrupts the Relationship Between Business and Society.pdf
Garel 2026 Firm-level nature dependence.pdf
Gjerde 2026 Corporate nature risk perceptions.pdf
Goethals 2025 Towards a Justice-Oriented Human Rights Due Diligence Approach for Migrant Labor.pdf
Guidolin 2026 The pricing of biodiversity risk in commodity markets.pdf
Guo 2025 Introduction to the special issue ‘Biodiversity and finance Risk, disclosure and double materiality.’.pdf
Haley 2026 Do sustainability reports contain financially material information.pdf
Hampton 2025 How negative accounting news events, voluntary ESG assurance, and assurance provider influence consumer purchasing intentions.pdf
```

### 2025-12 — Batch 3 of 5  (16 papers)

```
CONTEXT — Synapse NBS ingestion · 2025-12 · Batch 3/5 (16 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2025-12 folder. Run
the scoped steps below on EXACTLY the 16 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2025-12/pdfs/.

PRECONDITION: the one-time PREP block for 2025-12 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2025-12/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2025-12/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 16 PDFs in → 16 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 5 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2025-12.

THIS BATCH — 16 PDFs (process exactly these, ignore all others):
Hasselbalch 2025 Reimagining growth futures Overcoming the false binary between green growth and degrowth.pdf
Inoue 2025 Can objective information update subjective beliefs on sustainable farming Evidence from a randomized experiment with Japanese rice farmers.pdf
Jeong 2026 Bottom-up effects of female strategic leadership Firm performance effects through employees.pdf
Jia 2025 Alienable or inalienable, and how Individual property rights in commons governance.pdf
Kamal 2025 Does an exclusive relationship with government banks matter during a climate shock.pdf
Kapacinskaite 2026 From wells to windmills Resource redeployment and new technology investment in the energy sector.pdf
Karimzadeh 2025 Waste delinking A pathway to degrowth.pdf
Kim 2025 Changes in the Salience of Collective Reputations Information Disclosure and Shareholder Reactions.pdf
Kim 2025 When Good Intentions Backfire The Asymmetric Effects of Minority-Ownership Markers for Businesses on Online Platforms.pdf
Lee 2025 Leveraging Large Language Models for Hate Speech Detection Multi-Agent, Information-Theoretic Prompt Learning for Enhancing Contextual Understanding.pdf
Lee 2026 The Hidden Impact of Prosumers and Its Fair Mitigation.pdf
Li 2025 An optimized shared responsibility accounting framework unveiling the big black shadows behind small emitters in global value chains.pdf
Li 2025 Corporate biodiversity risk exposure in China A system-based perspective from natural capital theory using machine and deep learning algorithms.pdf
Li 2025 Redesigning Harvesting Processes and Improving Working Conditions in Agribusiness.pdf
Li 2025 The Ripple Effect of Reputation Spillover How Corruption Fugitives Shape Consumer Perceptions of Fugitives’ Host Countries and Their MNEs.pdf
Li 2025 The impact of green credit guidelines on green lending and environmental outcomes Evidence from Chinese banks.pdf
```

### 2025-12 — Batch 4 of 5  (16 papers)

```
CONTEXT — Synapse NBS ingestion · 2025-12 · Batch 4/5 (16 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2025-12 folder. Run
the scoped steps below on EXACTLY the 16 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2025-12/pdfs/.

PRECONDITION: the one-time PREP block for 2025-12 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2025-12/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2025-12/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 16 PDFs in → 16 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 5 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2025-12.

THIS BATCH — 16 PDFs (process exactly these, ignore all others):
Liu 2026 Financial value of nature coastal housing markets, mangroves, and climate resilience.pdf
Lodge 2025 From Paralysis to Publicization How Victims of the UK Post Office Horizon IT Scandal Experienced and Confronted Organizational Harm.pdf
Lovo 2026 Who should pay for ESG ratings.pdf
Maiolini 2025 The Persuasive Power of Signals How Narratives, Fundraising Model, and Number of Borrowers Drive Success in Lending-Based Prosocial Crowdfunding.pdf
McKie 2025 The Role of Information, Rewards, and Convenience in Take-Back Programs for Clothing.pdf
Milinski 2025 Climate extreme events and climate change are enforced by extortionate freeriders overloading those who mitigate – An economic experiment.pdf
Nair 2025 Stakeholder Political Ideology, Purpose of Business Beliefs, and Responses to CEO Activism Introducing an Asymmetry Model.pdf
Nguyen 2025 Engaged and Responsible Scholarship Why Qualitative Researchers Should Not Embrace GenAI.pdf
Nielsen 2025 Impact, Interrupted How and When Thwarted Prosocial Impact Undermines Employee Performance and Retention.pdf
Nissilä 2026 When the Time Never Comes Temporal Mobilization and Temporal Tensions in a Nascent Solar Energy Field.pdf
Papier 2025 Forced Labor in Labor Supply Chains Contracting and Information Asymmetry.pdf
Rao 2026 Who’s Afraid of the Minimum Wage Measuring the Impacts on Independent Businesses Using Matched U.S. Tax Returns.pdf
Rosenfeld 2025 Local development based on non-timber forest products Revisiting the case of São Francisco do Iratapuru in the Brazilian Amazon.pdf
Safaei 2026 No News About Climate Action is Good News for Low-Polluting Firms.pdf
Savini 2025 Socio-ecological inequalities in housing consumption How income, urban form, and tenure drive carbon footprints.pdf
Serra 2025 Climate change mitigation and green energy investment A stock-flow consistent model.pdf
```

### 2025-12 — Batch 5 of 5  (16 papers)

```
CONTEXT — Synapse NBS ingestion · 2025-12 · Batch 5/5 (16 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2025-12 folder. Run
the scoped steps below on EXACTLY the 16 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2025-12/pdfs/.

PRECONDITION: the one-time PREP block for 2025-12 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2025-12/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2025-12/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 16 PDFs in → 16 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 5 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2025-12.

THIS BATCH — 16 PDFs (process exactly these, ignore all others):
Soboleva 2025 Agent-based insight into eco-choices Simulating the fast fashion shift.pdf
Soto-Oñate 2025 Post-growth meets polycentric governance Toward an interdisciplinary research program.pdf
Spriha 2025 How Employees Who Have Made Upward Social Class Transitions Get Heard in the Workplace.pdf
Stangenberg 2025 The information value of energy labels Evidence from the Dutch residential housing market.pdf
Thomas 2025 Decommodifying cacao matchmaking between producers and buyers of fine flavour cacao from Peru.pdf
Viale 2026 “Taking Wendake Beyond Wendake” Economic Development and Legal Tenacity in the Wendat Community.pdf
Viallon 2025 Resource regimes and the success of local renewable energy projects.pdf
Villani 2025 The grey shades of green jobs Unpacking the occupational approach to green employment.pdf
Whittaker 2025 From grand challenges to bold solutions Investor perspectives on financing urban climate change adaptation.pdf
Willis 2025 Biodiversity finance What has been achieved and where is it heading.pdf
Wu 2026 Activism risk and corporate self-regulation Investigating how anti-SLAPP laws impact firms institutional corporate social performance.pdf
ZHI 2025 Do Nature-Loving CEOs Make the World Greener.pdf
Zatsarnaja 2025 Nudging grid-friendly electric vehicle charging Different shades of social framing and the power of individual factors.pdf
Zhang 2026 Transparency and divestment the impact of a public database about insurers’ carbon-intensive investments on their portfolio choices.pdf
Zhou 2026 Biodiversity co-benefits in carbon markets Evidence from voluntary offset projects.pdf
Zhu 2025 Toxic neighbors E -waste dumps and the decline of social capital.pdf
```

## FINALIZE — run ONCE for 2025-12, after the LAST batch (Batch 5)

This is the tail of `/synapse-ingest` (Steps 4–4.5). Deterministic + network
checks; token-light. It does NOT commit — PUBLISH does the single release commit.

```bash
cd /Users/tangbinqi/Claude/Synapse

python3 tools/build_index.py          # rebuild every derived view from notes/
python3 tools/export_csv.py
python3 tools/export_bibtex.py

python3 tools/validate_note.py notes/*.md     # full-corpus regression (all must pass)
python3 tools/verify_metadata.py              # Tier 2 gate: CrossRef cross-check, exit 0

sqlite3 index/synapse.db "SELECT COUNT(*) FROM papers;"   # expect 352
sqlite3 index/synapse.db "SELECT topic, COUNT(*) FROM topics GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
```

If validate or verify_metadata is not clean, fix before PUBLISH. The 3
doi-missing papers were never ingested, so they raise no MISMATCH here.

## PUBLISH — run ONCE for 2025-12, after FINALIZE is clean

This is the "…then commit and publish as a GitHub Release" half of the AMJ
one-liner. It mirrors exactly what every prior issue did (v0.15.0–v0.19.0):
ONE commit bundling notes + index + manifest + version bump, then tag, push,
GitHub Release. Token-light; a fresh session is fine.

Target: **v0.20.0** · library **270 → 352** (82 NBS-2025-12 notes)
(Counts assume 2025-12 is released before the other issue. If you flip the order,
swap the numbers. Use the ACTUAL note count from FINALIZE if any paper STOPped.)

```bash
cd /Users/tangbinqi/Claude/Synapse

# 1. (optional) Aggregate this issue's audit verdicts for the release notes:
ls incoming/_audits/nbs-2025-12-*.audit.json | wc -l        # notes audited
grep -ho '"verdict": *"[A-Z]*"' incoming/_audits/nbs-2025-12-*.audit.json | sort | uniq -c
```

2. **Version bump** (judgment step — describe THIS batch's results):
   - `CITATION.cff`: set `version: "0.20.0"`, `date-released: "<today>"`,
     and extend the `abstract` with one sentence on this batch (82 notes,
     library 270→352, the Layer-1/Layer-2 tally, any flagged IDs).
   - `README.md`: bump the version string + BibTeX `version`, update the note
     count, add a release-notes bullet for v0.20.0.
   - `AGENTS.md`: update the "270 curated notes" count if you keep it current.

3. **One commit + tag + push** (the established recipe):
```bash
git add notes/ index/ library/NBS/2025-12/manifest.tsv tools/prepare_paper.py \
        CITATION.cff README.md AGENTS.md
git commit -m "v0.20.0: NBS 2025-12 (82 notes, library 270 → 352)"
git tag v0.20.0
git push origin main --tags
```

4. **GitHub Release** (same shape as every prior issue):
```bash
gh release create v0.20.0 \
  --title "v0.20.0 — NBS 2025-12 (82 notes, library 270 → 352)" \
  --notes "Adds 82 NBS 2025-12 notes (library 270 → 352).
Three gates clean: populate_manifest (vol/issue/pages backfilled), lint_manifests
(structurally clean), verify_metadata (352/352 MATCH, exit 0).
Layer 1 / Layer 2 audit tally: <paste from step 1>. Flagged: <none | ids>.
Analyzed with Claude Opus 4.8."
```

After this, 2025-12 is fully published — identical end state to running the AMJ
one-liner, just reached through PREP → 5 batches → FINALIZE → PUBLISH.


### 2025-12 — doi-missing papers (NOT in any batch; later cleanup pass)

- Bernard 2026 — `Bernard 2026 Climate change and individual behavior.pdf`
- Giglio 2026 — `Giglio 2026 Biodiversity risk.pdf`
- Leippold 2026 — `Leippold 2026 Firm-level green innovation beyond patents.pdf`

# ════════════════  NBS 2026-01  ·  103 papers  ·  10 batches  ·  v0.21.0  ════════════════

Batch sizes: [11, 11, 11, 10, 10, 10, 10, 10, 10, 10]  (sum 103).  Release target: v0.21.0, library 352 → 455.

## PREP — run ONCE for 2026-01, before Batch 1 (do NOT skip)

Manifest-level + provenance setup. Not a batch; run once, confirm green, then run
the batch prompts in any order. Re-running is harmless.

```bash
cd /Users/tangbinqi/Claude/Synapse

# 1. Provenance: stamp the model you are ACTUALLY analyzing with into every bundle.
#    Today that is Opus 4.8. (See MODEL POLICY at the top — if a stronger Anthropic
#    model has shipped, put ITS name here instead.)
python3 - <<'PY'
import pathlib
p = pathlib.Path("tools/prepare_paper.py"); t = p.read_text()
import re
t2 = re.sub(r'EXTRACTION_MODEL = "claude-opus-4-\d+"',
            'EXTRACTION_MODEL = "claude-opus-4-8"', t)
if t2 != t:
    p.write_text(t2); print("EXTRACTION_MODEL -> claude-opus-4-8")
elif 'EXTRACTION_MODEL = "claude-opus-4-8"' in t:
    print("EXTRACTION_MODEL already claude-opus-4-8 — no change (idempotent)")
else:
    raise SystemExit("EXTRACTION_MODEL constant not found — inspect prepare_paper.py line 42 by hand")
PY

# 2. Tier 3 gate: backfill volume/issue/pages + auto-correct years from CrossRef.
python3 tools/populate_manifest.py library/NBS/2026-01/manifest.tsv --apply --fix-year
#    Exit 1 is EXPECTED on filename-derived manifests: it only means "TITLE differs"
#    warnings (filenames drop ':' and '?'). Step 3 fixes those. What matters here:
#    0 JOURNAL mismatches, and only small (+/-1) year auto-corrections.

# 3. Canonicalize titles from CrossRef. Filename-derived titles are lossy (no ':'
#    or '?'), which would fail the Step-4.5 verify_metadata gate. This upgrades each
#    DOI row's title to the CrossRef canonical form. SAFE: a row is upgraded only
#    when CrossRef's title is highly similar to the current one; a low-similarity
#    row is FLAGGED (possible wrong DOI), never silently changed. Dry-run, eyeball
#    flags (want 0), then --apply.
python3 tools/canonicalize_titles.py library/NBS/2026-01/manifest.tsv            # dry-run
python3 tools/canonicalize_titles.py library/NBS/2026-01/manifest.tsv --apply    # write

# 4. Structural lint gate. Clean for every DOI row. NOTE: doi-missing rows with a
#    filename year-typo or a non-Latin name may STAY flagged — that is fine; they
#    are excluded from the batches and deferred to the DOI-cleanup pass. A real
#    CrossRef compound-surname mismatch on a DOI row goes in KNOWN_COMPOUND_SURNAMES
#    (tools/lint_manifests.py) with a dated rationale, then re-lint.
python3 tools/lint_manifests.py --manifest library/NBS/2026-01/manifest.tsv

# 5. Bookkeeping: mark DOI-less rows status=doi-missing (excluded from all batches).
python3 - <<'PY'
import csv, pathlib
p = pathlib.Path("library/NBS/2026-01/manifest.tsv")
rows = list(csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"))
cols = list(rows[0].keys()); n = 0
for r in rows:
    if not (r.get("doi") or "").strip() and r.get("status") != "doi-missing":
        r["status"] = "doi-missing"; n += 1
with p.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter="\t"); w.writeheader(); w.writerows(rows)
print(f"marked {n} rows doi-missing")
PY
```

Proceed to batches once steps 2–4 are green (lint may keep doi-missing rows
flagged — that's expected). The 18 doi-missing papers for 2026-01 are listed
at the bottom of this section.

### 2026-01 — Batch 1 of 10  (11 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 1/10 (11 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 11 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 11 PDFs in → 11 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 11 PDFs (process exactly these, ignore all others):
ALLCOTT 2026 An Economic View of Corporate Social Impact.pdf
Achar 2026 From Stigma to Support “Black-Owned” Labels and Expertise Stereotypes in Cannabis and Psychedelics Markets.pdf
Allen 2026 Thinking-Being With a Garden Developing Ecocentric Ethics for Sustainable Organising.pdf
Bazdah 2025 Making Sense of Conflicts During Management Consulting Missions A Values-in-Practice Approach.pdf
Bhattacharjee 2025 Perceived Air Pollution and Innovative Work Behavior An Empirical Examination Based on Conservation of Resources Theory.pdf
Boeckx 2025 Green Pressure, Lean Measures Unveiling Corporate Downsizing Within the European Union Emissions Trading System.pdf
Boh 2026 Digital Resilience for the Climate Crisis A Multi-Perspective Analysis.pdf
Boroomand 2026 Business and management research on societal wellbeing a historic, multi-journal and large language model analysis of the UN’s Sustainable Development Goals.pdf
Butticè 2026 Sustainability-Oriented Institutions and the Success of Green Reward-Based Crowdfunding Campaigns.pdf
Cakanlar 2026 The politics of impact How political ideology shapes perceptions of the environmental impact of individual actions.pdf
Cao 2025 Detecting Gender Stereotype Biases Against Women Entrepreneurs in Large Language Models.pdf
```

### 2026-01 — Batch 2 of 10  (11 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 2/10 (11 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 11 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 11 PDFs in → 11 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 11 PDFs (process exactly these, ignore all others):
Castaldi 2026 European regions transitioning to green markets the role of related capabilities and public procurement policies.pdf
Chavan 2025 Can Purpose and Professional Advancement Coexist Review of Make It Meaningful How to Find Purpose in Life and Work by Debbie Haski-Leventhal.pdf
Chen 2026 Corporate Social Responsibility and Employee Information Sharing.pdf
Chindondondo 2025 Social Sustainability Practice The Interplay between State and Community Logics.pdf
Chowdhury 2026 Marginalized Stakeholder Theory A Normative Foundation for Decolonization.pdf
Ciulla 2026 Careless or Clueless the Lost Promise of Facebook.pdf
Coria 2000 Innovation under dual policies The impact of R&D subsidies and emissions trading on green patenting in Sweden.pdf
Cuny 1971 Political costs and strategic corporate communication.pdf
Discetti 2025 Re-enchanting Consumer Ethics Through Embodied Relationality An Ethnographic Approach to the Attitude-Behaviour Gap.pdf
Donaldson 2026 When are Customer Boycotts Permissible.pdf
Dudink 2025 A ‘Sticky’ Past The Viscosity of Organizational Memory in Navigating Ethical Change.pdf
```

### 2026-01 — Batch 3 of 10  (11 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 3/10 (11 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 11 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 11 PDFs in → 11 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 11 PDFs (process exactly these, ignore all others):
Dueñas 2057 The effect of extreme heat on economic growth Evidence from Latin America..pdf
Duguay 2023 Mandatory carbon disclosure and new business creation.pdf
Dumas 2025 The Business–Social Paradox of ESG Investing Responding to Persistent Tensions over Time.pdf
Edirisinghe 2025 What Happens After Whistleblowing A Systematic Literature Review of the Post-whistleblowing Phase.pdf
Elgaaied-Gambier 2026 Reframing Sustainable Consumption Toward an Ethical Dilemma Perspective.pdf
Elmachtoub 2026 Fair Fares for Vehicle Sharing Systems.pdf
Estey 2025 Toward a typology of boundaries in crisis management.pdf
Etzion 2026 Good Data, Good Questions Leveraging Comprehensive, Direct-Observation Data Sets for Impactful Research on Organizations and the Environment.pdf
Fisher 2025 Competing With Smart Machines The dark side of ‘conjoined agency’ in contemporary organizations.pdf
Gagliardi 2025 Entrepreneurship and Gentrification.pdf
Geiger 2026 “If I Accomplish Nothing Else but Hope, That Will be Enough” The Ethics and Morality of Market-Based Hope in Illness Entrepreneurship.pdf
```

### 2026-01 — Batch 4 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 4/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Giarratana 2026 Nourishing sustainability innovation Scientific trajectories in industrial protein research.pdf
Gibson 2025 The Crisis of Dignity at Work Dehumanization during Digital Transformation, Societal Upheaval, and Workforce Uncertainty.pdf
Gipper 2025 Carbon accounting quality Measurement and the role of assurance.pdf
Gond 2025 Making Better Uses of Classics Evaluating Critically the Legacy of Howard R. Bowen’s 1953 Social Responsibilities of the Businessman (1953–2023).pdf
Grisold 2025 Guardrails for Human-AI Ecologies Norm-Based Coordination and Design for Predictability.pdf
Groutsis 2026 Whose Justice A Turn to Relational Equality from the Experiences of Ethno-Racially Marginalised Women in Australian Workplaces.pdf
Guo 2025 Nexus Effect Unraveling the Impact of Political Patronage Connections on Corporate Investment.pdf
Hansen 2026 Green industrial policy and latecomer catch-up A missed green window of opportunity for domestic solar PV module manufacturers in Indonesia.pdf
Harvey 2025 Enacting responsible leadership in cross-sector partnerships A dynamic choreography of power.pdf
He 2025 Performing Diversity Navigating Tensions, Identity Threats, and Self-Instrumentalization in Applicant Diversity Statements.pdf
```

### 2026-01 — Batch 5 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 5/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Hetemi 2026 Knowledge ecosystem emergence Organizing participation, identity, and actorhood to bridge the governance void.pdf
Hirschmann 2026 Trademarks and the innovativeness of social enterprises.pdf
Hossain 2026 Rewarding Ethical Leadership Corporate LGBTQ+ Friendliness and CEO Compensation.pdf
Hughes 2026 Problematizing the role of artificial intelligence in hiring and organizational inequalities A multidisciplinary review.pdf
Jaufenthaler 2026 When Family Firm Reputation Backfires The Role of Controllability in Consumer Responses to Negative CSR Incidents.pdf
Jiang 2026 Symbol or Substance Environmental Protection and International Expansion in Emerging Market Multinationals.pdf
Jue-Rajasingh 2025 Second-Order Knowledge Intermediaries and Multi-Country Entrepreneurial Entry into a Nascent Industry.pdf
Juntunen 2022 Contextualizing policy mixes – A configurational study on rapid transitions.pdf
Kanze 2025 When Do Gender-Diverse Teams Engage More Investors Evidence of Threshold Alignment Benefits at Techstars.pdf
Kapteina 2026 Why Do Companies Engage in the Creation of Private Governance A Systematic Literature Review and Research Agenda.pdf
```

### 2026-01 — Batch 6 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 6/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Kherrazi 2025 Organizing Open Social Innovation for Grand Challenges Unlocking the Potential of Open Spaces.pdf
Kodeih 2025 Social Purpose Formation and Evolution in Nonprofit Organizations.pdf
Krammer 2025 The Empire’s New Clothes A Review of “Butler to the World How Britain Became the Servant of Tycoons, Tax Dodgers, Kleptocrats and Criminals” by Oliver Bullough.pdf
Kuhn 2026 Should We Talk About the News Coworker Discussion and Affective Well-Being in a Polarized Society.pdf
Lee 2026 Changing beliefs or changing behavior Understanding the belief-to-behavior process and intervening to curb the impact of misinformation.pdf
Leonardi 2026 Knowing Enough to Be Dangerous The Problem of “Artificial Certainty” for Expert Authority When Using AI for Decision Making and Planning.pdf
Lohmeyer 2026 Kafka and Organization Studies.pdf
Lu 2025 Market Demand, Competition for Knowledge Workers, and Impact on Invention Evidence from Electric Vehicle Technologies.pdf
Luo 2026 Stakeholder Satisfaction Interdependencies in 10-K Reports.pdf
MAGGIO 2026 Second Chance Life with Less Student Debt.pdf
```

### 2026-01 — Batch 7 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 7/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Maile 2025 Tech Ethics, Organizational Values, and Ethical Work Insights from a Qualitative Study of Five UK-Based Digital Technology Businesses.pdf
Mandray 2025 Distinguishing Three Concepts of the Societal Good The Managerial Case for Adopting the Thomistic Concept of the Common Good.pdf
Meister 2026 How Do Entrepreneurs Form Social Business Opportunity Beliefs An Opportunity Actualization Perspective.pdf
Nabity-Grover 2025 Social Media and Political Affiliation How Expressing Hot-Button Opinions Affects Raters’ Assessments of Job Applicants.pdf
Ng 2025 Ethical Leadership in Climate Action Navigating National Government Intervention, Financial Constraints, and Corporate Decarbonization.pdf
PEDERSEN 2026 Carbon Pricing versus Green Finance.pdf
PIKULINA 2026 Subtle Discrimination.pdf
Pan 2025 Carbon Emissions Reduction or ‘Relocation’ A Study on the Corporate Response to Climate Change and the Role of Environmental Law.pdf
Pawirosumarto 2026 Datafied Selves at Work Ethical Boundaries of Surveillance in People Analytics.pdf
Peiro 2025 Mapping Heterotopia Enjoyment as practice in two alternative spaces.pdf
```

### 2026-01 — Batch 8 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 8/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Pflitsch 2026 Rethinking the Third Mission Organizing dissonance in transformative universities.pdf
Pollach 2025 Sustaining Unsustainability The Legitimation Paradox of Unsustainable Companies.pdf
Raimi 2025 Judgmental Bot Conversational Agents in Online Mental Health Screening.pdf
Reich 2025 Homelessness-based impact hiring and consumers’ contagion concerns.pdf
Ren 2025 Earnings Pressure and Firms’ ESG Performance Do Executive Environmental Experience and MBA Experience Matter.pdf
Rice 2025 My Oppressive Past- and Present-Day Vulnerability Understanding How and When Authoritarian Leadership Adversely Impacts Black Employees at Work.pdf
Rong 2026 The data-based power of big-tech multinational enterprises.pdf
Roth 2026 Reimagining ESG A Tetralemma Approach to Multifunctional Sustainability Reporting.pdf
Rubel-Lifschitz 2026 Ethical Decision-Making in Organizations in Times of Conflict The Role of Personal Values and Collective Victimhood.pdf
STARKS 2026 Corporate ESG Profiles and Investor Horizons.pdf
```

### 2026-01 — Batch 9 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 9/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Schmelter 2026 Certified Sustainability Third-Party Certification of Sustainable Ventures and its Relationship to Venture Funding.pdf
Shantz 2025 Degrowth and Organization Studies.pdf
Silva 2026 Managing multi-stakeholder co-creation to address grand challenges The role of paradox management capabilities.pdf
Skiadopoulos 2025 Climate-Triggered Institutional Price Pressure Does It Affect Firms’ Cost of Equity.pdf
Stephan 2026 Institutions and social entrepreneurship a hierarchy of institutions to revisit institutional voids, support, and configurations.pdf
Sun 2026 Integrating Drama Performance Methods with Business Ethics Education A Mixed-Methods Approach.pdf
Sun 2026 The Power of Retail Investors The Effect of Online Interactions Over Environmental Issues on Corporate Greenwashing.pdf
Tambe 2026 ESG Controversies and Non-Audit Service Fees European Evidence.pdf
Tlaiss 2026 Muddling Through During the Pre-Liminal Period Women’s Transition to Entrepreneurship in the Midst of a Compound National Crisis.pdf
Valor 2025 Can Compassion Appeals Change the World A Critical Review and Reconceptualization.pdf
```

### 2026-01 — Batch 10 of 10  (10 papers)

```
CONTEXT — Synapse NBS ingestion · 2026-01 · Batch 10/10 (10 papers)
Project root: /Users/tangbinqi/Claude/Synapse
MODEL: this session MUST run on the current Anthropic SOTA — today, Claude Opus
4.8. Set it with  /model claude-opus-4-8[1m]  before you start. Subagents you
dispatch inherit this model — it is what actually analyzes the papers. (If a
stronger Anthropic model has since shipped, use it, and make sure PREP step 1
stamped that same name into prepare_paper.py.)

This is ONE shard of a manually-batched /synapse-ingest run. Do NOT invoke the
/synapse-ingest slash command — it would process the entire 2026-01 folder. Run
the scoped steps below on EXACTLY the 10 PDFs listed under THIS BATCH, and
ignore every other PDF in library/NBS/2026-01/pdfs/.

PRECONDITION: the one-time PREP block for 2026-01 has already run and is green.
Do NOT run populate_manifest or lint here. If you cannot confirm PREP ran, stop.

STEP A — text + bundle (deterministic, fast, per file). For each filename under
THIS BATCH, run, with the filename quoted exactly:
    python3 tools/pdf_to_text.py  "library/NBS/2026-01/pdfs/<filename>"
    python3 tools/prepare_paper.py "library/NBS/2026-01/pdfs/<filename>"
prepare_paper.py prints the paper_id and bundle path — collect them. If a file
has no matching manifest row or prepare_paper errors, stop and show me.

STEP B — extract (one subagent per paper; waves of MAX 3 concurrent — higher
fan-out has triggered socket-close cascades on this repo). For each paper_id,
dispatch an Agent subtask using the canonical Step-2 template in
.claude/commands/synapse-ingest.md ("You are extracting a single paper"). Each:
  • reads CLAUDE.md (5 hard rules), docs/extraction-prompt.md, index/topics.json,
    incoming/_bundles/<paper_id>.bundle.txt  (bib block is trusted)
  • writes one note with Write to notes/<paper_id>.md
  • runs, recording exit code + output:
        python3 tools/audit_note.py    notes/<paper_id>.md --flag
        python3 tools/validate_note.py notes/<paper_id>.md --flag
  • reports exactly one of OK / AUDIT_FAIL / FAIL / STOP (<150 words; quote
    flagged anchors/verdicts verbatim — never invent content to pass a gate)

STEP C — aggregate. One line per paper: OK/AUDIT_FAIL/FAIL/STOP <paper_id>.
Cross-check 10 PDFs in → 10 notes out. If ≥3 fail for the SAME root cause,
STOP and ask me (systemic, not per-note). Keep this batch's tally — PUBLISH
needs the aggregate across all 10 batches for the release notes.

Do NOT build the index, run verify_metadata, or commit here. Those are FINALIZE
and PUBLISH, run once after the LAST batch of 2026-01.

THIS BATCH — 10 PDFs (process exactly these, ignore all others):
Vaujany 2025 Rethinking Responsibility in the Digital Age A Narrative Approach.pdf
Walker 2026 Indigenous employees’ experiences of work An interdisciplinary review.pdf
Wan 2025 Does central supervision mitigate border pollution Evidence from the national specially monitored firms program in China.pdf
Wang 2026 Bridging the Gap, Building Trust Structural Holes as Dual Forces in Corporate Philanthropy.pdf
Wang 2026 Who Invests, Who Gets Funded Gender and Racial Bias in LLM-Generated Investment Advice.pdf
Wu 2025 Girls Help Girls The Gender Preference of FOF Managers.pdf
Xiang 2026 Political Tension and MNEs’ Disclosure of Host-Country ESG Activities.pdf
Zhang 2026 Artificial Intelligence and Disability Entrepreneurship Moving the Field Forward.pdf
Zhang 2026 Climate Beliefs and Attitudes and Corporate Tax Savings.pdf
Zheng 2026 Short-term fit, long-term trap The career development lock of low-skilled gig workers.pdf
```

## FINALIZE — run ONCE for 2026-01, after the LAST batch (Batch 10)

This is the tail of `/synapse-ingest` (Steps 4–4.5). Deterministic + network
checks; token-light. It does NOT commit — PUBLISH does the single release commit.

```bash
cd /Users/tangbinqi/Claude/Synapse

python3 tools/build_index.py          # rebuild every derived view from notes/
python3 tools/export_csv.py
python3 tools/export_bibtex.py

python3 tools/validate_note.py notes/*.md     # full-corpus regression (all must pass)
python3 tools/verify_metadata.py              # Tier 2 gate: CrossRef cross-check, exit 0

sqlite3 index/synapse.db "SELECT COUNT(*) FROM papers;"   # expect 455
sqlite3 index/synapse.db "SELECT topic, COUNT(*) FROM topics GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
```

If validate or verify_metadata is not clean, fix before PUBLISH. The 18
doi-missing papers were never ingested, so they raise no MISMATCH here.

## PUBLISH — run ONCE for 2026-01, after FINALIZE is clean

This is the "…then commit and publish as a GitHub Release" half of the AMJ
one-liner. It mirrors exactly what every prior issue did (v0.15.0–v0.19.0):
ONE commit bundling notes + index + manifest + version bump, then tag, push,
GitHub Release. Token-light; a fresh session is fine.

Target: **v0.21.0** · library **352 → 455** (103 NBS-2026-01 notes)
(Counts assume 2026-01 is released before the other issue. If you flip the order,
swap the numbers. Use the ACTUAL note count from FINALIZE if any paper STOPped.)

```bash
cd /Users/tangbinqi/Claude/Synapse

# 1. (optional) Aggregate this issue's audit verdicts for the release notes:
ls incoming/_audits/nbs-2026-01-*.audit.json | wc -l        # notes audited
grep -ho '"verdict": *"[A-Z]*"' incoming/_audits/nbs-2026-01-*.audit.json | sort | uniq -c
```

2. **Version bump** (judgment step — describe THIS batch's results):
   - `CITATION.cff`: set `version: "0.21.0"`, `date-released: "<today>"`,
     and extend the `abstract` with one sentence on this batch (103 notes,
     library 352→455, the Layer-1/Layer-2 tally, any flagged IDs).
   - `README.md`: bump the version string + BibTeX `version`, update the note
     count, add a release-notes bullet for v0.21.0.
   - `AGENTS.md`: update the "352 curated notes" count if you keep it current.

3. **One commit + tag + push** (the established recipe):
```bash
git add notes/ index/ library/NBS/2026-01/manifest.tsv tools/prepare_paper.py \
        CITATION.cff README.md AGENTS.md
git commit -m "v0.21.0: NBS 2026-01 (103 notes, library 352 → 455)"
git tag v0.21.0
git push origin main --tags
```

4. **GitHub Release** (same shape as every prior issue):
```bash
gh release create v0.21.0 \
  --title "v0.21.0 — NBS 2026-01 (103 notes, library 352 → 455)" \
  --notes "Adds 103 NBS 2026-01 notes (library 352 → 455).
Three gates clean: populate_manifest (vol/issue/pages backfilled), lint_manifests
(structurally clean), verify_metadata (455/455 MATCH, exit 0).
Layer 1 / Layer 2 audit tally: <paste from step 1>. Flagged: <none | ids>.
Analyzed with Claude Opus 4.8."
```

After this, 2026-01 is fully published — identical end state to running the AMJ
one-liner, just reached through PREP → 10 batches → FINALIZE → PUBLISH.


### 2026-01 — doi-missing papers (NOT in any batch; later cleanup pass)

- Brown 2025 — `Brown 2025 Editor’s CommentsBeyond Green IT From Digital Sustainability to Responsible Technology (2).pdf`
- Comi 2025 — `Comi 2025 Media Review How Can We Make Better Futures.pdf`
- Daskalaki 2026 — `Daskalaki 2026 Media Review The ‘Objective Necessity’ of Resistance Corporeal fragility against algocracy.pdf`
- Escribe 2050 — `Escribe 2050 Do sufficiency consumption changes drive emissions down A production network approach.pdf`
- Gibert 2013 — `Gibert 2013 The living lab and the cursed catalyst Navigating the legitimacy challenges of innovation intermediaries for sustainable innovation.pdf`
- Jemaa 2026 — `Jemaa 2026 Media Review The Invisible Cage as a New Form of Alienation in the Gig Economy.pdf`
- Kwok 1910 — `Kwok 1910 Firm ownership and pollution.pdf`
- Lee 2017 — `Lee 2017 Impact of digital transformation technology adoption on worker wages.pdf`
- Myers 2023 — `Myers 2023 Data, information, and the environment An introduction to this special issue.pdf`
- Nazar 2025 — `Nazar 2025 Media Review The Stigma Matrix.pdf`
- Peñaloza-Pacheco 2023 — `Peñaloza-Pacheco 2023 The non-green effects of going green Local environmental and economic consequences of lithium extraction in Chile.pdf`
- Sarkar 2026 — `Sarkar 2026 Media Review Redefining Management.pdf`
- Sawhney 2026 — `Sawhney 2026 Case Study When High-Tech Beauty Marketing Harms Teen Health.pdf`
- Strøm-Andersen 2020 — `Strøm-Andersen 2020 Navigating sustainability paradoxes Unveiling the dynamics of transformative change in the food industry.pdf`
- Thảo 2021 — `Thảo 2021 External search for specialized knowledge and green new product development speed A dual mediation mechanism and moderating role of absorptive capacity.pdf`
- Tian 2020 — `Tian 2020 Heterogeneous responses to carbon pricing Firm-level evidence from Beijing emissions trading scheme.pdf`
- Wunder 2000 — `Wunder 2000 Harvesting or nurturing Corporate venture capital and startup green innovation.pdf`
- Yu 2016 — `Yu 2016 Water stress and industrial firm productivity.pdf`
