#!/usr/bin/env python3
"""Rewrite note leads and descriptions to JoRap voice: first person, no em dashes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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
        "**Atomic notes** = one claim I'd say out loud - too many `and`s, split it.\n\n"
        "**Rule of thumb:** one thing I'd cite in conversation - "
        "\"why middle-click saves tab chaos\" is atomic; \"browser tips and meeting notes\" is not.\n\n"
        "Small notes stack like Lego blocks - claim, how-to, example - linked, not merged. "
        "Link with `[[wikilinks]]`; let [[Maps of Content]] and backlinks do the organizing. "
        "If I need headings inside one file, I probably need two notes."
    ),
    "building-a-personal-api": (
        "My personal API isn't OAuth - it's consistent frontmatter, wikilinks, and folder shapes "
        "my tools can read without me re-explaining everything."
    ),
    "building-a-second-brain": (
        "**Second Brain** = offload ideas so my head can think, not hoard.\n\n"
        "Remember CODE: [[Capture]], organize, distill, express. The system fails when any step is just for show. "
        "I review whether each step still earns its place every quarter."
    ),
    "bullet-journaling": (
        "I don't bullet journal for pretty spreads. I use rapid logging when digital capture feels slow - "
        "tasks, events, notes on paper, migrated weekly."
    ),
    "capture": (
        "**Capture** = save what resonates into one inbox I trust - then empty it weekly.\n\n"
        "Friction kills capture. One inbox, phone to desktop, weekly process - same as [[The Trusted Inbox]]. "
        "If I wouldn't act on it or cite it later, it doesn't get saved. Resonance is the filter, not FOMO."
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
        "Graph looks sci-fi. Mostly I use it to sort notes by link frequency - high, low, no body links, and orphans."
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
    "slow-productivity": (
        "**Slow Productivity** pushes back on busy-as-virtue. "
        "I run fewer active projects so notes become output, not backlog."
    ),
    "spaced-repetition-systems": (
        "SRS apps implement the algorithm; I supply the discipline. "
        "I keep Anki beside my wiki without merging them."
    ),
    "spaced-repetition": (
        "**Spaced repetition** = review facts on a schedule before I forget - for recall, not whole essays.\n\n"
        "Vocabulary, definitions, scripture references - anything I'll be quizzed on or need instant recall for. "
        "Whole essays don't belong on flashcards. The wiki holds understanding; Anki or SRS apps hold drill - "
        "separate lanes, algorithm handles timing. In this garden, only ~12 spine notes (~20%) opt in with "
        "`review: true`, and cards target habits (what to do when) - not definition trivia."
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
    "compounding": (
        "**Compounding** = repeat small gains until they stack - keep showing up; the curve looks flat until it doesn't.\n\n"
        "Borrowed from finance, but it applies anywhere today's gain makes tomorrow easier: notes linked over years, "
        "publish cadence, vocab drills. Heroic weeks feel good; boring repetition wins. "
        "The first months look like nothing - that's the trap."
    ),
    "low-hanging-fruit": (
        "**Low hanging fruit** = the easy win I can grab now - do it before I climb for the hard stuff.\n\n"
        "Not every task deserves hero energy. Fix the broken link, publish the half-done draft, "
        "delete the folder I haven't opened in a year. Small, obvious, done today. "
        "I use it when I'm avoiding work by planning harder work."
    ),
    "pareto-principle": (
        "**Pareto principle** = most results come from a small slice of work - find the slice, protect it, cut the rest.\n\n"
        "Named for Vilfredo Pareto (roughly 80% of results from 20% of effort - shorthand, not a law). "
        "I use it when my reading list, task board, or note tags all feel equally important: "
        "which few actually moved the needle? Same rule for flashcards: only ~12 habit spine notes "
        "carry `review: true` here (~20% of the garden). Cards ask what I'd *do*, not what I'd *define*."
    ),
    "minimum-effective-dose": (
        "**Minimum effective dose** = the smallest change that still moves the needle - not the heroic overhaul.\n\n"
        "I borrowed it from medicine: enough to work, not more than needed. "
        "Applies to PKM habits, fitness, and side projects. More input past the dose is noise."
    ),
    "minimum-viable-product": (
        "**Minimum viable product** = the smallest thing I can ship that tests the idea - not a polished fantasy.\n\n"
        "I'd rather publish a rough note or prototype and learn than polish in private for months."
    ),
    "sunk-cost-fallacy": (
        "**Sunk cost fallacy** = keeping a bad tool, project, or note because I already invested time - not because it still earns its place.\n\n"
        "Past effort is gone. I ask: if I found this today, would I start it?"
    ),
    "note-relationships": "",  # handled specially - keeps table
    "flashcards": (
        "**Flashcards** = drill lane beside the wiki - opt in per note, export to Anki when I want SRS on my phone.\n\n"
        "Twelve habit spine notes (~20% of the garden) use `review: true` ([[Pareto Principle]] applied). "
        "Each carries six scenario cards in frontmatter - prompts ask what I'd *do* when capture, review, "
        "or linking breaks down, not what a term *means*. **Quiz yourself** at [/notes/review/](/notes/review/)."
    ),
    "review": (
        "**Review** = active recall in the browser - show the prompt, try the answer, rate myself. "
        "Progress saves in this browser only; I use Anki export when I want phone sync."
    ),
    "issues": (
        "**Garden link issues** = broken wikilinks and note titles mentioned in prose without a `[[wikilink]]` - listed below and on each affected note.\n\n"
        "**Missing note** means the wikilink target does not match any published note. "
        "**Unlinked mention** means another note's title appears in the body without a link. "
        "Frontmatter and flashcards are not checked - only the note body."
    ),
    "random-duo": (
        "Two notes from the garden, picked at random. I hit **Shuffle** for another pair."
    ),
    "random-trio": (
        "Three notes from the garden, picked at random. Shuffle all, or lock two and shuffle one column."
    ),
}

# Second paragraph fixes (from enrich-evergreen-notes.py) - you → I where needed.
PARA2_FIXES: dict[str, str] = {
    "evergreen-notes": (
        "I write in complete sentences I'd still stand behind in two years. "
        "Revise when tools change, not when trends spike. "
        "Promotion from fleeting: during [[Periodic Knowledge Review]], when a spark keeps returning."
    ),
    "progressive-summarization": (
        "Layer one: bold the good sentences. Layer two: highlight the best bold. "
        "Layer three: summary at top - only when I reach for the note a second time. "
        "Distill on demand, not on save. Part of CODE's distill step."
    ),
}

DESCRIPTIONS: dict[str, str] = {
    "atomic-notes": "One idea per note I'd cite in conversation - not mini blog posts.",
    "capture": "Capture is where my PKM lives or dies - one trusted inbox, save what resonates.",
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
    "note-relationships": (
        "Five link types I use in the body - extends, contradicts, implements, alternative, index."
    ),
    "pareto-principle": (
        "Most results come from a small slice of work - find that slice, protect it, cut the rest."
    ),
    "compounding": (
        "Small gains stack on each other - boring repetition beats heroic weeks until the curve bends."
    ),
    "flashcards": "Flip cards from opt-in notes - habit prompts, not trivia. Export the same deck to Anki.",
    "review": "Quiz myself on habit spine cards with spaced repetition in the browser.",
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
        if stem in LEADS and LEADS[stem]:
            lead = LEADS[stem]
            if "\n\n" in lead:
                new_parts.extend(p.strip() for p in lead.split("\n\n"))
            else:
                new_parts.append(lead)
            if stem in PARA2_FIXES:
                new_parts.append(PARA2_FIXES[stem])
            for p in parts:
                if (p.startswith("Extends ") or p.startswith("Contradicts ") or p.startswith("Implements ")) and p not in new_parts:
                    new_parts.append(p)
        elif stem == "note-relationships":
            opener = (
                "**Note relationships** = five link types I put in the body - extends, contradicts, "
                "implements, alternative, index - so the graph shows how ideas push and pull.\n\n"
            )
            table_idx = body.find("| Type |")
            if table_idx == -1:
                print(f"skip {path.name}: no table")
                continue
            tail = body[table_idx:]
            see_idx = tail.find(SEE_ALSO)
            main_chunk = tail[:see_idx].strip() if see_idx != -1 else tail.strip()
            # Fix third-person line in table section if present
            main_chunk = main_chunk.replace(
                "Every atomic note gets **extends** and **contradicts** in the body",
                "I give every atomic note **extends** and **contradicts** in the body",
            )
            new_body = opener + main_chunk
            fm_inner = update_description(fm_inner, stem)
            fm_block = f"---\n{fm_inner}\n---"
            out = f"{fm_block}\n\n{no_em_dash(new_body)}\n\n{no_em_dash(see_also)}" if see_also else f"{fm_block}\n\n{no_em_dash(new_body)}\n"
            path.write_text(out, encoding="utf-8")
            updated += 1
            print(f"voice: {path.name}")
            continue
        elif stem in {"flashcards", "review", "issues", "random-duo", "random-trio"}:
            lead = LEADS[stem]
            rel_line = ""
            if stem == "flashcards":
                rel_line = "\n\nExtends [[Getting Started]]. Implements [[Spaced Repetition]]."
            elif stem == "review":
                rel_line = "\n\nExtends [[Getting Started]]. Implements [[Spaced Repetition]]."
            elif stem == "issues":
                rel_line = "\n\nExtends [[Getting Started]]. Implements [[Graph View Analytics]]."
            elif stem == "random-duo":
                rel_line = "\n\nExtends [[Getting Started]]. Implements [[Digital Serendipity]]."
            elif stem == "random-trio":
                rel_line = "\n\nExtends [[Getting Started]]. Implements [[Digital Serendipity]]."
            fm_inner = update_description(fm_inner, stem)
            fm_block = f"---\n{fm_inner}\n---"
            path.write_text(f"{fm_block}\n\n{no_em_dash(lead)}{rel_line}\n", encoding="utf-8")
            updated += 1
            print(f"voice: {path.name}")
            continue
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
    fm, fm_inner, body = split_frontmatter(gtext)
    if "**Graph**" not in body:
        graph.write_text(
            gtext.rstrip()
            + "\n\n**Graph** = open the link map and filter by link frequency: high, low, no body links, orphans.\n",
            encoding="utf-8",
        )
        print("voice: graph.md")

    # Global em-dash pass on every note file
    dash_count = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        fixed = no_em_dash(raw)
        if fixed != raw:
            path.write_text(fixed, encoding="utf-8")
            dash_count += 1
    if dash_count:
        print(f"em-dash pass: {dash_count} files")

    print(f"\nDone: {updated} notes updated.")


if __name__ == "__main__":
    main()
