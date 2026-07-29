---
name: personal-context-management
description: >-
  Tiago Forte PCM and Master Prompt Method: three context layers (persistent,
  project, perishable), six-section V1 master prompt, protocols/mini-programs.
  Use when setting up AI context, building a master prompt, AI hiring/SOP workflows,
  fixing generic AI output, context rot, PCM, master prompt method, or mapping
  Forte's AI Second Brain to Cursor.
---

# Personal Context Management (PCM)

Tiago Forte's discipline for the AI era: the bottleneck moved from capture to **curating the minimum right context** so AI stops averaging you out.

Sources:

| Topic | Video |
|-------|-------|
| PCM + three layers | [What Is Personal Context Management?](https://www.youtube.com/watch?v=o2S1ZbmVAAY) |
| Master Prompt Method (theory) | [Part 1: Unlock AI's Full Potential](https://www.youtube.com/watch?v=_K_F_icxtrI) |
| Master Prompt Method (live demo) | [Part 2: 3X Your AI Productivity](https://www.youtube.com/watch?v=D9DpUDntQRc) |
| Full system walkthrough | [The AI Second Brain](https://www.youtube.com/watch?v=yeTn8a5J-Gc) |

Full method reference: [master-prompt-method.md](master-prompt-method.md).

**Core lines:** Better results come from better context — not better one-shot prompts. Load context **upstream** (all at once, before the task), not via fancy per-chat prompts.

## Three layers (Three P's)

| Layer | What it is | Half-life | JoRap repo equivalent |
|-------|------------|-----------|------------------------|
| **Persistent** | Stable identity: who you are, how you work, values, voice | Months–years | `.cursor/rules/*.mdc`, user rules, [author-context.md](../jorap-voice/author-context.md), voice skills |
| **Project** | Current work: goals, decisions, constraints, reference files | Weeks–months | Loaded skill for the task, `__` draft files, project-specific instructions |
| **Perishable** | Minimal slice for *this* request | One turn | User message, `@` file picks, pasted excerpt |

**Rule:** Load the smallest bundle that completes the task. Dumping everything causes context rot — poisoning (one error hijacks the reply), distraction (irrelevant files), confusion (contradictory instructions).

## Master prompt

A **master prompt** is your cross-platform operating manual for AI: one document (Markdown, Google Doc, Claude Project file) with durable context so you never re-introduce yourself.

Forte separates **work** and **personal** master prompts so contexts don't bleed.

### Master Prompt Method (Parts 1 & 2)

Forte + Hayden Miyamoto's build sequence — see [master-prompt-method.md](master-prompt-method.md):

1. **Six V1 sections** — personal info & AI mandate → company → ICP/market → people/KPIs → culture → **protocols**
2. **General vs contextual knowledge** — you can't edit training data; contextual knowledge is the whole game
3. **Protocols** — trigger phrases (`AI hiring`, `AI SOP`) that run mini-programs against the shared base
4. **Company base + personal header** — shared org context; top section customized per role
5. **Test loop** — AI pre-fills from master prompt; you confirm; patch doc when it guesses wrong

Part 2 proof: empty Claude + "hire a marketing director" → generic fluff. Loaded master prompt + `AI hiring` → five confirm-or-correct questions, then JD, rubric, case studies, agendas — naming real people and metrics.

### What belongs in persistent context

- **PCM circle diagram** (identity, values, income, comms prefs, SWOT, etc.): [master-prompt-sections.md](master-prompt-sections.md)
- **Six-section V1 + protocols**: [master-prompt-method.md](master-prompt-method.md)

**JoRap already has pieces split across files** — don't duplicate; link:

| Master prompt section | Existing home |
|-----------------------|---------------|
| Voice / communication style | [jorap-voice](../jorap-voice/SKILL.md), [garden-voice](../garden-voice/SKILL.md) |
| Personal facts ledger | [author-context.md](../jorap-voice/author-context.md) → `__interesting-facts-about-jorap.md` |
| Writing workflow | [ai-writing-system](../ai-writing-system/SKILL.md) |
| Repo conventions | `.cursor/rules/*.mdc` |
| Code style / laziness | [ponytail](../ponytail/SKILL.md), `ponytail.mdc` |
| Protocols (repeatable workflows) | Cursor skills — see protocol table in [master-prompt-method.md](master-prompt-method.md#jorap-mapping) |

When building a master prompt for export (Claude Profile, ChatGPT Custom Instructions, Gemini), **assemble from these sources** — don't invent parallel copies in the skill.

**New repeatable workflow?** Add a skill (protocol), not a longer rule file.

## PCM flow (Forte)

```
Capture → Organize (PARA) → Master Prompt → AI advisors / tasks
```

Pre-AI CODE + PARA still matter. PCM adds the layer where organized knowledge becomes **curated context bundles** for AI — not a dump of your whole drive.

## Build workflow

Use when JoRap asks to create or refresh a master prompt (work or personal).

### 1. Pick scope

- **Work** — freelance WordPress, jorap.com, client delivery, consulting
- **Personal** — family, faith, health, hobbies, home

One master prompt per scope. Never merge.

### 2. Interview (one question at a time)

Walk the **six V1 sections** in [master-prompt-method.md](master-prompt-method.md), then PCM-only sections in [master-prompt-sections.md](master-prompt-sections.md). Skip sections already covered in repo files; note the canonical path instead.

Minimum before drafting:
- **AI mandate** — what weaknesses should AI compensate for?
- Name, role, location (if relevant to advice)
- What AI should **do** vs **not do**
- Communication preferences (plain words, no slop — cross-ref jorap-voice)
- Top 3 current goals + KPIs if work prompt
- Personal SWOT (honest, brief)
- At least one **protocol** candidate — workflow you'd trigger by name

### 3. Draft the document

- Human-readable first (Google Doc or `docs/master-prompt-work.md` — **gitignored or `[skip ci]`** if personal)
- Bullet lists over prose walls
- Mark **hypotheses** vs **decided** (proto master prompt)

### 4. LLM-optimize

Transform for token efficiency without losing behavioral rules:

```
Transform the following human-readable personal context document into an
LLM-optimized format that maximizes comprehension and actionability for AI
assistants. Preserve all behavioral instructions, frameworks, and trigger conditions.
Use headers, bullets, and "WHEN user X → do Y" patterns.
```

Add **ACTIVATE** / **AVOID** sections (see [Tinker w/ AI Master Prompt Method](https://tinkerwith.ai/p/the-master-prompt-method)).

### 5. Deploy per platform

| Platform | Where persistent context lives |
|----------|-------------------------------|
| **Cursor** | User rules + `.cursor/rules/` + skills (already split) |
| **Claude** | Settings → Profile → Personal Preferences, or Project instructions + one master file |
| **ChatGPT** | Custom Instructions (1,500 char × 2 — compress with distillation prompt) |
| **Gemini** | Saved context / Gems |

Cursor doesn't need one giant paste — **rules + skills ARE the master prompt**, sharded by concern.

## Maintenance loop

PCM is not set-and-forget. Schedule or trigger on life/work changes:

1. **Monthly (15–30 min):** Scan master prompt / rules for stale goals, wrong stack facts, tone drift
2. **After a repeated AI failure:** Patch the **system** (rule, skill, author-context row) — same pattern as [feedback-loop.md](../ai-writing-system/feedback-loop.md)
3. **Ask the AI for gaps:**
   ```
   Given my custom instructions and context files, what clarifications would help
   you assist me better? What context here is irrelevant to most tasks?
   ```
4. **Ask for blind spots** (ChatGPT Memory users): weaknesses noticed across chats

When persistent context is wrong, AI will **over-apply** it to unrelated tasks — trim sections that belong in project layer only.

## Agent behavior when this skill is active

1. **Classify the request** — which layer(s) does this need? Don't load voice skills for a Hugo bugfix; don't skip author-context for a personal blog draft.
2. **Prefer existing shards** — read author-context, jorap-voice, relevant rules before asking JoRap to repeat facts.
3. **Project context** — for a writing session, load ai-writing-system + voice skill + the `__` draft; not the whole garden.
4. **Perishable only in the message** — paste the minimum excerpt; point to file paths instead of dumping whole posts.
5. **Encode wins** — if JoRap corrects the same missing context twice, update the persistent layer (author-context, rule, or skill) per [self-improvement.mdc](../../rules/self-improvement.mdc).

## Quality checks

- [ ] Work and personal contexts separated where values/goals differ
- [ ] No contradictory instructions across rules and voice skills
- [ ] Facts match `__interesting-facts-about-jorap.md` ledger
- [ ] Project files/rules updated when a decision is made (DECISIONS pattern)
- [ ] Stale project context removed — old context worse than none

## Related skills

- [ai-writing-system](../ai-writing-system/SKILL.md) — PCM for *drafting* (samples + voice + interview)
- [jorap-voice](../jorap-voice/SKILL.md) / [garden-voice](../garden-voice/SKILL.md) — persistent voice layer
- [ponytail](../ponytail/SKILL.md) — persistent engineering values

## Further reading

- Forte free starter guide: [Build your own Master Prompt](https://bit.ly/4uwGhJu)
- [Glasp: Personal Context Management](https://glasp.co/articles/personal-context-management) — identity / knowledge / task framing
- [Tinker w/ AI: Master Prompt Method](https://tinkerwith.ai/p/the-master-prompt-method) — LLM-optimize + ChatGPT compression
- Five context levels (follow-on): [The Future of AI Prompting](https://www.youtube.com/watch?v=ipIOC55AwyQ)
