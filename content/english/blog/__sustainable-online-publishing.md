---
title: "Sustainable Online Publishing"
meta_title: "Sustainable Online Publishing - Own Your Corner of the Internet"
description: "Social media is easy to start and risky to depend on. Here's why I publish on my own site - and the free stack that makes it sustainable."
date: 2026-06-18T06:12:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Ideas", "Technology"]
author: "JoRap"
tags: ["Publishing", "Self-Hosting", "Hugo", "TiddlyWiki", "Cloudflare Pages", "Content Ownership", "Indie Web", "Digital Independence", "Open Publishing", "Platform Risk", "Blogging", "Digital Garden", "PKM"]
slug: "sustainable-online-publishing"
related_notes:
  - digital-garden
  - drafting-in-public
  - sketchpad
  - the-garage-concept
  - note-relationships
  - commonplace-book
featured: false
draft: true
---

I wanted to **put my work on the web** without begging an algorithm for reach. Social accounts make starting easy - sign up, post, done.

The catch: **you don't own the platform.** Rules change. Reach throttles. Accounts get restricted when enough people complain. Publishing entirely on rented land isn't sustainable if your voice matters long-term.

---

## The problem with social-only publishing

Facebook, X, YouTube, TikTok - they're useful **distribution**. They're terrible **sole archives.**

- Terms of service shift
- Monetization and reach change overnight
- Content disappears behind logins or dies when the app pivots
- Your best thread from 2019 isn't on your resume - it's on their servers

I still use social. I don't **trust** it as my only library.

---

## Sustainable publishing = domain + hosting you control

**Domain** - cheap annual rent on a name people can remember (`jorap.com`, `ideas.jorap.com`).

**Hosting** - where the files live. Classic hosting bills monthly. Static hosting can be **free** if you accept some technical shape:

| Piece | Role |
|---|---|
| **Hugo** (or similar) | Markdown → static HTML for the main site |
| **TiddlyWiki** | Second Brain that can also publish as static HTML |
| **GitHub** | Version control + backup |
| **Cloudflare Pages** | Build and serve on push - free tier |

That's the workflow behind JoRap Notes and [ideas.jorap.com](https://ideas.jorap.com/): **capture in TiddlyWiki, version in Git, publish on Cloudflare.**

I wrote the longer migration story in [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/) - this post is the philosophy slice.

---

## What "sustainable" doesn't mean

- Not "never use social again"
- Not "build everything custom for ego"
- Not "free means zero effort" - you trade money for Git pushes and Markdown

It means **the canonical copy lives somewhere you control**, and social becomes the megaphone - not the vault.

---

## Practical starting point

1. Buy a domain you won't hate in five years
2. Pick a static generator you can live with (Hugo worked for me)
3. Put content in Git from day one
4. Connect Cloudflare Pages (or Netlify, etc.) to auto-deploy
5. Share links on social - don't write only in the social text box

---

## How ideas.jorap.com fits

My wiki is where ideas start messy. Some become blog posts. Some stay reference forever. Publishing the wiki itself - even read-only - means **my notes have a URL I own**, not a Notion link that might change pricing.

Second Brain **capture**. Blog **express**. Same person, different stages.

---

## Bottom line

Social media is a great lobby. It's a bad foundation.

Sustainable online publishing is **your domain, your files, your deploy** - with social as optional amplification.

The stack can be free. The habit of owning your work is the part that compounds.

*Expanded from [Sustainable Online Publishing Workflow](https://ideas.jorap.com/) on [ideas.jorap.com](https://ideas.jorap.com/).*
