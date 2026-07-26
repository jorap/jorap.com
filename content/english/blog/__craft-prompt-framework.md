---
title: "The CRAFT Prompt Framework"
meta_title: "CRAFT - How to Write Prompts That Actually Work"
description: "Vague prompts get vague answers. CRAFT - Context, Role, Action, Format, Target Audience - is how I build prompts that don't leave the model guessing."
slug: "craft-prompt-framework"
date: "2026-06-18T06:13:00Z"
image: "/images/feature-consistent-ai-output.jpg"
categories: ["AI", "Writing", "Tips"]
author: "JoRap"
tags: ["AI", "Prompts", "CRAFT", "Prompt Engineering", "Writing", "ChatGPT", "LLM", "Content Creation", "PKM"]
related_notes:
  - intellectual-sourcing
  - the-feynman-technique
  - evergreen-notes
  - layered-reading
  - commonplace-book
  - literature-notes
featured: false
draft: true
---

"Write me a blog post about productivity" is a coin flip. I tried that once for a client newsletter and got three paragraphs of oatmeal with a "In conclusion" footer. Never again without a shape.

The prompts I keep in my notes share a structure. I call it **CRAFT** - Context, Role, Action, Format, Target Audience. Not my invention. The acronym I actually use before I hit enter.

---

## Five boxes before I hit enter

| Letter | Section | Job |
|---|---|---|
| **C** | Context | What's the situation? What does the model need to know? |
| **R** | Role | Who should it be? Expertise, voice, years in the trade |
| **A** | Action | Numbered steps, in order |
| **F** | Format | Essay, table, markdown, word count, headings |
| **T** | Target audience | Who reads it - job, literacy, geography |

Miss any letter and you get **generic middle.**

---

## Real prompt I used (Hugo migration checklist)

Not a meta-prompt about ultimate prompts. A real job:

```
CONTEXT: I'm migrating a client blog from WordPress to Hugo. Theme is Hugoplate. They have 40 posts with featured images in /uploads. Cloudflare Pages will build on push.

ROLE: Senior Hugo developer who's done messy WordPress exports before. Plain English, no hype.

ACTION:
1) List export steps from WordPress (plugin + manual checks)
2) Folder layout for Hugo page bundles with images
3) Frontmatter mapping (WP fields → Hugo YAML)
4) Cloudflare build settings to verify (Hugo version, NODE_VERSION)
5) Pass-off checklist for the client

FORMAT: Markdown with H2 sections and numbered steps inside each.

TARGET AUDIENCE: Freelancer (me) running the migration solo. Client is non-technical.
```

That returned something I could **execute**, not a motivational essay about digital transformation.

---

## Fill-in-the-blank beats hope

Good prompts leave intentional gaps:

- `[TOPIC]`
- `[WORD COUNT]`
- `[TONE: casual / formal]`
- `[EXCLUDE: topics or claims]`

Reuse the skeleton. Don't rewrite from scratch every Tuesday.

---

## Where my prompts still break

Role without context gets me "you're an expert" at what, for whom. Action as a paragraph loses to numbered steps every time. Skip the format and I get an essay when I needed HTML. Skip the audience and I get academic when I wanted blog casual.

---

CRAFT isn't bureaucracy. It's **kindness to future-you** - and to the model.
