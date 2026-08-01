---
title: "I Moved From Free Netlify to Free Cloudflare Pages"
meta_title: "Netlify to Cloudflare Pages - What Actually Changes on Hugo"
description: "HugoPlate pointed me at Netlify. jorap.com runs on Cloudflare Pages now. Same git-push workflow - different build settings, redirects, and CMS auth."
slug: "netlify-to-cloudflare-pages"
date: "2026-07-30T01:00:00Z"
image: "/images/website.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Cloudflare Pages", "Netlify", "Hugo", "Static Sites", "Migration", "Website Building", "DevOps", "GitHub"]
related_notes:
  - free-tier-hosting-stack
  - digital-garden
  - selling-static-sites
  - rollback-principle
level_depth: 3
featured: false
draft: true
---

HugoPlate's docs still show a Netlify tab. Fair - that's where a lot of Hugo themes point you first. I started there too.

Months later, [jorap.com](/) builds on **Cloudflare Pages**. Same repo. Same `git push` habit. The site still goes live in about ninety seconds. What changed was everything *around* Hugo: build command, where redirects live, how the CMS logs in, and how picky I got about burning deploys.

If you're on free Netlify with a static Hugo site and wondering whether Cloudflare is worth the afternoon, this is the move I actually made - not a vendor shootout.

---

## Why I bothered

Netlify worked. I'm not writing a breakup letter.

I moved because I wanted **one place** for DNS, CDN, and deploys. My domain already lived in Cloudflare's orbit. Running builds on Netlify while apex redirects and analytics argued with Cloudflare settings felt like paying rent in two buildings for one apartment.

The free tier math also lines up better with how I publish. Cloudflare Pages gives you **unmetered bandwidth** on static assets. The catch is build count - about **500 builds per month per account**, one at a time. Netlify's free tier caps build minutes instead. Neither is infinite. For a personal Hugo blog with batched commits, Cloudflare's meter matched my rhythm. Your push habits might differ.

I also run a **git-based CMS** at `/admin`. Netlify Identity was never in my stack. I needed GitHub OAuth on the host. Cloudflare Pages Functions gave me `/api/auth` and `/api/callback` without spinning up a separate server. That alone would have pushed me toward Pages eventually.

---

## What stays the same

If your site is already "Markdown in Git → CI builds HTML → CDN serves files," the migration is a hosting swap, not a rewrite.

- **GitHub** still holds the source. Every post is still a file you can clone.
- **`public/`** is still the output folder Hugo produces.
- **`_redirects`** uses the same Netlify-style syntax Cloudflare copied. Rules like `/old-path /new-path 301` still work.
- **Custom domains** still mean "point DNS, wait, test."

You are not learning a new CMS or exporting a database. You're re-pointing the build hook.

---

## What I changed in the repo

### Build command

Netlify examples often stop at `hugo` or `npm run build`. My production build is **`pnpm run deploy`**, which runs theme generation, note dates, Hugo with a cache dir, OKF exports, and CSP hashing. Cloudflare runs `pnpm install` automatically; I don't add an extra `npm install` hop on top.

In the Pages dashboard:

| Setting | Value |
| --- | --- |
| Build command | `pnpm run deploy` |
| Output directory | `public` |
| `NODE_VERSION` | pinned (see `scripts/deploy-versions.json`) |
| `GO_VERSION` | pinned for Hugo modules |

Hugo itself is **not** something I trust the platform to have preinstalled. `scripts/ensureHugo.mjs` downloads the exact version from `deploy-versions.json` during every build. Version drift between my laptop and the server was the most boring deploy failure I hit on Netlify. I fixed it once in-repo so every host behaves the same.

### Redirects belong in `static/`

This one bit me during the move.

`_redirects` at the **repo root** does not land in `public/` after Hugo runs. Netlify tutorials sometimes leave it there. Cloudflare only sees what ships in the build output.

Mine lives in **`static/_redirects`** - apex to `www`, a few renamed note paths, a 404 fallback. After deploy, I check the latest build's asset list and confirm `_redirects` exists at the site root. If apex still 404s, DNS is usually wrong, not Hugo.

### Headers and CSP

Cloudflare Pages drops HTTP header values over about **2 KB**. My Content-Security-Policy was longer than that once the site grew Disqus, analytics, and inline theme scripts.

`scripts/cspHashes.mjs` runs after Hugo and rewrites `public/_headers` with hashed allowances. That script is part of `pnpm run deploy`, not a manual step I remember on Fridays.

### CMS OAuth (only if you use `/admin`)

If you edit through the browser UI, the host needs OAuth endpoints.

I added **`functions/api/auth.js`** and **`functions/api/callback.js`**, plus `wrangler.toml` with the Pages project name and a public `GITHUB_CLIENT_ID`. The client secret lives as a dashboard secret - not in git.

GitHub OAuth app callback URL must match the canonical host (`https://www.jorap.com/api/callback` for me). Rocket Loader broke the admin once; the CMS script tag carries `data-cfasync="false"` so Cloudflare leaves it alone.

Full wiring is in the repo's `docs/CMS_SETUP.md` if you need the checklist.

### Deleted stale config

`netlify.toml`, old Vercel files, duplicate amplify configs - gone. One deploy path. Less "which file does CI actually read?"

---

## The migration afternoon

Rough order that worked for me:

1. **Create a Cloudflare Pages project** connected to the same GitHub repo and production branch.
2. **Set build command and output dir** to match what Netlify was already producing - or what `pnpm run deploy` produces if your pipeline grew legs.
3. **Copy environment variables** (`NODE_VERSION`, `GO_VERSION`, anything your build script reads). Pin versions. Write them down in the repo too.
4. **Enable build cache** in Pages settings. Hugo writes to `.cache` during deploy; the next build is noticeably faster.
5. **Deploy to the `*.pages.dev` URL** and click around. Run `pnpm run deploy` locally first if you can - same failures, no queue.
6. **Add custom domains** in Pages - both apex and `www` if you use both. Fix DNS at the registrar or in Cloudflare.
7. **Verify redirects** with `curl -I` on apex and a renamed path.
8. **Switch production traffic** - update DNS or remove the Netlify site once you're confident.
9. **Delete the Netlify project** so you don't accidentally push to a ghost.

I kept Netlify live until Cloudflare served the same HTML on the preview URL and the custom domain. Paranoia saves rollbacks.

---

## Free tier habits I had to learn

Cloudflare's free Pages tier is generous on bandwidth and stingy on **build slots**.

Every push to `main` triggers a build unless you skip it. I batch content edits into one commit when I can. Tooling-only changes under `.cursor/`, `docs/`, or `.specstory/` get **`[skip ci]`** in the commit message so I don't burn builds on skill tweaks.

That sounds fussy until you've queued behind your own third typo fix in ten minutes.

See also: [Free Tier Hosting Stack](/notes/free-tier-hosting-stack/) if you host more than one site on the same account. Five hundred builds sounds huge until several repos push on Fridays.

---

## What I'd do differently next time

I'd move **`static/_redirects` and version pins on day one**, even on Netlify. Root-level redirect files and "whatever Hugo version the platform has" are time bombs.

I'd run **`pnpm local`** (build + serve on port 8788) before touching DNS. Local Hugo dev and production deploy are not the same pipeline on this site. Previewing the real build caught CSP and missing static files Netlify and `hugo server` both hid from me.

I'd still pick **git as source of truth**. Hosting is rented. Markdown in the repo is mine. Cloudflare, Netlify, or the next thing - the content survives a swap.

---

## If you're still on Netlify

You don't *have* to move. Free Netlify is fine for a personal blog that deploys a few times a week and doesn't need Cloudflare Functions for auth.

Move when you have a concrete reason: DNS already on Cloudflare, build-minute pressure, OAuth on Pages, client sites you want on one account. Not because a blog post said Netlify is dead.

If you do move, treat it as a **hosting config migration**. Same Hugo site. New dashboard fields. One evening of curl tests. Then delete the old project so future-you doesn't wonder which green checkmark is real.
