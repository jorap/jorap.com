---
title: "{{ replace .Name "-" " " | title }}"
meta_title: "{{ replace .Name "-" " " | title }}"
description: "One sentence: the single claim this note makes."
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
---

**{{ replace .Name "-" " " | title }}** = one idea, stated plainly in one breath. If you need `and` or a second claim, split into another note and link it with `[[wikilinks]]`.

## Key Concept

Why this note matters — stakes, distinctions, wikilinks. Optional; skip when the definition is enough.

For habit spine notes (`review: true`), copy the frontmatter pattern from [/notes/flashcards/](/notes/flashcards/) or run `hugo new content/english/notes/my-note.md --kind notes-review`. Rules: double-quote every `front`, `back`, and set name; inline `card_sets: ["Set"]`; block list for `cards`; put `draft` last; do not add `| JoRap Notes` to `meta_title`. Don't `[[wikilink]]` utility pages (Graph, Issues, Flashcards, Review, Random Duo) — use URLs; see [[Getting Started]].
