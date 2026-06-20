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
status: seedling
review: false
featured: false
draft: true
---

**{{ replace .Name "-" " " | title }}** — one idea, stated plainly. If you need `and` or a second heading, split into another note and link it with `[[wikilinks]]`.

For habit spine notes (`review: true`), copy the frontmatter pattern from [/notes/cards/](/notes/cards/) or run `hugo new content/english/notes/my-note.md --kind notes-review`. Rules: double-quote every `front`, `back`, and set name; inline `card_sets: ["Set"]`; block list for `cards`; put `draft` last; do not add `| JoRap Notes` to `meta_title`. Don't `[[wikilink]]` utility pages (Graph, Issues, Flashcards, Review, Random Duo, Random Trio) — use URLs; see [[Getting Started]].
