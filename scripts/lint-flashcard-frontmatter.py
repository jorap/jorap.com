#!/usr/bin/env python3
"""Validate flashcard frontmatter on review notes (cards, card_sets)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

CARD_ITEM_RE = re.compile(
    r'^\s+-\s+front:\s+("(?:[^"\\]|\\.)*"|[^\n]+)\s*\n\s+back:\s+("(?:[^"\\]|\\.)*"|[^\n]+)\s*$',
    re.M,
)
QUOTED_RE = re.compile(r'^"(?:[^"\\]|\\.)*"$')


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end].strip(), text[end + 4 :]


def parse_bool(block: str, key: str) -> bool:
    match = re.search(rf"^{key}:\s*(true|false)\s*$", block, re.M)
    return match.group(1) == "true" if match else False


def parse_cards(block: str) -> list[tuple[str, str, str]]:
    """Return (front_raw, back_raw, raw_block) for each card."""
    if not re.search(r"^cards:\s*$", block, re.M):
        return []
    cards: list[tuple[str, str, str]] = []
    for match in CARD_ITEM_RE.finditer(block):
        cards.append((match.group(1).strip(), match.group(2).strip(), match.group(0)))
    return cards


def parse_card_sets(block: str) -> list[str]:
    match = re.search(r"^card_sets:\s*\[(.*)\]\s*$", block, re.M)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def is_quoted(value: str) -> bool:
    return bool(QUOTED_RE.match(value))


def lint_file(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    block, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    if not block:
        return errors

    if not parse_bool(block, "review"):
        return errors

    sets = parse_card_sets(block)
    cards = parse_cards(block)

    if not sets:
        errors.append(f"{rel}: review: true requires card_sets (inline list, quoted names)")
    for item in sets:
        if not is_quoted(item):
            errors.append(f"{rel}: card_sets entry must be double-quoted: {item}")

    if re.search(r"^card_sets:\s*$", block, re.M):
        errors.append(f"{rel}: card_sets must use inline [...] format like categories/tags")

    if not cards:
        errors.append(f"{rel}: review: true requires cards (block list with front/back pairs)")
    for front, back, _ in cards:
        if not is_quoted(front):
            errors.append(f"{rel}: card front must be double-quoted: {front[:60]}")
        if not is_quoted(back):
            errors.append(f"{rel}: card back must be double-quoted: {back[:60]}")

    if re.search(r"^cards:\s*\[", block, re.M):
        errors.append(f"{rel}: cards must use block list format, not inline [...]")

    if re.search(r'meta_title:.*\|\s*JoRap Notes', block):
        errors.append(f"{rel}: remove | JoRap Notes from meta_title (appended automatically)")

    return errors


def main() -> int:
    errors: list[str] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        errors.extend(lint_file(path))

    if errors:
        print("Flashcard frontmatter errors:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print("Flashcard frontmatter OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
