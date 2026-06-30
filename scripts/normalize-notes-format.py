#!/usr/bin/env python3
"""One-shot: normalize note formatting and strip card-echo duplicate examples."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}

CARD_ITEM_RE = re.compile(
    r'^\s+-\s+front:\s+"((?:[^"\\]|\\.)*)"\s*\n\s+back:\s+"((?:[^"\\]|\\.)*)"\s*$',
    re.M,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    fm = text[3:end].lstrip("\n")
    return fm, text[end + 4 :]


def parse_cards(fm: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in CARD_ITEM_RE.finditer(fm)]


def norm(s: str) -> str:
    s = re.sub(r"\[\[([^\]]+)\]\]", r"LINK", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def is_card_echo(bullet: str, cards: list[tuple[str, str]]) -> bool:
    text = bullet[2:].strip() if bullet.startswith("- ") else bullet.strip()
    ntext = norm(text)
    for front, back in cards:
        nfront, nback = norm(front), norm(back)
        combo = f"{nfront} - {nback}"
        if ntext == combo:
            return True
        # front - back pasted with minor punctuation tweaks
        if nfront in ntext and ntext.endswith(nback) and len(ntext) < len(combo) + 30:
            return True
        if ntext.startswith(nfront[: min(40, len(nfront))]) and nback in ntext:
            if len(ntext) < len(nfront) + len(nback) + 25:
                return True
    return False


def dedupe_examples(body: str, cards: list[tuple[str, str]]) -> tuple[str, int]:
    if "## Examples" not in body:
        return body, 0
    before, rest = body.split("## Examples", 1)
    examples_block, after = rest.split("##", 1)
    after = "##" + after if after else ""

    lines = examples_block.splitlines()
    kept: list[str] = []
    seen: set[str] = set()
    removed = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            key = norm(stripped)
            if key in seen:
                removed += 1
                continue
            if cards and is_card_echo(stripped, cards):
                removed += 1
                continue
            seen.add(key)
        kept.append(line)

    new_block = "\n".join(kept)
    return before + "## Examples" + new_block + after, removed


def normalize_file(path: Path, dry_run: bool = False) -> list[str]:
    changes: list[str] = []
    raw = path.read_text(encoding="utf-8")
    fixed = raw.replace("\u2014", "-").replace("\u2013", "-")

    fm, body = split_frontmatter(fixed)
    if not fm:
        if not fixed.endswith("\n"):
            fixed += "\n"
            changes.append("trailing newline")
        if fixed != raw and not dry_run:
            path.write_text(fixed, encoding="utf-8")
        return changes

    cards = parse_cards(fm)

    # No blank line inside frontmatter after opening ---
    if fm.startswith("\n"):
        fm = fm.lstrip("\n")
        changes.append("frontmatter leading blank")

    # Exactly one blank line between closing --- and body
    body = body.lstrip("\n")
    if body:
        body = "\n" + body

    new_body, removed = dedupe_examples(body, cards)
    if removed:
        changes.append(f"removed {removed} duplicate example(s)")

    out = f"---\n{fm}\n---{new_body}"
    if not out.endswith("\n"):
        out += "\n"
        changes.append("trailing newline")

    if out != raw:
        if not dry_run:
            path.write_text(out, encoding="utf-8")
        if not changes:
            changes.append("format normalized")
    return changes


def main() -> int:
    dry_run = "--check" in sys.argv
    total_changes = 0
    touched = 0

    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        changes = normalize_file(path, dry_run=dry_run)
        if changes:
            touched += 1
            total_changes += len(changes)
            print(f"{'[check] ' if dry_run else ''}{path.name}: {', '.join(changes)}")

    mode = "would update" if dry_run else "updated"
    print(f"\n{mode} {touched} files ({total_changes} fixes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
