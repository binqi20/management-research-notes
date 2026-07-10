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
import urllib.error
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

# Known CrossRef-side data errors live in tools/known_crossref_issues.json — a
# data file, not code, so the per-issue false-positive additions this registry
# accumulates are data edits rather than source edits (the inline dict was
# migrated out at 22 entries, v0.31.0). Mismatches matching a (paper_id, field)
# entry are reported as KNOWN_FP rather than MISMATCH, so the gate stays clean.
# Add entries only after manually confirming that the CrossRef record itself is
# wrong (not the note), with a dated rationale ("... Suppressed YYYY-MM-DD.").
KNOWN_CROSSREF_ISSUES_PATH = Path(__file__).resolve().parent / "known_crossref_issues.json"

_REGISTRY_CACHE: dict[str, dict] = {}


def _reject_duplicate_keys(pairs: list) -> dict:
    """object_pairs_hook that rejects duplicate keys instead of silently
    keeping the last one — the likeliest hand-edit accident in an append-heavy
    registry (copy an entry block, forget to change the key, silently clobber
    an existing suppression)."""
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key {key!r}")
        out[key] = value
    return out


def load_known_registry(
    path: Path, required_entry_keys: tuple[str, ...] | None = None
) -> dict:
    """Load and validate a {"_doc": [...], "entries": {...}} registry file.

    Fails LOUD with an actionable message on a missing file, malformed JSON,
    duplicate keys, wrong entry shapes, or undated rationales. These registries
    guard correctness — silent degradation to "no suppressions" is the one
    failure mode this loader exists to prevent. Memoized per path; call it at
    the top of main() so a broken file surfaces before any network work.
    """
    cache_key = str(path)
    if cache_key in _REGISTRY_CACHE:
        return _REGISTRY_CACHE[cache_key]
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(
            f"ERROR: registry file missing: {path}\n"
            f"  Restore it with: git checkout -- {path}"
        )
    try:
        data = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as e:
        raise SystemExit(
            f"ERROR: malformed JSON in {path}:{e.lineno}:{e.colno}: {e.msg}"
        )
    except ValueError as e:
        raise SystemExit(f"ERROR: {path}: {e}")
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, dict):
        raise SystemExit(f"ERROR: {path} must contain a top-level 'entries' object")
    date_re = re.compile(r"20\d\d-\d\d-\d\d")
    for key, entry in entries.items():
        if not isinstance(entry, dict) or not entry:
            raise SystemExit(f"ERROR: {path}: entry {key!r} must be a non-empty object")
        if required_entry_keys:
            missing = sorted(set(required_entry_keys) - set(entry))
            if missing:
                raise SystemExit(
                    f"ERROR: {path}: entry {key!r} missing required keys: "
                    f"{', '.join(missing)}"
                )
            checks = [("rationale", entry.get("rationale"))]
        else:
            checks = list(entry.items())
        for label, rationale in checks:
            if not isinstance(rationale, str) or not date_re.search(rationale):
                raise SystemExit(
                    f"ERROR: {path}: entry {key!r} ({label}) needs a dated rationale "
                    f"(e.g. 'Suppressed 2026-07-10.')"
                )
    _REGISTRY_CACHE[cache_key] = entries
    return entries


def known_crossref_errors() -> dict[str, dict[str, str]]:
    """The CrossRef false-positive registry (memoized)."""
    return load_known_registry(KNOWN_CROSSREF_ISSUES_PATH)


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

# CrossRef resilience (added v0.30.0). Every gate (populate_manifest,
# lint_manifests, verify_metadata) imports fetch_crossref, so retrying transient
# failures here hardens the whole pipeline: a single HTTPS stall no longer aborts
# a full-library sweep (cf. the v0.25.0 sweep that a handshake stall interrupted).
CROSSREF_MAX_ATTEMPTS = 3
CROSSREF_BACKOFF_BASE_SECONDS = 2.0
CROSSREF_RETRYABLE_STATUS = {429, 500, 502, 503, 504}
_NOT_FOUND_SENTINEL = {"__crossref_not_found__": True}


def fetch_crossref(doi: str) -> dict | None:
    """Query CrossRef for a DOI. Returns the `message` object, or None on miss.

    Transient failures (network errors, timeouts, HTTP 5xx, 429 rate-limits) are
    retried up to CROSSREF_MAX_ATTEMPTS with linear backoff. A genuine 404 (DOI
    not registered) is permanent and is cached as a negative result so it is not
    re-fetched on every run; `--no-cache` clears both positive and negative cache
    entries.
    """
    cache_key = urllib.parse.quote(doi, safe="")
    cache_path = CACHE_DIR / f"{cache_key}.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text())
        return None if cached == _NOT_FOUND_SENTINEL else cached

    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_err: Exception | None = None
    for attempt in range(1, CROSSREF_MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
                payload = json.loads(resp.read())
            msg = payload.get("message", {})
            cache_path.write_text(json.dumps(msg))
            time.sleep(RATE_LIMIT_SLEEP_SECONDS)
            return msg
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Permanent: DOI not in CrossRef. Cache the negative result.
                cache_path.write_text(json.dumps(_NOT_FOUND_SENTINEL))
                print(f"  WARN: CrossRef has no record for {doi} (404)", file=sys.stderr)
                return None
            if e.code not in CROSSREF_RETRYABLE_STATUS:
                print(f"  WARN: CrossRef fetch failed for {doi}: {e}", file=sys.stderr)
                return None
            last_err = e
        except Exception as e:  # URLError, socket timeout, JSON decode — transient
            last_err = e
        if attempt < CROSSREF_MAX_ATTEMPTS:
            time.sleep(CROSSREF_BACKOFF_BASE_SECONDS * attempt)

    print(
        f"  WARN: CrossRef fetch failed for {doi} after "
        f"{CROSSREF_MAX_ATTEMPTS} attempts: {last_err}",
        file=sys.stderr,
    )
    return None


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
    # Fail-early: a broken registry file must surface before the CrossRef
    # network loop, not midway through a 1,000-note sweep.
    known_crossref_errors()

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
                rationale = known_crossref_errors().get(
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
            "pipeline gate.\n  To audit, see tools/known_crossref_issues.json."
        )

    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
