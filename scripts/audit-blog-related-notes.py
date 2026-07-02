#!/usr/bin/env python3
"""Audit blog → garden note connections (tags, mentions, manual related_notes)."""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required for audit")

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "content/english/blog"
NOTES_DIR = ROOT / "content/english/notes"
MIN_SHARED_TAGS = 2
MIN_MENTION_LEN = 6
LIMIT = 6

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
HEADING = re.compile(r"^#{1,6}\s+[^\n]*\n?", re.MULTILINE)
FENCE = re.compile(r"```[\s\S]*?```")
INLINE_CODE = re.compile(r"`[^`\n]+`")
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")


def load_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end() :]
    return meta, body


def note_pool() -> list[tuple[Path, dict]]:
    pages = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        meta, _ = load_md(path)
        if meta.get("draft"):
            continue
        kind = meta.get("note_kind", "note")
        if kind in ("meta", "index"):
            continue
        pages.append((path, meta))
    return pages


def labels(meta: dict) -> list[str]:
    tags = meta.get("tags") or []
    cats = meta.get("categories") or []
    return list(tags) + list(cats)


def tag_matches(blog_labels: list[str], notes: list[tuple[Path, dict]]) -> list[tuple[str, float, list[str]]]:
    if not blog_labels:
        return []
    scored = []
    for path, meta in notes:
        note_labels = labels(meta)
        if not note_labels:
            continue
        shared = [x for x in blog_labels if x in note_labels]
        if len(shared) < MIN_SHARED_TAGS:
            continue
        score = len(shared) / math.sqrt(len(blog_labels) * len(note_labels))
        slug = meta.get("slug") or path.stem
        scored.append((slug, score, shared))
    scored.sort(key=lambda x: (-x[1], x[0]))
    return scored[:LIMIT]


def mention_raw(body: str) -> str:
    body = FENCE.sub("", body)
    body = INLINE_CODE.sub("", body)
    body = HEADING.sub("", body)
    body = WIKILINK.sub(" ", body)
    return body


def title_mentions(body: str, notes: list[tuple[Path, dict]], skip: set[str]) -> list[str]:
    raw = mention_raw(body)
    hits = []
    for path, meta in notes:
        slug = meta.get("slug") or path.stem
        if slug in skip:
            continue
        needles = [meta.get("title", path.stem)]
        needles.extend(meta.get("aliases") or [])
        for needle in needles:
            if len(needle) < MIN_MENTION_LEN:
                continue
            words = needle.split()
            if len(words) > 1:
                if not re.search(re.escape(needle), raw, re.I):
                    continue
                pat = rf"(?i)(?:^|[^\[\w]){re.escape(needle)}(?:[^\]\w]|$)"
            else:
                pat = rf"(?i)(?:^|[^\[\wA-Z]){re.escape(needle)}(?:[^\]\w]|$)"
            if re.search(pat, raw):
                hits.append(slug)
                break
    return hits[:LIMIT]


def main() -> None:
    notes = note_pool()
    rows = []
    for path in sorted(BLOG_DIR.glob("*.md")):
        if path.name == "_index.md":
            continue
        meta, body = load_md(path)
        if meta.get("draft"):
            continue
        slug = meta.get("slug") or path.stem
        blog_labels = labels(meta)
        manual = meta.get("related_notes")
        if manual is not None:
            rows.append((slug, "manual", manual, []))
            continue
        tags = tag_matches(blog_labels, notes)
        tag_slugs = {t[0] for t in tags}
        mentions = title_mentions(body, notes, tag_slugs)
        if tags or mentions:
            rows.append((slug, "auto", [t[0] for t in tags], mentions))
        else:
            rows.append((slug, "none", [], []))

    print(f"{'BLOG SLUG':<52} {'MODE':<6} NOTES")
    print("-" * 100)
    for slug, mode, tag_hits, mentions in rows:
        parts = []
        if mode == "manual":
            parts.append("→ " + ", ".join(tag_hits) if tag_hits else "(empty manual list)")
        else:
            if tag_hits:
                parts.append("tags: " + ", ".join(tag_hits))
            if mentions:
                parts.append("mentions: " + ", ".join(mentions))
            if not parts:
                parts.append("—")
        print(f"{slug:<52} {mode:<6} {' | '.join(parts)}")

    none = [r for r in rows if r[1] == "none"]
    print(f"\n{len(rows)} published blogs; {len(none)} with no garden connection.")


if __name__ == "__main__":
    main()
