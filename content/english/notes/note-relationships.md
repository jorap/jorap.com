---
title: "Note Relationships"
meta_title: "Note Relationships - Four Link Types for the Garden"
description: "Four pair types in the body table - extends, contradicts, implements, alternative. Hub and utility pages use note_kind flags."
date: 2026-06-19T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Linking", "PKM", "Note Taking", "Digital Garden", "Meta"]
slug: "note-relationships"
featured: false
status: evergreen
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
aliases: ["link types"]
---
**Note relationships** = four pair types in a body table - extends, contradicts, implements, alternative - so the graph shows how ideas push and pull. **Hub/MOC pages** use `note_kind: index` in frontmatter (not a row). **Utility pages** use `note_kind: meta` — link by URL, not wikilink.

| Type | Question | Example |
|------|----------|---------|
| **extends** | What does this build on? | [[Signal vs Noise]] extends [[Capture]] |
| **contradicts** | What tradeoff does this push against? | [[Slow Productivity]] contradicts [[The 12 Week Year]] when fewer deep projects beat quarterly sprints |
| **implements** | What makes this real? | [[Weekly Review Checklists]] implements [[Periodic Knowledge Review]] |
| **alternative** | What else could do this job? | [[Mobile Capture Workflows]] alternative to [[Analog Capture Tools]] |

Every atomic note (`note_kind: note`, the default) carries opening prose, optional **## Example** (one concrete scene), and a **## Note Relationships** table sorted by type: **alternative**, **contradicts**, **extends**, **implements**. At minimum: **extends** and **contradicts**, wikilinked, each with a **Reason** (what this builds on; a **when** clause on contradicts). Add **implements** and **alternative** when they fit. Broken wikilinks to obvious missing notes are fine - they flag future pages. "Pairs with" in older notes means informal extends. Pipeline order (capture → distill → express) is prose, not a fifth type.

## Example

I'm filing a new note on weekly review and add `| extends | [[Periodic Knowledge Review]] | Sunday habit this checklist names |` plus `| contradicts | [[The 12 Week Year]] | when a repeating ritual beats quarterly sprints |` before I publish. Two rows, typed tension, graph can read it.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| alternative | [[PARA Method]] | Body link types vs folder sort when typed links beat project buckets |
| contradicts | [[PARA Method]] | when typed body links beat sorting by project folder |
| extends | [[Associative Linking]] | Typed relationships name how links extend, contradict, and repair — beyond vague wikilinks |
| extends | [[Link Typing]] | Generic PKM term for what this page formalizes |
| implements | [[Associative Linking]] | Typed rows carry vague wikilinks into named push and pull |

## See also

- [[Reconciliation Before Worship]] - Eternal Principles, Gospel, Sermon on the Mount
- [[The Golden Rule]] - Eternal Principles, Gospel, Sermon on the Mount
- [[Associative Linking]] - Linking, Note Taking, PKM
- [[Getting Started]] - Digital Garden, Meta, PKM
- [[Maps of Content]] - Linking, Meta, PKM
