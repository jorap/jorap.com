#!/usr/bin/env python3
"""Rewrite spine flashcards so each front has exactly one valid back."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

# slug -> list of (front, back)
CARDS: dict[str, list[tuple[str, str]]] = {
    "associative-linking": [
        ("Associative linking (definition)", "Link by meaning when you write."),
        ("Folders vs links", "Folders sort; links think."),
        ("Associative linking: minimum typed links per note?", "Two — one extends, one contradicts."),
        ("Why link while writing a note?", "Filenames fade; the links stick."),
        (
            "Associative linking enables which garden pattern?",
            "Walkable Zettelkasten without a perfect folder tree.",
        ),
        ("Associative linking extends which note type?", "Atomic Notes."),
    ],
    "note-relationships": [
        ("Five note relationship types", "Extends, contradicts, implements, alternative, index."),
        ("Minimum typed links on an atomic note", "One extends and one contradicts."),
        ("Extends (note relationship) means", "Builds on or narrows another note."),
        ("Contradicts (note relationship) means", "Names the tradeoff this note pushes against."),
        ("Implements (note relationship) means", "A checklist or workflow that makes a concept real."),
        ("Index (note relationship) means", "A hub note that gathers many notes (a MOC)."),
    ],
    "weekly-review-checklists": [
        ("Weekly review checklist (four steps)", "Inbox, calendar, projects, one ship action."),
        ("Weekly review step 1", "Empty the Trusted Inbox."),
        ("Weekly review step 2", "Scan the calendar."),
        ("Weekly review step 3", "Review projects."),
        ("Weekly review: why the same list every week?", "Novelty in reviews means reinventing the wheel."),
        ("Weekly review timing", "Same day every week — boring on purpose."),
    ],
    "the-trusted-inbox": [
        ("Trusted inbox (definition)", "One capture pipe you empty every week."),
        ("Trusted inbox rhythm", "Weekly Review Checklists — no exceptions."),
        ("What breaks inbox trust?", "Items rot without weekly processing."),
        ("If the inbox is not trusted", "You capture in your head instead."),
        ("Trusted inbox: how many pipes?", "One inbox, one owner, one rhythm."),
        ("Trusted inbox extends", "Capture."),
    ],
    "the-collectors-fallacy": [
        ("Collector's fallacy (definition)", "Saving feels like learning — until something ships."),
        ("Collector's save filter question", "What will I make with this?"),
        ("No planned creative output means", "Don't save it."),
        ("Reading vs learning (Collector's fallacy)", "Learning starts when something leaves the notebook."),
        ("Collector's fallacy fix", "Tie every save to an express deadline."),
        ("Collector's fallacy symptom", "Backlog grows but nothing ships."),
    ],
    "spaced-repetition": [
        ("Spaced repetition (definition)", "Review facts on a schedule — not whole essays."),
        ("What belongs in SRS?", "Facts you need cold recall for."),
        ("Spaced repetition: the wiki holds", "Linked ideas and understanding."),
        ("Spaced repetition: SRS holds", "Drill — vocabulary, definitions, references."),
        ("How many notes get review:true in this garden?", "About 15 spine notes (~20%), not the whole library."),
        ("After Feynman finds gaps, use what for drill?", "Spaced repetition (SRS)."),
    ],
    "signal-vs-noise": [
        ("Signal vs noise (definition)", "Save only what changes action or belief this month."),
        ("Signal filter question", "Will this change what I do or believe this month?"),
        ("When content is noise", "Admire it and move on — don't save."),
        ("Capture without filtering becomes", "The Collector's Fallacy."),
        ("Signal vs noise extends", "Capture."),
        ("Signal vs noise tightens capture with what window?", "This month — action or belief."),
    ],
    "progressive-summarization": [
        ("Progressive summarization (definition)", "Bold, highlight, summarize — on reuse only."),
        ("Progressive summarization layer 1", "Bold the good sentences."),
        ("Progressive summarization layer 2", "Highlight the best bold."),
        ("Progressive summarization layer 3", "Summary at top — only on second use."),
        ("Progressive summarization belongs in CODE as", "Distill."),
        ("Progressive summarization: when NOT to summarize", "On first save."),
    ],
    "pkm": [
        ("PKM (four steps)", "Capture, organize, distill, express."),
        ("PKM in plain language", "A backup brain for a loud life."),
        ("PKM is NOT", "Productivity cosplay."),
        ("PKM success test", "Save, find, rewrite on reuse, ship on schedule."),
        ("PKM onboarding note for this garden", "Getting Started."),
        ("PKM fourth CODE step", "Express — ship something from the notes."),
    ],
    "pareto-principle": [
        ("Pareto principle (definition)", "Most results come from a tiny slice of work."),
        ("Pareto ratio (shorthand)", "Roughly 80/20 — not a physical law."),
        ("When to use Pareto", "When everything feels equally urgent but nothing moves."),
        ("Pareto rule for flashcards in this garden", "~15 spine notes with review:true — not every page."),
        ("Pareto action", "Find the slice, protect it, cut the rest."),
        ("Pareto principle namesake", "Vilfredo Pareto."),
    ],
    "para-method": [
        ("PARA (four buckets)", "Projects, Areas, Resources, Archive."),
        ("PARA sorts by", "Life responsibility — not topic."),
        ("PARA: P stands for", "Projects — active work with a deadline."),
        ("PARA: first A stands for", "Areas — ongoing responsibilities without an end date."),
        ("PARA: unnamed project or area?", "Stays in Resources until it matters."),
        ("PARA: R stands for", "Resources — reference material."),
    ],
    "gtd-vs-para": [
        ("GTD vs PARA (one line)", "GTD runs tasks; PARA runs notes."),
        ("GTD: where do tasks live?", "The task app."),
        ("PARA: where does reference material live?", "PARA buckets."),
        ("GTD and PARA are", "Cousins, not competitors."),
        ("Duplicate filing tax (GTD vs PARA)", "Filing the same item in the task app and note folders."),
        ("GTD maintain phase overlaps with", "Weekly Review Checklists."),
    ],
    "evergreen-notes": [
        ("Evergreen notes (definition)", "Claims you'll still cite — revise when reality shifts."),
        ("Evergreen vs fleeting (one line)", "Evergreen = cite later; fleeting = promote or drop."),
        ("Revise evergreen notes when", "Tools change — not when trends spike."),
        ("Promote fleeting to evergreen when", "A spark keeps returning in Periodic Knowledge Review."),
        ("Evergreen test (two-year bar)", "Complete sentences you'd still stand behind in two years."),
        ("Evergreen notes extend", "Atomic Notes."),
    ],
    "capture": [
        ("Capture (definition)", "Save what resonates into one trusted inbox."),
        ("Capture rhythm", "Empty the inbox weekly."),
        ("Capture filter (one question)", "Would I act on it or cite it later?"),
        ("What kills capture?", "Friction."),
        ("Capture's one-pipe partner note", "The Trusted Inbox."),
        ("Capture in CODE is step", "One — before organize, distill, express."),
    ],
    "building-a-second-brain": [
        ("Second Brain (one line)", "Offload ideas so your head can think, not hoard."),
        ("CODE stands for", "Capture, organize, distill, express."),
        ("Second Brain starts with which CODE step?", "Capture."),
        ("Second Brain fails when", "Any CODE step is just for show."),
        ("Second Brain: how often to audit CODE steps?", "Quarterly."),
        ("Second Brain organize step uses", "PARA buckets."),
    ],
    "atomic-notes": [
        ("Atomic notes (definition)", "One claim you'd say out loud — too many ands, split it."),
        ("Non-atomic note example", "Browser tips plus meeting notes in one file."),
        ("Atomic notes get organized by", "Wikilinks — not headings inside one file."),
        ("Atomic notes vs mini blog posts", "One citable claim — not a sectioned essay."),
        ("Atomicity test (one breath)", "Can you say the whole note without and?"),
        ("Atomic notes extend", "Zettelkasten."),
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
