---
title: "Note Relationships"
meta_title: "Note Relationships - Four Link Types for the Garden"
description: "Four pair types in `relationships` frontmatter - extends, contradicts, implements, alternative - so the graph shows how ideas push and pull. **Hub/MOC pages** use `note_kind: index` (not a row). **Utility pages** use `note_kind: meta` - link by URL, not wikilink."
key_concept: |
  Four pair types in `relationships` frontmatter show how ideas push and pull - not just that two notes mention each other.
  
  | Type | Question | Example |
  |------|----------|---------|
  | **extends** | What does this build on? | [[Signal vs Noise]] extends [[Capture]] |
  | **contradicts** | What tradeoff does this push against? | [[Slow Productivity]] contradicts [[The 12 Week Year]] when fewer deep projects beat quarterly sprints |
  | **implements** | What makes this real? | [[Weekly Review Checklists]] implements [[Periodic Knowledge Review]] |
  | **alternative** | What else could do this job? | [[Mobile Capture Workflows]] alternative to [[Analog Capture Tools]] |
  
  Every atomic note carries a one-breath definition in `description`, angle in `key_concept`, two scenes in `examples`, and typed links in `relationships` frontmatter - not body sections.
examples:
  - "I'm updating the family chore chart and add \"feeds into: Saturday yard work\" next to \"take out trash\" plus \"conflicts with: bedtime when done late\" before I tape it to the fridge."
  - "The coach's whiteboard lists \"feeds into: secondary break\" beside each drill - players see how today's reps connect before they leave the gym."
relationships:
  - type: alternative
    wikilink: "[[PARA Method]]"
    reason: "Body link types vs folder sort when typed links beat project buckets"
  - type: contradicts
    wikilink: "[[Maps of Content]]"
    reason: "when a hand-curated hub beats typing every edge in frontmatter"
  - type: extends
    wikilink: "[[Link Typing]]"
    reason: "Generic PKM term for what this page formalizes"
  - type: implements
    wikilink: "[[Associative Linking]]"
    reason: "Typed rows carry vague wikilinks into named push and pull"
slug: "note-relationships"
date: "2026-06-19 08:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Linking", "PKM", "Note Taking", "Digital Garden", "Meta"]
aliases: ["link types", "Link Typing"]
featured: false
review: true
card_sets: ["Linking", "Writing"]
cards:
  - front: "New note builds on an older atomic claim - typing the connection in the body now. One relationship word?"
    back: "Type extends in the body."
  - front: "This note pushes against a slower-work philosophy I named in the body. One typed link for that tension?"
    back: "Link as contradicts."
  - front: "Weekly checklist makes a review habit real in my notes. Link type that says this note carries it out?"
    back: "Link as implements."
  - front: "Hub page gathering twenty related notes under one roof. Frontmatter flag, not a table row?"
    back: "Set note_kind: index."
  - front: "Atomic note ready to publish - minimum typed links before filing?"
    back: "One extends, one contradicts."
  - front: "Two tools solve the same job - picking one for this note. Link type for the other tool?"
    back: "Link the other as alternative."
draft: false
---
