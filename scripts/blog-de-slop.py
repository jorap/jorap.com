#!/usr/bin/env python3
"""Mechanical blog de-slop: wiki footers and ## Bottom line headings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "content/english/blog"
SKIP = frozenset({"_index.md", "__blog-template.md"})
WIKI_FOOTER = re.compile(
    r"^\*Expanded from .+\*$\n?|^\*Idea captured from .+\*$\n?",
    re.M,
)
BOTTOM_BLOCK = re.compile(r"\n---\n\n## Bottom line\n\n", re.M)


def de_slop(text: str) -> str:
    text = WIKI_FOOTER.sub("", text)
    text = BOTTOM_BLOCK.sub("\n\n", text)
    # trailing ## Bottom line without preceding ---
    text = re.sub(r"\n---\n\n## Bottom line\n\n", "\n\n", text)
    if text.endswith("\n\n\n"):
        text = text.rstrip("\n") + "\n"
    return text


def process(path: Path, write: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    fixed = de_slop(raw)
    if fixed == raw:
        return False
    if write:
        path.write_text(fixed, encoding="utf-8")
    return True


def _self_check() -> None:
    sample = "---\n\n## Bottom line\n\nDone.\n\n*Expanded from [x](https://ideas.jorap.com/).*\n"
    out = de_slop(sample)
    assert "## Bottom line" not in out
    assert "Expanded from" not in out
    assert "Done." in out


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("blog-de-slop self-check OK")
        return 0

    write = "--write" in sys.argv
    changed = 0
    for path in sorted(BLOG.glob("*.md")):
        if path.name in SKIP:
            continue
        if process(path, write):
            changed += 1
            label = "de-slopped" if write else "would de-slop"
            print(f"  {label} {path.relative_to(ROOT)}")
    if write:
        print(f"\nDone: {changed} file(s)")
    elif changed:
        print(f"\n{changed} file(s) would change (pass --write)")
    else:
        print("No mechanical de-slop needed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
