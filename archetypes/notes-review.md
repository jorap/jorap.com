---
title: "{{ replace .Name "-" " " | title }}"
meta_title: "{{ replace .Name "-" " " | title }}"
description: "One sentence: the single claim this note makes."
date: {{ .Date }}
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: []
slug: "{{ .Name }}"
aliases: []
featured: false
review: true
card_sets: ["Set Name"]
cards:
  - front: "Situational cue I'd recognize mid-week — first person, mid-action, no options on the front."
    back: "Immediate move — plain imperative; the right default already loaded."
  - front: "Second prompt?"
    back: "Second answer."
  - front: "Third prompt?"
    back: "Third answer."
  - front: "Fourth prompt?"
    back: "Fourth answer."
  - front: "Fifth prompt?"
    back: "Fifth answer."
  - front: "Sixth prompt?"
    back: "Sixth answer."
draft: true
---

**{{ replace .Name "-" " " | title }}** — one idea, stated plainly. Link out instead of adding sections.
