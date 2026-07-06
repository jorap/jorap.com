#!/usr/bin/env python3
"""Add relationship rows for wikilinks in key_concept that lack typed links."""
from __future__ import annotations

from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

# (from_title, to_title): (type, reason)
ADDITIONS: dict[tuple[str, str], tuple[str, str]] = {
    ("Ask Seek Knock", "Periodic Knowledge Review"): (
        "extends",
        "Ask-seek-knock rhythm needs scheduled review, not one-off prayer bursts",
    ),
    ("Assurance", "Judgment Seat"): (
        "extends",
        "Assurance holds when the review comes - works judged, not the standing",
    ),
    ("Assurance", "Minimum Effective Dose"): (
        "alternative",
        "Enough assurance to obey vs endless self-audit for proof you belong",
    ),
    ("Atomic Notes", "Let Your Yes Be Yes"): (
        "extends",
        "One plain claim per note - same yes-means-yes discipline",
    ),
    ("Attention Economy", "Information Diet"): (
        "extends",
        "Platforms compete for attention - diet is the counter-move",
    ),
    ("Behavioral Economics", "Mental Models"): (
        "extends",
        "Bias catalog sits inside the wider mental-models shelf",
    ),
    ("Building a Second Brain", "Capture"): (
        "extends",
        "CODE starts with capture - nothing to organize until it lands",
    ),
    ("Building a Second Brain", "The Second Brain Workflow"): (
        "implements",
        "CODE stages operationalized in the workflow note",
    ),
    ("Christianity and Politics", "By Their Fruits"): (
        "extends",
        "Judge political claims by outcomes, not slogans or tribe",
    ),
    ("Christianity and Politics", "Great Commission"): (
        "extends",
        "Discipleship mission outranks party loyalty",
    ),
    ("Christianity and Politics", "Heart Righteousness"): (
        "extends",
        "Outward policy fights can't substitute for inward obedience",
    ),
    ("Christianity and Politics", "Information Diet"): (
        "extends",
        "Outrage feeds need the same diet discipline as any other feed",
    ),
    ("Christianity and Politics", "Let Your Light Shine"): (
        "extends",
        "Good works visible - politics isn't the only lamp stand",
    ),
    ("Christianity and Politics", "Signal vs Noise"): (
        "extends",
        "Political noise drowns signal - filter before you amplify",
    ),
    ("Commonplace Book", "Layered Reading"): (
        "extends",
        "Commonplace entries grow from layered passes through sources",
    ),
    ("Commonplace Book", "Literature Notes"): (
        "extends",
        "Literature notes feed the commonplace - quotes with context",
    ),
    ("Compounding", "Abide in Me"): (
        "extends",
        "Fruit compounds from staying connected - not self-powered streaks alone",
    ),
    ("Compounding", "Eternal Rewards"): (
        "extends",
        "Faithful small deposits stack toward kingdom repayment",
    ),
    ("Compounding", "Free Grace"): (
        "extends",
        "Compounding obedience follows grace received - not to earn the gift",
    ),
    ("Develop, Don't Endanger", "Purpose and Vision"): (
        "extends",
        "Challenge people toward a named purpose - not risk without aim",
    ),
    ("Discipleship", "Creative Output"): (
        "extends",
        "Follow Jesus includes making and sharing - not only consuming",
    ),
    ("Discipleship", "Great Commission"): (
        "extends",
        "Make disciples - the outward push of daily following",
    ),
    ("Discipleship", "Judgment Seat"): (
        "extends",
        "Following has a review - works weighed, standing secure in grace",
    ),
    ("Discipleship", "Take Up Your Cross"): (
        "extends",
        "Daily cross-bearing is the cost shape of following",
    ),
    ("Discipleship", "The Narrow Way"): (
        "extends",
        "Few find it - discipleship is the narrow path, not crowd default",
    ),
    ("Discipleship", "The Wise Builder"): (
        "extends",
        "Hear and do - obedience that survives the storm",
    ),
    ("Discipleship vs Leadership", "Free Grace"): (
        "extends",
        "Vertical seat rests on grace received - not leadership performance",
    ),
    ("Don't Worry", "Seek the Kingdom First"): (
        "extends",
        "Anxiety loses when kingdom priority names what comes first",
    ),
    ("Don't Worry", "Slow Productivity"): (
        "alternative",
        "Trust God's provision vs hustle-as-proof you're not falling behind",
    ),
    ("Eternal Rewards", "Let Your Light Shine"): (
        "extends",
        "Visible good works stored up - shine with eternity in view",
    ),
    ("Eternal Rewards", "Secret Devotion"): (
        "extends",
        "Hidden devotion repaid - Father who sees in secret",
    ),
    ("Eternal Rewards", "Treasure in Heaven"): (
        "extends",
        "Repayment language - store where moth and rust don't reach",
    ),
    ("Evergreen Notes", "Periodic Knowledge Review"): (
        "extends",
        "Evergreen notes stay sharp through scheduled revisit",
    ),
    ("Evergreen Notes", "The Beatitudes"): (
        "extends",
        "Timeless claims like the Beatitudes - notes that age well",
    ),
    ("Failure as Feedback", "Judgment Seat"): (
        "alternative",
        "Iterative learning from misses vs final review - different clocks",
    ),
    ("Faith and Works", "Discipleship"): (
        "extends",
        "Works flow from following - faith alive shows up in obedience",
    ),
    ("Faith and Works", "Sanctification"): (
        "extends",
        "James and Paul meet - faith that works is being made holy",
    ),
    ("Faith and Works", "The Narrow Way"): (
        "extends",
        "Faith without the narrow walk is dead on inspection",
    ),
    ("Faithful Steward", "Integrity Without an Audience"): (
        "extends",
        "Workplace lane - faithful use when nobody applauds",
    ),
    ("Forgiveness", "Ask Seek Knock"): (
        "extends",
        "Forgive as you have been forgiven - ask-seek-knock includes mercy",
    ),
    ("Free Grace", "Discipleship"): (
        "extends",
        "Grace received first - discipleship is response, not entry fee",
    ),
    ("Free Grace", "Eternal Rewards"): (
        "contradicts",
        "when repayment language starts to sound like wages for the gift",
    ),
    ("Free Grace", "Faith and Works"): (
        "extends",
        "Works don't buy grace - they prove faith is alive",
    ),
    ("Free Grace", "Sanctification"): (
        "extends",
        "Holiness follows justification - not the price of it",
    ),
    ("Fruits of the Spirit", "Assurance"): (
        "extends",
        "Spirit fruit confirms belonging - not earns it",
    ),
    ("Fruits of the Spirit", "Don't Worry"): (
        "extends",
        "Peace fruit pushes back on anxiety's grip",
    ),
    ("Fruits of the Spirit", "Faithful Steward"): (
        "extends",
        "Stewardship fruit - faithful use of what was entrusted",
    ),
    ("Fruits of the Spirit", "Humility and Service"): (
        "extends",
        "Gentleness and service - kingdom greatness through serving",
    ),
    ("Fruits of the Spirit", "Let Your Light Shine"): (
        "extends",
        "Good works fruit - visible light from inner life",
    ),
    ("Fruits of the Spirit", "Mercy"): (
        "extends",
        "Mercy named among the fruit cluster",
    ),
    ("Fruits of the Spirit", "Peacemakers"): (
        "extends",
        "Peacemaking fruit - blessed are those who mend",
    ),
    ("Fruits of the Spirit", "Slow the Moment"): (
        "extends",
        "Self-control fruit needs a slowed moment before reaction",
    ),
    ("Grateful Obedience", "Process Over Outcomes"): (
        "extends",
        "Obey gratefully in the process - not only when outcomes reward",
    ),
    ("Grateful Obedience", "Repent and Believe"): (
        "extends",
        "Believe first - obedience flows from repentance and faith",
    ),
    ("Grateful Obedience", "Take Up Your Cross"): (
        "extends",
        "Grateful yes to the daily cross - not grudging compliance",
    ),
    ("Great Commission", "Creative Output"): (
        "extends",
        "Make disciples includes teaching what you make - pass it on",
    ),
    ("Great Commission", "Free Grace"): (
        "extends",
        "Go and make disciples - mission flows from grace received",
    ),
    ("Heart Righteousness", "Free Grace"): (
        "extends",
        "Clean heart follows gift received - not performance that buys heaven",
    ),
    ("Judgment Seat", "Let Your Light Shine"): (
        "extends",
        "Works reviewed include visible good done in Christ's name",
    ),
    ("Judgment Seat", "Loss of Reward"): (
        "extends",
        "Review can mean loss of reward - standing secure, works weighed",
    ),
    ("Judgment Seat", "Periodic Knowledge Review"): (
        "alternative",
        "Final divine review vs garden revisit - same audit instinct, different scale",
    ),
    ("Judgment Seat", "Secret Devotion"): (
        "extends",
        "Hidden devotion reviewed - Father who sees in secret repays",
    ),
    ("Justification", "Eternal Rewards"): (
        "extends",
        "Declared righteous now - rewards for faithful use after",
    ),
    ("Justification", "Sanctification"): (
        "extends",
        "Justified once - being made holy is the lifelong follow-on",
    ),
    ("Let Your Light Shine", "Drafting in Public"): (
        "alternative",
        "Shine good works vs publish every draft for applause",
    ),
    ("Let Your Yes Be Yes", "Atomic Notes"): (
        "extends",
        "One plain yes per claim - atomic notes carry the same rule",
    ),
    ("Let Your Yes Be Yes", "Heart Righteousness"): (
        "extends",
        "Integrity starts in the heart - yes means yes inside first",
    ),
    ("Let Your Yes Be Yes", "Integrity"): (
        "extends",
        "Plain speech is integrity made audible",
    ),
    ("Let Your Yes Be Yes", "Let Your Light Shine"): (
        "extends",
        "Public yes matches private word - light and speech aligned",
    ),
    ("Literature Notes", "Atomic Notes"): (
        "extends",
        "Literature notes distill into atomic claims you can link",
    ),
    ("Loss of Reward", "Faith and Works"): (
        "extends",
        "Works that survive fire - faith without fruit may lose reward",
    ),
    ("Minimum Effective Dose", "Free Grace"): (
        "extends",
        "Enough gospel to believe - not endless proof before you rest",
    ),
    ("Minimum Viable Product", "Free Tier Hosting Stack"): (
        "extends",
        "Ship the smallest live site - free tier stack covers the first slice",
    ),
    ("Minimum Viable Product", "Selling Static Sites"): (
        "extends",
        "Client MVP lane - sell the smallest site that solves the job",
    ),
    ("Outcomes Over Pitch Decks", "Free Tier Hosting Stack"): (
        "extends",
        "Judge the stack by what ships - not slide charisma",
    ),
    ("Plain Commitments at Work", "Selling Static Sites"): (
        "extends",
        "Yes means yes on delivery dates - same plain promise discipline",
    ),
    ("Priorities Before the Inbox", "Deep Work"): (
        "extends",
        "Kingdom-first block before inbox - deep work needs protected priority",
    ),
    ("Reconciliation Before Worship", "Note Relationships"): (
        "alternative",
        "Repair people before ceremony - typed links need repair too",
    ),
    ("Sanctification", "Eternal Rewards"): (
        "extends",
        "Holiness now stacks toward kingdom repayment",
    ),
    ("Sanctification", "Free Grace"): (
        "extends",
        "Made holy after declared righteous - not to earn the gift",
    ),
    ("Sanctification", "Process Over Outcomes"): (
        "extends",
        "Sanctification is slow process faithfulness - not instant perfection",
    ),
    ("Secret Devotion", "Free Grace"): (
        "extends",
        "Hidden prayer isn't the price of grace - response from gift received",
    ),
    ("Seek the Kingdom First", "Treasure in Heaven"): (
        "extends",
        "Seek first - store treasure where the kingdom points",
    ),
    ("Selling Static Sites", "Git-Based CMS"): (
        "extends",
        "Client handoff lane - git-based CMS keeps them editing without you",
    ),
    ("Spaced Repetition", "Ask Seek Knock"): (
        "extends",
        "Persistent asking needs spaced return - not one-shot prayer",
    ),
    ("Spaced Repetition", "Pareto Principle"): (
        "extends",
        "Review the vital few cards - spaced reps on what moves recall",
    ),
    ("Standing vs Fellowship", "Reconciliation Before Worship"): (
        "extends",
        "Fellowship ledger needs repair before performance - same order",
    ),
    ("Standing vs Fellowship", "Repent and Believe"): (
        "extends",
        "Standing secured by faith - fellowship restored by repentance",
    ),
    ("Static Site Client Scope", "Client Site Pass-Off"): (
        "implements",
        "Scope note names the boundary - pass-off is how you close the handoff",
    ),
    ("Sunk Cost Fallacy", "Turn the Other Cheek"): (
        "alternative",
        "Cut the sunk cost vs absorb the hit - different exits from the same trap",
    ),
    ("Take Up Your Cross", "Discipleship"): (
        "extends",
        "Daily cross is the shape of following Jesus",
    ),
    ("Take Up Your Cross", "Process Over Outcomes"): (
        "extends",
        "Carry the cross in today's step - not only when outcomes reward",
    ),
    ("Take Up Your Cross", "The Narrow Way"): (
        "extends",
        "Cross-bearing is the narrow path - few take it",
    ),
    ("The Beatitudes", "Peacemakers"): (
        "extends",
        "Blessed are the peacemakers - beatitude named in the cluster",
    ),
    ("The Garage Concept", "Free Tier Hosting Stack"): (
        "extends",
        "Garage-stage sites run on free tier stacks first",
    ),
    ("The Narrow Way", "Discipleship"): (
        "extends",
        "Narrow gate is the discipleship path - few find it",
    ),
    ("The Trusted Inbox", "Building a Second Brain"): (
        "extends",
        "Trusted capture sits inside the wider second-brain system",
    ),
    ("The Wise Builder", "Creative Output"): (
        "extends",
        "Hear and do - output that survives the storm",
    ),
    ("The Wise Builder", "Loss of Reward"): (
        "contradicts",
        "Sand foundation looks built until the storm - false profession loses reward",
    ),
    ("The Wise Builder", "The Collector's Fallacy"): (
        "contradicts",
        "Hearing without doing is hoarding blueprints - same empty foundation",
    ),
    ("Treasure in Heaven", "Eternal Rewards"): (
        "extends",
        "Store up treasure - eternal rewards language for the same horizon",
    ),
    ("Treasure in Heaven", "Judgment Seat"): (
        "extends",
        "Treasure stored is treasure reviewed - kingdom accounting",
    ),
    ("Turn the Other Cheek", "Free Grace"): (
        "extends",
        "Forgiven people forgive - grace received enables the second cheek",
    ),
    ("Turn the Other Cheek", "Sunk Cost Fallacy"): (
        "contradicts",
        "Absorb the hit vs cut losses - cheek isn't sunk-cost denial",
    ),
}


def main() -> int:
    assert len(ADDITIONS) == 104, f"expected 104, got {len(ADDITIONS)}"

    title_to_path: dict[str, Path] = {}
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        raw_fm, _ = split_frontmatter(text)
        if not raw_fm:
            continue
        fm = yaml.safe_load(raw_fm) or {}
        title = fm.get("title")
        if title:
            title_to_path[title] = path

    by_file: dict[Path, list[tuple[str, str, str]]] = {}
    for (src, dst), (rtype, reason) in ADDITIONS.items():
        path = title_to_path.get(src)
        if not path:
            raise SystemExit(f"missing file for {src!r}")
        by_file.setdefault(path, []).append((dst, rtype, reason))

    updated = 0
    added = 0
    for path, rows in sorted(by_file.items(), key=lambda x: x[0].name):
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        rels = list(fm.get("relationships") or [])
        existing = {str(r.get("wikilink", "")).lower() for r in rels if isinstance(r, dict)}
        file_added = 0
        for dst, rtype, reason in rows:
            wikilink = f"[[{dst}]]"
            if wikilink.lower() in existing:
                continue
            rels.append({"type": rtype, "wikilink": wikilink, "reason": reason})
            existing.add(wikilink.lower())
            file_added += 1
        if not file_added:
            continue
        rels.sort(key=lambda r: (str(r.get("type", "")).lower(), str(r.get("wikilink", "")).lower()))
        fm["relationships"] = rels
        out = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if not out.endswith("\n"):
            out += "\n"
        path.write_text(out, encoding="utf-8")
        updated += 1
        added += file_added
        print(f"updated: {path.name} (+{file_added})")

    print(f"done: {updated} files, {added} rows added")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
