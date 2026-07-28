---
title: "Hugo Go Templates"
meta_title: "Hugo Go Templates - What I Learned Fixing a Listing"
description: "Hugo layouts scared me until I broke a blog listing and had to fix it. Most of what I touch is copy-paste from Hugoplate partials - Go templates with sprinkles."
slug: "hugo-go-templates"
date: "2026-06-19T06:00:00Z"
image: "/images/joraps-world.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Go Templates", "Web Development", "Static Sites", "Templating", "Hugoplate", "PKM", "Documentation"]
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

## The first break: blog list order

Early on I wanted featured posts to float to the top of the blog index. I wired up `featured: true` in frontmatter and edited a listing template before I'd read how Hugoplate already sorted pages.

Wrong context in the template - valid syntax, empty or wrong output. No error on the page. Just not what I expected. I refreshed three times thinking the browser was caching. It wasn't. The template was politely rendering nothing useful.

Fix was copying the site's `sort-featured-first` partial - filter on `.Params.featured`, then append the rest. I didn't learn Go. I learned **read the theme first.**

That afternoon still shapes how I edit layouts: grep Hugoplate for a working pattern before inventing a new file.

---

## Layout lookup (predictable names win)

Hugo picks templates in a hierarchy:

- `layouts/blog/single.html` beats `layouts/_default/single.html`
- Section-specific list templates beat defaults

When something renders wrong, I check **which template Hugo chose** before inventing a new file. Nine times out of ten the theme already had a hook I should have edited.

I name things the way Hugo expects now. Fighting the lookup order got me duplicate layouts and a confusing afternoon - two `single.html` files, one ignored, me editing the wrong one for twenty minutes.

---

## Partials: one change, whole site

Header, footer, card markup, related-notes block - anything repeated goes in `layouts/partials/`.

```go
{{ partial "components/blog-card.html" . }}
```

Change the card once, every listing page updates. That's how I tweaked blog cards without touching fifty files.

The `.` is the current page context. `.Title`, `.Params.description`, `.RelPermalink` - frontmatter and built-ins hang off that dot. Pipe it into partials when you need a sub-scope.

I once passed the wrong context into a partial and spent a while wondering why every card showed the same title. The template was fine. I handed it the wrong `.`.

---

## The syntax I actually use

Not a Go developer. These patterns cover almost everything I touch:

- `{{ if .Params.featured }}` - conditional blocks
- `{{ range .Pages }}` - loop a list
- `{{ with .Params.related_notes }}` - only render if field exists
- `{{ .Title | safeHTML }}` - filters on values

When I need something weirder, I grep the theme for a working example. Hugoplate is thousands of lines of answers.

Hugo Go templates reward small experiments on a local build. **Don't start from the official docs cover to cover.** Break one page you care about, fix it with the theme's partials as a cheat sheet.

Most of JoRap is assembled from patterns Hugoplate already had. My edits are tweaks, not a from-scratch framework. That's the lazy path, and it held for a year.
