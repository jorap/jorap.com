#!/usr/bin/env python3
"""P0-P3 shareable_thought + key_concept cleanup."""

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
MAX_SHAREABLE = 130
MIN_EXPAND = 40

# P0 + P1 hand-tuned fixes
NOTE_FIXES: dict[str, dict[str, object]] = {
    "composure.md": {
        "key_concept": (
            "Steady tone and pace when the room isn't - people read calm as competence.\n\n"
            "One beat before I reply often beats matching their volume.\n\n"
            "Composure isn't suppressing the reaction - it's choosing which one gets shown.\n\n"
            "The composure has to be visible - a calm voice with shaking hands under the table still reads as calm to everyone watching."
        ),
        "shareable_thought": [
            "Composure is steady voice and pace when the room isn't - people read calm as competence.",
            "One beat before I reply often beats matching their volume.",
            "Composure isn't suppressing the reaction - it's choosing which one gets shown.",
            "The composure has to be visible - a calm voice with shaking hands under the table still reads as calm to everyone watching.",
        ],
    },
    "signal-vs-noise.md": {
        "key_concept": (
            "I save only what changes what I do or believe this month - most content is noise.\n\n"
            "Admiring an article without a behavior change is entertainment, not signal.\n\n"
            "The filter is simple: would I act or cite this within thirty days?\n\n"
            "Most feeds are noise until proven otherwise."
        ),
        "shareable_thought": [
            "I save only what changes what I do or believe this month - most feeds are noise.",
            "Admiring an article without a behavior change is entertainment, not signal.",
            "The filter is simple: would I act or cite this within thirty days?",
            "Most feeds are noise until proven otherwise.",
        ],
    },
    "complete-the-cycle.md": {
        "key_concept": (
            "The meeting isn't done until recap, owners, dates, and verification close the loop.\n\n"
            "A decision without an owner and a date is still just talk - execution is where the loop actually starts.\n\n"
            "Mistakes need correction, not ceremony - fix the process or the miss comes back next week.\n\n"
            "Verification closes the loop - if nobody checks it landed, the cycle never really finished."
        ),
        "shareable_thought": [
            "The meeting isn't done until recap, owners, dates, and verification close the loop.",
            "A decision without an owner and a date is still just talk - execution is where the loop actually starts.",
            "Mistakes need correction, not ceremony - fix the process or the miss comes back next week.",
            "Verification closes the loop - if nobody checks it landed, the cycle never really finished.",
        ],
    },
    "inbox-zero.md": {
        "key_concept": (
            "I process the inbox to empty each week - decide, don't hoard.\n\n"
            "Process the inbox to empty regularly - each item decided, not hoarded.\n\n"
            "Zero isn't vanity - it's proof the capture system still works when Monday doesn't start with dread.\n\n"
            "Empty the capture pipe on schedule, or ideas retreat back into my head."
        ),
        "shareable_thought": [
            "I process the inbox to empty each week - decide, don't hoard.",
            "Each item gets decide, delete, or defer - not another week in the pile.",
            "Zero isn't vanity - it's proof the capture system still works.",
            "If I won't empty the inbox, I stop trusting it and hoard in my head instead.",
        ],
    },
    "expect-the-counter.md": {
        "key_concept": (
            "I plan what happens after the other side adapts, not just how my opening move looks on paper.\n\n"
            "The opening move isn't the game - they adapt, and I need a second plan ready.\n\n"
            "Rehearse the second move before tip-off, not only the play that looks good on paper.\n\n"
            "Don't cling to a tactic because it worked once - that's when the counter hurts most."
        ),
        "shareable_thought": [
            "I plan what happens after the other side adapts, not just how my opening move looks on paper.",
            "The opening move isn't the game - they adapt, and I need a second plan ready.",
            "Rehearse the second move before tip-off, not only the play that looks good on paper.",
            "Don't cling to a tactic because it worked once - that's when the counter hurts most.",
        ],
    },
    "the-feynman-technique.md": {
        "key_concept": (
            "I teach the idea out loud to a blank page - wherever I stumble, I don't understand yet.\n\n"
            "Explain it simply to a blank page - the stumble marks the gap.\n\n"
            "A blank page is the honest audience - no jargon to hide behind.\n\n"
            "Teach-it-to-learn-it keeps evergreen notes honest before I link them."
        ),
        "shareable_thought": [
            "I teach the idea out loud to a blank page - wherever I stumble, I don't understand yet.",
            "Explain it simply to a blank page - the stumble marks the gap.",
            "A blank page is the honest audience - no jargon to hide behind.",
            "Teach-it-to-learn-it keeps evergreen notes honest before I link them.",
        ],
    },
    "synthesis-as-a-goal.md": {
        "key_concept": (
            "I merge sources into what I believe and can defend - a quote pile isn't the goal.\n\n"
            "Collecting quotes isn't PKM for me - belief has to live in prose I can defend.\n\n"
            "Synthesis is when learning starts - merge sources into one claim I'd ship.\n\n"
            "The wiki can hold borrowed lines; I still owe one page in my own words."
        ),
        "shareable_thought": [
            "I merge sources into what I believe and can defend - a quote pile isn't the goal.",
            "Collecting quotes isn't PKM for me - belief has to live in prose I can defend.",
            "Synthesis is when learning starts - merge sources into one claim I'd ship.",
            "The wiki can hold borrowed lines; I still owe one page in my own words.",
        ],
    },
    "free-grace.md": {
        "key_concept": (
            "[[Grace]] is a gift I never earned - unmerited favor (Ephesians 2:8-9; John 3:16; Romans 4:5).\n\n"
            "Christ paid what I couldn't. I receive eternal life by believing His promise - not by climbing a moral ladder. Same shape as [[Minimum Effective Dose]] for salvation: faith is the smallest act that still works - not zero effort, not a lifetime of merit. Every [[Eternal Principles]] Jesus taught flows from that ground: principles for how believers live in grateful response, pursue fellowship with God, and store up [[Eternal Rewards]] - never as currency to buy heaven. [[Loss of Reward]] keeps the categories straight when a believer wastes years or worthless works burn: salvation stays on Christ, reward may shrink. Ephesians 2:10 keeps the order straight: saved by grace through faith first, then created in Christ Jesus for good works. [[Justification]] is free and finished at faith; [[Sanctification]], [[Discipleship]], and forgiveness toward others belong to the walk after. [[Grateful Obedience]] names the posture: obey from thanks, not to qualify. [[Assurance]] and [[Standing vs Fellowship]] keep doubt from collapsing standing with closeness. [[Faith and Works]] keeps the lanes straight: works prove faith alive, they don't buy heaven."
        ),
        "shareable_thought": [
            "Eternal life is Christ's gift received by faith alone, not wages for commandments, principles, or good works.",
            "Grace is a gift I never earned - Christ paid what I couldn't.",
            "Good works prove faith is alive - they never buy the ticket to heaven.",
            "Faith is the smallest act that still works - not a lifetime of merit stacked on top.",
        ],
    },
    "gentleness.md": {
        "key_concept": (
            "[[Fruits of the Spirit]] lists gentleness beside patience and self-control - power restrained, not power absent. (Galatians 5:22). [[Humility and Service]] is the garden echo: greatness is serving, not being served; the Son washed feet the night before the cross. [[Listen Before Fixing]] is gentleness in conversation - hear before you prescribe. [[The Beatitudes]] bless the meek - strength without grasping for status.\n\n"
            "Gentleness fruit is strength held back on purpose, not weakness or loud correction that skips love."
        ),
        "shareable_thought": [
            "Gentleness fruit is strength held back on purpose, not weakness or loud correction that skips love.",
            "Gentleness is power restrained, not power absent - Galatians 5:22 names it beside patience.",
            "The Beatitudes bless the meek - strength without grasping for status.",
            "Hear before you prescribe - loud correction without love isn't Spirit-grown gentleness.",
        ],
    },
    "backlinks.md": {
        "key_concept": (
            "Find anchor notes by who links here - snippet context per backlink, not just a count.\n\n"
            "Utility surface: link by URL from content notes, not `[[wikilinks]]`."
        ),
        "shareable_thought": [
            "Inbound wikilinks ranked by count - see which notes the garden treats as anchors.",
            "Find anchor notes by who links here - snippet context per backlink, not just a count.",
            "Utility surface: link by URL from content notes, not wikilinks.",
            "Anchor notes are the ones other notes link to most - rank by inbound count.",
        ],
    },
    "faithful-steward.md": {
        "key_concept": (
            "[[Free Grace]] settled where I spend forever.\n\n"
            "Stewardship settles what I do with what He entrusted after. The master returns to settle accounts - faithful use repaid, buried talent rebuked. [[Eternal Rewards]] names the promise; [[Faithful Steward]] names the parable Jesus told for it. [[Compounding]] is the PKM mirror: small faithful use over years, not one heroic week mistaken for a merit purchase on heaven. [[Judgment Seat]] is where accounts get reviewed; [[Secret Devotion]] and [[Integrity Without an Audience]] are hidden lanes of faithful use nobody applauded.\n\n"
            "After salvation is settled, stewardship is about faithful use of what God entrusted, not buying heaven with busy weeks."
        ),
        "shareable_thought": [
            "After salvation is settled, stewardship is about faithful use of what God entrusted, not buying heaven with busy weeks.",
            "Free Grace settled where I spend forever - stewardship is what I do with what He entrusted after.",
            "The master returns to settle accounts - faithful use repaid, buried talent rebuked.",
            "Quiet Tuesdays nobody applauded still count when the gift was used faithfully.",
        ],
    },
}

# P2: expand known short stubs to full standalone lines
STUB_EXPANSIONS: dict[str, str] = {
    "Break the escalation cycle.": "Break the escalation cycle - don't match tone for tone when a sharp email lands.",
    "Inbound wikilinks ranked by count.": "Inbound wikilinks ranked by count - see which notes the garden treats as anchors.",
    "Find anchor notes by who links here.": "Find anchor notes by who links here - snippet context per backlink, not just a count.",
    "A meeting needs follow-up.": "A meeting needs follow-up - recap, owners, and dates before anyone leaves the room.",
    "A decision needs execution.": "A decision needs execution - an owner and a date, or it's still just talk.",
    "A mistake needs correction.": "A mistake needs correction - fix the process or the miss comes back next week.",
    "The composure has to be visible.": "The composure has to be visible - calm voice with shaking hands still reads as calm to everyone watching.",
    "Friction kills capture.": "Friction kills capture - if saving takes three taps, the idea dies before the inbox.",
    "No party gets my soul.": "No party gets my soul - Caesar gets what Caesar is owed, God gets what I'm His.",
    "My head is for thinking, not storing.": "My head is for thinking, not storing - notes hold what I'd otherwise lose.",
    "Notes hold what I'd otherwise lose.": "Notes hold what I'd otherwise lose - capture is how ideas survive the week.",
    "Process the inbox to empty regularly.": "Process the inbox to empty regularly - each item decided, not hoarded.",
    "Each item decided, not hoarded.": "Each item gets decide, delete, or defer - not another week in the pile.",
    "Empty the capture pipe on schedule.": "Empty the capture pipe on schedule, or ideas retreat back into my head.",
    "The opening move isn't the game.": "The opening move isn't the game - they adapt, and I need a second plan ready.",
    "I rehearse what happens after they adapt.": "I rehearse what happens after they adapt - not only the play that looks good on paper.",
    "Rehearse the second move before tip-off.": "Rehearse the second move before tip-off, not only the play that looks good on paper.",
    "Explain it simply to a blank page.": "Explain it simply to a blank page - wherever I stumble, I don't understand yet.",
    "A quote pile isn't the goal.": "A quote pile isn't the goal - merge sources into what I believe and can defend.",
    "Collecting quotes isn't PKM for me.": "Collecting quotes isn't PKM for me - belief has to live in prose I can defend.",
    "Synthesis is when learning starts.": "Synthesis is when learning starts - merge sources into one claim I'd ship.",
    "Grace is a gift I never earned.": "Grace is a gift I never earned - Christ paid what I couldn't.",
    "Christ paid what I couldn't.": "Christ paid what I couldn't - I receive eternal life by believing His promise.",
    "Free Grace settled where I spend forever.": "Free Grace settled where I spend forever - stewardship is what I do with what He entrusted after.",
    "The master returns to settle accounts.": "The master returns to settle accounts - faithful use repaid, buried talent rebuked.",
    "Faithful use repaid, buried talent rebuked.": "Faithful use gets repaid; buried talent gets rebuked when the gift was never used.",
    "Fruits of the Spirit lists gentleness beside patience and self-control.": "Fruits of the Spirit lists gentleness beside patience and self-control in one cluster.",
    "The Beatitudes bless the meek.": "The Beatitudes bless the meek - strength without grasping for status.",
    "Power restrained, not power absent. (Galatians 5:22).": "Gentleness is power restrained, not power absent - Galatians 5:22 names it beside patience.",
    "Unmerited favor (Ephesians 2:8-9; John 3:16; Romans 4:5).": "Grace is unmerited favor - Ephesians 2:8-9 says the gift was never wages for works.",
    "One claim I'd say out loud.": "One claim I'd say out loud - if a note needs three ands, I split it before I link it.",
    "Too many ands, split it.": "Too many ands in one note means I split it before I link it.",
    "If I'm not paying, I'm the product.": "If I'm not paying, I'm the product - the feed sells my attention, not the article.",
    "Platforms compete for your focus.": "Platforms compete for your focus - I treat the feed like a slot machine someone else owns.",
    "Stop throwing anger after sunk hurt.": "Stop throwing anger after sunk hurt - break the loop before tone for tone takes over.",
    "Learn less, retain longer, apply more.": "Learn less, retain longer, apply more - cards exist so the right move loads when life shows up.",
    "Faith alone saves me.": "Faith alone saves me - good works follow, they never buy the ticket.",
    "Steady use of what God entrusted.": "Steady use of what God entrusted - faithful over years, not one heroic week on the report card.",
    "CMS doesn't add a database.": "A git CMS doesn't add a database - it commits markdown the same push-live build already uses.",
    "Maintenance targets, not vanity metrics.": "Read the graph for maintenance targets, not vanity metrics on link count.",
    "Top 20% = most total wikilinks.": "The top twenty percent by wikilinks are the anchors worth pruning around.",
    "Growth mindset treats ability as trainable.": "Growth mindset treats ability as trainable - mistakes are data, not a fixed label.",
    "I'm bad at this\" is a verdict.": "Saying \"I'm bad at this\" is a verdict - \"I missed three\" is data I can train on.",
    "I missed three\" is data.": "Saying \"I missed three\" is data - ability is trainable when I treat the miss as feedback.",
    "A quote pile isn't the goal.": "A quote pile isn't the goal - merge sources into what I believe and can defend.",
}

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")


def norm(text: str) -> str:
    text = WIKILINK.sub(r"\1", text.lower())
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def plain(text: str) -> str:
    return WIKILINK.sub(r"\1", text)


def paragraphs(key: str) -> list[str]:
    return [p.strip() for p in key.strip().split("\n\n") if p.strip()]


def dedupe_key_concept(fm: dict) -> str:
    key = fm.get("key_concept")
    if not isinstance(key, str) or not key.strip():
        return key or ""
    desc = fm.get("description") if isinstance(fm.get("description"), str) else ""
    shareable = fm.get("shareable_thought") if isinstance(fm.get("shareable_thought"), list) else []
    share_norms = {norm(s) for s in shareable if isinstance(s, str)}
    desc_norm = norm(desc)

    parts = paragraphs(key)
    if not parts:
        return key

    kept: list[str] = []
    seen: set[str] = set()

    for i, part in enumerate(parts):
        n = norm(part)
        if not n or n in seen:
            continue
        has_links = "[[" in part
        is_long = len(part) > 140
        is_shareable_echo = n in share_norms
        is_desc_echo = n == desc_norm

        # ponytail: keep punch + wikilink expansion; drop trailing shareable/desc echoes
        if i == 0:
            kept.append(part)
            seen.add(n)
            continue
        if has_links or is_long:
            if n not in seen:
                kept.append(part)
                seen.add(n)
            continue
        if is_shareable_echo or is_desc_echo:
            continue
        if n not in seen:
            kept.append(part)
            seen.add(n)

    return "\n\n".join(kept)


def expand_shareable_line(line: str, fm: dict) -> str:
    line = line.strip()
    if len(line) >= MIN_EXPAND:
        return line
    if line in STUB_EXPANSIONS:
        return STUB_EXPANSIONS[line]
    key = fm.get("key_concept") if isinstance(fm.get("key_concept"), str) else ""
    for part in paragraphs(key):
        plain_part = plain(part)
        if len(plain_part) >= MIN_EXPAND and norm(line) in norm(plain_part):
            candidate = plain_part if "[[" not in plain_part else plain(part)
            if len(candidate) <= MAX_SHAREABLE and gets_point_across(candidate):
                return candidate
    return line


def pad_shareable_to_four(fm: dict, lines: list[str]) -> list[str]:
    import importlib

    seed = importlib.import_module("seed-note-shareable-thought")
    out = list(lines)
    for line in seed.draft_shareable_thought(fm):
        if len(out) >= 4:
            break
        if any(shareable_lines_overlap(line, x) for x in out):
            continue
        out.append(line)
    for part in paragraphs(fm.get("key_concept") or ""):
        if len(out) >= 4:
            break
        plain_part = plain(part)
        if len(plain_part) > MAX_SHAREABLE or "[[" in plain_part:
            continue
        if any(shareable_lines_overlap(plain_part, x) for x in out):
            continue
        if gets_point_across(plain_part):
            out.append(plain_part)
    return out[:4]


def expand_shareable_thought(fm: dict) -> list[str]:
    lines = fm.get("shareable_thought")
    if not isinstance(lines, list):
        return lines
    out: list[str] = []
    for line in lines:
        if not isinstance(line, str):
            continue
        expanded = expand_shareable_line(line, fm)
        if len(expanded) > MAX_SHAREABLE:
            expanded = expanded[: MAX_SHAREABLE - 1].rstrip() + "."
        if any(shareable_lines_overlap(expanded, x) for x in out):
            continue
        if gets_point_across(expanded):
            out.append(expanded)
    if len(out) < 4:
        out = pad_shareable_to_four(fm, out)
    return out[:4]


def incorporate_shareables(fm: dict) -> None:
    key = fm.get("key_concept") if isinstance(fm.get("key_concept"), str) else ""
    parts = paragraphs(key)
    key_norm = norm("\n\n".join(parts))
    for line in fm.get("shareable_thought") or []:
        if isinstance(line, str) and norm(line) not in key_norm:
            parts.append(line)
            key_norm = norm("\n\n".join(parts))
    # final dedupe inside key
    seen: set[str] = set()
    final: list[str] = []
    for p in parts:
        n = norm(p)
        if n in seen:
            continue
        seen.add(n)
        final.append(p)
    fm["key_concept"] = "\n\n".join(final)


def apply_manual_fixes() -> int:
    changed = 0
    for name, patch in NOTE_FIXES.items():
        path = NOTES / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        for key, val in patch.items():
            fm[key] = val
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def apply_p2_p3() -> tuple[int, int]:
    p2 = p3 = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP or path.name in NOTE_FIXES:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue

        old_key = fm.get("key_concept", "")
        fm["key_concept"] = dedupe_key_concept(fm)
        if fm["key_concept"] != old_key:
            p3 += 1

        old_share = fm.get("shareable_thought")
        fm["shareable_thought"] = expand_shareable_thought(fm)
        if fm["shareable_thought"] != old_share:
            p2 += 1

        incorporate_shareables(fm)

        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
    return p2, p3


def finalize_all() -> int:
    import importlib

    seed = importlib.import_module("seed-note-shareable-thought")
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        lines = fm.get("shareable_thought")
        if not isinstance(lines, list) or len(lines) != 4:
            fm["shareable_thought"] = seed.draft_shareable_thought(fm)
        incorporate_shareables(fm)
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    manual = apply_manual_fixes()
    p2, p3 = apply_p2_p3()
    # Re-apply manual P0/P1 after bulk pass, then incorporate + pad all notes.
    manual_again = apply_manual_fixes()
    finalized = finalize_all()
    for name in NOTE_FIXES:
        path = NOTES / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        patch = NOTE_FIXES[name]
        for key, val in patch.items():
            fm[key] = val
        incorporate_shareables(fm)
        path.write_text(f"---\n{dump_frontmatter(fm)}\n---{body}", encoding="utf-8")
    print(f"P0/P1 manual fixes: {manual}")
    print(f"P2 shareable expansions: {p2}")
    print(f"P3 key_concept dedupes: {p3}")
    print(f"P0/P1 re-applied: {manual_again}")
    print(f"Finalized notes: {finalized}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
