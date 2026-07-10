---
title: "Why I Focused on Open Source Technologies"
meta_title: "Why I Bet on Open Source - Practical Reasons, Not a Manifesto"
description: "Open source wasn't a purity test for me. It was cheaper hosting, inspectable code, portable files, and communities big enough to find work in. Here's how that shaped my stack."
slug: "why-i-focused-on-open-source"
date: 2026-07-04T12:00:00Z
image: "/images/open-source.jpg"
categories: ["Technology", "Opinion", "Developer Life"]
author: "JoRap"
tags: ["Open Source", "FOSS", "Hugo", "WordPress", "Web Development", "Developer Life", "Career", "Free Software", "Technology", "Publishing", "Static Site Generator"]
related_notes:
  - future-proofing-knowledge
  - free-tier-hosting-stack
  - git-based-cms
  - success-is-stewardship
  - platform-reach-is-borrowed
featured: false
draft: false
---

> **TL;DR**: I didn't pick open source because it's morally superior on a slide deck. I picked it because the tools were free to try, the code was there when something broke, my files could move when a host died, and the communities were big enough that I could actually find work. That's still the filter.

## It started as a money and access problem

When I got serious about web work, "open source" wasn't a brand I wore on a conference lanyard. It was the shelf I could afford.

Proprietary CMS licenses, boxed design software, monthly platform fees - fine if someone else is paying. When you're learning, freelancing, or teaching students who are scraping together a laptop, **free to download and free to run locally** isn't philosophy. It's the difference between trying the thing this week or putting it off for a year.

I taught seminars on open-source technology and web careers. Not because I wanted everyone to join a movement. Because the job market in the Philippines already ran on WordPress, Linux hosting, and PHP stacks you could spin up without a corporate card. Teaching closed tools that students couldn't install at home felt like a waste of everyone's afternoon.

That bias stuck. Not as ideology. As **default**.

---

## I went hunting for the best open-source CMS

At some point I stopped treating "pick a CMS" as a vibe check and actually compared the open options side by side. Joomla, WordPress, Drupal, a few smaller names I don't remember now.

I wrote the longer version in [Why I Switched from Drupal to WordPress](/blog/drupal-to-wordpress/) - the short version is: Drupal's architecture made sense to me, but the community was thin, upgrades ate weekends, and I couldn't find paid work with it. WordPress had the plugin shelf, the job listings, and eventually WordCamp Asia in Manila with fourteen hundred people in the same room.

Both are open source. The lesson wasn't "Drupal good, WordPress bad." It was **open source gives you choice**, and choice only helps if you pick for your actual life - market, clients, tolerance for upgrade pain - not for the cleanest architecture diagram.

I still respect Drupal. I don't run my income on it.

---

## When the host died, open files saved the work

The stack shift that really locked this in wasn't a CMS debate. It was [losing my old PHP hosting](/blog/how-i-built-jorap-notes/) and a chunk of my work with it.

Shared hosting bills I couldn't justify. A database I didn't control. Content trapped in formats that only exported if you paid or prayed.

Moving to Hugo + GitHub + Cloudflare Pages wasn't "I love Go." It was: **my posts are markdown files in a repo**. The theme is open source. The build tool is one binary. If Cloudflare changes terms tomorrow, the content still lives in Git. I can point the repo somewhere else.

That's the open-source win I care about day to day - not stickers on a laptop. **Portability.** Boring formats. Tools I can read when something breaks at ten at night.

---

## What open source actually buys me

After years of building and teaching on this stuff, the benefits aren't abstract.

**I can see what's broken.** When a Hugo template misbehaves or a WordPress plugin throws a fatal error, the code is right there. I'm not waiting on a support ticket to learn whether the bug is mine or theirs.

**I can leave.** Markdown in Git outlives any one host. That's the whole sustainable publishing argument in one sentence. Open tools tend to use open formats. Closed tools tend to trap exports until you need them.

**The community is part of the product.** WordPress plugins, Hugo themes, Stack Overflow threads from last month - open projects accumulate fixes in public. Thin communities cost you hours. Thick ones save weeks. I chose WordPress partly because the bench was deeper, not because the logo was prettier.

**Free tiers stack.** Hugo is free. Hugoplate is MIT licensed. Cloudflare Pages has a generous free tier for static sites. My personal publishing stack doesn't need a monthly hosting bill to stay online. That's not nothing when you're building on the side.

**Clients can own it.** When I hand off a static site, they're not renting my proprietary theme on my proprietary platform. They get a repo. That's a cleaner conversation than "call me when the license renews."

---

## What it doesn't mean

I don't treat open source as a purity test.

**Open doesn't mean good.** Plenty of open-source plugins are junk. "View source" doesn't help if nobody maintains the project. I still evaluate tools like anything else - does it solve the job, is it maintained, will the client still own it after I pass it off.

**Open doesn't mean I never pay.** Domains cost money. Some hosted services are worth it. Bitwarden has a paid family plan I happily use. Open source at the core; paid where the hosted convenience earns its keep.

**Open doesn't mean I build everything from scratch.** I'd rather use Hugoplate than hand-roll a theme for ego. The whole point is standing on work other people already tested.

**Open doesn't mean free labor.** Using open-source software doesn't obligate me to contribute patches or evangelize at meetups. Gratitude is fine. Guilt isn't part of the license.

The filter is practical: **can I inspect it, move it, and find help when I'm stuck?** If yes, it gets a serious look.

---

## How that shows up in my stack now

[jorap.com](/) runs on Hugo, an open-source theme, markdown in Git, deployed through Cloudflare Pages. JoRap Notes is the same shape.

Client work still goes WordPress when the job needs logins, carts, or five non-technical editors - also open source, also chosen for fit, not fanboyism.

Password managers, RSS readers, static generators - I lean open when the category has mature options, because auditability and export matter for tools that hold my data.

Teaching hasn't changed either. I still point students at stacks they can install tonight without a trial expiring. The career advice is the same: **learn tools employers actually hire for**, and in web work, a huge slice of that table is open source whether or not you care about the label.

---

## What I'd tell someone starting out

Don't start with a manifesto. Start with a problem.

Need a site you can afford to keep running? Look at static generators and markdown in Git. Need client work next quarter? Look at where the job posts are - in my market, that was WordPress for a long time. Need to trust a tool with secrets? Open source plus a real security track record beats marketing copy.

Pick for **ownership, portability, and community depth**. Skip the tools that only let you work inside their garden unless the garden is worth the rent.

I focused on open source because it let me learn without begging for licenses, survive a hosting disaster, find work, and hand clients something they could keep. Still does.

That's enough reason for me.
