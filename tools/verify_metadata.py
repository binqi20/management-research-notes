#!/usr/bin/env python3
"""
verify_metadata.py — verify every note's bibliographic metadata against CrossRef.

Why this exists
---------------
The `manifest.tsv` files under `library/.../` are treated as the trusted source
of bibliographic metadata (per CLAUDE.md hard rule 1). But manifests are
populated by hand from journal TOCs and publisher websites, which means the
manifest itself is not automatically validated against any external authority.

v0.11.1 fixed 48 issue-year mismatches (27% of the library) where the manifest
had silently stored the *online-first* year instead of the APA-7-required
*issue year*. This tool extends that check to every bibliographic field
CrossRef returns:

  - year     (issue year per APA 7, via `published-print` > `issued`)
  - title
  - journal  (CrossRef field: container-title)
  - volume
  - issue
  - pages
  - authors  (family-name match in order)

Usage
-----
    python3 tools/verify_metadata.py                       # all fields, all notes
    python3 tools/verify_metadata.py --field year          # back-compat: years only
    python3 tools/verify_metadata.py --field year,title    # subset
    python3 tools/verify_metadata.py --tsv                 # machine-readable
    python3 tools/verify_metadata.py --quiet               # mismatches only
    python3 tools/verify_metadata.py --paper-id ID         # single paper
    python3 tools/verify_metadata.py --no-cache            # bypass cache

This tool is read-only. It reports discrepancies; fixing them is a separate
manual step (update the manifest, re-run extraction, rebuild indexes).

Methodology
-----------
For each note's DOI, query CrossRef's free public API:

    GET https://api.crossref.org/works/{doi}

Compare each selected field against the note's frontmatter using per-field
normalization (whitespace, smart quotes, em/en-dashes, HTML entities, accents).
The normalization is deliberately tolerant so we don't drown in false positives
from format-only differences — but tight enough that real errors surface.

Caching
-------
CrossRef responses are cached to /tmp/crossref_cache/ to avoid re-querying on
repeat runs. Cache is keyed by URL-encoded DOI. Use `--no-cache` to refresh.

Exit code
---------
0 if all selected fields match for all checked notes.
1 if any mismatch was found (suitable for use as a pipeline gate).
2 if invocation was malformed (e.g., unknown --paper-id).

Compatibility note
------------------
This tool supersedes `verify_years.py`. The `--field year` mode produces
identical year-only output for back-compat with anything that parsed the
old tool's TSV.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from html import unescape
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

# Fields we know how to compare. Order is the report order.
ALL_FIELDS = ("year", "title", "journal", "volume", "issue", "pages", "authors")

# Known CrossRef-side data errors. Mismatches matching (paper_id, field)
# entries here are reported as KNOWN_FP rather than MISMATCH, so the gate
# stays clean. Add entries here only after manually confirming that the
# CrossRef record itself is wrong (not the note). Each entry must include
# a dated rationale so future maintainers can re-verify whether the
# upstream record has since been fixed.
#
# TODO: migrate to a JSON file (e.g. tools/known_crossref_issues.json)
# if this list grows past ~5 entries — at that point the source-code
# edits feel more like data updates than code changes.
KNOWN_CROSSREF_DATA_ERRORS: dict[str, dict[str, str]] = {
    "nbs-2026-02-reinecke-2026": {
        "title": (
            "CrossRef record duplicates the title and embeds the author "
            "name mid-string ('...PaulKalpita Bhar. Ecophenomenology and "
            "the Environmental Crisis in the Sundarbans...'). The note's "
            "title matches the PDF correctly. Suppressed 2026-05-09."
        ),
    },
    "amj-vol-67-no-2-liao-2024": {
        "authors": (
            "CrossRef stores the last author as family='Man Tang', given='Pok' "
            "(Cantonese-romanization compound-surname interpretation). The PDF "
            "byline reads 'POK MAN TANG' and the journal's own running header "
            "uses 'Tang' as the family name throughout. The note matches the "
            "PDF + the journal convention. Suppressed 2026-05-10."
        ),
    },
}


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def _norm_string(s: str) -> str:
    """Generic string normalization for bibliographic fields.

    Collapses all whitespace (including non-breaking space \xa0) to single
    spaces, replaces smart quotes / em-dashes / en-dashes with their ASCII
    equivalents, decodes HTML entities, strips trailing punctuation, and
    lowercases. Tolerant of format-only differences but tight enough that
    real wording errors still surface.
    """
    if s is None:
        return ""
    s = unescape(s)  # &amp; -> &, &#x2014; -> em-dash
    # Strip HTML/XML tags. CrossRef titles use these for typesetting
    # hints (italicized journal name in editorial titles, italicized
    # foreign-language words in body, etc.) that manifests strip out.
    s = re.sub(r"<[^>]+>", "", s)
    # Add U+2010 HYPHEN -> ASCII (CrossRef sometimes emits the proper
    # Unicode hyphen; manifests use ASCII hyphen-minus). Also U+2011,
    # U+2012, U+2015, U+2212 for completeness.
    s = s.replace("‐", "-").replace("‑", "-").replace("‒", "-")
    s = s.replace("―", "-").replace("−", "-")
    # Smart quotes & dashes -> ASCII
    translations = str.maketrans({
        "‘": "'", "’": "'", "‚": "'", "‛": "'",
        "“": '"', "”": '"', "„": '"', "‟": '"',
        "–": "-", "—": "-", "―": "-",
        " ": " ", " ": " ", " ": " ", "​": "",
    })
    s = s.translate(translations)
    # Collapse whitespace runs to single space
    s = re.sub(r"\s+", " ", s).strip()
    # Strip trailing terminal punctuation
    s = s.rstrip(".;,:")
    return s.lower()


def _norm_pages(s: str) -> str | None:
    """Pages -> 'first-last' canonical form, or None if unparseable.

    Handles full ('725-748'), compressed ('725-48'), en-dash ('725–748'),
    and single-page ('742') variants.
    """
    if s is None:
        return None
    s = str(s).strip()
    # Replace en/em dashes with hyphens
    s = re.sub(r"[–—―]", "-", s)
    nums = re.findall(r"\d+", s)
    if not nums:
        return None
    if len(nums) == 1:
        return nums[0]
    first, last = nums[0], nums[-1]
    # Expand compressed last-page ('725-48' -> '725-748')
    if len(last) < len(first):
        last = first[: len(first) - len(last)] + last
    return f"{first}-{last}"


def _norm_int_str(v) -> str:
    """Normalize a value that's expected to be an int-like string (volume, issue)."""
    if v is None:
        return ""
    s = str(v).strip()
    # Strip leading zeros if it's purely numeric
    if s.isdigit():
        s = str(int(s))
    return s.lower()


def _fold_accents(s: str) -> str:
    """Strip accents/diacritics for accent-tolerant author family-name match."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )


def _norm_family_name(s: str) -> str:
    """Normalize author family name for comparison."""
    return _fold_accents(_norm_string(s))


# ---------------------------------------------------------------------------
# Note frontmatter parsing
# ---------------------------------------------------------------------------

def parse_note_frontmatter(note_path: Path) -> dict:
    """Pull the bibliographic fields we need from a note's YAML frontmatter.

    Uses PyYAML so that escape sequences like `\\u201C` (smart quote)
    resolve to their actual Unicode character. A naive regex parser
    would capture the literal 6 characters and falsely flag titles
    that are perfectly valid YAML — discovered the hard way during
    the v0.11.2 cleanup pass on Lazar 2025.
    """
    import yaml

    text = note_path.read_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{note_path.name}: no YAML frontmatter found")
    fm_dict = yaml.safe_load(parts[1]) or {}

    out = {"path": note_path, "paper_id": note_path.stem}
    for field in ("title", "journal", "volume", "issue", "pages", "year"):
        if field in fm_dict:
            out[field] = fm_dict[field]
    if "doi" in fm_dict:
        out["doi"] = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(fm_dict["doi"]).rstrip("/"))
    if "authors" in fm_dict and isinstance(fm_dict["authors"], list):
        out["authors"] = [str(a) for a in fm_dict["authors"]]
    else:
        out["authors"] = []
    return out


# ---------------------------------------------------------------------------
# CrossRef
# ---------------------------------------------------------------------------

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
        print(f"  WARN: CrossRef fetch failed for {doi}: {e}", file=sys.stderr)
        return None

    msg = payload.get("message", {})
    cache_path.write_text(json.dumps(msg))
    time.sleep(RATE_LIMIT_SLEEP_SECONDS)
    return msg


def crossref_year(msg: dict) -> tuple[int | None, str]:
    """Get the APA-7-preferred year, plus the source field label."""
    for field in ("published-print", "issued", "published-online"):
        date_parts = msg.get(field, {}).get("date-parts", [[None]])
        if date_parts and date_parts[0] and date_parts[0][0]:
            return int(date_parts[0][0]), field
    return None, "missing"


def crossref_title(msg: dict) -> str | None:
    titles = msg.get("title") or []
    return titles[0] if titles else None


def crossref_journal(msg: dict) -> str | None:
    cts = msg.get("container-title") or []
    return cts[0] if cts else None


def crossref_authors(msg: dict) -> list[str]:
    """Return list of family names in CrossRef order."""
    return [a.get("family", "") for a in (msg.get("author") or [])]


# ---------------------------------------------------------------------------
# Field-level comparison
# ---------------------------------------------------------------------------

def compare_field(field: str, note_val, cr_msg: dict) -> tuple[str, str, str]:
    """Compare one field. Returns (status, note_repr, crossref_repr).

    status is one of: MATCH, MISMATCH, MISSING (CrossRef has no value).
    """
    if field == "year":
        cr, src = crossref_year(cr_msg)
        if cr is None:
            return "MISSING", str(note_val), f"— ({src})"
        if note_val == cr:
            return "MATCH", str(note_val), f"{cr} ({src})"
        return "MISMATCH", str(note_val), f"{cr} ({src})"

    if field == "title":
        cr = crossref_title(cr_msg)
        if cr is None:
            return "MISSING", str(note_val or ""), "—"
        if _norm_string(note_val or "") == _norm_string(cr):
            return "MATCH", note_val or "", cr
        return "MISMATCH", note_val or "", cr

    if field == "journal":
        cr = crossref_journal(cr_msg)
        if cr is None:
            return "MISSING", str(note_val or ""), "—"
        if _norm_string(note_val or "") == _norm_string(cr):
            return "MATCH", note_val or "", cr
        return "MISMATCH", note_val or "", cr

    if field == "volume":
        cr = cr_msg.get("volume")
        if cr is None:
            return "MISSING", str(note_val or ""), "—"
        if _norm_int_str(note_val) == _norm_int_str(cr):
            return "MATCH", str(note_val), str(cr)
        return "MISMATCH", str(note_val), str(cr)

    if field == "issue":
        cr = cr_msg.get("issue")
        if cr is None:
            return "MISSING", str(note_val or ""), "—"
        if _norm_int_str(note_val) == _norm_int_str(cr):
            return "MATCH", str(note_val), str(cr)
        return "MISMATCH", str(note_val), str(cr)

    if field == "pages":
        cr = cr_msg.get("page")
        if cr is None:
            return "MISSING", str(note_val or ""), "—"
        n_norm = _norm_pages(note_val)
        c_norm = _norm_pages(cr)
        if n_norm and c_norm and n_norm == c_norm:
            return "MATCH", str(note_val), str(cr)
        return "MISMATCH", str(note_val), str(cr)

    if field == "authors":
        cr_families = crossref_authors(cr_msg)
        if not cr_families:
            return "MISSING", " ".join(note_val or []), "—"
        # Extract family names from "Family, G. I." note format
        note_families = []
        for a in (note_val or []):
            fam = a.split(",")[0].strip() if "," in a else a.strip().split()[-1]
            note_families.append(fam)
        if len(note_families) != len(cr_families):
            return (
                "MISMATCH",
                f"{len(note_families)} authors: " + "; ".join(note_families),
                f"{len(cr_families)} authors: " + "; ".join(cr_families),
            )
        n_norm = [_norm_family_name(f) for f in note_families]
        c_norm = [_norm_family_name(f) for f in cr_families]
        if n_norm == c_norm:
            return "MATCH", "; ".join(note_families), "; ".join(cr_families)
        return "MISMATCH", "; ".join(note_families), "; ".join(cr_families)

    return "MISSING", "", ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--field",
        default="all",
        help="comma-separated fields to check; 'all' for everything. "
             f"Available: {','.join(ALL_FIELDS)}",
    )
    ap.add_argument("--tsv", action="store_true", help="machine-readable TSV output")
    ap.add_argument("--quiet", action="store_true", help="only show discrepancies")
    ap.add_argument("--paper-id", help="check a single paper instead of all notes")
    ap.add_argument("--no-cache", action="store_true", help="ignore cache, force fresh CrossRef fetches")
    args = ap.parse_args()

    if args.field == "all":
        fields = list(ALL_FIELDS)
    else:
        fields = [f.strip() for f in args.field.split(",") if f.strip()]
        bad = [f for f in fields if f not in ALL_FIELDS]
        if bad:
            print(f"Unknown field(s): {bad}. Available: {ALL_FIELDS}", file=sys.stderr)
            return 2

    if args.no_cache:
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()

    if args.paper_id:
        notes = [NOTES_DIR / f"{args.paper_id}.md"]
        if not notes[0].exists():
            print(f"No such note: {notes[0]}", file=sys.stderr)
            return 2
    else:
        notes = sorted(NOTES_DIR.glob("*.md"))

    # Each row is a 7-tuple: (paper_id, doi, field, status, note_val,
    # cr_val, rationale). `rationale` is empty for normal rows; populated
    # for KNOWN_FP rows with the dated explanation from the registry.
    rows = []
    parse_errors = 0
    no_doi = 0
    lookup_errors = 0
    for note_path in notes:
        try:
            fm = parse_note_frontmatter(note_path)
        except Exception as e:
            rows.append((note_path.stem, "", "frontmatter", "ERROR", "", str(e)[:80], ""))
            parse_errors += 1
            continue

        doi = fm.get("doi")
        if not doi:
            rows.append((fm["paper_id"], "", "doi", "SKIP", "", "no DOI in frontmatter", ""))
            no_doi += 1
            continue

        msg = fetch_crossref(doi)
        if msg is None:
            rows.append((fm["paper_id"], doi, "crossref", "ERROR", "", "CrossRef fetch failed", ""))
            lookup_errors += 1
            continue

        for field in fields:
            note_val = fm.get(field)
            status, n_repr, c_repr = compare_field(field, note_val, msg)
            rationale = ""
            # Suppress known CrossRef-side data errors: re-classify
            # MISMATCH as KNOWN_FP if the (paper_id, field) is in the
            # registry. This keeps the gate clean while leaving an
            # audit trail in the report (and the TSV's rationale column).
            if status == "MISMATCH":
                rationale = KNOWN_CROSSREF_DATA_ERRORS.get(
                    fm["paper_id"], {}
                ).get(field, "")
                if rationale:
                    status = "KNOWN_FP"
            rows.append((fm["paper_id"], doi, field, status, n_repr, c_repr, rationale))

    # ---------- TSV output ----------
    if args.tsv:
        # 7th column "rationale" is new in v0.11.3+. Empty for normal
        # rows, populated for KNOWN_FP rows with the dated explanation.
        # Existing scripts that consume the first 6 columns still work.
        print("paper_id\tdoi\tfield\tstatus\tnote\tcrossref\trationale")
        for r in rows:
            paper_id, doi, field, status, n_repr, c_repr, rationale = r
            # tab-safe
            n_repr = (n_repr or "").replace("\t", " ")
            c_repr = (c_repr or "").replace("\t", " ")
            rationale = (rationale or "").replace("\t", " ")
            print(f"{paper_id}\t{doi}\t{field}\t{status}\t{n_repr}\t{c_repr}\t{rationale}")
        any_mismatch = any(r[3] == "MISMATCH" for r in rows)
        return 1 if any_mismatch else 0

    # ---------- Human report ----------
    by_field = {
        f: {"MATCH": 0, "MISMATCH": 0, "MISSING": 0, "KNOWN_FP": 0}
        for f in fields
    }
    mismatches = []  # rows with status==MISMATCH (real failures)
    known_fps = []   # rows with status==KNOWN_FP (suppressed, audit-only)
    for r in rows:
        paper_id, doi, field, status, n_repr, c_repr, rationale = r
        if field in by_field and status in by_field[field]:
            by_field[field][status] += 1
        if status == "MISMATCH":
            mismatches.append(r)
        elif status == "KNOWN_FP":
            known_fps.append(r)

    notes_checked = len({r[0] for r in rows if r[3] != "ERROR" and r[2] != "doi"})
    print(f"Verified {notes_checked} notes against CrossRef.")
    print(f"  Fields checked: {', '.join(fields)}\n")
    print(
        f"  {'Field':<10}  {'MATCH':>6}  {'MISMATCH':>9}  "
        f"{'MISSING':>8}  {'KNOWN_FP':>9}"
    )
    print(f"  {'-'*10}  {'-'*6}  {'-'*9}  {'-'*8}  {'-'*9}")
    for f in fields:
        s = by_field[f]
        print(
            f"  {f:<10}  {s['MATCH']:>6}  {s['MISMATCH']:>9}  "
            f"{s['MISSING']:>8}  {s['KNOWN_FP']:>9}"
        )
    print()
    if no_doi:
        print(f"  Skipped:        {no_doi}  (no DOI in frontmatter — typically editorials)")
    if lookup_errors:
        print(f"  Lookup errors:  {lookup_errors}  (CrossRef fetch failed)")
    if parse_errors:
        print(f"  Parse errors:   {parse_errors}  (frontmatter unreadable)")
    print()

    if mismatches:
        print("=" * 78)
        print("  MISMATCHES — review and fix manifest")
        print("=" * 78)
        # Group by paper_id for readable output
        by_paper: dict[str, list[tuple]] = {}
        for r in mismatches:
            by_paper.setdefault(r[0], []).append(r)
        for paper_id in sorted(by_paper):
            rows_for_paper = by_paper[paper_id]
            print(f"\n  {paper_id}")
            print(f"    DOI: {rows_for_paper[0][1]}")
            for r in rows_for_paper:
                _, _, field, _, n_repr, c_repr, _ = r
                # Show titles in full so the diff is visible; truncate
                # very long fields (rare) at 200 chars.
                n_show = (n_repr or "")[:200]
                c_show = (c_repr or "")[:200]
                print(f"    {field:<10} note: {n_show}")
                print(f"    {' '*10} cref: {c_show}")

    if known_fps:
        print()
        print("=" * 78)
        print("  KNOWN FALSE POSITIVES — suppressed by registry (audit only)")
        print("=" * 78)
        # Group by paper_id for readable output
        kfp_by_paper: dict[str, list[tuple]] = {}
        for r in known_fps:
            kfp_by_paper.setdefault(r[0], []).append(r)
        for paper_id in sorted(kfp_by_paper):
            rows_for_paper = kfp_by_paper[paper_id]
            print(f"\n  {paper_id}")
            print(f"    DOI: {rows_for_paper[0][1]}")
            for r in rows_for_paper:
                _, _, field, _, _, _, rationale = r
                print(f"    {field:<10} suppressed: {rationale}")
        print()
        print(
            "  These do NOT count as mismatches and do NOT fail the "
            "pipeline gate.\n  To audit, see KNOWN_CROSSREF_DATA_ERRORS "
            "in tools/verify_metadata.py."
        )

    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
