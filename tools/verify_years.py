#!/usr/bin/env python3
"""
verify_years.py — year-only alias for `verify_metadata.py`.

This file used to be a standalone script (introduced in v0.11.1 to surface
issue-year vs online-first-year mismatches). When `verify_metadata.py`
arrived as a comprehensive bibliographic-integrity checker, the year-only
logic was absorbed into it. This file is preserved as a thin alias so that:

  - existing docs that reference `tools/verify_years.py` still work;
  - the v0.11.1 release commit (`00cf744`) and its surrounding docs
    remain accurate after the fact;
  - any external script or CI pipeline that was wired to call
    `verify_years.py` keeps working unchanged.

It is exactly equivalent to `python tools/verify_metadata.py --field year`
plus whatever other flags you pass (--tsv, --quiet, --paper-id, --no-cache).

For new work, prefer calling verify_metadata.py directly — it surfaces the
broader class of bibliographic errors (title typos, missing volume/issue,
swapped authors) that this year-only check cannot catch.
"""
from __future__ import annotations

import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))

# Force --field year unless the caller explicitly passed --field. This
# preserves v0.11.1 semantics: `verify_years.py` checks years and only
# years, regardless of any default-changes in verify_metadata.py.
if not any(a == "--field" or a.startswith("--field=") for a in sys.argv[1:]):
    sys.argv.insert(1, "--field")
    sys.argv.insert(2, "year")

from verify_metadata import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
