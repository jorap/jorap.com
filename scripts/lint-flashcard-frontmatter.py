#!/usr/bin/env python3
"""Validate flashcard frontmatter on garden notes (2/4/6/8 cards by tier)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

SKIP_STEMS = {
    "_index",
    "flashcards",
    "review",
    "graph",
    "issues",
    "random-duo",
    "create",
    "okf-export",
}
SKIP_KINDS = {"meta", "index"}
SKIP_LAYOUTS = {"graph", "cards", "review", "issues", "backlinks", "random-duo", "create"}
ALLOWED_COUNTS = {2, 4, 6, 8}

CARD_ITEM_RE = re.compile(
    r'^\s+-\s+front:\s+("(?:[^"\\]|\\.)*"|[^\n]+)\s*\n\s+back:\s+("(?:[^"\\]|\\.)*"|[^\n]+)\s*$',
    re.M,
)
QUOTED_RE = re.compile(r'^"(?:[^"\\]|\\.)*"$')

MC_COMMA_OR_RE = re.compile(r",\s*[^,\n]+,\s*or\s+", re.I)
MC_FORK_OR_RE = re.compile(r"\bor\b[^.?!\n]*\?", re.I)
MC_PICK_RE = re.compile(r"\b(pick one|choose between|one of)\b", re.I)


def is_multiple_choice_front(front: str) -> bool:
    if MC_PICK_RE.search(front):
        return True
    if MC_COMMA_OR_RE.search(front):
        return True
    if MC_FORK_OR_RE.search(front):
        return True
    return False


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


def is_garden_note(block: str, stem: str) -> bool:
    if stem in SKIP_STEMS:
        return False
    kind = re.search(r'^note_kind:\s*"?(\w+)"?', block, re.M)
    if kind and kind.group(1) in SKIP_KINDS:
        return False
    layout = re.search(r'^layout:\s*"?(\w+)"?', block, re.M)
    if layout and layout.group(1) in SKIP_LAYOUTS:
        return False
    return True


def lint_file(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    block, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    if not block or not is_garden_note(block, path.stem):
        return errors

    sets = parse_card_sets(block)
    cards = parse_cards(block)
    review = parse_bool(block, "review")

    if not review:
        errors.append(f"{rel}: garden notes require review: true")
    if not sets:
        errors.append(f"{rel}: requires card_sets (inline list, quoted names)")
    if len(cards) < 2:
        errors.append(f"{rel}: requires at least 2 cards (has {len(cards)})")
    if len(cards) not in ALLOWED_COUNTS:
        errors.append(f"{rel}: card count must be 2, 4, 6, or 8 (has {len(cards)})")

    for item in sets:
        if not is_quoted(item):
            errors.append(f"{rel}: card_sets entry must be double-quoted: {item}")

    if re.search(r"^card_sets:\s*$", block, re.M):
        errors.append(f"{rel}: card_sets must use inline [...] format like categories/tags")

    for front, back, _ in cards:
        if not is_quoted(front):
            errors.append(f"{rel}: card front must be double-quoted: {front[:60]}")
        if not is_quoted(back):
            errors.append(f"{rel}: card back must be double-quoted: {back[:60]}")
        front_text = front[1:-1] if is_quoted(front) else front
        back_text = back[1:-1] if is_quoted(back) else back
        if len(front_text) <= len(back_text):
            errors.append(
                f"{rel}: card front must be longer than back "
                f"(front={len(front_text)}, back={len(back_text)}): {front_text[:40]}…"
            )
        if is_multiple_choice_front(front_text):
            errors.append(
                f"{rel}: card front must be cue-only, not multiple choice "
                f"(drop option lists like 'A or B?'): {front_text[:60]}…"
            )

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
