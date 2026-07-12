---
title: "Hugo Static Site Generator"
meta_title: "Hugo as a Static Site Generator - Why I Still Use It"
description: "Hugo turns Markdown into HTML at build time - no database, no PHP surprises. After losing old hosting, it's the engine behind JoRap Notes and most client sites I quote."
date: 2026-06-19T06:00:00Z
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Static Site Generator", "JAMstack", "Web Development", "JoRap Notes", "Cloudflare Pages", "PKM", "Publishing", "Digital Garden"]
slug: "hugo-static-site-generator"
related_notes:
  - the-garage-concept
  - digital-garden
  - drafting-in-public
  - sketchpad
  - free-tier-hosting-stack
  - selling-static-sites
featured: false
draft: true
---

A **static site generator** pre-builds HTML when you deploy - not when someone visits. No database on the server. No PHP cron jobs. No "why is admin slow at 2 AM."

**Hugo** is one of those generators: single Go binary, stupid fast builds, Markdown in, HTML out.

JoRap Notes runs on Hugo + GitHub + Cloudflare Pages. I push a post at lunch; it's live before I finish coffee. That rhythm is why I keep recommending Hugo for the right jobs - and saying no when it isn't.

---

## The push that actually made me switch

I'd been on shared PHP hosting for years. Modest monthly bill, split with a client. Client left, I kept paying for what was basically a personal blog. Then the host died and took a chunk of my work with it.

I'd heard about static sites forever. Losing hosting was the shove. Weekend of fumbling, Hugo won, [I wrote the longer migration story](/blog/how-i-built-jorap-notes/) when the dust settled.

The surprise wasn't speed - though pages feel instant. It was **boring infrastructure.** Nothing to patch mid-week except my own typos.

---

## Speed at build and browse

Hugo builds thousands of pages in seconds on a laptop. Served pages are plain files on a CDN. No WordPress plugin stack waiting to break on a security update.

For a text-heavy personal site, that trade is easy: give up the admin panel, gain sleep.

---

## Content as files in Git

Every post is a Markdown file. Diffable. Revertible. Movable to another host by pointing DNS and pushing the same repo.

When a platform owns your posts, you're renting. When they're in Git, you're holding the deed. I learned that lesson the expensive way once.

---

## Theme separation (mostly)

[Hugoplate](/blog/hugoplate-theme-review/) handles layout; `content/` is mine. Theme updates merge upstream; posts stay put.

"Mostly" because I live inside the theme for Tailwind tweaks and custom partials. It's not a black box you never touch. It's a starter you fork and own.

---

## Where Hugo is the wrong answer

I say no out loud for:

- E-commerce you host
- Member logins and session state
- Five non-technical editors publishing daily with no training plan

For those, WordPress, Shopify, or a hosted tool wins. [Static vs CMS](/blog/static-site-vs-cms/) is the longer fit check I use with clients.

For a blog, portfolio, brochure site, sermon archive, or docs that change occasionally - Hugo is hard to beat on cost and calm.

---

## Bottom line

Hugo fits **personal publishing with technical comfort:** Markdown, Git, hatred of monthly hosting bills for static pages.

It doesn't fit every job. When it fits, the workflow is push and forget. That's the feature I sell - including to myself.
