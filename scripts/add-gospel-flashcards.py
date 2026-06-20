#!/usr/bin/env python3
"""Add review flashcard decks to gospel notes missing them."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

DECKS: dict[str, dict] = {
    "the-beatitudes": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Feeling self-sufficient after a good week. Kingdom posture I'm missing?", "Poor in spirit - receive as gift."),
            ("Loss hit hard and I want to skip church. What posture did Jesus bless?", "Mourn - comfort comes to mourners."),
            ("Thumb itching to clap back and prove I'm strong. Which beatitude fork?", "Meek - don't grasp status."),
            ("Scrolling outrage instead of craving what God calls right. What's the blessed hunger?", "Hunger for righteousness."),
            ("Someone who wronged me needs help. First merciful move?", "Show mercy - merciful obtain mercy."),
            ("Persecuted for doing right - tempted to quit looking faithful. What's the promise?", "Kingdom of heaven - blessed are persecuted."),
        ],
    },
    "dont-worry": {
        "card_sets": ["Eternal Principles", "Gospel", "Priorities"],
        "cards": [
            ("2am spiral about bills before I prayed. What comes first?", "Kingdom first - pray, then act."),
            ("Thumb on news refresh about tomorrow's meeting. One move that breaks the worry loop?", "Today's enough - don't borrow tomorrow's trouble."),
            ("Treating worry like it'll add hours to my life. What does it actually do?", "Nothing useful - trust the Father."),
            ("Calendar packed, soul thin - anxious about everything at once. What did Jesus rank first?", "Seek kingdom first - needs follow."),
            ("Good week but still replaying what might go wrong Sunday. What's the antidote?", "Trust provision - Father knows what I need."),
            ("Work hustle and trust in God pulling opposite. How many masters?", "One Master - drop anxious serving of tomorrow."),
        ],
    },
    "judge-not": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Friend's speck obvious; my plank invisible. What do I fix first?", "Remove my plank - then help with speck."),
            ("About to quote their failure online. Who am I playing?", "Not their judge - I needed mercy first."),
            ("Condemning someone while excusing the same sin in me. What's the hypocrisy move?", "Stop condemning - diagnose myself first."),
            ("Charismatic teacher, ugly fruit in followers. What kind of judgment is allowed?", "Discern fruit - not play final judge."),
            ("Nitpick someone's parenting while mine's a mess. One check before I speak?", "Apply the standard to me first."),
            ("Tempted to roast someone else's mess while mine's hidden. What's my move?", "Fix my plank - audit myself first."),
        ],
    },
    "childlike-faith": {
        "card_sets": ["Eternal Principles", "Gospel", "Faith"],
        "cards": [
            ("Calculating if I'm good enough to pray tonight. What posture enters the kingdom?", "Childlike receive - stop merit math."),
            ("New believer ashamed they don't know the Bible. What would I tell them?", "Receive like a child - dependence, not achievement."),
            ("Negotiating with God before I trust the promise. What's the entry posture?", "Stop calculating - receive the gift."),
            ("Treating faith like a merit account I'm building. What's wrong?", "Trust receives - faith isn't stacked works."),
            ("Afraid to ask a dumb question in small group. What would Jesus say?", "Come like a child - ask, don't perform."),
            ("Delaying trust until I understand everything. When do I enter?", "Now - receive before I've figured it all out."),
        ],
    },
    "the-narrow-way": {
        "card_sets": ["Eternal Principles", "Gospel", "Discipleship"],
        "cards": [
            ("Comfortable path everyone else is on. Which gate am I choosing?", "Narrow - hard road, life at the end."),
            ("Saying Lord Lord but same secret sin unchanged. What did Jesus warn?", "Not everyone who says Lord enters - do his words."),
            ("Cross feels optional because grace saved me. What's still costly?", "Daily discipleship - not the salvation price."),
            ("Broad road tempting because it's crowded and easy. One move?", "Pick narrow - even if few find it."),
            ("Moral performance as salvation ticket. Which road is that?", "Broad self-righteousness - not the grace gate."),
            ("Tempted to skip hard obedience because everyone's comfortable. Who moves first?", "I take narrow - don't follow the crowd."),
        ],
    },
    "treasure-in-heaven": {
        "card_sets": ["Eternal Principles", "Gospel", "Priorities"],
        "cards": [
            ("Saving articles and gear I'll never use. Where's my heart drifting?", "Check treasure - moth and rust eat earth stuff."),
            ("Generosity impulse killed by fear of running out. What lasts?", "Store heaven-side - give, mercy, obey."),
            ("Hoarding bookmarks feels productive. What's the wrong treasure?", "Collector's fallacy - nothing lasting stored."),
            ("Wallet and calendar show where heart actually lives. One reframe?", "Move treasure - heart follows."),
            ("Tempted to stack earthly security after grace saved me. What's the order?", "Heaven secure - store what lasts there."),
            ("Thumb on another buy I don't need. One check before checkout?", "Will this rust - or store something that lasts?"),
        ],
    },
    "eternal-rewards": {
        "card_sets": ["Eternal Principles", "Gospel", "Priorities"],
        "cards": [
            ("Secret prayer and tempted to tell everyone so I feel credited. Who pays?", "Father in secret - not the audience."),
            ("Good works week - feels like I bought heaven. Correct the order?", "Grace saved first - reward follows faithfulness."),
            ("Stacked service feels like merit ladder to eternal life. What's the error?", "Gift first - repayment second."),
            ("Hidden generosity no one saw - discouraged it doesn't count. Who sees?", "Father sees hidden - he'll repay."),
            ("One heroic volunteer week mistaken for down payment on heaven. What's true?", "Saved by faith - rewards after."),
            ("Small daily obedience feels too small to matter eternally. What stacks?", "Faithful acts compound - Father repays."),
        ],
    },
    "secret-devotion": {
        "card_sets": ["Eternal Principles", "Gospel", "Prayer"],
        "cards": [
            ("About to post my quiet time for likes. Who's the real audience?", "Father alone - not the feed."),
            ("Giving with one hand while the other broadcasts it. What's wrong?", "Give in secret - Father who sees repays."),
            ("Prayer crafted for how it sounds out loud at dinner. One fix?", "Pray in secret - real audience is Father."),
            ("Fasting but making sure people notice I'm suffering. What's the move?", "Fast in secret - wash face, live normal."),
            ("Every piety act becoming content for applause. Which lane?", "Hidden devotion - not performance content."),
            ("Tempted to skip secret prayer because no one saw. Who saw?", "Father sees hidden - that's enough."),
        ],
    },
    "humility-and-service": {
        "card_sets": ["Eternal Principles", "Gospel", "Discipleship"],
        "cards": [
            ("Grasping for status in a group project. Kingdom path to greatness?", "Serve all - last becomes first."),
            ("Waiting to be served at home after serving at church. What's the gap?", "Serve here too - same kingdom ladder."),
            ("Foot-washing feels below my role. What did Jesus model?", "Serve, not be served - wash feet."),
            ("Visibility became the goal in ministry. What beats pride?", "Humble self - let God exalt."),
            ("Tempted to exalt myself in a story about my sacrifice. One check?", "Humble - don't grab the spotlight."),
            ("Leadership seat felt like the win. What makes someone great?", "Servant of all - not title grabbed."),
        ],
    },
    "let-your-light-shine": {
        "card_sets": ["Eternal Principles", "Gospel", "Discipleship"],
        "cards": [
            ("Good deed done but I want credit in the caption. Who gets glory?", "Father - not my brand."),
            ("Hiding help I gave from false modesty. What was the point of the light?", "Shine - they glorify God, not me."),
            ("Good works under a basket - scared of looking proud. What's the move?", "Let light shine - visibility for God."),
            ("Drafting a post about my charity. Audience check?", "Glorify Father - not perform righteousness."),
            ("Neighbor won't see God is real if I hide every good work. First move?", "Do good visibly - point to Father."),
            ("About to skip serving publicly because I hate attention. Why shine?", "So others glorify God - don't hide."),
        ],
    },
    "peacemakers": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Two friends feuding - tempted to pick a side and stoke it. What's the blessed move?", "Make peace - pursue reconciliation."),
            ("Conflict at work and I just want quiet. Peace-at-any-price?", "No - active peacemaking, not silence only."),
            ("Hard truth needs saying but I soft-pedal to avoid fight. What am I called to?", "Peace through truth in love."),
            ("Wronged and revenge would feel peaceful for five minutes. Family resemblance move?", "Reconcile like the Father did."),
            ("Family dinner tension - finger on gossip instead of bridge-building. First move?", "Pursue peace - speak to reconcile."),
            ("Someone thinks peace means never confronting sin. What do I say?", "Peace is work - truth plus reconciliation."),
        ],
    },
    "turn-the-other-cheek": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Insult landed - thumb drafting equal hurt back. What's the cycle-break?", "Don't retaliate - absorb without escalating."),
            ("Sunk cost anger - already invested rage in this feud. Stop line?", "Stop throwing anger after sunk hurt."),
            ("Eye-for-eye feels fair right now. Personal ethic Jesus gave?", "Turn cheek - refuse to become what hurt me."),
            ("Waiting to hit back before I act well toward them. What comes first?", "Break cycle - don't return evil."),
            ("Public slap to my reputation - outrage justified in my head. Next move?", "Non-retaliation - don't mirror evil."),
            ("They struck first so my payback feels righteous. Who keeps score?", "Grace freed me - don't score back."),
        ],
    },
    "by-their-fruits": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Charismatic preacher, messy lives in followers. How do I evaluate?", "Watch fruit - grapes from vines, not hype."),
            ("Trending teacher everyone bookmarks. Filter before I trust?", "Outcome over credentials - what does it produce?"),
            ("Wolf in sheep's clothing - credentials look perfect. Time tells what?", "Fruit over time - thorns don't grow grapes."),
            ("Can't tell if teaching helps or hurts. PKM parallel?", "Signal vs noise - what produces good over time?"),
            ("About to condemn the teacher's soul online. What do I do instead of playing judge?", "Discern fruit - not condemn souls."),
            ("New book everyone's sharing. One check before I adopt the teaching?", "What fruit does it produce - not charisma?"),
        ],
    },
    "heart-righteousness": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Anger simmering after traffic - treated them fine outwardly. What did Jesus call that?", "Murder in the heart - deal with anger."),
            ("Lust logged mentally while marriage looks fine outside. Inner standard?", "Adultery in heart - cut off at motive."),
            ("Polished Sunday face, nursing grudge Monday. Which righteousness counts?", "Heart - not outward compliance only."),
            ("About to send cold reply while sounding righteous. One inner check?", "Motives - anger is heart murder."),
            ("Performing good works while resentment runs inside. What exposes depth?", "Heart righteousness - God sees motive."),
            ("Tempted to excuse inner sin because nobody saw. Who sees?", "God sees heart - start where only He looks."),
        ],
    },
    "reconciliation-before-worship": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Gift in hand, brother still hurt by me. Order Jesus gave?", "Reconcile first - then offer gift."),
            ("Sunday worship while avoiding someone I wronged. What breaks?", "Hollow worship - go reconcile first."),
            ("Altar call feeling high but unrepaired relationship at home. First move?", "Leave gift - go be reconciled."),
            ("Broken link in the garden I keep ignoring. Human parallel?", "Repair breach first - face to face."),
            ("Know they're angry but hope ceremony fixes it. Who moves?", "I go - initiative on me."),
            ("Already saved but distant from a brother. What's restored?", "Fellowship - not re-earning heaven."),
        ],
    },
    "render-unto-caesar": {
        "card_sets": ["Eternal Principles", "Gospel", "Discipleship"],
        "cards": [
            ("Tax bill arrived - tempted to dodge as kingdom protest. Civic move?", "Pay lawful duty - give Caesar his coin."),
            ("Patriotism and worship tangled. Who gets ultimate allegiance?", "God ultimate - Caesar gets what's his."),
            ("State feels like lord of everything lately. Sort the two?", "Render each properly - don't idolize Rome."),
            ("Revolutionary tax refusal sounds faithful. What did Jesus model?", "Pay taxes - kingdom higher, still pay."),
            ("God's image bearer - what do I owe Him vs the state?", "Self to God - coin to Caesar."),
            ("Civic duty skipped because I'm kingdom-first. What's the move?", "Kingdom first doesn't excuse lawful duty."),
        ],
    },
    "great-commission": {
        "card_sets": ["Eternal Principles", "Gospel", "Discipleship"],
        "cards": [
            ("Notes garden full, gospel never leaves my mouth. What's the hoarding move?", "Share truth - don't hoard like bookmarks."),
            ("Someone asks how to follow Jesus - I lecture systems not gospel. Lead with?", "Repent and believe - then teach obedience."),
            ("Baptize and teach feels like someone else's job. Who did Jesus send?", "All disciples - go, he is with you."),
            ("Obedience teaching skipped because grace saved them. What's missing?", "Teach obedience - discipleship after faith."),
            ("Afraid to speak up at work about faith. Promise Jesus gave?", "I am with you - go anyway."),
            ("Truth hoarded in private study, zero disciples made. What's the commission?", "Go make disciples - not hoard in garden."),
        ],
    },
    "let-your-yes-be-yes": {
        "card_sets": ["Eternal Principles", "Gospel", "Ethics"],
        "cards": [
            ("Padding a promise with extra oaths so they'll believe me. What did Jesus say?", "Yes is yes - word stands alone."),
            ("Contract needs flashy language to feel binding. Integrity move?", "Plain yes - no manipulation."),
            ("Public post promises more than private life delivers. Which lane breaks?", "Private honesty first - words match life."),
            ("Kitchen-sink promise covering six things at once. Speech parallel?", "One plain yes - no padded speech."),
            ("Exaggerating to win an argument. Beyond yes/no comes from where?", "Manipulation - let the word be enough."),
            ("Thumb adding qualifiers to a simple commitment. Strip to what?", "Simple yes or no - no spin."),
        ],
    },
}


def format_cards_block(spec: dict) -> str:
    sets = ", ".join(f'"{s}"' for s in spec["card_sets"])
    lines = [f'review: true', f"card_sets: [{sets}]", "cards:"]
    for front, back in spec["cards"]:
        front_esc = front.replace('"', '\\"')
        back_esc = back.replace('"', '\\"')
        lines.append(f'  - front: "{front_esc}"')
        lines.append(f'    back: "{back_esc}"')
    return "\n".join(lines)


def inject(path: Path, block: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    if re.search(r"^review:\s*true", text, re.M):
        return False
    end = text.find("\n---", 3)
    fm, body = text[: end + 4], text[end + 4 :]
    if re.search(r"^draft:\s*false", fm, re.M):
        fm = re.sub(r"^draft:\s*false\s*$", block + "\ndraft: false", fm, count=1, flags=re.M)
    else:
        fm = fm.rstrip() + "\n" + block + "\n"
    path.write_text(fm + body, encoding="utf-8")
    return True


def main() -> int:
    n = 0
    for slug, spec in sorted(DECKS.items()):
        path = NOTES / f"{slug}.md"
        if not path.exists():
            print(f"  missing {slug}.md", file=__import__("sys").stderr)
            continue
        if inject(path, format_cards_block(spec)):
            print(f"  {slug}.md")
            n += 1
    print(f"\nDone: {n} decks added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
