---
description: Generate or update today's daily work log — a Markdown summary of the day's work in this conversation (what was done and why, commits/releases, problems and their fixes, lessons, end-of-day state, and next steps) written to worklogs/YYYY-MM-DD.md. Run this ONLY when the user explicitly invokes /daily-log at the end of a workday; never generate a log proactively. Use it when the user asks to "log today's work", "write the work log", "end-of-day summary", "daily log", or "wrap up the day".
argument-hint: "[optional: YYYY-MM-DD to target a specific day, or a short focus note]"
---

# /daily-log — end-of-day work log

You are writing (or updating) the **daily work log** for this project: a durable
Markdown record of what happened today, so the user can reflect, review, and
iterate later. This is a **manual, end-of-day** command — run it only when the
user invokes it, never proactively.

**Argument (optional):** `$ARGUMENTS`
- If it is a date in `YYYY-MM-DD` form, write the log for that day instead of today.
- Otherwise treat it as a short focus hint (e.g. "emphasize the 2026-01 cleanup") and weight the summary accordingly.
- If empty, log today's work with no special emphasis.

---

## Why this exists

Write the log for **future-you**: the version who returns in a week or a month
and needs to reconstruct not just *what* changed but *why*. So favour decisions
and their rationale over a blow-by-blow of every tool call. A good entry is
scannable in about 60 seconds and still answers: "what state did we leave things
in, and what's next?"

One file per calendar day. Over time `worklogs/` becomes a continuous record you
can grep, diff, and review — which only works if each entry is faithful and
specific. Vague logs ("did some cleanup") are worse than no logs; concrete ones
("verify_metadata exit 0 across 363 notes; shipped v0.20.0") compound in value.

## Step 1 — Resolve the date and target file

1. Get the date (use today's unless `$ARGUMENTS` is an explicit `YYYY-MM-DD`):
   ```bash
   date +%Y-%m-%d
   ```
   Call the result `<DATE>`.
2. The target file is `worklogs/<DATE>.md`.
3. Make sure the folder exists:
   ```bash
   mkdir -p worklogs
   ```

## Step 2 — Gather concrete, factual anchors (don't rely on memory alone)

Ground the log in evidence, not just recollection — the same discipline the rest
of this project uses (trust the on-disk signal over your own narration). Pull the
day's hard artifacts:

```bash
# Commits made today (hash + subject). For a past <DATE>, use
#   --since="<DATE> 00:00" --until="<DATE> 23:59" instead of --since=midnight.
git log --since=midnight --pretty=format:'%h %s'

# Tags / releases, newest first (note any created today)
git tag --sort=-creatordate | head

# What's changed but uncommitted right now (the end-of-day state)
git status --short
```

Use these to make "What shipped" and "State at end of day" accurate. If git and
your recollection disagree, **trust git**.

## Step 3 — Write the log

Compose the summary from **this conversation** plus the Step 2 anchors. Be
faithful: record only work that actually happened. Never invent commits,
results, or decisions — if something is uncertain, say so explicitly. Link
releases and PRs with full URLs so they stay clickable later.

**If `worklogs/<DATE>.md` does NOT exist**, create it with this template:

```markdown
# Work Log — <DATE>

> **TL;DR:** <one or two sentences capturing the day at a glance.>

## Summary
<2–5 short paragraphs or bullets: the narrative of what was worked on and why it mattered.>

## What shipped
- <commit `<hash>` — one-line description / release `<tag>` (full URL) / PR>
- *(or "Nothing committed today." if that's the case)*

## Key decisions
- **<decision>** — <rationale: what alternatives were weighed and why this one won.>

## Problems & fixes
- **<problem>** — root cause: <…>; fix: <…>.

## Lessons & insights
- <reusable takeaway worth carrying into future work.>

## State at end of day
- <committed vs uncommitted; gate / test status; what's in progress.>

## Next steps
- [ ] <concrete, actionable next task.>

---
*Logged via `/daily-log` at <HH:MM>.*
```

**If `worklogs/<DATE>.md` already exists** (you ran this earlier today, or across
multiple conversations), do NOT overwrite it. Append a new session block so the
day's record accumulates losslessly:

```markdown

---

## Session — <HH:MM>

<the same sections — Summary / What shipped / Key decisions / Problems & fixes / Lessons & insights / State / Next steps — covering only the work since the previous entry.>
```

Drop any section that genuinely has nothing to report rather than padding it.

## Step 4 — Confirm (do not commit)

Report back to the user:
- The path written (`worklogs/<DATE>.md`) and whether you **created** or **appended**.
- A short preview — the TL;DR plus the Next-steps list — so they can sanity-check it.
- A reminder that you did **not** commit it: `worklogs/` is gitignored (kept local/
  private, off the public repo) by design. If they want a log version-controlled,
  they remove the `worklogs/` line from `.gitignore` and commit it themselves.

---

## What this command does NOT do

- **Does not run automatically.** End-of-day, on-demand only — wait for the user to invoke it.
- **Does not commit or push.** It writes a local file and stops.
- **Does not overwrite an existing day's log.** It appends a timestamped session block.
- **Does not invent work.** If the conversation and git don't support a claim, leave it out or mark it uncertain.
