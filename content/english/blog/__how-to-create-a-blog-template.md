---
title: "Blog Template"
meta_title: "How to Create a Blog Template - Hugo Reference"
description: "Internal Hugo reference for blog frontmatter, shortcodes, and layout patterns on jorap.com. See the full template post for examples."
slug: "how-to-create-a-blog-template"
date: "1981-06-14T05:00:00Z"
image: "/images/joraps-world.jpg"
categories: ["Website", "Tutorial"]
author: "JoRap"
tags: ["Hugo CMS", "Markdown", "Shortcodes", "Frontmatter", "Blog Template", "Hugo", "Content Management", "Static Sites", "Web Development"]
related_notes:
  - digital-garden
featured: false
draft: true
---

This slug is a **pointer**, not a post.

The living Hugo blog template reference - frontmatter field order, shortcode examples, markdown samples, and layout notes - lives in [`__blog-template.md`](__blog-template.md) in this folder. I keep it as a draft so it doesn't ship as a public page, but agents and future-me can copy from it when spinning up a new post.

When you're writing a real article, start from `archetypes/blog.md` or duplicate a published post in the same category. Use the template file when you need the full cheat sheet, not when you need a voice check.

---

## Quick reminders (the parts I forget)

- Frontmatter order: `title`, `meta_title`, `description`, `slug`, `date`, `image`, then categories/tags, then `draft`
- Draft filenames use a `__` prefix; set `slug` to the intended publish URL
- Run `pnpm lint:blog && pnpm lint:voice && pnpm lint:slop` before `draft: false`
- Hero image: never leave `image-template.jpg` on anything you plan to publish

For voice, read [what I look for in wireless earphones](/blog/what-i-look-for-in-wireless-earphones/) or [why I stopped playing Marvel Snap](/blog/why-i-stopped-playing-marvel-snap/) - not the template file.
