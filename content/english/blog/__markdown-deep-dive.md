---
title: "Markdown Deep Dive"
meta_title: "Markdown Deep Dive - The Plain-Text Layer Under Everything"
description: "Markdown is the format behind JoRap, Hugo, GitHub, and my notes. Here's what I actually use beyond bold and bullets - and where flavors diverge."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Markdown", "Hugo", "Writing", "PKM", "Documentation", "Plain Text", "Note Taking"]
slug: "markdown-deep-dive"
related_notes:
  - future-proofing-knowledge
  - evergreen-notes
  - metadata-strategy
  - commonplace-book
  - intellectual-sourcing
  - the-feynman-technique
featured: false
draft: true
---

**Markdown** is lightweight markup: `#` for headings, `*` for emphasis, `[text](url)` for links. Hugo, GitHub, Obsidian, TiddlyWiki (with plugins) - variants everywhere.

Learning Markdown once paid off in every place I publish or capture. The syntax is boring on purpose. Boring survives tool churn.

---

## The 90% I actually use

Headings, paragraphs, bold, italic, links, images, ordered and unordered lists, blockquotes, horizontal rules, fenced code blocks.

That's almost every blog post on this site. The [Drupal to WordPress](/blog/drupal-to-wordpress/) essay is thousands of words and never needed more than that core set.

Fancy extensions are seasoning. Master the pot first.

---

## Frontmatter isn't Markdown (but it's always paired)

Hugo posts start with YAML between `---`:

```yaml
---
title: "Post title"
description: "One breath summary"
date: 2026-07-12T05:00:00Z
draft: false
---
```

Not part of the Markdown spec. Every static site generator has its own fields. I treat frontmatter as **publish metadata** and the body as **the writing.**

Broken YAML indentation has broken my build more than any Markdown typo. Tabs and colons are the enemy.

---

## Flavors differ - know your renderer

| Feature | Hugo / GitHub | Obsidian |
|---|---|---|
| Tables | Yes | Yes |
| `[[wikilinks]]` | No (without plugins) | Yes |
| Shortcodes | Hugo only | N/A |
| Raw HTML | Often allowed | Varies |

I draft blog posts in the same editor as notes, but I **don't** paste Obsidian wikilinks into Hugo content. They won't resolve. Use `relref` or plain paths.

Same words, different dialects. Like PHP and WordPress - related, not identical.

---

## Why plain text still wins for me

- **Diffable** in Git - see exactly what changed line by line
- **Portable** - move hosts without export wizard grief
- **Durable** - readable in twenty years without a proprietary app

When I lost PHP hosting, the posts I could recover as files were the ones that mattered. Markdown in a repo is backup strategy, not just format preference.

---

## Bottom line

Markdown deep dive, for me, meant mastering the boring basics and code fences. Everything else is optional.

If you're building on Hugo, learn frontmatter and shortcodes next. If you're capturing notes, learn your app's link syntax. The Markdown middle stays the same.
