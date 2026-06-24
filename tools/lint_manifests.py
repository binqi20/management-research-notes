#!/usr/bin/env python3
"""
lint_manifests.py — periodic structural audit of every library/*/*/manifest.tsv.

Why this exists
---------------
verify_metadata.py (post-extraction, Step 4.5) audits each NOTE against CrossRef.
populate_manifest.py (pre-extraction, Step 0) populates the manifest from CrossRef.
Both work great when the manifest's INPUT fields are well-formed. But neither
catches the class of bug where the manifest *itself* has a structural anomaly
that propagates cleanly through every downstream step.

The v0.13.1 D'Amico case was the motivating example: the manifest's
`first_author_last` column held "Stefania D'Amico" (a full given+family name)
instead of "D'Amico" (just the family name). Every step of the pipeline saw
the bad value and processed it cleanly, because no step was asking "is this
field structurally well-formed?" The bug only surfaced when we audited the
RESULTING paper_ids during the v0.13.1 cleanup.

This tool fills that gap: a per-row structural audit of every manifest, with
optional CrossRef cross-checks to catch full-name-instead-of-surname patterns.

Two tiers of check
------------------
Heuristic (fast, no network):
  - `first_author_last`:
      * non-empty, length 1-50
      * not purely numeric
      * no commas (which would suggest "Last, First" combined fields)
      * regex-validated against Latin letters + diacritics + apostrophes +
        whitespace
  - `year`: 4-digit integer in [1900, current_year+1]
  - `doi`: matches the CrossRef DOI pattern (10.NNNN/anything)
  - `saved_filename`: must exist as an actual file in the sibling `pdfs/`
    directory (when status='downloaded')

Authoritative (CrossRef cross-check, per-DOI, cached):
  - First-author family name from CrossRef (after accent-fold) must match
    manifest's `first_author_last` (after accent-fold). Mismatch = likely
    manifest-population error. Caught the D'Amico class.

Usage
-----
    python3 tools/lint_manifests.py                     # all manifests, heuristic + CrossRef
    python3 tools/lint_manifests.py --no-crossref       # heuristic only (fast, offline)
    python3 tools/lint_manifests.py --manifest PATH     # single manifest
    python3 tools/lint_manifests.py --quiet             # only show anomalies

Exit codes
----------
0: no anomalies
1: at least one row flagged
2: invocation error
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# Reuse verify_metadata's CrossRef client + normalization. Single source of
# truth for cache, SSL, User-Agent, accent-folding. Bug fixes propagate.
THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
sys.path.insert(0, str(THIS_FILE.parent))
from verify_metadata import fetch_crossref, _norm_family_name  # noqa: E402

LIBRARY = SYNAPSE_ROOT / "library"


# Known compound-surname false positives in the CrossRef cross-check.
# Some publishers store the formal compound family name in CrossRef (e.g.,
# "von Krogh", "Ter Wal", "van den Oever") while the corresponding manifest
# row uses the citation-convention short form ("Krogh", "Wal", "Oever").
# Both are defensible; neither is a bug. Suppress these via DOI-keyed
# entries so the linter doesn't flag them on every run.
#
# Same pattern as KNOWN_CROSSREF_DATA_ERRORS in verify_metadata.py. Add
# entries only after manually confirming the case is a legitimate compound-
# surname citation-convention difference (not a manifest bug). Each entry
# requires a dated rationale.
#
# TODO: migrate to a JSON file (e.g. tools/known_compound_surnames.json)
# if this list grows past ~10 entries.
KNOWN_COMPOUND_SURNAMES: dict[str, dict[str, str]] = {
    "10.5465/amj.2023.4002": {
        "manifest_surname": "Krogh",
        "crossref_family": "von Krogh",
        "rationale": (
            "Georg von Krogh (ETH Zürich) — Dutch/Swiss compound surname. "
            "CrossRef stores the formal 'von Krogh'; manifest uses the "
            "citation-convention short form 'Krogh'. Suppressed 2026-05-12."
        ),
    },
    "10.5465/amj.2018.1258": {
        "manifest_surname": "Cunningham",
        "crossref_family": "Lee Cunningham",
        "rationale": (
            "Tony Lee Cunningham — compound family name. CrossRef stores "
            "'Lee Cunningham'; manifest uses the citation-convention short "
            "form 'Cunningham'. Suppressed 2026-05-12."
        ),
    },
    "10.5465/amj.2020.1231": {
        "manifest_surname": "Wal",
        "crossref_family": "Ter Wal",
        "rationale": (
            "Anne L. J. Ter Wal — Dutch 'Ter Wal' compound prefix. CrossRef "
            "stores 'Ter Wal'; manifest uses citation-convention short form "
            "'Wal'. Suppressed 2026-05-12."
        ),
    },
    "10.5465/amj.2020.1623": {
        "manifest_surname": "Leon",
        "crossref_family": "de Leon",
        "rationale": (
            "Rebecca Ponce de Leon — Spanish compound surname 'Ponce de "
            "Leon' (the article cites it 17x). CrossRef splits it as "
            "given='Rebecca Ponce', family='de Leon'; manifest uses the "
            "citation-convention short form 'Leon'. Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2020.1740": {
        "manifest_surname": "Gomez",
        "crossref_family": "Munguia Gomez",
        "rationale": (
            "David M. Munguia Gomez — compound family name. CrossRef stores "
            "'Munguia Gomez'; manifest uses the citation-convention short "
            "form 'Gomez'. Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2020.1492": {
        "manifest_surname": "Rond",
        "crossref_family": "de Rond",
        "rationale": (
            "Mark de Rond (Cambridge) — 'de Rond' compound prefix. CrossRef "
            "stores 'de Rond'; manifest uses the citation-convention short "
            "form 'Rond'. Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2020.1516": {
        "manifest_surname": "Tang",
        "crossref_family": "Man Tang",
        "rationale": (
            "Pok Man Tang — Cantonese romanization; CrossRef parses "
            "family='Man Tang'. The journal running header and the existing "
            "liao-2024 note use 'Tang'; manifest matches that convention. "
            "Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2019.1402": {
        "manifest_surname": "Eleazar",
        "crossref_family": "Welbourne Eleazar",
        "rationale": (
            "Miranda J. Welbourne Eleazar — compound family name 'Welbourne "
            "Eleazar' (cited 12x). CrossRef stores 'Welbourne Eleazar'; "
            "manifest uses the citation-convention short form 'Eleazar'. "
            "Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2019.0616": {
        "manifest_surname": "Pamphile",
        "crossref_family": "Deeds Pamphile",
        "rationale": (
            "Vontrese Deeds Pamphile — compound family name. CrossRef stores "
            "'Deeds Pamphile'; manifest and the article's running text use the "
            "citation-convention short form 'Pamphile'. Suppressed 2026-06-23."
        ),
    },
    "10.5465/amj.2022.1075": {
        "manifest_surname": "Oever",
        "crossref_family": "van den Oever",
        "rationale": (
            "Koen van den Oever — Dutch 'van den Oever' compound prefix. "
            "CrossRef stores 'van den Oever'; manifest uses citation-"
            "convention short form 'Oever'. Suppressed 2026-05-12."
        ),
    },
    "10.1177/01708406251362935": {
        "manifest_surname": "Shantz",
        "crossref_family": "Slade Shantz",
        "rationale": (
            "Angelique Slade Shantz — compound family name. CrossRef stores "
            "'Slade Shantz'; manifest (filename-derived) uses the citation "
            "short form 'Shantz'. NBS 2026-01; DOI verified (title "
            "gate-matches CrossRef). Suppressed 2026-06-06."
        ),
    },
    "10.1016/j.respol.2025.105408": {
        "manifest_surname": "Silva",
        "crossref_family": "De Silva",
        "rationale": (
            "Muthu De Silva — 'De Silva' compound surname. CrossRef stores "
            "'De Silva'; manifest (filename-derived) uses the citation short "
            "form 'Silva'. NBS 2026-01; DOI verified (title gate-matches "
            "CrossRef). Suppressed 2026-06-06."
        ),
    },
    "10.25300/misq/2025/17970": {
        "manifest_surname": "Vaujany",
        "crossref_family": "de Vaujany",
        "rationale": (
            "François-Xavier de Vaujany — French 'de Vaujany' nobiliary "
            "particle. CrossRef stores 'de Vaujany'; manifest (filename-"
            "derived) uses the citation short form 'Vaujany'. NBS 2026-01; "
            "DOI verified (title gate-matches CrossRef). Suppressed 2026-06-06."
        ),
    },
}

# ---------------------------------------------------------------------------
# Heuristic validators
# ---------------------------------------------------------------------------

# Latin letters (A-Za-z) + diacritics across Latin-1 Supplement, Latin
# Extended-A/B, and Latin Extended Additional (U+1E00–U+1EFF, e.g. Vietnamese
# "Thảo") + apostrophes (straight/curly) + hyphens + whitespace. Allows
# compound surnames like "van der Berg", "De La Cruz", "O'Brien", "Tröster",
# "Peñaloza-Pacheco", "Strøm-Andersen", but still flags numerics, commas,
# over-long full-name captures, and non-Latin scripts (Cyrillic/CJK/etc.).
_FIRST_AUTHOR_LAST_RE = re.compile(
    r"^[A-Za-zÀ-ſƀ-ɏḀ-ỿ'’\-\s]+$"
)

_DOI_RE = re.compile(r"^10\.\d{3,}/\S+$")


def check_first_author_last(value: str) -> str | None:
    """Heuristic check on first_author_last. Returns error string or None."""
    if not value or not value.strip():
        return "empty value"
    if len(value) > 50:
        return f"unusually long ({len(value)} chars) — possible full-name capture"
    if value.strip().isdigit():
        return f"purely numeric ({value!r})"
    if "," in value:
        return f"contains comma — likely 'Last, First' instead of just family name"
    if not _FIRST_AUTHOR_LAST_RE.match(value):
        # Surface the offending characters for debugging
        bad = sorted({c for c in value if not _FIRST_AUTHOR_LAST_RE.match(c)})
        return f"contains non-Latin-alphabetic characters: {bad!r}"
    return None


def check_year(value: str) -> str | None:
    """Heuristic check on year. Returns error string or None."""
    if not value or not value.strip():
        return "empty value"
    try:
        y = int(value.strip())
    except ValueError:
        return f"not an integer ({value!r})"
    current_year = datetime.now().year
    if y < 1900 or y > current_year + 2:
        return f"out of range ({y}); expected 1900..{current_year + 2}"
    return None


def check_doi(value: str) -> str | None:
    """Heuristic check on DOI. Returns error string or None."""
    if not value or not value.strip():
        # Empty DOI is acceptable for editorials / book reviews lacking DOIs.
        # Caller can decide whether to flag based on row context.
        return None
    if not _DOI_RE.match(value.strip()):
        return f"does not match CrossRef DOI pattern ({value!r})"
    return None


def check_saved_filename(manifest_dir: Path, value: str, status: str) -> str | None:
    """Check that saved_filename exists in sibling pdfs/ dir when status=downloaded."""
    if status.strip().lower() != "downloaded":
        return None  # Files only required for downloaded rows
    if not value or not value.strip():
        return "empty filename (status=downloaded)"
    pdfs_dir = manifest_dir / "pdfs"
    pdf_path = pdfs_dir / value.strip()
    if not pdf_path.exists():
        return f"file not found: {pdf_path.relative_to(SYNAPSE_ROOT)}"
    return None


# ---------------------------------------------------------------------------
# CrossRef cross-check
# ---------------------------------------------------------------------------


def crossref_first_author_family(doi: str) -> str | None:
    """Return the family name of the first author from CrossRef, or None."""
    msg = fetch_crossref(doi)
    if msg is None:
        return None
    authors = msg.get("author") or []
    if not authors:
        return None
    # Prefer the entry marked sequence="first"; otherwise take index 0.
    first = next((a for a in authors if a.get("sequence") == "first"), authors[0])
    return first.get("family") or None


def check_first_author_vs_crossref(doi: str, manifest_value: str) -> str | None:
    """Compare manifest first_author_last with CrossRef's first-author family.

    Returns None if they match (after accent-fold), if CrossRef can't be
    queried, or if the (doi, manifest_value) pair is in the
    KNOWN_COMPOUND_SURNAMES allowlist. Returns an error string on
    real mismatch.
    """
    if not doi or not manifest_value:
        return None
    # Strip leading https://doi.org/ if present
    doi_clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip())
    cr_family = crossref_first_author_family(doi_clean)
    if cr_family is None:
        return None  # No CrossRef data; can't compare. Heuristic check handles empty.
    if _norm_family_name(manifest_value) == _norm_family_name(cr_family):
        return None
    # Check allowlist for known compound-surname false positives
    suppress = KNOWN_COMPOUND_SURNAMES.get(doi_clean)
    if suppress and suppress.get("manifest_surname") == manifest_value.strip():
        # Caller can decide whether to surface this; we return None so the
        # row is not flagged. The allowlist itself serves as the audit trail.
        return None
    return (
        f"manifest first_author_last={manifest_value!r} "
        f"≠ CrossRef first-author family={cr_family!r} "
        f"(after accent-fold). Possible full-name capture or wrong row."
    )


# ---------------------------------------------------------------------------
# Per-manifest audit
# ---------------------------------------------------------------------------


def audit_manifest(
    manifest_path: Path,
    check_crossref: bool,
    quiet: bool,
) -> tuple[int, int, list[str]]:
    """Audit one manifest. Returns (rows_checked, rows_flagged, lines_to_print)."""
    lines: list[str] = []
    rows_checked = 0
    rows_flagged = 0

    manifest_dir = manifest_path.parent
    with manifest_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    rel = manifest_path.relative_to(SYNAPSE_ROOT)

    for i, row in enumerate(rows, start=2):  # start=2 because line 1 is header
        rows_checked += 1
        anomalies: list[str] = []

        # Heuristic checks
        for col, checker in (
            ("first_author_last", check_first_author_last),
            ("year", check_year),
            ("doi", check_doi),
        ):
            value = row.get(col, "") or ""
            err = checker(value)
            if err:
                anomalies.append(f"{col}: {err}")

        # Saved-filename check requires status context
        if "saved_filename" in row and "status" in row:
            err = check_saved_filename(manifest_dir, row.get("saved_filename") or "",
                                        row.get("status") or "")
            if err:
                anomalies.append(f"saved_filename: {err}")

        # CrossRef cross-check (only when no heuristic complaint about
        # first_author_last or doi — otherwise the CrossRef result is
        # unreliable anyway)
        if check_crossref and not any(a.startswith(("first_author_last:", "doi:")) for a in anomalies):
            doi_val = (row.get("doi") or "").strip()
            fa_val = (row.get("first_author_last") or "").strip()
            if doi_val and fa_val:
                err = check_first_author_vs_crossref(doi_val, fa_val)
                if err:
                    anomalies.append(f"crossref: {err}")

        if anomalies:
            rows_flagged += 1
            label = f"{row.get('first_author_last', '?')} {row.get('year', '?')}"
            doi = (row.get("doi") or "").strip()
            lines.append(f"  ✗ Row {i}: {label}  (DOI: {doi or 'none'})")
            for a in anomalies:
                lines.append(f"      {a}")

    if rows_flagged == 0:
        if not quiet:
            lines.insert(0, f"\n{rel} ({rows_checked} rows)")
            lines.append("  ✓ All checks passed")
    else:
        lines.insert(0, f"\n{rel} ({rows_checked} rows, {rows_flagged} flagged)")

    return rows_checked, rows_flagged, lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--manifest", help="lint a single manifest instead of all")
    ap.add_argument(
        "--no-crossref",
        action="store_true",
        help="skip CrossRef cross-checks (heuristic only, fast, offline)",
    )
    ap.add_argument("--quiet", action="store_true",
                    help="suppress per-manifest 'all checks passed' lines")
    args = ap.parse_args()

    if args.manifest:
        manifests = [Path(args.manifest).resolve()]
        if not manifests[0].exists():
            print(f"manifest not found: {manifests[0]}", file=sys.stderr)
            return 2
    else:
        manifests = sorted(LIBRARY.glob("*/*/manifest.tsv"))

    if not manifests:
        print("No manifests found.", file=sys.stderr)
        return 2

    check_crossref = not args.no_crossref
    print(f"Linting {len(manifests)} manifest(s) under {LIBRARY.relative_to(SYNAPSE_ROOT)}/")
    if not check_crossref:
        print("  (CrossRef cross-check disabled — heuristic only)")
    print()

    total_rows = 0
    total_flagged = 0
    manifests_with_flags = 0

    for manifest in manifests:
        rows_checked, rows_flagged, lines = audit_manifest(
            manifest, check_crossref=check_crossref, quiet=args.quiet
        )
        total_rows += rows_checked
        total_flagged += rows_flagged
        if rows_flagged > 0:
            manifests_with_flags += 1
        for line in lines:
            print(line)

    print()
    print("=" * 70)
    print(f"  {len(manifests)} manifest(s) checked")
    print(f"  {total_rows} row(s) audited")
    if total_flagged == 0:
        print(f"  ✓ All clean")
    else:
        print(f"  ✗ {total_flagged} row(s) flagged across {manifests_with_flags} manifest(s)")
    print("=" * 70)

    return 1 if total_flagged > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
