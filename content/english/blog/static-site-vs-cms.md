---
title: "Static Site or CMS? How I Pick the Stack"
meta_title: "Static Site vs CMS - When Each One Actually Fits"
description: "The stack debate is usually the wrong fight. Who publishes, what changes live, and whether you need logins pick static vs WordPress (or a git CMS in between) better than any framework ranking."
date: 2026-07-10T06:00:00Z
image: "/images/static-vs-cms.jpg"
categories: ["Website", "Technology", "Tips"]
author: "JoRap"
tags: ["Website Building", "Static Site Generator", "CMS", "WordPress", "Hugo", "Sveltia CMS", "Web Development", "Tips"]
related_notes:
  - static-site-client-scope
  - git-based-cms
  - selling-static-sites
  - client-site-pass-off
  - minimum-effective-dose
featured: true
draft: false
---

> **TL;DR**: I don't pick Hugo because I like Hugo. I pick it when the site is mostly pages that change occasionally, nobody needs a login wall, and the publish path can stay simple. Two or more "dynamic" yes answers - logins, live database, cart you host, five daily non-technical editors with no plan - and I'm looking at WordPress or Shopify, not a markdown repo.

## The wrong question is "which is better"

The useful question is **what has to change after launch, and who does the changing**.

I've watched this go sideways both ways. A developer ships a gorgeous static portfolio, then the client expects five staff to edit pages like WordPress and nobody learned Git. I've also seen someone spin up WordPress for a four-page brochure, then spend a year patching plugins for a site that updates twice a year.

Neither failure is about the tool being dumb. Both are **stack mismatches** that should have been obvious before the first commit.

I run [jorap.com](/) on Hugo. I've built client sites the same way. I still send people to WordPress when that's the honest answer. Here's the fit check I use - for my own projects and for anyone asking me which way to go.

---

## When I reach for a static site

A static site is pre-built HTML (and assets) served from a CDN. No database at request time. Content usually lives in files - markdown, JSON, whatever - and a build step turns those files into pages.

That sounds technical. Day to day it mostly means **fast, cheap hosting and almost nothing to patch**.

**Portfolios and case studies.** Show work in order, with context, without an algorithm shuffling it. Push when you add a project. Done.

**Brochure sites.** Hours, location, services, team photos, contact form. A cafe menu with a link to the delivery app they already use. Text and images on git push.

**Blogs where one person (or two) owns publishing.** I write in markdown, commit, push. Live in about ninety seconds. No admin panel to log into for my own site - that's a feature for me.

**Docs and reference sites.** Content that changes occasionally. Changelog pages, project wikis, sermon archives without member accounts.

**Sites where the "dynamic" part lives somewhere else.** A gym embeds class schedules from a booking SaaS. Donations go through a third-party form. The shell stays static; the vendor carries the moving part.

The pattern: **mostly read, occasionally updated, no session state you own**. If that describes the job, static is hard to beat on speed, cost, and sleep.

---

## When I reach for a CMS instead

A CMS - WordPress is the one people mean nine times out of ten - keeps content in a database and builds pages on demand (or caches them, but the live app is still there). You get an admin UI, user roles, plugins, the whole familiar WordPress-shaped box.

That's overhead. It's also the right overhead when the job needs it.

**E-commerce you host.** Carts, checkout, inventory, payment flows on your domain. Shopify or WooCommerce territory. Not a markdown repo with hopes.

**Member login and private content.** Clients, students, donors, subscribers behind authentication. Static sites don't have sessions. A git-based CMS doesn't fix that either.

**Booking or inventory in your database.** If the schedule or stock level has to live in your system and update in real time, you're not buying a brochure site.

**Many non-technical editors publishing often.** Five staff posting daily announcements, event updates, news items - WordPress with roles and training can do that. A static repo cannot, unless someone pays for a workflow or learns Git on purpose.

**The owner expects "log in and click Edit".** Some people will never touch a repo. That's not a moral failing. It's a requirement. Match it.

I don't say WordPress because it's easier to build. I say it because **the publish model and the feature set already exist** and fighting that with a static stack is how you get a custom CMS nobody wanted to maintain.

---

## The middle ground: static site, CMS on top

Sometimes the site *is* static - pre-built pages, no database at the edge - but the people updating it won't use Git.

That's where **git-based CMS** tools come in: [Sveltia CMS](/blog/sveltia-cms/), Decap, similar. Buttons instead of terminal. Edits still commit to the repo; the build pipeline stays the same.

I use this when:

- The scope still fits static (brochure, blog, archive)
- The editor is a teammate, volunteer, or client who needs a UI
- We're honest that **someone still has to set up auth, media paths, and broken-build recovery**

It's not WordPress with fewer plugins. It's a bridge. Useful bridge. Wrong default for a solo dev who already lives in VS Code.

Pick it when static is right but Git won't land - not when you actually need logins and a live database.

---

## Five questions that pick the stack

Forget framework rankings for a minute. Answer these:

1. **Who updates content, and how often?** Daily from five people is a CMS job. Monthly from one owner might be static with a simple path.

2. **Anything private behind a login?** Members, clients, students - name it early. Static doesn't do this natively.

3. **Anything that changes in a live database?** Inventory, bookings, user comments, real-time feeds.

4. **Cart or checkout on your domain?** Not "we might sell stickers someday." Actual money moving through your stack.

5. **What happens if your developer (or you) is unavailable for a month?** If publishing stops unless one person checks email, you need a path that doesn't depend on a single inbox.

**Two or more dynamic yes answers** → CMS territory (WordPress, Shopify, whatever fits the job). **One yes** might be fine with an embed or external tool carrying the dynamic part. **Zero yes answers** → static is probably the honest pick.

---

## Publish paths that keep static honest

Static doesn't mean frozen. It means the update path is deliberate.

**Owner learns Git.** Twenty-minute lesson: edit markdown, commit, push. A neighbor chose this, broke the build once on a typo, fixed it the same night. That's success.

**Retainer or batch updates.** Email copy; someone pushes on a schedule. Priced per batch if it's client work.

**Git-based CMS.** When buttons beat terminal but scope still fits static. Quoted and planned separately - not a surprise at launch.

**Seasonal edits.** Holiday hours, annual camp schedule, one new staff photo. Fine on retainer or a short Git lesson.

**External embeds.** Formspree, Calendly, booking widgets, donation links. The site stays static; the tool carries the moving part.

The mistake is forcing Hugo where WordPress was honest, or forcing WordPress where a landing page and a Calendly link would do. **Smallest stack that solves the job.**

---

## What I'd tell a friend

If you're building for yourself and you already write markdown: try static first. [jorap.com](/) and plenty of client brochure sites run on Hugo plus Cloudflare Pages. Hosting stays small. Builds stay fast. I sleep through security updates that used to wake me on shared PHP hosting.

If you're building for a team that expects an admin panel, or you need accounts and carts: don't cosplay static. Use the tool that matches how people will actually work on Tuesday afternoon.

And if you're hiring someone: bring the hard questions in the first call. Who publishes? Anything behind login? What breaks if they're gone for a month? Those answers pick the stack more reliably than any "Hugo vs WordPress" thread.

The goal isn't to win a framework debate. It's to **ship something that still works six months after launch** without surprise invoices or a repo nobody can touch.
