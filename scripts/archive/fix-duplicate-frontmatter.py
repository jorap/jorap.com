#!/usr/bin/env python3
"""Fix duplicate frontmatter introduced by mark-notes-evergreen.py."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = ROOT / "content/english/notes"


def fix_duplicate_frontmatter(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end1 = text.find("\n---", 3)
    if end1 == -1:
        return None
    after_first = text[end1 + 4 :].lstrip("\n")
    if not after_first.startswith("title:"):
        return None

    lines = after_first.split("\n")
    fm_lines: list[str] = []
    body_lines: list[str] = []
    in_fm = True
    for line in lines:
        if in_fm and line and not re.match(r"^[a-z_]+:", line):
            in_fm = False
        if in_fm:
            fm_lines.append(line)
        else:
            body_lines.append(line)

    inner = "\n".join(fm_lines).strip()
    body = "\n".join(body_lines).lstrip("\n")
    return f"---\n{inner}\n---\n\n{body}"


def main() -> None:
    fixed = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        repaired = fix_duplicate_frontmatter(text)
        if repaired and repaired != text:
            path.write_text(repaired, encoding="utf-8")
            fixed += 1
            print(f"fixed: {path.name}")

    print(f"\nDone: {fixed} files repaired.")


if __name__ == "__main__":
    main()
