---
title: "Hugo Shortcodes Deep Dive"
meta_title: "Hugo Shortcodes - Fix Images Once, Not in Every Post"
description: "I use shortcodes for images, YouTube, Spotify - anything I'd otherwise paste as raw HTML. One template change updates every post that uses it."
social_media_intro: "Pasted one Spotify iframe \"just once\" - broke six months later. Shortcodes fix YouTube, images, embeds in one file. Article in the comments."
slug: "hugo-shortcodes"
date: "2026-06-19T06:00:00Z"
image: "/images/joraps-world.jpg"
image_prompt: "Markdown editor with blurred shortcode blocks, small embedded video and image placeholders rendered below, clean desk, no platform logos, no readable text, photorealistic"
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
level_depth: 3
aliases: ["hugo-shortcodes-deep-dive"]
featured: false
draft: true
---

**Hugo shortcodes** are mini templates you call from Markdown - glad they exist for the bits I repeat:

```markdown
{{</* image src="images/example.jpg" alt="..." */>}}
```

They keep posts readable and centralize markup. When I added WebP processing and lazy-loading to the image shortcode, every post that used it picked up the change. I did not open 200 files.

Years ago YouTube changed embed attributes. I fixed one `youtube.html` partial instead of grepping every post for raw iframes. That's the whole pitch - and the footgun I ignored for too long first.

---

## What I use on this site

I lean on three of them here. The **image shortcode** carries Facebook walkthrough posts, blueprint diagrams, and testimony screenshots, with params for caption, dimensions, `webp="true"`, and zoom - much better than hand-writing `<figure>` tags in every draft.

YouTube and Spotify embeds run the [DNPAP song resources](/blog/dnpap-song-resources/) page without iframe copy-paste drift. Params stay consistent, so if YouTube changes embed attributes I fix one file. TOC lets long template reference posts drop a table of contents without me maintaining it by hand.

Built-ins like `ref` and `relref` handle internal links when filenames move. I use permalinks in prose more often, but `relref` saves you when a slug changes and you forgot to grep the site.

The early mistake: I pasted a raw Spotify iframe into one post "just this once." Six months later the player UI shifted and that page looked broken while every shortcode page still worked. Once was enough. Third paste becomes a shortcode - or I stop pasting.

---

## One file in `layouts/shortcodes/`

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

I almost wrote a custom callout shortcode for every "note" box on the site. Then I counted how many callouts I actually publish. Almost none. Extract what repeats. Leave one-off prose alone.

---

## `<>` vs `%` delimiters (the footgun)

- `{{</* shortcode */>}}` - inner content treated as HTML (markdown not processed inside)
- `{{%/* shortcode */%}}` - inner content runs through markdown

I use `{{</* ... */>}}` for images and embeds on this site - that's almost every shortcode call in my posts. The `%` delimiter is for paired shortcodes when inner content needs markdown processing. I rarely need it here; Hugoplate's image and embed shortcodes are self-closing.

Get this wrong once and you'll wonder why your bold text stopped working inside a callout. I spent twenty minutes staring at `**this**` rendering as literal asterisks before I checked the delimiter. Most boring possible debug. Check the delimiters first.

---

## When to extract a shortcode

Rule of thumb: **third time you paste the same HTML block, make a shortcode.**

Alert boxes, button links, responsive embeds, author bios - anything that might change site-wide. I keep writing Markdown, and when the embed markup changes I fix one template instead of forty posts.

Shortcodes are the DRY layer between "I write posts" and "I maintain a theme." I didn't build many custom ones - Hugoplate shipped the heavy lifting. The few I added paid for themselves the first time an embed format changed.

Extract what repeats. Leave one-off prose alone. And don't paste "just this once" - future-you will find that iframe. Glad shortcodes catch the repeats before I do.
