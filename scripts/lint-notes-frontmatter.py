#!/usr/bin/env python3
"""Verify atomic notes keep structured data in frontmatter, not body sections."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}


def load_fm(raw_fm: str) -> dict:
    try:
        data = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError:
        data = {}
    return data if isinstance(data, dict) else {}


MAX_DESCRIPTION_WORDS = 20
MAX_SHAREABLE_LINE_CHARS = 130
SHAREABLE_LINE_COUNT = 4
TITLE_MAX_WORDS = 4
TITLE_FIVE_MIN_LEN = 30
# ponytail: phrase/scripture titles; lint cannot judge "better than best 4-word"
TITLE_PHRASE_EXEMPT = frozenset(
    {"Let Your Yes Be Yes", "There Is No Perfect Solution"}
)


def lint_title(path: Path, fm: dict) -> list[str]:
    if fm.get("note_kind", "note") in {"meta", "index"}:
        return []
    title = fm.get("title")
    if not isinstance(title, str) or not title.strip():
        return [f"FAIL missing title: {path.name}"]
    title = title.strip()
    words = len(title.split())
    if words <= TITLE_MAX_WORDS:
        return []
    if words > TITLE_MAX_WORDS + 1:
        return [f"FAIL title {words} words (max {TITLE_MAX_WORDS + 1}): {path.name}"]
    if title in TITLE_PHRASE_EXEMPT:
        return []
    if len(title) < TITLE_FIVE_MIN_LEN:
        return [
            f"FAIL title 5 words, {len(title)} chars "
            f"(need ≥{TITLE_FIVE_MIN_LEN} or trim to 4): {path.name}"
        ]
    return []


def lint_shareable_lines(path: Path, fm: dict) -> list[str]:
    if path.name in SKIP:
        return []
    lines = fm.get("shareable_lines")
    if not isinstance(lines, list) or len(lines) != SHAREABLE_LINE_COUNT:
        return [f"FAIL shareable_lines need {SHAREABLE_LINE_COUNT} items: {path.name}"]
    errs: list[str] = []
    for i, line in enumerate(lines):
        if not isinstance(line, str) or not line.strip():
            errs.append(f"FAIL shareable_lines[{i}] empty: {path.name}")
            continue
        if len(line) > MAX_SHAREABLE_LINE_CHARS:
            errs.append(f"FAIL shareable_lines[{i}] {len(line)} chars (max {MAX_SHAREABLE_LINE_CHARS}): {path.name}")
        if "[[" in line:
            errs.append(f"FAIL wikilink in shareable_lines[{i}]: {path.name}")
    return errs


def lint_description(path: Path, fm: dict) -> list[str]:
    """description = memorable one-breath definition; no wikilinks, <=20 words."""
    if fm.get("note_kind", "note") in {"meta", "index"}:
        return []
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return [f"FAIL missing description: {path.name}"]
    desc = desc.strip()
    errs: list[str] = []
    if "[[" in desc:
        errs.append(f"FAIL wikilink in description: {path.name}")
    words = len(desc.split())
    if words > MAX_DESCRIPTION_WORDS:
        errs.append(f"FAIL description {words} words (max {MAX_DESCRIPTION_WORDS}): {path.name}")
    return errs


def verify() -> int:
    bad = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = load_fm(raw_fm)
        for heading in ("Key Concept", "Examples", "Note Relationships", "See also"):
            if re.match(rf"^## {re.escape(heading)}\s*$", body, re.M):
                print(f"FAIL body still has ## {heading}: {path.name}")
                bad += 1
        if not fm.get("key_concept") and fm.get("note_kind", "note") not in {"meta", "index"}:
            print(f"FAIL missing key_concept: {path.name}")
            bad += 1
        if body.strip() and fm.get("note_kind", "note") not in {"meta", "index"}:
            print(f"FAIL non-empty body on atomic note: {path.name}")
            bad += 1
        for msg in lint_title(path, fm):
            print(msg)
            bad += 1
        for msg in lint_description(path, fm):
            print(msg)
            bad += 1
        for msg in lint_shareable_lines(path, fm):
            print(msg)
            bad += 1
    return bad


def _self_check() -> None:
    assert not lint_title(Path("x.md"), {"title": "Golden Rule at Work"})
    assert not lint_title(Path("x.md"), {"title": "Let Your Yes Be Yes"})
    assert lint_title(Path("x.md"), {"title": "The Golden Rule at Work"})
    assert lint_title(Path("x.md"), {"title": "One Two Three Four Five Six"})
    assert not lint_title(Path("x.md"), {"title": "Integrity Without an Audience"})
    assert not lint_title(Path("x.md"), {"title": "There Is No Perfect Solution"})


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("lint-notes-frontmatter self-check OK")
        return 0

    bad = verify()
    if bad:
        print(f"\n{bad} note(s) failed frontmatter lint")
        return 1
    print("Note frontmatter lint OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
