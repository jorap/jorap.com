---
title: "Hugo Go Templates"
meta_title: "Hugo Go Templates - Logic in Your Layouts"
description: "Hugo templates are Go's text/template with sprinkles. I use them to keep HTML DRY without turning the theme into spaghetti."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Go Templates", "Web Development", "Static Sites", "Templating", "Hugoplate", "PKM", "Documentation"]
slug: "hugo-go-templates"
featured: false
draft: true
---

Hugo builds pages from **Go templates** - `.html` files with `{{ }}` actions. Partials, layouts, shortcodes - all the same language. Scary until you copy one working example and tweak it.

I learned by breaking the homepage, then fixing it. Still my best teacher.

---

## Layout lookup order

Hugo picks templates by type and section - `layouts/blog/single.html` beats `_default/single.html`. **Name things predictably.**

---

## Partials for reuse

Header, footer, card component - `{{ partial "name.html" . }}`. **One change, whole site updates.**

---

## Pipe context

`.` is the current page. `.Params.title` is frontmatter. **Range over lists** with `{{ range .Pages }}`.

---

## Bottom line

Hugo Go templates reward small experiments. **Read the theme's existing partials before inventing.** Most of JoRap is assembled from patterns Hugoplate already had.

*Idea captured from [ideas.jorap.com](https://ideas.jorap.com/).*
