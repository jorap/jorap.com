---
title: "Native Hugo Taxonomies"
meta_title: "Native Hugo Taxonomies - Categories, Tags, and Limits"
description: "Hugo builds category and tag pages from frontmatter - no plugin. I use them for site navigation, not as a private Second Brain."
slug: "native-hugo-taxonomies"
date: "2026-06-19T06:00:00Z"
image: "/images/joraps-world.jpg"
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
level_depth: 3
featured: false
draft: true
---

**Hugo taxonomies** group content at build time. List every post tagged `hugo`, get `/tags/hugo/`. Same for categories. Native means it's in the core - frontmatter lists drive URLs, theme templates render them.

JoRap uses **categories** for broad buckets (Gear, Worship, Technology) and **tags** for specificity (Hugo, Instant Pot, Alex Eala). That's site structure for readers and search - not my private notes graph.

The notes garden uses `related_notes` in frontmatter for that. Different job. I tried stuffing the blog tags with every related idea once. Got a tag cloud that looked busy and meant nothing.

Copy-paste from an old SEO checklist gave one post fourteen tags including `Web Development` and `Website Development` for the same three articles. Hugo built both pages. Google didn't care. I cared when I opened the tag index and saw the duplication.

---

## Hugo builds every tag you invent

Hugo will happily build a tag page for every string you type. I've seen my own drafts with twenty tags copied from an old SEO habit. Each one spawns a thin archive page. Most of them useless.

I once published a post with near-duplicate tags - `Hugo` and `Hugo SSG` - and ended up with two thin archives that split the same three posts. Cleaning that up meant editing frontmatter and waiting for the build. Five minutes of discipline at draft time would have skipped the cleanup.

Categories: I try to keep it under a dozen readers can scan.

Tags: useful for recurring topics, embarrassing when every post invents a new synonym.

**Review the tag list before publish** the same way you'd review a messy folder tree. Hugo won't stop you. Future you will sigh.

---

## Categories vs tags - how I split them

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

I haven't needed a custom taxonomy on JoRap yet. Hugoplate already ships multi-author support. If I ran a serialized tutorial, `series` would be the obvious add. Until then I'm not inventing another axis to curate.

---

## Theme files vs what I actually curate

The theme already has the listing templates - category index, tag index, posts under one term. I rarely edit those. The work is upstream of the template: **don't create 400 empty tag pages.**

Native Hugo taxonomies organize the **public** site. My private wiki can be messier - wikilinks, backlinks, whatever.

I'll keep categories under a dozen and tags short. Hugo makes grouping free; I still have to curate what ships. When in doubt, fewer tags. Readers and future-me win.

Before I publish a post I scan the tag list the same way I scan a messy Downloads folder - delete the synonym, keep the one I'd actually click.
