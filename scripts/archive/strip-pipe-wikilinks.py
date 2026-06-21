#!/usr/bin/env python3
"""Replace [[target|label]] with [[target]] in note bodies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = ROOT / "content/english/notes"

PIPE_WIKILINK = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")


def strip_pipes(text: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"[[{match.group(1).strip()}]]"

    return PIPE_WIKILINK.sub(repl, text), count


def main() -> int:
    total = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        fm = text[: end + 4]
        body = text[end + 4 :]
        new_body, n = strip_pipes(body)
        if n:
            path.write_text(fm + new_body, encoding="utf-8")
            print(f"  {path.name}: {n} pipe wikilink(s)")
            total += n
    print(f"\nDone: {total} pipe wikilink(s) removed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
