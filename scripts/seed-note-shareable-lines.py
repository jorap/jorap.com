#!/usr/bin/env python3
"""Draft or verify shareable_lines frontmatter on garden notes (3 lines, max 130 chars)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
MAX_LINE = 130
LINE_COUNT = 3
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")
SKIP_LINE = re.compile(r"^\s*\|")


def plain(text: str) -> str:
    text = WIKILINK.sub(r"\1", text)
    return " ".join(text.split())


def clamp(text: str, limit: int = MAX_LINE) -> str:
    text = plain(text)
    if len(text) <= limit:
        return text
    ellipsis = "…"
    room = limit - len(ellipsis)
    cut = text[: room + 1].rsplit(" ", 1)[0]
    if len(cut) > room:
        cut = cut[:room]
    if len(cut) < limit // 2:
        cut = text[:room]
    return cut.rstrip(".,;:-— ") + ellipsis


def add_candidate(bucket: list[str], raw: str) -> None:
    line = plain(raw.strip().lstrip("- "))
    if not line or SKIP_LINE.match(raw) or len(line) < 12:
        return
    shareable = clamp(line)
    if shareable and shareable not in bucket:
        bucket.append(shareable)


def draft_shareable_lines(fm: dict) -> list[str]:
    candidates: list[str] = []
    add_candidate(candidates, str(fm.get("description") or ""))

    key_concept = fm.get("key_concept")
    if isinstance(key_concept, str):
        for block in key_concept.split("\n\n"):
            for line in block.split("\n"):
                add_candidate(candidates, line)

    for ex in fm.get("examples") or []:
        if isinstance(ex, str):
            add_candidate(candidates, ex.split(" - ")[0])
            add_candidate(candidates, ex)

    title = plain(str(fm.get("title") or "Note"))
    desc = plain(str(fm.get("description") or ""))
    fallbacks = [
        clamp(desc) if desc else clamp(title),
        clamp(f"{title} — {desc}") if desc else clamp(f"On {title} in the garden."),
        clamp(f"More on {title} in JoRap Notes."),
    ]
    for fb in fallbacks:
        if len(candidates) >= LINE_COUNT:
            break
        if fb and fb not in candidates:
            candidates.append(fb)

    return candidates[:LINE_COUNT]


def lint_shareable_lines(path: Path, fm: dict) -> list[str]:
    if path.name in SKIP:
        return []
    lines = fm.get("shareable_lines")
    if not isinstance(lines, list) or len(lines) != LINE_COUNT:
        return [f"FAIL shareable_lines need {LINE_COUNT} items: {path.name}"]
    errs: list[str] = []
    for i, line in enumerate(lines):
        if not isinstance(line, str) or not line.strip():
            errs.append(f"FAIL shareable_lines[{i}] empty: {path.name}")
            continue
        if len(line) > MAX_LINE:
            errs.append(f"FAIL shareable_lines[{i}] {len(line)} chars (max {MAX_LINE}): {path.name}")
        if "[[" in line:
            errs.append(f"FAIL wikilink in shareable_lines[{i}]: {path.name}")
    return errs


def write_shareable_lines(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    if not isinstance(fm, dict):
        return False
    fm["shareable_lines"] = draft_shareable_lines(fm)
    new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def _self_check() -> None:
    sample = {
        "title": "Capture",
        "description": "Save what resonates into one inbox I trust - then empty it weekly.",
        "key_concept": "Friction kills capture.\n\nOne inbox, weekly process.",
        "examples": ["Jeepney spark on a receipt - one pocket notebook, no sorting yet."],
    }
    lines = draft_shareable_lines(sample)
    assert len(lines) == 3
    assert all(len(t) <= MAX_LINE for t in lines)
    assert all("[[" not in t for t in lines)
    errs = lint_shareable_lines(Path("capture.md"), {"shareable_lines": lines})
    assert not errs


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("seed-note-shareable-lines self-check OK")
        return 0

    check_only = "--check" in sys.argv
    bad = 0
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, _ = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        if check_only:
            for msg in lint_shareable_lines(path, fm):
                print(msg)
                bad += 1
            continue
        if write_shareable_lines(path):
            changed += 1

    if check_only:
        if bad:
            print(f"\n{bad} shareable_lines lint issue(s)")
            return 1
        print("Note shareable_lines lint OK")
        return 0

    print(f"Wrote shareable_lines on {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
