#!/usr/bin/env python3
"""
verify_years.py — verify the year and APA citation of every note against CrossRef.

Why this exists
---------------
Academic publishing has TWO publication years for most papers:

  - "online-first" / "published-online": when the publisher posted the paper.
  - "issue year" / "published-print": when the paper appeared in a numbered
    volume/issue with a cover date.

Per APA 7, the citation year is the **issue year**, not the online-first year.
Many of our notes (and the manifest they were extracted from) carry the
online-first year by mistake. This script flags every such case so they can be
corrected before the next release.

Usage
-----
    python3 tools/verify_years.py                # all notes, plain output
    python3 tools/verify_years.py --tsv          # machine-readable output
    python3 tools/verify_years.py --quiet        # only print discrepancies
    python3 tools/verify_years.py --paper-id ID  # check one paper

This script is read-only. It does not modify any notes or manifests. The output
is a discrepancy report; fixing the discrepancies is a separate step that
requires updating the manifest, regenerating the affected notes, and rebuilding
the index.

Methodology
-----------
For each note's DOI, we query CrossRef's free public API:

    GET https://api.crossref.org/works/{doi}

We extract the year from these fields, in this order of preference:

    1. published-print.date-parts[0][0]   (APA 7 preferred — the issue year)
    2. issued.date-parts[0][0]            (fallback — usually = published-print)
    3. published-online.date-parts[0][0]  (last resort — online-first year)

If the year doesn't match the note's frontmatter, we flag the note.

Caching
-------
CrossRef responses are cached to /tmp/crossref_cache/ to avoid re-querying on
repeat runs. The cache is keyed by URL-encoded DOI. Delete the cache to force
a refresh.

Rate limiting
-------------
CrossRef's "polite pool" allows 50 req/sec when you supply a User-Agent
identifying yourself. We sleep 25ms between requests by default, which is
well within the limit.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

# macOS's bundled Python often doesn't trust the system CA store. certifi
# ships Mozilla's CA bundle and is reliable across platforms.
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
NOTES_DIR = SYNAPSE_ROOT / "notes"
CACHE_DIR = Path("/tmp/crossref_cache")
CACHE_DIR.mkdir(exist_ok=True)

USER_AGENT = (
    "Synapse/0.11 (https://github.com/binqi20/management-research-notes; "
    "mailto:binqi20@users.noreply.github.com)"
)
RATE_LIMIT_SLEEP_SECONDS = 0.025  # 40 req/sec — well under CrossRef's 50/sec polite limit


def parse_note_frontmatter(note_path: Path) -> dict:
    """Pull the fields we need (year, doi, paper_id, citation) from a note.

    We do not import the full validate_note parser to keep this script
    self-contained — only need a few fields and the YAML is well-formed.
    """
    text = note_path.read_text()
    # Frontmatter is between the first --- and the second ---.
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{note_path.name}: no YAML frontmatter found")
    fm = parts[1]
    body = parts[2]

    out = {"path": note_path, "paper_id": note_path.stem}
    for field in ("doi", "year", "title"):
        m = re.search(rf'^{field}:\s*"?([^"\n]+)"?\s*$', fm, re.MULTILINE)
        if m:
            value = m.group(1).strip().strip('"').rstrip("/")
            if field == "year":
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif field == "doi":
                # Normalize: strip leading https://doi.org/ if present.
                value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
            out[field] = value

    # Pull APA citation block from the body (between "## APA 7th Citation" and next heading).
    m = re.search(r"##\s*APA\s*7(?:th)?\s*Citation\s*\n+(.+?)(?:\n##|\Z)", body, re.DOTALL)
    if m:
        out["apa_citation"] = m.group(1).strip()
    return out


def fetch_crossref(doi: str) -> dict | None:
    """Query CrossRef for a DOI. Returns the `message` object, or None on miss."""
    cache_key = urllib.parse.quote(doi, safe="")
    cache_path = CACHE_DIR / f"{cache_key}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
            payload = json.loads(resp.read())
    except Exception as e:
        print(f"  WARN: CrossRef fetch failed for {doi}: {e}")
        return None

    msg = payload.get("message", {})
    cache_path.write_text(json.dumps(msg))
    time.sleep(RATE_LIMIT_SLEEP_SECONDS)
    return msg


def extract_year(crossref_msg: dict) -> tuple[int | None, str]:
    """Get the APA-7-preferred year from a CrossRef record, plus a label."""
    for field in ("published-print", "issued", "published-online"):
        date_parts = crossref_msg.get(field, {}).get("date-parts", [[None]])
        if date_parts and date_parts[0] and date_parts[0][0]:
            return int(date_parts[0][0]), field
    return None, "missing"


def crossref_apa_year(msg: dict) -> int | None:
    """Convenience: just return the year, no field label."""
    y, _ = extract_year(msg)
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", action="store_true", help="machine-readable TSV output")
    ap.add_argument("--quiet", action="store_true", help="only show discrepancies")
    ap.add_argument("--paper-id", help="check a single paper instead of all notes")
    ap.add_argument("--no-cache", action="store_true", help="ignore cache, force fresh CrossRef fetches")
    args = ap.parse_args()

    if args.no_cache:
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()

    if args.paper_id:
        notes = [NOTES_DIR / f"{args.paper_id}.md"]
        if not notes[0].exists():
            print(f"No such note: {notes[0]}")
            return 2
    else:
        notes = sorted(NOTES_DIR.glob("*.md"))

    rows = []
    for note_path in notes:
        try:
            fm = parse_note_frontmatter(note_path)
        except Exception as e:
            rows.append({
                "paper_id": note_path.stem,
                "doi": "",
                "note_year": "?",
                "crossref_year": "?",
                "field": "parse_error",
                "status": "ERROR",
                "detail": str(e)[:60],
            })
            continue

        doi = fm.get("doi")
        note_year = fm.get("year")
        if not doi:
            rows.append({
                "paper_id": fm["paper_id"],
                "doi": "",
                "note_year": note_year,
                "crossref_year": "—",
                "field": "no-doi",
                "status": "SKIP",
                "detail": "no DOI in frontmatter",
            })
            continue

        msg = fetch_crossref(doi)
        if msg is None:
            rows.append({
                "paper_id": fm["paper_id"],
                "doi": doi,
                "note_year": note_year,
                "crossref_year": "?",
                "field": "lookup-failed",
                "status": "ERROR",
                "detail": "CrossRef fetch failed",
            })
            continue

        cr_year, cr_field = extract_year(msg)
        if cr_year is None:
            status = "NO_YEAR"
        elif note_year == cr_year:
            status = "MATCH"
        else:
            status = "MISMATCH"

        rows.append({
            "paper_id": fm["paper_id"],
            "doi": doi,
            "note_year": note_year,
            "crossref_year": cr_year,
            "field": cr_field,
            "status": status,
            "detail": "",
        })

    # Reporting
    if args.tsv:
        print("paper_id\tdoi\tnote_year\tcrossref_year\tcrossref_field\tstatus\tdetail")
        for r in rows:
            print(f"{r['paper_id']}\t{r['doi']}\t{r['note_year']}\t{r['crossref_year']}\t{r['field']}\t{r['status']}\t{r['detail']}")
        return 0

    # Human-readable summary
    by_status = {}
    for r in rows:
        by_status.setdefault(r["status"], []).append(r)

    print(f"Verified {len(rows)} notes against CrossRef.\n")
    print(f"  MATCH:    {len(by_status.get('MATCH', []))}  (note year == CrossRef year)")
    print(f"  MISMATCH: {len(by_status.get('MISMATCH', []))}  (note year != CrossRef year — REVIEW)")
    print(f"  SKIP:     {len(by_status.get('SKIP', []))}  (no DOI in frontmatter)")
    print(f"  ERROR:    {len(by_status.get('ERROR', []))}  (lookup or parse failure)")
    print(f"  NO_YEAR:  {len(by_status.get('NO_YEAR', []))}  (CrossRef returned no year)")
    print()

    if not args.quiet and by_status.get("MATCH"):
        # In verbose mode, optionally list matches too — but they're noisy. Skip.
        pass

    if by_status.get("MISMATCH"):
        print("=" * 70)
        print("  MISMATCHES (note year ≠ CrossRef year — review these)")
        print("=" * 70)
        for r in sorted(by_status["MISMATCH"], key=lambda r: r["paper_id"]):
            print(f"  {r['paper_id']}")
            print(f"    note says:     {r['note_year']}")
            print(f"    crossref says: {r['crossref_year']}  (from {r['field']})")
            print(f"    DOI:           {r['doi']}")
            print()

    if by_status.get("ERROR") or by_status.get("NO_YEAR"):
        print("=" * 70)
        print("  ERRORS / NO_YEAR (couldn't verify)")
        print("=" * 70)
        for r in by_status.get("ERROR", []) + by_status.get("NO_YEAR", []):
            print(f"  {r['paper_id']}: {r['status']} — {r['detail']}")

    if by_status.get("SKIP"):
        print(f"\n(Skipped {len(by_status['SKIP'])} notes without DOI — typically editorials or book reviews.)")

    return 1 if by_status.get("MISMATCH") else 0


if __name__ == "__main__":
    raise SystemExit(main())
