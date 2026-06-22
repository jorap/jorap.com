#!/usr/bin/env python3
"""Normalize ## Note Relationships tables: note_kind index, sort rows, merge typed links."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}

TYPE_ORDER = {"alternative": 0, "contradicts": 1, "extends": 2, "implements": 3}
ROW_RE = re.compile(
    r"^\|\s*(alternative|contradicts|extends|implements|index)\s*\|\s*(\[\[[^\]]+\]\]|—)\s*\|\s*(.+?)\s*\|$"
)
INDEX_SLUGS = {"getting-started", "eternal-principles", "maps-of-content"}

# slug -> list of (type, wikilink_title, reason)
ADD: dict[str, list[tuple[str, str, str]]] = {
    "active-knowledge-curation": [
        ("implements", "Periodic Knowledge Review", "Monthly prune carries the review habit this note names"),
        ("alternative", "Maps of Content", "Hand-built hub vs revisit-and-prune when curation stays inline"),
    ],
    "associative-linking": [
        ("implements", "Atomic Notes", "Typed wikilinks make one-claim files usable"),
        ("alternative", "PARA Method", "Link-first graph vs life buckets when folders beat waiting for links"),
    ],
    "atomic-notes": [
        ("implements", "PKM", "One-claim files are the Lego blocks PKM stacks"),
        ("alternative", "Mind Mapping", "Single file per idea vs one bubble map when splitting early"),
    ],
    "building-a-personal-api": [
        ("alternative", "Local-first Software", "Structured API vs plain files when sync layers multiply"),
    ],
    "building-a-second-brain": [
        ("implements", "PKM", "CODE pipeline carries personal knowledge management into daily capture"),
        ("alternative", "GTD vs PARA", "Second brain stack vs task-first inbox when Forte's buckets win"),
    ],
    "capture": [
        ("implements", "The Trusted Inbox", "One inbox habit carries capture into something you'll empty"),
        ("alternative", "Frictionless Capture", "Single pipe vs zero-friction everywhere when trust beats options"),
    ],
    "creative-output": [
        ("implements", "Building a Second Brain", "Express lane carries CODE's output step"),
        ("alternative", "Minimum Viable Product", "Polished ship vs rough MVP when deadline forces cut scope"),
    ],
    "daily-notes": [
        ("alternative", "Fleeting Notes", "Dated scratch vs title-only fleeting when the pad is today's lane"),
        ("implements", "Capture", "Daily scratch carries the capture habit before anything goes evergreen"),
    ],
    "digital-garden": [
        ("alternative", "Drafting in Public", "Slow public growth vs ship drafts for feedback"),
        ("implements", "Evergreen Notes", "Public garden carries durable notes into visible growth"),
    ],
    "digital-minimalism": [
        ("alternative", "Digital Serendipity", "Fewer tools vs engineered surprise when cutting pipes wins"),
    ],
    "digital-serendipity": [
        ("alternative", "Digital Minimalism", "Surprise links vs fewer moving parts when rediscovery beats sync"),
        ("implements", "Associative Linking", "Random resurfacing carries link-first structure"),
    ],
    "drafting-in-public": [
        ("alternative", "Digital Garden", "Ship drafts vs slow garden when feedback must land this week"),
        ("implements", "Creative Output", "Public drafts carry express pressure into finished posts"),
    ],
    "evergreen-notes": [
        ("implements", "Atomic Notes", "Durable phrasing carries one-claim atoms into reuse"),
        ("alternative", "Daily Notes", "Two-year wording vs today's scratch when permanence can wait"),
    ],
    "evergreen-vs-fleeting-notes": [
        ("alternative", "Note Maturity", "Two-lane model vs staged maturity when lifecycle needs a third step"),
    ],
    "first-principles-thinking": [
        ("alternative", "Mental Models", "Strip-to-basics vs pick-a-model when a lens beats invention"),
    ],
    "future-proofing-knowledge": [
        ("alternative", "Building a Personal API", "Plain export vs structured API when boring files survive churn"),
    ],
    "getting-started": [
        ("contradicts", "Maps of Content", "when jumping into a hub beats reading onboarding first"),
    ],
    "graph-view-analytics": [
        ("alternative", "Maps of Content", "Link metrics vs hand-curated hub when counts beat judgment"),
        ("implements", "Associative Linking", "Graph rank carries link-first structure into visible hubs"),
    ],
    "gtd-vs-para": [
        ("alternative", "Getting Things Done", "Allen task inbox vs Forte life buckets when runway is the frame"),
        ("alternative", "PARA Method", "PARA sort vs GTD contexts when project folders beat action lists"),
    ],
    "intellectual-sourcing": [
        ("alternative", "Progressive Summarization", "Source-first citations vs bold layers when provenance must stay visible"),
    ],
    "local-first-software": [
        ("alternative", "Building a Personal API", "Local files vs push API when boring export wins"),
    ],
    "maps-of-content": [
        ("implements", "Active Knowledge Curation", "Hand-built hub carries curator work into one doorway"),
        ("alternative", "Graph View Analytics", "Curated index vs link rank when judgment beats counts"),
    ],
    "metadata-strategy": [
        ("alternative", "Building a Personal API", "Light tags vs machine schema when fewer fields stay honest"),
    ],
    "mind-mapping": [
        ("alternative", "Atomic Notes", "Bubble map vs one file per claim when the shape is still fuzzy"),
        ("implements", "Creative Output", "Visual brainstorm carries express before atoms split"),
    ],
    "minimum-viable-product": [
        ("implements", "Creative Output", "Rough ship carries express when polish would miss the window"),
        ("alternative", "Evergreen Notes", "MVP cut vs two-year phrasing when speed beats permanence"),
    ],
    "mobile-capture-workflows": [
        ("implements", "Capture", "Share-sheet capture carries the inbox habit on the phone"),
    ],
    "note-relationships": [
        ("implements", "Associative Linking", "Typed rows carry vague wikilinks into named push and pull"),
        ("alternative", "PARA Method", "Body link types vs folder sort when typed links beat project buckets"),
    ],
    "para-method": [
        ("alternative", "Associative Linking", "Life buckets vs link-first when owner and deadline are clear"),
        ("implements", "Building a Second Brain", "PARA folders carry CODE's organize step"),
    ],
    "periodic-knowledge-review": [
        ("implements", "Active Knowledge Curation", "Calendar review carries prune-and-connect curation"),
        ("alternative", "Minimum Effective Dose", "Scheduled review vs smallest habit when calendar beats dose"),
    ],
    "pkm": [
        ("implements", "Getting Started", "Garden rules carry PKM into how this site actually works"),
        ("alternative", "GTD vs PARA", "Note garden vs task inbox when architecture beats action lists"),
    ],
    "progressive-summarization": [
        ("alternative", "The Feynman Technique", "Bold layers vs explain-the-gap when distill stays on borrowed text"),
        ("implements", "Building a Second Brain", "Highlight layers carry CODE's distill step"),
    ],
    "signal-vs-noise": [
        ("alternative", "Active Knowledge Curation", "Filter at save vs curate after capture"),
        ("contradicts", "Capture", "when I save first and filter later"),
    ],
    "slow-productivity": [
        ("alternative", "The 12 Week Year", "Few deep projects vs quarterly sprint when pace should slow"),
    ],
    "spaced-repetition": [
        ("alternative", "The Feynman Technique", "Card drill vs explain-out-loud when scheduling beats narration"),
        ("implements", "Evergreen Notes", "SRS carries durable claims into phone review"),
    ],
    "synthesis-as-a-goal": [
        ("alternative", "Progressive Summarization", "Rewrite into belief vs bold layers when merge beats highlight"),
        ("implements", "Creative Output", "Merged belief carries express after sources settle"),
    ],
    "the-12-week-year": [
        ("alternative", "Slow Productivity", "Quarterly sprint vs fewer deep projects when scoreboard beats depth"),
    ],
    "the-collectors-fallacy": [
        ("alternative", "Capture", "Hoard without express vs disciplined inbox when saving feels like progress"),
    ],
    "the-feynman-technique": [
        ("alternative", "Spaced Repetition", "Explain gaps vs card drill when narration beats scheduling"),
        ("implements", "Evergreen Notes", "Explain-simple carries durable phrasing into belief"),
    ],
    "the-garage-concept": [
        ("alternative", "Digital Garden", "Private garage vs public growth when drafts need shelter"),
    ],
    "the-knowledge-lifecycle": [
        ("alternative", "Evergreen vs Fleeting Notes", "Stage model vs two-lane split when maturity needs a third step"),
        ("implements", "Evergreen vs Fleeting Notes", "Lifecycle names the lanes fleeting and evergreen notes use"),
    ],
    "the-second-brain-workflow": [
        ("alternative", "Minimum Effective Dose", "Full CODE loop vs smallest habit when the whole loop is too heavy"),
    ],
    "the-trusted-inbox": [
        ("alternative", "Mobile Capture Workflows", "One pipe vs frictionless phone capture when trust beats options"),
        ("implements", "Capture", "Empty-the-inbox carries capture into one pipe you'll actually process"),
    ],
    "there-is-no-perfect-solution": [
        ("alternative", "Pareto Principle", "Good-enough vs protect-the-vital-few when perfect is the enemy"),
    ],
    "weekly-review-checklists": [
        ("alternative", "Minimum Effective Dose", "Full checklist vs smallest review when travel week shrinks time"),
    ],
    # Gospel — alternative where sibling practices compete, not fourth-type filler
    "love-your-enemies": [
        ("alternative", "Turn the Other Cheek", "Enemy-love vs non-retaliation when the moment is personal insult"),
    ],
    "peacemakers": [
        ("alternative", "Love Your Enemies", "Make peace vs love enemies when the job is ending the fight"),
    ],
    "humility-and-service": [
        ("alternative", "Let Your Light Shine", "Hidden service vs visible good when modesty hides the work"),
    ],
    "secret-devotion": [
        ("alternative", "Let Your Light Shine", "Hidden piety vs public good works when the audience is Father alone"),
    ],
    "eternal-principles": [
        ("contradicts", "First Principles Thinking", "when I treat gospel ethics as ideas I invented"),
    ],
    # Relationship connection cluster
    "break-the-escalation-cycle": [
        ("extends", "Listen Before Fixing", "Hear before the sharp reply-all draft"),
        ("extends", "Name the Feeling", "Label the spike before it becomes the thread"),
        ("extends", "Set Calm Boundaries", "Calm limit stops the reply-all war"),
    ],
    "coaching-ethics": [
        ("extends", "Safety Comes First", "Consent doesn't erase the job when the drill is unsafe"),
        ("implements", "Follow Their Lead", "Join their world except when the move endangers them"),
    ],
    "complete-the-cycle": [
        ("extends", "Listen Before Fixing", "Hearing is step one; closing the loop is step two"),
    ],
    "continuous-improvement": [
        ("extends", "Create Regular Connection", "Small connection reps compound like process fixes"),
        ("extends", "Notice the Good", "Naming what worked feeds the next rep"),
    ],
    "create-regular-connection": [
        ("extends", "Listen Before Fixing", "The ritual only works if I hear before I fix"),
        ("extends", "Minimum Effective Dose", "Ten-minute check-in beats one grand gesture"),
    ],
    "develop-dont-endanger": [
        ("extends", "Safety Comes First", "Following their lead stops when the drill endangers them"),
        ("extends", "Follow Their Lead", "Join their world — not when the move crosses safety limits"),
    ],
    "duty-of-care": [
        ("implements", "Safety Comes First", "Stopping harm is duty of care in motion"),
    ],
    "emotional-regulation": [
        ("extends", "Listen Before Fixing", "Hold the urge to mail the first-draft answer"),
        ("extends", "Name the Feeling", "Label the spike before it drives the reply"),
        ("extends", "Set Calm Boundaries", "Steady voice lands the line better"),
    ],
    "forgiveness": [
        ("extends", "Set Calm Boundaries", "Forgive the heart; keep boundaries where trust still rebuilds"),
    ],
    "habit-formation": [
        ("extends", "Create Regular Connection", "Connection rituals are habits with a person's name on them"),
    ],
    "love-your-neighbor": [
        ("extends", "Follow Their Lead", "Love neighbor means entering their world before I redirect"),
        ("extends", "Listen Before Fixing", "Care I'd want includes being heard before being fixed"),
        ("extends", "Create Regular Connection", "Neighbor-love shows up in small repeated presence"),
    ],
    "minimum-effective-dose": [
        ("extends", "Create Regular Connection", "Smallest connection habit that still lands"),
    ],
    "notice-the-good": [
        ("extends", "The Golden Rule", "Specific praise is how I'd want to be treated"),
    ],
    "peacemakers": [
        ("extends", "Listen Before Fixing", "Make peace by hearing before prescribing"),
        ("extends", "Name the Feeling", "Truth in love often starts with naming what's carried"),
        ("extends", "Set Calm Boundaries", "Peace through truth includes calm limits"),
        ("implements", "Break the Escalation Cycle", "Peacemaking in the reply-all thread"),
    ],
    "process-over-outcomes": [
        ("extends", "Create Regular Connection", "The repeated moment matters more than one perfect date"),
        ("extends", "Notice the Good", "Reinforce the behavior in the loop, not only the score"),
    ],
    "psychological-safety": [
        ("extends", "Listen Before Fixing", "People speak up when being heard beats being fixed"),
        ("extends", "Follow Their Lead", "Join their framing before you redirect the blame"),
        ("extends", "Name the Feeling", "Naming emotion without punishment keeps reporting honest"),
    ],
    "reconciliation-before-worship": [
        ("extends", "Listen Before Fixing", "Repair starts by hearing what still hurts"),
        ("implements", "Follow Their Lead", "Leave the altar — go on their thread first"),
    ],
    "the-golden-rule": [
        ("extends", "Follow Their Lead", "I'd want someone to enter my world before fixing mine"),
        ("extends", "Listen Before Fixing", "I'd want to be heard before being handed advice"),
        ("extends", "Create Regular Connection", "I'd want steady presence, not one grand gesture"),
        ("extends", "Notice the Good", "I'd want someone to name what I did well, not vague good job"),
    ],
    "plain-commitments-at-work": [
        ("extends", "Set Calm Boundaries", "Plain yes/no at work uses the same steady-voice muscle"),
    ],
    "slow-the-moment": [
        ("implements", "Listen Before Fixing", "One beat before the fix lands"),
        ("implements", "Name the Feeling", "Pause before the label or the lecture"),
        ("implements", "Set Calm Boundaries", "Steady voice needs a beat first"),
    ],
    "self-control": [
        ("extends", "Listen Before Fixing", "Restraint is not interrupting with the answer"),
    ],
    "forgiveness-at-work": [
        ("extends", "Set Calm Boundaries", "Release the grudge; keep boundaries where trust still rebuilds"),
    ],
    "golden-rule-at-work": [
        ("extends", "Listen Before Fixing", "Treat them how I'd want — heard before fixed"),
        ("extends", "Follow Their Lead", "Reverse roles includes entering their thread first"),
    ],
    "reconcile-before-the-review": [
        ("extends", "Listen Before Fixing", "Repair starts by hearing what still hurts"),
        ("implements", "Follow Their Lead", "Coffee first — go on their thread before the slides"),
    ],
    "servant-leadership": [
        ("extends", "Follow Their Lead", "Serve by joining their world before redirecting credit"),
        ("extends", "Notice the Good", "Name what the team did — don't grab the praise slide"),
    ],
}

# Future-note extends (broken wikilink OK)
FUTURE_EXTENDS: dict[str, list[tuple[str, str]]] = {
    "building-a-second-brain": [("CODE Method", "Capture → Organize → Distill → Express pipeline Forte names")],
    "capture": [("Frictionless Capture", "Zero-friction inbox is the habit this note assumes")],
    "daily-notes": [("Fleeting Notes", "Scratch-pad lane before anything goes evergreen")],
    "digital-garden": [("Work in Progress", "Public drafts and visible growth — garden ethos")],
    "evergreen-notes": [("Permanent Notes", "Ahrens-style durable phrasing this note targets")],
    "gtd-vs-para": [("Getting Things Done", "Allen task-inbox system on the other side of the comparison")],
    "para-method": [("Getting Things Done", "Action-first capture Forte built PARA on top of")],
    "pkm": [("Personal Knowledge Management", "Umbrella term this garden sits under")],
    "progressive-summarization": [("Layered Reading", "Bold/highlight layers before rewrite — same distill move")],
    "slow-productivity": [("Deep Work", "Fewer deep projects — Newport's focus frame nearby")],
    "spaced-repetition": [("Forgetting Curve", "Ebbinghaus decay curve spaced repetition fights")],
    "the-12-week-year": [("Quarterly Planning", "Sprint scoreboard rhythm this method compresses")],
    "the-trusted-inbox": [("Inbox Zero", "Empty-the-inbox discipline this pipe depends on")],
    "pareto-principle": [("Vilfredo Pareto", "80/20 origin story — worth its own note later")],
    "sunk-cost-fallacy": [("Behavioral Economics", "Bias cluster this fallacy belongs to")],
    "anti-fragile-systems": [("Antifragility", "Taleb term — systems that gain from stress")],
    "first-principles-thinking": [("Elon Musk", "Famous modern example of strip-to-basics reasoning")],
    "minimum-viable-product": [("Lean Startup", "Ship-to-learn loop Ries named")],
    "local-first-software": [("CRDT", "Sync-without-server tech local-first apps use")],
    "mind-mapping": [("Tony Buzan", "Named mind-map method this note contrasts with atoms")],
    "the-feynman-technique": [("Richard Feynman", "Explain-like-I'm-twelve method named after him")],
    "drafting-in-public": [("Learning in Public", "Swyx frame — ship drafts, invite feedback")],
    "note-relationships": [("Link Typing", "Generic PKM term for what this page formalizes")],
    "analog-capture-tools": [("Commonplace Book", "Historical paper capture habit — same low-friction lane")],
    "building-a-personal-api": [("Webhooks", "Push events out — API glue this note imagines")],
    "compounding": [("Habit Stacking", "Small repeats that stack — same compounding mechanic")],
    "context-aware-capture": [("Voice Memos", "Capture in context — phone mic is the obvious tool")],
    "creative-blocks": [("Writer's Block", "Named stuck state this note tries to break")],
    "digital-minimalism": [("Attention Economy", "What Newport is pushing back on")],
    "digital-serendipity": [("Serendipity", "Happy accident discovery — the noun behind the method")],
    "evergreen-vs-fleeting-notes": [("Note Maturity", "Stages a note passes through — future lifecycle note")],
    "future-proofing-knowledge": [("Plain Text Files", "Boring format that survives app churn")],
    "graph-view-analytics": [("Network Analysis", "Graph metrics borrowed from network science")],
    "intellectual-sourcing": [("Literature Notes", "Source-first lane before synthesis")],
    "metadata-strategy": [("Taxonomy", "Tag-and-category design this note sizes")],
    "mobile-capture-workflows": [("Share Sheet", "OS capture surface most phone workflows use")],
    "signal-vs-noise": [("Information Diet", "What you let in — filter frame next to capture")],
    "synthesis-as-a-goal": [("Literature Notes", "Source notes you merge before belief")],
    "the-collectors-fallacy": [("Read Later Queue", "Where hoarding hides — pile without express")],
    "the-garage-concept": [("Sketchpad", "Private workshop before anything goes public")],
    "the-knowledge-lifecycle": [("Note Maturity", "Seedling → evergreen stages this note names")],
    "the-second-brain-workflow": [("CODE Method", "Capture–Organize–Distill–Express loop in motion")],
    "maps-of-content": [("Table of Contents", "Hand-written TOC — what a MOC is at heart")],
    "process-over-outcomes": [("Systems Thinking", "Trust the loop, not the scoreboard")],
    "active-knowledge-curation": [("Gardening Metaphor", "Prune and tend — same curator job")],
    "periodic-knowledge-review": [("Maintenance Window", "Scheduled upkeep — same calendar habit")],
}


def link(title: str) -> str:
    return f"[[{title}]]"


def split_fm(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    return text[: end + 4], text[end + 4 :].lstrip("\n")


def get_scalar(fm: str, key: str) -> str | None:
    m = re.search(rf'^{key}:\s*"(.*)"\s*$', fm, re.M)
    return m.group(1) if m else None


def set_note_kind(fm: str, kind: str) -> str:
    if re.search(r"^note_kind:", fm, re.M):
        return re.sub(r'^note_kind:\s*".*"', f'note_kind: "{kind}"', fm, count=1, flags=re.M)
    # after opening ---
    return fm.replace("---\n", f'---\nnote_kind: "{kind}"\n', 1)


def parse_rows(section: str) -> list[tuple[str, str, str]]:
    rows = []
    for line in section.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        typ, wikilink, reason = m.groups()
        if typ == "index":
            continue
        rows.append((typ, wikilink, reason))
    return rows


def row_key(row: tuple[str, str, str]) -> str:
    return f"{row[0]}|{row[1].lower()}"


def merge_rows(existing: list[tuple[str, str, str]], slug: str) -> list[tuple[str, str, str]]:
    seen = {row_key(r) for r in existing}
    out = list(existing)

    for typ, title, reason in ADD.get(slug, []):
        r = (typ, link(title), reason)
        k = row_key(r)
        if k not in seen:
            out.append(r)
            seen.add(k)

    for title, reason in FUTURE_EXTENDS.get(slug, []):
        r = ("extends", link(title), reason)
        k = row_key(r)
        if k not in seen:
            out.append(r)
            seen.add(k)

    out.sort(key=lambda r: (TYPE_ORDER.get(r[0], 99), r[1].lower()))
    return out


def format_table(rows: list[tuple[str, str, str]]) -> str:
    lines = [
        "## Note Relationships",
        "",
        "| Relationship | Wikilink | Reason |",
        "|--------------|----------|--------|",
    ]
    for typ, wikilink, reason in rows:
        lines.append(f"| {typ} | {wikilink} | {reason} |")
    return "\n".join(lines)


def replace_table(body: str, table: str) -> str:
    m = re.search(r"(?ms)^## Note Relationships\s*\n(\|[^\n]*\n)+", body)
    if not m:
        return body
    after = body[m.end() :]
    if after.startswith("\n## "):
        after = after[1:]
    elif after.startswith("\n\n## "):
        pass
    elif after.startswith("\n") and not after.startswith("\n\n"):
        after = "\n" + after
    return body[: m.start()].rstrip() + "\n\n" + table + ("\n" + after if after else "")


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    slug = path.stem
    if get_scalar(fm, "note_kind") == "meta":
        return False

    changed = False

    if slug in INDEX_SLUGS:
        new_fm = set_note_kind(fm, "index")
        if new_fm != fm:
            fm = new_fm
            changed = True

    if "## Note Relationships" not in body:
        return changed and path.write_text(fm + "\n" + body, encoding="utf-8") or changed

    section = body.split("## Note Relationships", 1)[1].split("\n## ", 1)[0]
    rows = parse_rows(section)
    new_rows = merge_rows(rows, slug)
    new_table = format_table(new_rows)
    new_body = replace_table(body, new_table)
    if new_body != body:
        body = new_body
        changed = True

    if changed:
        path.write_text(fm + "\n" + body, encoding="utf-8")
    return changed


def main() -> None:
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        if process_file(path):
            n += 1
            print("updated:", path.name)
    print(f"done: {n} files")


if __name__ == "__main__":
    main()
