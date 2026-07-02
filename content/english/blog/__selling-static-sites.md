---
title: "How I Quote Client Websites"
meta_title: "How I Quote Client Websites - Clear Line Items, No Mystery Fees"
description: "I break quotes into pieces you can read - discovery, build, migration, handoff, hosting. No bundled fog, no invoice that mixes labor with server rent you can't audit."
slug: "selling-static-sites"
date: 2026-07-02T05:00:00Z
image: "/images/website.jpg"
categories: ["Website", "Business", "Tips"]
author: "JoRap"
tags: ["Website Building", "Freelance", "Static Site Generator", "Hugo", "Cloudflare Pages", "GitHub", "Client Work", "Pricing", "Business", "Web Hosting"]
related_notes:
  - selling-static-sites
  - static-site-client-scope
  - client-site-handoff
  - plain-commitments-at-work
featured: false
draft: true
---

> **TL;DR**: I quote discovery, build, migration, handoff, and hosting as separate line items. You see what labor costs and what infrastructure costs - no $25/month "maintenance" bundle that hides half the bill in mystery server rent.

## The old way cost me money and trust

For years I shared a basic PHP hosting plan with a client - about $12 a month for both of us. When they moved on, I was paying the whole bill for what was basically my personal blog. That was my wake-up call about **marking up hosting**.

I also watched agencies sell "website packages" where half the monthly fee was mystery server rent the client could never audit. The site was a brochure. The bill looked like enterprise infrastructure.

I don't want to be that person. When I quote a client site now, I want them to understand **exactly** what each line item covers - labor, hosting, updates - without a bundled number that mixes all three.

---

## What I actually charge for

Every quote breaks into pieces the client can see:

**Discovery and scope.** Before I touch a theme, I run a short fit check: who updates content, how often, anything behind login, anything that needs a live database. If the job is a bad fit for a static stack, I say so in the room - not after they paid a deposit. That conversation is billable or folded into the build, but it always happens first.

**Repo and deploy setup.** New GitHub repo, Cloudflare Pages project, `HUGO_VERSION` and `NODE_VERSION` pinned in the build settings. Sounds boring. It is boring. It's also the difference between "push and live in ninety seconds" and "why is the build failing again."

**Theme and layout.** The visual shell, navigation, mobile behavior, contact form wiring, whatever the site actually needs to look credible.

**Content migration.** Moving copy, images, and old pages from whatever they had before - Facebook-only presence, a WordPress install, a pile of Google Docs, a PDF brochure.

**Handoff, priced separately.** Who publishes after launch? That's not a footnote. I price it as its own line because the answer changes the whole project. More on that in a separate post, but the short version: Git lesson, retainer batches, showroom branch, or a Git-based CMS - pick one before deposit.

**Retainer updates, if they want them.** Email me copy, I push on a schedule. Priced per batch, not folded into a vague monthly fee.

**Hosting and deploy.** CDN, HTTPS, build pipeline, account setup. Priced honestly - usually a modest annual or monthly line, not a bloated "package" left over from the cPanel era. Domain (~$12/year) stays visible and paid to the registrar.

---

## Why this stack keeps hosting lean

I run [jorap.com](/) on Hugo, GitHub, and Cloudflare Pages. Client sites use the same lane: markdown content, git push, live in about ninety seconds. No database to patch. No PHP version drama. No cPanel login nobody remembers.

That stack has limits. I'm honest about those too. It's not for online stores you host, member logins, or five non-technical editors publishing daily with no training. When the fit is wrong, I point them at Shopify, WordPress, or whoever actually solves the job.

When the fit is right - portfolio, org brochure, small business presence, sermon archive, project docs - hosting stays a small, predictable part of the quote. A neighbor's portfolio and a pastor's sermon archive both run on the same pipeline without enterprise hosting bills.

---

## What a real quote looks like

Rough shape, not a price list (every job differs):

| Line item | What it covers |
| --- | --- |
| Discovery | Fit check, sitemap, publish-path decision |
| Build | Repo, deploy, theme, core pages |
| Migration | Content and media from old sources |
| Handoff | Training, one-page doc, or CMS setup |
| Domain | ~$12/year, paid to registrar, visible |
| Hosting | CDN, HTTPS, deploy pipeline - priced in writing |

No "starting at" fog. No bundled mystery fees. If they want me on retainer after launch, that's a separate conversation with a real scope.

---

## How I grow the offer without a sales brochure

I didn't start with a three-tier pricing PDF. I started with **one paid pilot** - build the site, note what broke, fix the template, quote the next job faster.

Neighbor wanted a portfolio. Quoted build plus domain. She chose the Git lesson handoff, broke the build once fixing a typo, and fixed it the same night. That's more proof than any "services" page I could have polished first.

Pastor wanted a sermon archive. Static fit. Said no to member login. Scoped brochure plus archive pages only. Bulletin updates go through a retainer batch every Friday - one push, no CMS layer he didn't need.

Each job teaches me what to put in the base template so the next quote takes less guesswork. That's the loop: ship, learn, tighten, quote faster.

---

## When the default setup isn't enough

Heavy deploy habits, huge media folders, or policy requirements can push a site past what the starter hosting line covers. Some clients want their own Cloudflare org from day one. Concurrent builds can queue when volume spikes.

When that happens, we talk upgrade paths before it becomes an emergency - not after the invoice surprises everyone. Hosting scales with the job; the quote should say so upfront.

---

## What I'd tell a friend hiring someone like me

Ask your developer what's actually in the monthly fee. If they can't separate build from hosting from "maintenance," ask harder.

Ask who publishes after launch **before** you sign. "We'll figure it out at go-live" is how WordPress-style expectations land on a static stack and explode in week two.

Ask what happens if the fit is wrong. A yes on every job is not credibility. A clear no with a referral is.

I charge for work that moves the needle and hosting that's priced to match the job - not a padded monthly line left over from when every brochure needed a $12 PHP plan. That's the whole pitch - and I'd rather lose a job than hide what's in the quote.
