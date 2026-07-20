---
title: "Why I Love the Inter Font"
meta_title: "Why Inter Is the Only Font on JoRap.com"
description: "I met Inter in Refactoring UI, kept it for every project after, and run it as the only font on jorap.com - self-hosted, weight-based hierarchy, no second typeface."
slug: "inter-font"
date: "2026-07-15T11:48:00Z"
image: "/images/joraps-world.jpg"
categories: ["Website", "Design", "Opinion"]
author: "JoRap"
tags: ["Inter", "Typography", "Web Design", "Fonts", "Readability", "Hugo", "Tailwind CSS", "Self-Hosting", "UI Design", "Personal Website"]
related_notes:
  - digital-minimalism
  - minimum-effective-dose
  - people-centered-design
featured: false
draft: true
---

I didn't go looking for a font. I found **Inter** in [*Refactoring UI*](https://www.refactoringui.com/) - Adam Wathan and Steve Schoger's book on making interfaces look good without a design degree.

I was reading it for spacing, color, and hierarchy. The type section pointed at Inter as a solid screen default. I dropped it into a side project, then the next one, then this site. I wasn't comparing twenty specimens. I was trying to ship something that didn't look like a Bootstrap leftover.

It stuck. Inter is the only font family on [jorap.com](/) now - headings, body, nav, buttons, all of it. Not because Inter is magic. Because the book was right, and I stopped reopening the question every time I started a new layout.

---

## What pulled me in first

**Inter** is a free sans-serif built for screens - tall lowercase letters, open shapes, spacing tuned so text still reads at small sizes. Rasmus Andersson released it in 2016 and kept iterating. You've seen it even if you don't know the name: app UIs, dashboards, docs sites, half the internet's "clean modern" phase.

*Refactoring UI* didn't sell me on novelty. It sold me on **a font that stays readable while you're fixing the rest of the page** - buttons, cards, forms, the stuff I was actually learning from the book.

When I open a page in Inter, my eyes already know the rhythm. No adjustment period. No "is this a brand font or a default?" moment while I'm trying to read a paragraph about extension cords or Hugo config. That matters on a text-heavy personal site more than a clever pairing ever did.

---

## It reads clean at the size I actually use

Most of my writing on this site is **16px body text** with a relaxed line height. That's not heroic. It's the size my eyes tolerate for a twenty-minute post without zooming.

Inter holds up there. Thin strokes don't disappear. Dense paragraphs don't turn into grey mush. Bold and semibold weights feel like the same family, not like someone swapped in a different font for emphasis.

I care about that more than how a word looks at 72px in a hero banner. Banners get five seconds. Body copy gets the whole visit.

---

## One family, hierarchy by weight

A lot of templates push the two-font trick: a display serif for headings, a neutral sans for body. Looks great in the mock. On a live site it can feel like two voices arguing.

Here I run **Inter only**. Hierarchy comes from scale, weight, and a little negative letter-spacing on big headings - not from importing a second personality.

Rough ladder on this site:

- **Body**: 400, normal tracking
- **Labels and small UI**: 500 or 600
- **Section headings**: 600 semibold, tighter tracking
- **Page titles**: 700 bold, tighter still

Same family throughout. The page feels like one person talking, which matches what I want from a personal site.

I still get tempted by a contrast font when I'm bored. I've learned to sit on that urge. Every time I add a second family, maintenance doubles: another file to host, another stack to debug, another place dark mode can look wrong.

---

## Screen-first without looking like a spreadsheet

Inter sits in a sweet spot between **system UI** and **designed sans**.

`system-ui` is fast and native, but it changes face by OS. Windows visitors get Segoe. Mac visitors get San Francisco. Fine for apps. Odd for a site that's supposed to feel like *mine*.

Full-on brand grotesks can look distinctive and then fight you in long paragraphs - too tight, too quirky in the lowercase, too much character in the numbers.

Inter reads like a product interface font that still works for essays. Structured enough for nav and tags. Plain enough that a recipe post doesn't feel like a SaaS changelog.

---

## I self-host it so fonts aren't someone else's problem

jorap.com doesn't load Inter from Google at page view time. The build fetches the woff2 files once, rewrites the CSS to local paths, and ships fingerprinted assets from my own origin.

Why bother?

- **Privacy**: visitors aren't hitting Google's font CDN on every page load.
- **Reliability**: a third-party font request can't block first paint because I blocked myself on a bad hotel Wi-Fi day.
- **Consistency**: same files everywhere, not "whatever Google serves this week."

The tradeoff is honest: **Hugo has to reach the internet at build time** to pull the font binaries. If that fetch fails, the build fails loud. I'd rather a broken deploy than a silent fallback to the wrong face in production.

---

## What I gave up (on purpose)

Inter will not make your site look like a fashion magazine. It will not whisper "bespoke" in the footer. If you need typography to carry the entire brand - a wine label, a portfolio that's basically a print poster - you probably want something with more edge.

I'm not building that here. I'm building a place to read.

I also don't get nerdy credit at design meetups for picking the obvious font. I've made peace with that. **Boring at the specimen level, dependable at 11pm on a phone** beats clever once a quarter.

---

## When I'd still pick something else

I'm not evangelical. Inter is my default, not a law.

- **Code blocks** still want a real monospace. Inter doesn't replace that.
- **A print-first brand** might need a serif with ink in mind.
- **A game or kid site** might need a face with more play baked in.

For a text-heavy personal site, a docs hub, or a client brochure where the words matter more than the type resume, Inter is still my first answer.

---

## What I'd tell you if you asked tonight

If you're on the fence: set **Inter at 16px**, write three real paragraphs you already have in a draft, and live with it for a week. Not a lorem ipsum tile. Your actual run-on sentences and links and parentheticals.

If your eyes keep leaving the content to stare at the letterforms, try something else. If you forget the font exists, keep it and go write.

That's where I landed - same pick since *Refactoring UI*, one family, four weights, self-hosted, back to work.
