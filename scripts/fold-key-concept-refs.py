#!/usr/bin/env python3
"""Fold standalone Bible ref lines into the key_concept paragraph above."""

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

NOTES = Path(__file__).resolve().parents[1] / "content/english/notes"
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

REF_LINE = re.compile(
    r"^(?:[1-3]?\s*[A-Za-z]+\s+)?\d+:\d+(?:-\d+)?(?:\s*[;,]\s*(?:[1-3]?\s*[A-Za-z]+\s+)?\d+:\d+(?:-\d+)?)*\.?$"
)


def fold_key_concept(kc: str) -> str:
    lines = kc.split("\n")
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped and REF_LINE.fullmatch(stripped.replace(" ", " ").strip()):
            if out:
                ref = stripped.rstrip(".")
                prev = out[-1].rstrip()
                if ref not in prev:
                    out[-1] = f"{prev.rstrip('.')} ({ref})."
            continue
        out.append(line)
    return "\n".join(out).strip()


def main() -> int:
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw, body = split_frontmatter(text)
        if not raw:
            continue
        meta = yaml.safe_load(raw) or {}
        kc = meta.get("key_concept")
        if not isinstance(kc, str):
            continue
        new_kc = fold_key_concept(kc)
        if new_kc == kc:
            continue
        meta["key_concept"] = new_kc
        path.write_text(f"---\n{dump_frontmatter(meta)}\n---\n{body.lstrip()}", encoding="utf-8")
        n += 1
    print(f"Fixed {n} key_concept ref lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
