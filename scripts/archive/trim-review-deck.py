#!/usr/bin/env python3
"""Keep review flashcards on ~20% highest-impact notes (Pareto)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = ROOT / "content/english/notes"

# Spine of the garden: frameworks and daily-use distinctions (~20% of review notes).
REVIEW_KEEP = {
    "pkm",
    "capture",
    "signal-vs-noise",
    "the-trusted-inbox",
    "para-method",
    "gtd-vs-para",
    "atomic-notes",
    "evergreen-notes",
    "associative-linking",
    "progressive-summarization",
    "building-a-second-brain",
    "weekly-review-checklists",
    "the-collectors-fallacy",
    "spaced-repetition",
    "note-relationships",
    "pareto-principle",
}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def remove_field(inner: str, key: str) -> str:
    return re.sub(rf"^{re.escape(key)}:.*\n?", "", inner, flags=re.M)


def main() -> None:
    kept = 0
    dropped = 0

    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        _, inner, body = split_frontmatter(text)
        if not inner or not re.search(r"^review:\s*true\s*$", inner, re.M):
            continue

        if path.stem in REVIEW_KEEP:
            kept += 1
            continue

        new_inner = remove_field(inner, "review")
        new_inner = remove_field(new_inner, "card_front")
        new_inner = remove_field(new_inner, "card_back")
        new_inner = re.sub(r"^cards:\s*\n(?:\s+-\s+front:.*\n\s+back:.*\n?)+", "", new_inner, flags=re.M)
        new_inner = new_inner.strip() + "\n"
        path.write_text(f"---\n{new_inner}---\n\n{body}", encoding="utf-8")
        dropped += 1
        print(f"dropped review: {path.name}")

    print(f"\nDone: {kept} kept, {dropped} dropped ({kept} / {kept + dropped} in deck).")


if __name__ == "__main__":
    main()
