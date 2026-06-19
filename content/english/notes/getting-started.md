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

Or add a `.md` file under `content/english/notes/`. Use the same frontmatter as blog posts (`title`, `meta_title`, `description`, `slug`, `date`, `image`, `categories`, `author`, `tags`, `featured`, `draft`) plus optional lifecycle fields:

- `status` — `seedling` (draft claim), `evergreen` (stable), `inbox` (unprocessed), or `archived`

Created and updated timestamps come from the file itself at build time (`scripts/noteFileDates.js`) — no manual date fields to maintain.

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
- **Graph** - map view with filters for notes with no links, overloaded notes, and dead ends at [/notes/graph/](/notes/graph/)
- **See also** - tag-related notes generated at build time (not static in markdown)
- **Hover previews** - pause on a wikilink to peek at the target note
- **Maps of Content** - hub index at [[Maps of Content]]
- **Status badges** - seedling/evergreen/inbox/archived on each note; stale filter uses file edit time on [/notes/](/notes/)
- **Resurfacing** - recently created list and random note on [/notes/](/notes/)

## Explore

- **Outgoing links** and **backlinks** (with snippets) show below each note.
- **See also** suggests tag-related notes you haven't linked yet.
- **Graph** at [/notes/graph/](/notes/graph/) maps connections - filter notes with no links, too many links, and dead ends.
- **Status filters** on [/notes/](/notes/) — inbox, stale (by file edit age), seedling, evergreen, archived.
- `npm run lint:notes` catches broken wikilinks and unlinked mentions at build time.

## Publish to the blog

When a note is ready for a longer-form post, I distill it into `content/english/blog/` with the same frontmatter shape and set `draft: false`.
