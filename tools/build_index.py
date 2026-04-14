#!/usr/bin/env python3
"""
build_index.py — rebuild index/synapse.db from every note in notes/.

The database is fully derived. This script can be re-run any time without losing
data — it drops the tables, re-creates them from .synapse/schema.sql, and walks
notes/ in alphabetical order.

Usage:
  python tools/build_index.py
  python tools/build_index.py --note notes/nbs-2026-02-spoor-2026.md   # upsert one
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

import yaml

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
NOTES = SYNAPSE_ROOT / "notes"
INDEX_DIR = SYNAPSE_ROOT / "index"
DB = INDEX_DIR / "synapse.db"
SCHEMA = SYNAPSE_ROOT / ".synapse" / "schema.sql"


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("note must start with '---' YAML frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("YAML frontmatter is not terminated with '---'")
    fm = yaml.safe_load(text[4:end]) or {}
    body = text[end + 5 :]
    return fm, body


def parse_body_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    parts = re.split(r"^\*\*([^*]+)\*\*\s*\n", body, flags=re.MULTILINE)
    i = 1
    while i + 1 < len(parts):
        sections[parts[i].strip()] = parts[i + 1].strip()
        i += 2
    return sections


def first_match(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def parse_mechanism_block(text: str) -> dict[str, str]:
    return {
        "iv": first_match(text, r"IV\(s\):\s*(.+)") or "",
        "dv": first_match(text, r"DV\(s\):\s*(.+)") or "",
        "mediators": first_match(text, r"Mediators:\s*(.+)") or "",
        "moderators": first_match(text, r"Moderators:\s*(.+)") or "",
    }


def upsert_note(conn: sqlite3.Connection, note_path: Path) -> None:
    text = note_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    sections = parse_body_sections(body)
    paper_id = fm["id"]
    sample = fm.get("sample") or {}

    mech_text = sections.get("Mechanism Process", "")
    mech_parts = parse_mechanism_block(mech_text)
    # The narrative summary is whatever's left after the IV/DV/Mediator/Moderator bullets.
    summary_lines = [
        line for line in mech_text.splitlines()
        if not re.match(r"^\s*[-*]?\s*(IV|DV|Mediators|Moderators)", line)
    ]
    mechanism_summary = "\n".join(summary_lines).strip()

    apa = sections.get("APA 7th Citation", "")

    # Replace any existing rows for this paper.
    conn.execute("DELETE FROM papers   WHERE id = ?", (paper_id,))
    conn.execute("DELETE FROM authors  WHERE paper_id = ?", (paper_id,))
    conn.execute("DELETE FROM theories WHERE paper_id = ?", (paper_id,))
    conn.execute("DELETE FROM keywords WHERE paper_id = ?", (paper_id,))
    conn.execute("DELETE FROM topics   WHERE paper_id = ?", (paper_id,))
    conn.execute("DELETE FROM papers_fts WHERE id = ?", (paper_id,))

    conn.execute(
        """
        INSERT INTO papers (
            id, title, year, journal, doi, volume, issue, pages,
            paper_type, methods, industry, country, time_period, units, n_sample,
            research_question, mechanism_summary, iv, dv, mediators, moderators,
            theoretical_contribution, practical_implication, limitations,
            future_research, abstract, apa_citation,
            unit_of_analysis, level_of_theory, dependent_variable_family,
            source, pdf_path, text_path, note_path,
            extraction_model, extraction_version, ingested_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                  ?, ?, ?, ?, ?, ?, ?,
                  ?, ?, ?, ?, ?, ?,
                  ?, ?, ?,
                  ?, ?, ?,
                  ?, ?, ?,
                  ?, ?, ?, ?,
                  ?, ?, ?)
        """,
        (
            paper_id,
            fm.get("title"),
            fm.get("year"),
            fm.get("journal"),
            fm.get("doi"),
            str(fm.get("volume")) if fm.get("volume") is not None else None,
            str(fm.get("issue")) if fm.get("issue") is not None else None,
            fm.get("pages"),
            fm.get("paper_type"),
            fm.get("methods"),
            sample.get("industry"),
            sample.get("country"),
            sample.get("time_period"),
            sample.get("units"),
            sample.get("n"),
            sections.get("Research Question"),
            mechanism_summary,
            mech_parts["iv"],
            mech_parts["dv"],
            mech_parts["mediators"],
            mech_parts["moderators"],
            sections.get("Theoretical Contribution"),
            sections.get("Practical Implication"),
            sections.get("Limitations"),
            sections.get("Future Research"),
            sections.get("Abstract"),
            apa,
            fm.get("unit_of_analysis"),
            fm.get("level_of_theory"),
            fm.get("dependent_variable_family"),
            fm.get("source"),
            fm.get("pdf_path"),
            fm.get("text_path"),
            str(note_path.relative_to(SYNAPSE_ROOT)),
            fm.get("extraction_model"),
            fm.get("extraction_version"),
            fm.get("ingested_at"),
        ),
    )

    for i, name in enumerate(fm.get("authors") or []):
        conn.execute(
            "INSERT INTO authors (paper_id, position, name) VALUES (?, ?, ?)",
            (paper_id, i, name),
        )
    for theory in fm.get("theory") or []:
        conn.execute(
            "INSERT OR IGNORE INTO theories (paper_id, theory) VALUES (?, ?)",
            (paper_id, theory),
        )
    for kw in fm.get("keywords") or []:
        conn.execute(
            "INSERT OR IGNORE INTO keywords (paper_id, keyword) VALUES (?, ?)",
            (paper_id, kw),
        )
    for topic in fm.get("topics") or []:
        conn.execute(
            "INSERT OR IGNORE INTO topics (paper_id, topic) VALUES (?, ?)",
            (paper_id, topic),
        )

    conn.execute(
        """
        INSERT INTO papers_fts (
            id, title, abstract, research_question,
            mechanism_summary, theoretical_contribution, practical_implication
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper_id,
            fm.get("title"),
            sections.get("Abstract"),
            sections.get("Research Question"),
            mechanism_summary,
            sections.get("Theoretical Contribution"),
            sections.get("Practical Implication"),
        ),
    )


def reset_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS papers_fts;
        DROP TABLE IF EXISTS topics;
        DROP TABLE IF EXISTS keywords;
        DROP TABLE IF EXISTS theories;
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS papers;
        """
    )
    conn.executescript(SCHEMA.read_text())


def main() -> int:
    args = sys.argv[1:]
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")

    if "--note" in args:
        idx = args.index("--note")
        note_path = Path(args[idx + 1]).resolve()
        # Make sure tables exist (don't reset).
        conn.executescript(SCHEMA.read_text())
        upsert_note(conn, note_path)
        conn.commit()
        print(f"upserted: {note_path.relative_to(SYNAPSE_ROOT)}")
    else:
        reset_db(conn)
        notes = sorted(NOTES.glob("*.md"))
        for note_path in notes:
            upsert_note(conn, note_path)
        conn.commit()
        print(f"indexed {len(notes)} notes")
        cur = conn.execute("SELECT COUNT(*) FROM papers")
        print(f"papers in db: {cur.fetchone()[0]}")
        cur = conn.execute(
            "SELECT theory, COUNT(*) FROM theories GROUP BY theory ORDER BY 2 DESC LIMIT 5"
        )
        rows = cur.fetchall()
        if rows:
            print("top theories:")
            for theory, n in rows:
                print(f"  {n:3d}  {theory}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
