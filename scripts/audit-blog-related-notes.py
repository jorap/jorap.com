#!/usr/bin/env python3
"""Audit blog → garden note connections (tags, mentions, manual related_notes)."""

from __future__ import annotations

import argparse
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
SKIP_BLOG = {"_index.md", "__blog-template.md", "__blank-blog-template.md"}
MIN_SHARED_TAGS = 2
MIN_MENTION_LEN = 6
LIMIT = 6

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
RELATED_BLOCK = re.compile(r"^related_notes:\s*\n(?:  - .+\n)*", re.MULTILINE)
HEADING = re.compile(r"^#{1,6}\s+[^\n]*\n?", re.MULTILINE)
FENCE = re.compile(r"```[\s\S]*?```")
INLINE_CODE = re.compile(r"`[^`\n]+`")
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")


def load_md(path: Path) -> tuple[dict, str, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end() :], text


def note_pool() -> list[tuple[Path, dict]]:
    pages = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        meta, _, _ = load_md(path)
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


def find_related_slugs(meta: dict, body: str, notes: list[tuple[Path, dict]]) -> tuple[str, list[str], list[str]]:
    manual = meta.get("related_notes")
    if manual is not None:
        return "manual", list(manual), []
    tags = tag_matches(labels(meta), notes)
    tag_slugs = [t[0] for t in tags]
    mentions = title_mentions(body, notes, set(tag_slugs))
    if tag_slugs or mentions:
        return "auto", tag_slugs, mentions
    return "none", [], []


def combined_slugs(tag_slugs: list[str], mentions: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for slug in tag_slugs + mentions:
        if slug not in seen:
            seen.add(slug)
            out.append(slug)
    return out[:LIMIT]


def apply_related_notes(path: Path, slugs: list[str], *, force: bool) -> bool:
    _, _, text = load_md(path)
    if not slugs:
        return False
    if "related_notes:" in text.split("---", 2)[1] and not force:
        return False
    block = "related_notes:\n" + "".join(f"  - {s}\n" for s in slugs)
    if RELATED_BLOCK.search(text):
        new_text = RELATED_BLOCK.sub(block, text, count=1)
    else:
        new_text, n = re.subn(r"^(featured:)", block + r"\1", text, count=1, flags=re.MULTILINE)
        if n == 0:
            new_text, n = re.subn(r"^(draft:)", block + r"\1", text, count=1, flags=re.MULTILINE)
        if n == 0:
            return False
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def audit_rows(*, drafts_only: bool) -> list[tuple[str, str, list[str], list[str], Path]]:
    notes = note_pool()
    rows: list[tuple[str, str, list[str], list[str], Path]] = []
    for path in sorted(BLOG_DIR.glob("*.md")):
        if path.name in SKIP_BLOG:
            continue
        meta, body, _ = load_md(path)
        is_draft = bool(meta.get("draft"))
        if drafts_only and not is_draft:
            continue
        if not drafts_only and is_draft:
            continue
        slug = meta.get("slug") or path.stem
        mode, tag_hits, rest = find_related_slugs(meta, body, notes)
        if mode == "manual":
            rows.append((slug, mode, tag_hits, [], path))
        elif mode == "auto":
            rows.append((slug, mode, tag_hits, rest, path))
        else:
            rows.append((slug, mode, [], [], path))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drafts", action="store_true", help="audit draft posts only")
    parser.add_argument("--write", action="store_true", help="write related_notes frontmatter (drafts + auto matches)")
    parser.add_argument("--force", action="store_true", help="overwrite existing related_notes")
    args = parser.parse_args()

    rows = audit_rows(drafts_only=args.drafts)
    label = "draft" if args.drafts else "published"
    print(f"{'BLOG SLUG':<52} {'MODE':<6} NOTES")
    print("-" * 100)
    for slug, mode, tag_hits, mentions, _path in rows:
        parts = []
        if mode == "manual":
            parts.append("→ " + ", ".join(tag_hits) if tag_hits else "(empty manual list)")
        elif mode == "auto":
            combined = combined_slugs(tag_hits, mentions)
            if tag_hits:
                parts.append("tags: " + ", ".join(tag_hits))
            if mentions:
                parts.append("mentions: " + ", ".join(mentions))
            if not tag_hits and not mentions:
                parts.append("→ " + ", ".join(combined))
        else:
            parts.append("—")
        print(f"{slug:<52} {mode:<6} {' | '.join(parts)}")

    none = [r for r in rows if r[1] == "none"]
    print(f"\n{len(rows)} {label} blogs; {len(none)} with no garden connection.")

    if args.write:
        if not args.drafts:
            print("--write requires --drafts", file=sys.stderr)
            return 1
        updated = 0
        for slug, mode, tag_hits, mentions, path in rows:
            if mode == "manual":
                continue
            slugs = combined_slugs(tag_hits, mentions)
            if apply_related_notes(path, slugs, force=args.force):
                updated += 1
                print(f"  wrote {slug}: {', '.join(slugs)}")
        print(f"Updated {updated} draft(s).")
        # ponytail: self-check — re-read one written file
        sample = next((p for _, m, t, n, p in rows if m == "auto" and combined_slugs(t, n)), None)
        if sample:
            meta, _, _ = load_md(sample)
            assert meta.get("related_notes"), f"write check failed: {sample.name}"
    return 0


if __name__ == "__main__":
    sys.exit(main())
