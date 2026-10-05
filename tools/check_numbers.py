#!/usr/bin/env python3
"""Advisory numeric-presence check against a note's complete raw text_path.

A hit is not evidence that the number has the correct referent, sign, study or
interpretation. No fitted audit input, anchors, or audit verdicts are consulted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from bisect import bisect_right
import json
from pathlib import Path
import re
import sys

import yaml

try:
    from .validate_note import SYNAPSE_ROOT, parse_body_sections, split_frontmatter
except ImportError:  # Direct script execution / tools on sys.path.
    from validate_note import SYNAPSE_ROOT, parse_body_sections, split_frontmatter

SECTIONS = ("Hypotheses / Propositions", "Data & Measures", "Key Findings")
ADVISORY = (
    "Counts indicate numeric presence only; they do not establish the correct "
    "referent, sign, study, threshold or interpretation. Glyph matches are heuristic. "
    "Candidates never contribute hits; zero-hit and glyph-only rows require raw "
    "sign, unit, study and referent verification."
)
# Decimal and thousands boundaries prevent 27 matching 127, .27 or 27.5.
NUMBER = re.compile(
    r"(?<![\w.])(?P<sign>[+\-−]?)(?P<number>"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)"
    r"(?P<exponent>[eE][+\-]?\d+)?"
    r"(?P<percent>\s*(?:%|percent\b))?(?![\w]|\.\d|,\d)"
)
DOI = re.compile(r"(?:https?://(?:dx\.)?doi\.org/)?10\.\d{4,9}/[^\s<>]+", re.I)
# Require citation punctuation; plain prose such as 'In 2010' remains empirical.
AUTHOR = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'\-]+"
AUTHORS = rf"{AUTHOR}(?:\s+(?:et\s+al\.|(?:and|&)\s+{AUTHOR}))?"
CITATION = re.compile(rf"\b{AUTHORS}\s*(?:\(\s*|,\s*)(?:18|19|20)\d{{2}}[a-z]?(?:\s*[,;]\s*(?:18|19|20)\d{{2}}[a-z]?)*")
YEAR = re.compile(r"\b(?:18|19|20)\d{2}[a-z]?\b")
YEAR_RANGE = re.compile(r"\b(?:18|19|20)\d{2}\s*[-−–—]\s*(?:18|19|20)\d{2}\b")
LIST_NUMBER = re.compile(r"(?m)^\s*(?:[-*+]\s+)?(?:\(?\d+\)|\d+\.(?!\d))\s+")
# Only recognized statistical labels followed by a corrupted operator qualify.
STAT = r"(?:b|β|beta|r|ρ|t|z|p|N|n|SE|SD|M|F|χ²|R²)"
GLYPH = re.compile(
    rf"(?<!\w)(?P<label>{STAT})\s*(?P<op>5\s+|,)\s*"
    r"(?P<value>[+−\-]?(?:\d+(?:\.\d+)?|\.\d+))"
    r"(?![\w]|\.\d|,\d)"
)
# These labels and locations only describe candidates, never establish support.
CANDIDATE_LABEL = re.compile(
    rf"(?<!\w)(?P<label>{STAT}|B|g|γ|gamma|estimate|effect)\s*(?:5|=|,)\s*$"
)
ALTERNATE_MINUS = "–—‐‑‒﹣－⫺"


def _masked(text: str, *, note: bool) -> str:
    chars = list(text)
    spans = [match.span() for match in DOI.finditer(text)]
    if note:
        spans.extend(match.span() for match in LIST_NUMBER.finditer(text))
        ranges = [match.span() for match in YEAR_RANGE.finditer(text)]
        for citation in CITATION.finditer(text):
            spans.extend((citation.start() + m.start(), citation.start() + m.end())
                         for m in YEAR.finditer(citation.group())
                         if not any(start <= citation.start() + m.start() < end
                                    for start, end in ranges))
    for start, end in spans:
        chars[start:end] = " " * (end - start)
    return "".join(chars)


def _canonical(match: re.Match, *, note: bool = False) -> str:
    value = match.group("number").replace(",", "")
    if value.startswith("."):
        value = "0" + value
    sign = match.group("sign").replace("−", "-")
    if sign == "+":
        sign = ""
    # A dash between digits denotes a range, not a negative endpoint.
    if sign == "-" and match.start() and match.string[match.start() - 1].isdigit():
        sign = ""
    # A spaced year-like pair can instead be a year and a signed table value.
    # Only note prose with an immediate time-range cue gets this interpretation;
    # raw source counts always preserve the explicit signed literal.
    if (note and sign == "-"
            and re.fullmatch(r"(?:18|19|20)\d{2}", match.group("number"))
            and not match.group("exponent") and not match.group("percent")
            and re.search(r"\b(?:years|period|survey|from)[ \t]*[:,(]?[ \t]*"
                          r"(?:18|19|20)\d{2}[ \t]+$",
                          match.string[:match.start()], re.I)):
        sign = ""
    return sign + value + (match.group("exponent") or "").lower() + ("%" if match.group("percent") else "")


def _source_counts(raw: str) -> tuple[Counter, Counter]:
    raw = _masked(raw, note=False)
    artifact_counts: Counter = Counter()
    ambiguous_literals: Counter = Counter()
    chars = list(raw)
    for match in GLYPH.finditer(raw):
        value = match.group("value")
        # '2.27' can encode '-.27', but can also be the literal +2.27.
        # Keep both interpretations; presence does not settle the ambiguity.
        if match.group("op").strip() == "5" and re.fullmatch(r"2\d*\.\d+", value):
            value = "-" + value[1:]
        parsed = NUMBER.fullmatch(value)
        if parsed is not None:
            artifact_token = _canonical(parsed)
            artifact_counts[artifact_token] += 1
            literal = NUMBER.fullmatch(match.group("value"))
            if literal is not None and _canonical(literal) != artifact_token:
                ambiguous_literals[_canonical(literal)] += 1
            # Mask this occurrence after recording distinct interpretations,
            # avoiding duplicate counts for an identical canonical token.
            chars[match.start():match.end()] = " " * (match.end() - match.start())
    literal_counts = Counter(_canonical(m) for m in NUMBER.finditer("".join(chars)))
    literal_counts.update(ambiguous_literals)
    return literal_counts, artifact_counts


def _source_candidates(raw: str, targets: set[str]) -> dict[str, list[dict]]:
    """Locate possible negatives without changing literal/legacy hit counts.

    Offsets are zero-based, end-exclusive Unicode character offsets in the raw
    text loaded by analyze_note; physical line/column numbers are one-based.
    Table/CI hints and leading-2 alternatives remain explicitly ambiguous.
    """
    found = {token: [] for token in targets}
    if not targets:
        return found
    line_starts = [0] + [m.end() for m in re.finditer(r"\n", raw)]
    masked = _masked(raw, note=False)
    for match in NUMBER.finditer(masked):
        if match.group("sign"):
            continue
        value = match.group("number")
        alternatives = []
        # Keep the literal +2-prefixed interpretation in _source_counts.
        if value.startswith("2") and len(value) > 1:
            parsed = NUMBER.fullmatch("-" + value[1:] + (match.group("exponent") or "")
                                      + (match.group("percent") or ""))
            if parsed:
                alternatives.append((_canonical(parsed), match.start(), "minus_as_2"))
        prefix = masked[:match.start()]
        dash = re.search(rf"[{ALTERNATE_MINUS}]\s*$", prefix)
        if dash and not re.search(r"\d\s*$", prefix[:dash.start()]):
            alternatives.append(("-" + _canonical(match), dash.start(), "alternate_minus"))
        for token, start, reason in alternatives:
            if token not in targets:
                continue
            line_index = bisect_right(line_starts, start) - 1
            line_start = line_starts[line_index]
            line_end = raw.find("\n", match.end())
            if line_end < 0:
                line_end = len(raw)
            line = raw[line_start:line_end]
            label = CANDIDATE_LABEL.search(raw[line_start:start])
            reasons = [reason]
            if label:
                reasons.append("contextual_statistic")
            if re.search(r"\bCI\b|confidence\s+interval", line, re.I) or re.search(r"\[[^\]]*\]", line):
                reasons.append("ci_location_hint")
            if len(list(NUMBER.finditer(line))) >= 3 and re.search(r"\S[ \t]{2,}\S", line):
                reasons.append("table_location_hint")
            found[token].append({
                "raw_token": raw[start:match.end()], "raw_start": start,
                "raw_end": match.end(), "raw_line": line_index + 1,
                "raw_column": start - line_start + 1,
                "raw_end_line": bisect_right(line_starts, match.end() - 1),
                "literal_interpretation": _canonical(match),
                "candidate_interpretation": token, "reasons": reasons,
                "statistic_label": label.group("label") if label else None,
                "ambiguous": True, "requires_raw_verification": True,
            })
    return found


def _clause(text: str, position: int) -> str:
    """Return a verbatim sentence/semicolon/line span containing the token."""
    start = 0
    for boundary in re.finditer(r"\n|(?<=[;!?])\s+|(?<=\.)\s+(?=[A-Z])", text):
        if boundary.start() >= position:
            return text[start:boundary.start()].strip()
        start = boundary.end()
    return text[start:].strip()


def analyze_note(note_path: Path) -> dict:
    """Return JSON-serializable occurrence rows; raise on unreadable/invalid input.

    Relative text_path values resolve from SYNAPSE_ROOT, as in validate_note.
    Absent target sections are reported; a zero-token result is not verification.
    """
    note_path = Path(note_path).resolve()
    fm, body = split_frontmatter(note_path.read_text(encoding="utf-8"))
    text_value = fm.get("text_path")
    if not isinstance(text_value, str) or not text_value.strip():
        raise ValueError("frontmatter text_path must be a nonempty string")
    text_path = (SYNAPSE_ROOT / text_value).resolve()
    raw = text_path.read_text(encoding="utf-8", errors="replace")
    literal, artifacts = _source_counts(raw)
    sections = parse_body_sections(body)
    if "Hypotheses" in sections and "Hypotheses / Propositions" not in sections:
        sections["Hypotheses / Propositions"] = sections["Hypotheses"]
    rows = []
    for section in SECTIONS:
        content = sections.get(section, "")
        for match in NUMBER.finditer(_masked(content, note=True)):
            token = _canonical(match, note=True)
            rows.append({
                "section": section,
                "token": content[match.start():match.end()],
                "normalized_token": token,
                "clause": _clause(content, match.start()),
                "hit_count": literal[token] + artifacts[token],
                "literal_hit_count": literal[token],
                "artifact_hit_count": artifacts[token],
            })
    zero_hits = [row for row in rows if row["hit_count"] == 0]
    candidates = _source_candidates(raw, {
        row["normalized_token"] for row in rows
        if row["literal_hit_count"] == 0 and row["normalized_token"].startswith("-")
    })
    for row in rows:
        row["candidates"] = candidates.get(row["normalized_token"], [])
        row["requires_raw_verification"] = row["literal_hit_count"] == 0
    return {
        "note_path": str(note_path), "text_path": str(text_path),
        "advisory": ADVISORY,
        "sections_present": [name for name in SECTIONS if name in sections],
        "sections_missing": [name for name in SECTIONS if name not in sections],
        "tokens": rows, "zero_hits": zero_hits,
        "totals": {"tokens": len(rows), "tokens_with_hits": len(rows) - len(zero_hits),
                   "zero_hits": len(zero_hits)},
    }


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path)
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = parser.parse_args(argv)
    try:
        report = analyze_note(args.note)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"check_numbers: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(ADVISORY)
        print("\n| Section | Token | Hits | Literal | Glyph |")
        print("|---|---|---:|---:|---:|")
        for row in report["tokens"]:
            print("| " + " | ".join(_cell(row[key]) for key in
                  ("section", "token", "hit_count", "literal_hit_count", "artifact_hit_count")) + " |")
        print("\nZero-hit tokens\n\n| Section | Token | Verbatim clause |\n|---|---|---|")
        for row in report["zero_hits"]:
            print("| " + " | ".join(_cell(row[key]) for key in ("section", "token", "clause")) + " |")
        print("\nCandidate locations (not hits; raw verification required)")
        for row in report["tokens"]:
            for candidate in row["candidates"]:
                print(f"- {row['normalized_token']}: line {candidate['raw_line']}, "
                      f"column {candidate['raw_column']}, {candidate['raw_token']!r}; "
                      + ", ".join(candidate["reasons"]))
        print(f"\nTotals: {report['totals']}")
        if report["sections_missing"]:
            print("Sections absent (not checked): " + ", ".join(report["sections_missing"]))
    return 1 if report["zero_hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
