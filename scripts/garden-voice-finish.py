#!/usr/bin/env python3
"""Second-pass garden-voice fixes: faith verses, shareable overrides."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required")

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
FINISH = ROOT / "data/garden-voice-finish.yaml"
FM = re.compile(r"^(---\s*\n)(.*?)(\n---)", re.DOTALL)


def load_finish() -> tuple[dict[str, str], dict[str, list[str]]]:
    raw = yaml.safe_load(FINISH.read_text(encoding="utf-8")) or {}
    verses = {str(k): str(v) for k, v in (raw.get("verses") or {}).items()}
    shareable = {str(k): [str(x) for x in v] for k, v in (raw.get("shareable_fixes") or {}).items()}
    return verses, shareable


def prepend_verse(key_concept: str, shortcode: str) -> str:
    if shortcode in key_concept or "{{< bible" in key_concept:
        return key_concept
    return f"  {shortcode}\n{key_concept}"


def replace_shareable_block(fm: str, items: list[str]) -> str:
    header = re.search(r"^shareable_thought:\n", fm, re.M)
    if not header:
        return fm
    start = header.end()
    tail = fm[start:]
    next_key = re.search(r"^[a-z_][a-z0-9_]*:", tail, re.M)
    end = start + (next_key.start() if next_key else len(tail))
    block = "".join(f'  - "{item}"\n' for item in items)
    return fm[:start] + block + fm[end:]


def finish_file(path: Path, verses: dict[str, str], shareable: dict[str, list[str]]) -> bool:
    text = path.read_text(encoding="utf-8")
    match = FM.match(text)
    if not match:
        return False
    fm_open, fm, fm_close = match.group(1), match.group(2), match.group(3)
    meta = yaml.safe_load(fm) or {}
    if meta.get("note_kind") in ("meta", "index"):
        return False

    slug = path.stem
    changed = False

    if slug in verses:
        header = re.search(r"^key_concept: \|\n", fm, re.M)
        if header:
            start = header.end()
            tail = fm[start:]
            next_key = re.search(r"^[a-z_][a-z0-9_]*:", tail, re.M)
            end = start + (next_key.start() if next_key else len(tail))
            block = fm[start:end]
            new_block = prepend_verse(block, verses[slug])
            if new_block != block:
                fm = fm[:start] + new_block + fm[end:]
                changed = True

    if slug in shareable:
        new_fm = replace_shareable_block(fm, shareable[slug])
        if new_fm != fm:
            fm = new_fm
            changed = True

    if not changed:
        return False

    path.write_text(fm_open + fm + fm_close + text[match.end() :], encoding="utf-8")
    return True


def main() -> int:
    verses, shareable = load_finish()
    count = 0
    for path in sorted(NOTES.glob("*.md")):
        if finish_file(path, verses, shareable):
            print(f"  finished {path.relative_to(ROOT)}")
            count += 1
    print(f"Finished {count} notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
