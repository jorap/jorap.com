---
title: "Flashcards"
meta_title: "Notes Flashcards"
description: "Flip cards from opt-in notes - habit prompts, not trivia. Export the same deck to Anki."
slug: "flashcards"
layout: "cards"
note_kind: "meta"
date: 2026-06-18T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Notes", "Meta", "Anki", "Learning"]
featured: false
draft: false
aliases:
  - /notes/cards/
---

**Flashcards** = drill lane beside the wiki - opt in per note, export to Anki when I want SRS on my phone.

This page is a **utility surface** (`note_kind: meta`) - not a garden note. Evergreen notes should not `[[wikilink]]` here; point readers to [/notes/flashcards/](/notes/flashcards/) or [/notes/review/](/notes/review/) by URL instead.

Twelve-plus habit and gospel spine notes (~20% of the garden) use `review: true` ([[Pareto Principle]] applied). Each carries six scenario cards in frontmatter and a `card_sets:` list so Review can filter by group (Capture, Linking, Review, **Eternal Principles**, etc.). Gospel spine notes also tag a section set - **Faith**, **Commandments**, **Ethics**, **Prayer**, **Priorities**, **Discipleship** - matching [[Eternal Principles]] sections. Cards ask what I'd *do* when capture, review, linking, or discipleship breaks down - not what a term *means*. **Cue → apply:** front = life's moment I'd recognize; back = principle compressed into the next move (do, decide, or say in one breath). **Cue only - no multiple choice:** state the moment on the front; never list options (`X, Y, or Z?`, `A or B?`) to pick from. **Front longer than back:** the prompt carries the scenario; the answer stays short. **No answer telegraphy:** don't name the note title, quote the verse, or fill in the blank on the front - give a subtle situational trigger instead. **Quiz yourself** at [/notes/review/](/notes/review/).

## Frontmatter format (review notes)

Use this shape - inline `card_sets`, block `cards`, double-quoted strings, `draft` last:

```yaml
review: true
card_sets: ["Capture", "Workflow"]
cards:
  - front: "Mid-commute spark I might forget before I'm home."
    back: "Drop in one inbox. Don't organize yet."
  - front: "Interesting link, unsure it's worth saving. One filter question I ask before anything hits the inbox?"
    back: "Would I act on it or cite it later?"
draft: false
```

**Rules that prevent build/export errors:**

- Double-quote every `front`, `back`, and set name (apostrophes and colons stay safe inside `"..."`).
- **Front longer than back** - the prompt carries a scenario; the answer stays short.
- **Subtle hints only** - no note title, verse citation, or fill-in-the-blank that gives away the back.
- **Cue only - no multiple choice** - front states the moment; never list options to pick from (`A or B?`, `X, Y, or Z?`).
- Use inline `[...]` for `card_sets` (same as `categories` / `tags`); block lists for `cards` only.
- Indent each `back:` four spaces under its `- front:` line.
- Set names are short labels (`Capture`, `Linking`, `Review`, `Faith`, `Commandments`, `Ethics`, `Prayer`, `Priorities`, `Discipleship`) - not note tags.
- Optional per-card override: add `sets: ["Capture"]` under one card item.
- Do not put `| JoRap Notes` in `meta_title` (the theme appends it).
- Validate with `npm run lint:cards` before commit.

New spine note scaffold: `hugo new content/english/notes/my-note.md --kind notes-review`.
