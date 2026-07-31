#!/usr/bin/env python3
"""Move Level 1-5 bullets from key_concept into level_1..level_5 fields."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from notes_content import (
    LEVEL_KEYS,
    dump_frontmatter,
    extract_levels_from_key_concept,
    split_frontmatter,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}


def load_fm(raw_fm: str) -> dict:
    data = yaml.safe_load(raw_fm) or {}
    return data if isinstance(data, dict) else {}


def migrate_file(path: Path, *, write: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = load_fm(raw_fm)
    kc = fm.get("key_concept")
    if not isinstance(kc, str) or not kc.strip():
        return False

    cleaned, extracted = extract_levels_from_key_concept(kc)
    if not extracted:
        return False

    fm["key_concept"] = cleaned
    for key in LEVEL_KEYS:
        if key in extracted:
            fm[key] = extracted[key]

    if not write:
        return True

    out = f"---\n{dump_frontmatter(fm)}\n---"
    body_text = body.lstrip("\n")
    path.write_text(f"{out}\n{body_text}" if body_text else f"{out}\n", encoding="utf-8")
    return True


def main() -> int:
    write = "--write" in sys.argv
    paths = sorted(p for p in NOTES.glob("*.md") if p.name not in SKIP)
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    if named:
        paths = [NOTES / named[0]]

    count = 0
    for path in paths:
        if migrate_file(path, write=write):
            count += 1
            print(path.name)

    action = "migrated" if write else "would migrate"
    print(f"\n{count} note(s) {action}")
    if not write and count:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
