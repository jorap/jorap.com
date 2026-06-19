#!/usr/bin/env python3
"""Apply reviewed tag additions across blog posts and notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "english"

# slug -> tags to add (only additions; existing tags preserved)
BLOG_ADDITIONS: dict[str, list[str]] = {
    "how-i-built-jorap-notes": ["Publishing", "Digital Garden", "PKM"],
    "hugoplate-theme-review": ["Publishing", "Digital Garden", "PKM"],
    "consistent-ai-output-wordpress-builds": ["Writing", "Documentation", "PKM"],
    "getting-started-with-rss-feeds-beginners-guide": ["PKM", "Research"],
    "top-reasons-create-maintain-your-own-website": ["Publishing", "Digital Garden"],
    "top-reasons-why-you-still-need-use-desktop-laptop": ["Note Taking"],
    "facebooks-hidden-gem-how-favorites-feed-transforms-your-social-media-experience": ["PKM"],
    # draft / prepublish PKM & Hugo cluster
    "__obsidian-vs-hugo": ["Digital Garden", "Note Taking"],
    "__markdown-formatting": ["PKM", "Readability"],
    "__markdown-deep-dive": ["Note Taking", "Documentation"],
    "__sustainable-online-publishing": ["Digital Garden", "PKM", "Blogging"],
    "__native-hugo-taxonomies": ["PKM", "Note Taking"],
    "__password-managers": ["PKM", "Note Taking"],
    "__remote-work-checklist": ["Checklist", "PKM"],
    "__how-to-create-a-good-habit": ["PKM", "Note Taking"],
    "__hugo-static-site-generator": ["PKM", "Publishing", "Digital Garden"],
    "__hugo-page-bundles": ["PKM", "Static Site Generator"],
    "__hugo-shortcodes-deep-dive": ["PKM", "Documentation"],
    "__hugo-go-templates": ["PKM", "Documentation"],
    "__make-ai-articles-more-human": ["PKM", "Note Taking"],
    "__craft-prompt-framework": ["PKM", "Note Taking"],
    "__jobs-to-be-done-framework": ["PKM", "Productivity"],
    "__smart-plug": ["PKM"],
    "__personal-immune-booster-supplements": ["Wellness"],
}

NOTE_ADDITIONS: dict[str, list[str]] = {
    "getting-started": ["PKM", "Digital Garden", "Note Taking", "Hugo", "Website Building"],
    "graph": ["PKM", "Note Taking", "Digital Garden"],
    "process-over-outcomes": ["PKM", "Note Taking"],
    "spaced-repetition-systems": ["PKM", "Note Taking"],
    "there-is-no-perfect-solution": ["PKM", "Note Taking"],
    "digital-garden": ["Hugo", "Static Site Generator", "Website Building"],
    "drafting-in-public": ["Hugo", "Website Building"],
    "maps-of-content": ["Hugo", "Website Building"],
    "the-garage-concept": ["Hugo", "Static Site Generator", "Website Building"],
    "building-a-personal-api": ["Static Site Generator", "Automation", "Documentation"],
    "advantages-of-digital-gardens": ["Website Building", "Blogging", "Hugo"],
    "future-proofing-knowledge": ["Markdown", "Documentation", "Hugo"],
    "local-first-software": ["Security"],
    "privacy-and-data-sovereignty": ["Security"],
    "e2ee-security": ["Privacy"],
    "newsletter-filtering": ["RSS", "Information Diet"],
    "digital-minimalism": ["Mindful Tech", "Information Diet"],
    "the-second-brain-workflow": ["Hugo", "Tools"],
    "note-taking-for-researchers": ["Research", "Note Taking"],
    "weekly-review-checklists": ["Workflow", "Habits"],
    "rss-for-research": ["Digital Minimalism"],
    "metadata-strategy": ["Hugo", "Documentation"],
    "formatting-for-readability": ["Documentation"],
    "distraction-free-writing": ["Writing", "Productivity"],
    "progressive-summarization": ["Research", "Writing"],
    "intellectual-sourcing": ["Research", "Writing"],
    "collaborative-knowledge": ["Workflow"],
    "anti-fragile-systems": ["Mindset", "Productivity"],
    "digital-serendipity": ["Research", "Browser Tips"],
    "serendipitous-resurfacing": ["Research", "Workflow"],
    "context-aware-capture": ["Workflow", "Capture"],
    "mobile-capture-workflows": ["Workflow", "Capture"],
    "analog-capture-tools": ["Capture"],
    "bullet-journaling": ["Habits", "Planning"],
    "mind-mapping": ["Visual Thinking"],
    "graph-view-analytics": ["Graph", "Meta"],
}


def parse_tags(fm: str) -> tuple[str | None, list[str], str]:
    """Return (match_text, tags, format) where format is inline or yaml."""
    inline = re.search(r"^tags:\s*\[(.*?)\]\s*$", fm, re.M)
    if inline:
        tags = re.findall(r'"([^"]*)"', inline.group(1))
        return inline.group(0), tags, "inline"

    yaml = re.search(r"^tags:\s*\n((?:\s+-\s+.+\n?)+)", fm, re.M)
    if yaml:
        block = yaml.group(0)
        tags = [
            m.group(1).strip().strip('"').strip("'")
            for m in re.finditer(r"^\s+-\s+(.+)\s*$", block, re.M)
        ]
        return block, tags, "yaml"

    return None, [], "missing"


def render_tags(tags: list[str], fmt: str) -> str:
    if fmt == "yaml":
        lines = ["tags:"] + [f"  - {t}" for t in tags]
        return "\n".join(lines)
    quoted = ", ".join(f'"{t}"' for t in tags)
    return f"tags: [{quoted}]"


def add_tags(path: Path, additions: list[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False

    end = text.find("\n---", 3)
    if end == -1:
        return False

    fm = text[3:end]
    body = text[end:]
    match_text, tags, fmt = parse_tags(fm)
    if fmt == "missing":
        fmt = "inline"
        tags = []

    existing = set(tags)
    new_tags = [t for t in additions if t not in existing]
    if not new_tags:
        return False

    merged = tags + new_tags
    new_block = render_tags(merged, fmt)

    if match_text:
        fm = fm.replace(match_text, new_block, 1)
    else:
        fm = fm.rstrip() + "\n" + new_block

    path.write_text(f"---{fm}{body}", encoding="utf-8")
    return True


def fix_instant_pot(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text
    if "slug: ''" in updated:
        updated = updated.replace("slug: ''", 'slug: "instant-pot-chicken-adobo"', 1)
    if "meta_title: ''" in updated:
        updated = updated.replace(
            "meta_title: ''",
            'meta_title: "Instant Pot Chicken Adobo - Filipino Comfort Food"',
            1,
        )
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    changed: list[str] = []

    blog_dir = CONTENT / "blog"
    for slug, additions in BLOG_ADDITIONS.items():
        name = slug if slug.startswith("__") else slug
        path = blog_dir / f"{name}.md"
        if not path.exists():
            print(f"skip missing blog: {path.name}", file=sys.stderr)
            continue
        if add_tags(path, additions):
            changed.append(f"blog/{path.name}: +{additions}")

    notes_dir = CONTENT / "notes"
    for slug, additions in NOTE_ADDITIONS.items():
        path = notes_dir / f"{slug}.md"
        if not path.exists():
            print(f"skip missing note: {path.name}", file=sys.stderr)
            continue
        if add_tags(path, additions):
            changed.append(f"notes/{path.name}: +{additions}")

    adobo = blog_dir / "instant-pot-chicken-adobo.md"
    if adobo.exists() and fix_instant_pot(adobo):
        changed.append("blog/instant-pot-chicken-adobo.md: fixed slug/meta_title")

    print(f"Updated {len(changed)} files:\n")
    for line in changed:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
