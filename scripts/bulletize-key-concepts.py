#!/usr/bin/env python3
"""Convert key_concept prose blocks to bullets; keep bible shortcodes and tables as-is."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}

BIBLE_RE = re.compile(r"^\{\{<\s*bible\b", re.I)
TABLE_RE = re.compile(r"^\|")
BULLET_RE = re.compile(r"^-\s+")


def bulletize_key_concept(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    prose: list[str] = []

    def flush_prose() -> None:
        if not prose:
            return
        content = " ".join(s.strip() for s in prose if s.strip())
        prose.clear()
        if not content:
            return
        if BULLET_RE.match(content):
            out.append(content)
        else:
            out.append(f"- {content}")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_prose()
            if out and out[-1] != "":
                out.append("")
            continue
        if BIBLE_RE.match(stripped):
            flush_prose()
            out.append(stripped)
            continue
        if TABLE_RE.match(stripped):
            flush_prose()
            out.append(stripped)
            continue
        if BULLET_RE.match(stripped):
            flush_prose()
            out.append(stripped)
            continue
        prose.append(stripped)

    flush_prose()
    # Collapse trailing blank lines; keep single blanks between blocks.
    trimmed: list[str] = []
    for line in out:
        if line == "" and trimmed and trimmed[-1] == "":
            continue
        trimmed.append(line)
    return "\n".join(trimmed).rstrip("\n")


def process_note(path: Path, dry_run: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    kc = fm.get("key_concept")
    if not isinstance(kc, str) or not kc.strip():
        return False
    new_kc = bulletize_key_concept(kc)
    if new_kc == kc.rstrip("\n"):
        return False
    if dry_run:
        print(path.name)
        return True
    fm["key_concept"] = new_kc
    path.write_text(f"---\n{dump_frontmatter(fm)}\n---\n{body}", encoding="utf-8")
    return True


def _self_check() -> None:
    kc = (
        '{{< bible ref="Matthew 7:7" >}}\n'
        "Keep asking.\n"
        "\n"
        "Second point here.\n"
        "\n"
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |"
    )
    out = bulletize_key_concept(kc)
    assert '{{< bible ref="Matthew 7:7" >}}' in out
    assert "- Keep asking." in out
    assert "- Second point here." in out
    assert "| A | B |" in out
    assert not out.startswith("- {{")


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("bulletize-key-concepts self-check OK")
        return 0

    dry_run = "--dry-run" in sys.argv
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        if process_note(path, dry_run=dry_run):
            changed += 1
    print(f"{'Would change' if dry_run else 'Changed'} {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
