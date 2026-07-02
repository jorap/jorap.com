#!/usr/bin/env python3
"""Rewrite note frontmatter with notes_content.dump_frontmatter (preserves | blocks)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {
    "_index.md",
    "graph.md",
    "cards.md",
    "review.md",
    "backlinks.md",
    "create.md",
    "issues.md",
    "random-duo.md",
}


def needs_reformat(raw_fm: str) -> bool:
    if re.search(r'^key_concept:\s*["\']', raw_fm, re.M):
        return True
    if re.search(r"^examples:\s*\n- ", raw_fm, re.M):  # unquoted list items
        return True
    if re.search(r"^  wikilink: '\[\[", raw_fm, re.M):
        return True
    return False


def main() -> int:
    force = "--all" in sys.argv
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        if not raw_fm:
            continue
        if not force and not needs_reformat(raw_fm):
            continue
        meta = yaml.safe_load(raw_fm) or {}
        out = f"---\n{dump_frontmatter(meta)}\n---\n{body.lstrip()}"
        if out != text:
            path.write_text(out, encoding="utf-8")
            n += 1
    print(f"Reformatted {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
