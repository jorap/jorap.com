#!/usr/bin/env python3
"""Add typed relationship lines (extends/contradicts/…) to note bodies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {"_index.md"}

# slug -> relationship parts (wikilink titles)
RELATIONSHIPS: dict[str, dict[str, str | list[str]]] = {
    "active-knowledge-curation": {
        "extends": "Building a Second Brain",
        "contradicts": "The Collector's Fallacy",
    },
    "analog-capture-tools": {
        "extends": "Capture",
        "contradicts": "Digital Minimalism",
        "alternative": "Mobile Capture Workflows",
    },
    "anti-fragile-systems": {
        "extends": "Future-Proofing Knowledge",
        "contradicts": "Building a Personal API",
    },
    "associative-linking": {
        "extends": "Atomic Notes",
        "contradicts": "PARA Method",
    },
    "atomic-notes": {
        "extends": "PKM",
        "contradicts": "Maps of Content",
    },
    "building-a-personal-api": {
        "extends": "Metadata Strategy",
        "contradicts": "Digital Minimalism",
    },
    "building-a-second-brain": {
        "extends": "PKM",
        "contradicts": "The Collector's Fallacy",
    },
    "capture": {
        "extends": "PKM",
        "contradicts": "Signal vs Noise",
    },
    "cards": {
        "implements": "Spaced Repetition",
        "extends": "Getting Started",
    },
    "compounding": {
        "extends": "Process Over Outcomes",
        "contradicts": "Pareto Principle",
    },
    "context-aware-capture": {
        "extends": "Capture",
        "contradicts": "Metadata Strategy",
    },
    "creative-blocks": {
        "extends": "Creative Output",
        "contradicts": "Capture",
    },
    "creative-output": {
        "extends": "Building a Second Brain",
        "contradicts": "The Collector's Fallacy",
    },
    "daily-notes": {
        "extends": "Capture",
        "contradicts": "Evergreen Notes",
    },
    "digital-garden": {
        "extends": "Evergreen Notes",
        "contradicts": "The Garage Concept",
    },
    "digital-minimalism": {
        "extends": "Minimum Effective Dose",
        "contradicts": "Digital Serendipity",
    },
    "digital-serendipity": {
        "extends": "Associative Linking",
        "contradicts": "Digital Minimalism",
    },
    "drafting-in-public": {
        "extends": "Digital Garden",
        "contradicts": "Evergreen Notes",
    },
    "evergreen-notes": {
        "extends": "Atomic Notes",
        "contradicts": "Daily Notes",
    },
    "evergreen-vs-fleeting-notes": {
        "extends": "The Knowledge Lifecycle",
        "contradicts": "Evergreen Notes",
    },
    "first-principles-thinking": {
        "extends": "Synthesis as a Goal",
        "contradicts": "Eternal Principles",
    },
    "future-proofing-knowledge": {
        "extends": "Local-first Software",
        "contradicts": "Building a Personal API",
    },
    "getting-started": {
        "extends": "Note Relationships",
        "index": "this site",
    },
    "graph": {
        "implements": "Graph View Analytics",
        "extends": "Getting Started",
    },
    "graph-view-analytics": {
        "extends": "Associative Linking",
        "contradicts": "Maps of Content",
    },
    "gtd-vs-para": {
        "extends": "PARA Method",
        "contradicts": "PKM",
    },
    "intellectual-sourcing": {
        "extends": "Synthesis as a Goal",
        "contradicts": "Progressive Summarization",
    },
    "local-first-software": {
        "extends": "PKM",
        "contradicts": "Drafting in Public",
    },
    "low-hanging-fruit": {
        "extends": "Pareto Principle",
        "contradicts": "Compounding",
    },
    "maps-of-content": {
        "extends": "Active Knowledge Curation",
        "contradicts": "Atomic Notes",
        "index": "the garden",
    },
    "mental-models-list": {
        "extends": "PKM",
        "contradicts": "There Is No Perfect Solution",
    },
    "metadata-strategy": {
        "extends": "PARA Method",
        "contradicts": "Building a Personal API",
    },
    "mind-mapping": {
        "extends": "Creative Output",
        "contradicts": "Atomic Notes",
    },
    "minimum-effective-dose": {
        "extends": "Pareto Principle",
        "contradicts": "Compounding",
    },
    "minimum-viable-product": {
        "extends": "Creative Output",
        "contradicts": "Evergreen Notes",
    },
    "mobile-capture-workflows": {
        "extends": "Capture",
        "contradicts": "Analog Capture Tools",
        "alternative": "Analog Capture Tools",
    },
    "note-relationships": {
        "extends": "Associative Linking",
        "contradicts": "PARA Method",
    },
    "para-method": {
        "extends": "Building a Second Brain",
        "contradicts": "Associative Linking",
    },
    "pareto-principle": {
        "extends": "Signal vs Noise",
        "contradicts": "Compounding",
    },
    "periodic-knowledge-review": {
        "extends": "Active Knowledge Curation",
        "contradicts": "Minimum Effective Dose",
    },
    "pkm": {
        "extends": "Getting Started",
        "contradicts": "The Collector's Fallacy",
    },
    "process-over-outcomes": {
        "extends": "Compounding",
        "contradicts": "The 12 Week Year",
    },
    "progressive-summarization": {
        "extends": "Building a Second Brain",
        "contradicts": "Synthesis as a Goal",
    },
    "random-duo": {
        "implements": "Digital Serendipity",
        "extends": "Getting Started",
    },
    "random-trio": {
        "implements": "Digital Serendipity",
        "extends": "Getting Started",
    },
    "review": {
        "implements": "Spaced Repetition",
        "extends": "Getting Started",
    },
    "rss-for-research": {
        "extends": "Capture",
        "contradicts": "Signal vs Noise",
    },
    "signal-vs-noise": {
        "extends": "Capture",
        "contradicts": "RSS for Research",
    },
    "slow-productivity": {
        "extends": "Creative Output",
        "contradicts": "The 12 Week Year",
    },
    "spaced-repetition": {
        "extends": "Evergreen Notes",
        "contradicts": "Progressive Summarization",
    },
    "sunk-cost-fallacy": {
        "extends": "There Is No Perfect Solution",
        "contradicts": "Forgiveness",
    },
    "synthesis-as-a-goal": {
        "extends": "Creative Output",
        "contradicts": "Progressive Summarization",
    },
    "the-12-week-year": {
        "extends": "Periodic Knowledge Review",
        "contradicts": "Slow Productivity",
    },
    "the-collectors-fallacy": {
        "extends": "Creative Output",
        "contradicts": "Capture",
    },
    "the-feynman-technique": {
        "extends": "Evergreen Notes",
        "contradicts": "Spaced Repetition",
    },
    "the-garage-concept": {
        "extends": "Digital Garden",
        "contradicts": "Drafting in Public",
    },
    "the-knowledge-lifecycle": {
        "extends": "Evergreen vs Fleeting Notes",
        "contradicts": "Evergreen Notes",
    },
    "the-second-brain-workflow": {
        "implements": "Building a Second Brain",
        "extends": "Capture",
        "contradicts": "Minimum Effective Dose",
    },
    "the-trusted-inbox": {
        "extends": "Capture",
        "contradicts": "Mobile Capture Workflows",
    },
    "there-is-no-perfect-solution": {
        "extends": "Mental Models List",
        "contradicts": "Pareto Principle",
    },
    "visual-thinking": {
        "extends": "Mind Mapping",
        "contradicts": "Atomic Notes",
    },
    "weekly-review-checklists": {
        "implements": "Periodic Knowledge Review",
        "extends": "The Trusted Inbox",
        "contradicts": "Minimum Effective Dose",
    },
    "eternal-principles": {
        "extends": "Free Grace",
        "contradicts": "First Principles Thinking",
        "index": "gospel notes in this garden",
    },
    "free-grace": {
        "extends": "Minimum Effective Dose",
        "contradicts": "Compounding",
    },
    "love-god": {
        "extends": "Free Grace",
        "contradicts": "Don't Worry",
    },
    "love-your-neighbor": {
        "extends": "Free Grace",
        "contradicts": "Love Your Enemies",
    },
    "the-golden-rule": {
        "extends": "Free Grace",
        "contradicts": "Love Your Enemies",
    },
    "love-your-enemies": {
        "extends": "Free Grace",
        "contradicts": "The Golden Rule",
    },
    "forgiveness": {
        "extends": "Free Grace",
        "contradicts": "Sunk Cost Fallacy",
    },
    "seek-the-kingdom-first": {
        "extends": "Free Grace",
        "contradicts": "Signal vs Noise",
    },
    "dont-worry": {
        "extends": "Free Grace",
        "contradicts": "The 12 Week Year",
    },
    "the-beatitudes": {
        "extends": "Free Grace",
        "contradicts": "Humility and Service",
    },
    "peacemakers": {
        "extends": "Free Grace",
        "contradicts": "Love Your Enemies",
    },
    "reconciliation-before-worship": {
        "extends": "Free Grace",
        "contradicts": "Love God",
    },
    "humility-and-service": {
        "extends": "Free Grace",
        "contradicts": "Let Your Light Shine",
    },
    "let-your-light-shine": {
        "extends": "Free Grace",
        "contradicts": "The Garage Concept",
    },
    "treasure-in-heaven": {
        "extends": "Free Grace",
        "contradicts": "The Collector's Fallacy",
    },
    "eternal-rewards": {
        "extends": "Free Grace",
        "contradicts": "Compounding",
    },
    "the-narrow-way": {
        "extends": "Free Grace",
        "contradicts": "The Golden Rule",
    },
    "repent-and-believe": {
        "extends": "Free Grace",
        "contradicts": "Compounding",
    },
    "turn-the-other-cheek": {
        "extends": "Love Your Enemies",
        "contradicts": "The Golden Rule",
    },
    "judge-not": {
        "extends": "Free Grace",
        "contradicts": "Humility and Service",
    },
    "ask-seek-knock": {
        "extends": "Free Grace",
        "contradicts": "Don't Worry",
    },
    "let-your-yes-be-yes": {
        "extends": "Love Your Neighbor",
        "contradicts": "Drafting in Public",
    },
    "take-up-your-cross": {
        "extends": "Free Grace",
        "contradicts": "There Is No Perfect Solution",
    },
    "childlike-faith": {
        "extends": "Free Grace",
        "contradicts": "Compounding",
    },
    "the-wise-builder": {
        "extends": "Free Grace",
        "contradicts": "The Narrow Way",
    },
    "heart-righteousness": {
        "extends": "Judge Not",
        "contradicts": "Let Your Light Shine",
    },
    "secret-devotion": {
        "extends": "Ask Seek Knock",
        "contradicts": "Drafting in Public",
    },
    "by-their-fruits": {
        "extends": "Judge Not",
        "contradicts": "Signal vs Noise",
    },
    "render-unto-caesar": {
        "extends": "Seek the Kingdom First",
        "contradicts": "Treasure in Heaven",
    },
    "great-commission": {
        "extends": "Repent and Believe",
        "contradicts": "The Collector's Fallacy",
    },
    "abide-in-me": {
        "extends": "Free Grace",
        "contradicts": "Compounding",
    },
}

PAIRS_RE = re.compile(
    r"(?<=\.)?\s*(?:Also\s+)?Pairs with \[\[[^\]]+\]\](?: and \[\[[^\]]+\]\])?(?:\.\s*Also pairs with \[\[[^\]]+\]\])?\.\s*",
    re.I,
)
OLD_REL_RE = re.compile(
    r"\s*Extends \[\[[^\]]+\]\]\.\s*Contradicts \[\[[^\]]+\]\]\."
    r"(?:\s*Implements \[\[[^\]]+\]\]\.)?"
    r"(?:\s*Alternative to \[\[[^\]]+\]\]\.)?"
    r"(?:\s*Index for [^.]+\.)?\s*",
    re.I,
)


def link(title: str) -> str:
    return f"[[{title}]]"


def format_relations(spec: dict[str, str | list[str]]) -> str:
    parts: list[str] = []
    if spec.get("extends"):
        parts.append(f"Extends {link(str(spec['extends']))}.")
    if spec.get("contradicts"):
        parts.append(f"Contradicts {link(str(spec['contradicts']))}.")
    if spec.get("implements"):
        parts.append(f"Implements {link(str(spec['implements']))}.")
    if spec.get("alternative"):
        parts.append(f"Alternative to {link(str(spec['alternative']))}.")
    if spec.get("index"):
        parts.append(f"Index for {spec['index']}.")
    return " ".join(parts)


def normalize_see_also_spacing(body: str) -> str:
    return re.sub(r"(\[\[[^\]]+\]\]\.)\n## See also", r"\1\n\n## See also", body)


def apply_body(body: str, slug: str) -> tuple[str, bool]:
    if slug not in RELATIONSHIPS:
        return body, False

    relation_line = format_relations(RELATIONSHIPS[slug])
    cleaned = PAIRS_RE.sub(" ", body)
    cleaned = OLD_REL_RE.sub(" ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    if relation_line in cleaned:
        result = normalize_see_also_spacing(cleaned.strip() + "\n")
        return result, result != body

    if "## See also" in cleaned:
        head, tail = cleaned.split("## See also", 1)
        head = head.rstrip() + "\n\n" + relation_line + "\n\n"
        new_body = head + "## See also" + tail
    else:
        new_body = cleaned.rstrip() + "\n\n" + relation_line + "\n"

    new_body = new_body.strip() + "\n"
    new_body = normalize_see_also_spacing(new_body)
    return new_body, True


def main() -> None:
    updated = 0
    missing = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.name in SKIP:
            continue
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        fm, body = text[: end + 4], text[end + 4 :].lstrip("\n")

        if slug in RELATIONSHIPS:
            new_body, changed = apply_body(body, slug)
        else:
            new_body, changed = body, False
            missing.append(slug)

        spaced = normalize_see_also_spacing(new_body)
        if spaced != new_body:
            new_body = spaced
            changed = True

        if changed:
            path.write_text(fm + "\n" + new_body, encoding="utf-8")
            updated += 1
            print(f"  updated {path.name}")

    print(f"\nDone: {updated} notes updated.")
    if missing:
        print(f"Missing mappings ({len(missing)}): {', '.join(missing)}")


if __name__ == "__main__":
    main()
