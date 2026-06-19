---
title: "Getting Started"
meta_title: "Getting Started | Notes Garden"
description: "How my linked notes garden works on this site - atomic claims, wikilinks, and a public graph."
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

My notes garden is **public** at [/notes/](/notes/). Set `draft: false` to publish a note; `draft: true` keeps it hidden until I'm ready.

## Atomic rule

One note = **one claim** I'd cite in conversation. No `##` sections, no "bottom line" - link out to other notes instead. See [[Atomic Notes]].

## Create a note

```bash
hugo new notes/my-idea.md
```

Or add a `.md` file under `content/english/notes/`. Use the same frontmatter as blog posts (`title`, `meta_title`, `description`, `slug`, `date`, `image`, `categories`, `author`, `tags`, `featured`, `draft`).

## Link between notes

Use wikilinks in the body:

- `[[Atomic Notes]]` - link by title
- `[[Atomic Notes|atoms]]` - link with custom label
- `[[atom]]` - works via the `aliases` frontmatter field

Obsidian-style features I wired on this site:

- **Wikilinks** - `[[Note Title]]` and `[[alias|label]]` in note bodies
- **Aliases** - alternate link targets in frontmatter (`aliases: ["PARA"]` on [[PARA Method]])
- **Backlinks** - listed at the bottom of each note when another note links here
- **Graph** - force-directed view of all wikilink connections at [/notes/graph/](/notes/graph/)
- **See also** - tag-related notes appended to most pages
- **Maps of Content** - hub index at [[Maps of Content]]

## Explore

- **Backlinks** show at the bottom of each note.
- **Graph** at [/notes/graph/](/notes/graph/) maps connections.

## Publish to the blog

When a note is ready for a longer-form post, I distill it into `content/english/blog/` with the same frontmatter shape and set `draft: false`.

## See also

- [[Maps of Content]]
- [[PKM]]
- [[Atomic Notes]]
- [[Building a Second Brain]]
