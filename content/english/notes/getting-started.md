---
note_kind: "index"
title: "Getting Started"
meta_title: "Getting Started - Notes Garden"
description: "Notes garden = one claim per page, wikilinks, public graph. How this site works and how to add your first note."
slug: "getting-started"
date: 2026-06-18T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Notes", "Meta", "PKM", "Digital Garden", "Note Taking", "Hugo", "Website Building"]
aliases: ["start"]
featured: true
draft: false
---
**Notes garden** = one claim per page, linked with `[[wikilinks]]`, browsable at [/notes/](/notes/).

Public when `draft: false`; hidden while `draft: true`. Each note opens with a definition I can quote in one breath - the graph and backlinks do the organizing. Start at [[Maps of Content]] or walk through the steps below. Faith parallel: [[Childlike Faith]] - beginner posture; receive the guide, don't perform expertise on day one.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| contradicts | [[Maps of Content]] | when jumping into a hub beats reading onboarding first |
| extends | [[Note Relationships]] | Getting started teaches the garden rules that note relationships formalize with typed links |
## Atomic rule

**One note = one claim** I'd cite in conversation. Optional **## Examples** (up to five concrete scenes, ranked best-first) when the claim needs it; required **## Note Relationships** table (extends + contradicts at minimum, sorted by type). No other `##` sections - link out instead. See [[Atomic Notes]] and [[Note Relationships]].

**Examples** - plain bullets, no genre labels. Mid-action scenes I might hit this week: jeepney, clinic, group chat, bedtime, inbox. Each bullet shows the principle firing, not a definition restated.

## Create a note

```bash
hugo new notes/my-idea.md
```

Or add a `.md` file under `content/english/notes/`. Use the same frontmatter as blog posts (`title`, `meta_title`, `description`, `slug`, `date`, `image`, `categories`, `author`, `tags`, `featured`, `draft`).

Created and updated timestamps come from the file itself at build time (`scripts/noteFileDates.js`) - no manual date fields to maintain.

## Link between notes

Use wikilinks in the body:

- `[[Atomic Notes]]` - link by title
- `[[atom]]` - works via the `aliases` frontmatter field

What this site gives you:

- **Wikilinks** - `[[Note Title]]` in note bodies (no pipe labels)
- **Aliases** - alternate link targets in frontmatter (`aliases: ["PARA"]` on [[PARA Method]])
- **Outgoing links** - listed below each note's body
- **Backlinks** - with context snippets when another note links here
- **Graph** - map view; filter by high, low, no body links, and orphans at [/notes/graph/](/notes/graph/)
- **Issues** - broken wikilinks, pipe wikilinks, and unlinked mentions at [/notes/issues/](/notes/issues/); also shown on each note
- **See also** - tag-related notes generated at build time (not static in markdown)
- **Hover previews** - pause on a wikilink to peek at the target note
- **Maps of Content** - hub index at [[Maps of Content]]
- **Resurfacing** - featured random note and [Random Duo](/notes/random-duo/) on [/notes/](/notes/)
- **Create Note** - topic → AI prompt for one lint-ready atomic note at [/notes/create/](/notes/create/)
- **Copy MD** - on every note page: copies Hugo source for ChatGPT or your editor
- **Copy hub cluster** - on hub/MOC pages (`note_kind: index`): hub + all direct wikilink targets in one paste
- **Copy catalog** - on [OKF Export](/notes/okf-export/): full garden index for ChatGPT project context
- **Copy issues** - on [Issues](/notes/issues/): structured link/structure report for maintenance sprints
- **Agent copy** - OKF handoff markdown per note (resolved links), upper right beside Copy MD
- **OKF export** - full bundle at [/notes/okf-export/](/notes/okf-export/) and [/exports/okf/](/exports/okf/)
- **Flashcards** - ~12 habit spine notes (~20%) with `review: true` carry six scenario `cards:` in frontmatter plus `card_sets:` for Review grouping; habit prompts I drill at [/notes/review/](/notes/review/)

## Page kinds

| `note_kind` | What it is | Relationships table | Link from content notes? |
|-------------|------------|---------------------|--------------------------|
| `note` (default) | Atomic garden claim | Required (extends + contradicts minimum) | Yes - `[[wikilink]]` |
| `index` | Hub / MOC ([[Maps of Content]], [[Eternal Principles]], this page) | Optional | Yes |
| `meta` | Tool surface (Graph, Issues, Review, etc.) | Skip | No - URL only |

## Utility surfaces (don't wikilink)

These pages are **meta tools** (`note_kind: meta`), not garden ideas: [Graph](/notes/graph/), [Issues](/notes/issues/), [Flashcards](/notes/flashcards/), [Review](/notes/review/), [Backlinks](/notes/backlinks/), [Random Duo](/notes/random-duo/), [Create Note](/notes/create/), [OKF Export](/notes/okf-export/). They are excluded from the graph node set, random pickers, and flashcard sources. **No `## Note Relationships` table** on utility pages - link by URL when pointing readers at a tool. **Don't `[[wikilink]]` to them** from content notes. `npm run lint:utility-links` catches violations.

## Explore

- **Outgoing links** and **backlinks** (with snippets) show below each note.
- **See also** suggests tag-related notes you haven't linked yet.
- **Graph** at [/notes/graph/](/notes/graph/) maps connections - filter high, low, no body links, and orphans.
- **Issues** at [/notes/issues/](/notes/issues/) lists broken wikilinks and unlinked note mentions; warnings also show on each affected note.
- `npm run lint:notes` catches broken wikilinks and unlinked mentions in the **body** at build time (frontmatter is not linted - use note titles freely in `cards:` and other fields).

## Publish to the blog

When a note is ready for a longer-form post, I distill it into `content/english/blog/` with the same frontmatter shape and set `draft: false`.
