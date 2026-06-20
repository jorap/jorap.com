#!/usr/bin/env python3
"""Rewrite flashcard pairs: cue → apply, front longer than back."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

# slug -> list of (front, back) - life's cue on front; immediate move on back
REWRITES: dict[str, list[tuple[str, str]]] = {
    "capture": [
        (
            "Mid-commute spark I might forget. First move - drop in one inbox, or organize into folders on the spot?",
            "Drop in one inbox. Don't organize yet.",
        ),
        (
            "Thumb hovering over save on an interesting link I'm unsure about. One question before it hits the inbox?",
            "Would I act on it or cite it later?",
        ),
        (
            "Ideas keep dying before they reach the inbox - friction somewhere. First fix I try?",
            "Simplify to one pipe.",
        ),
        (
            "Tempted to split work and home into two capture inboxes. Merge into one pipe, or keep separate?",
            "Merge - one pipe.",
        ),
        (
            "Friday review and raw captures still sitting unprocessed. Leave them where until I process?",
            "Still in the inbox.",
        ),
        (
            "Something lands and I want to tag and file immediately. Where do I actually stop?",
            "Stop at inbox. Organize later.",
        ),
    ],
    "free-grace": [
        (
            "Friend at coffee lists good deeds as their heaven ticket. What do I trust for eternal life?",
            "Christ's promise - grace through faith.",
        ),
        (
            "Good week makes me feel qualified for heaven. Correct the order in my head - what saves, what follows?",
            "Faith saves first. Obedience follows.",
        ),
        (
            "Head says I must perform before God accepts me. Turn from that - what's the entry point?",
            "Trust Christ - not my performance.",
        ),
        (
            "Tempted to list my works when someone asks how to be saved. Lead with what?",
            "Grace through faith in Christ.",
        ),
        (
            "Someone says they earned God's favor by trying hard. One sentence I'd say back?",
            "Unmerited - Christ paid what I couldn't.",
        ),
        (
            "Obedience after conversion - am I paying for heaven or living gratefully?",
            "Live gratefully - grace already saved.",
        ),
    ],
    "love-god": [
        (
            "Sunday worship felt high but I haven't opened the Bible all week. Which part of whole-person love am I skipping?",
            "Mind - open Scripture today.",
        ),
        (
            "Calendar full, prayer thin - reordering the day. What comes first?",
            "Love God first - pray before inbox.",
        ),
        (
            "Church checkbox ticked, heart still elsewhere. Move from compliance to what?",
            "Grateful response - engage heart.",
        ),
        (
            "About to snap at family right after worship. Which love comes first at home?",
            "Love God first - then neighbor.",
        ),
        (
            "Morning fork: scroll or five minutes with God. One faculty to feed right now?",
            "Pick one - heart, soul, mind, or strength.",
        ),
        (
            "Devotion feels vague - 'love God' with no next step. What's one move today?",
            "Pray, read, or serve - one faculty.",
        ),
    ],
    "love-your-neighbor": [
        (
            "Neighbor I'd rather avoid lives next door. Do they count - likability, or proximity and need?",
            "Show mercy - proximity counts.",
        ),
        (
            "Deciding how much help to give someone hard to love. What standard do I use?",
            "Care I'd want if roles reversed.",
        ),
        (
            "Worship felt fine but I'm snapping at family tonight. Which paired loves am I splitting?",
            "Stop splitting - love both today.",
        ),
        (
            "Walking past someone hurt on the road - shared ethnicity or mercy defines neighbor?",
            "Act with mercy - that's neighbor.",
        ),
        (
            "They wronged me - withholding help until they're nicer. What do I do?",
            "Love as yourself - go first.",
        ),
        (
            "Mental loop: do they qualify as neighbor? Flip the question - what do I ask instead?",
            "Am I being neighbor to them?",
        ),
    ],
    "the-golden-rule": [
        (
            "Thumb on post button, public critique loaded. One check before I hit send?",
            "Reverse roles - would I want this said to me?",
        ),
        (
            "Waiting for fair treatment before I act well toward someone. Who moves first?",
            "I go first - treat as I'd want.",
        ),
        (
            "About to deliver hard truth with a harsh tone. How should I speak it?",
            "As I'd want it spoken - in love.",
        ),
        (
            "Tempted to just avoid harm and skip doing good. What's the active move?",
            "Do good - not only avoid harm.",
        ),
        (
            "Ethical fork, no rulebook handy. One experiential check before I act?",
            "How would I want to be treated?",
        ),
        (
            "Criticism is true but tone is cruel. Say it anyway, or pause?",
            "Pause - reverse roles first.",
        ),
    ],
    "love-your-enemies": [
        (
            "Someone slandered me online - outrage rising. Outrage, silence, or prayer first?",
            "Pray for them.",
        ),
        (
            "Only loving people who love me back. What's my standard - tax-collector level or higher?",
            "Higher - bless enemies too.",
        ),
        (
            "Enemy hurt me - tempted to agree just to keep peace. Pretend it didn't happen?",
            "No - bless and pray; don't return evil.",
        ),
        (
            "Returning evil for evil feels justified right now. What's the break-the-cycle move?",
            "Bless - don't return evil.",
        ),
        (
            "Persecutors keep coming - tempted to retaliate. Practical handle besides not hitting back?",
            "Love, bless, pray for them.",
        ),
        (
            "Sun and rain on wicked and righteous - what do I copy toward my persecutors?",
            "Father's kindness - bless both kinds.",
        ),
    ],
    "forgiveness": [
        (
            "Praying but nursing a grudge - skipping the line about others. Say it now?",
            "Forgive those who trespass against us.",
        ),
        (
            "Wronged and refusing to forgive. Does that undo salvation or break fellowship?",
            "Breaks fellowship - forgive from the heart.",
        ),
        (
            "Same person hurt me again - tempted to stop counting. Forgive again or close the ledger?",
            "Forgive again - stop counting.",
        ),
        (
            "Hurt still stings - forgiving feels like pretending it didn't matter. True or false?",
            "False - release debt anyway.",
        ),
        (
            "Repeat offender apologizes again. Forgive with boundaries, or enable the pattern?",
            "Forgive heart; keep boundaries.",
        ),
        (
            "I was forgiven much but choking someone over pocket change. What's my move?",
            "Forgive - release the small debt.",
        ),
    ],
    "seek-the-kingdom-first": [
        (
            "Anxiety scrolling finances before I've prayed. Seek what first - then let needs follow?",
            "Kingdom first - pray, then act.",
        ),
        (
            "Calendar filled before I opened Scripture this week. Reorder - what comes first?",
            "Kingdom first - Scripture before inbox.",
        ),
        (
            "Tuesday 7am, inbox calling before work. One move that puts God's reign first?",
            "Scripture or prayer before inbox.",
        ),
        (
            "Work hustle and Sunday worship pulling opposite directions - two masters. Pick which?",
            "God - not mammon.",
        ),
        (
            "Wallet and calendar both pulling hard. Which leads - money or heart?",
            "Move treasure - heart follows.",
        ),
        (
            "Treating kingdom life like something I must earn. Receive first, or perform first?",
            "Receive by faith - then live it.",
        ),
    ],
    "repent-and-believe": [
        (
            "Delaying faith until my habits improve. Enter when - when fixed, or today?",
            "Today - by faith, not when fixed.",
        ),
        (
            "Someone groveling until they feel good enough for God. One sentence I'd say?",
            "Turn from self-trust - not merit.",
        ),
        (
            "Head agrees with gospel facts but life unchanged. Enough assent, or must I rely on Christ?",
            "Rely on Christ's promise - trust.",
        ),
        (
            "Trying to obey my way into eternal life. What receives life vs what guides after?",
            "Repent/believe receives. Obedience guides after.",
        ),
        (
            "Same sin again - despair that heaven is lost. Turn again means re-earn, or restore?",
            "Restore fellowship - not re-earn heaven.",
        ),
        (
            "Waiting until I'm worthy to enter. Enter someday, or by faith today?",
            "Enter by faith today.",
        ),
    ],
    "ask-seek-knock": [
        (
            "Email and inbox before any quiet time with God most mornings. How keep approaching the Father?",
            "Ask, seek, knock - keep coming.",
        ),
        (
            "Prayer feels like earning answers by performance. Come as wage earner or child?",
            "Child asking a parent.",
        ),
        (
            "Asked for something harmful - bitter God didn't comply. What does a wise Father give?",
            "What's good - not always what I asked.",
        ),
        (
            "Rushing through the Lord's Prayer to daily bread. Whose name, kingdom, will first?",
            "Father's name, kingdom, will first.",
        ),
        (
            "Praying where people can notice me. Who is the real audience?",
            "The Father alone.",
        ),
        (
            "Know the words by heart but haven't opened Scripture in a week. Besides asking, what do I do?",
            "Seek in Scripture - open the Book.",
        ),
    ],
    "take-up-your-cross": [
        (
            "Comfortable faith - avoiding the hard obedience I heard preached. Count cost or stay comfortable?",
            "Count cost - deny self, follow daily.",
        ),
        (
            "Cross-bearing to feel saved or earn heaven. Earn salvation or shape life after faith?",
            "Shape discipleship - grace already saved.",
        ),
        (
            "One big surrender last year, same sin pattern today. One heroic moment or daily posture?",
            "Daily - pick up cross again today.",
        ),
        (
            "Clutching comfort when obedience will cost me something today. Save my life or lose it for his sake?",
            "Lose it for his sake - follow behind.",
        ),
        (
            "Choosing scroll over the costly obedience I know is next. Deny self or indulge?",
            "Deny self - follow him today.",
        ),
        (
            "Heard the hard teaching, unchanged how I treat people. What's missing - hear or do?",
            "Do what he said - act today.",
        ),
    ],
    "abide-in-me": [
        (
            "Trying harder at fruit - more service, less sin - but feeling dry inside. Where does fruit come from?",
            "Stay connected - fruit from the vine.",
        ),
        (
            "No prayer or Scripture all week - patience snapped at someone. Apart from the vine, what can I produce?",
            "Nothing good - reconnect now.",
        ),
        (
            "Pruning hurts - fear God revoked my place. Does pruning revoke salvation or refine connection?",
            "Refines - stay grafted, bear fruit.",
        ),
        (
            "Self-help spiritual growth plan vs staying connected. Willpower alone or receive from the vine?",
            "Receive - drop willpower alone.",
        ),
        (
            "Morning fork: scroll news or five minutes in Scripture. First move to stay connected?",
            "Scripture and prayer - connect first.",
        ),
        (
            "Prayers feel misaligned with God's will. Besides staying connected, what must dwell in me?",
            "His words - read Scripture.",
        ),
    ],
    "the-wise-builder": [
        (
            "Heard the Sermon preached many times - how I treat people unchanged. What's missing?",
            "Do one command today - not hear only.",
        ),
        (
            "Storm of job loss or betrayal hits hard. What reveals rock vs sand under me?",
            "Obedience under stress - not just hearing.",
        ),
        (
            "Can quote the hard commands on money and enemies but skip them. Lip service or obey?",
            "Obey the hard commands - today.",
        ),
        (
            "Bible study Monday, same gossip Tuesday. Which builder am I being?",
            "Do what he said - match hearing.",
        ),
        (
            "Faith saved me but hearing feels empty. What proves genuine hearing?",
            "Act - obey one command.",
        ),
        (
            "Saved sermons and notes but no obedience showing up. One move I take today?",
            "Obey one command Jesus gave.",
        ),
    ],
    "pareto-principle": [
        (
            "Task board and reading list both screaming urgent. Protect which slice - roughly what percent moved the needle?",
            "The vital ~20%.",
        ),
        (
            "Review deck bloated to forty notes - skipping drills. Trim to what fraction of the garden?",
            "~20% spine - weekly habits only.",
        ),
        (
            "Everything feels equally important and nothing moves. What's the move on the long tail?",
            "Cut polish on the rest.",
        ),
        (
            "Found the vital few tasks that matter. After that, what do I protect?",
            "That slice - stop polishing the rest.",
        ),
        (
            "Polishing the long tail while the vital few stall. Stop polishing or keep equal effort?",
            "Protect the vital few - cut tail polish.",
        ),
        (
            "Someone treats 80/20 as physical law. Correct them - math homework or shorthand?",
            "Shorthand ratio - not a law.",
        ),
    ],
    "note-relationships": [
        (
            "New note builds on an older atomic claim - typing the link in the body now. Which label?",
            "Extends.",
        ),
        (
            "Naming the tradeoff against a slower-work philosophy in this note. Which typed link?",
            "Contradicts.",
        ),
        (
            "Weekly checklist makes a review habit real in practice. Extends the idea or implements it?",
            "Implements.",
        ),
        (
            "Hub page gathering twenty related notes into one index. Which relationship type?",
            "Index (MOC).",
        ),
        (
            "Atomic note ready to publish - minimum typed links before filing. How many extends and contradicts?",
            "One extends, one contradicts.",
        ),
        (
            "Two tools solve the same job - picking one for this note. Which relationship type?",
            "Alternative.",
        ),
    ],
    "associative-linking": [
        (
            "Just finished a new atomic note - filing it now. Minimum typed links before it's garden-ready?",
            "Add one extends, one contradicts.",
        ),
        (
            "Naming the tradeoff against slow productivity in the body. Which link type captures the push?",
            "Contradicts.",
        ),
        (
            "Tempted to file by folder tree only and skip wikilinks. Folders sort - what thinks?",
            "Links think - add wikilinks.",
        ),
        (
            "Six months later I remember the filename but not the idea. What should I have done while writing?",
            "Link while writing - filenames fade.",
        ),
        (
            "Perfect folder tree but zero wikilinks in the body. Can the garden be walked?",
            "No - add links, not taxonomy.",
        ),
        (
            "Atomic note has extends but no contradicts - optional polish or minimum?",
            "Minimum - add one contradicts.",
        ),
    ],
    "atomic-notes": [
        (
            "Draft mixes browser tips AND meeting notes in one file. Split into two notes, or keep as one?",
            "Split - one claim per note.",
        ),
        (
            "Can't say the whole note in one breath without using 'and'. Split or keep?",
            "Split into atomic notes.",
        ),
        (
            "Three ideas under one heading in a single file. Three wikilinks, or one long file?",
            "Split - three wikilinks.",
        ),
        (
            "Note reads like a mini blog post with multiple sections. Trim or split?",
            "Split - one citable claim.",
        ),
        (
            "Tempted to organize with headings inside one file instead of links. What do I use?",
            "Wikilinks between notes.",
        ),
        (
            "Can't link to one idea buried in a kitchen-sink note. What's the fix?",
            "Split it - not atomic yet.",
        ),
    ],
    "building-a-second-brain": [
        (
            "New to CODE and overwhelmed - capture, organize, distill, express. Which step first?",
            "Capture first - offload now.",
        ),
        (
            "Notes pile up but nothing publishes. Which step is failing - schedule what?",
            "Express - schedule ship.",
        ),
        (
            "Organize step uses projects, areas, resources, archive. Name the acronym?",
            "PARA.",
        ),
        (
            "Skipped capture and jumped straight to folders and tags. What order did I violate?",
            "Capture before organize.",
        ),
        (
            "Second brain filling with interesting links - hoard or ship?",
            "Ship output - not hoard.",
        ),
        (
            "Tempted to publish raw captures without distilling. Ship raw only, or distill first?",
            "Distill first - then express.",
        ),
    ],
    "evergreen-notes": [
        (
            "Fleeting spark keeps showing up in weekly review. Promote to evergreen, or leave fleeting?",
            "Promote - if two-year bar passes.",
        ),
        (
            "Tool I rely on changed how I work - trending spike on Twitter. Revise note on every spike?",
            "Revise when still true - ignore hype.",
        ),
        (
            "Sentences might not hold in two years. Evergreen or keep fleeting?",
            "Keep fleeting - or rewrite first.",
        ),
        (
            "I'd cite this in conversation later this year. Evergreen bucket, or fleeting?",
            "Evergreen if cite-later; else fleeting.",
        ),
        (
            "Trendy take I might regret next year. Evergreen it now, or wait?",
            "Wait - keep fleeting.",
        ),
        (
            "Evergreen note has bold layers but no claim I'd quote. Publish as-is or distill?",
            "Distill - need one citable claim.",
        ),
    ],
    "signal-vs-noise": [
        (
            "Interesting article but it won't change what I do this month. Save it, or admire and move on?",
            "Admire and move on - don't save.",
        ),
        (
            "Thumb on save - one filter question about action or belief before I commit?",
            "Change action or belief this month?",
        ),
        (
            "Saving everything just in case - hoarding bookmarks with no output. What's the drift?",
            "Collector's Fallacy - skip the save.",
        ),
        (
            "Trending thread everyone bookmarks. Noise unless it changes what this month?",
            "Skip - noise this month.",
        ),
        (
            "Good content, wrong month, no action hook. Trophy case, or skip the save?",
            "Skip the save.",
        ),
        (
            "Capture filter needs a time window on action or belief. How tight?",
            "This month - not someday.",
        ),
    ],
    "the-collectors-fallacy": [
        (
            "Reading list grows but nothing ships. One question before every save?",
            "What will I make with this?",
        ),
        (
            "No planned creative output tied to this save. Save anyway, or skip?",
            "Skip - don't save it.",
        ),
        (
            "Finished the article and filed it - feels like learning. Does it count yet?",
            "Not yet - ship or rewrite first.",
        ),
        (
            "Hoarded bookmarks everywhere with no deadline. Tie every save to what?",
            "An express deadline.",
        ),
        (
            "Saving articles feels like learning. When does learning actually start?",
            "When something leaves the notebook.",
        ),
        (
            "Bookmark folder growing again - can only ask one question before save. Which?",
            "What will I make with this?",
        ),
    ],
    "the-trusted-inbox": [
        (
            "Forty inbox items untouched two weeks. Trust is broken - recovery move today?",
            "Empty it now. Same day weekly.",
        ),
        (
            "Friday review starting - step one before calendar or projects?",
            "Empty the Trusted Inbox first.",
        ),
        (
            "Items rotting without weekly processing - occasional misses or rot kills trust faster?",
            "Rot kills trust - empty weekly.",
        ),
        (
            "Mid-day an inbox item screams for a project folder. File now, or wait for review?",
            "Wait - break flow if I file now.",
        ),
        (
            "Two inboxes for work and home - merge into one pipe, or keep separate?",
            "Merge - one pipe.",
        ),
        (
            "I tag and label but the inbox never empties. Trusted?",
            "No - empty means delete or file out.",
        ),
    ],
    "weekly-review-checklists": [
        (
            "Friday review - inbox and calendar done. Fourth step before I close?",
            "Pick one ship action.",
        ),
        (
            "Review feels stale - tempted to reinvent the checklist for creativity. Reinvent or keep boring?",
            "Keep same checklist - boring on purpose.",
        ),
        (
            "Finished inbox and calendar but skipping express. Required before I close review?",
            "Pick one ship action.",
        ),
        (
            "Travel week - review might get skipped entirely. Twenty minutes or zero?",
            "Twenty minutes - shorten, don't skip.",
        ),
        (
            "When do I run weekly review - whenever I remember, or same day every week?",
            "Same day every week.",
        ),
        (
            "Step three after inbox and calendar - what do I review next?",
            "Active projects - stuck and next.",
        ),
    ],
    "para-method": [
        (
            "Active work with a deadline just landed in my notes. Which bucket - and if I don't name it?",
            "Projects - or it stays Resources.",
        ),
        (
            "Reference material with no owner yet. Projects, areas, or resources shelf?",
            "Resources - until claimed.",
        ),
        (
            "Tempted to sort notes by topic tag instead of life responsibility. Sort by what?",
            "Who owns it and when it ends.",
        ),
        (
            "Project finished - files still in active work folder. Leave or move?",
            "Archive - out of Projects.",
        ),
        (
            "Ongoing responsibility with no end date - project bucket or area?",
            "Areas - not Projects.",
        ),
        (
            "Topic folder tree vs PARA - am I tagging subject or naming owner and deadline?",
            "Owner and deadline - not subject.",
        ),
    ],
}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, ""
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, ""
    return text[: end + 4], text[end + 4 :], text[3:end].strip()


def format_cards(cards: list[tuple[str, str]]) -> str:
    lines = ["cards:"]
    for front, back in cards:
        lines.append(f'  - front: "{front}"')
        lines.append(f'    back: "{back}"')
    return "\n".join(lines)


def apply_rewrite(path: Path, cards: list[tuple[str, str]]) -> None:
    for front, back in cards:
        if len(front) <= len(back):
            raise ValueError(f"{path.name}: front not longer than back: {len(front)}<={len(back)}: {front!r}")

    text = path.read_text(encoding="utf-8")
    fm_head, body, fm_inner = split_frontmatter(text)
    if not fm_inner:
        raise ValueError(f"{path.name}: no frontmatter")

    new_cards = format_cards(cards)
    if not re.search(r"^cards:\s*$", fm_inner, re.M):
        raise ValueError(f"{path.name}: no cards block")

    new_fm_inner = re.sub(
        r"^cards:\s*\n(?:  - front:.*\n    back:.*\n?)+",
        new_cards + "\n",
        fm_inner,
        count=1,
        flags=re.M,
    )
    path.write_text(f"---\n{new_fm_inner}\n---\n{body.lstrip()}", encoding="utf-8")


def main() -> int:
    updated = 0
    for slug, cards in REWRITES.items():
        path = NOTES_DIR / f"{slug}.md"
        if not path.exists():
            print(f"Missing: {path}", file=sys.stderr)
            return 1
        apply_rewrite(path, cards)
        updated += 1
        print(f"  updated {path.name}")

    print(f"\nDone: {updated} notes updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
