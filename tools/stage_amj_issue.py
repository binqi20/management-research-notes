#!/usr/bin/env python3
"""Stage a Codex AMJ issue into the Synapse library.

Copies an issue's PDFs from <codex-root>/Volume <V> Issue <I>/ into
library/AMJ/vol-<V>-no-<I>/pdfs/ and converts the Codex manifest.tsv (a
superset schema with download-QA columns) into the Synapse AMJ manifest
schema. Leaves volume/issue/pages empty for tools/populate_manifest.py to
backfill from CrossRef (Tier-3 gate), exactly like the existing AMJ issues.

The Codex manifest already records per-PDF completeness (pdf_complete /
actual_page_count); rows that look like 1-page stubs are reported so they
can be re-acquired before extraction — they are still copied, never dropped.

Usage:
  python tools/stage_amj_issue.py <volume> <issue> [--codex-root PATH] [--dry-run]
"""
import argparse
import csv
import shutil
import sys
from pathlib import Path

DEFAULT_CODEX_ROOT = Path("/Users/tangbinqi/Codex/AMJ")
LIBRARY_AMJ = Path(__file__).resolve().parent.parent / "library" / "AMJ"

# Synapse AMJ manifest schema (column order is intentional, matches existing issues).
TARGET_COLS = [
    "title", "first_author_last", "year", "saved_filename", "doi", "status",
    "section", "article_type", "article_url", "pdf_url", "note",
    "volume", "issue", "pages",
]


def is_stub(row: dict) -> bool:
    """Codex pre-recorded completeness; treat false/incomplete or <=1 page as a stub."""
    pc = (row.get("pdf_complete") or "").strip().lower()
    if pc in ("false", "no", "0", "incomplete"):
        return True
    apc = (row.get("actual_page_count") or "").strip()
    if apc:
        try:
            if int(float(apc)) <= 1:
                return True
        except ValueError:
            pass
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("volume", type=int)
    ap.add_argument("issue", type=int)
    ap.add_argument("--codex-root", default=str(DEFAULT_CODEX_ROOT))
    ap.add_argument("--dry-run", action="store_true", help="report only; copy nothing")
    args = ap.parse_args()

    src = Path(args.codex_root) / f"Volume {args.volume} Issue {args.issue}"
    dst = LIBRARY_AMJ / f"vol-{args.volume}-no-{args.issue}"
    src_manifest = src / "manifest.tsv"
    if not src_manifest.exists():
        sys.exit(f"Codex manifest not found: {src_manifest}")

    with src_manifest.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    if not args.dry_run:
        (dst / "pdfs").mkdir(parents=True, exist_ok=True)
        (dst / "text").mkdir(parents=True, exist_ok=True)

    out_rows, copied, missing, stubs = [], 0, [], []
    for r in rows:
        sf = (r.get("saved_filename") or "").strip()
        out = {c: (r.get(c) or "").strip() for c in TARGET_COLS}
        out["volume"] = out["issue"] = out["pages"] = ""  # populate_manifest backfills
        out_rows.append(out)

        if not sf:
            missing.append("(blank saved_filename)")
            continue
        spdf = src / sf
        if spdf.exists():
            if not args.dry_run:
                shutil.copy2(spdf, dst / "pdfs" / sf)
            copied += 1
        else:
            missing.append(sf)
        if is_stub(r):
            stubs.append(sf)

    if not args.dry_run:
        with (dst / "manifest.tsv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=TARGET_COLS, delimiter="\t")
            w.writeheader()
            w.writerows(out_rows)

    tag = "[dry-run] " if args.dry_run else ""
    print(f"{tag}vol-{args.volume}-no-{args.issue}: manifest rows={len(rows)}  pdfs copied={copied}")
    print(f"  dst: {dst}")
    if missing:
        print(f"  MISSING PDFs ({len(missing)}): {missing}")
    if stubs:
        print(f"  STUBS flagged by Codex (re-acquire before extract) ({len(stubs)}): {stubs}")
    if not missing and not stubs:
        print("  OK: all PDFs present, none flagged as stubs")


if __name__ == "__main__":
    main()
