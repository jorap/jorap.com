#!/usr/bin/env python3
"""Add card_front and card_back to review notes for memorable flashcard answers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

# Short recall prompt + punchy answer (no wikilinks).
CARDS: dict[str, tuple[str, str]] = {
    "active-knowledge-curation": (
        "Active curation",
        "Revisit on schedule; cut what you wouldn't save again.",
    ),
    "advantages-of-digital-gardens": (
        "Digital gardens",
        "Public, linked, imperfect - not sealed essays.",
    ),
    "analog-capture-tools": (
        "Paper capture",
        "Same trusted inbox, different medium.",
    ),
    "anti-fragile-systems": (
        "Anti-fragile notes",
        "Plain files, open formats, backups you test.",
    ),
    "associative-linking": (
        "Associative linking",
        "Folders sort, links think.",
    ),
    "atomic-design-for-notes": (
        "Atomic design for notes",
        "One idea per file, stack like Lego.",
    ),
    "atomic-notes": (
        "Atomic notes",
        "One claim out loud - too many ands, split it.",
    ),
    "building-a-personal-api": (
        "Personal API",
        "Notes tools can read without a lecture.",
    ),
    "building-a-second-brain": (
        "Second Brain",
        "Ideas outside your head so you can think.",
    ),
    "bullet-journaling": (
        "Bullet journaling",
        "Rapid paper logging when digital feels slow.",
    ),
    "capture": (
        "Capture",
        "One inbox for what resonates.",
    ),
    "collaborative-knowledge": (
        "Collaborative knowledge",
        "Shared docs, clear owners, one truth per topic.",
    ),
    "compounding": (
        "Compounding",
        "Small gains stack - flat until suddenly not.",
    ),
    "context-aware-capture": (
        "Context-aware capture",
        "Save the why, not just the link.",
    ),
    "creative-blocks": (
        "Creative block",
        "Too much inventory, not enough shipping.",
    ),
    "creative-output": (
        "Creative output",
        "Notes leaving the warehouse.",
    ),
    "curation-as-creation": (
        "Curation as creation",
        "What you include is the argument.",
    ),
    "daily-notes": (
        "Daily notes",
        "Today's scratch pad - not a diary.",
    ),
    "digital-garden": (
        "Digital garden",
        "Public notes that grow and get revised.",
    ),
    "digital-minimalism": (
        "Digital minimalism (PKM)",
        "Fewer apps, fewer sync layers.",
    ),
    "digital-serendipity": (
        "Digital serendipity",
        "Design luck so old notes resurface.",
    ),
    "distraction-free-writing": (
        "Distraction-free writing",
        "Full screen, plain text, phone away.",
    ),
    "drafting-in-public": (
        "Drafting in public",
        "Publish rough, revise in public.",
    ),
    "e2ee-security": (
        "E2EE",
        "Only you and the recipient read it - not the server.",
    ),
    "evergreen-notes": (
        "Evergreen notes",
        "Claims that stay true, updated when reality shifts.",
    ),
    "evergreen-vs-fleeting-notes": (
        "Evergreen vs fleeting",
        "Sparks vs truth - two lanes, one promotion path.",
    ),
    "first-principles-thinking": (
        "First-principles thinking",
        "Rebuild from scratch, not someone else's quote.",
    ),
    "formatting-for-readability": (
        "Readable notes",
        "Short blocks, bold on the claim.",
    ),
    "from-note-to-book": (
        "From note to book",
        "Compile from atoms, don't invent from zero.",
    ),
    "future-proofing-knowledge": (
        "Future-proofing",
        "Plain text, open tools, tested exports.",
    ),
    "graph-view-analytics": (
        "Graph analytics",
        "Orphans, hubs, missing links - not wallpaper.",
    ),
    "gtd-vs-para": (
        "GTD vs PARA",
        "GTD runs tasks; PARA runs notes.",
    ),
    "intellectual-sourcing": (
        "Intellectual sourcing",
        "Minimum citation so future-you trusts it.",
    ),
    "interstitial-journaling": (
        "Interstitial journaling",
        "30 seconds between tasks: flush the buffer.",
    ),
    "local-first-software": (
        "Local-first",
        "Your device is truth; sync is backup.",
    ),
    "low-hanging-fruit": (
        "Low hanging fruit",
        "Easy win first, hard climb later.",
    ),
    "mental-models-list": (
        "Mental models",
        "Shortcuts that survived real decisions.",
    ),
    "metadata-strategy": (
        "Metadata strategy",
        "Tags that help find notes - not a second job.",
    ),
    "mind-mapping": (
        "Mind maps",
        "Spatial first draft before linear notes.",
    ),
    "minimum-effective-dose": (
        "Minimum effective dose",
        "Smallest effort that still works.",
    ),
    "minimum-viable-product": (
        "Minimum viable product",
        "Smallest shippable version to learn.",
    ),
    "mobile-capture-workflows": (
        "Mobile capture",
        "Two taps to inbox - sparks die fast.",
    ),
    "newsletter-filtering": (
        "Newsletter filtering",
        "Batch weekly, clip what resonates.",
    ),
    "note-taking-for-researchers": (
        "Research notes",
        "Source notes with the book; yours in your words.",
    ),
    "organization": (
        "PKM organization",
        "Enough structure to find things when life is loud.",
    ),
    "para-method": (
        "PARA",
        "Projects, Areas, Resources, Archive.",
    ),
    "pareto-principle": (
        "Pareto principle",
        "Most results from a tiny slice of work.",
    ),
    "periodic-knowledge-review": (
        "Periodic review",
        "Weekly rhythm, quarterly deep pass.",
    ),
    "pkm": (
        "PKM",
        "Capture, organize, distill, express.",
    ),
    "privacy-and-data-sovereignty": (
        "Data sovereignty",
        "You choose where notes live and who reads them.",
    ),
    "process-over-outcomes": (
        "Process over outcomes",
        "Rerun the habit; outcomes follow unevenly.",
    ),
    "progressive-summarization": (
        "Progressive summarization",
        "Bold, highlight, summarize on reuse.",
    ),
    "rss-for-research": (
        "RSS for research",
        "Subscribe, batch read, clip to notes.",
    ),
    "second-brain-daily-workflow": (
        "Daily Second Brain workflow",
        "Tabs, feeds, capture in the gaps.",
    ),
    "serendipitous-resurfacing": (
        "Serendipitous resurfacing",
        "Design for rediscovery, not search-only.",
    ),
    "signal-vs-noise": (
        "Signal vs noise",
        "Save what changes action or belief this month.",
    ),
    "slip-box-history": (
        "Slip-box history",
        "Cards and links - method, not magic stationery.",
    ),
    "slow-productivity": (
        "Slow productivity",
        "Fewer projects, more finished work.",
    ),
    "spaced-repetition": (
        "Spaced repetition",
        "Review facts on a schedule, not whole essays.",
    ),
    "spaced-repetition-systems": (
        "SRS apps",
        "Algorithm schedules; you supply cards.",
    ),
    "sunk-cost-fallacy": (
        "Sunk cost fallacy",
        "Past effort doesn't justify future spending.",
    ),
    "synthesis-as-a-goal": (
        "Synthesis",
        "Your words, your claim - not quote collage.",
    ),
    "the-12-week-year": (
        "12-week year",
        "One quarter = one year: ship with urgency.",
    ),
    "the-archive-method": (
        "Archive (PARA)",
        "Finished work out of active view.",
    ),
    "the-collectors-fallacy": (
        "Collector's fallacy",
        "Saving isn't learning until something ships.",
    ),
    "the-feynman-technique": (
        "Feynman technique",
        "Teach it plain; stumbles show gaps.",
    ),
    "the-future-of-pkm": (
        "Future of PKM",
        "New tools, same loop: capture, connect, create.",
    ),
    "the-garage-concept": (
        "Garage vs showroom",
        "Messy garage for notes, showroom for guests.",
    ),
    "the-knowledge-lifecycle": (
        "Knowledge lifecycle",
        "Capture → use → polish → fade → archive.",
    ),
    "the-power-of-interconnectivity": (
        "Interconnectivity",
        "Alone it's a fact, linked it's a case.",
    ),
    "the-second-brain-workflow": (
        "Second Brain workflow",
        "CODE on a loop, weekly.",
    ),
    "the-trusted-inbox": (
        "Trusted inbox",
        "One pipe, emptied every week.",
    ),
    "the-zettelkasten-myth": (
        "Zettelkasten myth",
        "Luhmann wrote the books, not the box.",
    ),
    "there-is-no-perfect-solution": (
        "No perfect solution",
        "Good enough today beats optimal someday.",
    ),
    "visual-thinking": (
        "Visual thinking",
        "Boxes and arrows before prose piles up.",
    ),
    "weekly-review-checklists": (
        "Weekly review checklist",
        "Inbox, calendar, projects, one ship action.",
    ),
    "zettelkasten": (
        "Zettelkasten",
        "One idea per note, dense links, write the network.",
    ),
}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def upsert_field(inner: str, key: str, value: str) -> str:
    escaped = value.replace('"', '\\"')
    line = f'{key}: "{escaped}"'
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    if pattern.search(inner):
        return pattern.sub(line, inner, count=1)
    if re.search(r"^review:\s*true\s*$", inner, re.M):
        return re.sub(r"^(review:\s*true\s*)$", rf"\1\n{line}", inner, count=1, flags=re.M)
    return inner + f"\n{line}"


def main() -> None:
    updated = 0
    missing_review: list[str] = []

    for slug, (front, back) in sorted(CARDS.items()):
        path = NOTES_DIR / f"{slug}.md"
        if not path.exists():
            print(f"missing file: {slug}.md")
            continue

        text = path.read_text(encoding="utf-8")
        fm, inner, body = split_frontmatter(text)
        if not fm:
            print(f"skip (no frontmatter): {slug}.md")
            continue
        if not re.search(r"^review:\s*true\s*$", inner, re.M):
            missing_review.append(slug)
            continue

        new_inner = upsert_field(inner, "card_front", front)
        new_inner = upsert_field(new_inner, "card_back", back)
        if new_inner == inner:
            continue

        path.write_text(f"---\n{new_inner}\n---\n\n{body}", encoding="utf-8")
        updated += 1
        print(f"card fields: {slug}.md")

    print(f"\nDone: {updated} notes updated.")
    if missing_review:
        print(f"Skipped (review not true): {', '.join(missing_review)}")


if __name__ == "__main__":
    main()
