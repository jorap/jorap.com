---
title: "Native Hugo Taxonomies"
meta_title: "Native Hugo Taxonomies - Categories, Tags, and What I Don't Let Grow Wild"
description: "Hugo builds category and tag pages from frontmatter - no plugin. I use them for site navigation, not as a private Second Brain."
slug: "native-hugo-taxonomies"
date: "2026-06-19T06:00:00Z"
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Taxonomies", "Tags", "Categories", "SEO", "Content Management", "PKM", "Note Taking"]
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

**Hugo taxonomies** group content at build time. List every post tagged `hugo`, get `/tags/hugo/`. Same for categories. Native means it's in the core - frontmatter lists drive URLs, theme templates render them.

JoRap uses **categories** for broad buckets (Gear, Worship, Technology) and **tags** for specificity (Hugo, Instant Pot, Alex Eala). That's site structure for readers and search - not my private notes graph.

The notes garden uses `related_notes` in frontmatter for that. Different job.

---

## The discipline problem (not the Hugo problem)

Hugo will happily build a tag page for every string you type. I've seen my own drafts with twenty tags copied from an old SEO habit. Each one spawns a thin archive page. Most of them useless.

Categories: I try to keep it under a dozen readers can scan.

Tags: useful for recurring topics, embarrassing when every post invents a new synonym.

**Review the tag list before publish** the same way you'd review a messy folder tree. Hugo won't stop you. Future you will sigh.

---

## categories vs tags (how I split them)

| | Categories | Tags |
|---|---|---|
| Count | Few | More |
| Reader job | "What shelf is this?" | "What else like this?" |
| Example | `Gear`, `Filipino` | `Extension Cord`, `Shopee` |

A post gets one or two categories. Tags are optional seasoning - not a keyword dump.

---

## Custom taxonomies (when native fits the URL)

You can add `series`, `authors`, whatever in `hugo.toml`:

```toml
[taxonomies]
  category = "categories"
  tag = "tags"
  series = "series"
```

I haven't needed a custom taxonomy on JoRap yet. Hugoplate already ships multi-author support. If I ran a serialized tutorial, `series` would be the obvious add.

---

## Templates you might touch

`layouts/categories/terms.html` - index of all categories

`layouts/tags/terms.html` - index of all tags

`layouts/_default/taxonomy.html` - posts in one term

Theme handles display. **You** handle not creating 400 empty tag pages.

---

## Bottom line

Native Hugo taxonomies organize the **public** site. My private wiki can be messier - wikilinks, backlinks, whatever.

Published taxonomy should be intentional. Hugo makes grouping free. Curation is still work.

When in doubt, fewer tags. Readers and future-you win.
