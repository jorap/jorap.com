---
title: "Tailwind CSS v4.0"
meta_title: "Tailwind CSS v4.0 - What Changed for Theme Builders"
description: "Tailwind v4 shifted config and build integration. JoRap's theme rides Hugoplate - here's what v4 means when you touch styles."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Tailwind CSS", "CSS", "Web Development", "Hugo", "Hugoplate", "Frontend"]
slug: "tailwind-css-v4"
related_notes:
  - future-proofing-knowledge
  - the-garage-concept
  - free-tier-hosting-stack
  - git-based-cms
  - metadata-strategy
featured: false
draft: true
---

**Tailwind CSS v4** moved toward CSS-first config, new engine, tighter Vite integration. If you maintain a Hugo theme with Tailwind, **upgrade isn't npm bump only** - check how Hugoplate wires PostCSS.

I follow the theme upstream and try not to fork CSS blindly.

---

## CSS-native configuration

`@theme` in CSS replaces some `tailwind.config.js` patterns. **Read migration guide before editing.**

---

## Build tool coupling

Vite/esbuild paths differ from v3. **Match Hugo asset pipeline docs.**

---

## Utility-first unchanged

Still classes in markup. **Mental model holds; plumbing moved.**

---

## Bottom line

Tailwind v4 is infrastructure churn for site maintainers. **Sync theme upstream, test locally, deploy.** Users reading posts won't notice; developers will.

*Idea captured from [ideas.jorap.com](https://ideas.jorap.com/).*
