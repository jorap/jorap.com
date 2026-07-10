---
title: "Free Tier Hosting Stack"
meta_title: "Free Tier Hosting Stack - Hugo, GitHub, Cloudflare Pages"
description: "Hugo, GitHub, and Cloudflare Pages ship static sites for $0 - until build caps, queues, or account limits bite."
key_concept: |
  - Hard caps on Cloudflare free: about 500 builds per month per account, one concurrent build, 20,000 files per deployment, and a 20-minute build timeout.
  - Static bandwidth is unmetered - the traps are build count, queue time, and fat repos.
  - Flow: Hugo turns markdown into HTML, GitHub holds source, Cloudflare Pages builds on push and serves over CDN.
  - Full walkthrough: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/) - same pipeline for [[Selling Static Sites]] and the [[Digital Garden]].
  - No database, no admin panel - which is why [[Static Site Client Scope]] matters.
  - One account hosting many clients who push often burns the 500-build budget fast; pin `HUGO_VERSION` on every project.
examples:
  - "Twelve client sites on one free account - hit 500 builds mid-month and Friday deploys started queuing."
  - "Build failed until Hugo was pinned - env var on every new project template now, and that failure still counted against the cap."
shareable_thought:
  - "Hugo, GitHub, and Cloudflare Pages ship static sites for $0."
  - "Until build caps, queues, or account limits bite."
  - "Static bandwidth is unmetered - the traps are build count, queue time, and fat repos."
  - "No database, no admin panel."
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




