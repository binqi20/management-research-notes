#!/usr/bin/env python3
"""
populate_dois.py — fill missing `doi` cells in a manifest via CrossRef title+author search.

Why this exists
---------------
NBS digests (and some other sources) ship as a list of PDFs whose filenames
encode <Author> <Year> <Title>.pdf but rarely embed the DOI. Without a DOI,
the downstream pipeline can't:

  - run Tier 3 (`populate_manifest.py` queries CrossRef BY DOI)
  - run Tier 2 (`verify_metadata.py` cross-checks notes BY DOI)
  - generate a clean BibTeX entry (BibTeX keys are DOI-derived)

This tool does the reverse lookup: given (title, first_author_last, year)
from each manifest row, query CrossRef's `/works?query.title=...&query.author=...`
endpoint and pick the best-scoring candidate. Auto-populate the `doi` column
only when the match is high-confidence; surface ambiguous matches for human
review; leave low-confidence rows untouched.

Scoring (composite weighted score)
----------------------------------
- Title similarity (60% weight): difflib SequenceMatcher.ratio on normalized
  titles (NFKD-folded, lowercased, whitespace-collapsed, HTML tags stripped).
- First-author family-name match (25%): manifest `first_author_last` against
  CrossRef item's first author family (sequence=first). Match after accent-fold.
- Year match (15%): exact match = 1.0, ±1 = 0.7, otherwise 0.

Default thresholds:
  composite >= 0.85 → auto-populate (high confidence)
  0.6 <= composite < 0.85 → surface as needs-manual-review
  composite < 0.6 → no match found

Usage
-----
    python tools/populate_dois.py library/NBS/2026-01/manifest.tsv
        # dry-run: print proposed populations, don't write

    python tools/populate_dois.py library/NBS/2026-01/manifest.tsv --apply
        # write proposed populations back to the manifest (saves backup as .tsv.bak)

    python tools/populate_dois.py library/NBS/2026-01/manifest.tsv --apply --threshold 0.9
        # stricter auto-populate threshold

Exit codes
----------
0: success (regardless of how many DOIs were populated)
2: invocation error (manifest not found, etc.)
"""
from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# Reuse verify_metadata's normalization helpers — single source of truth.
THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))
from verify_metadata import _norm_string, _norm_family_name  # noqa: E402

# macOS-friendly SSL bundle (same as verify_metadata / populate_manifest).
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

USER_AGENT = (
    "Synapse/0.19 (https://github.com/binqi20/management-research-notes; "
    "mailto:binqi20@users.noreply.github.com)"
)

# Separate cache so we don't collide with the DOI-keyed cache used by
# verify_metadata.py and populate_manifest.py.
CACHE_DIR = Path("/tmp/crossref_search_cache")
CACHE_DIR.mkdir(exist_ok=True)

RATE_LIMIT_SLEEP_SECONDS = 0.05  # 20 req/sec — well under CrossRef's 50/sec polite limit


# ---------------------------------------------------------------------------
# CrossRef search
# ---------------------------------------------------------------------------

def search_crossref(title: str, author: str, year: str, rows: int = 5) -> list[dict] | None:
    """Query CrossRef by title+author with year-window filter. Returns items list."""
    # Cache key: title prefix + author + year (full title would blow path limits)
    raw_key = f"{title[:120]}_{author[:30]}_{year}"
    safe_key = urllib.parse.quote(raw_key, safe="")[:250]
    cache_path = CACHE_DIR / f"{safe_key}.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except json.JSONDecodeError:
            cache_path.unlink()  # corrupt, redo

    params = {
        "query.title": title,
        "query.author": author,
        "rows": str(rows),
    }
    # ±1 year window if year is a valid 4-digit integer
    try:
        y = int(year)
        params["filter"] = f"from-pub-date:{y - 1}-01-01,until-pub-date:{y + 1}-12-31"
    except (ValueError, TypeError):
        pass

    url = f"https://api.crossref.org/works?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
            payload = json.loads(resp.read())
    except Exception as e:
        print(f"    WARN: CrossRef search failed for {author} {year} — {e}",
              file=sys.stderr)
        return None

    items = payload.get("message", {}).get("items", [])
    cache_path.write_text(json.dumps(items))
    time.sleep(RATE_LIMIT_SLEEP_SECONDS)
    return items


# ---------------------------------------------------------------------------
# Candidate scoring
# ---------------------------------------------------------------------------

def score_candidate(candidate: dict, target_title: str, target_author: str,
                    target_year: str) -> dict[str, float]:
    """Per-field scores in [0, 1] for a candidate CrossRef item."""
    scores = {"title": 0.0, "author": 0.0, "year": 0.0}

    # Title similarity (fuzzy ratio on normalized strings)
    cand_titles = candidate.get("title") or []
    cand_title = cand_titles[0] if cand_titles else ""
    if cand_title and target_title:
        n_target = _norm_string(target_title)
        n_cand = _norm_string(cand_title)
        scores["title"] = difflib.SequenceMatcher(None, n_target, n_cand).ratio()

    # Author family match (first author)
    cand_authors = candidate.get("author") or []
    if cand_authors and target_author:
        first = next(
            (a for a in cand_authors if a.get("sequence") == "first"),
            cand_authors[0],
        )
        cand_family = first.get("family", "") or ""
        if cand_family:
            n_target = _norm_family_name(target_author)
            n_cand = _norm_family_name(cand_family)
            # Exact match, OR target is contained in candidate (e.g., short
            # form "Krogh" matches compound "von Krogh"), OR vice versa.
            if n_target == n_cand or n_target in n_cand or n_cand in n_target:
                scores["author"] = 1.0

    # Year match (exact or ±1)
    if target_year:
        try:
            target_y = int(target_year)
            cand_y = None
            for field in ("published-print", "issued", "published-online"):
                date_parts = candidate.get(field, {}).get("date-parts", [[None]])
                if date_parts and date_parts[0] and date_parts[0][0]:
                    cand_y = int(date_parts[0][0])
                    break
            if cand_y is not None:
                diff = abs(cand_y - target_y)
                if diff == 0:
                    scores["year"] = 1.0
                elif diff == 1:
                    scores["year"] = 0.7
        except (ValueError, TypeError):
            pass

    return scores


def composite_score(scores: dict[str, float]) -> float:
    """Weighted composite — title dominates."""
    return scores["title"] * 0.6 + scores["author"] * 0.25 + scores["year"] * 0.15


def best_match(items: list[dict], title: str, author: str, year: str
               ) -> tuple[dict | None, dict | None, float]:
    """Return (best_item, scores, composite). (None, None, 0.0) if items empty."""
    best_item, best_scores, best_score = None, None, 0.0
    for item in items:
        scores = score_candidate(item, title, author, year)
        composite = composite_score(scores)
        if composite > best_score:
            best_item, best_scores, best_score = item, scores, composite
    return best_item, best_scores, best_score


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest", help="path to manifest.tsv")
    ap.add_argument("--apply", action="store_true",
                    help="write proposed populations back (default: dry-run)")
    ap.add_argument("--threshold", type=float, default=0.85,
                    help="composite score threshold for auto-populate (default 0.85)")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress per-row output")
    args = ap.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    with manifest_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        cols = reader.fieldnames
        rows = list(reader)

    if "doi" not in cols:
        print(f"manifest does not have a 'doi' column: {manifest_path}", file=sys.stderr)
        return 2

    print(f"Manifest:    {manifest_path}")
    print(f"Rows:        {len(rows)}")
    print(f"Threshold:   {args.threshold}  (composite score for auto-populate)")
    print(f"Mode:        {'APPLY' if args.apply else 'DRY-RUN'}")
    print()

    already_has_doi = []
    populated = []        # composite >= threshold → auto-populated
    needs_review = []     # 0.6 <= composite < threshold
    no_match = []         # composite < 0.6 or fetch failure

    for row in rows:
        if (row.get("doi") or "").strip():
            already_has_doi.append(row)
            continue

        title = (row.get("title") or "").strip()
        author = (row.get("first_author_last") or "").strip()
        year = (row.get("year") or "").strip()

        if not title or not author:
            no_match.append((row, "row missing title or first_author_last"))
            if not args.quiet:
                print(f"  ✗ SKIP   row missing title/author: {row.get('saved_filename', '?')[:60]}")
            continue

        items = search_crossref(title, author, year)
        if items is None:
            no_match.append((row, "CrossRef fetch failed"))
            continue
        if not items:
            no_match.append((row, "no candidates returned"))
            if not args.quiet:
                print(f"  ✗ NONE   no candidates: {author} {year}  {title[:60]}")
            continue

        item, scores, composite = best_match(items, title, author, year)
        label = f"{author} {year}: {title[:55]}"

        if composite >= args.threshold:
            populated.append((row, item, scores, composite))
            row["doi"] = item.get("DOI", "")
            if not args.quiet:
                print(f"  ✓ AUTO   ({composite:.2f})  {label}")
                print(f"           → {item.get('DOI')}")
        elif composite >= 0.6:
            needs_review.append((row, item, scores, composite))
            if not args.quiet:
                print(f"  ⚠ REVIEW ({composite:.2f})  {label}")
                print(f"           Top candidate: {item.get('DOI', '?')}")
                print(f"           t={scores['title']:.2f} a={scores['author']:.2f} y={scores['year']:.2f}")
        else:
            no_match.append((row, f"low confidence ({composite:.2f})"))
            if not args.quiet:
                print(f"  ✗ LOW    ({composite:.2f})  {label}")

    # Write back if --apply and we have populations
    if args.apply and populated:
        backup = manifest_path.with_suffix(".tsv.dois.bak")
        manifest_path.rename(backup)
        with manifest_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({c: row.get(c, "") for c in cols})
        print(f"\nWrote {len(populated)} new DOIs. Backup: {backup.name}")

    # Summary
    print()
    print("=" * 60)
    print(f"  Already had DOI:        {len(already_has_doi):4d}")
    print(f"  Auto-populated:         {len(populated):4d}  (composite >= {args.threshold})")
    print(f"  Needs manual review:    {len(needs_review):4d}  (0.6 ≤ composite < {args.threshold})")
    print(f"  No match found:         {len(no_match):4d}  (composite < 0.6 or error)")
    print(f"  Total rows:             {len(rows):4d}")
    if not args.apply and populated:
        print(f"\nDRY-RUN: no changes written. Re-run with --apply to populate.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
