"""Reproduce local, hash-bound PDF evidence for an optional abstract check.

No supplied transcript or command is executed. Recipes select one of two fixed
extractors. Boundary-review assertions record human/parent judgments; reproducing
the text cannot establish that a region contains the whole abstract.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path


class EvidenceError(ValueError):
    """Abstract evidence cannot be reproduced or is stale."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def typography(text: str) -> str:
    """Only explicit line-end soft hyphens and Latin presentation ligatures.

    Run before the existing whitespace normalization. Removing U+00AD first
    would leave a space inside a word when its following newline is collapsed.
    Do not apply this helper to claims quotations or evidence anchors.
    """
    text = re.sub("\u00ad[ \t]*\r?\n[ \t]*", "", text)
    return text.translate(str.maketrans({
        "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
        "ﬅ": "st", "ﬆ": "st",
    }))


def extract(pdf: Path, recipe: dict) -> tuple[str, str]:
    """Return deterministic text and actual extractor version; never write PDF."""
    require(isinstance(recipe, dict), "extractor must be an object")
    name = recipe.get("name")
    if name == "pdftotext-reading-order":
        require(set(recipe) <= {"name", "version", "first_page", "last_page"},
                "unknown reading-order recipe option")
        first, last = recipe.get("first_page"), recipe.get("last_page")
        require(type(first) is int and type(last) is int and 1 <= first <= last,
                "invalid one-based page range")
        version_result = subprocess.run(["pdftotext", "-v"], capture_output=True,
                                        check=True, timeout=60)
        version = (version_result.stderr or version_result.stdout).decode("utf-8").splitlines()[0]
        result = subprocess.run(
            ["pdftotext", "-f", str(first), "-l", str(last), str(pdf.resolve()), "-"],
            capture_output=True, check=True, timeout=60,
        )
        return result.stdout.decode("utf-8"), version
    require(name == "pymupdf-regions", "unknown abstract extractor")
    require(set(recipe) <= {"name", "version", "regions"}, "unknown region recipe option")
    import fitz  # Optional dependency: only needed for explicit region recipes.

    regions = recipe.get("regions")
    require(isinstance(regions, list) and bool(regions), "regions must be nonempty")
    chunks, previous, seen = [], None, []
    with fitz.open(pdf) as document:
        for region in regions:
            require(isinstance(region, dict) and set(region) == {"page", "rect"},
                    "region needs page and rect")
            page, rect = region["page"], region["rect"]
            require(type(page) is int and 1 <= page <= len(document), "invalid region page")
            require(isinstance(rect, list) and len(rect) == 4
                    and all(type(v) in (int, float) and math.isfinite(v) for v in rect),
                    "invalid region coordinates")
            box = fitz.Rect(*rect)
            require(box.is_valid and not box.is_empty and document[page - 1].rect.contains(box),
                    "region lies outside page or has no area")
            order = (page, rect[1], rect[0])
            require(previous is None or order > previous, "regions must be in reading order")
            require(not any(p == page and box.intersects(b) for p, b in seen),
                    "abstract regions overlap")
            seen.append((page, box))
            previous = order
            chunks.append(document[page - 1].get_text(clip=box))
    return "\n".join(chunks), fitz.VersionBind


def verify(record: dict, root: Path, fm: dict, abstract: str, normalize) -> None:
    """Fail closed on supplied evidence, even if the original text would pass."""
    require(isinstance(record, dict), "abstract evidence must be an object")
    require(record.get("schema_version") == "pdf-abstract-evidence-v1", "invalid evidence schema")
    require(record.get("paper_id") == fm.get("id") and isinstance(fm.get("id"), str),
            "abstract evidence paper identity mismatch")
    require(bool(abstract) and abstract != "Not reported in paper", "evidence needs an actual abstract")
    for key in ("pdf_path", "text_path"):
        require(isinstance(fm.get(key), str) and bool(fm[key]), f"missing {key}")
        require(record.get(key) == fm[key], f"abstract evidence {key} mismatch")
        hash_key = "pdf_sha256" if key == "pdf_path" else "text_sha256"
        require(digest((root / fm[key]).read_bytes()) == record.get(hash_key), f"stale {hash_key}")
    require(record.get("abstract_sha256") == digest(abstract.encode("utf-8")),
            "abstract changed since boundary review")
    review = record.get("boundary_review")
    require(isinstance(review, dict) and review.get("complete") is True
            and all(isinstance(review.get(k), str) and review[k].strip()
                    for k in ("reviewer", "source_location", "rationale")),
            "complete PDF boundary review required")
    text, version = extract(root / fm["pdf_path"], record.get("extractor"))
    require(record["extractor"].get("version") == version, "extractor version mismatch")
    require(record.get("derived_text_sha256") == digest(text.encode("utf-8")),
            "derived extraction hash mismatch")
    # Tolerate word-internal hyphens only; do not erase negative signs or
    # numeric-range separators as the legacy hyphen-agnostic fallback does.
    def comparison(value: str) -> str:
        # Keep the separator when rejoining a wrapped token: normalize_ws
        # otherwise deletes it for both letters and digits (10-\n20 -> 1020).
        value = re.sub(r"-\s+(?=\w)", "-", typography(value))
        return re.sub(r"(?<=[^\W\d_])-(?=[^\W\d_])", "", normalize(value))

    require(comparison(abstract) in comparison(text),
            "abstract is not an exact match in reproduced PDF evidence")


def main() -> int:
    from validate_note import SYNAPSE_ROOT, split_frontmatter, parse_body_sections, normalize_ws

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path)
    parser.add_argument("--recipe-json", required=True, type=Path)
    parser.add_argument("--review-json", required=True, type=Path,
                        help="completed PDF boundary review; never generated by this tool")
    parser.add_argument("--output", required=True, type=Path,
                        help="new local evidence JSON; existing files are never overwritten")
    args = parser.parse_args()
    try:
        fm, body = split_frontmatter(args.note.read_text(encoding="utf-8"))
        abstract = parse_body_sections(body).get("Abstract", "")
        recipe = json.loads(args.recipe_json.read_text(encoding="utf-8"))
        review = json.loads(args.review_json.read_text(encoding="utf-8"))
        text, version = extract(SYNAPSE_ROOT / fm["pdf_path"], recipe)
        if "version" in recipe:
            require(recipe["version"] == version, "extractor version mismatch")
        record = {
            "schema_version": "pdf-abstract-evidence-v1", "paper_id": fm["id"],
            "pdf_path": fm["pdf_path"], "text_path": fm["text_path"],
            "pdf_sha256": digest((SYNAPSE_ROOT / fm["pdf_path"]).read_bytes()),
            "text_sha256": digest((SYNAPSE_ROOT / fm["text_path"]).read_bytes()),
            "abstract_sha256": digest(abstract.encode("utf-8")),
            "extractor": {**recipe, "version": version},
            "derived_text_sha256": digest(text.encode("utf-8")), "boundary_review": review,
        }
        verify(record, SYNAPSE_ROOT, fm, abstract, normalize_ws)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    except (ValueError, OSError, ImportError, subprocess.SubprocessError, RuntimeError,
            KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"Created {args.output}; boundary judgments still require independent review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
