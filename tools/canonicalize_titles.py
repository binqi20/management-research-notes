#!/usr/bin/env python3
"""
canonicalize_titles.py — replace lossy manifest titles with canonical CrossRef titles.

Why this exists
---------------
Manifests built from PDF *filenames* (the NBS digests are the canonical case)
carry lossy titles: filenames cannot contain ":" (filesystem-illegal) or "?",
so every subtitle colon and trailing question mark is dropped. A filename-derived
title like

    More-than-capitalist economies Insights from community supported agriculture

is missing the colon CrossRef has:

    More-than-capitalist economies: Insights from community supported agriculture

These cosmetic-but-real differences are invisible to extraction but fail the
Step 4.5 gate (`verify_metadata.py`), which compares note title vs CrossRef with
`_norm_string(note) == _norm_string(crossref)` — and `_norm_string` keeps colons
and "?". On a filename-derived batch that is ~75% of rows, turning verify_metadata
into a wall of MISMATCHes at FINALIZE.

This tool fixes the source (the manifest) before extraction, so notes carry the
canonical title and the gate passes clean. CrossRef is the trusted authority for
bibliographic fields when the DOI is known (CLAUDE.md hard rule 1), so for a row
whose DOI is verified-correct, the CrossRef title is the right value.

Safety
------
A *wrong* auto-populated DOI would also produce a "title differs" — and blindly
copying its CrossRef title would import the wrong paper's title. So this tool
only upgrades when the CrossRef title is highly similar to the current manifest
title (same paper, cosmetic diff); any row below the similarity threshold is
FLAGGED, never changed, for manual review. That makes the tool safe to run on
machine-populated DOIs.

The canonical form stored is `html.unescape -> strip HTML/XML tags ->
collapse whitespace`, keeping proper colons, "?", curly quotes and Unicode
hyphens (display quality) while guaranteeing `_norm_string(stored) ==
_norm_string(crossref_raw)` — i.e., the verify_metadata title check passes by
construction (it applies the same unescape + tag-strip + whitespace-collapse).

Usage
-----
    python3 tools/canonicalize_titles.py library/NBS/2026-01/manifest.tsv
        # dry-run: show proposed title upgrades + any flagged rows

    python3 tools/canonicalize_titles.py library/NBS/2026-01/manifest.tsv --apply
        # write upgraded titles back (backup saved as .tsv.titles.bak)

Exit codes
----------
0: success, nothing flagged
1: one or more rows flagged as low-similarity (possible wrong DOI) — review them
2: invocation error (manifest missing, no doi/title column, etc.)
"""
from __future__ import annotations

import argparse
import csv
import difflib
import html
import re
import sys
from pathlib import Path

# Reuse verify_metadata's CrossRef access + normalization — single source of truth.
THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))
from verify_metadata import fetch_crossref, crossref_title, _norm_string  # noqa: E402


def canonical_title(raw: str) -> str:
    """CrossRef raw title -> clean display title.

    Mirror the parts of verify_metadata._norm_string that remove noise
    (entity-decode, tag-strip, whitespace-collapse) but KEEP case, colons,
    "?", curly quotes and Unicode hyphens so the stored title is canonical
    display quality. Because _norm_string also unescapes + strips tags +
    collapses whitespace, _norm_string(canonical_title(x)) == _norm_string(x),
    so the verify_metadata title gate passes by construction.
    """
    t = html.unescape(raw)
    t = re.sub(r"<[^>]+>", "", t)        # drop <scp>, <i>, <sub>, ... typesetting tags
    t = re.sub(r"\s+", " ", t).strip()    # collapse newlines/runs from multi-line CrossRef titles
    return t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest", help="path to manifest.tsv")
    ap.add_argument("--apply", action="store_true",
                    help="write upgraded titles back (default: dry-run)")
    ap.add_argument("--threshold", type=float, default=0.72,
                    help="min normalized similarity to upgrade; below = flag (default 0.72)")
    ap.add_argument("--quiet", action="store_true", help="suppress per-row output")
    args = ap.parse_args()

    path = Path(args.manifest).resolve()
    if not path.exists():
        print(f"manifest not found: {path}", file=sys.stderr)
        return 2

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        cols = reader.fieldnames
        rows = list(reader)
    if not cols or "doi" not in cols or "title" not in cols:
        print(f"manifest needs 'doi' and 'title' columns: {path}", file=sys.stderr)
        return 2

    print(f"Manifest:  {path}")
    print(f"Rows:      {len(rows)}   Threshold: {args.threshold}   Mode: {'APPLY' if args.apply else 'DRY-RUN'}\n")

    upgraded, already, flagged, no_doi = [], [], [], []

    for row in rows:
        doi = (row.get("doi") or "").strip()
        if not doi:
            no_doi.append(row)
            continue
        msg = fetch_crossref(doi)
        cr = crossref_title(msg) if msg else None
        if not cr:
            flagged.append((row, "CrossRef fetch failed or no title"))
            if not args.quiet:
                print(f"  ⚠ FLAG   {row.get('first_author_last','?')} — CrossRef fetch failed / no title")
            continue

        new = canonical_title(cr)
        cur = row.get("title", "") or ""
        ratio = difflib.SequenceMatcher(None, _norm_string(cur), _norm_string(new)).ratio()

        if cur == new:
            already.append(row)
        elif ratio >= args.threshold:
            upgraded.append((row, cur, new))
            row["title"] = new
            if not args.quiet:
                print(f"  ✓ UPGRADE ({ratio:.2f}) {row.get('first_author_last','?')}")
                print(f"       was: {cur[:88]}")
                print(f"       now: {new[:88]}")
        else:
            flagged.append((row, f"low similarity {ratio:.2f} — possible wrong DOI"))
            if not args.quiet:
                print(f"  ⚠ FLAG   ({ratio:.2f}) {row.get('first_author_last','?')} — possible wrong DOI")
                print(f"       manifest: {cur[:80]}")
                print(f"       crossref: {new[:80]}")

    if args.apply and upgraded:
        backup = path.with_suffix(".tsv.titles.bak")
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({c: row.get(c, "") for c in cols})
        print(f"\nWrote {len(upgraded)} upgraded titles. Backup: {backup.name}")

    print("\n" + "=" * 60)
    print(f"  Upgraded to CrossRef:   {len(upgraded):4d}")
    print(f"  Already canonical:      {len(already):4d}")
    print(f"  Flagged (review):       {len(flagged):4d}")
    print(f"  No DOI (skipped):       {len(no_doi):4d}")
    print(f"  Total rows:             {len(rows):4d}")
    if not args.apply and upgraded:
        print("\nDRY-RUN: no changes written. Re-run with --apply to upgrade.")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
