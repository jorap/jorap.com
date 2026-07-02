---
title: "Native Hugo Taxonomies"
meta_title: "Native Hugo Taxonomies - Categories and Tags in Hugo"
description: "Hugo ships with taxonomies - categories, tags, and custom ones. I use them for navigation, not as my private PKM brain."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Taxonomies", "Tags", "Categories", "SEO", "Content Management", "PKM", "Note Taking"]
slug: "native-hugo-taxonomies"
related_notes:
  - metadata-strategy
  - commonplace-book
  - future-proofing-knowledge
  - literature-notes
  - evergreen-vs-fleeting-notes
  - note-relationships
featured: false
draft: true
---

**Hugo taxonomies** group content at build time - `/categories/productivity/`, `/tags/hugo/`. Native means no plugin required; frontmatter lists drive it all.

JoRap uses categories for broad buckets and tags for specificity. **Site structure, not full Second Brain.**

---

## categories vs tags

Categories: few, navigable. Tags: many, granular. **Don't let either list grow unreviewed.**

---

## Custom taxonomies

`series`, `authors` - define in `hugo.toml`. **Use when native fits URL design.**

---

## Taxonomy templates

`layouts/categories/terms.html` controls list pages. **Theme handles display; you handle discipline.**

---

## Bottom line

Native Hugo taxonomies organize the public site. **Private wiki can be messier.** Keep publish taxonomy intentional.

*Idea captured from [ideas.jorap.com](https://ideas.jorap.com/).*
