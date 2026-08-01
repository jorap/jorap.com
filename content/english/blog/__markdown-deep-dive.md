---
title: "Markdown Deep Dive"
meta_title: "Markdown Deep Dive - What I Use Beyond Bold and Bullets"
description: "Markdown is the format behind JoRap, Hugo, GitHub, and my notes. Here's what I actually use beyond bold and bullets - and where flavors diverge."
slug: "markdown-deep-dive"
date: "2026-06-19T06:00:00Z"
image: "/images/note.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Markdown", "Hugo", "Writing", "PKM", "Documentation", "Plain Text", "Note Taking"]
related_notes:
  - future-proofing-knowledge
  - evergreen-notes
  - metadata-strategy
  - commonplace-book
  - intellectual-sourcing
  - the-feynman-technique
level_depth: 3
featured: false
draft: true
---

**Markdown** is lightweight markup: `#` for headings, `*` for emphasis, `[text](url)` for links. Hugo, GitHub, Obsidian, TiddlyWiki (with plugins) - variants everywhere.

I learned it the boring way: copy-pasting forum posts into a PHP blog years ago and wondering why my bold text showed literal asterisks. Once the muscle memory clicked, every tool after that felt like the same language with a different accent.

Learning Markdown once paid off in every place I publish or capture. The syntax is boring on purpose. Boring survives tool churn.

---

## The 90% I actually use

Headings, paragraphs, bold, italic, links, images, ordered and unordered lists, blockquotes, horizontal rules, fenced code blocks.

That's almost every blog post on this site. The [Drupal to WordPress](/blog/drupal-to-wordpress/) essay is thousands of words and never needed more than that core set.

I still catch myself reaching for a clever extension - footnotes, callouts, custom admonitions - then deleting it because the post didn't need the decoration. Fancy extensions are seasoning. Master the pot first.

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

Broken YAML indentation has broken my build more than any Markdown typo. I once indented a list wrong in `related_notes` and spent twenty minutes thinking Hugo hated me. Tabs and colons are the enemy. When the build fails after a "tiny" frontmatter edit, check indentation before you rewrite the body.

---

## Flavors differ - know your renderer

| Feature | Hugo / GitHub | Obsidian |
|---|---|---|
| Tables | Yes | Yes |
| `[[wikilinks]]` | No (without plugins) | Yes |
| Shortcodes | Hugo only | N/A |
| Raw HTML | Often allowed | Varies |

I draft blog posts and garden notes in the same editor, but I **don't** paste vault-style `[[wikilinks]]` into Hugo blog content unless the build resolves them. I did that once early on - a note link that looked fine in the editor and published as a dead `[[like-this]]` string on the live site. In JoRap Notes, wikilinks work at build time; in blog posts, use `relref` or plain paths.

Same words, different dialects. Like PHP and WordPress - related, not identical.

---

## Why plain text still wins for me

When [I lost PHP hosting](/blog/how-i-built-jorap-notes/), the posts I could recover as files were the ones that mattered. Markdown in a repo is backup strategy, not just format preference.

Plain text diffs cleanly in Git so I can see exactly what changed line by line, moves hosts without export-wizard grief, and stays readable in twenty years without a proprietary app.

If you're building on Hugo, learn frontmatter and shortcodes next. If you're capturing notes, learn your app's link syntax. The boring basics and code fences are the whole middle, and they don't change.
