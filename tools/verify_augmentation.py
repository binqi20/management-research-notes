#!/usr/bin/env python3
"""
verify_augmentation.py — mechanical diff-guard for the v2→v3 backfill.

The augmentation pipeline (docs/augmentation-prompt.md) promises that upgrading
a v2 note to v3 ADDS three body sections, three evidence anchors, a version
bump, and two provenance lines — and changes NOTHING else. This tool makes that
promise checked, not assumed: it diffs the augmented note against its
pre-augmentation state and fails on any change outside the permitted delta.

It is the backfill's Layer 0, run after every augmentation and before the
independent Layer 2 audit. The audited v2 prose is the asset being protected:
a silent rewording of an already-audited field would invalidate its audit
without anyone noticing.

Checks:
  1. Old note is extraction_version "v2"; new note is "v3".
  2. Frontmatter: every original key except `extraction_version` is
     value-identical (parsed comparison, so cosmetic YAML restyling of an
     untouched value does not false-positive — but see check 4 for anchors);
     exactly two new keys added: `augmented_model` (non-empty string) and
     `augmented_at` (YYYY-MM-DD). No other additions or removals.
  3. Body: the pre-heading region (title line) is byte-identical; each of the
     8 original v2 sections is byte-identical (as parsed); the new heading
     order is exactly the 11-heading v3 order; the three new sections are
     non-empty.
  4. Evidence: for editorial/book-review, the block is untouched (absent stays
     absent; present stays exactly equal, no new keys). For all other types,
     every original anchor key is present with a string-identical value, and
     exactly the three v3 keys (`hypotheses_source`, `measures_overview`,
     `findings_overview`) are added.

Usage:
  python3 tools/verify_augmentation.py notes/<paper_id>.md
      # compares against the git HEAD version of the same path (the normal
      # batch flow: trees are clean before an augmentation wave starts)
  python3 tools/verify_augmentation.py notes/<paper_id>.md --before <file>
      # compares against an explicit pre-state file (used by the tests)

Exit codes: 0 = augmentation is exactly the permitted delta; 1 = violations
(each printed); 2 = usage/parse error.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
SYNAPSE_ROOT = THIS_FILE.parent.parent
sys.path.insert(0, str(THIS_FILE.parent))

from validate_note import (  # noqa: E402
    REQUIRED_HEADINGS,
    REQUIRED_HEADINGS_V3,
    split_frontmatter,
)

V2_HEADINGS = [h for h, _ in REQUIRED_HEADINGS]
V3_HEADINGS = [h for h, _ in REQUIRED_HEADINGS_V3]
NEW_HEADINGS = [h for h in V3_HEADINGS if h not in V2_HEADINGS]
NEW_ANCHOR_KEYS = {"hypotheses_source", "measures_overview", "findings_overview"}
EVIDENCE_FROZEN_TYPES = {"editorial", "book-review"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def split_body_regions(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (pre-heading region, [(heading, content), ...]) preserving order.

    Same delimiter grammar as validate_note.parse_body_sections, but kept as an
    ordered list (duplicate-safe) and exposing the pre-heading title region.
    """
    parts = re.split(r"^\*\*([^*]+)\*\*\s*\n", body, flags=re.MULTILINE)
    pre = parts[0]
    sections: list[tuple[str, str]] = []
    i = 1
    while i + 1 < len(parts):
        sections.append((parts[i].strip(), parts[i + 1].strip()))
        i += 2
    return pre, sections


def load_before_text(note_path: Path, before: str | None) -> str:
    if before is not None:
        return Path(before).read_text(encoding="utf-8")
    rel = note_path.resolve().relative_to(SYNAPSE_ROOT)
    proc = subprocess.run(
        ["git", "show", f"HEAD:{rel.as_posix()}"],
        capture_output=True, text=True, cwd=SYNAPSE_ROOT,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"ERROR: cannot read pre-augmentation state from git HEAD for {rel}\n"
            f"  {proc.stderr.strip()}\n"
            f"  (Is the note new/renamed? Pass --before <file> explicitly.)"
        )
    return proc.stdout


def verify(old_text: str, new_text: str) -> list[str]:
    errors: list[str] = []
    try:
        old_fm, old_body = split_frontmatter(old_text)
        new_fm, new_body = split_frontmatter(new_text)
    except (ValueError, Exception) as exc:  # yaml errors subclass Exception
        return [f"parse error: {exc}"]

    # -- 1. version gate ---------------------------------------------------------
    if old_fm.get("extraction_version") != "v2":
        errors.append(
            f"pre-state is extraction_version {old_fm.get('extraction_version')!r}, "
            "not 'v2' — only v2 notes are augmented (v1 notes are re-extracted)"
        )
    if new_fm.get("extraction_version") != "v3":
        errors.append(
            f"augmented note is extraction_version "
            f"{new_fm.get('extraction_version')!r}, expected 'v3'"
        )

    # -- 2. frontmatter delta ------------------------------------------------------
    old_keys, new_keys = set(old_fm), set(new_fm)
    missing = old_keys - new_keys
    if missing:
        errors.append(f"frontmatter keys removed: {sorted(missing)}")
    added = new_keys - old_keys
    allowed_added = {"augmented_model", "augmented_at"}
    unexpected = added - allowed_added
    if unexpected:
        errors.append(f"unexpected new frontmatter keys: {sorted(unexpected)}")
    for key in sorted(allowed_added - added):
        errors.append(f"required provenance key missing: {key}")
    am = new_fm.get("augmented_model")
    if "augmented_model" in new_fm and (not isinstance(am, str) or not am.strip()):
        errors.append("augmented_model must be a non-empty string")
    aa = new_fm.get("augmented_at")
    if "augmented_at" in new_fm and (
        not isinstance(aa, str) or not DATE_RE.match(aa.strip())
    ):
        errors.append(f"augmented_at must be YYYY-MM-DD, got {aa!r}")

    for key in sorted(old_keys & new_keys - {"extraction_version", "evidence"}):
        if old_fm[key] != new_fm[key]:
            errors.append(f"frontmatter value changed for {key!r} (forbidden)")

    # -- 3. evidence delta ---------------------------------------------------------
    paper_type = old_fm.get("paper_type", "")
    old_ev, new_ev = old_fm.get("evidence"), new_fm.get("evidence")
    if paper_type in EVIDENCE_FROZEN_TYPES:
        if old_ev != new_ev:
            errors.append(
                f"evidence block must be untouched for paper_type {paper_type!r}"
            )
    else:
        if not isinstance(old_ev, dict):
            errors.append(
                f"pre-state has no evidence mapping (paper_type {paper_type!r}) — "
                "this note is not a well-formed v2 note; do not augment it"
            )
        elif not isinstance(new_ev, dict):
            errors.append("augmented note lost its evidence mapping")
        else:
            for k, v in old_ev.items():
                if k not in new_ev:
                    errors.append(f"original evidence anchor removed: {k!r}")
                elif new_ev[k] != v:
                    errors.append(f"original evidence anchor changed: {k!r} (forbidden)")
            added_ev = set(new_ev) - set(old_ev)
            if added_ev - NEW_ANCHOR_KEYS:
                errors.append(
                    f"unexpected new evidence keys: {sorted(added_ev - NEW_ANCHOR_KEYS)}"
                )
            for k in sorted(NEW_ANCHOR_KEYS - set(new_ev)):
                errors.append(f"required v3 evidence anchor missing: {k!r}")

    # -- 4. body delta ---------------------------------------------------------------
    old_pre, old_sections = split_body_regions(old_body)
    new_pre, new_sections = split_body_regions(new_body)
    if old_pre != new_pre:
        errors.append("pre-heading region (title line) changed (forbidden)")

    old_map = dict(old_sections)
    new_map = dict(new_sections)
    new_order = [h for h, _ in new_sections]
    if new_order != V3_HEADINGS:
        errors.append(
            "augmented body headings are not the canonical v3 order:\n"
            f"  expected: {V3_HEADINGS}\n"
            f"  found:    {new_order}"
        )
    old_order = [h for h, _ in old_sections]
    if old_order != V2_HEADINGS:
        errors.append(
            f"pre-state body headings are not the v2 order (found {old_order}) — "
            "refusing to certify an augmentation over a malformed base"
        )
    for heading in V2_HEADINGS:
        if heading in old_map and heading in new_map and old_map[heading] != new_map[heading]:
            errors.append(f"original section {heading!r} content changed (forbidden)")
    for heading in NEW_HEADINGS:
        if heading in new_map and not new_map[heading].strip():
            errors.append(f"new section {heading!r} is empty")

    return errors


def main() -> int:
    args = sys.argv[1:]
    before = None
    if "--before" in args:
        i = args.index("--before")
        try:
            before = args[i + 1]
        except IndexError:
            print("--before requires a path", file=sys.stderr)
            return 2
        del args[i : i + 2]
    if len(args) != 1:
        print("usage: verify_augmentation.py notes/<paper_id>.md [--before <file>]",
              file=sys.stderr)
        return 2
    note_path = Path(args[0])
    if not note_path.exists():
        print(f"note does not exist: {note_path}", file=sys.stderr)
        return 2

    try:
        old_text = load_before_text(note_path, before)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2
    new_text = note_path.read_text(encoding="utf-8")

    errors = verify(old_text, new_text)
    if errors:
        print(f"FAIL  {note_path} — augmentation violates the permitted delta:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK    {note_path} — augmentation is exactly the permitted delta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
