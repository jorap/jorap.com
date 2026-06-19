---
title: "Hugo Page Bundles"
meta_title: "Hugo Page Bundles - Posts With Their Assets"
description: "Page bundles keep images and Markdown together. I use them when a post has multiple files that shouldn't live in /static."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Page Bundles", "Content Management", "Static Sites", "Markdown", "Assets", "PKM", "Static Site Generator"]
slug: "hugo-page-bundles"
featured: false
draft: true
---

A **Hugo page bundle** is a folder with `index.md` plus sibling assets - images, downloads, nested shortcodes. The post owns its files. No guessing which `/images/` filename matches which draft.

I switch to bundles when a post has more than one custom image or an attachment.

---

## Folder structure

`content/blog/my-post/index.md` and `hero.jpg` beside it. Reference with `![alt](hero.jpg)` - **relative paths just work.**

---

## Leaf vs branch

Leaf bundle: one page per folder. Branch bundle: section index with children. **Most blog posts are leaf bundles** when I bother.

---

## Headless bundles

Resources without their own URL - reusable image sets. Niche but handy for components.

---

## Bottom line

Hugo page bundles reduce asset chaos. **Colocate what ships together.** For single-image posts, plain `.md` files are still fine.

*Idea captured from [ideas.jorap.com](https://ideas.jorap.com/).*
