#!/usr/bin/env python3
"""Remove key_concept bullets that repeat description."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, key_concept_overlaps_description, split_frontmatter, strip_description_from_key_concept

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}


def fix_note(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    if not isinstance(fm, dict):
        return False
    if fm.get("draft") or fm.get("note_kind", "note") in {"meta", "index"}:
        return False
    desc = fm.get("description")
    kc = fm.get("key_concept")
    if not isinstance(desc, str) or not isinstance(kc, str):
        return False
    if not key_concept_overlaps_description(desc, kc):
        return False
    fm["key_concept"] = strip_description_from_key_concept(kc, desc)
    new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    check_only = "--check" in sys.argv
    changed = 0
    bad = 0

    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, _ = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        if fm.get("draft") or fm.get("note_kind", "note") in {"meta", "index"}:
            continue
        desc = fm.get("description")
        kc = fm.get("key_concept")
        if not isinstance(desc, str) or not isinstance(kc, str):
            continue
        if not key_concept_overlaps_description(desc, kc):
            continue
        if check_only:
            print(f"FAIL description in key_concept: {path.name}")
            bad += 1
            continue
        if fix_note(path):
            changed += 1

    if check_only:
        if bad:
            print(f"\n{bad} note(s) repeat description in key_concept")
            return 1
        print("No description in key_concept")
        return 0

    print(f"Stripped description from key_concept on {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
