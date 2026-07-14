#!/usr/bin/env python3
"""One-shot blog slug/filename alignment. Run with --write to apply."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from blog_frontmatter import canonical_blog_fm, dump_blog_frontmatter

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "content" / "english" / "blog"
CONTENT = ROOT / "content"

# old_stem -> (new_stem, extra_aliases)
# Stems are without __ draft prefix.
RENAMES: dict[str, tuple[str, list[str]]] = {
    # published: shorten SEO-bait slugs; alias old paths
    "facebooks-hidden-gem-how-favorites-feed-transforms-your-social-media-experience": (
        "facebook-favorites-feed",
        [],
    ),
    "getting-started-with-rss-feeds-beginners-guide": ("getting-started-with-rss-feeds", []),
    "power-of-worship-pads-enhancing-your-worship-experience": ("worship-pads-solo-guitar", []),
    "top-reasons-why-you-still-need-use-desktop-laptop": ("why-keep-desktop-laptop", []),
    "top-reasons-create-maintain-your-own-website": ("why-run-your-own-website", []),
    "power-of-the-mouse-wheel-click": ("mouse-wheel-click", []),
    # drafts: shorter filenames matching intent
    "blank-blog-template": ("how-to-create-a-blog-template", []),
    "stuart-mcgill-big-three-low-back-exercises": ("mcgill-big-three", []),
    "personal-immune-booster-supplements": ("immune-booster-supplements", []),
    "worcestershire-sauce-lee-and-perrins": ("worcestershire-sauce", []),
    "hugo-shortcodes-deep-dive": ("hugo-shortcodes", []),
    "make-ai-articles-more-human": ("humanize-ai-articles", []),
}

LINK_RE = re.compile(r"(/blog/)([a-z0-9-]+)(/?)")


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        raise ValueError("missing frontmatter")
    return yaml.safe_load(match.group(1)) or {}, text[match.end() :]


def stem_of(path: Path) -> str:
    return path.stem[2:] if path.stem.startswith("__") else path.stem


def draft_prefix(path: Path) -> str:
    return "__" if path.name.startswith("__") else ""


def update_frontmatter(path: Path, new_stem: str, extra_aliases: list[str], write: bool) -> None:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    old_slug = str(fm.get("slug") or stem_of(path))
    aliases = list(fm.get("aliases") or [])
    for alias in [old_slug, *extra_aliases]:
        if alias and alias != new_stem and alias not in aliases:
            aliases.append(alias)
    fm["slug"] = new_stem
    if aliases:
        fm["aliases"] = aliases
    elif "aliases" in fm:
        del fm["aliases"]
    canon = canonical_blog_fm(fm, path)
    new_text = f"---\n{dump_blog_frontmatter(canon)}\n---\n\n{body.lstrip(chr(10))}"
    if write:
        path.write_text(new_text, encoding="utf-8")


def update_links(write: bool) -> int:
    slug_map = {old: new for old, (new, _) in RENAMES.items()}
    changed = 0
    for path in CONTENT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        new_text = LINK_RE.sub(
            lambda m: f"{m.group(1)}{slug_map.get(m.group(2), m.group(2))}{m.group(3)}",
            text,
        )
        if new_text != text:
            changed += 1
            if write:
                path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> int:
    write = "--write" in sys.argv
    missing: list[str] = []

    for old_stem, (new_stem, extra_aliases) in RENAMES.items():
        candidates = [BLOG / f"{old_stem}.md", BLOG / f"__{old_stem}.md"]
        src = next((p for p in candidates if p.exists()), None)
        if not src:
            missing.append(old_stem)
            continue
        prefix = draft_prefix(src)
        dst = BLOG / f"{prefix}{new_stem}.md"
        if dst.exists() and dst != src:
            print(f"collision: {dst}", file=sys.stderr)
            return 1
        update_frontmatter(src, new_stem, extra_aliases, write=write)
        if write and src != dst:
            src.rename(dst)
        print(f"{'renamed' if write else 'would rename'}: {src.name} -> {dst.name}")

    if missing:
        print("missing:", ", ".join(missing), file=sys.stderr)

    link_files = update_links(write=write)
    print(f"{'updated' if write else 'would update'} internal links in {link_files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
