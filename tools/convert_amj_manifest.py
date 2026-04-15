#!/usr/bin/env python3
"""
convert_amj_manifest.py — one-off scaffolding to project an AMJ source manifest
into a Synapse-compatible manifest.tsv.

The user staged 19 issues of Academy of Management Journal at
/Users/tangbinqi/Claude/AMJ/, each with its own manifest.tsv. Those manifests
have an 11-column schema where:

  - column "doi" is actually an AOM internal ID (e.g., "AMJ_20264001"), NOT a
    real DOI; and
  - the real DOI is embedded in column "article_url" (e.g.,
    "https://journals.aom.org/doi/10.5465/amj.2026.4001").

This script reads each AMJ source manifest, extracts the real DOI from
article_url, validates the 5 columns that prepare_paper.py actually consumes
(saved_filename, first_author_last, year, title, doi), and writes a Synapse
manifest into library/AMJ/<vol-slug>/manifest.tsv with CRLF line endings to
match the NBS convention.

This script is disposable: it lives in tools/ for reproducibility but it is
NEVER invoked by the runtime ingestion pipeline. After it runs, the on-disk
Synapse manifest is the source of truth.

Usage:
  # Dry-run a single issue (writes to stdout, no files modified):
  python tools/convert_amj_manifest.py --dry-run "Volume 69 Issue 1"

  # Convert all 19 issues from the staging tree into library/AMJ/:
  python tools/convert_amj_manifest.py --all

  # Default staging root: /Users/tangbinqi/Claude/AMJ
  # Override with --src <path>
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# --- locate the Synapse root ------------------------------------------------------

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
LIBRARY = SYNAPSE_ROOT / "library"

DEFAULT_SRC = Path("/Users/tangbinqi/Claude/AMJ")
SOURCE_SLUG = "AMJ"

# Output schema: the 5 columns prepare_paper.py and validate_note.py actually
# read, plus status (for triage) and a few AMJ extras that ride along
# harmlessly. Order is chosen for readability when scanning the file.
OUT_COLUMNS = [
    "title",
    "first_author_last",
    "year",
    "saved_filename",
    "doi",
    "status",
    "section",
    "article_type",
    "article_url",
    "pdf_url",
    "note",
]

# Map "Volume 66 Issue 1" -> "vol-66-no-1"
FOLDER_RE = re.compile(r"^Volume\s+(\d+)\s+Issue\s+(\d+)\s*$")

# Real DOIs hide inside article_url like
#   https://journals.aom.org/doi/10.5465/amj.2026.4001
DOI_FROM_URL_RE = re.compile(r"journals\.aom\.org/doi/(10\.\d{4,9}/[^?#\s]+)")


def folder_to_slug(folder_name: str) -> str:
    """`Volume 69 Issue 1` -> `vol-69-no-1`. Raises on unrecognized formats."""
    m = FOLDER_RE.match(folder_name)
    if not m:
        raise ValueError(
            f"unrecognized AMJ folder name {folder_name!r}; "
            f"expected 'Volume <N> Issue <N>'"
        )
    return f"vol-{m.group(1)}-no-{m.group(2)}"


def extract_real_doi(article_url: str) -> str:
    """Pull the bare DOI out of an AOM article_url. Returns '' if not found."""
    if not article_url:
        return ""
    m = DOI_FROM_URL_RE.search(article_url)
    return m.group(1) if m else ""


def convert_row(src_row: dict, lineno: int) -> tuple[dict, list[str]]:
    """Project one source row to the Synapse schema. Returns (out_row, errors)."""
    errors: list[str] = []
    out: dict[str, str] = {col: "" for col in OUT_COLUMNS}

    # Pass-through fields (no transformation).
    for col in ("title", "first_author_last", "year", "saved_filename",
                "status", "section", "article_type", "article_url",
                "pdf_url", "note"):
        out[col] = (src_row.get(col) or "").strip()

    # The trusted DOI lives in article_url, not in the misnamed `doi` column.
    out["doi"] = extract_real_doi(out["article_url"])

    # Validate the 5 load-bearing columns.
    for required in ("title", "first_author_last", "year", "saved_filename", "doi"):
        if not out[required]:
            errors.append(f"row {lineno}: missing {required}")

    # Year sanity check.
    if out["year"] and not re.fullmatch(r"\d{4}", out["year"]):
        errors.append(f"row {lineno}: year {out['year']!r} is not a 4-digit year")

    return out, errors


def convert_manifest(src_manifest: Path) -> tuple[list[dict], list[str]]:
    """Read AMJ source manifest, return (converted_rows, errors)."""
    if not src_manifest.exists():
        return [], [f"source manifest not found: {src_manifest}"]
    rows: list[dict] = []
    errors: list[str] = []
    with src_manifest.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for lineno, src_row in enumerate(reader, start=2):  # header is line 1
            out_row, row_errors = convert_row(src_row, lineno)
            rows.append(out_row)
            errors.extend(row_errors)
    return rows, errors


def write_synapse_manifest(rows: list[dict], dest: Path) -> None:
    """Write rows to <dest> with CRLF line endings (matches NBS convention)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=OUT_COLUMNS, delimiter="\t", lineterminator="\r\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def render_to_stdout(rows: list[dict]) -> None:
    """Print rows to stdout in TSV form (LF, for terminal readability)."""
    writer = csv.DictWriter(
        sys.stdout, fieldnames=OUT_COLUMNS, delimiter="\t", lineterminator="\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


def list_source_folders(src_root: Path) -> list[Path]:
    """Return the AMJ issue folders, sorted by (volume, issue)."""
    folders: list[tuple[int, int, Path]] = []
    for child in src_root.iterdir():
        if not child.is_dir():
            continue
        m = FOLDER_RE.match(child.name)
        if not m:
            continue
        folders.append((int(m.group(1)), int(m.group(2)), child))
    folders.sort()
    return [p for _, _, p in folders]


def process_one(src_folder: Path, *, dry_run: bool) -> tuple[int, int, list[str]]:
    """Convert one AMJ issue. Returns (n_rows, n_errors, error_messages)."""
    src_manifest = src_folder / "manifest.tsv"
    rows, errors = convert_manifest(src_manifest)
    slug = folder_to_slug(src_folder.name)
    dest = LIBRARY / SOURCE_SLUG / slug / "manifest.tsv"
    if dry_run:
        print(f"# DRY RUN: {src_folder.name} -> {dest.relative_to(SYNAPSE_ROOT)}")
        print(f"# {len(rows)} rows, {len(errors)} errors")
        if errors:
            for e in errors:
                print(f"# ERROR: {e}", file=sys.stderr)
        print()
        render_to_stdout(rows)
    else:
        if errors:
            for e in errors:
                print(f"ERROR: {src_folder.name}: {e}", file=sys.stderr)
            return len(rows), len(errors), errors
        write_synapse_manifest(rows, dest)
        print(
            f"wrote {dest.relative_to(SYNAPSE_ROOT)}  "
            f"({len(rows)} rows)"
        )
    return len(rows), len(errors), errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--src", type=Path, default=DEFAULT_SRC,
                   help=f"AMJ staging root (default: {DEFAULT_SRC})")
    p.add_argument("--dry-run", metavar="FOLDER",
                   help="dry-run mode: print converted manifest for one folder "
                        "to stdout, no files written")
    p.add_argument("--all", action="store_true",
                   help="convert all 19 AMJ issues into library/AMJ/")
    args = p.parse_args()

    if args.dry_run:
        src_folder = args.src / args.dry_run
        if not src_folder.exists():
            print(f"folder not found: {src_folder}", file=sys.stderr)
            return 2
        process_one(src_folder, dry_run=True)
        return 0

    if args.all:
        if not args.src.exists():
            print(f"staging root not found: {args.src}", file=sys.stderr)
            return 2
        folders = list_source_folders(args.src)
        if not folders:
            print(f"no AMJ issue folders found under {args.src}", file=sys.stderr)
            return 2
        total_rows = 0
        total_errors = 0
        for f in folders:
            n_rows, n_errors, _ = process_one(f, dry_run=False)
            total_rows += n_rows
            total_errors += n_errors
        print(
            f"\nconverted {len(folders)} issues, "
            f"{total_rows} total rows, {total_errors} errors"
        )
        return 1 if total_errors else 0

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
