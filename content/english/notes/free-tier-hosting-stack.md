---
title: "Free Tier Hosting Stack"
meta_title: "Free Tier Hosting Stack - Hugo, GitHub, Cloudflare Pages"
description: "Hugo, GitHub, and Cloudflare Pages ship static sites for $0 - until build caps, queues, or account limits bite."
key_concept: |
  - **Free tier is not unlimited.** Re-read [Cloudflare limits](https://developers.cloudflare.com/pages/platform/limits/) before quoting anything to a client. Hard caps on the free plan: about **500 builds per month** (whole account, not per site), **1 concurrent build** (second push waits in line), **20,000 files per deployment**, **20-minute build timeout**. Static bandwidth is unmetered - that part is genuinely generous. The traps are build count, queue time, and fat repos.
  
  - Full walkthrough: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/). Same pipeline for [[Selling Static Sites]] and the [[Digital Garden]] - markdown in, fast site out, no PHP patch Tuesday. **Hugo** turns markdown plus theme into plain HTML. **GitHub** is source of truth and backup (private client repos are fine on free GitHub). **Cloudflare Pages** builds on push, serves over CDN with HTTPS. Flow: edit → `git push` → live in about ninety seconds. No database, no admin panel - which is why [[Static Site Client Scope]] matters.
  
  - **Where free breaks first:** one account hosting many clients who push often burns the 500-build budget fast. A theme with thousands of unoptimized images can hit the 20k-file cap. One slow Hugo build plus a second push means the second deploy sits behind the first - fine for a solo site, painful when three clients want Friday updates. GitHub free is separate but has its own limits (Actions minutes if you use them; plain git push hosting is usually fine until the repo is huge).
  
  - Hugo, GitHub, and Cloudflare Pages ship static sites for $0.
  
  - Until build caps, queues, or account limits bite.
examples:
  - "Twelve client sites on one free account - hit 500 builds mid-month and Friday deploys started queuing."
  - "Build failed until Hugo was pinned - env var on every new project template now, and that failure still counted against the cap."
shareable_thought:
  - "Hugo, GitHub, and Cloudflare Pages ship static sites for $0."
  - "Until build caps, queues, or account limits bite."
  - "Free tier is not unlimited."
  - "Static bandwidth is unmetered - that part is genuinely generous."
relationships:
  - type: contradicts
    wikilink: "[[Building a Personal API]]"
    reason: "when the site needs a live API and database, not static HTML"
  - type: contradicts
    wikilink: "[[Local-first Software]]"
    reason: "when the workflow needs sync apps, not git-push-to-deploy"
  - type: extends
    wikilink: "[[Digital Garden]]"
    reason: "Same Hugo-plus-git publish lane I use for the notes garden"
  - type: extends
    wikilink: "[[Future-Proofing Knowledge]]"
    reason: "Markdown in git survives; hosting vendor is swappable"
  - type: extends
    wikilink: "[[Getting Started]]"
    reason: "Same markdown-first workflow as garden notes"
  - type: extends
    wikilink: "[[Selling Static Sites]]"
    reason: "Default host for client static sites until limits force upgrade"
  - type: extends
    wikilink: "[[Static Site Client Scope]]"
    reason: "Stack limits define what jobs fit"
  - type: extends
    wikilink: "[[Success is Stewardship]]"
    reason: "Steward the build budget on borrowed infra"
  - type: implements
    wikilink: "[[Rollback Principle]]"
    reason: "Git revert and previous Cloudflare deploy are the rollback lane"
  - type: implements
    wikilink: "[[Staged Rollout]]"
    reason: "PR preview deploy before Pages merges to main"
slug: "free-tier-hosting-stack"
date: "2026-06-29 10:05:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["Website Building", "Static Site Generator", "Hugo", "GitHub", "Cloudflare Pages", "Free Hosting", "DevOps"]
aliases: ["github cloudflare stack", "free static hosting"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "500 builds per month sounds huge until twelve clients deploy weekly. What's the move?"
    back: "Client-owned Cloudflare account or Pages Pro before month-end crunch"
  - front: "Build failed until Hugo was pinned. What's the move?"
    back: "Env var on every new project template now"
draft: false
---

