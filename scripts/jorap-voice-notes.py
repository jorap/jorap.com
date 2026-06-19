#!/usr/bin/env python3
"""Rewrite note leads and descriptions to JoRap voice: first person, no em dashes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SEE_ALSO = "## See also"

# Lead paragraph (before ## See also). First person, no **Title** — dictionary openers.
LEADS: dict[str, str] = {
    "active-knowledge-curation": (
        "Saving links isn't curation. I revisit monthly, prune what I wouldn't save again today, "
        "and connect what I actually care about."
    ),
    "advantages-of-digital-gardens": (
        "I prefer a garden over polishing every thought into a finished essay - "
        "messy, linked, and alive beats a portfolio of sealed posts."
    ),
    "analog-capture-tools": (
        "I love my wiki, but sometimes paper wins - meetings, sermons, "
        "the pocket notebook that survives a dead phone battery."
    ),
    "anti-fragile-systems": (
        "Fragile systems break when an app shuts down. I build around plain files, "
        "open formats, and exports I actually test."
    ),
    "associative-linking": (
        "Folders sort. Links think. I link so notes meet without me remembering every filename."
    ),
    "atomic-design-for-notes": (
        "I borrowed Brad Frost's atomic design for UI and applied it to notes - "
        "one idea per file, combinable later."
    ),
    "atomic-notes": (
        "An **atomic note** holds one claim or question. If I'm writing `and` too much, I split it. "
        "Link with `[[wikilinks]]`; let [[Maps of Content]] and backlinks do the organizing.\n\n"
        "**Rule of thumb:** one thing I'd say in conversation - "
        "\"why middle-click saves tab chaos\" is atomic; \"browser tips and meeting notes\" is not."
    ),
    "building-a-personal-api": (
        "My personal API isn't OAuth - it's consistent frontmatter, wikilinks, and folder shapes "
        "my tools can read without me re-explaining everything."
    ),
    "building-a-second-brain": (
        "My brain is for having ideas, not storing them. A Second Brain holds them - "
        "starting with [[Capture]]."
    ),
    "bullet-journaling": (
        "I don't bullet journal for pretty spreads. I use rapid logging when digital capture feels slow - "
        "tasks, events, notes on paper, migrated weekly."
    ),
    "capture": (
        "**Capture** is where [[PKM]] lives or dies. I save what resonates, not everything I see - "
        "and I keep one inbox I actually trust."
    ),
    "collaborative-knowledge": (
        "Most of my notes are solo, but teams need shared context too. "
        "I look for owners, edit norms, and one source of truth per topic."
    ),
    "context-aware-capture": (
        "A link without context is a mystery six weeks later. "
        "I capture why I saved something - project, mood, question - while it's still obvious."
    ),
    "creative-blocks": (
        "I have thousands of notes and still stare at a blank page sometimes. "
        "Creative blocks aren't solved by more capture - here's what actually unsticks me."
    ),
    "creative-output": (
        "Notes are inventory. Output is the point - blog posts, sermons, code, dinner experiments. "
        "Here's how I push from archive to shipped."
    ),
    "curation-as-creation": (
        "Selecting, ordering, and framing notes is creative work. I stopped treating curation as housekeeping."
    ),
    "daily-notes": (
        "**Daily Notes** are my scratch pad for the day - tasks, fragments, links. "
        "Not a diary. Not permanent by default."
    ),
    "digital-garden": (
        "My digital garden is where notes grow in public - linked, imperfect, alive."
    ),
    "digital-minimalism": (
        "Fewer apps, fewer sync layers, fewer notifications. "
        "My PKM got better when I stopped collecting tools."
    ),
    "digital-serendipity": (
        "Serendipity isn't luck for me - I build systems where old notes surprise me at the right time."
    ),
    "distraction-free-writing": (
        "Fullscreen, plain text, notifications off. I don't need a special app - "
        "I need fewer excuses to leave the sentence."
    ),
    "drafting-in-public": (
        "I publish rough ideas before they're finished. "
        "Drafting in public keeps me honest and makes the garden grow."
    ),
    "e2ee-security": (
        "End-to-end encryption matters when my notes are actually private. "
        "I balance convenience with what I'm willing to store in plain text."
    ),
    "evergreen-notes": (
        "I write evergreen notes to stay useful - timeless phrasing, clear claims, "
        "updated when reality changes."
    ),
    "evergreen-vs-fleeting-notes": (
        "Fleeting notes catch sparks. Evergreen notes hold truth. "
        "I need both lanes and a clear promotion path."
    ),
    "first-principles-thinking": (
        "When a note is just a quote from someone smarter, I add a section: "
        "what do I actually believe from scratch."
    ),
    "formatting-for-readability": (
        "Dense walls of text don't get reread. I format notes like I'd format a post - "
        "headings, bullets, bold for the point."
    ),
    "from-note-to-book": (
        "Books aren't written; they're compiled. My path from atomic notes to long-form is "
        "outline, link, expand."
    ),
    "future-proofing-knowledge": (
        "Future-proofing isn't predicting tech for me - it's plain text, open tools, "
        "and exports I test before I need them."
    ),
    "graph-view-analytics": (
        "Graph view looks sci-fi. Mostly I use it to find orphans, hubs, and notes I forgot to link."
    ),
    "gtd-vs-para": (
        "GTD runs my tasks. PARA runs my notes. They're cousins, not competitors - "
        "here's how I use both without doubling admin."
    ),
    "intellectual-sourcing": (
        "I cite sources in notes not for academia - so I can trust my own synthesis "
        "and find the original six months later."
    ),
    "interstitial-journaling": (
        "Between meetings and deep work, I jot what just happened and what's next. "
        "Interstitial journaling clears the buffer."
    ),
    "local-first-software": (
        "Local-first means my device holds the truth; sync is optional icing. "
        "That's how I want my brain's backup to behave."
    ),
    "mental-models-list": (
        "Mental models are shortcuts for thinking. I keep a short list of ones that survived "
        "contact with real decisions - not every model on Wikipedia."
    ),
    "metadata-strategy": (
        "Tags, categories, dates, aliases - metadata should help me find notes, not become a second job."
    ),
    "mind-mapping": (
        "Mind maps are for the messy first pass - branches, bubbles, relationships. "
        "I export to atomic notes after, not instead."
    ),
    "mobile-capture-workflows": (
        "Most sparks die on mobile because capture takes twelve taps. "
        "I reduced mine to share sheet → inbox."
    ),
    "newsletter-filtering": (
        "Newsletters are RSS with delivery guilt. I filter them to a label, batch read weekly, "
        "clip what resonates."
    ),
    "note-taking-for-researchers": (
        "Researchers drown in PDF highlights. I borrow lit-review habits: "
        "source notes, synthesis notes, never merge the two."
    ),
    "organization": (
        "Organization in [[PKM]] isn't a perfect tree - it's enough structure to find things when life gets loud."
    ),
    "para-method": (
        "**[[PARA]]** is how I sort notes by life responsibility - not by topic alphabet soup. "
        "Four buckets, clear questions."
    ),
    "periodic-knowledge-review": (
        "Notes rot without review. I calendar weekly and quarterly passes - inbox, projects, evergreens."
    ),
    "pkm": (
        "**PKM** is the boring name for how I save, organize, and use what I learn. "
        "Here's my unspectacular definition."
    ),
    "privacy-and-data-sovereignty": (
        "I want to control where my notes live, who can read them, and how they leave my machine."
    ),
    "process-over-outcomes": (
        "Results matter, but optimizing only for outcomes wins once. "
        "I optimize for a repeatable process that wins again and again."
    ),
    "progressive-summarization": (
        "I don't rewrite whole notes when I distill - bold, then highlight, then summarize "
        "when I actually reuse the note."
    ),
    "rss-for-research": (
        "RSS is how I research without Twitter. Subscribe to blogs, clip to notes, ignore the rest."
    ),
    "second-brain-daily-workflow": (
        "A Second Brain isn't only notes for me - it's how I move through the day: "
        "middle-click tabs, curated feeds, faster learning loops."
    ),
    "serendipitous-resurfacing": (
        "I design for resurfacing - systems that bring old notes back beat systems that only search "
        "what I remember to search for."
    ),
    "signal-vs-noise": (
        "Most content is noise. PKM fails if capture doesn't filter. "
        "I save signal - stuff that changes action or belief."
    ),
    "slip-box-history": (
        "The slip-box (Zettelkasten) wasn't magic software - Luhmann's physical note cards and links. "
        "History helps separate myth from method."
    ),
    "slow-productivity": (
        "**Slow Productivity** pushes back on busy-as-virtue. "
        "I run fewer active projects so notes become output, not backlog."
    ),
    "spaced-repetition-systems": (
        "SRS apps implement the algorithm; I supply the discipline. "
        "I keep Anki beside my wiki without merging them."
    ),
    "spaced-repetition": (
        "Spaced repetition schedules reviews before I forget. "
        "I use it for facts I need cold, not for whole wiki pages."
    ),
    "synthesis-as-a-goal": (
        "Collecting quotes isn't PKM for me. Synthesis means merging sources into what I believe and can defend."
    ),
    "the-12-week-year": (
        "Twelve-week years compress annual goals into quarters I actually feel. "
        "I map wiki projects to 12-week arcs."
    ),
    "the-archive-method": (
        "Archive isn't delete. It's moving finished work out of active PARA so today's projects breathe."
    ),
    "the-collectors-fallacy": (
        "Collecting articles feels like progress. It isn't. "
        "The collector's fallacy bit me until I tied saves to express deadlines."
    ),
    "the-feynman-technique": (
        "I explain notes like I'm teaching someone - gaps in my explanation show gaps in understanding."
    ),
    "the-future-of-pkm": (
        "AI, agents, new apps - PKM hype cycles spin. "
        "The future still looks like capture, connect, create, with better search."
    ),
    "the-garage-concept": (
        "The garage holds tools, scraps, experiments. The showroom is the blog. I don't confuse the two."
    ),
    "the-knowledge-lifecycle": (
        "Ideas have lifecycles in my vault: capture, active use, evergreen, decay, archive. "
        "I match effort to stage."
    ),
    "the-power-of-interconnectivity": (
        "A note's value for me lives in what it connects to - files become a network I think inside."
    ),
    "the-second-brain-workflow": (
        "CODE and PARA in one loop: capture to inbox, organize by project, distill on use, express weekly."
    ),
    "the-trusted-inbox": (
        "If I don't trust my inbox, I capture in my head instead. One pipe, weekly empty, no exceptions."
    ),
    "the-zettelkasten-myth": (
        "Luhmann's output wasn't copy-paste from buying the right notebook. "
        "The Zettelkasten myth oversells tools and undersells writing."
    ),
    "there-is-no-perfect-solution": (
        "Waiting for the perfect tool, plan, or answer feels responsible. It's often the nirvana fallacy. "
        "Here's why I choose good-enough tradeoffs on purpose."
    ),
    "visual-thinking": (
        "Some thoughts need boxes and arrows before words. "
        "Visual thinking in PKM means diagrams beside Markdown."
    ),
    "weekly-review-checklists": (
        "My weekly review is a checklist - inbox, calendar, projects, one express action. Boring on purpose."
    ),
    "zettelkasten": (
        "**Zettelkasten** is one [[Atomic Notes|atomic]] idea per note, dense links, writing from the network."
    ),
}

# Second paragraph fixes (from enrich-evergreen-notes.py) - you → I where needed.
PARA2_FIXES: dict[str, str] = {
    "evergreen-notes": (
        "I write in complete sentences I'd still stand behind in two years. "
        "Revise when tools change, not when trends spike. "
        "Promotion from fleeting: during [[Periodic Knowledge Review]], when a spark keeps returning."
    ),
    "zettelkasten": (
        "I write notes I'd link to, not notes I'd folder. "
        "Density of links matters more than count of files. "
        "History in [[Slip-box History]]; myths in [[The Zettelkasten Myth]]."
    ),
    "atomic-notes": (
        "I split when I need `and` twice. Link when ideas touch. "
        "[[Maps of Content]] collect clusters; backlinks show what I forgot I wrote. "
        "The graph is the organization."
    ),
    "progressive-summarization": (
        "Layer one: bold the good sentences. Layer two: highlight the best bold. "
        "Layer three: summary at top - only when I reach for the note a second time. "
        "Distill on demand, not on save. Part of CODE's distill step."
    ),
}

DESCRIPTIONS: dict[str, str] = {
    "atomic-notes": "One idea per note, written to stand alone and link freely - not mini blog posts.",
    "building-a-second-brain": (
        "My brain is for having ideas, not storing them. "
        "A Second Brain is the system that holds them - starting with capture."
    ),
    "digital-garden": (
        "My digital garden is a personal site where notes grow in public - linked, imperfect, alive."
    ),
    "metadata-strategy": (
        "Tags, categories, dates, aliases - metadata should help me find notes, not become a second job."
    ),
    "pkm": "PKM is the boring name for how I save, organize, and use what I learn. Here's my unspectacular definition.",
    "privacy-and-data-sovereignty": (
        "I want to control where my notes live, who can read them, and how they leave my machine."
    ),
    "progressive-summarization": (
        "I don't rewrite whole notes when I distill - bold, then highlight, then summarize when I reuse."
    ),
    "second-brain-daily-workflow": (
        "A Second Brain isn't only notes for me - it's how I move through the day: "
        "middle-click tabs, curated feeds, and faster learning loops."
    ),
    "spaced-repetition": (
        "Spaced repetition schedules reviews before I forget. "
        "I use it for facts I need cold, not for whole wiki pages."
    ),
    "spaced-repetition-systems": (
        "SRS apps implement the algorithm; I supply the discipline. "
        "Here's how I fit Anki beside my wiki without merging them."
    ),
    "synthesis-as-a-goal": (
        "Collecting quotes isn't PKM for me. Synthesis is merging sources into what I believe and can defend."
    ),
    "the-feynman-technique": (
        "I explain notes like I'm teaching someone - gaps in my explanation show gaps in understanding."
    ),
    "the-power-of-interconnectivity": (
        "A note's value for me lives in what it connects to. "
        "Interconnectivity turns files into a network I think inside."
    ),
    "the-trusted-inbox": (
        "If I don't trust my inbox, I capture in my head instead. One pipe, weekly empty, no exceptions."
    ),
    "future-proofing-knowledge": (
        "Future-proofing isn't predicting tech for me. "
        "It's plain text, open tools, and exports I test before I need them."
    ),
    "the-12-week-year": (
        "Twelve-week years compress annual goals into quarters I actually feel. "
        "I map wiki projects to 12-week arcs."
    ),
    "digital-serendipity": (
        "Serendipity isn't random luck for me - it's building a system where old notes surprise me at the right time."
    ),
    "serendipitous-resurfacing": (
        "I design for resurfacing - old notes beat systems that only search what I remember to search for."
    ),
    "building-a-personal-api": (
        "My personal API isn't OAuth and microservices. "
        "It's structured context for future me and my tools without re-explaining everything."
    ),
    "evergreen-notes": (
        "I write evergreen notes to stay useful - timeless phrasing, clear claims, updated when reality changes."
    ),
    "the-garage-concept": (
        "The garage holds tools, scraps, experiments. The showroom is the blog. I don't confuse the two."
    ),
    "maps-of-content": (
        "A MOC is a curated index of notes on a topic - not a folder list, a table of contents I write by hand."
    ),
}

SKIP = {"graph"}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def extract_see_also(body: str) -> str:
    idx = body.find(SEE_ALSO)
    if idx == -1:
        return ""
    return body[idx:].rstrip() + "\n"


def main_paragraphs(body: str) -> list[str]:
    idx = body.find(SEE_ALSO)
    chunk = body[:idx] if idx != -1 else body
    parts = [p.strip() for p in re.split(r"\n\n+", chunk.strip()) if p.strip()]
    return parts


def no_em_dash(text: str) -> str:
    return text.replace("—", "-").replace("–", "-")


def update_description(fm_inner: str, stem: str) -> str:
    desc = DESCRIPTIONS.get(stem)
    if not desc:
        return fm_inner
    desc = no_em_dash(desc)
    if re.search(r'^description:\s*".*"', fm_inner, re.M):
        return re.sub(r'^description:\s*".*"', f'description: "{desc}"', fm_inner, count=1, flags=re.M)
    return fm_inner


def main() -> None:
    updated = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        stem = path.stem
        if stem in SKIP:
            continue

        text = path.read_text(encoding="utf-8")
        fm, fm_inner, body = split_frontmatter(text)
        see_also = extract_see_also(body)
        parts = main_paragraphs(body)

        new_parts: list[str] = []
        if stem in LEADS:
            lead = LEADS[stem]
            if "\n\n" in lead:
                new_parts.extend(p.strip() for p in lead.split("\n\n"))
            else:
                new_parts.append(lead)
            if stem in PARA2_FIXES:
                new_parts.append(PARA2_FIXES[stem])
            elif len(parts) > 1:
                new_parts.append(parts[1])
        elif stem == "getting-started":
            # Meta page: keep structure, fix voice touches in place.
            path.write_text(no_em_dash(text), encoding="utf-8")
            updated += 1
            print(f"em-dash pass: {path.name}")
            continue
        elif stem == "maps-of-content":
            new_body = (
                "**Maps of Content (MOCs)** are hub notes that index related ideas. "
                "I use pages like this to wander the garden.\n\n"
            )
            rest_idx = body.find("## Maps")
            if rest_idx != -1:
                new_body += body[rest_idx:]
            path.write_text(
                f"{fm}\n\n{no_em_dash(new_body.rstrip())}\n",
                encoding="utf-8",
            )
            updated += 1
            print(f"voice: {path.name}")
            continue
        elif stem == "_index":
            new_body = (
                "A personal note garden of **atomic notes** - one claim per page, linked with `[[wikilinks]]`. "
                "Start at [[Getting Started]] or [[Maps of Content]].\n"
            )
            path.write_text(f"{fm}\n\n{new_body}", encoding="utf-8")
            updated += 1
            print(f"voice: {path.name}")
            continue
        else:
            print(f"no lead mapping: {path.name}")
            continue

        new_body = "\n\n".join(no_em_dash(p) for p in new_parts)
        fm_inner = update_description(fm_inner, stem)
        fm_block = f"---\n{fm_inner}\n---"
        out = f"{fm_block}\n\n{new_body}\n\n{no_em_dash(see_also)}" if see_also else f"{fm_block}\n\n{new_body}\n"
        path.write_text(out, encoding="utf-8")
        updated += 1
        print(f"voice: {path.name}")

    # graph.md body
    graph = NOTES_DIR / "graph.md"
    gtext = graph.read_text(encoding="utf-8")
    if gtext.endswith("---\n"):
        graph.write_text(
            gtext.rstrip() + "\n\nForce-directed map of how my notes link. Open at [/notes/graph/](/notes/graph/).\n",
            encoding="utf-8",
        )
        print("voice: graph.md")

    print(f"\nDone: {updated} notes updated.")


if __name__ == "__main__":
    main()
