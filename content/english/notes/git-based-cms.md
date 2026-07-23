---
title: "Git-Based CMS"
meta_title: "Git-Based CMS - Buttons for Non-Git Editors"
description: "A git CMS commits markdown to the repo so clients get buttons while the same push-live build still runs."
key_concept: |
  - Publish via Git directly when you are the author; clients often will not.
  - Level 1: You push through Git when you write the site - clients need buttons, like cooking versus a menu with pictures.
  - Level 2: Git-based CMS is like a kitchen with a back door for chefs and a counter for customers - Git for authors, buttons for clients who will never touch a terminal.
  - Level 3: Because Git stays source of truth, the CMS is just another commit path - not a second database that forks reality.
  - Level 4: Use Git publish for solo sites; offer a CMS when the client will never touch a terminal - still say no to bad dynamic scope.
  - Level 5: Git stays source of truth; the CMS is just another commit path - [[Minimum Effective Dose]] for solo sites is skip the CMS layer entirely.
  - Git stays source of truth; the CMS is just another commit path.
  - Still say no to bad dynamic scope - CMS does not add a database.
  - [[Minimum Effective Dose]] for solo sites: skip the CMS layer entirely.
examples:
  - "Church volunteer will not open a terminal - Sveltia on the repo, she edits announcements, Cloudflare rebuilds on save."
  - "I added Decap for a client who insisted on WordPress-like editing - honest scope: blog posts only, not plugins; still cheaper than hosted WordPress long term."
shareable_thought:
  - "A git CMS commits markdown to the repo so clients get buttons while the same push-live build still runs."
  - "Still say no to bad dynamic scope."
  - "CMS does not add a database."
  - "Publish via Git directly when you are the author; clients often will not."
relationships:
  - type: contradicts
    wikilink: "[[Minimum Effective Dose]]"
    reason: "when a solo dev site does not need a CMS layer on top of markdown"
  - type: extends
    wikilink: "[[Client Site Pass-Off]]"
    reason: "CMS pass-off is a fourth path when Git lesson will not land"
  - type: extends
    wikilink: "[[Free Tier Hosting Stack]]"
    reason: "Still markdown in git, still Cloudflare build on push"
  - type: extends
    wikilink: "[[Static Site Client Scope]]"
    reason: "Widens who can edit without redirecting to WordPress"
slug: "git-based-cms"
date: "2026-06-28 10:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["Website Building", "Hugo", "CMS", "Static Site Generator", "Freelance", "Git"]
aliases: ["Sveltia CMS", "Decap CMS", "git backed cms", "git based cms"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "Church volunteer won't open a terminal but needs to edit announcements. What's the middle path?"
    back: "Git CMS on the repo - Cloudflare rebuilds on save."
  - front: "Client insists on WordPress feel for blog posts only. Honest scope - what's still true?"
    back: "Decap on the repo - still markdown, still cheaper long term."
draft: false
---






