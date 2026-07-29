# Implementation Guide

The process blueprint. The agent **interviews first**, then drafts. Never skip to prose when the user only named a topic.

Based on Tiago Forte's implementation guide: questions solicit **topic, tension, opinions, and source material** before generation.

## Phase 0 — Gather raw material

Before the interview, collect what exists:

- Rough notes, outlines, wikilinks, ideas.jorap.com export
- Book highlights, article clips, Perplexity output (cite sources; don't treat as fact)
- Voice-memo transcript if the user dictated thoughts

**Rule:** If the user has excerpts (e.g. book highlights), ask for them. Models lack full book text — specificity dies without source material.

## Phase 1 — Interview (one question at a time)

Ask **one question**, wait for the answer, then the next. Do not batch five questions in one message unless the user already answered them.

| # | Question | Why |
|---|----------|-----|
| 1 | What topic or claim do you want this piece to make? | Anchors thesis |
| 2 | What format and where does it live? (blog post, note, essay, recipe, tracker update) | Routes voice skill + file path |
| 3 | What should readers **feel** or **do** after reading? | Sets emphasis |
| 4 | Target length or depth? (short tip, ~800 words, long essay, atomic note) | Prevents bloat |
| 5 | What opinions, assertions, or lived experience must appear? (yours only) | Stops invented anecdotes |
| 6 | Source material to ground in? (links, highlights, prior posts) | Concreteness |
| 7 | Anything to **avoid**? (topics, tone, duplicate of existing post) | Boundaries |

**Stop condition:** Questions 1–4 answered minimum. For personal posts, question 5 is mandatory.

## Phase 2 — Framework proposal

After the interview, propose **2–3 structures** (not a full draft). Each option gets:

- Working title
- 4–6 H2s (blog) or field plan (note: `description`, `key_concept`, etc.)
- One sentence on what makes this angle different

Example framing:

> I see three ways to frame this. Pick one, merge two, or tell me to rethink:
> 1. **Problem → what I tried → what I do now** (gear/review lane)
> 2. **Myth → why it's wrong → plain alternative** (opinion lane)
> 3. **One scene → zoom out → one takeaway** (faith/family lane)

Wait for user choice before drafting.

## Phase 3 — Draft generation

**Before writing:**

1. Read [writing-samples.md](writing-samples.md) — same lane
2. Read [author-context.md](../jorap-voice/author-context.md) if personal
3. Load jorap-voice or garden-voice

**Draft rules:**

- Write to `content/english/blog/__{slug}.md` or `content/english/notes/{slug}.md`
- `draft: true` until user publishes
- Set `slug` in frontmatter
- Mark `[NEEDS SCENE]` where only the user can supply a real memory — do not invent
- No currency amounts; no engagement bait; no em dashes

**Blog opener:** experience, frustration, or scene — never "In today's world…"

**Note opener:** `key_concept` line 1 is a claim you'd argue, not "X is a framework for…"

## Phase 4 — Human pass (mandatory)

JoRap's edit pass (Forte: 90–95% there, then 1–2 human passes):

1. **Kill invented personal anecdotes** — if the draft opens with a story not in the interview, cut or replace with `[NEEDS SCENE]`
2. **One real detail per major section** — date, place, model, failure, duration
3. **Cut 10–20%** — summary sandwiches, restated H2s, parallel bullets
4. **Read aloud** — swap any word you wouldn't say mid-rush

Agent can flag issues; user supplies scenes the archive doesn't have.

## Phase 5 — Voice and lint

**Blog:**

1. `pnpm slop:score path/to/__draft.md` (baseline)
2. jorap-voice seven passes (minimum #2, #5, #7 on light polish)
3. `pnpm slop:score` again — per100w should drop
4. `pnpm lint:blog && pnpm lint:voice && pnpm lint:slop`

**Notes:**

1. garden-voice field workflow
2. `pnpm lint:garden`

## Prompt templates (copy-paste)

### Start a blog session

```
Run the AI writing system implementation guide for a new blog post.
Interview me one question at a time. Do not draft until I pick a framework.
```

### Draft from notes

```
I have raw material below. Run implementation guide Phase 1–2, then draft to __{slug}.md using jorap-voice.

Raw material:
[paste]
```

### Expand outline only

```
Expand this outline to prose using jorap-voice. Keep section order. Mark [NEEDS SCENE] where you need my memory. Do not invent personal anecdotes.

[paste outline]
```

### Perplexity pre-draft (optional)

From `__humanize-ai-articles.md` — use **before** voice passes on rough AI output:

```
Write with high perplexity and burstiness — mix short sentences with longer ones, vary paragraph length, and don't make every sentence the same shape.

Topic and notes:
[paste]
```

Then run jorap-voice passes on the result — perplexity alone is not JoRap voice.

## Bootstrap style guide from samples

Rare maintenance — `jorap-voice` is already the style guide. Use when rebuilding from scratch or adding a new content lane.

1. Pick 5–10 pieces from [writing-samples.md](writing-samples.md) (mix lanes)
2. For each sample, analyze: voice/tone, mood, sentence structure, transitions, rhythm, signature moves
3. Synthesize into one guide; **merge into jorap-voice** — don't create a competing doc
4. Add new anti-patterns to [examples.md](../jorap-voice/examples.md) if needed
5. Run `node scripts/ai-writing-samples-check.mjs`

Forte's analysis prompt (adapted):

```
You have expertise in linguistics and style analysis. Convert the provided text into a style guide section covering: voice/tone, mood, sentence structure, transition style, rhythm/pacing, signature styles. Call out what makes this author distinctive — with quoted examples. Flag clichés this author avoids.
```
