---
title: "Sustainable Online Publishing"
meta_title: "Sustainable Online Publishing - Own Your Site"
description: "Social media is easy to start and risky to depend on. I publish on my own site anyway - a free stack that works and why the habit matters more than the tools."
slug: "sustainable-online-publishing"
date: "2026-06-12T14:58:00Z"
image: "/images/sustainable-publishing.jpg"
categories: ["Website", "Ideas", "Technology"]
author: "JoRap"
tags: ["Publishing", "Self-Hosting", "Hugo", "Cloudflare Pages", "Content Ownership", "Platform Risk", "Blogging", "Digital Garden"]
related_notes:
  - digital-garden
  - drafting-in-public
  - the-garage-concept
  - note-relationships
  - commonplace-book
  - success-is-stewardship
featured: false
draft: false
---

Every few months someone asks why I bother with a website when I could just post on Facebook. Fair question. Signing up takes five minutes. The audience is already there. You don't have to think about hosting or deploys or why your build failed at 11pm.

I still wanted **my work on the web** without begging an algorithm for reach. Social makes starting easy. The catch is you don't own the platform. Rules change. Reach throttles. Accounts get restricted when enough people complain. I learned that the hard way when I lost old PHP hosting and a chunk of my work with it - not a social ban, but the same lesson: **rented land is rented land.**

Publishing only on platforms you don't control isn't sustainable if your voice matters past this quarter.

---

## Social is a lobby, not a library

Facebook, X, YouTube - I still use them. They're fine for **getting a link in front of people.** They're a terrible place to keep the only copy of something you care about.

Terms of service shift. Monetization rules change overnight. Content disappears behind logins or dies when the app pivots. Your best thread from 2019 isn't on your resume - it's on their servers, and you can't export it cleanly if they decide you can't.

I don't treat social as my archive. I treat it as the thing I point at my archive.

---

## Sustainable publishing = a domain and files you control

**Domain** - cheap annual rent on a name people can remember (`jorap.com`). Buy something you won't cringe at in five years.

**Hosting** - where the files actually live. Classic hosting bills monthly. Static hosting can be **free** if you're willing to learn a little Git and Markdown:

| Piece | Role |
|---|---|
| **Hugo** (or similar) | Markdown → static HTML for the main site |
| **GitHub** | Version control + backup |
| **Cloudflare Pages** | Build and serve on push - free tier |

No database, no admin panel, no PHP cron jobs to babysit.

---

## What I don't mean by "sustainable"

I'm not saying quit social. I'm not saying build everything custom to prove you're serious. And free hosting doesn't mean zero work - you trade a monthly bill for Git pushes and Markdown files.

What I mean is simpler: **the real copy lives somewhere you control.** Social is the megaphone. Not the vault.

---

## If you're starting from zero

1. Buy a domain you won't hate in five years
2. Pick a static generator you can live with (Hugo worked for me; write down the version number the day you install it)
3. Put content in Git from day one - that's your backup whether you think you need it yet or not
4. Connect Cloudflare Pages (or Netlify, etc.) to auto-deploy on push
5. Share links on social - don't write only in the social text box

You don't need the full stack on day one. Domain + Git + static hosting is enough.

---

## Bottom line

Social media is a great lobby. It's a bad foundation.

Sustainable online publishing is **your domain, your files, your deploy** - with social optional when you want people to notice.

The stack can be free. The habit of owning your work is the part that compounds.
