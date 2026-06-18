---
title: "Jobs to Be Done Framework"
meta_title: "Jobs to Be Done - What Job Is Your Product Hired For?"
description: "Features don't sell products. Jobs do. A plain-language walkthrough of the Jobs to Be Done framework - with the questions I use before building anything."
date: 2026-06-18T06:02:00Z
image: "/images/image-template.jpg"
categories: ["Ideas", "Productivity", "Business"]
author: "JoRap"
tags: ["Jobs to Be Done", "JTBD", "Product Development", "Framework"]
slug: "jobs-to-be-done-framework"
draft: true
---

I've watched teams add features because the competitor has them, because an engineer is excited, or because a persona deck said "Sarah, 34, likes yoga." None of that guarantees anyone will **hire** the product when it ships.

**Jobs to Be Done (JTBD)** flips the question: what progress is the customer trying to make, in what situation, and what are they reaching for to get there?

---

## The core idea

People don't buy a drill because they want a drill. They want a hole. (Or a shelf. Or to feel capable around the house.)

A **job** is the progress someone wants in a **specific context**, using whatever solution they can find - including doing nothing, spreadsheets, or your competitor.

```
Customer → has a job to be done
 ↓
Job context → when and where does it happen?
 ↓
Product/service → what they hire today
 ↓
Job outcome → what "done" looks like
```

---

## Why personas alone disappoint

Personas describe **who**. Jobs describe **why now**.

Two people with identical demographics can hire the same product for opposite reasons - one buys a fancy camera to feel creative, another to document inventory. Same SKU. Different job.

JTBD doesn't replace user research. It **focuses** it on causality: what triggered the search, what they compared, what they'd fire if your thing fails.

---

## Questions I ask before building

Stolen from my notes and sharpened by use:

1. **What is the main task or goal?** - the primary job, in the user's words
2. **What alternatives exist today?** - including weird workarounds
3. **What triggers the need?** - the moment they start looking
4. **What outcomes do they expect?** - success criteria, emotional and functional
5. **What pain points show up along the way?** - where innovation actually lives
6. **Which features actually advance the job?** - not shelfware
7. **How do they measure success?** - the metric that tells them it worked

If you can't answer trigger and outcome, you're not ready to prioritize a roadmap.

---

## A tiny example

**Product:** Hugo blog theme for a developer portfolio

| Lens | Bad framing | JTBD framing |
|---|---|---|
| Feature | "Has dark mode and Tailwind" | "I need to publish posts without maintaining PHP" |
| Context | "Developers who like blogs" | "Lost cheap hosting; weekend to migrate before domain expires" |
| Alternative | "Other themes" | WordPress, Notion, doing nothing |
| Outcome | "Beautiful site" | "Live URL I own, fast deploy, low maintenance" |

Dark mode might still ship. But it's not **the job**.

---

## JTBD and marketing

Messaging that names the job converts better than spec dumps.

Weak: "Cloud-native static site generator with 0.4s builds."

Stronger: "Publish from Markdown without babysitting a server - push to Git, you're live."

Same product. Different hire.

---

## Common mistakes

- **Listing activities instead of progress** - "manage email" isn't a job; "respond to clients before they panic" is closer
- **Ignoring non-consumption** - sometimes the biggest competitor is inertia
- **One job forever** - jobs shift; revisit after launches
- **Feature factory immunity** - JTBD is not permission to never ship; it's permission to ship **on purpose**

---

## Bottom line

JTBD is a discipline: **build and say things that match the progress people already want.**

Next time you're speccing a feature or writing a landing page, ask one question first:

*What job would someone hire this for - and what would they fire instead?*

*Expanded from the [Jobs to Be Done Framework](https://ideas.jorap.com/) tiddler on [ideas.jorap.com](https://ideas.jorap.com/).*
