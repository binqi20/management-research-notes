#!/usr/bin/env python3
"""
export_bibtex.py — produce index/library.bib, a BibTeX file with one @article
entry per paper in the library. Use when drafting literature reviews in
Word / LaTeX / Typst / anywhere that consumes BibTeX.

BibTeX key = paper_id (stable, e.g. nbs-2026-02-spoor-2026). Author names are
joined with ' and '. Title is wrapped in {{...}} to preserve capitalization.

Usage:
  python tools/export_bibtex.py
  python tools/export_bibtex.py --out index/library.bib
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
INDEX = SYNAPSE_ROOT / "index"
DB = INDEX / "synapse.db"
DEFAULT_OUT = INDEX / "library.bib"


def escape_bibtex(value: str | None) -> str:
    if value is None:
        return ""
    # Minimal BibTeX escaping — percent, ampersand, underscore, hash, dollar.
    # Inside {{...}}, braces protect most chars; we only escape % and comments.
    return (
        value.replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("$", r"\$")
        .replace("_", r"\_")
    )


def normalize_doi(doi: str | None) -> str:
    if not doi:
        return ""
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)


def main() -> int:
    args = sys.argv[1:]
    out_path = DEFAULT_OUT
    if "--out" in args:
        out_path = Path(args[args.index("--out") + 1]).resolve()

    if not DB.exists():
        print(f"database not found: {DB}. run tools/build_index.py first", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    papers = conn.execute("SELECT * FROM papers ORDER BY id").fetchall()

    entries: list[str] = []
    for p in papers:
        pid = p["id"]
        authors = [
            r["name"]
            for r in conn.execute(
                "SELECT name FROM authors WHERE paper_id = ? ORDER BY position", (pid,)
            )
        ]
        author_field = " and ".join(authors) if authors else ""

        fields = [
            ("title", f"{{{escape_bibtex(p['title'])}}}"),
            ("author", escape_bibtex(author_field)),
            ("journal", escape_bibtex(p["journal"]) if p["journal"] else ""),
            ("year", str(p["year"]) if p["year"] else ""),
            ("volume", escape_bibtex(p["volume"]) if p["volume"] else ""),
            ("number", escape_bibtex(p["issue"]) if p["issue"] else ""),
            ("pages", escape_bibtex(p["pages"]) if p["pages"] else ""),
            ("doi", normalize_doi(p["doi"])),
        ]
        # Drop empty-string fields (keep `title` and `year` even if odd).
        body_lines = [
            f"  {k} = {{{v}}}," for k, v in fields if v
        ]
        entry = "\n".join(
            [f"@article{{{pid},"] + body_lines + ["}"]
        )
        entries.append(entry)

    conn.close()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "% Synapse library. Derived from notes/. Regenerate with tools/export_bibtex.py.\n\n"
        + "\n\n".join(entries)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path.relative_to(SYNAPSE_ROOT)}  ({len(papers)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
