#!/usr/bin/env python3
"""Opt content notes into auto flashcards (review: true + opening definition line)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {
    "_index",
    "graph",
    "cards",
    "review",
    "random-duo",
    "random-trio",
    "getting-started",
    "maps-of-content",
}
LEAD_RE = re.compile(r"^\*\*([^*]+)\*\*\s*(?:=\s*|—\s*|-\s*)(.+)$")


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def add_review(inner: str) -> str:
    if re.search(r"^review:\s*true\s*$", inner, re.M):
        return inner
    if re.search(r"^review:", inner, re.M):
        return re.sub(r"^review:.*$", "review: true", inner, count=1, flags=re.M)
    if re.search(r"^status:", inner, re.M):
        return re.sub(r"^(status:.*)$", r"\1\nreview: true", inner, count=1, flags=re.M)
    if re.search(r"^draft:", inner, re.M):
        return re.sub(r"^(draft:.*)$", r"review: true\n\1", inner, count=1, flags=re.M)
    return inner + "\nreview: true"


def lead_line(body: str) -> str:
    return body.strip().split("\n", 1)[0].strip() if body.strip() else ""


def main() -> None:
    updated = 0
    skipped = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        fm, inner, body = split_frontmatter(text)
        if not fm:
            print(f"skip (no frontmatter): {path.name}")
            continue
        first = lead_line(body)
        if not LEAD_RE.match(first):
            print(f"skip (no lead card): {path.name}")
            continue
        new_inner = add_review(inner)
        if new_inner == inner:
            skipped += 1
            continue
        path.write_text(f"---\n{new_inner}\n---\n\n{body}", encoding="utf-8")
        updated += 1
        print(f"review: {path.name}")

    print(f"\nDone: {updated} opted in, {skipped} already had review: true.")


if __name__ == "__main__":
    main()
