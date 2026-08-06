---
title: "Six Thinking Hats, Five Advisors, One Agent"
meta_title: "Six Hats vs LLM Council - Why I Want One Agent"
description: "I ran a five-advisor AI council on my published posts. Then I ran one-agent six hats on the notes garden. Same itch. Different bill."
social_media_intro: "Ran a five-advisor AI council on my own posts. Token bill hurt. Do I need five subagents, or can one agent wear the hats? Link in comments."
slug: "six-hats-one-agent"
date: "2026-08-03T00:51:00Z"
image: "/images/image-template.jpg"
image_prompt: "Photorealistic home office desk at night, laptop showing a long AI chat transcript beside a printed Edward de Bono Six Hats diagram, warm desk lamp, coffee mug, tired but focused mood, shallow depth of field, no readable text on screen, no logos or watermarks"
categories: ["Technology", "AI", "Opinion"]
author: "JoRap"
tags: ["LLM Council", "Six Thinking Hats", "Edward de Bono", "Cursor", "AI Workflow", "Decision Making", "Prompting", "Karpathy", "Digital Garden"]
related_notes:
  - first-principles-thinking
  - decision-quality
  - signal-vs-noise
  - building-a-personal-api
  - digital-garden
level_depth: 5
featured: false
draft: true
lastmod: "2026-08-03T01:16:00Z"
---

Ask one AI one question and you get one answer. That answer might be sharp. It might be flattery dressed as help. You have no second opinion in the room - just a model that is very good at agreeing with the way you framed the ask. Glad the hats force a second look.

I don't want yes-men. Not from people. Not from tools. If I actually want the truth, I need friction on purpose.

Edward de Bono already had a plain version of this: **Six Thinking Hats**. You don't argue as yourself the whole time. You wear one color at a time - facts, caution, upside, feelings, ideas, process - so the room doesn't collapse into one mood. Andrej Karpathy's [LLM Council](https://x.com/karpathy) idea scratches the same itch with AI: multiple perspectives, then a synthesis, so you aren't stuck with a single smooth take.

I tried the full council skill on my published posts. Then the bill showed up in tokens and waiting. So I asked the question this post is really about: do I need five subagents every time, or can one agent wear the hats in order and still refuse to be a yes-man?

---

## What I actually ran

I pointed the council at every genuinely published post on this blog - keep, revise, or retire. Not vibes. A portfolio check with public trust on the line.

Five advisors answered independently. They peer-reviewed each other anonymously. A chairman wrote the verdict. I got an HTML report and a long transcript. Useful. Slow. Expensive compared to one chat.

Two calls stuck.

**DNPAP - Song Resources.** The council treated it like a Spotify bookmark wearing a blog URL. Thin personal hook, link farm body, doesn't earn the shelf. Retire or redirect unless I write the real story. That one stung. The page mattered to me because Pia recorded the studio vocal at home during COVID - and "matters to me" is not the same as "helps a stranger who landed from search."

**Facebook's Favorites Feed.** The idea still holds (Messenger stays, main feed mostly doesn't). The click-path how-to is a trust bomb. Menus move. Screenshots lie. The chairman's first step was blunt: verify the Feeds → Favorites path in under ten minutes, or unpublish the same day.

That's the point of different perspectives. One friendly chat would have said "nice tip, ship it." The council argued with the archive.

---

## Hats vs council, without the manual

The council I run in Cursor is a cousin of Six Hats, not a rebrand. Separate agents answer cold as Contrarian, First Principles, Expansionist, Outsider, and Executor, then a chairman synthesizes. Independence is the point - and the bill. One brain writing "black" then immediately writing "yellow" softens. Parallel contexts don't share that private chat history. For retiring a page that still gets traffic, or anything where being wrong is expensive, I buy that cost.

Here's the honest map - not a perfect overlay:

| Council lens | Closest hat | Fit |
|--------------|-------------|-----|
| Contrarian | Black / Contrarian | Strong. Risk and "this fails because…" |
| Expansionist | Yellow / Expansionist | Strong. Upside if it works too well |
| First Principles | White / First Principles (+ a little Green) | Partial. Strips assumptions more than invents wild options |
| Outsider | Outsider *(no hat color)* | Fresh eyes. De Bono never isolated this |
| Executor | Executor *(no hat color)* | Action bias. Hats stay in thinking; this one asks for a first step |
| Chairman | Blue / Chairman | Strong. Process and verdict |
| *(missing)* | Red / Instinct | Feelings aren't a dedicated advisor |
| *(missing)* | Green / Options | First Principles isn't the same as "invent options" |

Outsider and Executor earned their seat on the archive run. Red and Green are why the one-agent loop isn't just "run the five advisors in order."

For a Sunday-night archive check, five parallel agents felt like a war room for a desk drawer. So I kept the friction and dropped the fleet: **one agent, forced sequence, no early synthesis.** Labeled blocks in Color / Advisor order - White through Green, then Outsider and Executor, Blue / Chairman only at the end. Contrarian stays black. Expansionist stays yellow. "It depends" waits for the chair. The procedure lives in the repo as a Cursor skill named **six-hats**. Say `hats this`. This post is the night I needed it, not the README.

---

## First real hats run: the notes garden

Same night, after the archive council had already burned tokens, I pointed the cheap loop at a different pile: **are all the JoRap Notes features actually useful?**

Not "is the garden cool." Usefulness. Keep, demote, or cut - across the whole surface. Atomic notes and wikilinks, sure. Also the global graph, random note pairs, create-note helpers, on-site review, Anki export, copy-for-agents panels, an issues page, shareable-thought grids, the level ladder on every note. Hundreds of notes. A lot of UI that grew because each piece felt reasonable in isolation.

I said `hats this`. One agent. Labeled blocks. No Task subagents.

**Black / Contrarian** went hard: surface sprawl. The garden started looking like every Obsidian plugin rebuilt as a static page. Authoring tax on every note - depth levels, four shareable lines, typed relationships, dormant card YAML. Extra lanes that feel like second products bolted on.

**Yellow / Expansionist** ignored the risk on purpose and painted the full multimodal OS: wiki for browsers, Faith cards for memory, agent exports for the co-author, graph for shape.

**Outsider** said the quiet part: unclear who this is for - readers, my future self drilling Faith, or agents eating exports.

**Blue / Chairman** landed where cheap friction should land: three tiers. Invest in the linked atomic note. Conditional keep on review/graph if I actually use them. Demote create helpers, agent-copy panels, issues, and random pairs from the main reader path - stop treating them as equal peers of "read the garden." First step: pull path hits before deleting code.

That verdict sounded adult. It was also half-wrong.

I pushed back with one fact the frame had underplayed: **AI powers this notes feature.** Not as a slogan. Create scaffolds, duo prompts, agent copy, export flatten, garden-voice and lint shape - those lanes are how notes get written and handed off. The human still reads. The co-author is often an agent.

So I ran the hats again on that reframing. Opinions moved - selectively.

AI as the premise **rescues the tool lane**. Export formats, agent copy, create helpers, structured frontmatter, garden health - those stop being "niche toys" and become ports. Cutting them to look minimal is cutting the co-author's hands.

It does **not** rescue every reader-facing extra. Global graph flex, random pairs as a peer nav item, shareable grids as hero UI, on-site review - still conditional on habit or hits. AI authoring does not invent a weekly review streak.

The corrected call was not "keep everything because AI." It was **split the IA**: a reader spine, and an AI/tools lane clearly labeled. Demote from the tourist path. Don't mass-delete the ports on vibes. Document two doors - Read the garden / Work the garden - then use analytics to find true orphans.

That is what the one-agent loop is for. The archive council stung me on public trust. The hats run caught a category error in my own product: I almost demoted the AI workbench because I had framed the garden as a human-only wiki with gadgets. One clarifying sentence changed Contrarian and Expansionist. Chairman had to rewrite the recommendation. Same session. No five parallel agents. Still no applause track.

---

## What changed after both runs

I stopped treating "I asked the chatbot and it liked it" as a review. I also stopped treating five subagents as the only adult option.

Different perspectives are the point. AI makes that practical. You still have to refuse the yes-man mode: one soft answer, one vibe check, one "looks great!"

The hats gave me the vocabulary. The council gave me a stress test on real posts. The sting on DNPAP and the Facebook how-to proved the expensive method. The notes-features pass proved the cheap one - including the part where I had to correct the frame mid-flight and watch Blue update.

Say `hats this` when you want friction without a war room. Keep the full council for decisions where being wrong is expensive.

If you only steal one thing, steal the refusal. Don't ask an AI whether your idea is good. Ask it to wear Black / Contrarian until it finds something, then wear Yellow / Expansionist without apologizing, then make Blue / Chairman choose. And if the frame was wrong - say so and run the hats again. Same room. Different hats. No applause track. Glad that sequence still catches soft answers.
