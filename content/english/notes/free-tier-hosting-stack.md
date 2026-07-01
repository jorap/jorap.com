---
title: "Free Tier Hosting Stack"
meta_title: "Free Tier Hosting Stack - Hugo, GitHub, Cloudflare Pages"
description: "My default client host: Hugo builds static HTML, GitHub stores the repo, Cloudflare Pages deploys on push - free until limits force an upgrade."
date: 2026-06-29T10:05:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Website Building", "Static Site Generator", "Hugo", "GitHub", "Cloudflare Pages", "Free Hosting", "DevOps"]
slug: "free-tier-hosting-stack"
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "JoRap.com on this stack for months. What's the move?"
    back: "Notice"
  - front: "Build failed until Hugo was pinned. What's the move?"
    back: "Env var on every new project template now"
draft: false
aliases: ["github cloudflare stack", "free static hosting"]
---
**Free tier hosting stack** = Hugo builds static HTML, GitHub stores the repo, Cloudflare Pages builds and serves on every push - $0 until account limits or client policy say upgrade.

## Key Concept

Full walkthrough: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/).

Same pipeline for [[Selling Static Sites]] and my [[Digital Garden]] - markdown in, fast site out, no PHP patch Tuesday. **Hugo** turns markdown plus theme into plain HTML. **GitHub** is source of truth and backup (private client repos are fine on free GitHub). **Cloudflare Pages** builds on push, serves over CDN with HTTPS. Flow: edit → `git push` → live in about ninety seconds. No database, no admin panel - which is why [[Static Site Client Scope]] matters.

**Pin env vars on every project:** set `NODE_VERSION` and `GO_VERSION` as **build-time** vars in the Pages dashboard (Settings → Build → Variables) - `wrangler.toml [vars]` are runtime-only and won't apply at build. Pin Hugo once in a versions file the build script reads. Enable **Build cache** in Pages (one-time) plus Hugo `--cacheDir .cache` in the build script. Enable **Git submodules** in Pages settings if the theme is a submodule. Version drift and missing submodules are the most boring deploy failures.

**Save builds:** batch commits before push; `[skip ci]` for non-site files (`.specstory`, internal `docs/`). Run `scripts/setup-git-hooks.sh` to auto-append skip markers. Client template: `docs/CLIENT_STATIC_SITE.md`.

**Free tier headroom** (re-read [Cloudflare limits](https://developers.cloudflare.com/pages/platform/limits/) before quoting): about 500 builds per month, 1 concurrent build, 20,000 files per deployment, unlimited static bandwidth, 20-minute build timeout. Normal brochure sites sit far below that. Risk shows up when one account hosts many clients who deploy often, or themes ship huge unoptimized image trees.

**When free tier stops fitting:** move to the client's Cloudflare account, trim file bloat, step up to Pages Pro (~$20/mo) for build volume, or split projects across accounts. Domain stays separate (~$12/year). Early pilots can live on my account; before scale, production should move to **client-owned Cloudflare plus GitHub** with a one-page handoff doc. [[Future-Proofing Knowledge]] parallel: markdown in git is the portable asset; Cloudflare is swappable hosting.

## Examples

- JoRap.com on this stack for months - domain is the only recurring bill I notice.
- Build failed until Hugo was pinned - env var on every new project template now.
- Client wanted daily CMS auto-deploy fantasy - counted builds per month; static plus Git pushes stay inside free tier for normal humans.
- Shop hit file count on a bloated theme - trimmed assets before anyone paid for Pro.
- Submodule theme broke Pages until I enabled submodule cloning in project settings.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| contradicts | [[Building a Personal API]] | when the site needs a live API and database, not static HTML |
| contradicts | [[Local-first Software]] | when the workflow needs sync apps, not git-push-to-deploy |
| extends | [[Digital Garden]] | Same Hugo-plus-git publish lane I use for the notes garden |
| extends | [[Future-Proofing Knowledge]] | Markdown in git survives; hosting vendor is swappable |
| extends | [[Getting Started]] | Same markdown-first workflow as garden notes |
| extends | [[Selling Static Sites]] | Default host for client static sites until limits force upgrade |
| extends | [[Static Site Client Scope]] | Stack limits define what jobs fit |
| implements | [[Rollback Principle]] | Git revert and previous Cloudflare deploy are the rollback lane |

## See also

- [[Git-Based CMS]] - Hugo, Static Site Generator, Website Building
- [[The Garage Concept]] - Hugo, Static Site Generator, Website Building
- [[Client Site Handoff]] - Static Site Generator, Website Building
