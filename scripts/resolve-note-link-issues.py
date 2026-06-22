#!/usr/bin/env python3
"""One-shot: add aliases and create stub notes for broken wikilink targets."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

ALIASES: dict[str, list[str]] = {
    "anti-fragile-systems.md": ["Antifragility"],
    "the-feynman-technique.md": ["Richard Feynman"],
    "creative-blocks.md": ["Writer's Block"],
    "pareto-principle.md": ["Vilfredo Pareto"],
    "note-relationships.md": ["Link Typing"],
    "drafting-in-public.md": ["Learning in Public"],
    "digital-serendipity.md": ["Serendipity"],
    "evergreen-vs-fleeting-notes.md": ["Fleeting Notes"],
    "evergreen-notes.md": ["Permanent Notes"],
    "the-knowledge-lifecycle.md": ["Note Maturity"],
    "capture.md": ["Frictionless Capture"],
    "maps-of-content.md": ["Table of Contents"],
    "digital-garden.md": ["Gardening Metaphor", "Work in Progress"],
    "future-proofing-knowledge.md": ["Plain Text Files"],
    "building-a-second-brain.md": ["CODE Method"],
}

STUBS: list[dict] = [
    {
        "slug": "getting-things-done",
        "title": "Getting Things Done",
        "claim": "**Getting Things Done** = David Allen's capture-clarify-organize system — inbox first, next actions, trusted lists.",
        "example": "My brain isn't a filing cabinet. GTD was one trusted inbox and a weekly review so open loops lived on paper, not at 2 a.m.",
        "tags": ["PKM", "Productivity", "GTD"],
        "extends": ["GTD vs PARA", "The Trusted Inbox"],
        "contradicts": "Slow Productivity",
    },
    {
        "slug": "coaching-ethics",
        "title": "Coaching Ethics",
        "claim": "**Coaching ethics** = develop the person without hiding behind their consent when the drill is unsafe or pointless.",
        "example": "The coach who said 'they signed the waiver' after a near-drown wasn't coaching — he dodged duty of care.",
        "tags": ["Leadership", "Safety", "Ethics"],
        "extends": ["Develop, Don't Endanger", "Servant Leadership"],
        "contradicts": "Life Before Achievement",
    },
    {
        "slug": "duty-of-care",
        "title": "Duty of Care",
        "claim": "**Duty of care** = leaders owe reasonable protection to people under their authority — not zero risk, not reckless harm.",
        "example": "The pool had a lifeguard on deck because 'swim at your own risk' doesn't erase the job of watching kids.",
        "tags": ["Leadership", "Safety", "Ethics"],
        "extends": ["Develop, Don't Endanger", "Life Before Achievement"],
        "contradicts": "Outcomes Over Pitch Decks",
    },
    {
        "slug": "psychological-safety",
        "title": "Psychological Safety",
        "claim": "**Psychological safety** = people can name mistakes and near-misses without fear of humiliation or retaliation.",
        "example": "The nurse reported the near-mix-up because the charge nurse thanked the catch, not the messenger.",
        "tags": ["Leadership", "Safety", "Work"],
        "extends": ["Heed Every Near-Miss", "Own the Error"],
        "contradicts": "Break the Escalation Cycle",
    },
    {
        "slug": "risk-management",
        "title": "Risk Management",
        "claim": "**Risk management** = name what can go wrong, how likely, how bad — then choose controls in order of strength.",
        "example": "We moved the hot oil station away from the walk lane before buying more warning signs — eliminate before manage.",
        "tags": ["Safety", "Systems Thinking"],
        "extends": ["Eliminate Before Managing", "Heed Every Near-Miss"],
        "contradicts": "There Is No Perfect Solution",
    },
    {
        "slug": "hierarchy-of-controls",
        "title": "Hierarchy of Controls",
        "claim": "**Hierarchy of controls** = remove the hazard first, then substitute, engineer, admin, PPE — in that order.",
        "example": "Guard rails beat 'be careful' signs; removing the trip hazard beats both.",
        "tags": ["Safety", "Systems Thinking"],
        "extends": ["Eliminate Before Managing"],
        "contradicts": "Standard Operating Procedures",
    },
    {
        "slug": "safety-by-design",
        "title": "Safety by Design",
        "claim": "**Safety by design** = build the activity so harm is hard to cause — not only train people to be careful around danger.",
        "example": "The new stove puts controls where elbows can't bump them — safer layout, not another lecture.",
        "tags": ["Safety", "Systems Thinking"],
        "extends": ["Eliminate Before Managing", "Hierarchy of Controls"],
        "contradicts": "Develop, Don't Endanger",
    },
    {
        "slug": "incident-investigation",
        "title": "Incident Investigation",
        "claim": "**Incident investigation** = find system causes after a miss — not only who to blame.",
        "example": "After the tray spill they traced prep timing, not just 'server was clumsy.'",
        "tags": ["Safety", "Continuous Improvement"],
        "extends": ["Heed Every Near-Miss", "Own the Error"],
        "contradicts": "By Their Fruits",
    },
    {
        "slug": "normalization-of-deviance",
        "title": "Normalization of Deviance",
        "claim": "**Normalization of deviance** = repeated close calls slowly redefine 'normal' until disaster feels surprising but was predictable.",
        "example": "Third time someone ran the red light in the parking lot and nobody wrote it up — until the fender bender.",
        "tags": ["Safety", "Leadership"],
        "extends": ["Heed Every Near-Miss"],
        "contradicts": "Failure as Feedback",
    },
    {
        "slug": "learning-organizations",
        "title": "Learning Organizations",
        "claim": "**Learning organizations** = teams that change process after mistakes instead of burying them.",
        "example": "After every Friday service they kept one 'what broke' line on the whiteboard until it was fixed or accepted.",
        "tags": ["Leadership", "Continuous Improvement"],
        "extends": ["Continuous Improvement", "Convert Pain Into Learning"],
        "contradicts": "By Their Fruits",
    },
    {
        "slug": "reversibility",
        "title": "Reversibility",
        "claim": "**Reversibility** = prefer choices you can undo — irreversible harm needs a higher bar.",
        "example": "Try the haircut at home with clippers that still leave length — not the zero guard first.",
        "tags": ["Decision Making", "Safety"],
        "extends": ["Life Before Achievement", "Decision Quality"],
        "contradicts": "Finish Strong",
    },
    {
        "slug": "ethical-leadership",
        "title": "Ethical Leadership",
        "claim": "**Ethical leadership** = authority used to protect people and tell the truth — not to win at their expense.",
        "example": "The manager killed the unsafe team-building exercise when a safer option achieved the same goal.",
        "tags": ["Leadership", "Ethics"],
        "extends": ["Servant Leadership", "Life Before Achievement"],
        "contradicts": "Outcomes Over Pitch Decks",
    },
    {
        "slug": "commonplace-book",
        "title": "Commonplace Book",
        "claim": "**Commonplace book** = a personal book of quotes and ideas worth keeping — ancestor of linked notes.",
        "example": "Grandpa's notebook of sermon lines and recipes — same job as my capture file, paper instead of wikilinks.",
        "tags": ["PKM", "Note Taking"],
        "extends": ["Analog Capture Tools", "Intellectual Sourcing"],
        "contradicts": "Digital Minimalism",
    },
    {
        "slug": "webhooks",
        "title": "Webhooks",
        "claim": "**Webhooks** = HTTP callbacks when something happens — push events instead of polling.",
        "example": "Form submit hits my script instantly instead of me refreshing the inbox every five minutes.",
        "tags": ["PKM", "Tools"],
        "extends": ["Building a Personal API"],
        "contradicts": "Local-first Software",
    },
    {
        "slug": "voice-memos",
        "title": "Voice Memos",
        "claim": "**Voice memos** = capture ideas by speaking when hands or eyes are busy.",
        "example": "Driving home from clinic I dictated the thought into the phone — transcribed later into the inbox.",
        "tags": ["PKM", "Capture"],
        "extends": ["Context-Aware Capture", "Mobile Capture Workflows"],
        "contradicts": "Atomic Notes",
    },
    {
        "slug": "ship-it",
        "title": "Ship It",
        "claim": "**Ship it** = publish the good-enough version instead of polishing forever.",
        "example": "The blog post went live with one rough paragraph — feedback beat another month in drafts.",
        "tags": ["Productivity", "Creative Output"],
        "extends": ["Creative Output", "Minimum Viable Product"],
        "contradicts": "Attention to Detail",
    },
    {
        "slug": "attention-economy",
        "title": "Attention Economy",
        "claim": "**Attention economy** = platforms compete for your focus — your attention is the product.",
        "example": "Twenty minutes 'checking news' was twenty minutes of ads aimed at my outrage — not rest.",
        "tags": ["Productivity", "Digital Minimalism"],
        "extends": ["Digital Minimalism", "Signal vs Noise"],
        "contradicts": "Digital Serendipity",
    },
    {
        "slug": "elon-musk",
        "title": "Elon Musk",
        "claim": "**Elon Musk** = public example people cite for first-principles reinvention — useful as shorthand, not as gospel.",
        "example": "Friend said 'Musk would strip it to atoms' about our overbuilt onboarding — fair push, wrong idol.",
        "tags": ["Mental Models", "Thinking"],
        "extends": ["First Principles Thinking"],
        "contradicts": "There Is No Perfect Solution",
    },
    {
        "slug": "network-analysis",
        "title": "Network Analysis",
        "claim": "**Network analysis** = study links and hubs in a graph — who connects whom, what's isolated.",
        "example": "The graph showed one note linking twelve others — that's the doorway I'd prune first.",
        "tags": ["PKM", "Graph"],
        "extends": ["Graph View Analytics", "Associative Linking"],
        "contradicts": "Maps of Content",
    },
    {
        "slug": "literature-notes",
        "title": "Literature Notes",
        "claim": "**Literature notes** = notes about a source in your own words — not a highlight dump.",
        "example": "One page per book chapter with my takeaway, not yellow paint on every line.",
        "tags": ["PKM", "Note Taking", "Research"],
        "extends": ["Intellectual Sourcing", "Progressive Summarization"],
        "contradicts": "The Collector's Fallacy",
    },
    {
        "slug": "crdt",
        "title": "CRDT",
        "claim": "**CRDT** = data structures that merge edits without a central lock — useful for offline-first sync.",
        "example": "Two phones edited the same list offline and both changes merged — no 'you must sync first' fight.",
        "tags": ["PKM", "Tools"],
        "extends": ["Local-first Software"],
        "contradicts": "Building a Personal API",
    },
    {
        "slug": "taxonomy",
        "title": "Taxonomy",
        "claim": "**Taxonomy** = a classification scheme — folders, tags, types — for finding things later.",
        "example": "Tags for 'faith' and 'PKM' beat one junk drawer folder called 'misc.'",
        "tags": ["PKM", "Metadata"],
        "extends": ["Metadata Strategy", "PARA Method"],
        "contradicts": "Associative Linking",
    },
    {
        "slug": "tony-buzan",
        "title": "Tony Buzan",
        "claim": "**Tony Buzan** = popularized mind mapping as a radiant, branching sketch — name people cite for the method.",
        "example": "The workshop called it 'Buzan style' — center idea, branches, no sentence essays on the page.",
        "tags": ["PKM", "Learning"],
        "extends": ["Mind Mapping"],
        "contradicts": "Atomic Notes",
    },
    {
        "slug": "lean-startup",
        "title": "Lean Startup",
        "claim": "**Lean startup** = build the smallest test, measure, learn — don't scale before validation.",
        "example": "Ten users on a landing page before I built the full app — saved a month on the wrong feature.",
        "tags": ["Productivity", "Projects"],
        "extends": ["Minimum Viable Product"],
        "contradicts": "Finish Strong",
    },
    {
        "slug": "share-sheet",
        "title": "Share Sheet",
        "claim": "**Share sheet** = the phone menu that sends a link or file into another app — mobile capture's front door.",
        "example": "Highlight in the browser → Share → Notes app — captured before I forgot why it mattered.",
        "tags": ["PKM", "Mobile"],
        "extends": ["Mobile Capture Workflows", "Capture"],
        "contradicts": "Analog Capture Tools",
    },
    {
        "slug": "maintenance-window",
        "title": "Maintenance Window",
        "claim": "**Maintenance window** = scheduled time to prune, fix links, and archive — not random Sunday panic.",
        "example": "First Sunday of the month is garden maintenance — broken links, stale drafts, nothing else.",
        "tags": ["PKM", "Review"],
        "extends": ["Periodic Knowledge Review", "Weekly Review Checklists"],
        "contradicts": "The Collector's Fallacy",
    },
    {
        "slug": "layered-reading",
        "title": "Layered Reading",
        "claim": "**Layered reading** = pass through the same source at increasing depth — skim, highlight, summarize.",
        "example": "First pass marked three sections; second pass only those got sentences in my own words.",
        "tags": ["PKM", "Learning"],
        "extends": ["Progressive Summarization", "Literature Notes"],
        "contradicts": "Spaced Repetition",
    },
    {
        "slug": "information-diet",
        "title": "Information Diet",
        "claim": "**Information diet** = choose what you consume on purpose — feeds are not neutral.",
        "example": "Unfollowed three outrage accounts and my morning wasn't ruined before breakfast.",
        "tags": ["PKM", "Productivity"],
        "extends": ["Signal vs Noise", "Digital Minimalism"],
        "contradicts": "Digital Serendipity",
    },
    {
        "slug": "deep-work",
        "title": "Deep Work",
        "claim": "**Deep work** = long, uninterrupted focus on hard thinking — Cal Newport's term for the opposite of fragment.",
        "example": "Phone in the drawer for ninety minutes — one note drafted that'd been 'almost done' for weeks.",
        "tags": ["Productivity", "Focus"],
        "extends": ["Slow Productivity"],
        "contradicts": "Mobile Capture Workflows",
    },
    {
        "slug": "forgetting-curve",
        "title": "Forgetting Curve",
        "claim": "**Forgetting curve** = memory fades fast without review — Ebbinghaus curve spaced repetition fights.",
        "example": "Forgot half the vocab by Friday until I drilled five words on the fridge during rice.",
        "tags": ["Learning", "Memory"],
        "extends": ["Spaced Repetition"],
        "contradicts": "Progressive Summarization",
    },
    {
        "slug": "behavioral-economics",
        "title": "Behavioral Economics",
        "claim": "**Behavioral economics** = how people actually decide — biases, framing, sunk costs — not only rational models.",
        "example": "Kept the gym membership because 'I already paid' — classic sunk cost, not future value.",
        "tags": ["Mental Models", "Decision Making"],
        "extends": ["Sunk Cost Fallacy", "Decision Quality"],
        "contradicts": "First Principles Thinking",
    },
    {
        "slug": "quarterly-planning",
        "title": "Quarterly Planning",
        "claim": "**Quarterly planning** = set goals and review on a thirteen-week rhythm — short enough to feel real.",
        "example": "January's vague 'get fit' became twelve weeks with a fridge scoreboard — week ten finally bit.",
        "tags": ["Productivity", "Planning"],
        "extends": ["The 12 Week Year", "Periodic Knowledge Review"],
        "contradicts": "Slow Productivity",
    },
    {
        "slug": "read-later-queue",
        "title": "Read Later Queue",
        "claim": "**Read later queue** = a parking lot for links you'll process later — dangerous if it becomes a graveyard.",
        "example": "Four hundred saved articles and I'd read twelve — the queue was guilt storage, not reading.",
        "tags": ["PKM", "Capture"],
        "extends": ["The Collector's Fallacy", "The Trusted Inbox"],
        "contradicts": "Active Knowledge Curation",
    },
    {
        "slug": "sketchpad",
        "title": "Sketchpad",
        "claim": "**Sketchpad** = private scratch space before anything goes public — drafts, diagrams, half-ideas.",
        "example": "The napkin layout for the garden page lived in Notes app for a month before one paragraph shipped.",
        "tags": ["PKM", "Digital Garden"],
        "extends": ["The Garage Concept", "Drafting in Public"],
        "contradicts": "Creative Output",
    },
    {
        "slug": "inbox-zero",
        "title": "Inbox Zero",
        "claim": "**Inbox zero** = process the inbox to empty regularly — each item decided, not hoarded.",
        "example": "Friday afternoon I triaged email to zero — Monday started from decisions made, not dread.",
        "tags": ["PKM", "Productivity"],
        "extends": ["The Trusted Inbox", "Getting Things Done"],
        "contradicts": "The Collector's Fallacy",
    },
]


def merge_aliases(path: Path, new_aliases: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return
    end = text.find("\n---", 3)
    fm = text[3:end]
    body = text[end + 4 :]
    existing = []
    m = re.search(r"^aliases:\s*\[(.*)\]\s*$", fm, re.M)
    if m:
        existing = [a.strip().strip('"') for a in m.group(1).split(",") if a.strip()]
    seen = {a.lower() for a in existing}
    merged = list(existing)
    for a in new_aliases:
        if a.lower() not in seen:
            merged.append(a)
            seen.add(a.lower())
    if merged == existing:
        return
    quoted = ", ".join(f'"{a}"' for a in merged)
    if m:
        fm = re.sub(r"^aliases:\s*\[.*\]\s*$", f"aliases: [{quoted}]", fm, count=1, flags=re.M)
    else:
        fm = fm.rstrip() + f"\naliases: [{quoted}]"
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")
    print(f"aliases: {path.name}")


def stub_markdown(stub: dict) -> str:
    title = stub["title"]
    slug = stub["slug"]
    extends = stub["extends"]
    if isinstance(extends, str):
        extends = [extends]
    contradicts = stub["contradicts"]
    desc = stub["claim"].strip("*").split("=", 1)[-1].strip()
    rows = []
    for ex in extends:
        rows.append(f"| extends | [[{ex}]] | Named in notes that link here |")
    rows.append(f"| contradicts | [[{contradicts}]] | when the opposite frame fits better |")
    table = "\n".join(rows)
    tags = ", ".join(f'"{t}"' for t in stub["tags"])
    return f"""---
title: "{title}"
meta_title: "{title}"
description: "{desc}"
date: 2026-06-22T06:00:00Z
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: [{tags}]
slug: "{slug}"
featured: false
status: seedling
draft: false
aliases: []
---
{stub["claim"]}

## Example

{stub["example"]}

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
{table}
"""


def main() -> None:
    for fname, aliases in ALIASES.items():
        path = NOTES / fname
        if path.exists():
            merge_aliases(path, aliases)

    for stub in STUBS:
        path = NOTES / f"{stub['slug']}.md"
        if path.exists():
            print(f"skip exists: {path.name}")
            continue
        path.write_text(stub_markdown(stub), encoding="utf-8")
        print(f"created: {path.name}")


if __name__ == "__main__":
    main()
