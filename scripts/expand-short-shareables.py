#!/usr/bin/env python3
"""Expand label-like shareable_thought lines under 40 chars."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import (
    dump_frontmatter,
    gets_point_across,
    shareable_lines_overlap,
    split_frontmatter,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
MIN_LEN = 40
MAX_LEN = 130
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")

# Punchy short lines that already work standalone - do not expand.
KEEP_SHORT = frozenset(
    {
        "Small fixes to how you work, repeated.",
        "Trust grows in the boring reps.",
        "I train the weak slice on purpose.",
        "Discipleship is following Jesus daily.",
        "Fatigue hits more than muscles.",
        "Plans earn nothing until work lands.",
        "A miss tells you what to fix next.",
        "If you can't, you don't own it yet.",
        "Free tier is not unlimited.",
        "One cluster the Spirit grows.",
        "I don't wait for them to go first.",
        "What you do matches what you claim.",
        "God declared me righteous at faith.",
        "Change the process after a miss.",
        "Don't bury it and move on.",
        "A saved believer can still lose reward.",
        "The easy win I can grab now.",
        "More input past the dose is noise.",
        "Twelve taps kills the spark.",
        "On mobile, friction is the enemy.",
        "Smooth talkers ship thorns sometimes.",
        "The Pareto principle is the 80/20 rule.",
        "I wait without turning brittle.",
        "If I never revisit notes, they rot.",
        "Crisis review is always too late.",
        "Output beats tuning the system alone.",
        "Say yes or no clearly.",
        "Pressure reveals what easy days hide.",
        "I hit Shuffle for another pair.",
        "Dangerous if it becomes a graveyard.",
        "Prefer choices you can undo.",
        "Respect isn't letting harm run.",
        "I pick the next move on purpose.",
        "The urge doesn't get to drive.",
        "My margin is labor, not hosting markup.",
        "Pass on what you figured out.",
        "Busy isn't the same as finished.",
        "I slow down one breath before I answer.",
        "I review on a schedule so ideas stick.",
        "I retune instead of clinging.",
        "Past effort is gone either way.",
        "I trace the loop behind the fire.",
        "I deny myself and follow Christ daily.",
        "One capture pipe I empty every week.",
        '"Good job" teaches nothing.',
    }
)

EXPANSIONS: dict[str, str] = {
    "Notes are inventory for me.": "Notes are inventory for me - posts, sermons, and code are the point, not the pile.",
    "The smallest setup that still works.": "Digital minimalism means the smallest setup that still works - not the fanciest stack I never open.",
    "The Father already feeds birds.": "The Father already feeds birds - worry about tomorrow argues with someone who runs the weather.",
    "Two speeds, one promotion rule.": "Fleeting notes and evergreen notes run at two speeds - one promotion rule decides what graduates.",
    "Still say no to bad dynamic scope.": "A git CMS still means saying no to bad dynamic scope - buttons for clients, same static build underneath.",
    "I publish via Git directly.": "I publish via Git directly when I'm the author - the CMS is for clients who need buttons.",
    '"I\'m bad at this" is a verdict.': 'Growth mindset treats "I\'m bad at this" as a verdict - "I missed three" is data I can train on.',
    '"I missed three" is data.': 'Growth mindset says "I missed three" is data to train on - not a fixed label on who I am.',
    "Jesus taught greatness through service.": "Jesus taught greatness through service - the Son washed feet the night before the cross.",
    "Before my obedience caught up.": "Justification means God declared me righteous at faith - before my obedience caught up.",
    "Love your enemies.": "Love your enemies - bless, pray, and do good without pretending the harm didn't happen.",
    "Second command, paired with loving God.": "Love your neighbor is the second command, paired with loving God - same heart, next person in front of me.",
    "Note the ones that earn repeat use.": "I note the mental models that earn repeat use in real decisions - retire the rest.",
    "Judge Not starts from the same ground.": "Mercy and Judge Not start from the same ground - I've needed grace I didn't earn.",
    "Study links and hubs in a graph.": "Network analysis means studying links and hubs in the graph - who connects whom, what's isolated.",
    "Who connects whom, what's isolated.": "Network analysis shows who connects whom in the graph - and which notes sit isolated without links.",
    "Open Knowledge Format (OKF) bundle.": "The OKF bundle is the same garden flattened for agents - markdown paths, required type, no Hugo build.",
    "Forgiveness flows the same way.": "Grace and forgiveness flow the same way - gift received first, extension to others second.",
    "Growth, not the ticket in.": "Sanctification is growth after faith - not the ticket that got me in the door.",
    "Discipleship is the daily walk.": "Discipleship is the daily walk with Jesus - not a one-time decision I filed and forgot.",
    "Gospel depth: Humility and Service.": "Servant leadership has gospel depth in humility and service - greatness is serving, not being served.",
    "Keep the person.": "Set calm boundaries and keep the person - firm line, steady voice, relationship intact.",
    "One clear line in a steady voice.": "Set one clear line in a steady voice - boundaries work when tone stays readable under pressure.",
    "Free Grace secured eternal life once.": "Free Grace secured eternal life once - standing stays settled even when fellowship feels distant.",
    "Classification in service of retrieval.": "Taxonomy is classification in service of retrieval - tags should help me find notes, not become a second job.",
    "A picture of who the kingdom favors.": "The Beatitudes are a picture of who the kingdom favors - meek, merciful, peacemakers, not the loud and grasping.",
    "Which fits Free Grace perfectly.": "The Beatitudes fit Free Grace perfectly - kingdom favor is gift, not wages for performance.",
    "The showroom is the blog.": "The garage concept splits showroom and workshop - the blog is the showroom, drafts are the garage.",
    "Active care, not just avoiding harm.": "The Golden Rule is active care for my neighbor - not just avoiding harm and calling it love.",
    "Enter by the narrow gate.": "Enter by the narrow gate - few find it because it costs self-rule, not because God hides the door.",
    "The road to life is narrow and hard.": "The narrow way warns the road to life is narrow and hard - few find it, but it's the one Jesus named.",
    "CODE and PARA in one loop.": "The second-brain workflow runs CODE and PARA in one loop - capture daily, express weekly.",
    "I store up what lasts.": "Treasure in heaven means I store up what lasts - earthly trophies rust, kingdom storage doesn't.",
    "One block on the actual deliverable.": "Priorities before the inbox means one protected block on the actual deliverable - email can wait its turn.",
    "Short enough to feel real.": "Quarterly planning works in thirteen-week arcs - short enough to feel real on the calendar.",
    "Irreversible harm needs a higher bar.": "Reversibility means irreversible harm needs a higher bar before I commit - undo when I can, slow down when I can't.",
    "Active recall in the browser.": "Review is active recall in the browser - flip cards when the right move needs to load under pressure.",
    "I pursue peace on purpose.": "Peacemakers pursue peace on purpose - they don't just avoid conflict and call it fine.",
    "Save, organize, reuse.": "PKM is save, organize, reuse - output beats tuning the system alone.",
    "The loops you build on purpose.": "Systems for growth are the loops I build on purpose - habits on ordinary Tuesdays, not crisis heroics.",
}


def norm(text: str) -> str:
    text = WIKILINK.sub(r"\1", text.lower())
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def plain(text: str) -> str:
    return WIKILINK.sub(r"\1", text)


def paragraphs(key: str) -> list[str]:
    return [p.strip() for p in key.strip().split("\n\n") if p.strip()]


def sentences(key: str) -> list[str]:
    out: list[str] = []
    for part in paragraphs(key):
        for sent in re.split(r"(?<=[.!?])\s+", part):
            sent = plain(sent.strip())
            if sent:
                out.append(sent)
    return out


def expand_line(line: str, fm: dict) -> str:
    line = line.strip()
    if len(line) >= MIN_LEN or line in KEEP_SHORT:
        return line
    if line in EXPANSIONS:
        return EXPANSIONS[line]
    key = fm.get("key_concept") if isinstance(fm.get("key_concept"), str) else ""
    line_norm = norm(line)
    best = ""
    best_score = 0.0
    for sent in sentences(key):
        if len(sent) < MIN_LEN or len(sent) > MAX_LEN or "[[" in sent:
            continue
        sn = norm(sent)
        if line_norm in sn or sn in line_norm:
            if len(sent) > len(best):
                best = sent
        else:
            lw = set(line_norm.split())
            sw = set(sn.split())
            if not lw or not sw:
                continue
            score = len(lw & sw) / len(lw | sw)
            if score > best_score and score >= 0.45:
                best_score = score
                best = sent
    if best and gets_point_across(best):
        return best
    return line


def incorporate_shareables(fm: dict) -> None:
    key = fm.get("key_concept") if isinstance(fm.get("key_concept"), str) else ""
    parts = paragraphs(key)
    key_norm = norm("\n\n".join(parts))
    for line in fm.get("shareable_thought") or []:
        if isinstance(line, str) and norm(line) not in key_norm:
            parts.append(line)
            key_norm = norm("\n\n".join(parts))
    seen: set[str] = set()
    final: list[str] = []
    for p in parts:
        n = norm(p)
        if n in seen:
            continue
        seen.add(n)
        final.append(p)
    fm["key_concept"] = "\n\n".join(final)


def main() -> int:
    expanded_lines = 0
    changed_notes = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        lines = fm.get("shareable_thought")
        if not isinstance(lines, list):
            continue
        new_lines: list[str] = []
        for line in lines:
            if not isinstance(line, str):
                continue
            fixed = line.replace('.".', '."').replace("..", ".")
            out = expand_line(fixed, fm)
            if len(out) > MAX_LEN:
                out = out[: MAX_LEN - 1].rstrip() + "."
            if any(shareable_lines_overlap(out, x) for x in new_lines):
                new_lines.append(fixed)
                continue
            if out != fixed:
                expanded_lines += 1
            new_lines.append(out)
        if len(new_lines) == 4:
            fm["shareable_thought"] = new_lines
        incorporate_shareables(fm)
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed_notes += 1
    print(f"Expanded {expanded_lines} shareable line(s) across {changed_notes} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
