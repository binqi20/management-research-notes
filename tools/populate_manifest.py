#!/usr/bin/env python3
"""
populate_manifest.py — populate a manifest's bibliographic columns from CrossRef.

Why this exists (Tier 3 of the bibliographic-integrity prevention strategy)
--------------------------------------------------------------------------
v0.11.1 fixed 48 wrong years; v0.11.2 fixed 21 papers' null vol/issue/pages.
Both were symptoms of the same root cause: **manifest TSVs are populated by
hand, and humans get bibliographic metadata wrong**. Wrong year (online-first
vs issue), missing Oxford comma, null volume because the issue hadn't
published yet at extraction time, etc.

This tool eliminates the manual entry step. Given a manifest with DOIs, it
queries CrossRef and fills in (or upgrades) `volume`, `issue`, `pages`
columns from the authoritative DOI registry. It also cross-checks `year`,
`title`, `journal` against CrossRef and warns on discrepancies — so manual
manifest typos surface BEFORE extraction rather than after.

Tier 1 (verify_years.py) and Tier 2 (verify_metadata.py) are end-of-pipeline
gates that catch errors after they've propagated. Tier 3 prevents the errors
at the source — the manifest is no longer hand-typed for the fields CrossRef
can authoritatively provide.

Usage
-----
    python tools/populate_manifest.py library/AMJ/vol-67-no-2/manifest.tsv
        # dry-run: shows what would change, doesn't write

    python tools/populate_manifest.py library/AMJ/vol-67-no-2/manifest.tsv --apply
        # writes the upgraded manifest back to disk

    python tools/populate_manifest.py path/to/manifest.tsv --apply --quiet
        # only print warnings/changes, suppress per-row noise

How it integrates with the rest of the pipeline
-----------------------------------------------
1. populate_manifest.py runs FIRST in the ingestion workflow (Phase 0,
   before pdf_to_text / prepare_paper).
2. The manifest TSV gains `volume`, `issue`, `pages` columns at the end.
3. prepare_paper.py reads those columns and includes them in the trusted
   bib block passed to the extraction agent.
4. The extraction agent puts them verbatim in the note frontmatter — the
   prompt at docs/extraction-prompt.md ALREADY has placeholders for these
   fields and tells the agent to use them when present.
5. verify_metadata.py runs LAST (Phase 6.5) and confirms every field
   round-tripped correctly through the pipeline. The two gates bookend
   the same data and should always agree.

Compatibility
-------------
- Manifests without `volume`/`issue`/`pages` columns: tool ADDS them.
- Manifests that already have them: tool UPDATES if CrossRef differs.
- DOIs missing from the manifest row: tool skips, warns.
- CrossRef misses (online-first papers without issue assignments yet):
  tool writes empty value, doesn't fail.
- All existing manifest columns (title, first_author_last, year, etc.)
  are preserved in their original positions.

Exit codes
----------
0: success, no discrepancies in existing fields
1: discrepancies found in existing fields (year/title/journal mismatch);
   review the warnings before re-running with --apply
2: usage error (manifest not found, etc.)
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Reuse the CrossRef client from verify_metadata.py — single source of truth
# for caching, SSL config, User-Agent, rate limiting. This means any future
# improvements to the CrossRef interaction propagate to both tools.
THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))
from verify_metadata import (  # noqa: E402
    fetch_crossref,
    crossref_year,
    crossref_title,
    crossref_journal,
    _norm_string,
    _norm_pages,
)


# Columns we manage. Appended at the end of the manifest if not already
# present. Order matters for the column write-back: same order as
# verify_metadata.py's ALL_FIELDS where overlapping.
MANAGED_COLUMNS = ("volume", "issue", "pages")


def upgrade_row(row: dict, dry_run: bool, quiet: bool, fix_year: bool) -> tuple[dict, list[str], list[str]]:
    """For one manifest row, query CrossRef and produce an upgraded row.

    Returns:
        (upgraded_row, info_messages, warning_messages)

    info_messages: per-row activity log (skip for --quiet output)
    warning_messages: discrepancies vs existing manifest values (always shown)

    If fix_year is True, year mismatches get auto-corrected to CrossRef's
    published-print value AND a warning is still emitted (so the audit
    trail records the change). Title/journal mismatches are always
    warning-only — those have too many legitimate format variations
    to safely auto-correct without human review.
    """
    info: list[str] = []
    warnings: list[str] = []
    upgraded = dict(row)  # copy; we'll overlay new columns

    doi = (row.get("doi") or "").strip()
    if not doi:
        info.append(f"  SKIP (no DOI): {row.get('first_author_last', '?')}")
        return upgraded, info, warnings

    # Normalize DOI: strip leading https://doi.org/ if present
    if doi.startswith("http"):
        doi = doi.split("doi.org/", 1)[-1]

    msg = fetch_crossref(doi)
    if msg is None:
        warnings.append(
            f"  CrossRef fetch failed for DOI {doi} ({row.get('first_author_last', '?')})"
        )
        return upgraded, info, warnings

    # ---------- Cross-check existing fields (warn on mismatch) ----------

    # Year
    cr_year, _ = crossref_year(msg)
    existing_year = (row.get("year") or "").strip()
    if cr_year is not None and existing_year:
        if str(cr_year) != existing_year:
            if fix_year:
                upgraded["year"] = str(cr_year)
                warnings.append(
                    f"  YEAR auto-corrected for {row.get('first_author_last', '?')} "
                    f"({doi}): manifest={existing_year} → {cr_year} (CrossRef "
                    f"published-print, APA 7 issue year)"
                )
            else:
                warnings.append(
                    f"  YEAR mismatch for {row.get('first_author_last', '?')} "
                    f"({doi}): manifest={existing_year}, crossref={cr_year} "
                    f"(APA 7 issue year). Re-run with --fix-year to auto-correct."
                )

    # Title (informational only — minor differences are common)
    cr_title = crossref_title(msg)
    existing_title = (row.get("title") or "").strip()
    if cr_title and existing_title:
        if _norm_string(cr_title) != _norm_string(existing_title):
            warnings.append(
                f"  TITLE differs for {row.get('first_author_last', '?')} ({doi}):\n"
                f"    manifest:  {existing_title[:120]}\n"
                f"    crossref:  {cr_title[:120]}"
            )

    # Journal (informational only)
    cr_journal = crossref_journal(msg)
    existing_journal = (row.get("journal") or "").strip()
    if cr_journal and existing_journal:
        if _norm_string(cr_journal) != _norm_string(existing_journal):
            warnings.append(
                f"  JOURNAL differs for {row.get('first_author_last', '?')} ({doi}): "
                f"manifest={existing_journal!r}, crossref={cr_journal!r}"
            )

    # ---------- Populate / upgrade managed columns ----------

    cr_volume = msg.get("volume")
    cr_issue = msg.get("issue")
    cr_pages_raw = msg.get("page")
    cr_pages = _norm_pages(cr_pages_raw) if cr_pages_raw else None

    new_values: dict[str, str] = {}
    new_values["volume"] = "" if cr_volume is None else str(cr_volume)
    new_values["issue"] = "" if cr_issue is None else str(cr_issue)
    new_values["pages"] = "" if cr_pages is None else cr_pages

    changes_for_row: list[str] = []
    for col in MANAGED_COLUMNS:
        old_val = (row.get(col) or "").strip()
        new_val = new_values[col].strip()
        if old_val == new_val:
            continue
        if not old_val and new_val:
            changes_for_row.append(f"{col}: (empty) → {new_val!r}")
        elif old_val and not new_val:
            changes_for_row.append(
                f"{col}: {old_val!r} → (empty)  [CrossRef has no value; keeping manifest? "
                f"NO — overwriting per CrossRef-as-source policy]"
            )
        else:
            changes_for_row.append(f"{col}: {old_val!r} → {new_val!r}")
        upgraded[col] = new_val

    label = f"{row.get('first_author_last', '?')} {existing_year} ({doi})"
    if changes_for_row:
        info.append(f"  {label}")
        for c in changes_for_row:
            info.append(f"    {c}")
    elif not quiet:
        info.append(f"  {label}: no changes")

    return upgraded, info, warnings


def write_upgraded_manifest(path: Path, rows: list[dict], original_columns: list[str]) -> None:
    """Write the upgraded manifest back to disk.

    Preserves the original column order, then appends any of MANAGED_COLUMNS
    that weren't already present. This keeps existing tools that read
    specific columns by position (none should, but defensive) working.
    """
    # Final column order = original + (any managed column not already there)
    columns = list(original_columns)
    for col in MANAGED_COLUMNS:
        if col not in columns:
            columns.append(col)

    # Write atomically: tempfile + rename, so a crash mid-write doesn't
    # leave a half-rewritten manifest.
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # Ensure every column has a value (empty string for missing keys).
            full_row = {c: (row.get(c) or "") for c in columns}
            writer.writerow(full_row)
    tmp.replace(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest", help="path to manifest.tsv")
    ap.add_argument("--apply", action="store_true",
                    help="write changes back (default: dry-run)")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress per-row 'no changes' output")
    ap.add_argument("--fix-year", action="store_true",
                    help="auto-correct year mismatches from CrossRef "
                         "published-print (APA 7 issue year). Warnings "
                         "are still emitted for the audit trail.")
    args = ap.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    # Read existing manifest
    with manifest_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        original_columns = list(reader.fieldnames or [])
        rows = list(reader)

    if not rows:
        print(f"manifest has no rows: {manifest_path}", file=sys.stderr)
        return 2

    print(f"Manifest:    {manifest_path}")
    print(f"Rows:        {len(rows)}")
    print(f"Mode:        {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Original columns ({len(original_columns)}): {original_columns}")
    new_cols = [c for c in MANAGED_COLUMNS if c not in original_columns]
    if new_cols:
        print(f"Will add new columns: {new_cols}")
    print()

    upgraded_rows: list[dict] = []
    all_warnings: list[str] = []
    n_changed = 0

    for row in rows:
        upgraded, info, warnings = upgrade_row(
            row, dry_run=not args.apply, quiet=args.quiet, fix_year=args.fix_year
        )
        upgraded_rows.append(upgraded)
        if not args.quiet:
            for line in info:
                print(line)
        if warnings:
            all_warnings.extend(warnings)
        # Track if upgrade produced any change vs original
        for col in MANAGED_COLUMNS:
            if (upgraded.get(col, "") or "").strip() != (row.get(col, "") or "").strip():
                n_changed += 1
                break

    print()
    print("=" * 70)
    print(f"  {n_changed} row(s) have CrossRef-derived changes "
          f"to {MANAGED_COLUMNS}")
    if all_warnings:
        print(f"  {len(all_warnings)} warning(s) about existing-field discrepancies:")
        print("=" * 70)
        for w in all_warnings:
            print(w)
    else:
        print("  No warnings — existing year/title/journal columns all "
              "agree with CrossRef.")
    print("=" * 70)

    if args.apply:
        write_upgraded_manifest(manifest_path, upgraded_rows, original_columns)
        print(f"\nWrote upgraded manifest to {manifest_path}.")
    else:
        print("\nDRY-RUN: no files modified. Re-run with --apply to write.")

    return 1 if all_warnings else 0


if __name__ == "__main__":
    sys.exit(main())
