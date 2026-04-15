---
description: Re-run the two-layer faithfulness audit on a single Synapse note. Useful after manual edits, after a prompt change, or to spot-check a suspicious paper. Prints a structured verdict and writes a fresh audit report to incoming/_audits/<paper_id>.audit.json.
argument-hint: "<paper_id | notes/<paper_id>.md>"
---

# /audit-note — on-demand faithfulness audit

You are running the **Synapse faithfulness audit** on a single note. This
command is the on-demand companion to the audit step in `/synapse-ingest`
— same tool, same rubric, same exit codes, but invoked one note at a time.

**The argument is:** `$ARGUMENTS`

If no argument was passed, **stop** and ask the user which note they want
audited. Accept either form:

- A bare paper_id like `nbs-2026-02-spoor-2026`
- A note path like `notes/nbs-2026-02-spoor-2026.md`

---

## When to use this command

Use `/audit-note` when you want a faithfulness verdict for a single note
and you don't want to re-run the whole `/synapse-ingest` pipeline:

- **After a manual edit.** You hand-fixed a typo or a misattribution in
  `notes/<paper_id>.md` and want to confirm the edit didn't introduce a
  claim that's no longer supported by the PDF.
- **After an extraction-prompt change.** You bumped `prompt_version` or
  tightened the rubric; re-audit a representative note to see the new
  verdict shape.
- **Spot-checking a suspicious paper.** You noticed a claim in a note that
  feels too confident or too specific; re-run the audit to get a fresh
  second opinion from a cold-context subagent.
- **Debugging Layer 1 anchors.** You suspect an anchor is a false positive
  or false negative — the audit JSON will show exactly which quote fired
  and what the two-pass normalization turned it into.

This command is **read-only by default**. It will NOT write a
`.reason.txt` sidecar even if the audit fails. If you want the failure
persisted to `incoming/_flagged/`, add `--flag` explicitly when invoking
`audit_note.py` directly, or re-run the full `/synapse-ingest` pipeline.

---

## What to do

### Step 1 — Resolve the argument to a note path

Parse `$ARGUMENTS`:

1. Strip any surrounding whitespace or quotes.
2. If it ends in `.md` and exists on disk, use it as the note path.
3. Otherwise, treat it as a paper_id and resolve to
   `notes/<paper_id>.md`.
4. If the resolved path does not exist, stop and report clearly:
   "No note found at `notes/<paper_id>.md`. Run
   `ls notes/ | grep <partial-id>` to find the right one."

Do **not** try to be clever about partial matches or fuzzy search — the
user should pass an exact paper_id or an exact path. If they don't know
the exact id, they can use `Grep` over `notes/` first.

### Step 2 — Verify preconditions

Read the note's YAML frontmatter (use `Read` on the note file, then
inspect the first block between the `---` fences). Check:

1. `extraction_version` is present. If it's `v1` or missing, warn the
   user that Layer 1 (evidence anchors) will be **skipped** — only
   v2 notes have the `evidence:` block. Layer 2 still runs on v1 notes.
2. `paper_type` is present and is one of the eight allowed types. If
   missing, stop and tell the user the note appears malformed.
3. The PDF text file referenced by `text_path` in the frontmatter
   exists on disk. If not, stop and report — Layer 1 needs the PDF
   text, and so does the Layer 2 prompt.

### Step 3 — Run the audit

```bash
python tools/audit_note.py notes/<paper_id>.md
```

This is the default path: Layer 1 first, then a fresh Claude subagent
via `claude --print` for Layer 2. No `--flag` (this command is
read-only). No `--dry-run` (we want the audit JSON written to disk so
the user can re-open it later for full detail).

**Expected cost:** ~1–5 minutes wall clock per invocation, dominated by
the Layer 2 subagent dispatch. If Layer 1 fails, Layer 2 is
short-circuited and the whole thing takes about one second.

### Step 4 — Report the verdict to the user

Read the fresh audit JSON at `incoming/_audits/<paper_id>.audit.json`
and produce a human-readable summary in this shape:

```
AUDIT VERDICT: <PASS|FAIL> — <paper_id>
  auditor: <auditor_model>
  audited_at: <timestamp>

Layer 1 (evidence anchors): <pass|fail|skipped>
  anchors checked: N
  <if fail, list each anchors_not_found_in_pdf entry with a 40-char preview>

Layer 2 (prose faithfulness): <pass|fail|skipped>
  research_question:          <verdict> (<confidence>) — <one-line note>
  mechanism_process:          <verdict> (<confidence>) — <one-line note>
  theoretical_contribution:   <verdict> (<confidence>) — <one-line note>
  practical_implication:      <verdict> (<confidence>) — <one-line note>
  limitations:                <verdict> (<confidence>) — <one-line note>
  future_research:            <verdict> (<confidence>) — <one-line note>

Flagged claims: <count>
  <bulleted list of each flagged_claims entry with its field and verdict>

Full report: incoming/_audits/<paper_id>.audit.json
```

Trim each note to its first ~80 characters so the verdict stays scannable.
If a field is `SUPPORTED` with high confidence, print a checkmark
character instead of the full note — reduce visual noise so the failures
stand out.

If the overall verdict is PASS, say so plainly and stop. Do not embellish.

If the overall verdict is FAIL, offer the user three next-step options
in one sentence each:

1. **Re-audit:** "Run `/audit-note <paper_id>` again if you suspect a
   transient subagent error" (Layer 2 is non-deterministic).
2. **Re-extract:** "Re-run `tools/prepare_paper.py` + extraction for
   this paper if the root cause is a bad initial extraction" (the
   cleanest fix).
3. **Flag:** "If you want the failure recorded in `_flagged/`, re-run
   `python tools/audit_note.py notes/<paper_id>.md --flag` directly."

---

## Flags the user may pass through

The slash command itself takes only a paper_id or note path. If the user
wants non-default behavior, tell them to invoke `audit_note.py` directly:

| Flag                  | Effect                                                 |
|-----------------------|--------------------------------------------------------|
| `--flag`              | Also write `.reason.txt` to `_flagged/` on fail        |
| `--dry-run`           | Do not write the audit JSON; just print the verdict   |
| `--skip-layer-2`      | Layer 1 only; no subagent dispatch (fast)              |
| `--force-layer-2`     | Run Layer 2 even if Layer 1 failed                     |
| `--auditor-model <m>` | Override the Layer 2 auditor model                     |
| `--prompt-only`       | Print the Layer 2 prompt to stdout and exit (debug)    |

---

## Things this command does NOT do

- **Does not re-extract the note.** If the note is garbage, re-run
  `/synapse-ingest` on the underlying PDF or call
  `tools/prepare_paper.py` manually.
- **Does not modify the note file.** The audit is a read-only verdict;
  any edits are the user's responsibility.
- **Does not rebuild the SQLite index.** The audit status is not yet
  reflected in `index/synapse.db`; that's a future enhancement.
- **Does not delete or move the note on fail.** Failed audits write a
  `.audit.json` report (and optionally a `.reason.txt` sidecar if
  `--flag` is passed to the underlying tool). The note itself stays
  in `notes/`.
- **Does not run in parallel.** One note per invocation. For a corpus
  sweep, use the retroactive-sweep tooling (gated by the plan's Step 7
  hard checkpoint).
