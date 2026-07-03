#!/usr/bin/env python3
"""Key_concept expansions + four distinct principle-only shareable_lines."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, shareable_lines_overlap, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

KEY_PATCHES: dict[str, str] = {
    "build-a-reliable-default.md": (
        "Make that fallback a simple, dependable response - rehearsed enough to run when thinking is thin.\n\n"
        "When thinking is thin, run the script you already rehearsed.\n\n"
        "The rehearsed move beats improvising when the clock is loud."
    ),
    "coaching-ethics.md": (
        "Consent doesn't erase the job when the drill is unsafe.\n\n"
        "Unsafe or pointless drills still owe reasonable protection to people under your influence.\n\n"
        "Reasonable protection still applies when consent was given for a bad drill."
    ),
    "creative-blocks.md": (
        "Creative blocks aren't solved by more capture - ship one small action instead.\n\n"
        "Staring at a blank page with full notes means output fixes, not another capture pass.\n\n"
        "One small ship action usually unsticks me when the page stays blank."
    ),
    "daily-notes.md": (
        "Daily notes are fleeting by default, with quick buffer flushes between tasks.\n\n"
        "Promote a repeating fragment to a real note; let the rest fade.\n\n"
        "A scratch pad for the day - not every fragment deserves to become permanent."
    ),
    "deep-work.md": (
        "Protected focus blocks; Capture handles the rest.\n\n"
        "Hard thinking earns a protected block. Capture handles what tries to interrupt it."
    ),
    "digital-garden.md": (
        "My digital garden is a personal site where notes grow in public.\n\n"
        "Public, linked, imperfect notes beat a private hoard.\n\n"
        "Update in public instead of hoarding drafts until they feel ready."
    ),
    "first-principles-thinking.md": (
        "When a note is only a quote, I add what I actually believe from scratch.\n\n"
        "Rebuild the claim in your own words before you link it.\n\n"
        "Borrowed quotes aren't principles until you rebuild the claim yourself."
    ),
    "habit-stacking.md": (
        "Habit stacking attaches a new small move to a habit that already runs on autopilot - one anchor, one add-on.\n\n"
        "One anchor habit, one tiny add-on - not a whole new routine."
    ),
    "incident-investigation.md": (
        "Blameless tone keeps investigation on system causes.\n\n"
        "Trace layout, limits, and rules - not just who was standing there when it broke.\n\n"
        "Fix the system before you close the file on who to blame."
    ),
    "learning-organizations.md": (
        '"What broke" line stays until fixed or accepted.\n\n'
        "Change the process after a miss - don't bury it and move on."
    ),
    "maps-of-content.md": (
        "A MOC is a curated index of notes on a topic.\n\n"
        "Write the hub by hand when the topic sprawls past what you can hold in memory.\n\n"
        "A table of contents I write by hand beats whatever the folder tree implies."
    ),
    "mental-models.md": (
        "Mainstream mental models for decisions and performance - note the ones that earn repeat use.\n\n"
        "Keep the lens only if it survives a real decision.\n\n"
        "Retire the model when real decisions prove it wrong."
    ),
    "mind-mapping.md": (
        "Mind maps and sketches are the messy first pass - turn them into atomic notes after, not instead.\n\n"
        "Branches and bubbles first; atomic notes after."
    ),
    "pressure-reveals-weakness.md": (
        "Pressure reveals what easy days hide.\n\n"
        "Build habits and systems that still work when stakes spike.\n\n"
        "Rehearse the move on easy days so it runs when pressure hits.\n\n"
        "Easy days are for rehearsing the move pressure will demand later."
    ),
    "psychological-safety.md": (
        "Join their framing before you redirect the blame.\n\n"
        "Thank the person for speaking up - silence teaches the next person to hide the miss.\n\n"
        "Near-miss reports need gratitude, not punishment."
    ),
    "quarterly-planning.md": (
        "Zoom out every ninety days so weekly noise doesn't eat the year's aim.\n\n"
        "Thirteen weeks is short enough to feel real on the calendar.\n\n"
        "Ninety-day zoom-outs keep weekly noise from eating the year's aim."
    ),
    "signal-vs-noise.md": (
        "I save only what changes what I do or believe this month - most content is noise.\n\n"
        "If it won't change action or belief this month, it's noise."
    ),
    "sustainable-performance.md": (
        "Sustainable performance is output you can keep without burning out or cutting corners on safety.\n\n"
        "Pace you can repeat beats a sprint that mortgages next month.\n\n"
        "Don't mortgage next month's capacity for this week's sprint."
    ),
    "the-collectors-fallacy.md": (
        "Collecting articles feels like progress - tie saves to express deadlines or cut them.\n\n"
        "Every save needs a ship date or a delete date."
    ),
    "the-knowledge-lifecycle.md": (
        "Ideas move through capture, use, polish, fade, and archive - spend effort where the note actually is.\n\n"
        "Match effort to the stage the note is in, not the stage you wish it were."
    ),
    "pkm.md": (
        "PKM is the plain name for the save-organize-use system getting started introduces ([[Getting Started]]).\n\n"
        "Save, organize, reuse - output beats tuning the system alone."
    ),
    "the-12-week-year.md": (
        "Twelve-week arcs compress goals into review quarters you actually feel ([[Periodic Knowledge Review]]).\n\n"
        "Map wiki projects to the arc you can actually feel on the calendar.\n\n"
        "Review quarters you can feel beat vague annual resolutions."
    ),
    "the-feynman-technique.md": (
        "Teach-it-to-learn-it exposes gaps so evergreen notes stay honest and clear ([[Evergreen Notes]]).\n\n"
        "Explain it simply to a blank page - the stumble marks the gap."
    ),
    "workplace-principles.md": (
        "One standup-sized claim per note - plain language I can share with a secular team.\n\n"
        "Faith stays in the faith cluster; these are the versions I can share with a secular team without watering down the move.\n\n"
        "Meeting-sized examples with wikilink back to gospel depth when I need the full move."
    ),
    "issues.md": (
        "Fix the speck in the graph without playing judge over the author.\n\n"
        "Structure issues flag missing extends or contradicts rows in the Note Relationships table."
    ),
    "accountability.md": (
        "Clear ownership - who answers for the outcome, the miss, and the fix.\n\n"
        "One owner per outcome - not \"everyone was involved.\"\n\n"
        "Name the owner, the miss, and the fix before the conversation ends."
    ),
    "hierarchy-of-controls.md": (
        "Eliminate the hazard before warnings, admin, or PPE.\n\n"
        "Guard rails beat signs when you can remove the hazard instead.\n\n"
        "Named rollback is a control layer before irreversible harm."
    ),
    "random-duo.md": (
        "Forced serendipity - two unrelated claims side by side so I notice links I forgot to make.\n\n"
        "Two notes from the garden, picked at random.\n\n"
        "Shuffle again when the pair doesn't spark a link worth making.\n\n"
        "Side-by-side unrelated claims surface links I forgot to make."
    ),
}

SHAREABLE: dict[str, list[str]] = {
    "build-a-reliable-default.md": [
        "A reliable default is the simple rehearsed move I run when thinking is thin.",
        "Make that fallback a simple, dependable response - rehearsed enough to run when thinking is thin.",
        "When thinking is thin, run the script you already rehearsed.",
        "The rehearsed move beats improvising when the clock is loud.",
    ],
    "coaching-ethics.md": [
        "Develop the person without hiding behind consent when the drill is unsafe or pointless.",
        "Consent doesn't erase the job when the drill is unsafe.",
        "Unsafe or pointless drills still owe reasonable protection to people under your influence.",
        "Reasonable protection still applies when consent was given for a bad drill.",
    ],
    "creative-blocks.md": [
        "Thousands of notes and I still stare at a blank page - one small ship action usually unsticks me.",
        "Creative blocks aren't solved by more capture - ship one small action instead.",
        "Staring at a blank page with full notes means output fixes, not another capture pass.",
        "One small ship action usually unsticks me when the page stays blank.",
    ],
    "daily-notes.md": [
        "My daily note is a scratch pad for today's fragments, not a diary I expect to last forever.",
        "Daily notes are fleeting by default, with quick buffer flushes between tasks.",
        "Promote a repeating fragment to a real note; let the rest fade.",
        "A scratch pad for the day - not every fragment deserves to become permanent.",
    ],
    "deep-work.md": [
        "I protect uninterrupted blocks for hard thinking and let capture catch what tries to interrupt.",
        "Protected focus blocks; Capture handles the rest.",
        "Hard thinking earns a protected block.",
        "Capture handles what tries to interrupt it.",
    ],
    "digital-garden.md": [
        "My garden is where notes grow in public - linked, imperfect, alive on Hugo and Git.",
        "My digital garden is a personal site where notes grow in public.",
        "Public, linked, imperfect notes beat a private hoard.",
        "Update in public instead of hoarding drafts until they feel ready.",
    ],
    "first-principles-thinking.md": [
        "First principles thinking is rebuilding from what I actually believe, not someone else's quote.",
        "When a note is only a quote, I add what I actually believe from scratch.",
        "Rebuild the claim in your own words before you link it.",
        "Borrowed quotes aren't principles until you rebuild the claim yourself.",
    ],
    "habit-stacking.md": [
        "I piggyback a new tiny habit onto one that already runs without thinking, like notebook after coffee.",
        "Habit stacking attaches a new small move to a habit that already runs on autopilot - one anchor, one add-on.",
        "One anchor habit, one tiny add-on - not a whole new routine.",
    ],
    "incident-investigation.md": [
        "Find system causes after a miss - not only who to blame.",
        "Blameless tone keeps investigation on system causes.",
        "Trace layout, limits, and rules - not just who was standing there when it broke.",
        "Fix the system before you close the file on who to blame.",
    ],
    "learning-organizations.md": [
        "Teams that change process after mistakes instead of burying them.",
        '"What broke" line stays until fixed or accepted.',
        "Change the process after a miss - don't bury it and move on.",
    ],
    "maps-of-content.md": [
        "I write hub notes by hand when one topic spreads across too many files to hold in my head.",
        "A MOC is a curated index of notes on a topic.",
        "Write the hub by hand when the topic sprawls past what you can hold in memory.",
        "A table of contents I write by hand beats whatever the folder tree implies.",
    ],
    "mental-models.md": [
        "Mental models are thinking shortcuts I keep when they survive real decisions.",
        "Mainstream mental models for decisions and performance - note the ones that earn repeat use.",
        "Keep the lens only if it survives a real decision.",
        "Retire the model when real decisions prove it wrong.",
    ],
    "mind-mapping.md": [
        "Mind maps are for the messy first pass - branches, bubbles, relationships. I export to atomic notes after, not instead.",
        "Mind maps and sketches are the messy first pass - turn them into atomic notes after, not instead.",
        "Branches and bubbles first; atomic notes after.",
    ],
    "pressure-reveals-weakness.md": [
        "Pressure reveals what easy days hide.",
        "Build habits and systems that still work when stakes spike.",
        "Rehearse the move on easy days so it runs when pressure hits.",
        "Easy days are for rehearsing the move pressure will demand later.",
    ],
    "psychological-safety.md": [
        "People can name mistakes and near-misses without fear of humiliation or retaliation.",
        "Join their framing before you redirect the blame.",
        "Thank the person for speaking up - silence teaches the next person to hide the miss.",
        "Near-miss reports need gratitude, not punishment.",
    ],
    "quarterly-planning.md": [
        "Set goals and review on a thirteen-week rhythm.",
        "Zoom out every ninety days so weekly noise doesn't eat the year's aim.",
        "Thirteen weeks is short enough to feel real on the calendar.",
        "Ninety-day zoom-outs keep weekly noise from eating the year's aim.",
    ],
    "signal-vs-noise.md": [
        "I save only what changes what I do or believe this month - most feeds are noise.",
        "I save only what changes what I do or believe this month - most content is noise.",
        "If it won't change action or belief this month, it's noise.",
    ],
    "sustainable-performance.md": [
        "I aim for a pace I can hold next month without burning out or cutting safety corners.",
        "Sustainable performance is output you can keep without burning out or cutting corners on safety.",
        "Pace you can repeat beats a sprint that mortgages next month.",
        "Don't mortgage next month's capacity for this week's sprint.",
    ],
    "the-collectors-fallacy.md": [
        "Saving articles felt like progress until I tied every save to an express deadline or cut it.",
        "Collecting articles feels like progress - tie saves to express deadlines or cut them.",
        "Every save needs a ship date or a delete date.",
    ],
    "the-knowledge-lifecycle.md": [
        "Ideas move through capture, use, polish, fade, and archive in my vault - I match effort to the stage.",
        "Ideas move through capture, use, polish, fade, and archive - spend effort where the note actually is.",
        "Match effort to the stage the note is in, not the stage you wish it were.",
    ],
    "pkm.md": [
        "PKM is how I save, organize, and reuse what I learn - not a hobby of collecting apps.",
        "PKM is the plain name for the save-organize-use system getting started introduces.",
        "Save, organize, reuse - output beats tuning the system alone.",
    ],
    "the-12-week-year.md": [
        "I compress yearly goals into twelve-week arcs I can actually feel.",
        "Twelve-week arcs compress goals into review quarters you actually feel.",
        "Map wiki projects to the arc you can actually feel on the calendar.",
        "Review quarters you can feel beat vague annual resolutions.",
    ],
    "the-feynman-technique.md": [
        "I teach the note out loud to a blank page - wherever I stumble, I don't understand yet.",
        "Teach-it-to-learn-it exposes gaps so evergreen notes stay honest and clear.",
        "Explain it simply to a blank page - the stumble marks the gap.",
    ],
    "workplace-principles.md": [
        "The same ethics as Eternal Principles, in plain office language where religious terms sound awkward.",
        "One standup-sized claim per note - plain language I can share with a secular team.",
        "Faith stays in the faith cluster; these are the versions I can share with a secular team without watering down the move.",
        "Meeting-sized examples with wikilink back to gospel depth when I need the full move.",
    ],
    "issues.md": [
        "Broken wikilinks and note titles mentioned in prose without a wikilink - listed below and on each affected note.",
        "Fix the speck in the graph without playing judge over the author.",
        "Frontmatter and flashcards are not checked - only the note body.",
        "Structure issues flag missing extends or contradicts rows in the Note Relationships table.",
    ],
    "accountability.md": [
        "Accountability is naming who owns the result - and what happens when it slips.",
        "Clear ownership - who answers for the outcome, the miss, and the fix.",
        "One owner per outcome - not \"everyone was involved.\"",
        "Name the owner, the miss, and the fix before the conversation ends.",
    ],
    "hierarchy-of-controls.md": [
        "Remove the hazard first, then substitute, engineer, admin, PPE - in that order.",
        "Eliminate the hazard before warnings, admin, or PPE.",
        "Guard rails beat signs when you can remove the hazard instead.",
        "Named rollback is a control layer before irreversible harm.",
    ],
    "random-duo.md": [
        "Forced serendipity - two unrelated claims side by side so I notice links I forgot to make.",
        "Two notes from the garden, picked at random.",
        "Shuffle again when the pair doesn't spark a link worth making.",
        "Side-by-side unrelated claims surface links I forgot to make.",
    ],
}


def _pad_to_four(lines: list[str], fm: dict) -> list[str]:
    merged: list[str] = []
    for line in lines:
        if any(shareable_lines_overlap(line, x) for x in merged):
            continue
        merged.append(line)
        if len(merged) >= 4:
            return merged[:4]
    import importlib

    seed = importlib.import_module("seed-note-shareable-lines")
    for line in seed.draft_shareable_lines(fm):
        if any(shareable_lines_overlap(line, x) for x in merged):
            continue
        merged.append(line)
        if len(merged) >= 4:
            break
    return merged[:4]


def main() -> int:
    changed = 0
    targets = set(KEY_PATCHES) | set(SHAREABLE)
    for path in sorted(NOTES.glob("*.md")):
        if path.name not in targets:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if path.name in KEY_PATCHES:
            fm["key_concept"] = KEY_PATCHES[path.name]
        if path.name in SHAREABLE:
            fm["shareable_lines"] = _pad_to_four(SHAREABLE[path.name], fm)
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Patched {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
