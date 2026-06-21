#!/usr/bin/env python3
"""Mark distilled atomic notes as status: evergreen."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {"_index", "graph"}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def add_status(inner: str) -> str:
    if re.search(r"^status:", inner, re.M):
        return inner
    if re.search(r"^draft:", inner, re.M):
        return re.sub(r"^(draft:.*)$", r"status: evergreen\n\1", inner, count=1, flags=re.M)
    return inner + "\nstatus: evergreen"


def main() -> None:
    updated = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        fm, inner, body = split_frontmatter(text)
        if not fm:
            continue
        new_inner = add_status(inner)
        if new_inner == inner:
            continue
        path.write_text(f"---\n{new_inner}\n---\n\n{body}", encoding="utf-8")
        updated += 1
        print(f"evergreen: {path.name}")

    print(f"\nDone: {updated} notes marked evergreen.")


if __name__ == "__main__":
    main()
