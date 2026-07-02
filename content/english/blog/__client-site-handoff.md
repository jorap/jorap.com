---
title: "What Happens After Your Website Goes Live"
meta_title: "Client Site Handoff - Who Publishes After Launch"
description: "Launch day isn't the finish line. Before deposit I name who publishes next - Git lesson, retainer batches, showroom branch, or CMS - and I leave a one-page doc so you're not stuck calling me for every typo."
slug: "client-site-handoff"
date: 2026-07-02T07:00:00Z
image: "/images/website.jpg"
categories: ["Website", "Business", "Tips"]
author: "JoRap"
tags: ["Website Building", "Freelance", "Client Work", "Handoff", "Static Site Generator", "GitHub", "Business", "Documentation"]
related_notes:
  - client-site-handoff
  - selling-static-sites
  - static-site-client-scope
  - share-what-you-learn
  - the-garage-concept
  - plain-commitments-at-work
featured: false
draft: true
---

> **TL;DR**: Pick exactly one publish path before deposit - not "we'll figure it out at launch." I hand off a one-page doc with repo URL, deploy settings, DNS, and who to call when the build fails. The goal is a site you can run without me in the loop for every comma.

## Launch day is when the real job starts

I've seen sites go live to applause and die quietly six weeks later because nobody agreed on **who publishes next**.

The developer disappears. The client opens cPanel out of habit and finds nothing familiar. Staff still email copy to someone's personal Gmail. Typos sit for a month because "that's a developer thing."

That's not a hosting problem. It's a **handoff** problem - and it should be solved in the sales call, not improvised over Zoom while the DNS is still propagating.

---

## Four paths I actually use

Every client picks **one primary model**. Not a buffet. Not "we'll see." One path, named in the proposal, priced if it costs extra.

### Git lesson

The owner gets repo access and a short doc: here's the file, edit the text between these marks, commit, push, wait ninety seconds.

Fits people who want control and won't panic at a terminal. My neighbor chose this for her portfolio. I spent about twenty minutes walking through edit, commit, push. She broke the build once fixing a typo - YAML indentation, classic - and fixed it the same night without calling me. That's the test.

### Retainer batches

They email copy, photos, or PDFs; I push on a schedule. Priced per batch, not disguised as monthly hosting.

A pastor sends the bulletin every Friday. One push. No CMS layer he didn't need. He doesn't want Git. He wants the site current before Sunday. Fine.

### Showroom branch

My experiments stay off their deploy branch. What they see is clean `main` only - the garage concept applied to client work. Their site stays a showroom even when I'm testing layout ideas elsewhere in the repo.

Good when they want stability and I still need a sandbox.

### Git-based CMS

When Git won't land but scope still fits static. Buttons instead of terminal. Sveltia or similar - quoted separately from the build because setup and training take real time.

Middle path between "learn Git" and "install WordPress for a five-page brochure."

---

## The handoff that always fails

Promise WordPress-style daily edits to five non-technical staff **with no training, no retainer, and no CMS**.

That's not a static site handoff. That's a scope lie from the sales call finally catching up. Week two someone asks why they can't "just log in and fix the header like the old site." Because we never chose a publish path. Because static doesn't have a mystery admin panel unless we build one on purpose.

If that's what the job needs, WordPress or a CMS layer should have been in scope from day one - with the price and training to match.

---

## The one-page doc I leave behind

The product isn't tribal knowledge in my head. It's a single page the client can forward to their successor:

- **Repo URL** and who has access
- **Cloudflare project** name and which branch deploys
- **Environment variables** that matter (`HUGO_VERSION`, `NODE_VERSION`, anything custom)
- **Domain and DNS** - where the registrar is, what points where
- **Build failures** - the three boring fixes (version mismatch, bad frontmatter, asset too large)
- **Who to call** when none of that works

If they can publish a correction without a panic call, handoff worked. If every comma routes through my inbox forever, I underpriced the job or skipped the training line item.

---

## What I price separately (on purpose)

Build and handoff are different work. Setup is theme, pages, migration, deploy. Handoff is training, documentation, CMS wiring, or an ongoing retainer agreement.

Bundling them into one opaque number sounds simpler. It isn't. Clients forget what they paid for. I forget what I promised. Separate lines keep **plain commitments** plain.

Retainer isn't "hosting." It's labor on a schedule. Say that in writing so nobody thinks the hosting line covers unlimited content changes they never scoped.

---

## Questions to ask before you hire anyone

If you're the client - or you're writing the brief for your org - ask these before deposit:

**Who publishes the first typo fix after launch?** Name a person and a method.

**What does "emergency" mean?** Site down is different from "we need a new photo on the about page by 4pm."

**What do I own if we part ways?** Repo access, domain registrar login, Cloudflare account - all of it should be yours, not rented through the developer's email.

**What's not included?** New sections, seasonal campaigns, integration with a tool you haven't bought yet. Surprises here are how friendships end.

I ask the same questions from my side. If the answers are fuzzy, we fix them before money moves.

---

## Why this matters for credibility

Anyone can make a pretty homepage. The hireable part is whether the site **keeps working** when the meeting ends.

Clients don't remember your build pipeline. They remember whether Tuesday's announcement went live without a crisis. They remember whether the handoff doc existed when your phone was off.

I'd rather lose a job than promise a publish path I won't support. I'd rather price training honestly than absorb unlimited "small tweaks" until I resent the client.

Launch is not the finish line. It's the handoff. Get that right and the build actually earns its keep.
