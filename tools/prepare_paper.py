#!/usr/bin/env python3
"""
prepare_paper.py — given a PDF inside the canonical library/ layout, look up the
trusted bibliographic metadata from the source's manifest.tsv and emit an extraction
bundle that the LLM (Claude inside Claude Code) will read to produce the note.

The bundle is a single text file in incoming/_bundles/<paper_id>.bundle.txt and
contains:
  - The trusted bibliographic block (authoritative, not to be changed by the LLM)
  - The full extracted text of the paper
  - A pointer to the canonical extraction prompt at docs/extraction-prompt.md

Usage:
  python tools/prepare_paper.py <pdf-path>

After running, the LLM (Claude Code session) is responsible for:
  - Reading docs/extraction-prompt.md
  - Reading the bundle
  - Writing notes/<paper_id>.md via the Write tool
  - Running validate_note.py on the result
"""

from __future__ import annotations

import csv
import datetime as dt
import re
import sys
from pathlib import Path

# --- locate the Synapse root ------------------------------------------------------

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent

LIBRARY = SYNAPSE_ROOT / "library"
BUNDLES_DIR = SYNAPSE_ROOT / "incoming" / "_bundles"
NOTES_DIR = SYNAPSE_ROOT / "notes"
PROMPT_PATH = SYNAPSE_ROOT / "docs" / "extraction-prompt.md"

EXTRACTION_MODEL = "claude-opus-4-6"
EXTRACTION_VERSION = "v1"


# --- helpers ----------------------------------------------------------------------


def slugify(value: str, max_length: int = 40) -> str:
    """Lowercase, ASCII-ish, hyphen-separated. Used for paper IDs."""
    value = value.lower()
    # Replace common diacritics minimally
    replacements = {"’": "'", "–": "-", "—": "-", "“": '"', "”": '"'}
    for k, v in replacements.items():
        value = value.replace(k, v)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:max_length]


def parse_library_path(pdf: Path) -> tuple[str, str]:
    """
    Given .../library/<source>/<year-month>/pdfs/foo.pdf return ('source', 'year-month').
    Raises if the PDF is not inside the canonical layout.
    """
    try:
        rel = pdf.resolve().relative_to(LIBRARY.resolve())
    except ValueError:
        raise SystemExit(f"PDF is not under {LIBRARY}: {pdf}")
    parts = rel.parts
    if len(parts) < 4 or parts[2] != "pdfs":
        raise SystemExit(
            f"Expected layout library/<source>/<year-month>/pdfs/<file>.pdf, got {rel}"
        )
    return parts[0], parts[1]


def load_manifest(source: str, issue: str) -> list[dict]:
    manifest = LIBRARY / source / issue / "manifest.tsv"
    if not manifest.exists():
        raise SystemExit(f"manifest not found: {manifest}")
    with manifest.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "to", "for", "from", "with",
    "is", "are", "as", "at", "by", "be", "its", "this", "that", "into", "over",
    "under", "how", "why", "what", "when", "does", "do", "can", "not", "no",
    "evidence", "case", "study", "an",
}


def _title_tokens(text: str) -> set[str]:
    """Return the informative lowercase tokens of a title/filename, minus stopwords."""
    norm = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return {t for t in norm.split() if len(t) > 3 and t not in STOPWORDS}


def find_manifest_row(rows: list[dict], pdf_name: str) -> dict:
    """Match by saved_filename; fall back to title-word overlap.

    Real-world batches often contain PDFs that were renamed after download (e.g.,
    "Anjier Chen 2026 Sharing is..." → "Chen 2026 Examining the Impact..."). When
    the exact filename match fails, we compute Jaccard overlap between the PDF
    stem's informative tokens and each manifest row's title tokens and take the
    best match if it clears a threshold.
    """
    # Fast path: exact filename match.
    for row in rows:
        if row.get("saved_filename") == pdf_name:
            return row

    # Fallback: title-word overlap.
    pdf_tokens = _title_tokens(Path(pdf_name).stem)
    if not pdf_tokens:
        raise SystemExit(f"no manifest row matched filename {pdf_name!r}")

    scored: list[tuple[float, int, dict]] = []
    for row in rows:
        title = row.get("title", "") or ""
        title_tokens = _title_tokens(title)
        if not title_tokens:
            continue
        overlap = pdf_tokens & title_tokens
        if not overlap:
            continue
        jaccard = len(overlap) / len(pdf_tokens | title_tokens)
        scored.append((jaccard, len(overlap), row))

    if not scored:
        raise SystemExit(
            f"no manifest row matched filename {pdf_name!r} (checked {len(rows)} rows)"
        )

    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    best_jaccard, best_overlap, best_row = scored[0]
    if best_jaccard < 0.2 or best_overlap < 3:
        raise SystemExit(
            f"no confident manifest match for {pdf_name!r}; "
            f"best candidate was {best_row.get('title')!r} "
            f"(jaccard={best_jaccard:.2f}, overlap={best_overlap})"
        )
    print(
        f"[fallback] matched {pdf_name!r} -> {best_row.get('title')!r} "
        f"by title overlap (jaccard={best_jaccard:.2f})",
        file=sys.stderr,
    )
    return best_row


def derive_text_path(pdf: Path) -> Path:
    return pdf.parent.parent / "text" / (pdf.stem + ".txt")


def derive_paper_id(
    source: str,
    issue: str,
    first_author_last: str,
    year: str,
    title: str,
    rows: list[dict],
) -> str:
    """Build a stable paper ID.

    Base form: {source-slug}-{issue}-{author-slug}-{year} (e.g., nbs-2026-02-spoor-2026).

    When the same (first_author_last, year) pair appears more than once in the
    manifest — e.g., four "Lee 2026" papers in one issue — we disambiguate by
    appending up to 3 informative title words. IDs remain stable across re-runs
    because they are derived deterministically from the manifest content.
    """
    author_slug = slugify(first_author_last)
    year_str = str(year).strip()
    base = "-".join([slugify(source), issue, author_slug, year_str])

    # Count how many manifest rows share this (author, year) pair.
    same_cohort = [
        r for r in rows
        if slugify(r.get("first_author_last", "")) == author_slug
        and str(r.get("year", "")).strip() == year_str
    ]
    if len(same_cohort) <= 1:
        return base

    # Collision — append a short title slug (first 3 informative words).
    tokens = [t for t in slugify(title, max_length=120).split("-") if len(t) > 3 and t not in STOPWORDS]
    suffix = "-".join(tokens[:3])
    if not suffix:
        # Fall back to a hash of the title to guarantee uniqueness.
        import hashlib
        suffix = hashlib.md5(title.encode("utf-8")).hexdigest()[:6]
    return f"{base}-{suffix}"


# --- main -------------------------------------------------------------------------


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: prepare_paper.py <pdf>", file=sys.stderr)
        return 2

    pdf = Path(sys.argv[1]).resolve()
    if not pdf.exists() or pdf.suffix.lower() != ".pdf":
        print(f"not a pdf: {pdf}", file=sys.stderr)
        return 2

    source, issue = parse_library_path(pdf)
    rows = load_manifest(source, issue)
    row = find_manifest_row(rows, pdf.name)

    paper_id = derive_paper_id(
        source=source,
        issue=issue,
        first_author_last=row["first_author_last"],
        year=row["year"],
        title=row.get("title", ""),
        rows=rows,
    )

    text_path = derive_text_path(pdf)
    if not text_path.exists():
        raise SystemExit(
            f"extracted text not found: {text_path}\n"
            f"run: python tools/pdf_to_text.py {pdf}"
        )

    pdf_text = text_path.read_text(encoding="utf-8", errors="replace")

    # Build the trusted bib block. DOI is normalized to https://doi.org/...
    doi_raw = (row.get("doi") or "").strip()
    if doi_raw and not doi_raw.startswith("http"):
        doi_full = f"https://doi.org/{doi_raw}"
    else:
        doi_full = doi_raw or ""

    rel_pdf = pdf.relative_to(SYNAPSE_ROOT)
    rel_text = text_path.relative_to(SYNAPSE_ROOT)
    today = dt.date.today().isoformat()

    bib_block = "\n".join(
        [
            "TRUSTED BIBLIOGRAPHIC METADATA (use verbatim, do not change):",
            f"id: {paper_id}",
            f"title: {row['title']}",
            f"first_author_last: {row['first_author_last']}",
            f"year: {row['year']}",
            f"doi: {doi_full}",
            f"source: {source}/{issue}",
            f"pdf_path: {rel_pdf}",
            f"text_path: {rel_text}",
            f"ingested_at: {today}",
            f"extraction_model: {EXTRACTION_MODEL}",
            f"extraction_version: {EXTRACTION_VERSION}",
        ]
    )

    bundle = "\n\n".join(
        [
            bib_block,
            "PAPER TEXT (extracted from PDF):",
            pdf_text,
            "Please produce the Synapse note now. Read the canonical extraction "
            f"prompt at {PROMPT_PATH.relative_to(SYNAPSE_ROOT)} and follow its "
            f"format exactly. Write the result to notes/{paper_id}.md.",
        ]
    )

    BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
    bundle_path = BUNDLES_DIR / f"{paper_id}.bundle.txt"
    bundle_path.write_text(bundle, encoding="utf-8")

    print(f"paper_id:    {paper_id}")
    print(f"note_target: notes/{paper_id}.md")
    print(f"bundle:      {bundle_path.relative_to(SYNAPSE_ROOT)}")
    print(f"text chars:  {len(pdf_text):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
