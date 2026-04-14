#!/usr/bin/env python3
"""
ingest_batch.py — walk a folder of PDFs and run the deterministic half of the
ingestion pipeline for each one: extract text, look up trusted bibliographic
metadata from the manifest, and emit an extraction bundle in incoming/_bundles/.

This does NOT run the LLM extraction itself — that step is driven from a Claude
Code session which reads each bundle, applies the canonical extraction prompt at
docs/extraction-prompt.md, and writes notes/<paper_id>.md.

Usage:
  python tools/ingest_batch.py library/NBS/2026-02/pdfs
  python tools/ingest_batch.py library/NBS/2026-02/pdfs --skip-text

Flags:
  --skip-text   Skip pdf_to_text.py (useful if text/ is already populated).
  --only-new    Skip PDFs whose paper_id already has a note in notes/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
TOOLS = SYNAPSE_ROOT / "tools"
NOTES = SYNAPSE_ROOT / "notes"
BUNDLES = SYNAPSE_ROOT / "incoming" / "_bundles"


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def existing_note_ids() -> set[str]:
    return {p.stem for p in NOTES.glob("*.md")}


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: ingest_batch.py <pdf-folder> [--skip-text] [--only-new]", file=sys.stderr)
        return 2
    folder = Path(args[0]).resolve()
    skip_text = "--skip-text" in args
    only_new = "--only-new" in args
    if not folder.is_dir():
        print(f"not a directory: {folder}", file=sys.stderr)
        return 2

    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        print(f"no PDFs found in {folder}")
        return 0

    notes_before = existing_note_ids()
    BUNDLES.mkdir(parents=True, exist_ok=True)

    ok = 0
    fail = 0
    skipped = 0
    for pdf in pdfs:
        print(f"\n=== {pdf.name}")

        if not skip_text:
            rc, out, err = run([sys.executable, str(TOOLS / "pdf_to_text.py"), str(pdf)])
            if rc != 0:
                print(f"  [text] FAIL: {err.strip()}")
                fail += 1
                continue
            print(f"  [text] {out.strip()}")

        rc, out, err = run([sys.executable, str(TOOLS / "prepare_paper.py"), str(pdf)])
        if rc != 0:
            print(f"  [bundle] FAIL: {err.strip()}")
            fail += 1
            continue
        print(f"  [bundle] {out.strip()}")

        # Parse paper_id from prepare_paper output (first line: "paper_id:    <id>")
        paper_id = ""
        for line in out.splitlines():
            if line.startswith("paper_id:"):
                paper_id = line.split(":", 1)[1].strip()
                break

        if only_new and paper_id and paper_id in notes_before:
            print(f"  [skip] note already exists for {paper_id}")
            skipped += 1
            continue

        ok += 1

    print(f"\nbundles ready: {ok}  failed: {fail}  skipped: {skipped}  total PDFs: {len(pdfs)}")
    print(f"bundles in: {BUNDLES.relative_to(SYNAPSE_ROOT)}")
    print("\nNext: open each bundle in a Claude Code session and produce the note.")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
