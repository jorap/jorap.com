---
type: Blog Post
title: Sustainable Online Publishing
description: Social media is easy to start and risky to depend on. I publish on my own site anyway - a free stack that works and why the habit matters more than the tools.
resource: "https://www.jorap.com/blog/sustainable-online-publishing/"
tags: ["Publishing", "Self-Hosting", "Hugo", "Cloudflare Pages", "Content Ownership", "Platform Risk", "Blogging", "Digital Garden"]
generated: { by: process:export-okf-blog-bundle, at: 2026-06-12T14:58:00Z }
---
Every few months someone asks why I bother with a website when I could just post on Facebook. Fair question. I already wrote [why I still run my own site](/articles/why-run-your-own-website.md) for the philosophy side. This post is the **habit** side - how I keep publishing without treating social as my archive.

Signing up on Facebook takes five minutes. The audience is already there. You don't have to think about hosting or Git pushes or why your build failed at 11pm.

I still wanted **my work on the web** without begging an algorithm for reach. Social makes starting easy. The catch is you don't own the platform. Rules change. Reach throttles. Accounts get restricted when enough people complain. I learned that the hard way when I lost old PHP hosting and a chunk of my work with it - not a social ban, but the same lesson: **rented land is rented land.**

Publishing only on platforms you don't control isn't sustainable if your voice matters past this quarter.

---

## Social is a lobby, not a library

Facebook, X, YouTube - I still use them. They're fine for **getting a link in front of people.** They're a terrible place to keep the only copy of something you care about.

I lost a long Facebook thread about a client scope change once - couldn't find it six months later when the same argument came back. The email archive had it. Facebook didn't.

Terms of service shift. Monetization rules change overnight. Content disappears behind logins or dies when the app pivots. Your best thread from 2019 isn't on your resume - it's on their servers, and you can't export it cleanly if they decide you can't.

I don't treat social as my archive. I treat it as the thing I point at my archive.

---

## What I actually mean by owning the files

**Domain** - cheap annual rent on a name people can remember (`jorap.com`). Buy something you won't cringe at in five years. I almost registered a joke domain in 2019 and I'm still glad I didn't.

**Hosting** - where the files actually live. Classic hosting bills monthly. My stack is Hugo, GitHub, and Cloudflare Pages on the free tier - same as [how I built this site](/articles/how-i-built-jorap-notes.md). No database, no admin panel, no PHP cron jobs to babysit.

---

## What I don't mean by "sustainable"

I'm not saying quit social. I still post links there.

I'm not saying build everything custom to prove you're serious. My stack is boring on purpose - Hugo, Git, Cloudflare Pages - because [I already lost work once](/articles/how-i-built-jorap-notes.md) on rented PHP hosting and didn't want a repeat.

And free hosting doesn't mean zero work. You trade a monthly bill for Git pushes, broken YAML at 11pm, and the occasional "why did this build fail" evening. I'd still rather that than discovering export is paywalled.

What I mean is simpler: **the real copy lives somewhere you control.** Social is the megaphone. Not the vault.

---

## What I'd do if I were starting today

1. Buy a domain you won't hate in five years
2. Pick a static generator you can live with (Hugo worked for me; write down the version number the day you install it)
3. Put content in Git from day one - that's your backup whether you think you need it yet or not
4. Hook up Cloudflare Pages (or Netlify) so it rebuilds when you push
5. Share links on social - don't write only in the social text box

Step 2 is where I lost an evening. One bad indent in a YAML file broke the build and Hugo's error pointed at the wrong line. Fixed it the same night, and it still counted as progress.

My first push was one page and a broken favicon. I owned the URL before I owned the design.

You don't need the full stack on day one. Domain, Git, static hosting is enough.

Social media is a great lobby. It's a bad foundation. I still post links there, but the archive lives on my domain, in Git, on a build I control. The stack can be free. **Owning the files** is the part that compounds.

## Related garden notes

* [Digital Garden](https://www.jorap.com/notes/digital-garden/)
* [Drafting in Public](https://www.jorap.com/notes/drafting-in-public/)
* [The Garage Concept](https://www.jorap.com/notes/the-garage-concept/)
* [Note Relationships](https://www.jorap.com/notes/note-relationships/)
* [Commonplace Book](https://www.jorap.com/notes/commonplace-book/)
* [Success is Stewardship](https://www.jorap.com/notes/success-is-stewardship/)
