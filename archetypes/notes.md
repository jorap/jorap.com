---
title: "{{ replace .Name "-" " " | title }}"
meta_title: "{{ replace .Name "-" " " | title }}"
description: "One idea, stated plainly in one breath."
slug: "{{ .Name }}"
date: {{ .Date }}
image: "/images/note.jpg"
categories: []
author: "JoRap"
tags: []
aliases: []
review: false
featured: false
draft: true
key_concept: |
  One sentence — the angle, not a second definition.

  Further explanation: stakes, distinctions, [[wikilinks]]. Skip the second paragraph when the description is enough.
examples:
  - "Mid-action scene where this principle fires — not a definition restated."
  - "Second scene from a different field — jeepney, clinic, inbox, bedtime."
relationships:
  - type: extends
    wikilink: "[[Related Note]]"
    reason: "what this note builds on"
  - type: contradicts
    wikilink: "[[Tension Note]]"
    reason: "when …"
---

For habit spine notes (`review: true`), copy the frontmatter pattern from [/notes/flashcards/](/notes/flashcards/) or run `hugo new content/english/notes/my-note.md --kind notes-review`. Rules: double-quote every `front`, `back`, and set name; inline `card_sets: ["Set"]`; block list for `cards`; put `draft` last; do not add `| JoRap Notes` to `meta_title`. Don't `[[wikilink]]` utility pages (Graph, Issues, Flashcards, Review, Random Duo) — use URLs; see [[Getting Started]].
