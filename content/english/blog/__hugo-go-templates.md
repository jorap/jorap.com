---
title: "Hugo Go Templates"
meta_title: "Hugo Go Templates - How I Learned Without Reading the Whole Manual"
description: "Hugo layouts scared me until I broke the homepage and had to fix it. Most of what I touch is copy-paste from Hugoplate partials - Go templates with sprinkles."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Go Templates", "Web Development", "Static Sites", "Templating", "Hugoplate", "PKM", "Documentation"]
slug: "hugo-go-templates"
related_notes:
  - future-proofing-knowledge
  - metadata-strategy
  - drafting-in-public
  - the-garage-concept
  - digital-garden
  - building-a-personal-api
featured: false
draft: true
---

Hugo builds HTML from **Go templates** - `.html` files full of `{{ }}` actions. Partials, layouts, shortcodes - same language everywhere. The docs read like a reference manual. I learned by breaking something visible, then fixing it with the theme's existing files open beside me.

Still my best teacher.

---

## The first break: homepage featured posts

Early on I wanted the homepage to show something different - featured posts, notes garden links, less of the default Hugoplate marketing blocks. I edited a layout, pushed, and got a blank section. No error on the page. Just missing HTML.

Turned out I'd referenced `.Params.featured` wrong and Hugo quietly rendered nothing. Classic template bug: **valid syntax, wrong context.**

Fix was copying how Hugoplate already ranged over `.Pages` in another partial, then swapping in my filter. I didn't learn Go. I learned **read the theme first.**

---

## Layout lookup (predictable names win)

Hugo picks templates in a hierarchy:

- `layouts/blog/single.html` beats `layouts/_default/single.html`
- Section-specific list templates beat defaults

When something renders wrong, I check **which template Hugo chose** before inventing a new file. Nine times out of ten the theme already had a hook I should have edited.

Name things the way Hugo expects. Fighting the lookup order means duplicate layouts and confusion.

---

## Partials: one change, whole site

Header, footer, card markup, related-notes block - anything repeated goes in `layouts/partials/`.

```go
{{ partial "components/blog-card.html" . }}
```

Change the card once, every listing page updates. That's how I tweaked blog cards without touching fifty files.

The `.` is the current page context. `.Title`, `.Params.description`, `.RelPermalink` - frontmatter and built-ins hang off that dot. Pipe it into partials when you need a sub-scope.

---

## The syntax I actually use

Not a Go developer. These patterns cover almost everything I touch:

- `{{ if .Params.featured }}` - conditional blocks
- `{{ range .Pages }}` - loop a list
- `{{ with .Params.related_notes }}` - only render if field exists
- `{{ .Title | safeHTML }}` - filters on values

When I need something weirder, I grep the theme for a working example. Hugoplate is thousands of lines of answers.

---

## Bottom line

Hugo Go templates reward small experiments on a local build. **Don't start from the official docs cover to cover.** Break one page you care about, fix it with the theme's partials as a cheat sheet.

Most of JoRap is assembled from patterns Hugoplate already had. My edits are tweaks, not a from-scratch framework. That's the lazy path, and it held for a year.
