---
title: "Private Notes vs Hugo"
meta_title: "Private Notes vs Hugo - Garage vs Public Garden"
description: "I don't run a separate Obsidian vault anymore. Private captures stay in the garage; Hugo builds the public garden on jorap.com."
slug: "obsidian-vs-hugo"
date: "2026-06-19T06:00:00Z"
image: "/images/note.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "PKM", "Publishing", "Markdown", "Workflow", "Digital Garden", "Note Taking"]
related_notes:
  - the-garage-concept
  - drafting-in-public
  - future-proofing-knowledge
  - digital-garden
  - note-relationships
  - commonplace-book
featured: false
draft: true
---

For a year I ran **two homes** for the same ideas: a private wiki app for thinking, Hugo for the public site. Same topics, two places to maintain, and a Sunday every month where I'd copy a polished paragraph from one into the other and wonder why I hadn't just written it once.

I don't do that anymore. **JoRap Notes** is the public garden on this Hugo build. Private stuff stays in [the garage](/notes/the-garage-concept/) - drafts, offline captures, half-baked opinions - not a parallel vault I have to sync.

Private vs public isn't winner-take-all. It's two rooms in the same house.

---

## The weekend I stopped syncing

The breaking point was boring. I had a garden note about client handoffs half-written in the wiki and a blog draft stub in Hugo with overlapping paragraphs. I spent an afternoon reconciling which version was "true," fixed a broken wikilink in one app, exported markdown from the other, and still wasn't sure Git had the latest text.

Cutting the extra app was the lazy fix. One capture habit. One publish pipeline. **Garage → garden → push** - not two masters fighting over the same idea.

---

## Private richness, public polish

In the garage I write mess: half-sentences, wrong takes, links to notes that don't exist yet. On the public site I want clean URLs, taxonomy that makes sense, and nav a stranger can scan.

Explode wikilinks in the garden; use `relref` or plain paths in blog posts. Copy or distill when something is ready to ship. The public side gets theme, search, and a CDN deploy. The private side gets permission to be wrong.

---

## Git as the bridge (not a second wiki host)

Some folks keep drafts in `content/drafts/` or `draft: true` frontmatter. Same files, different build targets.

My version: garden notes are Markdown in Git; what you see at `/notes/` is the subset I'm willing to grow in public. When I lost PHP hosting, the posts that survived were **files in a repo**. Markdown travels. You don't need Obsidian *and* Hugo *and* a sync plugin to make that true.

---

## What I still don't do

I don't paste vault-style `[[wikilinks]]` into Hugo blog content unless the build resolves them. I don't maintain a private graph and a public graph of the same links. If it's worth connecting in public, it gets a `related_notes` line or a real link in prose.

Think private, ship public. The Markdown middle stays the same; the room you publish in picks the rules.
