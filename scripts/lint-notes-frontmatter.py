#!/usr/bin/env python3
"""Verify atomic notes keep structured data in frontmatter, not body sections."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}


def load_fm(raw_fm: str) -> dict:
    try:
        data = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError:
        data = {}
    return data if isinstance(data, dict) else {}


def verify() -> int:
    bad = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = load_fm(raw_fm)
        for heading in ("Key Concept", "Examples", "Note Relationships", "See also"):
            if re.match(rf"^## {re.escape(heading)}\s*$", body, re.M):
                print(f"FAIL body still has ## {heading}: {path.name}")
                bad += 1
        if not fm.get("key_concept") and fm.get("note_kind", "note") not in {"meta", "index"}:
            print(f"FAIL missing key_concept: {path.name}")
            bad += 1
        if body.strip() and fm.get("note_kind", "note") not in {"meta", "index"}:
            print(f"FAIL non-empty body on atomic note: {path.name}")
            bad += 1
    return bad


def main() -> int:
    bad = verify()
    if bad:
        print(f"\n{bad} note(s) failed frontmatter lint")
        return 1
    print("Note frontmatter lint OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
