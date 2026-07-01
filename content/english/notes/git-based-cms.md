---
title: "Git-Based CMS"
meta_title: "Git-Based CMS - Buttons for Non-Git Editors"
description: "A web editor (I use Sveltia or Decap) that commits markdown to the repo - same [[Free Tier Hosting Stack]] build on push, but the client gets buttons instead of VS Code."
key_concept: |
  I publish via Git directly.
  
  Clients often won't. Before I redirect them to WordPress, this is the middle path: marketing volunteer, pastor's secretary, family member posting updates - still static HTML out the other end, still free tier hosting if deploy volume stays sane. Git stays source of truth; the CMS is just another commit path. More setup than raw markdown (auth, config, media folders) - quote it, don't tuck it in "theme tweaks." **When it fits [[Static Site Client Scope]]:** one or two non-technical editors, occasional posts, no member login, no cart. **When it doesn't:** five daily editors with workflows, private content, or "make it exactly like our old WordPress admin" without budget for config. Still say no to bad dynamic scope - CMS doesn't add a database. **Ops I don't skip:** treat the CMS like a small production app (auth, who can publish, which branch). Pin the same `HUGO_VERSION` on Cloudflare. Count CMS-triggered builds toward the monthly quota. [[Minimum Effective Dose]] for solo sites: skip the CMS layer entirely.
examples:
  - "Church volunteer won't open a terminal - Sveltia on the repo, she edits announcements, Cloudflare rebuilds on save."
  - "I added Decap for a client who insisted on \"WordPress-like\" - honest scope: blog posts only, not plugins; still cheaper than hosted WordPress long term."
relationships:
  - type: contradicts
    wikilink: "[[Minimum Effective Dose]]"
    reason: "when a solo dev site doesn't need a CMS layer on top of markdown"
  - type: extends
    wikilink: "[[Client Site Handoff]]"
    reason: "CMS handoff is a fourth path when Git lesson won't land"
  - type: extends
    wikilink: "[[Free Tier Hosting Stack]]"
    reason: "Still markdown in git, still Cloudflare build on push"
  - type: extends
    wikilink: "[[Static Site Client Scope]]"
    reason: "Widens who can edit without redirecting to WordPress"
slug: "git-based-cms"
date: "2026-06-28 10:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Website Building", "Hugo", "CMS", "Static Site Generator", "Freelance", "Git"]
aliases: ["Sveltia CMS", "Decap CMS", "git backed cms", "git based cms"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "Church volunteer won't open a terminal. What's the move?"
    back: "Cloudflare rebuilds on save"
  - front: "I added Decap for a client who insisted on \"WordPress-like\""
    back: "Still cheaper than hosted WordPress long term"
draft: false
---
