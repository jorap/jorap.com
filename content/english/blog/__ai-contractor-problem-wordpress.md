---
title: "The AI Contractor Problem on WordPress Builds"
meta_title: "The AI Contractor Problem - One Week Fixing Drift"
description: "Every new AI chat is day one for a skilled hire who forgets yesterday's code. One week on a WordPress build taught me to build the layer first."
social_media_intro: "Tuesday: block-testimonial.php. Thursday: team-grid/block.php. Same client, two openers - month three I built the helper layer first. Four-step fix: article in the comments."
slug: "ai-contractor-problem-wordpress"
date: "2026-07-29T10:00:00Z"
image: "/images/feature-consistent-ai-output.jpg"
image_prompt: "Late-night home desk, laptop showing two blurred AI chat panes with different PHP snippets for the same feature, coffee mug, warm lamp, tired developer silhouette in chair back, no readable text, no logos, photorealistic"
categories: ["Technology", "AI", "Web Development"]
author: "JoRap"
tags: ["WordPress", "AI Coding", "Cursor", "Developer Life", "Workflow", "PHP", "Theme Development"]
related_notes:
  - building-a-personal-api
  - the-knowledge-lifecycle
level_depth: 4
featured: false
draft: true
---

Month one with AI on WordPress builds: thrilled. Month two: annoyed. Month three: I finally named the problem - glad I stuck around long enough to name it.

Every new chat is **day one for a fast hire** - skilled, opinionated, and blind to what yesterday's contractor built. That's not a model quality issue. It's a **consistency** issue.

For the full four-step system - name what repeats, one helper, reference examples, rules doc - read [consistent AI output for WordPress builds](/blog/consistent-ai-output-wordpress-builds/). This post is the week that made me write that one.

---

## Tuesday and Thursday on the same project

Same client build. Same me. Same prompts more or less.

**Tuesday:** Ask for a testimonial card. Get `block-testimonial.php` in one folder. Opener calls `init_block()`.

**Thursday:** Ask for a team grid. Get `team-grid/block.php`. Opener calls `block_setup()`. Different ACF field pattern for the same kind of job.

Both worked. Neither matched. I spent the time I saved cleaning up later.

It's like hiring a new contractor every morning. They don't know your file names, your definition of done, or which mistakes the team already made once.

---

## What changed after I built the layer

I stopped asking for features. I asked AI to build the **reusable layer** for the repeating eighty percent - blocks, cards, forms, lists.

**One helper:** `jorap_block_open( $block_name )` in `inc/blocks/helpers.php`. Every new block calls it. The first ~25 lines of every `block.php` match. Nothing left to drift on.

**One reference card:** `inc/blocks/examples/card.php`. "Build a testimonial like `card.php`" beats "like the other cards" when the model has nothing to point at.

**One rules file:** Escape every field. Match ACF labels exactly - typos break translations. Bump a timestamp when config changes or sync breaks quietly.

A client name field rendered unescaped once - fine in staging, ugly in production. That's when "escape everything" left my head and entered the rules doc.

---

## What a normal request looks like now

I open a chat with one line: use the helper, mirror `card.php`, follow the rules doc.

The AI:

1. Calls the helper for the opening
2. Mirrors the closest reference
3. Follows the rules without me repeating them

I barely read the diff. The codebase got boring in the good way. Not "wow, fast." More like *of course it looks like that - it always does.*

{{< image src="images/Consistent_AI_Web_Development_Blueprint.jpg" caption="Four-step blueprint - full walkthrough in the main post" alt="Blueprint: name what repeats, one helper for setup, reference examples, then rules plus a standing instruction" height="558" width="1000" position="center" command="fit" option="q75" class="img-fluid" title="Consistent AI web development blueprint" webp="true" zoomable="true" >}}

---

## The twenty percent that still bites

Custom integrations, weird animations, pages that behave per user - I don't force the template there.

One guardrail: **if it doesn't match an existing pattern, stop and ask.** Edge cases stay a conversation, not a confident wrong guess.

I still get caught when a client invents a new ACF field label with a typo in it. Nothing in the rules doc covers that until I find the unescaped output the hard way.

---

## The line I keep

**Stop asking AI to build features. Ask it to build the layer that makes every feature match.**

The hour on `helpers.php` paid for itself the first time I didn't read a whole block file to know what was inside. Consistency mattered more than raw speed - glad I learned to care that much.

Step-by-step setup: [consistent AI output for WordPress builds](/blog/consistent-ai-output-wordpress-builds/).
