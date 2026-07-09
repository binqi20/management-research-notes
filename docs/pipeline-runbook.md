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
- **Unit of release = one volume.** Keep per-issue work local; push and tag a
  release only when every issue of a volume is complete and verified (AMJ = 6
  issues per volume).
- **Parallel-agent cap = 6.** At most 6 active extraction agents *or* 6 active
  audit agents per wave. Never mix extraction and audit in the same wave. On any
  cap/timeout/coordination trouble, fall back 6 → 5 → 3 → serial. See
  [`AGENTS.md` §4.1](../AGENTS.md).

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

Dispatch fresh auditor agents that read **only** the rubric + the note + its
extracted text (never the extraction agent's reasoning). Each writes
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

## Publishing a completed volume

Only when every issue of the volume is done and Steps 4–4.5 are clean:

```
git add notes/ index/ library/<source>/<vol>/*/manifest.tsv
git commit -m "Add <SOURCE> volume <N> notes"
```

**Push over SSH** — HTTPS has repeatedly stalled on these large commits (see the
2026-07-07 worklog). The remote currently still points at HTTPS; switch it **once**,
only after confirming an SSH key is registered with GitHub:
```
# One-time setup — do this only if `ssh -T git@github.com` does NOT greet you by name:
#   ssh-keygen -t ed25519 -C "you@example.com"   # if you have no key yet
#   then add ~/.ssh/id_ed25519.pub at https://github.com/settings/keys
ssh -T git@github.com    # must print: Hi binqi20! You've successfully authenticated...
git remote set-url origin git@github.com:binqi20/management-research-notes.git

# Every release thereafter:
git push origin main
git tag vX.Y.Z && git push origin vX.Y.Z
```
**Do not switch the remote while `ssh -T` still returns "Permission denied
(publickey)"** — a non-working SSH remote is worse than a slow HTTPS one. Fallback
for a stalled HTTPS push is the GitHub Git database API (upload blobs → tree →
commit → tag), then realign local `HEAD`/`origin/main`/tag to the verified remote.
Tagged releases are archived to Zenodo.

---

## Note version tiers (important for auditing & querying)

The corpus is intentionally heterogeneous; tools branch on `extraction_version`:

- **v1** (legacy) — no evidence anchors; exempt from Layer 1. 6 audited prose fields.
- **v2** — 7 evidence anchors; 8 body sections; 6 audited prose fields.
- **v3** (current, going-forward) — 10 evidence anchors; 11 body sections; **9**
  audited prose fields (adds Hypotheses / Propositions, Data & Measures, Key
  Findings). New notes are v3; existing v1/v2 notes are **not** backfilled and
  remain valid unchanged.
