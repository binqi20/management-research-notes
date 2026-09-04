# Ingestion & Release Runbook (vendor-neutral)

This is the portable, step-by-step procedure for turning one journal **issue** of
PDFs into committed, audited Synapse notes, and for publishing a completed
**volume**. It is written for any agent runtime (Codex, Claude Code, a custom SDK)
— the sequence, gates, and stop conditions are the same regardless of who runs it.

Claude Code users can invoke the same sequence via the `/synapse-ingest` slash
command; that command is a thin wrapper over the steps below. Codex and other
runtimes should follow this document directly.

Read first: [`AGENTS.md`](../AGENTS.md) (the 7 rules), then
[`extraction-prompt.md`](extraction-prompt.md) and
[`audit-rubric.md`](audit-rubric.md). The manifest is the trusted bibliographic
source; three CrossRef gates bracket extraction to catch hand-entry errors.

---

## Scope of one run

- **Unit of work = one issue.** Ingest and audit a single
  `library/<source>/<issue>/` at a time.
- **Unit of release = one issue** (policy updated 2026-07-10; matches the
  v0.4–v0.19 precedent). When an issue's analysis, audit, and gates are all
  clean, publish that issue: commit, push, tag, GitHub Release. Publication
  still requires the user's explicit go-ahead in the conversation that runs it.
- **Parallel-agent cap = 6.** At most 6 active extraction agents *or* 6 active
  audit agents per wave. Never mix extraction and audit in the same wave. On any
  cap/timeout/coordination trouble, fall back 6 → 5 → 3 → serial. See
  [`AGENTS.md` §4.1](../AGENTS.md).

## Runtime modes

Two equivalent ways to run Steps 2–2.5, sharing the same caps, write scopes, and
independence rules. Pick by runtime; never mix extraction and audit in one wave
in either mode.

- **Wave mode (Codex).** The operator session dispatches ≤6 extraction workers,
  waits for all to return, closes them, then dispatches ≤6 audit workers as a
  separate wave. Repeat per wave until the issue is covered. This is the mode the
  worked ledgers under `incoming/_ledgers/` record.
- **Chunked two-phase mode (Claude Code / code-orchestrated runtimes).** Split the
  issue into chunks of ~4–5 papers. For each chunk: Phase E runs the chunk's
  extraction agents concurrently **to completion** (barrier), then Phase A runs
  fresh audit agents for the chunk's validated notes concurrently to completion.
  Chunk k's audits must finish before chunk k+1's extraction starts (no
  cross-chunk overlap — a mixed 9–10-agent burst is the historical rate-limit
  failure). Root-cause tallies accumulate across chunks; ≥3 same-cause failures
  aborts the run between phases. Extraction agents may self-fix a mechanical
  validator failure **once** (anchor re-selection, never invented content) and
  must report the pre-fix cause either way.

In both modes: extraction agents write only `notes/<paper_id>.md`; audit agents
write only `incoming/_audits/<paper_id>.layer2.json`; **subagents never run git
commands** (staging, committing, tagging, and pushing are parent-session actions
only); the parent session verifies expected files **on disk** (never trusting
agent self-reports), assembles official audits, makes repairs, and rebuilds
derived indexes.

---

## Preconditions (stop if any fails)

1. Folder resolves to `library/<source>/<issue>/pdfs/` with a sibling
   `manifest.tsv` (header: `title, first_author_last, year, saved_filename, doi,
   status, …`).
2. `docs/extraction-prompt.md` and `index/topics.json` exist.
3. `pdftotext` (poppler) is on `PATH`.

---

## Step 0 — Populate the manifest from CrossRef (Tier 3, mandatory)

```
python tools/populate_manifest.py library/<source>/<issue>/manifest.tsv --apply --fix-year
```
Backfills `volume/issue/pages` and auto-corrects the year to CrossRef
`published-print` (the APA-7 issue year). **Gate:** stop and show the user any
unexpected title/journal warning before proceeding.

## Step 0.5 — Structural manifest lint (mandatory)

```
python tools/lint_manifests.py --manifest library/<source>/<issue>/manifest.tsv
```
Catches the "D'Amico bug class" (full given+family name captured in
`first_author_last`) and malformed year/DOI/filename rows. **Gate:** do not
proceed until the linter exits 0, or every remaining flag is a documented
allowlisted false positive.

## Step 1 — Prepare extraction bundles (deterministic)

```
python tools/ingest_batch.py library/<source>/<issue>/pdfs
```
Runs `pdf_to_text.py` then `prepare_paper.py` per PDF, emitting one
`incoming/_bundles/<paper_id>.bundle.txt` each. Bundles are stamped
`extraction_version: v3`. **Gate:** any `failed` entry → stop and show the user.

## Step 2 — Extraction wave (≤6 agents; write notes only)

Each agent reads, in order: `AGENTS.md` → `docs/extraction-prompt.md` →
`index/topics.json` → its `incoming/_bundles/<paper_id>.bundle.txt`; writes exactly
one `notes/<paper_id>.md`; then self-validates:
```
python tools/validate_note.py notes/<paper_id>.md --flag
```
Each agent returns **OK / FAIL / STOP**. Extraction agents must **not** run the
Layer 2 audit. v3 notes carry 11 body sections (Abstract, Research Question,
Hypotheses / Propositions, Mechanism Process, Data & Measures, Key Findings,
Theoretical Contribution, Practical Implication, Limitations, Future Research, APA)
and 10 evidence anchors for empirical papers.

*Two-column anchor recovery:* if Layer 1 fails on "anchors not contiguous in the
extracted text," `grep` the candidate phrase in `library/<source>/<issue>/text/…`
and pick a shorter intra-line substring (see the extraction prompt's two-column
guidance).

## Step 2.5 — Independent audit wave (≤6 agents; separate wave)

Dispatch fresh auditor agents that never see the extraction agent's reasoning.
Each auditor's preferred input is the output of
`python tools/audit_note.py notes/<paper_id>.md --prompt-only` — a single
self-contained prompt holding the current rubric, the note body, and the
**anchor-aware fitted PDF text**, so what the auditor reads is exactly what the
assembled report's `audit_context` records. (Reading the rubric + note + raw
text file directly is a legacy fallback; on long papers it diverges from the
recorded fitting metadata.) Each auditor writes
`incoming/_audits/<paper_id>.layer2.json` with a `provenance` block
(`paper_id, note_sha256, text_sha256, rubric_version, auditor_model, generated_at,
dispatch_mode`; `rubric_version` is **v2**). The parent then assembles:
```
python tools/audit_note.py notes/<paper_id>.md \
  --layer-2-json incoming/_audits/<paper_id>.layer2.json --flag
```
For v3 notes the auditor scores **9** prose fields (the original six plus
Hypotheses, Data & Measures, Key Findings). Key Findings is held to the
sign-reversal `CONTRADICTED` rule — a flipped direction fails the audit.

## Step 3 — Aggregate outcomes + systemic-failure gates

Log `OK / AUDIT_FAIL / FAIL / STOP` per paper. **Stop and ask the user** if **≥3
papers fail validation for the same root cause** or **≥3 fail audit for the same
reason** — that signals prompt/vocab/rubric drift, not per-note fixes. Individual
failures: re-extract (cleanest) or narrow the offending prose field, then re-audit.

**Ordering invariant (load-bearing):** assemble the official audit report for
**every** note (`audit_note.py --layer-2-json … --flag`) **before** making any
repair edit. Editing a note changes its `note_sha256`, which invalidates its
existing layer2.json — after a repair, re-assembly is impossible and the note
needs a **fresh** independent audit, not a re-run of the old one.

**PARTIAL policy:** `PARTIAL` verdicts do not fail the audit, but the release
standard is to **repair every repairable PARTIAL before publishing** — narrow the
overstated field to the paper's own scope, revalidate, and re-audit **only the
changed notes** with fresh auditors. Small drift compounds across a literature
review; every recent release shipped at 0 PARTIAL. If ≥3 PARTIALs in one issue
share a root cause, treat it as prompt drift (fix `docs/extraction-prompt.md`),
not as per-note repair work.

## Step 4 — Rebuild derived indexes (sequential, not parallel)

```
python tools/build_index.py        # full reset — applies schema.sql, incl. v3 columns
python tools/export_csv.py
python tools/export_bibtex.py
```
Confirm SQLite = CSV = BibTeX counts and the new issue count.
**Note:** `build_index.py --note <path>` does *not* migrate an existing DB's
columns — after any schema change, run the full `build_index.py` (reset) at least
once so the new columns exist.

## Step 4.5 — Bibliographic integrity (Tier 2, last gate before commit)

```
python tools/verify_metadata.py --quiet --paper-id <paper_id>   # per changed note
```
Checks year, title, journal, volume, issue, pages, authors against CrossRef. **Do
not commit until the changed-note scope returns clean.** Known CrossRef-side false
positives are registered in the tool's known-issues registry. Reserve a
full-library sweep for global metadata changes, not routine issues.

## Step 5 / 6 — Sanity + report

Spot-check `sqlite3 index/synapse.db` counts by `paper_type`/`topic`; report the
folder, per-paper tally, any flagged IDs, and commit-readiness. **Do not commit or
push unless the user explicitly asks.**

---

## Publishing a completed issue

Publish **per issue** (policy updated 2026-07-10): when Steps 0–4.5 are clean for
the issue and the user has asked for publication —

1. **Release hygiene — update from evidence, not memory:**
   - README: new changelog entry in "Faithfulness audit" (verdict counts, repairs,
     record totals), snapshot count, AMJ pilot coverage list + issue-history line,
     paper-type table (from `sqlite3 index/synapse.db "SELECT paper_type, COUNT(*)
     FROM papers GROUP BY 1"`), version-tier sentence, BibTeX `version`.
   - `CITATION.cff`: `version`, `date-released`, a new abstract paragraph, and the
     current-snapshot sentence. Validate with `python3 -c "import yaml;
     yaml.safe_load(open('CITATION.cff'))"`.
   - `AGENTS.md`: §1 counts/coverage, §5 audit state (date + verdict totals),
     §6 citation version.
   - **Version-currency sweep (mandatory, batch-24 lesson):** after updating the
     three files, `grep -n -iE "current|0\.[0-9]+\.[0-9]+" README.md AGENTS.md
     CITATION.cff` and require every line that asserts *currency* — "current",
     "now contains", the version-tier sentence, the §6 citation, `version:`
     fields — to carry THIS release's number. Historical per-release paragraphs
     are exempt. Named line checks alone do not close the class: a "current
     v0.47.0 snapshot" sentence in CITATION.cff's abstract survived nine
     releases and two runtimes because the stale-line check named only the
     README tier sentence and AGENTS §6. Absolute guarantee sentences ("has
     never produced…", "zero…") must be re-read the first time their
     underlying event occurs: batch 28's first-ever round-one CONTRADICTED
     verdict (repaired before publication) left AGENTS §5 asserting the
     library had "never produced" one.
2. **Stage public artifacts only** — the issue's `notes/*.md`, its
   `library/.../manifest.tsv`, the rebuilt `index/` files, and any docs/tooling
   changes. Never `incoming/`, `pdfs/`, `text/`, or worklogs. Verify:
   `git diff --cached --name-only | grep -E "incoming/|pdfs/|/text/"` must be empty.
3. **Commit, push, tag, release:**
   ```
   git commit -m "Add <SOURCE> vol-<V>-no-<I> notes"
   git push origin main
   git tag -a vX.Y.Z -m "vX.Y.Z — <SOURCE> vol-<V>-no-<I>" && git push origin vX.Y.Z
   gh release create vX.Y.Z --title "vX.Y.Z — <SOURCE> vol-<V>-no-<I>" --notes "<verification summary>"
   ```
4. **Verify on the remote:** `git ls-remote origin main refs/tags/vX.Y.Z` — local
   HEAD must equal remote main and the tag must be present. Update the issue
   ledger's `publication_status`.

**Transport:** the remote is **SSH**
(`git@github.com:binqi20/management-research-notes.git`; key registered
2026-07-10) — pushes are fast and reliable for any git client on this machine,
Codex included. Setting up a new machine: generate an ed25519 key, add the
public key at github.com/settings/keys, confirm `ssh -T git@github.com` greets
by name, then `git remote set-url origin git@github.com:…`. Fallback for a
broken transport is the GitHub Git database API (blobs → tree → commit → tag),
then realign local refs to the verified remote. Zenodo archiving of releases is
currently parked (user decision, 2026-07-10).

---

## Backfill batches (v2→v3 augmentation / v1 re-extraction)

The 2026 v3 backfill (user decision 2026-07-12, superseding "going-forward
only") upgrades the pre-v3 corpus **two issues per user-triggered batch**,
newest issue first, so every note eventually carries Hypotheses /
Propositions, Data & Measures, and Key Findings. Two tiers, two treatments:

- **v2 notes → AUGMENT** per [`docs/augmentation-prompt.md`](augmentation-prompt.md):
  an agent ADDS the three sections + three anchors + version bump + provenance
  lines (`augmented_model`, `augmented_at`) and changes nothing else.
  `extraction_model` keeps recording who wrote the six original fields.
  **Named-entity verification (mandatory, batch-25 lesson):** every proper noun
  an augmenter writes into the three NEW sections — database and data-source
  names, scale names, software, panel names — must be grep-verified present in
  the raw extracted text before writing, exactly as anchors are. Batch 25's
  krause note drew the backfill's first UNSUPPORTED verdict when its Data &
  Measures draft named five data sources the paper never mentions; the blind
  audit caught it, but the class is writer-side fabrication and must be
  blocked at the writer. **Per-study attribution (batch-28 lesson):** literal
  membership is necessary, not sufficient. For multi-study papers, verify each
  named entity WITHIN the Methods lines of the study it is attributed to
  (line-level column view), not merely anywhere in the paper. Batch 28's desai
  draft drew the backfill's first CONTRADICTED verdict with participant names,
  a recruitment source, and an item count that all exist in the paper — but
  belong to other studies.
  **`tools/verify_augmentation.py`** (the diff-guard, Layer 0 of the backfill)
  mechanically proves the do-not-touch guarantee against the git HEAD version
  after every augmentation, before the audit.
- **v1 notes → FULL RE-EXTRACTION** with the standard pipeline (they have no
  anchors to preserve; augmenting them cannot reach v3's 10-anchor bar). Same
  `paper_id`, note replaced. Regenerate bundles with
  `ingest_batch.py <pdfs> --model <actual model> --skip-text` — **`--skip-text`
  is mandatory in a backfill**: the extracted text already exists and is the
  baseline every existing anchor, audit hash, and diff-guard comparison rests
  on; regenerating it could silently shift that baseline. Do NOT pass
  `--only-new` (it would skip papers that already have notes).
  `prepare_paper.py` automatically reuses the existing note's **frozen
  paper_id** when a note matching the row's DOI exists (rule 4 — online-first
  papers embed an earlier year in their frozen id than the corrected manifest
  year; batch 01 hit this on 8/16 papers before the automatic lookup existed).
  Still verify every regenerated bundle's `id:` maps to an existing note file
  before extracting.

**Per-batch procedure:** preflight (notes + texts exist; tier census; clean
tree — the diff-guard diffs against HEAD) → augmentation/re-extraction waves
(≤5–6 agents, chunked two-phase mode) → per note: `validate_note.py` +
`verify_augmentation.py` (augmented notes only) → **fresh full 9-field Layer 2
audits** for every touched note (native machinery, rubric v2 — this is the
uniform guarantee: every v3 note, native or augmented, passed the full audit)
→ assemble ALL official audits before any repair → repairs + scoped re-audits
→ gates → sequential rebuild → ledger → one release per batch.

**Backfill-specific policies:**
- **Scoped CrossRef is SKIPPED for augmented notes** — their bibliographic
  frontmatter is diff-guard-proven unchanged, so re-checking CrossRef would be
  ritual. Re-extracted v1 notes DO get the scoped check (their frontmatter is
  regenerated from the manifest).
- **Legacy-PARTIAL policy:** fresh audits re-examine old fields written before
  current standards. The ≥3-same-cause stop rule applies at full strength to
  the three NEW fields (drift there = augmentation-prompt problem). A repeated
  same-cause pattern on OLD fields is expected legacy drift: repair the batch,
  report the tally, continue — do not stop 33 times for a known pattern.
- **All-augmentation batch signature (batch 03):** `index/library.bib` is a pure
  projection of bibliographic frontmatter, which augmentation is forbidden to
  touch — so in a batch with no re-extraction it regenerates **byte-identical**
  and does not appear in the commit. Only `synapse.db` and `papers.csv` change
  (they index the new sections and `extraction_version`). Two-of-three index
  files changing is the *correct* signature, not a failed export.
- **Faithful-note PARTIALs (the li-2025 precedent, batch 02):** when a PARTIAL
  flags a sentence you can verify is faithful against the RAW extracted text,
  do NOT edit the note. Accept the residual PARTIAL, record it in the ledger
  and release notes (the note's overall audit is still pass), and move on.
  Editing accurate content to appease a verification artifact is a
  faithfulness violation, not a repair.
  **Verification requires BOTH search modes (batch-08 banerjee lesson):**
  two-column interleaving can splice a body sentence word-by-word into the
  references region (defeating raw line-based grep, the li-2025 case) AND can
  inject column-2 content mid-phrase (defeating whitespace-tolerant search —
  banerjee's "opposite directionality than predicted" sat around an injected
  "Robustness Model 1…" run). Search the raw text line-based on SHORT
  fragments *and* whitespace-tolerant on longer ones; a 0-hit search is never
  by itself proof a claim is absent from the paper.
- **Appendix-trim PARTIALs are fixed in-tool (batches 09–10: hersel,
  lauriano, xu-2022):** `audit_note.py` now strips only the references block
  and RE-APPENDS the appendix (capped at 40K chars, seam-marked, announced in
  the auditor preamble), so a note faithfully citing appendix-sourced details
  no longer draws a PARTIAL from an auditor who never saw the appendix. A
  corpus scan found 113 papers (~10%) carry a retainable appendix. For audit
  reports produced before this change, or if a claim sits beyond the 40K cap
  (3 papers corpus-wide), the acceptance path above applies: verify in the
  RAW text, accept-and-document.
- **Interleaved-references truncation (batch 11: ferns 25%, pamphile 18.5%
  of paper lost — class still OPEN):** in two-column output a *real*
  REFERENCES heading can sit atop column 2 while column 1 still carries
  Discussion prose, so the strip discards interleaved body text and faithful
  claims in that region draw PARTIALs. The fitter now records
  `references_strip_ratio` and sets `references_strip_suspicious` above 15%
  (calibrated: the known victims measured 25% and 18.5%; ~25% of the corpus
  flags, mostly legitimate long bibliographies — the flag is a caution, not
  a diagnosis), and the auditor preamble on flagged papers warns to score an
  unfindable claim as PARTIAL with suspected strip loss, never as
  fabrication. Parent handling: verify truncation-shaped PARTIALs against
  the RAW text with both search modes; faithful-in-stripped-region →
  accepted PARTIAL (ferns/pamphile precedent). The 15% flag ROUTES
  attention — it does not bound the class: batch-20 de-stefano lost
  Discussion prose at a 13.9% strip with no caution issued, so treat ANY
  truncation-shaped PARTIAL as a raw-text verification case regardless of
  the ratio. The cut-point logic itself is
  deliberately NOT fixed mid-backfill — it is global regex behavior under
  the corpus-sweep policy, and by user decision (2026-07-30) the fix is
  scheduled AFTER the AMJ backfill completes (all 67 issues at v3), in a
  dedicated scoped session alongside the cleanup pass. That session should
  also re-audit the strip-loss accepted PARTIALs accumulated by then (the
  notes are faithful and unchanged, so post-fix fresh audits should convert
  them to SUPPORTED and clear the public record). Until then: detector +
  accept-and-document, no cut-point edits.
- **Model outages during dispatch (batch 12, API 529 storm):** subagent
  waves can die at zero tokens while the parent session keeps working — a
  capacity outage, not a concurrency problem. Never substitute a different
  model for the specified M: extractor/auditor provenance is load-bearing,
  and silently downgrading the faithfulness gate would weaken a published
  guarantee (batch-08 precedent: model divergence is stop-and-ask). Back
  off and walk the wave ladder (6 → 5 → 3 → serial), check
  status.claude.com to distinguish capacity from concurrency, and if the
  outage is sustained, stop and report — the audit phase is read-only
  until layer2 assembly, so an interrupted batch resumes later with zero
  rework. An account/session USAGE LIMIT is not an API outage (batch 23):
  when a quota kill takes out part of a wave, bank the completed
  verdicts, wait for the stated reset time, and re-dispatch only the
  outstanding notes — no ladder walk, no model substitution, zero rework.
  Dispatch scripts must fail FAST on a dead wave: `parallel()`
  resolves dead agents to null and never rejects, so check for an all-null
  wave and abort instead of marching through the remaining waves. A
  PARTIAL wave — most agents return, one dies on a connection error — is
  NOT an outage: re-dispatch just the dead agent (batch-13 guo). And a
  Claude Code note: the Workflow tool has no `run_in_background`
  parameter (that flag belongs to the Agent tool); workflows always run
  in the background and notify on completion — sequence the two issues by
  waiting for the notification, never by forcing a synchronous run
  (batch-13 InputValidationError). Two further dispatch-hygiene rules
  (batch 14): read agent returns from the workflow JOURNAL — the
  authoritative record of each agent's raw return — never from the
  background task's `.output` file, which can be a truncated preview that
  parses into the wrong shape (batch 14: a 13-agent result parsed as 7
  string keys and threw; a quieter truncation would silently drop
  concerns). And once a mutation workflow is in flight, take any census
  or baseline from **git HEAD**, not the working tree — agents land
  mid-flight, so the tree is no longer a fixed reference frame (batch
  14's one-note census wobble). And when invoking the Workflow tool with
  `args`, pass arrays/objects as ACTUAL JSON values — never a
  JSON-encoded string; a stringified `args` reaches the script as one
  string, so `args.ids`/`args.chunks` are undefined and the wave dies at
  zero agents (batch-15 `CHUNKS.length`, 0 tokens). Scripts that read
  `args` should open with
  `const A = typeof args === 'string' ? JSON.parse(args) : args`.
- **Regenerate audit prompts LAST, immediately before dispatch (batch
  13):** `--prompt-only` snapshots the note into a file, so the prompt and
  the note silently diverge the moment any repair lands after generation.
  Batch 13 regenerated prompts, then applied two round-3 repairs, and
  dispatched auditors against stale snapshots — caught and re-dispatched
  before any verdict was recorded (the layer2 note-hash would have flagged
  it at assembly, but only after burning the auditor runs). Rule: repairs
  first, then regenerate, then dispatch — never the other order.
- **Section attribution needs the column view, never offsets (batch 14,
  methot + bain):** in two-column pdftotext output, a heading's character
  offset does NOT bound the preceding section — column 1 can still be
  running the prior section's prose while column 2 has already started
  the next, so an `index('STUDY 3')`-style boundary silently mis-attributes
  content. Batch 14 diagnosed exactly this on methot, then repeated it on
  bain an hour later, writing a repair that credited a Study 2 result to
  Study 3 and costing an extra audit round. When attributing a claim to a
  study or section during verification or repair, read the line-level
  column geometry around the boundary; never conclude from offsets.
- **Verification sweeps run in ONE Python script, not composite shell
  chains (batches 04–21):** zsh word-splitting, quoting artifacts, and
  grep's exit-1-on-no-match have each either mislabeled a clean state as
  a failure or silently suppressed later checks in the same `&&` chain
  (batch 21: the disk-scope grep found nothing — the GOOD outcome — and
  its exit 1 aborted the anchor and heading checks queued behind it). Run
  independent checks as separate commands or one Python script; any grep
  used as a display filter where zero matches is success gets `|| true`.
- **Strip-loss proof = presence-in-raw + absence-in-fitted (batch-21
  sherf):** to verify a suspected strip-loss PARTIAL, do not stop at
  finding the content in the raw text — RECONSTRUCT the exact fitted text
  the auditor received via `audit_note.fit_pdf_text_for_audit(raw)` and
  probe THAT. Content present in raw and absent from fitted is the proof;
  content present in both means the auditor saw it and the PARTIAL needs
  a different explanation. **The proof establishes only that the auditor
  was BLIND — not that the note is faithful (batch-23 kotha):** after
  proving blindness, READ the recovered passage and judge accept-vs-repair
  on its content. Kotha's Limitations tail was both invisible to the
  auditor AND wrong (the note claimed a generalization limit where the
  recovered text says the principles "will generally apply") — stopping
  at the proof would have false-accepted an invented claim.
- **Full-line rule (batch 15, zipay + opper):** a width-truncated preview
  of a matched line is the sibling failure of the 0-hit search. Batch 15
  nearly deleted a supported claim and DID ship a wrong repair from a
  130-character preview whose full line said the opposite ("M2 and M3 are
  ordinary least squares…" hidden past the cut). When verifying a flagged
  claim or drafting a repair, print the complete matched line(s)
  untruncated (repr-style, no width cap) and read the surrounding
  raw-text paragraph before writing a word. Treat repairs as first
  drafts: three of batch 15's round-2 PARTIALs were introduced by its own
  round-1 repairs and caught only by the mandatory re-audit — never skip
  the re-audit of a repaired note, however trivial the edit looks.
- **Two-channel adjudication (batch-14 bain):** "the audit adjudicates"
  is the default disposition for augmentation-agent concerns, not a
  ceiling on parent verification. A concern alleging a source-verifiable
  FACTUAL error — study scope, direction, attribution — that the audit
  scores SUPPORTED must still be parent-verified against the raw text
  before closeout; if it verifies, it is an always-fix repair regardless
  of the verdict (bain: the auditor checked model structure, the flag was
  about multi-study scope, and "voice type" had zero hits outside
  Study 1). The two channels see different things — a writer who just
  read the whole paper catches scope; a verdict-oriented auditor catches
  structure.
- **Repair convergence bound:** source-verified factual errors are always
  fixed, regardless of how many rounds it takes (batch-02 preston needed
  three, each a distinct genuine error). But when a fresh auditor keeps
  surfacing new *subjective or wording* nuances on legacy fields after two
  rounds, accept-and-document rather than play whack-a-mole.
- **Premise repairs touch sibling fields (batch-10 dwertmann):** when a
  repair corrects a *premise* rather than a sentence (e.g., "single-country
  sample ⇒ limited generalizability" where the paper argues the opposite),
  check the adjacent prose fields for the same premise in the same pass — a
  legacy misreading absorbed once tends to surface in both Limitations and
  Future Research, and repairing only one costs an extra audit round.
- Batch order: newest-first (69-1+68-6, then 68-5+68-4, … down to 58-1+58-2);
  the 27 v1 notes all sit in 69-1/68-6/68-5, so re-extraction clears in the
  first two batches (done as of batch 02 — batches 03+ are pure
  augmentation). NBS (272 notes: 61 v1 + 211 v2) is a separate later
  decision.

## Note version tiers (important for auditing & querying)

The corpus is intentionally heterogeneous; tools branch on `extraction_version`:

- **v1** (legacy) — no evidence anchors; exempt from Layer 1. 6 audited prose fields.
- **v2** — 7 evidence anchors; 8 body sections; 6 audited prose fields.
- **v3** — 10 evidence anchors; 11 body sections; **9** audited prose fields
  (adds Hypotheses / Propositions, Data & Measures, Key Findings). New notes
  are extracted natively at v3; pre-v3 notes are being upgraded by the
  backfill above. An **augmented** v3 note carries `augmented_model` /
  `augmented_at` frontmatter: its six original prose fields were written by
  `extraction_model`, its three v3 sections by `augmented_model`, and the
  whole note passed a fresh full 9-field rubric-v2 audit at augmentation time.
