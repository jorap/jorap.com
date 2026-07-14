---
title: "What JoRap Notes Actually Does"
meta_title: "JoRap Notes - Features, Applications, and Principles"
description: "My blog is for essays. JoRap Notes is a linked garden of one-claim pages - graph, flashcards, typed links, all on the same Hugo site."
slug: "jorap-notes-features"
date: "2026-07-03T02:00:00Z"
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
  - workplace-principles
featured: false
draft: true
---

> **TL;DR**: JoRap Notes is not a separate app. It is a second surface on this site - short linked pages, each holding one claim I'd say out loud, with a graph, flashcard review, typed relationships, shareable thoughts, and copy buttons that hand the whole garden to ChatGPT. The blog is for long essays. The garden is for ideas I want to walk through and reuse.

## Two surfaces, one site

If you have only read my blog posts, you have seen half the site.

Blog posts live at `/blog/`. They are long-form - stories, tutorials, gear picks, recipes. A post might take an hour to write and ten minutes to read.

The notes garden lives at `/notes/`. Each page is one idea - a principle about work, a faith concept, a PKM habit. Most notes fit on one screen. You are meant to hop between them with links, not read them front to back like a book.

Same Hugo build. Same theme. Same push-to-GitHub workflow. Different shape of thinking.

I built the hosting stack first (Hugo, GitHub, Cloudflare - [that story is here](/blog/how-i-built-jorap-notes/)). The garden grew on top once I had a place to put linked notes in public without paying for a wiki host.

---

## Features at a glance

| Feature | What it does | Apply it when… |
|--------|--------------|----------------|
| **Atomic notes** | One claim per page; argument lives in frontmatter | You want a quote you'd actually say in a meeting, not a chapter |
| **Shareable thoughts** | Four self-contained ideas per note, shown on the page | You need a Slack reply, card pull-quote, or social post without rewriting |
| **Wikilinks + aliases** | `[[Note Title]]` resolves to the note; aliases catch shorthand | You think in links, not folder trees |
| **Typed relationships** | `extends`, `contradicts`, `implements`, `alternative` with a one-line reason | Two notes share a word but pull opposite ways - you need the tension visible |
| **Hub pages (MOCs)** | Curated indexes with prose; Copy hub cluster | One topic sprawled across twenty files and you need a hand-built map |
| **Graph** | PixiJS network map with link-density filters | You want to spot orphans, over-linked hubs, or missing bridges |
| **Flashcards + Review** | Scenario cards in frontmatter; spaced repetition in the browser | You want habits loaded when life shows up, not just understood once |
| **Copy MD / Agent copy** | Raw Hugo source or OKF-resolved markdown per note | You paste one note into an editor or AI session without re-explaining context |
| **OKF export** | Full garden bundle at `/exports/okf/` | You want an agent or project to know what the garden already claims |
| **Issues + lint** | Broken links, voice checks, frontmatter shape | You wrote half the garden on a tired Sunday and need it to still work in six months |
| **Random Duo** | Two random notes plus a connection prompt | You want serendipity without doom-scrolling your own index |
| **Create Note** | Topic → lint-ready AI prompt for one atomic note | You have a claim in your head and want the right frontmatter shape on the first try |
| **Blog bridge** | `related_notes` on essays links into the garden | A long post should hand readers the atomic claims behind the story |

---

## One note, one claim

The atomic rule sounds strict until you try it.

**One note = one claim** I'd cite in conversation. If I need an "and" to finish the sentence, I split it into two notes and link them.

Each atomic note stores its whole argument in frontmatter - not in the body:

- **description** - one breath. What is this idea? Twenty words max, no wikilinks.
- **key_concept** - the angle, not a second definition. Stakes, distinctions, `[[wikilinks]]`.
- **examples** - exactly two scenes from different parts of life (jeepney and deploy, clinic and group chat - not two tweaks of the same story).
- **shareable_thought** - four self-contained ideas I'd paste into Slack, a standup, or a caption without editing. Pulled from `description` and `key_concept` only - principle and angle, not examples. Max 130 characters each, plain text, no wikilinks.
- **relationships** - typed links to other notes (more on that below).

Hugo assembles `## Key Concept`, `## Examples`, `## Shareable thoughts`, and `## Note Relationships` at build time. The Markdown body stays empty for atomic notes. That keeps every note the same shape when you browse, copy, or export.

**Application:** When a coworker asks "what's your take on X?", you open one URL and read the description aloud. When you need a pull-quote for a deck, you grab a shareable thought. When an idea won't fit one breath, that's your signal to split.

**Principle:** Compression forces clarity. If you cannot state the claim in one sentence, you do not understand it yet - or you are smuggling two ideas into one file.

Hub pages like [Maps of Content](/notes/maps-of-content/) and [Workplace Principles](/notes/workplace-principles/) break the rule on purpose. They are indexes - curated lists with prose in the body. Tool pages like [Graph](/notes/graph/) and [Review](/notes/review/) are meta surfaces, not garden ideas. You link to those by URL, not `[[wikilink]]`.

---

## Shareable thoughts

Every note carries four **shareable thoughts** in frontmatter. They render in a grid on the note page - ready-made quotes you can copy without hunting through `key_concept`.

The rules are tight on purpose:

- Exactly four thoughts per note
- Max 130 characters each
- Plain text only - no `[[wikilinks]]`
- Pulled from `description` and `key_concept` only - the claim and its angle, not `examples` or relationship tension
- All four must be distinct - no duplicate claims or one thought that is a fragment of another

**Application:** Paste into Slack when someone asks for your framing. Drop into a slide without rewriting. Feed a social post. Hand an AI session a quotable summary without the full frontmatter dump.

**Principle:** Ideas you cannot quote are ideas you cannot reuse. Shareable thoughts are the garden's "out loud" layer - what you'd actually say when someone interrupts you mid-coffee.

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

**Application:** Write the way you think - name the idea, link it, move on. Backlinks surface connections you forgot you made. See also nudges you to link notes that share tags but not yet prose.

**Principle:** The graph is the product. Folders sort files; links sort ideas. A note nobody links to is a note nobody will find when they need it.

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

**Application:** Before you publish a new note, ask "what does this extend?" and "what does this push against?" The reason field is your future self explaining the link in one breath. Use the graph filter when a hub feels bloated or when you suspect duplicate claims.

**Principle:** Ideas live in tension. Naming `contradicts` keeps you honest about tradeoffs instead of pretending every note agrees with every other note.

---

## Tool pages

These are built-in utilities, not ideas in the garden:

| Tool | URL | What it does | Apply it when… |
|------|-----|--------------|----------------|
| **List** | [/notes/](/notes/) | Filterable index; featured random note at the top | You want to browse or rediscover without a plan |
| **Graph** | [/notes/graph/](/notes/graph/) | Network map with filters | You need the shape of the garden, not one page |
| **Issues** | [/notes/issues/](/notes/issues/) | Broken wikilinks, pipe links, unlinked mentions | You are doing a link-maintenance sprint |
| **Backlinks** | [/notes/backlinks/](/notes/backlinks/) | Garden-wide backlink index | You want "who points here?" across the whole garden |
| **Flashcards** | [/notes/flashcards/](/notes/flashcards/) | Browse cards by set | You want to see what is in the review deck before quizzing |
| **Review** | [/notes/review/](/notes/review/) | Spaced-repetition quiz in the browser | You have five minutes and want habit spine loaded |
| **Random Duo** | [/notes/random-duo/](/notes/random-duo/) | Two random notes plus a "how do these connect?" prompt | You want creative friction between distant ideas |
| **Create Note** | [/notes/create/](/notes/create/) | Type a topic, get a lint-ready AI prompt for one atomic note | You are starting a new claim and want the right shape |
| **OKF Export** | [/notes/okf-export/](/notes/okf-export/) | Full garden bundle for agents | You are seeding a ChatGPT project or agent workflow |

Utility pages are excluded from the graph node set and from random pickers. Lint catches `[[wikilink]]` to a tool page from content notes - those links belong as URLs.

---

## Copy buttons (for humans and agents)

Every note page has **Copy MD** in the corner. One click copies the raw Hugo source - frontmatter and all - for pasting into an editor or ChatGPT.

**Agent copy** sits beside it. Same note, but wikilinks resolved to real URLs and formatted for the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) export pipeline. I use this when I want an AI session to know what the garden already claims without re-explaining fifty notes.

Hub pages add **Copy hub cluster** - the hub plus every note it wikilinks to, in one paste.

[OKF Export](/notes/okf-export/) adds **Copy catalog** - the full garden index for seeding a ChatGPT project.

[Issues](/notes/issues/) adds **Copy issues** - a structured link and structure report for a maintenance sprint.

The full garden exports to `/exports/okf/` on every production build. Static viz included. Regenerate locally with `pnpm export:okf`.

**Application:** Copy MD when you are editing in your IDE. Agent copy when you are pair-writing with AI and need resolved links. Copy hub cluster when you are briefing someone on a whole topic lane. Copy catalog when you are onboarding an agent to the entire garden.

**Principle:** Your notes should travel. If copying context takes longer than writing the prompt, you will stop using the garden as source of truth.

---

## Flashcards and review

About twenty percent of notes opt into flashcards (`review: true`). These are habit-spine ideas - gospel, capture, linking, workplace ethics - things I want loaded when life shows up, not just understood once.

Each review note carries scenario cards in frontmatter:

- **Front** - a moment I'd recognize (no multiple choice, no telegraphing the answer)
- **Back** - what I'd do, decide, or say in one breath

Card count scales with importance: six on core PKM and faith spine notes, fewer on secondary topics. `card_sets` groups them so Review can filter by Capture, Faith, Eternal Principles, and so on.

[/notes/review/](/notes/review/) runs spaced repetition in the browser. Progress lives in `localStorage` on your device - no account, no server. Flip animation respects `prefers-reduced-motion`.

I can also export to Anki when I want drills on my phone. The garden stays the source; Anki is a mirror.

**Application:** Drill before the hard conversation, not after you fumbled it. Filter Review by `card_sets` when you only have five minutes. Use flashcard fronts as scenario prompts in team retros.

**Principle:** Understanding and recall are different jobs. The note holds the claim; the card holds the move you'd make when the claim meets real life.

---

## Issues, voice lint, and guardrails

A garden rots when links break and nobody notices.

[/notes/issues/](/notes/issues/) aggregates warnings garden-wide: broken `[[wikilinks]]`, pipe syntax I do not support, note titles mentioned in prose without a link. Warnings also show on the affected note page.

Before deploy, `pnpm lint:garden` checks frontmatter shape, flashcard rules, utility-link violations, shareable thought counts, title length, and voice lint (plain words, no em dashes). `pnpm lint:notes` fails the build on broken wikilinks. Created and updated dates come from the file itself at build time - I do not maintain `lastmod` by hand.

Titles stay short - four words by default, five only when the phrase is long enough to need the extra word (scripture lines, full principles). Descriptions stay under twenty words. Shareable thoughts stay under 130 characters. The linter enforces what my tired Sunday self would skip.

These are not features you brag about at a party. They are why the graph still works six months after I wrote half the notes on a tired Sunday.

**Application:** Run Issues before a big publish batch. Paste Copy issues into an AI session and ask for fix suggestions. Use voice lint when prose starts sounding like a textbook.

**Principle:** Constraints are features. The garden stays usable because broken links and vague titles fail the build instead of silently degrading.

---

## Blog and garden together

Blog posts can declare `related_notes` in frontmatter - slugs of garden notes that extend the essay. The note page does not automatically link back, but the blog single surfaces the bridge.

When a note outgrows one screen, I distill it into a blog post under `content/english/blog/`. The note stays the atomic claim; the post is the story around it.

Faith notes, PKM notes, and workplace principles share the same machinery. Only the subject changes. [Workplace Principles](/notes/workplace-principles/) is the clearest example of audience-specific application: the same ethics as [Eternal Principles](/notes/eternal-principles/), rewritten in language that fits a secular standup or 1:1.

**Application:** Write the essay once; link the claims you want readers to keep. When a team will not open a theology note, build a workplace hub that wikilinks back to the source when depth is needed.

**Principle:** Long form and atomic notes serve different memory. The post persuades; the note persists.

---

## Principles worth stealing

You do not need my exact Hugo setup to benefit from the pattern. These are the moves that pay off regardless of tool:

1. **One claim per file** - If you need "and" to finish the sentence, split. Compression is a clarity test.
2. **Links over folders** - Wikilinks and backlinks surface structure you did not plan. Folders hide it.
3. **Name the tension** - `extends` and `contradicts` beat a flat "related" list. Ideas live in push and pull.
4. **Quote-ready output** - Description, shareable thoughts, and flashcard backs are three registers of the same claim: define it, share it, apply it.
5. **Tools are not ideas** - Graph, Review, and Issues are meta pages. Keep garden notes about ideas; link to tools by URL.
6. **Agents eat structure** - Copy buttons and OKF export only matter if your notes are already shaped consistently. Garbage in, garbage out - but shaped garbage travels.
7. **Lint what you will not notice** - Broken links and vague titles rot quietly. Automate the boring checks so the garden survives your tired Sundays.
8. **Public subset, private garage** - Not everything belongs in the garden. [The Garage Concept](/notes/the-garage-concept/) stays draft or offline; the subset you are willing to grow in public lands here.
9. **Same ethics, different rooms** - Hub pages like Workplace Principles let one body of thought meet different audiences without duplicating the whole graph.
10. **Serendipity on purpose** - Random Duo and featured notes resurface ideas you wrote and forgot. The garden should surprise you, not just store you.

---

## Who this is for (and who it is not)

**Good fit** if you already think in linked notes, want a public garden without a monthly wiki bill, and are fine editing Markdown in Git. The copy buttons, shareable thoughts, and OKF export matter if you pair the garden with AI editing sessions or need quotable output for work.

**Bad fit** if you need real-time collaboration, a WYSIWYG editor for non-technical co-authors, or private notes behind a login. This is a static site. Everything published is public. Private thinking stays in Obsidian or TiddlyWiki; the subset I am willing to grow in public lands here.

I am not selling JoRap Notes as a product. It is my corner of the internet, documented in case the pattern helps you build your own.

---

## Where to start

- Walk the garden: [/notes/](/notes/)
- Read the rules: [Getting Started](/notes/getting-started/)
- Browse by hub: [Maps of Content](/notes/maps-of-content/)
- Office-friendly ethics lane: [Workplace Principles](/notes/workplace-principles/)
- Pick a random pair: [Random Duo](/notes/random-duo/)
- Hosting and deploy: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/)

If you build something similar, start with one claim per file and working wikilinks. Add shareable thoughts, the graph, flashcards, and agent export after you have twenty notes worth linking - not before.
