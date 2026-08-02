---
name: six-hats
description: >-
  Pressure-test a decision with one agent wearing Six Thinking Hats plus
  Outsider and Executor lenses in a forced sequence, then a Blue / Chairman
  verdict. Cheaper cousin of llm-council (no Task subagents). MANDATORY
  TRIGGERS: 'hats this', 'six hats', 'wear the hats', 'one-agent council',
  'one agent council', 'thinking hats'. STRONG TRIGGERS (real tradeoff,
  not expensive enough for full council): 'get another angle', 'no yes-men',
  'pressure-test cheap', 'sequential perspectives'. Prefer llm-council when
  being wrong is expensive (pricing, hire, retire a ranking URL). Do NOT
  trigger on factual lookups or pure creation.
---

# Six Hats (One Agent)

You ask one AI a question, you get one answer - often a yes-man. This skill
forces **friction in one session**: labeled lens blocks in order, no early
synthesis, Blue / Chairman only at the end.

Based on Edward de Bono's Six Thinking Hats, plus Outsider and Executor from
the [llm-council](../llm-council/SKILL.md) skill. Method from the draft
`content/english/blog/__six-hats-one-agent.md`.

**Do not spawn Task subagents.** One agent. One pass through the loop.

Label every block as **Color / Advisor** (same pattern as council names where they map).

| Color | Advisor |
|-------|---------|
| White | First Principles |
| Red | Instinct |
| Black | Contrarian |
| Yellow | Expansionist |
| Green | Options |
| *(none)* | Outsider |
| *(none)* | Executor |
| Blue | Chairman |

---

## When to use this vs llm-council

| Use **six-hats** | Use **llm-council** |
|------------------|---------------------|
| Archive/tips pressure test, draft critique, "should I revise X" | Pricing, hire-vs-automate, kill a URL that ranks, high-stakes pivot |
| Need tension tonight without the token bill | Need true independence + anonymous peer review |
| User says hats / one-agent / no yes-men | User says council / war room / pressure-test (expensive) |

If the user asks for council but the stakes look low, say one line: "This fits six-hats (cheaper). Say council if you still want five subagents." Then run six-hats unless they insist.

---

## Hard rules (anti-yes-man)

1. **No merging mid-stream.** Finish each labeled block before starting the next. Do not soften Black / Contrarian inside Yellow / Expansionist.
2. **Pick a side in Black / Contrarian and Yellow / Expansionist.** "It depends" belongs only in Blue / Chairman.
3. **No applause.** Do not open with "Great idea!" or end lens blocks with fake balance.
4. **Outsider near the end of the lenses** (after Green / Options) so it can call out insider mush.
5. **Blue / Chairman last.** Clear recommendation + one first step. Not a five-point plan.
6. **Never use the Task tool** for this skill.

---

## The loop

Scan 1–2 workspace files if the question names them (same habit as council Step 1A). Then run every step below in order in **one reply** (or one reply per step if the user asks to go slow).

### 1. Frame (neutral)

One short paragraph only:

- Core decision/question
- Key context from the user
- Key context from files (if any)
- What's at stake

No preferred answer. No advice.

### 2. White / First Principles

Known, unknown, checkable. Strip assumptions. No advice yet. Target 80–150 words.

### 3. Red / Instinct

Feelings and gut only. Allowed to be unfair. Target 40–80 words.

### 4. Black / Contrarian

What's wrong, missing, or fatal. Dig deeper if it looks solid. Target 100–200 words.

### 5. Yellow / Expansionist

Upside if it works. **Ignore risk here on purpose.** Target 100–200 words.

### 6. Green / Options

At least **two** alternatives to the default plan, including **do nothing**. Target 80–150 words.

### 7. Outsider

Zero insider context. Respond only to what's framed. What looks weird to a stranger? Target 80–150 words.

### 8. Executor

**One** Monday-morning step only. Can it be done? Fastest path? Target 40–80 words.

### 9. Self-review (optional, still one agent)

Three bullets only:

1. Strongest block so far, and why
2. Biggest blind spot among the blocks
3. What all blocks missed

Skip if the question is tiny; run when stakes are medium.

### 10. Blue / Chairman

Use this exact structure:

```markdown
## Where the lenses agree
[High-confidence overlap]

## Where the lenses clash
[Real tension; both sides]

## Blind spots
[From self-review or gaps you now see]

## The recommendation
[Clear answer. Not "it depends." One paragraph of reasoning.]

## The one thing to do first
[Single concrete next step. Not a list.]
```

---

## Output shape

Lead with the framed question in a blockquote or bold one-liner, then:

```markdown
### White / First Principles
…

### Red / Instinct
…

### Black / Contrarian
…

### Yellow / Expansionist
…

### Green / Options
…

### Outsider
…

### Executor
…

### Self-review
…

### Blue / Chairman
## Where the lenses agree
…
```

Keep the whole run scannable. Prefer short blocks over essays. No HTML report required (unlike llm-council). Optional: if the user asks to save, write `council/hats-transcript-YYYYMMDD-HHMMSS.md` (safe filename: digits and hyphens only).

---

## Example triggers

- "hats this: should I retire the Facebook Favorites post?"
- "six hats on this draft"
- "one-agent council: keep or cut the DNPAP page?"
- "wear the hats - is this the right stack for the client?"

---

## Credits

- Edward de Bono, *Six Thinking Hats*
- [Andrej Karpathy's LLM Council](https://x.com/karpathy) (independence idea; this skill trades independence for cost)
- Sibling skill: [llm-council](../llm-council/SKILL.md)
