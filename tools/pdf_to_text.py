#!/usr/bin/env python3
"""
pdf_to_text.py — extract plain text from a PDF and write it next to the canonical
text/ folder for its source/issue.

Strategy:
  1. Try `pdftotext` (poppler) with the -layout flag. Fast, accurate for most journals.
  2. If pdftotext is missing or the result is suspiciously short, fall back to
     pdfplumber (pure Python).
  3. Normalize whitespace minimally: strip form feeds, collapse runs of blank lines.

Usage:
  python tools/pdf_to_text.py <path-to-pdf>
  python tools/pdf_to_text.py library/NBS/2026-02/pdfs/Spoor\\ 2026\\ A\\ Design\\ for\\ All...pdf

Output:
  Writes a sibling .txt file under .../text/ matching the PDF basename, and prints
  the output path + character count.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

MIN_REASONABLE_CHARS = 1500   # below this we suspect a scanned/image-only PDF


def extract_with_pdftotext(pdf: Path) -> str | None:
    if shutil.which("pdftotext") is None:
        return None
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"[pdftotext] failed: {exc.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout


def extract_with_pdfplumber(pdf: Path) -> str | None:
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        print("[pdfplumber] not installed; cannot fall back", file=sys.stderr)
        return None
    pages: list[str] = []
    with pdfplumber.open(str(pdf)) as pdf_obj:
        for page in pdf_obj.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n\n".join(pages)


def normalize(text: str) -> str:
    # Drop form feeds and trailing whitespace; collapse 3+ blank lines to 2.
    text = text.replace("\x0c", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    # Reunite words broken by line-wrap hyphenation: "neurodiver-\n     sity" → "neurodiversity".
    # Only triggers when there is actual whitespace after the hyphen (i.e. a line break),
    # so genuine compounds like "self-report" are left alone.
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def derive_text_path(pdf: Path) -> Path:
    """
    Map .../{Source}/{Year-Month}/pdfs/foo.pdf -> .../{Source}/{Year-Month}/text/foo.txt
    For PDFs outside the library layout (e.g. incoming/), write next to the PDF.
    """
    if pdf.parent.name == "pdfs":
        text_dir = pdf.parent.parent / "text"
        text_dir.mkdir(parents=True, exist_ok=True)
        return text_dir / (pdf.stem + ".txt")
    return pdf.with_suffix(".txt")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: pdf_to_text.py <pdf>", file=sys.stderr)
        return 2

    pdf = Path(sys.argv[1]).resolve()
    if not pdf.exists() or pdf.suffix.lower() != ".pdf":
        print(f"not a pdf: {pdf}", file=sys.stderr)
        return 2

    text = extract_with_pdftotext(pdf)
    if text is None or len(text) < MIN_REASONABLE_CHARS:
        if text is not None:
            print(
                f"[pdftotext] yielded only {len(text)} chars; falling back to pdfplumber",
                file=sys.stderr,
            )
        text = extract_with_pdfplumber(pdf)

    if not text:
        print("[error] both extractors failed or returned empty", file=sys.stderr)
        return 1

    text = normalize(text)
    out = derive_text_path(pdf)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}  ({len(text):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
