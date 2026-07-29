# Master prompt section checklist

From Tiago Forte's PCM framework ([video](https://www.youtube.com/watch?v=o2S1ZbmVAAY), [AI Second Brain walkthrough](https://www.youtube.com/watch?v=yeTn8a5J-Gc)). Use as an interview outline — not every section applies to everyone.

**Work master prompt** and **personal master prompt** are separate documents.

## Personal identity

- [ ] Basic personal details (name, age range, location, family members)
- [ ] Core values (individual, not company)
- [ ] Personal vision and mission
- [ ] Goals and intentions (repeat if needed — Forte marks these twice on purpose)
- [ ] Personal SWOT: strengths, weaknesses, opportunities, threats
- [ ] Skills and expertise (what you're actually good at)
- [ ] What quality looks like to you

## Professional context (work prompt)

- [ ] Job title, role, team, reporting lines
- [ ] Company info: mission, vision, values, org chart
- [ ] Products / services offered
- [ ] Ideal customer profile
- [ ] Business strengths and weaknesses
- [ ] Brand voice examples
- [ ] Strategic processes, value chain, how you serve customers
- [ ] Income sources (only if AI will advise on money, pricing, promotions)

## How you work with AI

- [ ] Intentions for AI usage — what you're trying to accomplish
- [ ] Communication preferences (tone, length, format)
- [ ] How you **don't** want to communicate
- [ ] Working style (async vs sync, depth vs speed)
- [ ] Tool preferences and workflows
- [ ] Rules, boundaries, non-negotiables
- [ ] Embedded protocols — trigger phrases for repeatable workflows (e.g. "run morning briefing")

## LLM-optimized structure (after human draft)

Convert the human doc into:

```markdown
**USER PROFILE:** [one-line identity]

# CORE CONTEXT
[Role, activities, constraints]

# BEHAVIORAL INSTRUCTIONS
## ALWAYS
- [non-negotiable behaviors]

## ACTIVATE WHEN
- [signal] → [response pattern]

## AVOID
- [patterns that waste time or break trust]

# FRAMEWORKS
[Decision filters, pillars, prioritization hierarchies]

# RESPONSE STYLE
[How to structure answers by query type]

# SUCCESS INDICATORS
[What a good answer includes]
```

## ChatGPT compression (when over 1,500 chars)

Use a distillation pass — preserve behavioral rules, frameworks, and trigger conditions; compress examples to shorthand. Split across "What should ChatGPT know about you?" and "How should ChatGPT respond?" without dropping either half.

## What does NOT belong in persistent context

Move these to **project** layer:

- Single client details (unless you're a one-client shop)
- Active draft text
- Meeting notes from this week
- Temporary campaign or launch specifics
- Internal politics for one engagement

Move these to **perishable** layer:

- The paragraph you're editing right now
- One-off data pulls
- "Fix this error message" stack traces
