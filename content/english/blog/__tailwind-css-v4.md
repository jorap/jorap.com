---
title: "Tailwind CSS v4.0"
meta_title: "Tailwind CSS v4 - What Changed When Hugoplate Upgraded"
description: "Tailwind v4 moved config into CSS and shuffled the build pipeline. I didn't fork blindly - I synced Hugoplate upstream and tested before pushing live."
social_media_intro: "Tailwind v4 moved config into CSS. I edited tailwind.config.js out of habit and nothing changed. What broke my Hugoplate upgrade checklist: article in the comments."
slug: "tailwind-css-v4"
date: "2026-06-19T06:00:00Z"
image: "/images/joraps-world.jpg"
image_prompt: "Photorealistic developer desk, code editor showing CSS @theme block on one monitor, faded tailwind.config.js tab on another, mechanical keyboard, neutral daylight, focused upgrade-session mood, no readable code text, no logos"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Tailwind CSS", "CSS", "Web Development", "Hugo", "Hugoplate", "Frontend"]
related_notes:
  - future-proofing-knowledge
  - the-garage-concept
  - free-tier-hosting-stack
  - git-based-cms
  - metadata-strategy
level_depth: 3
featured: false
draft: true
---

**Tailwind CSS v4** wasn't a npm bump and forget for this site. Config moved into CSS. The engine changed. Build tooling shifted toward Vite/Oxide. If you maintain a Hugo theme that ships Tailwind, **upgrade is infrastructure work** - readers won't notice, developers will. Glad I did the boring upgrade once.

I ride [Hugoplate](/blog/hugoplate-theme-review/) upstream and try not to fork CSS blindly. v4 was the test of that habit.

---

## What broke my mental model from v3

In v3 I lived in `tailwind.config.js` - colors, fonts, spacing tokens in JavaScript. v4 pushes a lot of that into CSS with `@theme`:

```css
@theme {
  --color-primary: #2563eb;
  --font-primary: "Inter", sans-serif;
}
```

Change a token, watch it propagate. For a personal rebrand that's genuinely fun - I tweaked accent colors without touching layout files.

The footgun: old config habits don't port line for line. I opened my old JavaScript config out of muscle memory, edited nothing useful, and wondered why tokens weren't updating. The answer was in CSS. Read the migration guide once before editing. I skimmed it the first time. Paid for that with a confused afternoon.

---

## Why I picked Hugoplate partly because of Tailwind

Most Hugo themes ship bespoke SCSS you'll never fully learn. Hugoplate uses utility classes I already knew from other projects. `p-8` to `p-6` on a card. `text-lg` on a heading. No theme-specific dialect.

v4 kept that **utility-first mental model.** The plumbing moved; the day-to-day editing didn't.

When the upstream theme merged v4, I pulled, ran `hugo server`, clicked around - homepage, blog single, notes garden, dark mode toggle. Boring checklist before push live. Dark mode was the one that bit me: a contrast issue on a tag pill I only saw after toggling twice. Local check caught it. Pushing blind wouldn't have.

Notes garden cards use different padding than blog singles. I almost shipped a layout where garden card titles clipped on mobile - caught it on a narrow browser window, not on my laptop at full width.

---

## Hugo and Tailwind have to agree

Hugo's asset pipeline and Tailwind's new engine have to agree. Hugoplate documents how PostCSS/Vite wiring works in their repo - I didn't invent it.

If you're on an old fork frozen on v3, budget an afternoon, not ten minutes. Compare upstream's `package.json` and CSS entry files to yours. Diff beats guessing. I once tried to "just bump the version" without syncing the rest of the theme. Build failed in a way that looked like Hugo's fault. It wasn't.

---

## What readers never see

Faster rebuilds on my laptop. Slightly smaller CSS output. Zero change to how a blog post reads.

That's fine. Infrastructure churn isn't content. **Sync theme, test locally, push live** is the whole playbook.

Tailwind v4 is maintainers' work, not writers'. I let Hugoplate carry most of it and kept my custom CSS thin.

If you forked a theme years ago and cherry-pick nothing, upgrades hurt. If you stay close to upstream, v4 is a manageable merge - annoying, not catastrophic.

I don't enjoy CSS infrastructure weeks. Glad I don't maintain a fork that drifts every time Tailwind ships a point release.
