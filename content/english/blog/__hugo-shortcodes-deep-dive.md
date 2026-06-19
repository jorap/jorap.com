---
title: "Hugo Shortcodes Deep Dive"
meta_title: "Hugo Shortcodes - Reusable Markdown Macros"
description: "Shortcodes are Hugo's way to drop components into Markdown without raw HTML everywhere. I use them for images, alerts, and embeds."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Shortcodes", "Markdown", "Web Development", "Static Sites", "Components", "PKM", "Documentation"]
slug: "hugo-shortcodes-deep-dive"
featured: false
draft: true
---

**Hugo shortcodes** are mini templates you call from Markdown: `{{</* image src="..." */>}}`. They keep posts clean and centralize markup changes.

When I update how images lazy-load, I fix one shortcode - not 200 posts.

---

## Built-ins worth knowing

`figure`, `ref`, `relref` - linking and media without broken paths. **Read the docs once**, bookmark examples.

---

## Custom shortcodes

`layouts/shortcodes/youtube.html` with params. Pass `id` from Markdown. **Params become `.Get` in the template.**

---

## Markdown vs shortcode delimiters

`{{</* */>}}` vs `{{{%/* */%}}%}}` - markdown processing differs. **I use `<>` when I want Hugo to handle inner markdown.**

---

## Bottom line

Shortcodes are the DRY layer between Markdown writers and theme maintainers. **Extract anything you use three times.** Your future refactors will send thanks.

*Idea captured from [ideas.jorap.com](https://ideas.jorap.com/).*
