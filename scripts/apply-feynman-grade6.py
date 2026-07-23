#!/usr/bin/env python3
"""Insert Feynman grade-6 simplification as key_concept bullet 2.

Reads data/feynman-grade6-bullets.yaml: {slug: bullet text}
Inserts before current bullet 2; existing bullets shift down.
Skips slugs already present as bullet 2 (exact match after normalize).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
DATA = ROOT / "data" / "feynman-grade6-bullets.yaml"
BIBLE_RE = re.compile(r"^\s*\{\{<\s*bible\b", re.I)
BULLET_RE = re.compile(r"^\s*-\s+")


def parse_key_concept_block(block: str) -> tuple[list[str], list[str]]:
    """Return (prefix lines, bullet texts) from key_concept block scalar."""
    prefix: list[str] = []
    bullets: list[str] = []
    in_bullets = False
    for raw in block.splitlines():
        stripped = raw.strip()
        if BULLET_RE.match(raw):
            in_bullets = True
            bullets.append(stripped[2:].strip())
        elif not in_bullets and stripped:
            prefix.append(stripped)
    return prefix, bullets


def rebuild_key_concept(prefix: list[str], bullets: list[str]) -> str:
    lines: list[str] = []
    lines.extend(prefix)
    if prefix and bullets:
        lines.append("")
    for b in bullets:
        lines.append(f"- {b}")
    return "\n".join(lines) + ("\n" if lines else "")


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def apply_note(path: Path, grade6: str, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    if not raw_fm:
        return "no-fm"
    fm = yaml.safe_load(raw_fm) or {}
    kc = fm.get("key_concept")
    if not isinstance(kc, str) or not kc.strip():
        return "no-kc"
    prefix, bullets = parse_key_concept_block(kc)
    if not bullets:
        return "no-bullets"
    grade6 = grade6.strip()
    if not grade6:
        return "empty"
    if len(bullets) > 1 and norm(bullets[1]) == norm(grade6):
        return "skip"
    bullets = [bullets[0], grade6, *bullets[1:]]
    fm["key_concept"] = rebuild_key_concept(prefix, bullets)
    if dry_run:
        return "dry"
    path.write_text(f"---\n{dump_frontmatter(fm)}\n---\n{body}", encoding="utf-8")
    return "ok"


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not DATA.exists():
        print(f"missing {DATA}", file=sys.stderr)
        return 1
    data = yaml.safe_load(DATA.read_text(encoding="utf-8")) or {}
    counts: dict[str, int] = {}
    for slug, bullet in data.items():
        path = NOTES / f"{slug}.md"
        if not path.exists():
            print(f"missing note: {slug}")
            counts["missing"] = counts.get("missing", 0) + 1
            continue
        status = apply_note(path, str(bullet), dry_run=dry)
        counts[status] = counts.get(status, 0) + 1
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
