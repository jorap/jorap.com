#!/usr/bin/env python3
"""JoRap voice pass on ## Examples: em dash → hyphen; basketball Sports where better."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

# Sports bullets: basketball when it lands clearer than the prior sport.
SPORTS_BB: dict[str, str] = {
    "accountability": (
        'After we lost on a bad inbounds pass, the coach named who calls the play '
        '- not "the whole team messed up." One owner, one fix before the next possession.'
    ),
    "adaptability": (
        "Rain canceled our outdoor run and we moved practice to the covered court "
        "- same goal of getting reps in, different floor when the weather shifted."
    ),
    "atomic-notes": (
        '"Why my basketball shoes live by the door" is one claim - I\'d say it alone at carpool.'
    ),
    "attention-to-detail": (
        "We almost threw the inbounds pass on the wrong side of the line because two "
        "hash marks looked identical - the second read of the court map caught it."
    ),
    "compounding": (
        "Ten minutes of free throws every Tuesday looked pointless for months - then "
        "the percentage bent without me noticing the curve."
    ),
    "context-aware-capture": (
        'I saved a drill clip titled "use when our pick-and-roll breaks down" - six '
        "weeks later I knew why I kept it, not just what it showed."
    ),
    "daily-notes": (
        "Today's pocket slip is just fragments - pick up basketball shoes, ice after "
        "practice, call coach back - I promote one line to a real note when it repeats."
    ),
    "deliberate-practice": (
        "Our guard drills the weak-hand finish fifty times, not the whole scrimmage on autopilot "
        "- train the weak slice on purpose."
    ),
    "evergreen-notes": (
        "My free-throw note keeps the release point and follow-through - not last week's "
        "trending drill tip I'd regret next season."
    ),
    "expect-the-counter": (
        "We changed our full-court press and the other team adjusted by halftime - "
        "expect the counter meant building a backup look before tip-off."
    ),
    "failure-as-feedback": (
        "I missed three free throws in a row - failure as feedback was follow-through "
        "and routine, not deciding I'm \"not a basketball person.\""
    ),
    "growth-mindset": (
        "I missed three free throws in a row at clinic. Growth mindset was ten minutes "
        "on form, not deciding I'd never shoot reliably in a game."
    ),
    "judge-not": (
        "I spotted my teammate's travel in five seconds and missed my own lazy dribble "
        "- judge not starts with the log in my eye."
    ),
    "local-first-software": (
        "My kid's shooting log lives in a notebook in the gym bag - not an app that "
        "might vanish when the vendor pivots."
    ),
    "mental-models": (
        "Saturday basketball camp signup had forty options listed and I froze - Pareto "
        "got me to three that fit our budget, [[Low Hanging Fruit]] was registering "
        "before slots closed, compounding was ten minutes of ball-handling a week."
    ),
    "note-relationships": (
        'The coach\'s whiteboard lists "feeds into: secondary break" beside each drill '
        "- players see how today's reps connect before they leave the gym."
    ),
    "pareto-principle": (
        "The kids' activity list had six things and we skipped three nights - I trimmed "
        "to basketball and piano and we actually showed up."
    ),
    "stay-effective-in-new-conditions": (
        "Our guard dominates on the outdoor court and looks lost on the slick indoor "
        "floor for a week - staying effective means adjusting footwork, not defending "
        "yesterday's surface."
    ),
    "sunk-cost-fallacy": (
        "I kept running a set play that lost four straight because we'd drilled it all "
        "preseason - sunk cost is asking whether I keep it because it cost time, not "
        "because it still works."
    ),
    "the-12-week-year": (
        '"Fix our free-throw rate" lived as a someday goal until I gave it twelve weeks '
        "and a scoreboard on the locker - week ten finally bit."
    ),
    "the-feynman-technique": (
        "I tried to explain the three-second violation to my kid at halftime and stalled "
        "halfway - that gap told me I don't own the idea yet."
    ),
    "the-knowledge-lifecycle": (
        'The new set play lives in "learning" for three weeks, graduates to "game plan," '
        "then gets archived when we change offense."
    ),
    "versatility": (
        "When our center covers the wing for ten minutes, the team survives - useful "
        "without forgetting who normally owns the paint."
    ),
    "secret-devotion": (
        "The player doesn't live-stream her 5 a.m. shootarounds for applause - she "
        "trains because the game is the point, not the Strava badge."
    ),
    "network-analysis": (
        "The playbook diagram showed one motion offense linking twelve other sets - "
        "that was the doorway I'd simplify first."
    ),
    "spaced-repetition": (
        "We drill the baseline out-of-bounds play five minutes before every practice - "
        "same little doses beat cramming it the night before a game."
    ),
}


def fix_examples_block(block: str, slug: str) -> str:
    block = block.replace("\u2014", " - ")  # em dash
    if slug in SPORTS_BB:
        block = re.sub(
            r"- \*\*Sports:\*\* .+",
            f"- **Sports:** {SPORTS_BB[slug]}",
            block,
            count=1,
        )
    return block


def process(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    slug = path.stem
    m = re.search(r"(## Examples\n\n)(.*?)(\n## )", raw, re.S)
    if not m:
        return False
    new_block = fix_examples_block(m.group(2), slug)
    if new_block == m.group(2):
        return False
    new_raw = raw[: m.start(2)] + new_block + raw[m.end(2) :]
    path.write_text(new_raw, encoding="utf-8")
    return True


def main() -> None:
    n = sum(process(p) for p in sorted(NOTES.glob("*.md")))
    print(f"updated {n} notes")


if __name__ == "__main__":
    main()
