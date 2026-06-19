---
title: "Getting Started"
meta_title: "Getting Started | Notes Garden"
description: "Notes garden = one claim per page, wikilinks, public graph. How this site works and how to add your first note."
slug: "getting-started"
date: 2026-06-18T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Notes", "Meta", "PKM", "Digital Garden", "Note Taking", "Hugo", "Website Building"]
aliases: ["start"]
status: evergreen
last_reviewed: 2026-06-19T08:00:00Z
featured: true
draft: false
---

**Notes garden** = one claim per page, linked with `[[wikilinks]]`, browsable at [/notes/](/notes/).

Public when `draft: false`; hidden while `draft: true`. Each note opens with a definition you can quote in one breath - the graph and backlinks do the organizing. Start at [[Maps of Content]] or walk through the steps below.

## Atomic rule

**One note = one claim** you'd cite in conversation. No `##` sections, no "bottom line" - link out instead. See [[Atomic Notes]].

## Create a note

```bash
hugo new notes/my-idea.md
```

Or add a `.md` file under `content/english/notes/`. Use the same frontmatter as blog posts (`title`, `meta_title`, `description`, `slug`, `date`, `image`, `categories`, `author`, `tags`, `featured`, `draft`) plus lifecycle fields:

- `status` — `seedling` (draft claim), `evergreen` (stable), `inbox` (unprocessed), or `archived`
- `last_reviewed` — ISO date; drives the stale filter on [/notes/review/](/notes/review/)

## Daily capture

```bash
hugo new notes/daily/$(date +%Y-%m-%d).md
```

Daily notes live under `content/english/notes/daily/`, start as `status: inbox` and `draft: true`, and appear in the [/notes/daily/](/notes/daily/) archive. Promote anything worth keeping during weekly review.

## Link between notes

Use wikilinks in the body:

- `[[Atomic Notes]]` - link by title
- `[[Atomic Notes|atoms]]` - link with custom label
- `[[atom]]` - works via the `aliases` frontmatter field

What this site gives you:

- **Wikilinks** - `[[Note Title]]` and `[[alias|label]]` in note bodies
- **Aliases** - alternate link targets in frontmatter (`aliases: ["PARA"]` on [[PARA Method]])
- **Outgoing links** - listed below each note's body
- **Backlinks** - with context snippets when another note links here
- **Graph** - force-directed view with orphan/hub/dead-end filters at [/notes/graph/](/notes/graph/)
- **See also** - tag-related notes generated at build time (not static in markdown)
- **Hover previews** - pause on a wikilink to peek at the target note
- **Maps of Content** - hub index at [[Maps of Content]]
- **Status & review** - seedling/evergreen/inbox/archived badges, [/notes/review/](/notes/review/) for inbox + stale notes
- **Resurfacing** - recently updated list and random note on [/notes/](/notes/)

## Explore

- **Outgoing links** and **backlinks** (with snippets) show below each note.
- **See also** suggests tag-related notes you haven't linked yet.
- **Graph** at [/notes/graph/](/notes/graph/) maps connections - filter orphans, hubs, and dead ends.
- **Weekly review** at [/notes/review/](/notes/review/) — inbox queue and notes past the review window.
- `npm run lint:notes` catches broken wikilinks and unlinked mentions at build time.

## Publish to the blog

When a note is ready for a longer-form post, I distill it into `content/english/blog/` with the same frontmatter shape and set `draft: false`.

## See also

- [[Maps of Content]]
- [[PKM]]
- [[Atomic Notes]]
- [[Building a Second Brain]]
