#!/usr/bin/env python3
"""
export_csv.py — produce index/papers.csv, a flat tabular view of the library
suitable for opening in Excel / R / pandas.

One row per paper, joining the top-level papers table with the authors, theories,
topics, and keywords tables (collapsed to semicolon-separated strings). All columns
are strings to keep the CSV uniform.

Usage:
  python tools/export_csv.py
  python tools/export_csv.py --out index/papers.csv
"""

from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
INDEX = SYNAPSE_ROOT / "index"
DB = INDEX / "synapse.db"
DEFAULT_OUT = INDEX / "papers.csv"


COLUMNS = [
    "id", "title", "year", "journal", "doi",
    "paper_type", "unit_of_analysis", "level_of_theory", "dependent_variable_family",
    "methods", "industry", "country", "time_period", "units", "n_sample",
    "authors", "theories", "topics", "keywords",
    "research_question", "mechanism_summary",
    "theoretical_contribution", "practical_implication",
    "limitations", "future_research", "abstract", "apa_citation",
    "source", "pdf_path", "text_path", "note_path",
    "extraction_model", "extraction_version", "ingested_at",
]


def semi(rows: list[tuple]) -> str:
    return "; ".join(r[0] for r in rows)


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
    papers = conn.execute("SELECT * FROM papers ORDER BY year DESC, id").fetchall()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for p in papers:
            pid = p["id"]
            authors = conn.execute(
                "SELECT name FROM authors WHERE paper_id = ? ORDER BY position", (pid,)
            ).fetchall()
            theories = conn.execute(
                "SELECT theory FROM theories WHERE paper_id = ? ORDER BY theory", (pid,)
            ).fetchall()
            topics = conn.execute(
                "SELECT topic FROM topics WHERE paper_id = ? ORDER BY topic", (pid,)
            ).fetchall()
            keywords = conn.execute(
                "SELECT keyword FROM keywords WHERE paper_id = ? ORDER BY keyword", (pid,)
            ).fetchall()
            row = dict(p)
            row["authors"] = semi(authors)
            row["theories"] = semi(theories)
            row["topics"] = semi(topics)
            row["keywords"] = semi(keywords)
            writer.writerow(row)

    conn.close()
    print(f"wrote {out_path.relative_to(SYNAPSE_ROOT)}  ({len(papers)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
