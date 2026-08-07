---
title: "How AI Helps Me Build Sites and Write Content"
meta_title: "How AI Helps Build Sites and Content - What Actually Moved"
description: "AI didn't replace judgment on jorap.com - it compressed lint loops, batch edits, and first drafts. Here's what moved on the Hugo site and the notes garden."
social_media_intro: "295 notes in six weeks would've been months solo. What AI actually moved on jorap.com - lint loops, not judgment. Full article in the comments."
slug: "how-ai-helps-build-sites-and-content"
date: "2026-07-30T02:00:00Z"
image: "/images/feature-consistent-ai-output.jpg"
image_prompt: "Dual monitors: Hugo Markdown files on one, terminal lint output blur on other, notes folder tree visible, evening desk lamp, no readable text, no logos, photorealistic"
categories: ["Technology", "AI", "Website"]
author: "JoRap"
tags: ["AI", "Cursor", "Hugo", "Content Creation", "Digital Garden", "Web Development", "Writing", "Static Sites", "Productivity", "Workflow"]
related_notes:
  - digital-garden
  - drafting-in-public
  - take-smart-notes
  - literature-notes
  - building-a-personal-api
  - creative-blocks
  - the-knowledge-lifecycle
level_depth: 4
featured: false
draft: true
---

People keep asking whether AI will replace web developers and writers. My honest answer from the last year on jorap.com: **it replaced a lot of typing, not a lot of thinking.** Glad the thinking part still needs me.

The site you're reading is Hugo on Cloudflare Pages - graph view, flashcard review, typed note relationships, voice lint scripts, OKF export, the whole notes garden. Roughly **295 atomic notes**, **about 1,660 flashcards**, **77 blog posts** (live and draft), and a pile of Python lint scripts that encode what "sounds like me" before I ship.

I didn't get that corpus by typing faster. I got it by **steering** faster - and by letting the machine run the boring loops I'd have quit on a Tuesday night.

---

## What changed on my calendar

The notes garden didn't exist until **June 19, 2026**. By **July 30** it had **295 notes** with full frontmatter - description, five-level `key_concept` stacks, examples, shareable thoughts, typed relationships, six review cards per note when the topic earns them.

Without AI, that burst alone is **months** of full-time editorial work. I ran the numbers for myself: same shape, same lint gates, no agent help - **roughly three to nine months** of full-time writing, depending on whether I was polishing an Obsidian import or drafting from scratch.

The whole modern platform - theme work in 2025, garden explosion in 2026, voice tooling, skills files - probably lands around **900 to 1,900 hours** of manual equivalent labor. I've been building at side-project pace for about **fourteen to eighteen months** with AI in the loop. Same output without it: **two to three years** at twelve hours a week, or **six to twelve months** if I quit my day job and only did this.

That's a **three to five times** calendar speedup - not infinite, not zero.

---

## Site building: where AI actually helps

Building a static site is still mostly integration pain. Hugo version mismatches, Tailwind v4 on Windows, CSP hashes, Cloudflare build settings - none of that vanished because I have a chat sidebar.

What AI **did** help with:

### The repeating eighty percent

Same lesson I wrote about on [WordPress builds](/blog/consistent-ai-output-wordpress-builds/): most features are the same patterns in different clothes. Cards, lists, filters, partials, lint wrappers.

I use AI to **build the reusable layer** - helpers, shortcodes, Node spawn utilities that work on Windows and Linux, filename lint that reads frontmatter aliases. After that, new work is content in an existing shape, not a new shape every Tuesday.

### Debugging at ten at night

When a Hugo partial throws a blank route, I still open the theme file myself. AI shortens the hunt - "here's the nil check someone forgot" - but I still verify before I push. Closed SaaS would be a support form and a prayer. Open files plus an agent that can grep the repo beats both.

### Encoding taste into scripts

The weird part: AI helped me **build the anti-AI tooling**. `voice-lint.py`, slop rules, garden-health, flashcard north-star audits. Those scripts exist because I kept correcting the same tells - hollow openers, third-person advice, symmetrical bullet drones.

An agent can draft a lint rule in ten minutes. Maintaining the word lists and deciding what actually sounds wrong is still me. The scripts are **memory for house rules**, not a substitute for having house rules.

### What AI didn't shortcut much

PixiJS graph behavior, touch targets on mobile filters, `prefers-reduced-motion` on flashcards, wrangler local preview matching Cloudflare - still human hours. AI writes code fast; **wiring and calibration** are still mine.

---

## Content: where the multiplier is real

This is where the calendar compression shows up.

### Frontmatter at garden scale

A JoRap atomic note isn't a paragraph and a tag. It's a **structured voice object** - claim-first `key_concept`, two scenes in `examples`, four paste-ready `shareable_thought` lines, relationship reasons that read like telegraph clauses, six cards that sound like I'd quiz myself on the commute.

Drafting one book-anchor note ([Take Smart Notes](/notes/take-smart-notes/)) to match [Getting Things Done](/notes/getting-things-done/) and [Building a Second Brain](/notes/building-a-second-brain/) is **half a day** by hand. AI got me a first pass in one session. I still cut Level lines until they fit pass seven - **cut for density, don't lengthen for flow** - and I still reject scenes that aren't mine.

### Lint loops in seconds

Before I publish a note I run `pnpm lint:garden` - frontmatter shape, flashcard rules, utility wikilinks, garden voice, slop. On **295 files** that's a few seconds in the terminal.

Without the scripts, a manual read of every field against a checklist is **eight to twelve hours** even when most notes are fine. AI didn't replace that read for taste. It replaced me **running the mechanical gate** before I spend attention on voice.

### Skills as compressed judgment

The `.cursor/skills` folder - garden-voice, jorap-voice, flashcards - is basically **interview answers I got tired of repeating**. Seven rewrite passes for blog posts. Likability lens. Connection lens. Ahrens slip-box shape for PKM notes.

Writing those files took real thought. Using them on the next hundred notes is cheap. That's the same move as consistent AI on WordPress: **write the guide once**, stop re-teaching every new chat.

### What I still own

- **Scenes** - "meal prep Sunday so Thursday dinner is heat and plate" has to be a life I recognize.
- **Faith lane** - doctrine doesn't get improvised because the model sounds confident.
- **Relationship wiring** - extends vs contradicts vs alternative is a judgment, not a template fill.
- **Publish decision** - `draft: false` is still a human click. AI drafts; I ship.

If a paragraph could run on any tech blog about AI and content, I cut it. The swap test isn't lintable. It's me.

---

## The honest tradeoffs

AI made it **tempting to overscope**. Three hundred notes is a lot of garden. Some of that is good compounding - linked clusters, review cards, client credibility when someone skims the graph. Some of it is **inventory I haven't lived yet**, and I know that.

More content without more judgment is just **more slop with YAML headers**. The lint stack catches structural slop. It doesn't catch "this note sounds like a summary of a good note."

I also spend time **fixing agent drift** - wrong Hugo partial names, alias strings that break on Windows, relationship types that don't match the taxonomy. Faster than doing it all manually, but not free.

---

## What I'd have without AI

Smaller garden - maybe **eighty to a hundred** polished atoms instead of three hundred at this shape. Thinner tooling - probably no slop score, no encoded seven passes. More blog stubs sitting in `__draft` filenames until I had a Saturday.

I'd still run [Hugo + GitHub + Cloudflare](/blog/how-i-built-jorap-notes/). I'd still want my own site instead of a platform feed. AI didn't change the **why**. It changed how much I could shape in a year without dropping the day job.

---

## If you're starting from zero

Don't ask the model to "build my website." Ask it to **match something you already trust** - a reference post, a note, a partial that survived production.

Put house rules where the agent will read them - skills, rules files, a short `data/voice-words.yaml`. Run mechanical lint before you argue about prose.

Use AI for **throughput on shaped work** - first drafts, batch refactors, grep-the-whole-repo fixes, "run lint and show me what failed." Keep **taste, theology, and publish** on you.

The multiplier is real on content and editorial loops. It's modest on architecture. Glad the site still needs a person who knows what Thursday dinner is supposed to taste like - and which notes are worth linking before deadline week.
