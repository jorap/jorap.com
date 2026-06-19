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
featured: false
draft: true
---

**{{ replace .Name "-" " " | title }}** — one idea, stated plainly. If you need `and` or a second heading, split into another note and link it with `[[wikilinks]]`.
