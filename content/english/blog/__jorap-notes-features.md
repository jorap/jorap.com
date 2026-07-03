---
title: "What JoRap Notes Actually Does"
meta_title: "JoRap Notes - Features and How the Garden Works"
description: "My blog is for essays. JoRap Notes is a linked garden of one-claim pages - graph, flashcards, typed links, and copy buttons for AI - all on the same Hugo site."
slug: "jorap-notes-features"
date: 2026-07-03T02:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Digital Garden", "PKM", "Note Taking", "Hugo", "Wiki", "Flashcards", "Second Brain", "Website Building", "Markdown", "Publishing"]
related_notes:
  - digital-garden
  - getting-started
  - note-relationships
  - flashcards
  - maps-of-content
  - the-garage-concept
featured: false
draft: true
---

> **TL;DR**: JoRap Notes is not a separate app. It is a second surface on this site - short linked pages, each holding one claim I'd say out loud, with a graph, flashcard review, typed relationships, and copy buttons that hand the whole garden to ChatGPT. The blog is for long essays. The garden is for ideas I want to walk through.

## Two surfaces, one site

If you have only read my blog posts, you have seen half the site.

Blog posts live at `/blog/`. They are long-form - stories, tutorials, gear picks, recipes. A post might take an hour to write and ten minutes to read.

The notes garden lives at `/notes/`. Each page is one idea - a principle about work, a faith concept, a PKM habit. Most notes fit on one screen. You are meant to hop between them with links, not read them front to back like a book.

Same Hugo build. Same theme. Same push-to-GitHub workflow. Different shape of thinking.

I built the hosting stack first (Hugo, GitHub, Cloudflare - [that story is here](/blog/how-i-built-jorap-notes/)). The garden grew on top once I had a place to put linked notes in public without paying for a wiki host.

---

## One note, one claim

The atomic rule sounds strict until you try it.

**One note = one claim** I'd cite in conversation. If I need an "and" to finish the sentence, I split it into two notes and link them.

Each atomic note stores its whole argument in frontmatter - not in the body:

- **description** - one breath. What is this idea?
- **key_concept** - the angle, not a second definition. Stakes, distinctions, `[[wikilinks]]`.
- **examples** - exactly two scenes from different parts of life (jeepney and deploy, clinic and group chat - not two tweaks of the same story).
- **relationships** - typed links to other notes (more on that below).

Hugo assembles `## Key Concept`, `## Examples`, and `## Note Relationships` at build time. The Markdown body stays empty for atomic notes. That keeps every note the same shape when you browse, copy, or export.

Hub pages like [Maps of Content](/notes/maps-of-content/) break the rule on purpose. They are indexes - curated lists with prose in the body. Tool pages like [Graph](/notes/graph/) and [Review](/notes/review/) are meta surfaces, not garden ideas. You link to those by URL, not `[[wikilink]]`.

---

## Wikilinks and aliases

Linking is the whole point.

In note text I write `[[Golden Rule at Work]]` and Hugo resolves it to `/notes/golden-rule-at-work/`. If a note has an alias - say `aliases: ["PARA"]` on the PARA note - `[[PARA]]` works too.

On every note page you get:

- **Outgoing links** - where this note points
- **Backlinks** - who points here, with a snippet of the sentence around the link
- **See also** - tag-related notes I have not linked yet (build-time suggestions, not hand-curated)
- **Hover previews** - pause on a wikilink to peek at the target's title and description

Pipe labels (`[[note|display text]]`) are not supported. I kept the resolver simple on purpose.

---

## Typed relationships, not just "related"

Two notes can mention the same word and mean opposite things. A flat "related notes" list hides that.

Every atomic note carries a `relationships` table in frontmatter with four types:

| Type | What it means |
|------|----------------|
| **extends** | This builds on that |
| **contradicts** | Tension, exception, tradeoff |
| **implements** | This makes that operational |
| **alternative** | Different path, similar job |

Each row has a one-line **reason** - telegraphic is fine. "Rollback first; after-action review after calm" beats a paragraph.

Minimum on every atomic note: at least one `extends` and one `contradicts`. That forces me to place the idea in a graph of push and pull, not a pile of definitions.

The [Graph](/notes/graph/) view shows the same links as edges. Filters let you hide noisy nodes, surface orphans, or focus on notes with few body links. It runs in the browser with PixiJS - only loads on the graph page, not on every note.

---

## Tool pages

These are built-in utilities, not ideas in the garden:

| Tool | URL | What it does |
|------|-----|--------------|
| **List** | [/notes/](/notes/) | Filterable index; featured random note at the top |
| **Graph** | [/notes/graph/](/notes/graph/) | Network map with filters |
| **Issues** | [/notes/issues/](/notes/issues/) | Broken wikilinks, pipe links, unlinked mentions |
| **Backlinks** | [/notes/backlinks/](/notes/backlinks/) | Garden-wide backlink index |
| **Flashcards** | [/notes/flashcards/](/notes/flashcards/) | Browse cards by set |
| **Review** | [/notes/review/](/notes/review/) | Spaced-repetition quiz in the browser |
| **Random Duo** | [/notes/random-duo/](/notes/random-duo/) | Two random notes plus a "how do these connect?" prompt |
| **Create Note** | [/notes/create/](/notes/create/) | Type a topic, get a lint-ready AI prompt for one atomic note |
| **OKF Export** | [/notes/okf-export/](/notes/okf-export/) | Full garden bundle for agents |

Utility pages are excluded from the graph node set and from random pickers. Lint catches `[[wikilink]]` to a tool page from content notes - those links belong as URLs.

---

## Copy buttons (for humans and agents)

Every note page has **Copy MD** in the corner. One click copies the raw Hugo source - frontmatter and all - for pasting into an editor or ChatGPT.

**Agent copy** sits beside it. Same note, but wikilinks resolved to real URLs and formatted for the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) export pipeline. I use this when I want an AI session to know what the garden already claims without re-explaining fifty notes.

Hub pages add **Copy hub cluster** - the hub plus every note it wikilinks to, in one paste.

The full garden exports to `/exports/okf/` on every production build. Static viz included. Regenerate locally with `pnpm export:okf`.

---

## Flashcards and review

About twenty percent of notes opt into flashcards (`review: true`). These are habit-spine ideas - gospel, capture, linking, workplace ethics - things I want loaded when life shows up, not just understood once.

Each review note carries scenario cards in frontmatter:

- **Front** - a moment I'd recognize (no multiple choice, no telegraphing the answer)
- **Back** - what I'd do, decide, or say in one breath

Card count scales with importance: six on core PKM and faith spine notes, fewer on secondary topics. `card_sets` groups them so Review can filter by Capture, Faith, Eternal Principles, and so on.

[/notes/review/](/notes/review/) runs spaced repetition in the browser. Progress lives in `localStorage` on your device - no account, no server. Flip animation respects `prefers-reduced-motion`.

I can also export to Anki when I want drills on my phone. The garden stays the source; Anki is a mirror.

---

## Issues and lint (the boring guardrails)

A garden rots when links break and nobody notices.

[/notes/issues/](/notes/issues/) aggregates warnings garden-wide: broken `[[wikilinks]]`, pipe syntax I do not support, note titles mentioned in prose without a link. Warnings also show on the affected note page.

Before deploy, `pnpm lint:garden` checks frontmatter shape, flashcard rules, utility-link violations, and voice lint (plain words, no em dashes). `pnpm lint:notes` fails the build on broken wikilinks. Created and updated dates come from the file itself at build time - I do not maintain `lastmod` by hand.

These are not features you brag about at a party. They are why the graph still works six months after I wrote half the notes on a tired Sunday.

---

## Blog and garden together

Blog posts can declare `related_notes` in frontmatter - slugs of garden notes that extend the essay. The note page does not automatically link back, but the blog single surfaces the bridge.

When a note outgrows one screen, I distill it into a blog post under `content/english/blog/`. The note stays the atomic claim; the post is the story around it.

Faith notes, PKM notes, and workplace principles share the same machinery. Only the subject changes.

---

## Who this is for (and who it is not)

**Good fit** if you already think in linked notes, want a public garden without a monthly wiki bill, and are fine editing Markdown in Git. The copy buttons and OKF export matter if you pair the garden with AI editing sessions.

**Bad fit** if you need real-time collaboration, a WYSIWYG editor for non-technical co-authors, or private notes behind a login. This is a static site. Everything published is public. Private thinking stays in Obsidian or TiddlyWiki; the subset I am willing to grow in public lands here.

I am not selling JoRap Notes as a product. It is my corner of the internet, documented in case the pattern helps you build your own.

---

## Where to start

- Walk the garden: [/notes/](/notes/)
- Read the rules: [Getting Started](/notes/getting-started/)
- Browse by hub: [Maps of Content](/notes/maps-of-content/)
- Pick a random pair: [Random Duo](/notes/random-duo/)
- Hosting and deploy: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/)

If you build something similar, start with one claim per file and working wikilinks. Add the graph, flashcards, and agent export after you have twenty notes worth linking - not before.
