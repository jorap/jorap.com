---
note_kind: "meta"
layout: "cards"
title: "Flashcards"
meta_title: "Notes Flashcards"
description: "Learn less, retain longer, apply more - I opt notes into drill cards when recall and use in real life matter, and export to Anki when I want SRS on my phone."
key_concept: |
  - **Guiding principle:** Learn less, retain longer, and apply more.
  - Level 1: Pack only tools you will use - learn fewer things, remember longer, use them when life shows up.
  - Level 2: Flashcards are like spare keys clipped where you will find them - cue on the front, move on the back when the moment hits.
  - Level 3: Because recall under pressure differs from recognition during review, cards train the move you need when the cue appears in real life.
  - Level 4: Keep a card only if it helps with a recurring problem - drop cards that only feel smart during review but never fire in life.
  - Level 5: Cue on the front, immediate move on the back - not definitions dressed as advice; ~20% of notes opt in at [/notes/review/](/notes/review/).
  - **The question:** Can I recall and use this knowledge when it matters? - not review count, streak length, or facts memorized - retention, application, and explanation in real life.
  - This page is a **utility surface** (`note_kind: meta`) - not a garden note.
  - Evergreen notes should not `[[wikilink]]` here; point readers to [/notes/flashcards/](/notes/flashcards/) or [/notes/review/](/notes/review/) by URL instead.
  - Cards exist so the right move is already loaded when life shows up.
  - Cue on the front, immediate move on the back - not definitions dressed as advice.
  - Keep a card only if the knowledge helps solve a recurring problem or make a better decision.
  - Or perform a useful skill, understand an important subject, or communicate more clearly.
  - ~20% of notes opt in - gospel and PKM spine share [/notes/review/](/notes/review/).
  - Learn less, retain longer, apply more - cards exist so the right move loads when life shows up.
  - I opt notes into drill cards when recall and use in real life matter, and export to Anki when I want SRS on my phone.
shareable_thought:
  - "Learn less, retain longer, apply more."
  - "I opt notes into drill cards when recall and use in real life matter, and export to Anki when I want SRS on my phone."
  - "Cards exist so the right move loads when life shows up."
  - "Guiding principle: Learn less, retain longer, and apply more."
slug: "flashcards"
date: "2026-06-18 08:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["Notes", "Meta", "Anki", "Learning"]
aliases: ["/notes/cards/"]
featured: false
draft: false
---





## Frontmatter format (atomic notes)

Atomic garden notes store all claim data in frontmatter - body stays empty unless the page is a hub or utility doc:

```yaml
description: "One breath definition."
key_concept: |
  One sentence - the angle.

  Optional second paragraph with [[wikilinks]].
examples:
  - "Mid-action scene one."
  - "Mid-action scene two - different field."
relationships:
  - type: extends
    wikilink: "[[Related Note]]"
    reason: "what this builds on"
  - type: contradicts
    wikilink: "[[Tension Note]]"
    reason: "when …"
```

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

New spine note scaffold: `hugo new content/english/notes/my-note.md --kind notes-review`. Pairs with [[Random Duo]].
