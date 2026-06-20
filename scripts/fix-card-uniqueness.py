#!/usr/bin/env python3
"""Rewrite spine flashcards: JoRap voice, habit prompts, unique fronts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

# slug -> list of (front, back) - first person, plain speech, no em dashes
CARDS: dict[str, list[tuple[str, str]]] = {
    "capture": [
        ("Mid-commute spark. My first move?", "One trusted inbox. Don't organize yet."),
        ("Before I save, I ask:", "Would I act on it or cite it later? If no, skip."),
        ("Capture keeps dying on me. Likely cause?", "Friction. Simplify to one pipe."),
        ("I want two inboxes for work and home.", "Merge them. Split pipes rot."),
        ("Friday review - where's raw capture until then?", "Still in the inbox. Process on review day."),
        ("I'm tempted to tag and file on capture.", "Stop at inbox. Organize later."),
    ],
    "the-trusted-inbox": [
        ("40 inbox items, two weeks untouched.", "Trust is broken. Empty it now, same day every week."),
        ("Friday review - my step 1?", "Empty the Trusted Inbox first."),
        ("I stopped using the inbox and capture in my head.", "One pipe, weekly empty, no exceptions."),
        ("Second capture app for quick notes?", "One inbox, one owner, one rhythm."),
        ("What kills inbox trust fastest?", "Items rot without weekly processing."),
        ("Inbox item screams for a project folder mid-day.", "Wait for weekly review. Don't break capture flow."),
    ],
    "weekly-review-checklists": [
        ("Friday review - four steps in order?", "Inbox, calendar, projects, one ship action."),
        ("Review feels fresh and creative each week.", "Wrong. Same checklist every week - novelty reinvents the wheel."),
        ("I finish inbox and calendar but skip express.", "Pick one ship action before I close the review."),
        ("When do I run weekly review?", "Same day every week. Boring on purpose."),
        ("Step 3 of my weekly review?", "Review active projects - what's stuck, what's next."),
        ("Travel week and review gets skipped.", "Twenty minutes beats zero. Shorten, don't skip."),
    ],
    "signal-vs-noise": [
        ("Interesting article, won't change what I do this month.", "Admire it and move on. Don't save."),
        ("Before capture, my signal filter asks:", "Will this change what I do or believe this month?"),
        ("I save everything just in case.", "Capture without filtering - that's Collector's Fallacy."),
        ("Trending thread everyone is bookmarking.", "Noise unless it changes my action or belief this month."),
        ("Good content, wrong month, no action hook.", "Skip the save. The wiki isn't a trophy case."),
        ("Signal vs noise tightens capture how?", "This-month window on action or belief."),
    ],
    "the-collectors-fallacy": [
        ("Reading list grows but nothing ships.", "On every save I ask: what will I make with this?"),
        ("No planned creative output for a save.", "Don't save it."),
        ("Saving feels like learning.", "Learning starts when something leaves the notebook."),
        ("Fix for hoarded bookmarks?", "Tie every save to an express deadline."),
        ("I finished the article and filed it.", "Not learning yet. Ship or rewrite before it counts."),
        ("Collector's save filter - one question?", "What will I make with this?"),
    ],
    "atomic-notes": [
        ("Draft mixes browser tips AND meeting notes.", "Split. One claim per note."),
        ("Can I say the whole note in one breath without 'and'?", "If no, split into atomic notes."),
        ("I wrote three ideas under one heading.", "Three wikilinks beats one long file."),
        ("Note reads like a mini blog post with sections.", "One citable claim. Trim or split."),
        ("How do I organize atomic notes?", "Wikilinks between notes - not headings inside one file."),
        ("I can't link to one idea in a kitchen-sink note.", "Atomicity problem. Split so I can link."),
    ],
    "associative-linking": [
        ("I finish a new note. Minimum links?", "Two typed links - one extends, one contradicts."),
        ("Tempted to file by folder tree only.", "Folders sort. Links think. Link by meaning."),
        ("I remember the filename, not the idea.", "That's why I link while writing - filenames fade."),
        ("My note builds on Atomic Notes. Link type?", "Extends."),
        ("My note pushes against Slow Productivity. Link type?", "Contradicts - name the tradeoff."),
        ("Perfect folder tree but no wikilinks.", "Walkable garden needs links, not taxonomy."),
    ],
    "evergreen-notes": [
        ("Fleeting spark keeps showing up in weekly review.", "Promote to evergreen - complete sentences, two-year bar."),
        ("A tool I rely on changed how I work.", "Revise the evergreen note - not every trend spike."),
        ("My two-year test for evergreen:", "Sentences I'd still stand behind in two years."),
        ("Evergreen vs fleeting - daily choice?", "Cite later: evergreen. One-off spark: promote or drop."),
        ("Trendy take I might regret next year.", "Keep fleeting or skip. Don't evergreen it yet."),
        ("Evergreen feels stale but the topic is hot on Twitter.", "Revise for tool shifts. Ignore hype cycles."),
    ],
    "building-a-second-brain": [
        ("Audit: organize is theater, express never happens.", "Fix or cut that CODE step. No step just for show."),
        ("New to CODE - where do I start?", "Capture first. Offload before I organize."),
        ("Quarterly: which CODE step hasn't shipped anything?", "That step is cosplay. Redesign or drop it."),
        ("Notes pile up, nothing published.", "Express is the failure. Schedule ship from notes."),
        ("My organize step uses:", "PARA buckets - projects, areas, resources, archive."),
        ("I skipped capture and jumped to folders.", "CODE order: capture before organize, distill, express."),
    ],
    "para-method": [
        ("Active work with a deadline lands in my notes.", "Projects bucket. Name it or it stays Resources."),
        ("Ongoing responsibility, no end date.", "Areas bucket."),
        ("Reference with no owner yet.", "Resources - until a project claims it."),
        ("PARA sorts by what, not topic?", "Life responsibility - project vs area vs reference."),
        ("Finished project files?", "Archive - out of active Projects."),
        ("Topic folder tree vs PARA?", "PARA asks who owns it and when it ends - not the subject tag."),
    ],
    "pareto-principle": [
        ("Task board and reading list both feel urgent.", "Find the ~20% that moved the needle. Protect that slice."),
        ("Pareto rule for flashcards in this garden?", "~12 habit spine notes (~20%). Not every page."),
        ("Everything feels equally important, nothing moves.", "Pareto moment. Cut polish on the long tail."),
        ("Flashcard deck bloated to 40 notes.", "Violates Pareto. Trim to habits I use weekly."),
        ("I found the vital few tasks.", "Protect that slice. Stop polishing the rest."),
        ("80/20 is a physical law?", "No. Shorthand ratio, not math homework."),
    ],
    "note-relationships": [
        ("My note builds on Atomic Notes. Typed link?", "Extends."),
        ("My note names the tradeoff against Slow Productivity.", "Contradicts."),
        ("My checklist makes Weekly Review real. Link type?", "Implements."),
        ("Maps of Content gathers 20 notes. Link type?", "Index (MOC)."),
        ("Minimum on my atomic note:", "One extends plus one contradicts."),
        ("Two tools solve the same job - pick one for this note.", "Alternative relationship."),
    ],
}


def format_cards(cards: list[tuple[str, str]]) -> str:
    lines = ["cards:"]
    for front, back in cards:
        lines.append(f'  - front: "{front}"')
        lines.append(f'    back: "{back}"')
    return "\n".join(lines)


def replace_cards_block(text: str, slug: str) -> str:
    cards_yaml = format_cards(CARDS[slug])
    pattern = r"^cards:\n(?:\s+-\s+front:.*\n\s+back:.*\n?)+"
    if not re.search(pattern, text, re.M):
        raise SystemExit(f"No cards block in {slug}")
    return re.sub(pattern, cards_yaml + "\n", text, count=1, flags=re.M)


def main() -> None:
    fronts: dict[str, list[str]] = {}
    for slug, cards in CARDS.items():
        for front, _back in cards:
            fronts.setdefault(front, []).append(slug)

    dupes = {f: s for f, s in fronts.items() if len(s) > 1}
    if dupes:
        raise SystemExit(f"Duplicate fronts across deck: {dupes}")

    for slug in sorted(CARDS):
        path = NOTES_DIR / f"{slug}.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(replace_cards_block(text, slug), encoding="utf-8")
        print(f"  updated {path.name}")

    print(f"\nDone: {len(CARDS)} notes, {sum(len(c) for c in CARDS.values())} cards.")


if __name__ == "__main__":
    main()
