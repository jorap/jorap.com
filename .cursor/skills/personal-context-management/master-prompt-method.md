# Master Prompt Method (Forte + Miyamoto)

Hayden Miyamoto's operating-system layer on top of PCM. Taught in Forte's YouTube series:

- **Part 1:** [Unlock AI's Full Potential](https://www.youtube.com/watch?v=_K_F_icxtrI) — what it is, why upstream context wins, six-section V1 structure
- **Part 2:** [Live Demo That Will 3X Your AI Productivity](https://www.youtube.com/watch?v=D9DpUDntQRc) — side-by-side without vs with master prompt; protocols in action

Related full workshop: [Build Your AI Operating System](https://www.youtube.com/watch?v=yNpbnrlAFzA).

PCM (three layers) answers *when* to load context. Master Prompt Method answers *what* goes in persistent context and *how* to structure it.

## One-sentence definition

Provide **all** context about you, your organization, and your offerings **upfront and at once** — upstream, before the task — so every later interaction inherits it.

**Not this:** fancy multi-step prompts per chat (better than a bare question, weaker than persistent context).

## Two knowledge types

| Type | What it is | Your control |
|------|------------|--------------|
| **General** | Training data — internet-scale facts | None. Model choice only. |
| **Contextual** | Who you are, org chart, products, values, metrics, processes | **Everything.** This is the master prompt. |

Most people over-index on model picking and under-invest in contextual knowledge.

## Operational vs transformational

| Focus | Examples | AI payoff |
|-------|----------|-----------|
| **Operational** | Faster email, tidier calendar, slightly better meetings | Marginal |
| **Transformational** | Hire an A-player in minutes; six-month SOP project → 30 minutes; 10× goal revision | Where master prompt pays |

Design protocols for transformational workflows you repeat — hiring packs, SOP generation, onboarding docs — not one-off chat tricks.

## V1 structure (six sections)

Build in a Google Doc or Markdown file. Treat V1 as a **proto master prompt** — hypotheses, not gospel. Use AI as thought partner to fill each section via interview questions.

### 1. Personal info & AI mandate

- Name, role, where you sit in the hierarchy, who you report to
- Strengths and weaknesses (honest)
- **AI mandate:** how AI should compensate — e.g. "I want AI to drive accountability, documentation, and schedule discipline because those are my gaps"

### 2. Core company / work context

- What you do, when you started, team size
- Products and services — features, benefits, pricing if relevant
- The "what we really sell" outcome (not feature lists)

### 3. Ideal customer & market

- ICP — who you serve perfectly (specific beats vague)
- Competitors and differentiators
- Market positioning

### 4. People & KPIs

- Team members, roles, reporting lines
- Metrics each role owns — conversion rates, targets, funnel stages
- Enough detail that AI names **real people and real numbers**, not generics

### 5. Culture & core values

- Mission, vision, values, long-term goals (BHAG if you have one)
- Brand voice examples

### 6. Protocols (mini-programs)

Embedded workflows the AI runs on a **trigger phrase**:

| Trigger | What it does |
|---------|--------------|
| `AI hiring` | Ask 5 questions one at a time, pre-fill answers from master prompt, then produce JD, rubric, case studies, onboarding agendas |
| `AI SOP` | From a screenshot or flowchart, generate step-by-step SOPs in your house style |

Protocols are **short paragraphs + instructions**, not the whole 20-page doc. Add over time. Don't bury long-term strategy here — keep protocols executable.

## Document shape (Hayden's live example)

~20–30 pages in human-readable form; shorter when LLM-optimized.

```
[PERSONAL HEADER — customized per user/role]
  name, role, personal goals for this AI instance

[SHARED COMPANY BASE — same for whole team]
  structure, products, goals, sales funnel, conversion metrics,
  teams, fixed costs, core values, protocols

[TRIGGER: protocol name]
  when user says X → run this workflow
```

- **Company base** — shared with team; part of onboarding
- **Personal header** — top section customized per person so same company prompt serves CFO vs marketing director

## Part 2 demo pattern (before / after)

**Without master prompt:** "I need to hire a marketing director" → generic job-description filler; you'd Google and paste.

**With master prompt + `AI hiring` protocol:**
1. AI asks five questions **one at a time**
2. Pre-fills each answer from master prompt ("based on what I know…")
3. You confirm or correct (`yes` / edits)
4. AI outputs multiple artifacts: JD with KPIs per responsibility, screening rubric, posting copy, case studies, meeting agendas, contractor agreement — tied to **your** frameworks (e.g. Topgrading)

Same pattern for operations: paste flowchart screenshot → `AI SOP` → checklist-style SOPs per step in your format.

**Quality bar:** Output should name specific people, metrics, and values — not plausible-sounding fiction. If it hallucinates org facts, the master prompt is missing or wrong.

## Build loop

1. **Questionnaire → draft** — answer section prompts; let AI generate first pass
2. **LLM-optimize** — compress to headers, ALWAYS / ACTIVATE / AVOID (see [master-prompt-sections.md](master-prompt-sections.md))
3. **Deploy** — Claude Personal Preferences, Project file, ChatGPT Custom Instructions, or Cursor rules/skills
4. **Test** — run a protocol; when AI pre-fills an answer, verify accuracy; patch the doc
5. **Ask for gaps:**
   ```
   Given my master prompt, answer [task] using only what you know about me.
   Show your reasoning. What did you have to guess?
   ```
6. **Monthly review** — goals, metrics, team, and protocols drift; stale context worse than none

## JoRap mapping

| Master Prompt Method | JoRap equivalent |
|----------------------|------------------|
| Shared company base | `.cursor/rules/` + repo conventions |
| Personal header | Cursor user rules, `author-context.md` |
| Voice / brand | `jorap-voice`, `garden-voice` |
| Protocols | Cursor **skills** (e.g. `alex-eala-tracker-update`, `ai-writing-system`, `changelog-update`) |
| Project layer | `__` drafts, task-specific skill load |
| Perishable | Current message + `@` files |

**Cursor advantage:** master prompt is already **sharded** — don't merge into one 30-page paste unless exporting to Claude/ChatGPT. Add a new **protocol** by adding a skill with a clear trigger description.

### JoRap-sized protocols (examples)

| Trigger intent | Skill to load |
|----------------|---------------|
| New blog from scratch | `ai-writing-system` |
| Voice polish | `jorap-voice` / `garden-voice` |
| Tracker update | `alex-eala-tracker-update` |
| Ship changelog | `changelog-update` |
| Lazy diff review | `ponytail-review` |

When a workflow repeats and needs the same context bundle every time, that's a protocol candidate — encode it as a skill, not a longer user message.

## Anti-patterns

- **Fancy prompts without persistent context** — re-explaining yourself every chat
- **Dumping the whole drive** — context rot; use PCM three-layer discipline
- **Protocols that are really essays** — keep triggers short; detail lives in base doc
- **One master prompt for work + personal** — Forte and Hayden both separate these
- **Set and forget** — metrics, team, and goals change; review monthly
