#!/usr/bin/env python3
"""Replace em/en dashes in all note files (jorap-voice: no em dashes)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"


def sanitize(text: str) -> str:
    return text.replace("\u2014", "-").replace("\u2013", "-")


def main() -> None:
    count = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        fixed = sanitize(raw)
        if fixed != raw:
            path.write_text(fixed, encoding="utf-8")
            count += 1
            print(f"  sanitized {path.name}")
    print(f"\nDone: {count} files updated.")


if __name__ == "__main__":
    main()
