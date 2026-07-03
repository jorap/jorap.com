#!/usr/bin/env python3
"""Fix shareable_thought self-contained + independent issues from Jul 2026 review."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

KEY_APPEND: dict[str, str] = {
    "flashcards.md": (
        "Can I recall and use this knowledge when it matters - not review count or streak length?"
    ),
}

KEY_PATCHES: dict[str, str] = {
    "ethical-leadership.md": (
        "The standard you walk past is the standard you accept for everyone under you.\n\n"
        "Ethical leadership is integrity the team can see - what you tolerate in the open, not what you preach on the poster.\n\n"
        "The team copies what you tolerate, not what you preach."
    ),
    "systems-thinking.md": (
        "Systems thinking traces inputs, delays, and feedback behind the symptom.\n\n"
        "Change the process that keeps producing the fire - don't only patch tonight's symptom.\n\n"
        "Trace inputs, delays, and feedback before you patch tonight's symptom."
    ),
    "leadership.md": (
        "You take responsibility for direction, pace, and care when people look to you - title optional.\n\n"
        "When people look to you, they need someone to set direction - not just a name on the org chart.\n\n"
        "Pace matters as much as direction - calm urgency beats either panic or drift.\n\n"
        "Care means the people counting on you still feel seen when the pressure spikes."
    ),
    "signal-vs-noise.md": (
        "I save only what changes what I do or believe this month - most content is noise.\n\n"
        "If it won't change action or belief this month, it's noise.\n\n"
        "Admiring an article without a behavior change is entertainment, not signal.\n\n"
        "The filter is simple: would I act or cite this within thirty days?"
    ),
    "composure.md": (
        "Steady tone and pace when the room isn't - people read calm as competence.\n\n"
        "One beat before I reply often beats matching their volume.\n\n"
        "Stay readable and deliberate when others speed up or heat up.\n\n"
        "Slower speech and one clarifying question beat reflex when the room runs hot."
    ),
    "note-relationships.md": (
        "Four pair types in `relationships` frontmatter show how ideas push and pull - not just that two notes mention each other.\n\n"
        "Extends asks what this idea builds on; contradicts names the tradeoff it pushes against.\n\n"
        "Implements names what makes the idea real; alternative names another path that does the job."
    ),
    "the-feynman-technique.md": (
        "Teach-it-to-learn-it exposes gaps so evergreen notes stay honest and clear.\n\n"
        "Explain it simply to a blank page - the stumble marks the gap.\n\n"
        "A blank page is the honest audience - no jargon to hide behind."
    ),
    "the-knowledge-lifecycle.md": (
        "Ideas move through capture, use, polish, fade, and archive - spend effort where the idea actually is.\n\n"
        "I match effort to the stage an idea is in, not the stage I wish it were.\n\n"
        "Match effort to the stage an idea is in, not the stage you wish it were.\n\n"
        "Spend effort on polish only when an idea is in reuse - not when it's still a raw capture.\n\n"
        "Spend effort where the idea actually is - not on every flicker in the inbox."
    ),
    "first-principles-thinking.md": (
        "A saved quote isn't a principle until I rebuild the claim in my own words.\n\n"
        "Rebuild the claim in your own words before you link it.\n\n"
        "Borrowed quotes aren't principles until you rebuild the claim yourself."
    ),
    "joy.md": (
        "Fruits of the Spirit names joy beside love and peace in one cluster.\n\n"
        "Joy is grown by walking in the Spirit, not manufactured for credit. (Galatians 5:22).\n\n"
        "Performing joy while empty at home told me I was forcing fruit by will instead of abiding in Christ."
    ),
    "expect-the-counter.md": (
        "The opening move isn't the game.\n\n"
        "I rehearse what happens after they adapt.\n\n"
        "Rehearse the second move before tip-off - second-order thinking with skin in the game."
    ),
    "linking-by-meaning.md": (
        "Folders sort files; links connect ideas.\n\n"
        "One link to what extends the thought, one to what pushes back.\n\n"
        "Two typed links are enough for the garden to stay walkable six months later when the folder path is gone."
    ),
    "listen-before-fixing.md": (
        "Feeling heard comes before being helped.\n\n"
        "I repeat what I heard before I prescribe.\n\n"
        "Repeating what I heard keeps advice from landing like a correction."
    ),
    "local-first-software.md": (
        "Local-first means your device holds the truth; choose what's public, what's private, and what gets encrypted.\n\n"
        "Sync should merge edits without picking last-write-wins by clock alone."
    ),
    "the-trusted-inbox.md": (
        "If I don't trust my inbox, I capture in my head instead. One pipe, weekly empty, no exceptions.\n\n"
        "An inbox I don't empty becomes a junk drawer I stop using.\n\n"
        "If capture lives in my head, the system is decoration - not a second brain."
    ),
    "getting-things-done.md": (
        "GTD vs PARA splits tasks from notes; Allen owns the task side.\n\n"
        "Allen task-inbox system: capture everything, clarify next actions, trust the weekly review.\n\n"
        "Capture everything, clarify next actions, trust the weekly review.\n\n"
        "Tasks and notes live in separate systems - capture and weekly review own the task lane."
    ),
    "standard-operating-procedures.md": (
        "SOPs are simple written steps for recurring work - so nobody improvises under stress.\n\n"
        "Written steps beat improvisation when stress shrinks working memory.\n\n"
        "Nobody should improvise recurring work when stress shrinks working memory."
    ),
    "metadata-strategy.md": (
        "Tags, categories, dates, aliases - metadata should help me find notes, not become a second job.\n\n"
        "Light tags and aliases beat taxonomy hell inside PARA buckets.\n\n"
        "Metadata earns its keep when I can find the note in ten seconds."
    ),
    "periodic-knowledge-review.md": (
        "Crisis review is always too late.\n\n"
        "I calendar weekly and quarterly passes the way I'd calendar bills - inbox, active projects, evergreens on the clock, not when guilt spikes.\n\n"
        "Active curation on schedule beats guilt-driven binge review when the vault feels heavy."
    ),
    "safety-comes-first.md": (
        "Respect doesn't mean I ignore danger - I stop serious harm first, then restore choice when it's safe.\n\n"
        "Stopping harm first isn't disrespect - it's the precondition for real choice later."
    ),
    "lean-startup.md": (
        "Build the smallest test, measure, learn - don't scale before validation.\n\n"
        "Validate before you scale - polish comes after proof someone wants it.\n\n"
        "Measure what happened, then fix the template - not the pitch deck."
    ),
    "digital-serendipity.md": (
        "Serendipity isn't luck for me - I build systems where old notes resurface at the right time.\n\n"
        "I link notes on purpose so forgotten ideas surprise me when a new problem rhymes.\n\n"
        "A walkable graph beats hoping I'll remember the right filename."
    ),
    "duty-of-care.md": (
        "Owe people the care you'd expect if roles reversed - not the minimum the handbook allows.\n\n"
        "Duty of care is the legal and moral floor - not the minimum the handbook allows.\n\n"
        "Stop serious harm first; reasonable protection isn't optional because paperwork says so."
    ),
    "follow-through.md": (
        "The work after the handshake - recap, owners, dates, verification.\n\n"
        "Follow-through is the ticket, the check-in, and verification - not the enthusiasm at yes.\n\n"
        "A yes without owners and dates is a promise with no delivery address."
    ),
    "the-second-brain-workflow.md": (
        "CODE and PARA in one daily-to-weekly loop - capture daily, express weekly.\n\n"
        "Organize by project, distill when you reuse - don't polish notes nobody reads yet.\n\n"
        "Express weekly closes the loop - capture and organize are not enough."
    ),
    "slow-productivity.md": (
        "Busy isn't the same as finished.\n\n"
        "I run fewer active projects so notes become shipped work, not a guilt backlog.\n\n"
        "Four half-started builds eat the one client site that was supposed to ship this month."
    ),
    "habit-stacking.md": (
        "Habit stacking attaches a new small move to a habit that already runs on autopilot - one anchor, one add-on.\n\n"
        "One anchor habit, one tiny add-on - not a whole new routine.\n\n"
        "No new time slot - chain the new move onto one that already runs without thinking."
    ),
    "follow-their-lead.md": (
        "I join their world before I redirect it - their activity, topic, pace, starting point.\n\n"
        "Enter their frame before you try to redirect the conversation.\n\n"
        "Connection first, critique second - run their play once before you offer yours.\n\n"
        "Skip their starting point and you're fixing a problem they weren't naming."
    ),
}

DESC_PATCHES: dict[str, str] = {
    "the-feynman-technique.md": (
        "I teach the idea out loud to a blank page - wherever I stumble, I don't understand yet."
    ),
    "local-first-software.md": (
        "Local-first means my device holds the truth; sync is optional icing - backup should behave the same way."
    ),
}

SHAREABLE: dict[str, list[str]] = {
    "ethical-leadership.md": [
        "What I let slide in front of my team becomes their real standard, not what's printed on the poster.",
        "The standard you walk past is the standard you accept for everyone under you.",
        "Ethical leadership is integrity the team can see - what you tolerate in the open, not what you preach on the poster.",
        "The team copies what you tolerate, not what you preach.",
    ],
    "the-wise-builder.md": [
        "Hearing the words isn't enough - I build on rock when I actually do what Jesus said.",
        "Empty \"Lord, Lord\" without doing the Father's will is the fool's house (Matthew 7:21-23).",
        "Doing isn't what saves - faith saves - but genuine hearing still produces action.",
        "Both builders hear the sermon; only one obeys. (Matthew 7:24-27).",
    ],
    "outcomes-over-pitch-decks.md": [
        "Judge vendors, frameworks, and internal champions by what they produce - not slide polish, not LinkedIn aura.",
        "Smooth talkers ship thorns sometimes.",
        "I look at downstream stress, turnover, delivery, and whether the team got healthier or more brittle.",
        "Don't condemn souls; do read the fruit over time.",
    ],
    "note-relationships.md": [
        "My graph shows extends, contradicts, implements, alternative - not just two notes mentioning the same word.",
        "Four pair types in relationships frontmatter show how ideas push and pull - not just that two notes mention each other.",
        "Extends asks what this idea builds on; contradicts names the tradeoff it pushes against.",
        "Implements names what makes the idea real; alternative names another path that does the job.",
    ],
    "the-feynman-technique.md": [
        "I teach the idea out loud to a blank page - wherever I stumble, I don't understand yet.",
        "Explain it simply to a blank page - the stumble marks the gap.",
        "Teach-it-to-learn-it exposes gaps so evergreen notes stay honest and clear.",
        "A blank page is the honest audience - no jargon to hide behind.",
    ],
    "the-knowledge-lifecycle.md": [
        "Ideas move through capture, use, polish, fade, and archive in my vault.",
        "I match effort to the stage an idea is in, not the stage I wish it were.",
        "Spend effort on polish only when an idea is in reuse - not when it's still a raw capture.",
        "Spend effort where the idea actually is - not on every flicker in the inbox.",
    ],
    "first-principles-thinking.md": [
        "First principles thinking is rebuilding from what I actually believe, not someone else's quote.",
        "A saved quote isn't a principle until I rebuild the claim in my own words.",
        "Rebuild the claim in your own words before you link it.",
        "Borrowed quotes aren't principles until you rebuild the claim yourself.",
    ],
    "systems-thinking.md": [
        "I trace the loop behind the fire - inputs, delays, feedback - and fix the process, not tonight's patch.",
        "Systems thinking traces inputs, delays, and feedback behind the symptom.",
        "Change the process that keeps producing the fire - don't only patch tonight's symptom.",
        "Trace inputs, delays, and feedback before you patch tonight's symptom.",
    ],
    "digital-garden.md": [
        "My garden is where notes grow in public - linked, imperfect, alive on Hugo and Git.",
        "Public, linked, imperfect notes beat a private hoard.",
        "Update in public instead of hoarding drafts until they feel ready.",
        "My digital garden is a personal site where notes grow in public.",
    ],
    "joy.md": [
        "Joy is Spirit-grown gladness in believers who rest on Christ's promise - not a good-week performance.",
        "Fruits of the Spirit names joy beside love and peace in one cluster.",
        "Joy is grown by walking in the Spirit, not manufactured for credit. (Galatians 5:22).",
        "Performing joy while empty at home told me I was forcing fruit by will instead of abiding in Christ.",
    ],
    "judgment-seat.md": [
        "Believers stand before Christ after salvation to have works evaluated for reward.",
        "Eternal life was already settled by faith.",
        "Free Grace and Justification already decided where I spend forever.",
        "Wood, hay, and stubble burn; gold, silver, and precious stones last at the fire test.",
    ],
    "slow-productivity.md": [
        "Slow productivity is fewer active projects so work finishes deep instead of piling as guilt.",
        "Busy isn't the same as finished.",
        "I run fewer active projects so notes become shipped work, not a guilt backlog.",
        "Four half-started builds eat the one client site that was supposed to ship this month.",
    ],
    "expect-the-counter.md": [
        "I plan what happens after the other side adapts, not just how my opening move looks on paper.",
        "The opening move isn't the game.",
        "I rehearse what happens after they adapt.",
        "Rehearse the second move before tip-off - second-order thinking with skin in the game.",
    ],
    "linking-by-meaning.md": [
        "I link notes so ideas meet in the graph without me memorizing every folder path.",
        "Folders sort files; links connect ideas.",
        "One link to what extends the thought, one to what pushes back.",
        "Two typed links are enough for the garden to stay walkable six months later when the folder path is gone.",
    ],
    "listen-before-fixing.md": [
        "Listen before fixing - repeat what you heard, then respond.",
        "Feeling heard comes before being helped.",
        "I repeat what I heard before I prescribe.",
        "Repeating what I heard keeps advice from landing like a correction.",
    ],
    "local-first-software.md": [
        "Local-first means my device holds the truth; sync is optional icing.",
        "I want my notes backup to behave like local-first - device holds truth, sync is optional icing.",
        "Local-first means your device holds the truth; choose what's public, what's private, and what gets encrypted.",
        "Sync should merge edits without picking last-write-wins by clock alone.",
    ],
    "leadership.md": [
        "Leadership is owning direction, pace, and care when people look to you - title optional.",
        "When people look to you, they need someone to set direction - not just a name on the org chart.",
        "Pace matters as much as direction - calm urgency beats either panic or drift.",
        "Care means the people counting on you still feel seen when the pressure spikes.",
    ],
    "signal-vs-noise.md": [
        "I save only what changes what I do or believe this month - most feeds are noise.",
        "If it won't change action or belief this month, it's noise.",
        "Admiring an article without a behavior change is entertainment, not signal.",
        "The filter is simple: would I act or cite this within thirty days?",
    ],
    "composure.md": [
        "Composure is steady voice and pace when the room isn't - people read calm as competence.",
        "One beat before I reply often beats matching their volume.",
        "Stay readable and deliberate when others speed up or heat up.",
        "Slower speech and one clarifying question beat reflex when the room runs hot.",
    ],
    "habit-stacking.md": [
        "I piggyback a new tiny habit onto one that already runs without thinking, like notebook after coffee.",
        "Habit stacking attaches a new small move to a habit that already runs on autopilot - one anchor, one add-on.",
        "One anchor habit, one tiny add-on - not a whole new routine.",
        "No new time slot - chain the new move onto one that already runs without thinking.",
    ],
    "follow-their-lead.md": [
        "I join their world - their topic, pace, starting point - before I try to steer.",
        "Enter their frame before you try to redirect the conversation.",
        "Connection first, critique second - run their play once before you offer yours.",
        "Skip their starting point and you're fixing a problem they weren't naming.",
    ],
    "the-trusted-inbox.md": [
        "One capture pipe I empty every week - if I don't trust it, I hoard ideas in my head instead.",
        "One pipe, weekly empty, no exceptions - trust is built by emptying, not by hoping.",
        "An inbox I don't empty becomes a junk drawer I stop using.",
        "If capture lives in my head, the system is decoration - not a second brain.",
    ],
    "flashcards.md": [
        "Learn less, retain longer, apply more.",
        "Can I recall and use this knowledge when it matters - not review count or streak length?",
        "Cards exist so the right move is already loaded when life shows up.",
        "I opt notes into drill cards when recall and use in real life matter, and export to Anki when I want SRS on my phone.",
    ],
    "metadata-strategy.md": [
        "If tagging a note takes longer than writing it, my system is fighting me.",
        "Tags, categories, dates, aliases - metadata should help me find notes, not become a second job.",
        "Light tags and aliases beat taxonomy hell inside PARA buckets.",
        "Metadata earns its keep when I can find the note in ten seconds.",
    ],
    "periodic-knowledge-review.md": [
        "If I never revisit notes, they rot.",
        "I calendar weekly and quarterly passes like I'd calendar bills.",
        "Crisis review is always too late.",
        "Active curation on schedule beats guilt-driven binge review when the vault feels heavy.",
    ],
    "safety-comes-first.md": [
        "I stop the unsafe thing first, then restore choice when the situation is stable.",
        "Respect isn't letting harm run.",
        "Respect doesn't mean I ignore danger - I stop serious harm first, then restore choice when it's safe.",
        "Stopping harm first isn't disrespect - it's the precondition for real choice later.",
    ],
    "lean-startup.md": [
        "I'd rather ship a rough test and learn than polish a product nobody wanted.",
        "Build the smallest test, measure, learn - don't scale before validation.",
        "Validate before you scale - polish comes after proof someone wants it.",
        "Measure what happened, then fix the template - not the pitch deck.",
    ],
    "digital-serendipity.md": [
        "Old notes surprise me on schedule because I linked them on purpose, not because I got lucky.",
        "Serendipity isn't luck for me - I build systems where old notes resurface at the right time.",
        "I link notes on purpose so forgotten ideas surprise me when a new problem rhymes.",
        "A walkable graph beats hoping I'll remember the right filename.",
    ],
    "duty-of-care.md": [
        "If roles flipped, I'd want reasonable protection from harm - that's the bar I owe people under me.",
        "Owe people the care you'd expect if roles reversed - not the minimum the handbook allows.",
        "Duty of care is the legal and moral floor - not the minimum the handbook allows.",
        "Stop serious harm first; reasonable protection isn't optional because paperwork says so.",
    ],
    "follow-through.md": [
        "Saying yes is cheap; follow-through is recap, owners, dates, and checking it actually landed.",
        "The work after the handshake - recap, owners, dates, verification.",
        "Follow-through is the ticket, the check-in, and verification - not the enthusiasm at yes.",
        "A yes without owners and dates is a promise with no delivery address.",
    ],
    "the-second-brain-workflow.md": [
        "Capture to inbox, organize by project, distill on reuse, express weekly - CODE and PARA in one loop.",
        "CODE and PARA in one daily-to-weekly loop - capture daily, express weekly.",
        "Organize by project, distill when you reuse - don't polish notes nobody reads yet.",
        "Express weekly closes the loop - capture and organize are not enough.",
    ],
    "getting-things-done.md": [
        "David Allen's capture-clarify-organize loop gives me a trusted inbox, next actions, and a weekly review.",
        "GTD vs PARA splits tasks from notes; Allen owns the task side.",
        "Capture everything, clarify next actions, trust the weekly review.",
        "Tasks and notes live in separate systems - capture and weekly review own the task lane.",
    ],
    "standard-operating-procedures.md": [
        "I write short steps for deploys and incidents so nobody has to improvise when the clock is loud.",
        "SOPs are simple written steps for recurring work.",
        "Nobody should improvise recurring work when stress shrinks working memory.",
        "Written steps beat improvisation when stress shrinks working memory.",
    ],
}


def apply() -> int:
    changed = 0
    for name in sorted(set(KEY_PATCHES) | set(SHAREABLE) | set(DESC_PATCHES) | set(KEY_APPEND)):
        path = NOTES / name
        if not path.exists():
            print(f"SKIP missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        if name in DESC_PATCHES:
            fm["description"] = DESC_PATCHES[name]
        if name in KEY_PATCHES:
            fm["key_concept"] = KEY_PATCHES[name]
        if name in KEY_APPEND:
            existing = (fm.get("key_concept") or "").rstrip()
            patch = KEY_APPEND[name]
            if patch not in existing:
                fm["key_concept"] = f"{existing}\n\n{patch}"
        if name in SHAREABLE:
            fm["shareable_thought"] = SHAREABLE[name]
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    n = apply()
    print(f"Updated {n} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
