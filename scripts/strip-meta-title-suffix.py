#!/usr/bin/env python3
"""Remove legacy manual SEO suffixes from meta_title frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SUFFIXES = ("JoRap Notes", "JoRap", "Notes Garden")
META_LINE = re.compile(
    r'^(meta_title:\s*)(["\'])(.*?)\2\s*$',
    re.MULTILINE,
)


def strip_suffix(value: str) -> str:
    updated = value
    for _ in range(5):
        for suffix in SUFFIXES:
            if updated.endswith(f" | {suffix}"):
                updated = updated[: -len(f" | {suffix}")].rstrip()
    return updated


def clean_file(path: Path) -> bool:
    text = path.read_text()
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        prefix, quote, value = match.group(1), match.group(2), match.group(3)
        cleaned = strip_suffix(value)
        if cleaned != value:
            changed = True
        return f"{prefix}{quote}{cleaned}{quote}"

    updated = META_LINE.sub(repl, text)
    if changed:
        path.write_text(updated)
    return changed


def main() -> int:
    changed_files = [p for p in sorted(CONTENT.rglob("*.md")) if clean_file(p)]
    for path in changed_files:
        print(path.relative_to(ROOT))
    print(f"Updated {len(changed_files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
