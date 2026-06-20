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
    "advantages-of-digital-gardens": {
        "extends": "Digital Garden",
        "contradicts": "Evergreen Notes",
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
        "contradicts": "Organization",
    },
    "atomic-design-for-notes": {
        "extends": "Atomic Notes",
        "contradicts": "Mind Mapping",
    },
    "atomic-notes": {
        "extends": "Zettelkasten",
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
    "bullet-journaling": {
        "extends": "Analog Capture Tools",
        "contradicts": "Building a Second Brain",
        "alternative": "Daily Notes",
    },
    "capture": {
        "extends": "PKM",
        "contradicts": "Signal vs Noise",
    },
    "cards": {
        "implements": "Spaced Repetition",
        "extends": "Getting Started",
    },
    "collaborative-knowledge": {
        "extends": "Building a Personal API",
        "contradicts": "Digital Garden",
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
    "curation-as-creation": {
        "extends": "Active Knowledge Curation",
        "contradicts": "Organization",
    },
    "daily-notes": {
        "extends": "Capture",
        "contradicts": "Evergreen Notes",
        "alternative": "Bullet Journaling",
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
    "distraction-free-writing": {
        "extends": "Creative Output",
        "contradicts": "Drafting in Public",
    },
    "drafting-in-public": {
        "extends": "Digital Garden",
        "contradicts": "Evergreen Notes",
    },
    "e2ee-security": {
        "extends": "Privacy and Data Sovereignty",
        "contradicts": "Digital Garden",
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
        "contradicts": "Progressive Summarization",
    },
    "formatting-for-readability": {
        "extends": "Evergreen Notes",
        "contradicts": "Atomic Notes",
    },
    "from-note-to-book": {
        "extends": "Maps of Content",
        "contradicts": "Minimum Viable Product",
    },
    "future-proofing-knowledge": {
        "extends": "Local-first Software",
        "contradicts": "The Future of PKM",
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
        "extends": "Organization",
        "contradicts": "PKM",
    },
    "intellectual-sourcing": {
        "extends": "Note-Taking for Researchers",
        "contradicts": "Progressive Summarization",
    },
    "interstitial-journaling": {
        "extends": "Daily Notes",
        "contradicts": "Slow Productivity",
    },
    "local-first-software": {
        "extends": "Privacy and Data Sovereignty",
        "contradicts": "Collaborative Knowledge",
    },
    "low-hanging-fruit": {
        "extends": "Pareto Principle",
        "contradicts": "Compounding",
    },
    "maps-of-content": {
        "extends": "Curation as Creation",
        "contradicts": "Atomic Notes",
        "index": "the garden",
    },
    "mental-models-list": {
        "extends": "PKM",
        "contradicts": "There Is No Perfect Solution",
    },
    "metadata-strategy": {
        "extends": "Organization",
        "contradicts": "Building a Personal API",
    },
    "mind-mapping": {
        "extends": "Visual Thinking",
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
    "newsletter-filtering": {
        "extends": "RSS for Research",
        "contradicts": "Signal vs Noise",
    },
    "note-relationships": {
        "extends": "Associative Linking",
        "contradicts": "Organization",
    },
    "note-taking-for-researchers": {
        "extends": "Synthesis as a Goal",
        "contradicts": "Progressive Summarization",
    },
    "organization": {
        "extends": "PARA Method",
        "contradicts": "Associative Linking",
    },
    "para-method": {
        "extends": "Building a Second Brain",
        "contradicts": "Zettelkasten",
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
    "privacy-and-data-sovereignty": {
        "extends": "Local-first Software",
        "contradicts": "Drafting in Public",
    },
    "process-over-outcomes": {
        "extends": "Compounding",
        "contradicts": "The 12 Week Year",
    },
    "progressive-summarization": {
        "extends": "Building a Second Brain",
        "contradicts": "Synthesis as a Goal",
    },
    "random-two": {
        "implements": "Digital Serendipity",
        "extends": "Getting Started",
    },
    "random-three": {
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
    "second-brain-daily-workflow": {
        "implements": "The Second Brain Workflow",
        "extends": "Capture",
        "contradicts": "Slow Productivity",
    },
    "serendipitous-resurfacing": {
        "extends": "Digital Serendipity",
        "contradicts": "Spaced Repetition",
    },
    "signal-vs-noise": {
        "extends": "Capture",
        "contradicts": "RSS for Research",
    },
    "slip-box-history": {
        "extends": "Zettelkasten",
        "contradicts": "The Zettelkasten Myth",
    },
    "slow-productivity": {
        "extends": "Creative Output",
        "contradicts": "The 12 Week Year",
    },
    "spaced-repetition": {
        "extends": "Evergreen Notes",
        "contradicts": "Progressive Summarization",
    },
    "spaced-repetition-systems": {
        "extends": "Spaced Repetition",
        "contradicts": "Progressive Summarization",
    },
    "sunk-cost-fallacy": {
        "extends": "There Is No Perfect Solution",
        "contradicts": "Compounding",
    },
    "synthesis-as-a-goal": {
        "extends": "Creative Output",
        "contradicts": "Progressive Summarization",
    },
    "the-12-week-year": {
        "extends": "Periodic Knowledge Review",
        "contradicts": "Slow Productivity",
    },
    "the-archive-method": {
        "extends": "PARA Method",
        "contradicts": "Evergreen Notes",
    },
    "the-collectors-fallacy": {
        "extends": "Creative Output",
        "contradicts": "Capture",
    },
    "the-feynman-technique": {
        "extends": "Evergreen Notes",
        "contradicts": "Spaced Repetition",
    },
    "the-future-of-pkm": {
        "extends": "Building a Personal API",
        "contradicts": "Local-first Software",
    },
    "the-garage-concept": {
        "extends": "Digital Garden",
        "contradicts": "Drafting in Public",
    },
    "the-knowledge-lifecycle": {
        "extends": "Evergreen vs Fleeting Notes",
        "contradicts": "Evergreen Notes",
    },
    "the-power-of-interconnectivity": {
        "extends": "Associative Linking",
        "contradicts": "Atomic Notes",
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
    "the-zettelkasten-myth": {
        "extends": "Slip-box History",
        "contradicts": "Zettelkasten",
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
    "zettelkasten": {
        "extends": "Atomic Notes",
        "contradicts": "PARA Method",
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
