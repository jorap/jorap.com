---
title: "Flashcards"
meta_title: "Notes Flashcards"
description: "Flip cards from opt-in notes - habit prompts, not trivia. Export the same deck to Anki."
slug: "cards"
layout: "cards"
note_kind: "meta"
date: 2026-06-18T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Notes", "Meta", "Anki", "Learning"]
featured: false
draft: false
---

**Flashcards** = drill lane beside the wiki - opt in per note, export to Anki when I want SRS on my phone.

Twelve habit spine notes (~20% of the garden) use `review: true` ([[Pareto Principle]] applied). Each carries six scenario cards in frontmatter and a `card_sets:` list so Review can filter by group (Capture, Linking, Review, etc.). Cards ask what I'd *do* when capture, review, or linking breaks down, not what a term *means*. **Quiz yourself** at [/notes/review/](/notes/review/).

## Frontmatter format (review notes)

Use this shape — inline `card_sets`, block `cards`, double-quoted strings, `draft` last:

```yaml
review: true
card_sets: ["Capture", "Workflow"]
cards:
  - front: "Mid-commute spark. My first move?"
    back: "One trusted inbox. Don't organize yet."
  - front: "Before I save, I ask:"
    back: "Would I act on it or cite it later? If no, skip."
draft: false
```

**Rules that prevent build/export errors:**

- Double-quote every `front`, `back`, and set name (apostrophes and colons stay safe inside `"..."`).
- Use inline `[...]` for `card_sets` (same as `categories` / `tags`); block lists for `cards` only.
- Indent each `back:` four spaces under its `- front:` line.
- Set names are short labels (`Capture`, `Linking`, `Review`) — not note tags.
- Optional per-card override: add `sets: ["Capture"]` under one card item.
- Do not put `| JoRap Notes` in `meta_title` (the theme appends it).
- Validate with `npm run lint:cards` before commit.

New spine note scaffold: `hugo new content/english/notes/my-note.md --kind notes-review`.

Extends [[Getting Started]]. Implements [[Spaced Repetition]].
