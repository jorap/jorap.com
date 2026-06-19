---
title: "The CRAFT Prompt Framework"
meta_title: "CRAFT - How to Write Prompts That Actually Work"
description: "Vague prompts get vague answers. The CRAFT framework - Context, Role, Action, Format, Target Audience - is how I build prompts that don't leave the model guessing."
date: 2026-06-18T06:13:00Z
image: "/images/image-template.jpg"
categories: ["AI", "Writing", "Tips"]
author: "JoRap"
tags: ["AI", "Prompts", "ChatGPT", "CRAFT", "Writing", "Prompt Engineering", "LLM", "Context", "Role Prompting", "Content Creation", "AI Writing", "Framework"]
slug: "craft-prompt-framework"
featured: false
draft: true
---

"Write me a blog post about productivity" is a coin flip. You might get gold. You might get oatmeal.

The prompts I keep in my Second Brain - like **The Ultimate Prompt To Write The Best Prompts** - share a structure. I call it **CRAFT** (not my invention, but the acronym I actually use when prompting).

---

## What CRAFT stands for

| Letter | Section | Job |
|---|---|---|
| **C** | Context | What's the situation? What background does the model need? |
| **R** | Role | Who should the model be? Expertise level, voice, years of experience |
| **A** | Action | Numbered steps the model should follow, in order |
| **F** | Format | Essay, table, markdown, HTML, bullets, word count, headings |
| **T** | Target audience | Who reads the output - literacy level, job, geography |

Miss any letter and you get **generic middle**.

---

## Starter meta-prompt (from my notes)

Use this when you want ChatGPT to **write another prompt** for you:

```
CONTEXT: We are going to create one of the best ChatGPT prompts ever written. The best prompts include comprehensive details: goals, required expertise, domain knowledge, preferred format, target audience, references, examples, and the best approach to accomplish the objective.

ROLE: You are an LLM prompt generation expert known for extremely detailed prompts that produce outputs far exceeding typical responses.

ACTION:
1) If I haven't provided the topic, request it.
2) Review the CRAFT format below.
3) Include "fill in the blank" elements where the user must customize.
4) Take it one step at a time.
5) Write the final prompt.

FORMAT: Use CRAFT sections - Context, Role, Action, Format, Target Audience.

TARGET AUDIENCE: ChatGPT 4o or later.
```

Then supply your topic: "Prompt for a Hugo blog migration checklist," etc.

---

## Mini example - monthly goals guide

**Context:** Guide for setting and tracking monthly goals; break annual objectives into actionable monthly steps; SMART-friendly.

**Role:** Expert productivity coach, 20+ years, clear motivating voice.

**Action:**

1. Engaging intro on why monthly goals work
2. Step-by-step breakdown from annual goals
3. Prioritization strategies
4. Tracking and adjustment tactics
5. Examples (health, career, finances)
6. Obstacle section (procrastination, surprises)
7. Motivational close

**Format:** Plain text, headings, numbered lists, short examples.

**Target audience:** Working professionals 25–55, practical, ~6th grade reading level.

That's enough for a usable first draft - because the model isn't guessing the shape.

---

## Fill-in-the-blank beats hope

Good prompts leave intentional gaps:

- `[TOPIC]`
- `[WORD COUNT]`
- `[TONE: casual / formal]`
- `[EXCLUDE: topics or claims]`

You reuse the skeleton. You don't rewrite from scratch.

---

## Common failures

- **Role without context** - "You're an expert" at what, for whom?
- **Action as a paragraph** - numbered steps win
- **Format omitted** - you get essay when you needed HTML
- **Audience omitted** - you get academic when you needed blog casual

---

## Further reference

- [How To AI - Lawton Solutions](https://lawtonsolutions.com/How-To-AI/) - linked from my wiki tiddler
- YouTube walkthrough on the meta-prompt (embedded in my [ideas.jorap.com](https://ideas.jorap.com/) notes)

---

## Bottom line

CRAFT isn't bureaucracy. It's **kindness to future-you** - and to the model.

Context, Role, Action, Format, Target Audience. Five boxes. Fill them before you hit enter, and "ultimate prompts" stop being luck.

*Expanded from [The Ultimate Prompt To Write The Best Prompts](https://ideas.jorap.com/) on [ideas.jorap.com](https://ideas.jorap.com/).*
