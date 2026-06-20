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

Set `review: true` only on spine concepts worth cold recall (~20% of notes). Add a `cards:` list with `front` / `back` pairs (six per spine note). The opening line stays the wiki definition. Extra one-off cards: `{{< card front="Question" back="Answer" >}}`.
