---
title: "Hugo Shortcodes Deep Dive"
meta_title: "Hugo Shortcodes - Fix Images Once, Not in Every Post"
description: "I use shortcodes for images, YouTube, Spotify - anything I'd otherwise paste as raw HTML. One template change updates every post that uses it."
slug: "hugo-shortcodes"
date: "2026-06-19T06:00:00Z"
image: "/images/joraps-world.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Shortcodes", "Markdown", "Web Development", "Static Sites", "Components", "PKM", "Documentation"]
related_notes:
  - future-proofing-knowledge
  - metadata-strategy
  - drafting-in-public
  - evergreen-notes
  - creative-output
  - the-garage-concept
aliases: ["hugo-shortcodes-deep-dive"]
featured: false
draft: true
---

**Hugo shortcodes** are mini templates you call from Markdown:

```markdown
{{</* image src="images/example.jpg" alt="..." */>}}
```

They keep posts readable and centralize markup. When I added WebP processing and lazy-loading to the image shortcode, every post that used it picked up the change. I did not open 200 files.

When YouTube changed embed attributes years ago, I fixed one `youtube.html` partial instead of grepping every post for raw iframes. That's the whole pitch.

---

## What I use on this site

**Image shortcode** - Facebook walkthrough posts, blueprint diagrams, testimony screenshots. Params for caption, dimensions, `webp="true"`, zoom. Way better than hand-writing `<figure>` tags in every draft.

**YouTube / Spotify** - the DNPAP song resources page embeds tracks without iframe copy-paste drift. Params stay consistent; if YouTube changes embed attributes, I fix one file.

**TOC** - long template reference posts can drop a table of contents without maintaining it by hand.

Built-ins like `ref` and `relref` handle internal links when filenames move. I use permalinks in prose more often, but `relref` saves you when a slug changes and you forgot to grep the site.

---

## Custom shortcode anatomy

File: `layouts/shortcodes/youtube.html`

```go
<div class="ratio ratio-16x9">
  <iframe src="https://www.youtube.com/embed/{{ .Get "id" }}" ...></iframe>
</div>
```

Markdown passes `id`:

```markdown
{{</* youtube id="abc123" */>}}
```

`.Get "param"` reads what you passed. `.Inner` is content between opening and closing tags for paired shortcodes.

---

## `<>` vs `%` delimiters (the footgun)

- `{{</* shortcode */>}}` - inner content treated as HTML (markdown not processed inside)
- `{{{%/* shortcode */%}}%}}` - inner content runs through markdown

I use `{{</* ... */>}}` for images and embeds on this site - that's almost every shortcode call in my posts. The `%` delimiter is for paired shortcodes when inner content needs markdown processing. I rarely need it here; Hugoplate's image and embed shortcodes are self-closing.

Get this wrong once and you'll wonder why your bold text stopped working inside a callout.

---

## When to extract a shortcode

Rule of thumb: **third time you paste the same HTML block, make a shortcode.**

Alert boxes, button links, responsive embeds, author bios - anything that might change site-wide. Markdown writers keep writing; theme maintainers keep one template.


Shortcodes are the DRY layer between "I write posts" and "I maintain a theme." I didn't build many custom ones - Hugoplate shipped the heavy lifting. The few I added paid for themselves the first time an embed format changed.

Extract what repeats. Leave one-off prose alone.
