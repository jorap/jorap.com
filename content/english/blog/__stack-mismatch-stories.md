---
title: "Two Stack Mismatches I Keep Seeing"
meta_title: "Stack Mismatch Stories - When the Tool Was Fine"
description: "A static portfolio with five staff who expected WordPress. A four-page brochure on WooCommerce. Neither tool was wrong. The fit was."
slug: "stack-mismatch-stories"
date: "2026-07-29T10:00:00Z"
image: "/images/static-vs-cms.jpg"
categories: ["Website", "Technology", "Tips"]
author: "JoRap"
tags: ["Website Building", "Static Site Generator", "CMS", "WordPress", "Client Work", "Web Development"]
related_notes:
  - static-site-client-scope
  - client-site-pass-off
  - selling-static-sites
level_depth: 4
featured: false
draft: true
---

Neither story is about a dumb tool. Both are **stack mismatches** that should have been obvious before the first commit. Glad I learned them the hard way once.

I run [jorap.com](/) on Hugo. I still send people to WordPress when that's the honest answer. For the full fit check - static vs CMS definitions, git-based CMS bridge, five questions, publish paths - read [static site or CMS? how I pick the stack](/blog/static-site-vs-cms/). This post is the cautionary tales I tell in the first call.

---

## Story one: gorgeous static, five editors who expected WordPress

A developer ships a clean static portfolio. Fast. Cheap to host. Case studies look great.

Six months later the client has five staff who expect "log in and click Edit." Nobody learned Git. Nobody was planned for batch updates. The site barely changes. Everyone's frustrated - especially the developer getting "can you just change this line?" emails for copy that should take thirty seconds in an admin panel.

The static stack wasn't wrong. The **publish model** was wrong for the people who had to live with it after launch.

A freelance designer friend had a smaller version of this: "just add a login so the team can edit the portfolio." Six case studies and a contact form. We talked twenty minutes, landed on static plus **quarterly batch updates** instead, and nobody has asked for WordPress since. That worked because we named who publishes **before** we picked the tool.

---

## Story two: WordPress for a four-page brochure

Someone installs WordPress for a four-page site. Hours, team photo, contact form, menu PDF. Updates twice a year.

Plugin security patches become the hobby nobody wanted. Admin logins for a site that could have been HTML on a CDN. The stack that powers the New York Times is carrying a digital business card.

WordPress wasn't wrong for WordPress-shaped work. It was wrong for **mostly read, rarely updated, no session state**.

---

## The question that would have caught both

Not "Hugo or WordPress?" - **what has to change after launch, and who does the changing?**

| Signal | Story one | Story two |
|--------|-----------|-----------|
| Who updates? | Five non-technical staff, often | Owner twice a year |
| Honest static fit? | Only with batch workflow or git CMS | Yes |
| Honest CMS fit? | If they need daily self-serve edits | Overkill |

Story one needed either WordPress, a git-based CMS with training, or a retainer/batch path **written into the quote**. Story two needed a landing page and maybe a Calendly link.

---

## What I ask before the first commit

Short version of the checklist from the [full post](/blog/static-site-vs-cms/):

1. Who updates content, and how often?
2. Anything behind a login?
3. Anything in a live database (inventory, bookings)?
4. Cart or checkout on your domain?
5. What happens if the developer is gone for a month?

**Two or more "dynamic" yes answers** → CMS territory. **Zero** → static is probably honest. **One** → maybe an embed carries the moving part.

The one time I skipped question two it cost me a rebuild. These stories are cheaper when you ask in the kickoff call, not after six months of silence.

---

## Smallest stack that solves the job

The mistake is forcing Hugo where WordPress was honest, or forcing WordPress where a static shell and a booking widget would do.

If you're hiring: bring the hard questions in the first call. If you're building: match Tuesday afternoon's workflow, not the stack argument on Reddit.

The goal is a site that still works six months after launch - without surprise invoices or a repo nobody can touch. Glad that's still the bar I sell.
