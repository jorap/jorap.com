#!/usr/bin/env python3
"""Audit note categories against the garden taxonomy.

Categories are topical buckets for the notes index filter — not \"every note is an idea.\"
Do not use Ideas. Tips is only for procedural how-tos you can run this week.

Primary categories (one per note, Tips optional second):
  Faith       — gospel cluster (Eternal Principles card_sets; not workplace translations)
  Productivity — PKM, capture/distill/organize, garden meta and Hugo tooling
  Leadership  — workplace + pressure hubs, safety/ops, work ethics
  Thinking    — mental models, decision lenses, strategy, cognitive bias
  Growth      — habits, performance loops, personal development (Systems for Growth hub)

Tips (optional second category): concrete workflow/checklist notes from TIPS_SLUGS only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}

GOSPEL_CARD_SETS = {
    "Eternal Principles",
    "Faith",
    "Commandments",
    "Prayer",
    "Priorities",
    "Discipleship",
    "Gospel",
}

PKM_TAGS = {
    "PKM",
    "Note Taking",
    "Second Brain",
    "Capture",
    "CODE Method",
    "Digital Garden",
    "Anki",
    "Hugo",
    "Website Building",
    "Git",
    "CMS",
    "Zettelkasten",
    "Linking",
    "Organization",
    "GTD",
    "PARA",
    "Flashcards",
    "SRS",
    "Metadata",
    "Taxonomy",
    "Progressive Summarization",
    "Evergreen Notes",
    "Daily Notes",
    "Inbox",
    "Workflow",
    "Tools",
    "Static Sites",
    "Selling Static Sites",
    "Client Site",
    "DevOps",
    "MOC",
    "Maps of Content",
}

GARDEN_META = {
    "getting-started",
    "maps-of-content",
    "note-relationships",
    "flashcards",
    "graph",
    "review",
    "backlinks",
    "create",
    "issues",
    "random-duo",
    "cards",
    "okf-export",
}

LEADERSHIP_TAGS = {"Leadership", "Workplace", "Safety", "Work", "Accountability"}

THINKING_TAGS = {"Mental Models", "Strategy", "Bias"}

# Procedural how-tos only — not frameworks or principles.
TIPS_SLUGS = {
    "analog-capture-tools",
    "context-aware-capture",
    "daily-notes",
    "habit-stacking",
    "inbox-zero",
    "layered-reading",
    "mobile-capture-workflows",
    "progressive-summarization",
    "read-later-queue",
    "share-sheet",
    "sketchpad",
    "the-trusted-inbox",
    "voice-memos",
    "weekly-review-checklists",
}


def title_to_slug(title: str) -> str:
    return title.strip().lower().replace(" ", "-")


def hub_slugs(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    _, body = split_frontmatter(text)
    return {title_to_slug(m) for m in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body)}


def primary_category(
    slug: str,
    fm: dict,
    workplace: set[str],
    growth: set[str],
    pressure: set[str],
) -> str:
    tags = set(fm.get("tags") or [])
    card_sets = set(fm.get("card_sets") or [])
    kind = fm.get("note_kind", "note")

    if slug == "eternal-principles" or (
        card_sets & GOSPEL_CARD_SETS and "Workplace" not in tags
    ):
        return "Faith"

    if slug in {"workplace-principles", "pressure-reveals-weakness"}:
        return "Leadership"
    if slug in workplace | pressure:
        return "Leadership"

    if slug == "systems-for-growth" or (slug in growth and "PKM" not in tags):
        return "Growth"

    if slug == "mental-models" or tags & THINKING_TAGS:
        return "Thinking"

    if tags & LEADERSHIP_TAGS:
        return "Leadership"

    if kind == "meta" or slug in GARDEN_META:
        return "Productivity"
    if tags & PKM_TAGS:
        return "Productivity"

    return "Growth"


def expected_categories(
    slug: str,
    fm: dict,
    workplace: set[str],
    growth: set[str],
    pressure: set[str],
) -> tuple[str, ...]:
    primary = primary_category(slug, fm, workplace, growth, pressure)
    if slug in TIPS_SLUGS:
        return (primary, "Tips") if primary != "Tips" else ("Tips",)
    return (primary,)


def apply_categories(path: Path, cats: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    if not raw_fm:
        raise ValueError(f"no frontmatter: {path.name}")
    fm = yaml.safe_load(raw_fm) or {}
    fm["categories"] = list(cats)
    out = f"---\n{dump_frontmatter(fm)}\n---\n{body.lstrip()}"
    path.write_text(out, encoding="utf-8")


def _self_check() -> None:
    assert expected_categories("abide-in-me", {"card_sets": ["Eternal Principles"]}, set(), set(), set()) == (
        "Faith",
    )
    assert expected_categories("inbox-zero", {"tags": ["PKM"]}, set(), set(), set()) == (
        "Productivity",
        "Tips",
    )
    assert expected_categories("systems-thinking", {"tags": []}, set(), {"systems-thinking"}, set()) == (
        "Growth",
    )
    assert "Ideas" not in expected_categories("slow-the-moment", {"tags": ["Leadership"]}, set(), set(), {"slow-the-moment"})


def main() -> int:
    _self_check()
    write = "--write" in sys.argv
    workplace = hub_slugs(NOTES / "workplace-principles.md")
    growth = hub_slugs(NOTES / "systems-for-growth.md")
    pressure = hub_slugs(NOTES / "pressure-reveals-weakness.md")

    changes: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = []
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        raw_fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        fm = yaml.safe_load(raw_fm) or {}
        slug = fm.get("slug") or path.stem
        cur = tuple(fm.get("categories") or [])
        new = expected_categories(slug, fm, workplace, growth, pressure)
        if cur != new:
            changes.append((slug, cur, new))

    if not changes:
        print("All note categories match expected taxonomy.")
        return 0

    print(f"{'WRITE' if write else 'DRY RUN'}: {len(changes)} note(s) need category updates\n")
    for slug, cur, new in changes:
        print(f"  {slug:45s} {cur or '()'} -> {new}")

    if write:
        for path in sorted(NOTES.glob("*.md")):
            if path.name in SKIP:
                continue
            raw_fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            fm = yaml.safe_load(raw_fm) or {}
            slug = fm.get("slug") or path.stem
            cur = tuple(fm.get("categories") or [])
            new = expected_categories(slug, fm, workplace, growth, pressure)
            if cur != new:
                apply_categories(path, new)
        print(f"\nUpdated {len(changes)} file(s).")
    else:
        print("\nRe-run with --write to apply.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
