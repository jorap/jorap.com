#!/usr/bin/env python3
"""Add a second evergreen paragraph to each atomic note body."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {"_index", "graph", "maps-of-content", "getting-started"}
SEE_ALSO = "## See also"

# Second paragraph(s) appended after the lead claim. Use wikilinks; no em dashes.
ENRICHMENTS: dict[str, str] = {
    "active-knowledge-curation": (
        "Once a month I open old folders and ask: would I save this again today? "
        "If not, I delete or merge. Curation is [[Periodic Knowledge Review]] with teeth - "
        "fewer notes, stronger links, notes I actually open."
    ),
    "advantages-of-digital-gardens": (
        "Finished essays age fast. Garden notes can sit half-right, get linked, get updated. "
        "Readers see the thinking, not just the conclusion. That's closer to how ideas actually grow. "
        "See [[Drafting in Public]] and [[Digital Garden]]."
    ),
    "analog-capture-tools": (
        "Paper goes through the same rule as digital: one trusted inbox, processed weekly. "
        "I photograph or transcribe into [[Capture]] - the medium changes, the pipe doesn't. "
        "Meetings and sermons are where analog still wins for me."
    ),
    "anti-fragile-systems": (
        "If an app vanished tomorrow, could I still read my notes? "
        "Markdown in a folder, exports I test twice a year, no single gatekeeper. "
        "Stress should surface gaps, not erase years of work. See [[Future-Proofing Knowledge]] and [[Local-first Software]]."
    ),
    "associative-linking": (
        "When I write a note, I link to two neighbors minimum - what it extends, what it contradicts. "
        "Filenames fade; relationships stick. That's how [[Zettelkasten]] and a [[Digital Garden]] "
        "stay walkable without a perfect folder tree."
    ),
    "atomic-design-for-notes": (
        "Atoms stack into molecules: a claim note, a how-to note, a example note - linked, not merged. "
        "Same idea as [[Atomic Notes]], borrowed from UI work. Combinable beats monolithic every time."
    ),
    "atomic-notes": (
        "I split when I need `and` twice. Link when ideas touch. "
        "[[Maps of Content]] collect clusters; backlinks show what I forgot I wrote. "
        "The graph is the organization."
    ),
    "building-a-personal-api": (
        "For me that's consistent frontmatter, wikilinks, and folder shapes my tools can read - "
        "not a REST server in the closet. Agents and scripts work better when notes already speak a common language. "
        "See [[Metadata Strategy]]."
    ),
    "building-a-second-brain": (
        "CODE still frames it: [[Capture]], organize, distill, express. "
        "The system fails when any step is ornamental. I review whether each step still earns its place every quarter."
    ),
    "bullet-journaling": (
        "Rapid logging only: dot for task, dash for note, circle for event. "
        "No layout guilt. Friday means migrate open dots to [[Capture]] or drop them. "
        "Paper is a lane, not a second brain."
    ),
    "capture": (
        "Friction kills capture. One inbox, phone to desktop, weekly process - same as [[The Trusted Inbox]]. "
        "If I wouldn't act on it or cite it later, it doesn't get saved. Resonance is the filter, not FOMO."
    ),
    "collaborative-knowledge": (
        "Shared wikis need owners, edit norms, and a single source of truth per topic. "
        "I still keep a solo garden for thinking; team docs live where decisions stick. "
        "Different jobs, different homes."
    ),
    "context-aware-capture": (
        "One line of why beats a perfect title. "
        "\"For the sermon series\" or \"contradicts my take on X\" - future me needs the hook. "
        "Pairs with [[Intellectual Sourcing]] when the save is a quote or link."
    ),
    "creative-blocks": (
        "I pick one small express action: outline three bullets, publish a stub, record a voice memo. "
        "More [[Capture]] rarely helps; shipping something ugly does. "
        "See [[Creative Output]] and [[Process Over Outcomes]]."
    ),
    "creative-output": (
        "Every project gets an express deadline, even if it's just \"post one paragraph.\" "
        "Notes without output become [[The Collector's Fallacy]]. "
        "Inventory exists to leave the warehouse."
    ),
    "curation-as-creation": (
        "A [[Maps of Content]] is a curated playlist of ideas - order is an argument. "
        "Choosing what to include, what to cut, and what sits beside what is as creative as drafting new prose."
    ),
    "daily-notes": (
        "Morning dump, evening sweep. Fleeting by default - promote to evergreen during [[Periodic Knowledge Review]], "
        "not while the coffee's still hot. [[Daily Notes]] are a lane, not the archive."
    ),
    "digital-garden": (
        "Publish early, link often, revise in public. "
        "The opposite of a portfolio of polished essays. "
        "Mine follows [[The Garage Concept]]: messy workshop, curated showroom elsewhere."
    ),
    "digital-minimalism": (
        "One capture app, one wiki, one task list. Each new tool pays rent in sync and attention. "
        "When PKM felt heavy, the fix was subtraction, not another Notion template."
    ),
    "digital-serendipity": (
        "Backlinks, random walks through [[Maps of Content]], and review queues surface what search misses. "
        "Luck is designed: old notes meet new problems when the graph is dense enough."
    ),
    "distraction-free-writing": (
        "Plain Markdown, full screen, phone in another room. "
        "Fancy writing apps became another place to tweak instead of type. "
        "The goal is one uninterrupted paragraph, then another."
    ),
    "drafting-in-public": (
        "Rough posts beat perfect drafts in a folder. "
        "Readers correct me; I update the note. That's [[Evergreen Notes]] in practice - "
        "living text, not a sealed essay."
    ),
    "e2ee-security": (
        "Journal entries and credentials get encryption; blog drafts and garden notes stay plain text I can grep. "
        "Threat model first, then tools. See [[Privacy and Data Sovereignty]]."
    ),
    "evergreen-notes": (
        "I write in complete sentences I'd still stand behind in two years. "
        "Revise when tools change, not when trends spike. "
        "Promotion from fleeting: during [[Periodic Knowledge Review]], when a spark keeps returning."
    ),
    "evergreen-vs-fleeting-notes": (
        "Fleeting lives in [[Daily Notes]] and the inbox; evergreen lives where I link and teach from. "
        "The promotion question: is this still true, and would I cite it to a friend? "
        "If yes, rewrite in timeless voice and file as evergreen."
    ),
    "first-principles-thinking": (
        "I add a short \"from scratch\" block: assumptions, what would have to be true, what I'd bet on. "
        "Quotes stay attributed; my claim sits beside them. "
        "Pairs with [[Mental Models List]] and [[Synthesis as a Goal]]."
    ),
    "formatting-for-readability": (
        "Short paragraphs, bold on the claim, bullets only for real lists. "
        "If I won't reread a wall of text, neither will anyone else. "
        "Same rules as blog posts, tighter scope."
    ),
    "from-note-to-book": (
        "Start with a [[Maps of Content]] as the table of contents. "
        "Each chapter pulls linked [[Atomic Notes]]; gaps show up as missing links. "
        "Assembly writing: expand what's already true, don't invent from zero."
    ),
    "future-proofing-knowledge": (
        "Export quarterly. Open files in a plain editor. "
        "If it breaks, fix the pipeline now, not during a panic. "
        "[[Anti-Fragile Systems]] beat predictions about which app wins next year."
    ),
    "graph-view-analytics": (
        "Orphans mean missing links; hubs mean overloaded notes that should split. "
        "I don't worship the pretty picture - I fix what it accuses. "
        "See [[The Power of Interconnectivity]]."
    ),
    "gtd-vs-para": (
        "Tasks live in the task app with contexts and next actions. "
        "Reference and project material lives in [[PARA Method]] buckets. "
        "Overlap is fine; duplicate filing is the tax I refuse to pay."
    ),
    "intellectual-sourcing": (
        "Author, URL, date, and one line on why I cared - minimum viable citation. "
        "When I synthesize across sources, I can trace the chain and spot where I added opinion. "
        "See [[Note-Taking for Researchers]]."
    ),
    "interstitial-journaling": (
        "Thirty seconds between tasks: what happened, what's next, what's stuck in RAM. "
        "Clears the mental tab bar before deep work. "
        "Often feeds [[Capture]] or stays in [[Daily Notes]] until Friday."
    ),
    "local-first-software": (
        "Files on disk I own; sync is backup, not boss. "
        "Offline should work; online is a bonus. "
        "Same philosophy as [[Future-Proofing Knowledge]] - my notes survive plane mode and vendor whims."
    ),
    "mental-models-list": (
        "I keep maybe a dozen: inversion, second-order effects, opportunity cost, [[First Principles Thinking]]. "
        "Each gets its own note when it earns repeat use. "
        "The list is a [[Maps of Content]], not a Wikipedia binge."
    ),
    "metadata-strategy": (
        "Tags for broad themes, aliases for link targets, dates for publish not theology. "
        "If tagging takes longer than writing, the schema is wrong. "
        "See [[Context-Aware Capture]] for the fields that actually get used."
    ),
    "mind-mapping": (
        "Excalidraw or paper for the burst; then one idea per file. "
        "Maps are compost, not compost bins - they feed [[Atomic Notes]], they don't replace them."
    ),
    "mobile-capture-workflows": (
        "Share sheet to inbox, voice memo when walking, photo of whiteboard before the room clears. "
        "Twelve taps was a design failure I fixed once and stopped re-litigating."
    ),
    "newsletter-filtering": (
        "Gmail label, weekly batch, clip only what changes a project or belief. "
        "Same diet rules as [[RSS for Research]] - subscribe generously, process ruthlessly."
    ),
    "note-taking-for-researchers": (
        "Literature notes stay close to the source; permanent notes are my words only. "
        "Never highlight into a synthesis note without rewriting. "
        "Classic [[Zettelkasten]] hygiene that survives outside academia."
    ),
    "organization": (
        "[[PARA Method]] answers \"where does this live for my life right now?\" "
        "Topics answer \"what is this about?\" I need both, but life responsibility wins when I'm rushed."
    ),
    "para-method": (
        "Projects, Areas, Resources, Archive - four questions, not forty folders. "
        "If I can't name the project or area, it probably stays in Resources until it matters. "
        "See [[The Archive Method]] when work finishes."
    ),
    "periodic-knowledge-review": (
        "Weekly: inbox, calendar, one express action. "
        "Quarterly: prune dead links, promote sparks, archive stale projects. "
        "[[Weekly Review Checklists]] handle the rhythm; this note is the why."
    ),
    "pkm": (
        "Capture what matters, organize enough to find it, distill on reuse, express on schedule. "
        "Not a productivity cosplay - a backup brain for a life that's too loud to hold everything in RAM. "
        "Start at [[Getting Started]] or [[Building a Second Brain]]."
    ),
    "privacy-and-data-sovereignty": (
        "Know what's on whose server. "
        "Garden notes public by choice; journals and credentials stay local or encrypted. "
        "Export paths matter as much as passwords. See [[E2EE Security]]."
    ),
    "process-over-outcomes": (
        "I can't control every result; I can control showing up to the weekly review, the publish cadence, the capture habit. "
        "Outcomes still matter - but the process is what I rerun when motivation dips."
    ),
    "progressive-summarization": (
        "Layer one: bold the good sentences. Layer two: highlight the best bold. "
        "Layer three: summary at top - only when I reach for the note a second time. "
        "Distill on demand, not on save. Part of CODE's distill step."
    ),
    "rss-for-research": (
        "Feed reader, not timeline. Blogs I trust, batch read, clip to [[Capture]] with context. "
        "Twitter was infinite noise dressed as research; RSS is appointment reading."
    ),
    "second-brain-daily-workflow": (
        "Middle-click opens tabs I'll read later; feeds replace scroll holes; capture happens in the gaps. "
        "The wiki is the archive - the day is how stuff gets in. "
        "See [[The Second Brain Workflow]] for the full loop."
    ),
    "serendipitous-resurfacing": (
        "Spaced review, backlink browsing, and \"related notes\" beats hoping I'll remember to search. "
        "Design for rediscovery; memory is unreliable storage. "
        "Ties to [[Digital Serendipity]] and [[Periodic Knowledge Review]]."
    ),
    "signal-vs-noise": (
        "The filter question: will this change what I do or believe this month? "
        "If not, admire it and move on. "
        "[[Capture]] without filtering becomes [[The Collector's Fallacy]]."
    ),
    "slip-box-history": (
        "Luhmann wrote thousands of cards and thousands of pages - the method was writing, not stationery. "
        "Software can help; it can't substitute. See [[The Zettelkasten Myth]] before buying another app."
    ),
    "slow-productivity": (
        "Fewer active projects means notes become sermons and posts instead of guilt. "
        "Busy isn't depth. I'd rather finish three things than juggle twelve. "
        "Pairs with [[Process Over Outcomes]] and [[Creative Output]]."
    ),
    "spaced-repetition-systems": (
        "Anki for cards, wiki for ideas - separate lanes. "
        "Facts I need cold (language, definitions) get SRS; concepts live in linked notes. "
        "See [[Spaced Repetition]] for when the algorithm helps."
    ),
    "spaced-repetition": (
        "Vocabulary, definitions, scripture references - anything I'll be quizzed on or need instant recall for. "
        "Whole essays don't belong on flashcards. "
        "The wiki holds understanding; SRS holds drill."
    ),
    "synthesis-as-a-goal": (
        "After reading, one note in my words: what I think now, what would change my mind. "
        "Quotes are evidence, not the product. "
        "Without synthesis, [[PKM]] is a bookmark graveyard."
    ),
    "the-12-week-year": (
        "Twelve weeks is long enough to ship, short enough to feel urgent. "
        "Wiki project notes get a season tag; review at week twelve, archive or renew. "
        "Beats annual goals that die in February."
    ),
    "the-archive-method": (
        "Done means out of Projects, into Archive - searchable, not deleted. "
        "Active lists stay short; finished work stops stealing attention. "
        "Core [[PARA Method]] hygiene."
    ),
    "the-collectors-fallacy": (
        "I tied every save to a question: what will I make with this? "
        "No express action, no save - harsh, but the backlog shrank. "
        "Reading isn't learning until something leaves the notebook."
    ),
    "the-feynman-technique": (
        "I explain the note aloud or in a blank doc - no paste from the source. "
        "Where I stumble, the note gets a gap marker and a rewrite pass. "
        "Teaching exposes what highlighting hid."
    ),
    "the-future-of-pkm": (
        "Better search, agents that read my folders, sure - but capture, connect, create doesn't retire. "
        "New tools should shorten the loop, not replace thinking. "
        "Skepticism earns its keep every hype cycle."
    ),
    "the-garage-concept": (
        "Notes garden is the garage: experiments, half-ideas, tools scattered on benches. "
        "The blog is the showroom - cleaned up, narrative, guest-ready. "
        "Mixing them makes both worse."
    ),
    "the-knowledge-lifecycle": (
        "Not every note should be evergreen forever. "
        "Some decay honestly; some get archived; some get rewritten when the world shifts. "
        "Match effort to stage - see [[Evergreen vs Fleeting Notes]]."
    ),
    "the-power-of-interconnectivity": (
        "A note alone is a fact; a note in a graph is an argument. "
        "I ask on every edit: what should this link to that it doesn't yet? "
        "Density beats volume. See [[Associative Linking]]."
    ),
    "the-second-brain-workflow": (
        "Morning capture sweep, project filing when I touch a note, distill when I reuse, express before the week ends. "
        "Same loop whether the tool is TiddlyWiki or Hugo. "
        "See [[Second Brain Daily Workflow]] for the day-scale version."
    ),
    "the-trusted-inbox": (
        "Weekly process, no exceptions - even if it's twenty minutes. "
        "Trust is behavioral: if items disappear or rot, I'll stop using the pipe. "
        "One inbox, one owner, one rhythm."
    ),
    "the-zettelkasten-myth": (
        "The notebook didn't write the books; Luhmann did. "
        "Tools lower friction; they don't replace sentences. "
        "Buy plain text and a linking habit before another productivity pilgrimage."
    ),
    "there-is-no-perfect-solution": (
        "Good enough today beats optimal someday. "
        "I pick tools I can export, workflows I can repeat tired, tradeoffs I can name. "
        "Perfectionism dressed as research is still procrastination."
    ),
    "visual-thinking": (
        "Sketch the system before prose piles up. "
        "Boxes, arrows, ugly diagrams in the note - Excalidraw embeds fine. "
        "Complements [[Mind Mapping]]; both feed atomic notes after the picture clears."
    ),
    "weekly-review-checklists": (
        "Same list every Friday: empty inbox, scan calendar, review projects, one ship action. "
        "Boring is the feature - novelty in reviews means I'm reinventing the wheel. "
        "GTD's maintain phase, sized for a real week."
    ),
    "zettelkasten": (
        "I write notes I'd link to, not notes I'd folder. "
        "Density of links matters more than count of files. "
        "History in [[Slip-box History]]; myths in [[The Zettelkasten Myth]]."
    ),
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[: end + 4], text[end + 4 :].lstrip("\n")


def extract_see_also(body: str) -> str:
    idx = body.find(SEE_ALSO)
    if idx == -1:
        return ""
    return body[idx:].rstrip() + "\n"


def lead_paragraph(body: str) -> str:
    idx = body.find(SEE_ALSO)
    chunk = body[:idx] if idx != -1 else body
    return chunk.strip()


def already_enriched(lead: str, enrichment: str) -> bool:
    first_sentence = enrichment.split(".")[0].strip()
    return first_sentence in lead or enrichment[:40] in lead


def main() -> None:
    updated = 0
    skipped = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP:
            continue
        enrichment = ENRICHMENTS.get(path.stem)
        if not enrichment:
            print(f"no enrichment: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        see_also = extract_see_also(body)
        lead = lead_paragraph(body)
        if already_enriched(lead, enrichment):
            skipped += 1
            continue
        new_body = f"{lead}\n\n{enrichment.rstrip('.')}."
        path.write_text(f"{fm}\n\n{new_body}\n\n{see_also}", encoding="utf-8")
        updated += 1
        print(f"enriched: {path.name}")

    print(f"\nDone: {updated} enriched, {skipped} already done.")


if __name__ == "__main__":
    main()
