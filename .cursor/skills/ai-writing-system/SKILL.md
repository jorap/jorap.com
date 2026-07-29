---
name: ai-writing-system
description: >-
  JoRap's AI writing system (Tiago Forte model): interview for ideas, draft in voice,
  polish with lint. Use when starting a new blog post or note from scratch, expanding
  an outline, running a writing session, or when the user says "AI writing system",
  "write like me", or "draft from my notes". Routes to jorap-voice (blog) or
  garden-voice (notes). Style guide already lives in those skills — this skill runs
  the implementation guide and feedback loop.
---

# AI Writing System

Tiago Forte's model, adapted for Cursor: **style guide + implementation guide + feedback loop**, not a pile of one-off prompts.

| Forte piece | JoRap equivalent |
|-------------|------------------|
| Writing samples | [writing-samples.md](writing-samples.md) |
| Style guide | [jorap-voice](../jorap-voice/SKILL.md) (blog) · [garden-voice](../garden-voice/SKILL.md) (notes) · `data/voice-words.yaml` |
| Prioritized rules | [style-priorities.md](style-priorities.md) — when rules conflict, higher wins |
| Implementation guide | [implementation-guide.md](implementation-guide.md) |
| Claude Project | This skill + Cursor rules (`anti-slop.mdc`) |
| Feedback loop | [feedback-loop.md](feedback-loop.md) |

Inspired by [How to Build Your AI Writing System](https://www.youtube.com/watch?v=TUfGJY7gRxw) and [I Trained AI to Write Like Me](https://www.youtube.com/watch?v=vlc_enCxaJE). Persistent context layer: [personal-context-management](../personal-context-management/SKILL.md) (Forte PCM / master prompt).

## When to use

- New blog post or note from a topic, outline, or source material
- Expanding a `__` draft or ideas.jorap.com export
- User wants a repeatable writing session, not a single prompt
- Rebuilding or auditing the voice system after repeated failures

**Not this skill alone:** line edits on finished prose → `jorap-voice` or `garden-voice` directly.

## Four-step system (already built)

### Step 1 — Samples

Canonical on-voice pieces are listed in [writing-samples.md](writing-samples.md). Before a big draft, read **1–2 samples in the same lane** (gear, how-to, opinion, PKM note, faith note).

To refresh samples: run the bootstrap flow in [implementation-guide.md](implementation-guide.md#bootstrap-style-guide-from-samples) — rare; `jorap-voice` is the living style guide.

### Step 2 — Style guide

Do **not** improvise voice. Load the right skill:

| Output | Skill | Facts ledger |
|--------|-------|--------------|
| `content/english/blog/` | jorap-voice | [author-context.md](../jorap-voice/author-context.md) |
| `content/english/notes/` frontmatter | garden-voice | author-context when personal |

On conflict between rules, follow [style-priorities.md](style-priorities.md).

### Step 3 — Implementation guide

Follow [implementation-guide.md](implementation-guide.md) end to end:

1. **Interview** — one question at a time; no drafting until answers are in
2. **Framework** — agent proposes 2–3 structures; user picks or merges
3. **Draft** — first pass at 90% voice, not publish-ready
4. **Human pass** — JoRap adds real scenes, cuts invented anecdotes, fixes facts
5. **Voice + lint** — seven passes (blog) or garden workflow; `pnpm slop:score` before/after

### Step 4 — Feedback loop

When a draft fails the same way twice, patch the system — not just the draft. See [feedback-loop.md](feedback-loop.md).

## Quick start (one session)

Copy this checklist and run it in order:

```
Session:
- [ ] Route: blog or note?
- [ ] Read author-context if personal/faith/gear/family
- [ ] Read 1–2 samples from writing-samples.md (same lane)
- [ ] Interview (implementation-guide) — STOP if user hasn't answered
- [ ] Propose 2–3 frameworks → user picks
- [ ] Draft to file (`__slug.md`, draft: true)
- [ ] Human pass: kill invented anecdotes, add one real detail per section
- [ ] Voice passes + pnpm slop:score → lint
```

## Content-type routing

| User wants | Start file | Voice skill | Extra |
|------------|------------|-------------|-------|
| Blog post | `content/english/blog/__{slug}.md` | jorap-voice | `archetypes/blog.md` frontmatter order |
| Note (new) | `content/english/notes/{slug}.md` | garden-voice | Field workflow in garden-voice |
| Outline → prose | existing `__` draft | jorap-voice **Expanding outlines** | Delete wiki footer after rewrite |
| Note from blog seed | note file | garden-voice | Distill; don't paste blog tone into `description` |
| Flashcards | note `cards` frontmatter | garden-voice + flashcards | |

## Quality bar

- **90–95% on first draft** is the target (Forte). One or two human editing passes, not ten.
- **Blockers before publish:** invented personal facts, AI anecdotes, currency amounts, em dashes, slop lint failures.
- **Swap test:** every section must fail the "any blog could run this" test — jorap-voice pass #1.

## Related drafts on site

- `content/english/blog/__humanize-ai-articles.md` — perplexity/burstiness prompt for raw AI shape
- `content/english/blog/__craft-prompt-framework.md` — CRAFT for one-off prompts outside this system

## Verify samples resolve

```bash
node scripts/ai-writing-samples-check.mjs
```
