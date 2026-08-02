---
name: llm-council
description: >-
  Run any question, idea, or decision through a council of 5 AI advisors who
  independently analyze it, peer-review each other anonymously, and synthesize
  a final verdict. Based on Karpathy's LLM Council methodology. MANDATORY
  TRIGGERS: 'council this', 'run the council', 'war room this',
  'pressure-test this', 'stress-test this', 'debate this'. STRONG TRIGGERS
  (use when combined with a real decision or tradeoff): 'should I X or Y',
  'which option', 'what would you do', 'is this the right move',
  'validate this', 'get multiple perspectives', 'I can't decide',
  'I'm torn between'. Do NOT trigger on simple yes/no questions, factual
  lookups, or casual 'should I' without a meaningful tradeoff (e.g. 'should I
  use markdown' is not a council question). DO trigger when the user presents
  a genuine decision with stakes, multiple options, and context that suggests
  they want it pressure-tested from multiple angles.
---

# LLM Council

You ask one AI a question, you get one answer. That answer might be great. It might be mid. You have no way to tell because you only saw one perspective.

The council fixes this. It runs your question through 5 independent advisors, each thinking from a fundamentally different angle. Then they review each other's work. Then a chairman synthesizes everything into a final recommendation that tells you where the advisors agree, where they clash, and what you should actually do.

Adapted from [Andrej Karpathy's LLM Council](https://x.com/karpathy): dispatch to multiple perspectives, anonymous peer review, then a chairman verdict. In Cursor this uses the **Task** tool (`generalPurpose` subagents) with different thinking lenses instead of different models. Upstream skill: [tenfoldmarc/llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill).

---

## When to run the council

The council is for questions where being wrong is expensive.

**Good:** pricing/positioning choices, pivots, landing-page critique, hire-vs-automate, which of N options.

**Bad:** factual lookups, pure creation ("write a tweet"), summarization, casual should-I with no real tradeoff.

If the user already knows the answer and just wants validation, the council will likely push back. That's the point.

**Cheaper sibling:** for tension without five Task subagents, use [six-hats](../six-hats/SKILL.md) (`hats this`, `six hats`, `one-agent council`). Same anti-yes-man goal; forced sequence in one agent. Escalate to this skill when independence is worth the bill.

---

## The five advisors

Thinking styles that create tension — not job titles.

### 1. The Contrarian
Looks for what's wrong, missing, or fatal. Digs deeper if everything looks solid. Not a pessimist — the friend who saves you from a bad deal.

### 2. The First Principles Thinker
Asks "what are we actually trying to solve?" Strips assumptions. Rebuilds from the ground up. May say "you're asking the wrong question."

### 3. The Expansionist
Looks for upside and adjacent opportunity. Ignores risk (Contrarian's job). Cares what happens if this works better than expected.

### 4. The Outsider
Zero context about the user, field, or history. Responds only to what's in front of them. Catches curse-of-knowledge blind spots.

### 5. The Executor
Only: can this be done, and what's the fastest path? "What do you do Monday morning?" Flags brilliant ideas with no clear first step.

**Tensions:** Contrarian vs Expansionist · First Principles vs Executor · Outsider keeps everyone honest.

---

## How a council session works

### Step 1: Frame the question (with context enrichment)

**A. Scan the workspace (~30s).** Read the 2–3 files that ground the advisors. Prefer:

- `AGENTS.md`, relevant `.cursor/skills/*/SKILL.md`, or project README
- Files the user attached or named
- Recent `council/council-transcript-*.md` (avoid rehashing the same ground)
- Domain files for the question (e.g. content drafts, pricing notes, audience docs)

**B. Frame.** Neutral prompt for all five advisors:

1. Core decision/question
2. Key context from the user message
3. Key context from workspace files
4. What's at stake

Do not add your opinion or steer. If the ask is too vague ("council this: my business"), ask **one** clarifying question, then proceed. Save the framed question for the transcript.

### Step 2: Convene the council (5 subagents in parallel)

Spawn **all five** in one turn via the Task tool (`subagent_type: generalPurpose`). Do not run them sequentially.

Each advisor gets identity + thinking style + framed question + instruction to lean fully into their angle (no hedging, no balance). Target **150–300 words**. No preamble.

**Advisor prompt template:**

```
You are [Advisor Name] on an LLM Council.

Your thinking style: [advisor description from above]

A user has brought this question to the council:

---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be balanced. Lean fully into your assigned angle. The other advisors will cover the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

### Step 3: Peer review (5 subagents in parallel)

Anonymize advisor outputs as Response A–E (**randomize** the mapping). Spawn five reviewers in parallel; each sees all five anonymized responses and answers:

1. Which response is strongest, and why? (pick one)
2. Which has the biggest blind spot, and what is it?
3. What did ALL five miss that the council should consider?

**Reviewer prompt template:**

```
You are reviewing the outputs of an LLM Council. Five advisors independently answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

**Response C:**
[response]

**Response D:**
[response]

**Response E:**
[response]

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

### Step 4: Chairman synthesis

Parent agent (or one Task) receives: framed question, **de-anonymized** advisor responses, all peer reviews. Produce:

## Where the Council Agrees
## Where the Council Clashes
## Blind Spots the Council Caught
## The Recommendation
## The One Thing to Do First

Rules: clear recommendation (not "it depends"); chairman may dissent from the majority if reasoning is stronger; one concrete first step only.

**Chairman prompt template:**

```
You are the Chairman of an LLM Council. Your job is to synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question brought to the council:
---
[framed question]
---

ADVISOR RESPONSES:

**The Contrarian:**
[response]

**The First Principles Thinker:**
[response]

**The Expansionist:**
[response]

**The Outsider:**
[response]

**The Executor:**
[response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. These are high-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that only emerged through peer review. Things individual advisors missed that others flagged.]

## The Recommendation
[A clear, direct recommendation. Not "it depends." A real answer with reasoning.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

Be direct. Don't hedge. The whole point of the council is to give the user clarity they couldn't get from a single perspective.
```

### Step 5: Write the HTML report

Save to `council/council-report-YYYYMMDD-HHMMSS.html` (safe filename: digits and hyphens only — no colons).

Single self-contained HTML file, inline CSS. Include:

1. Question at the top
2. Chairman verdict prominent
3. Simple agreement/disagreement visual (grid or spectrum of advisor positions)
4. Collapsible `<details>` for each advisor response (collapsed by default)
5. Collapsible peer-review highlights
6. Footer: timestamp + what was counciled

Style: white background, subtle borders, system sans-serif, soft accent colors per advisor. Professional briefing, not flashy. Open/show the file after writing.

### Step 6: Save the transcript

Save `council/council-transcript-YYYYMMDD-HHMMSS.md` with:

- Original question
- Framed question
- All 5 advisor responses
- All 5 peer reviews + anonymization mapping revealed
- Chairman synthesis

Do not commit council artifacts unless the user asks.

---

## Output format

Every session produces:

```
council/council-report-YYYYMMDD-HHMMSS.html
council/council-transcript-YYYYMMDD-HHMMSS.md
```

Surface the verdict in chat briefly; point the user at the HTML report for the full scan.

---

## Example (product decision)

**User:** "Council this: I'm thinking of building a $297 course on Claude Code for beginners. My audience is mostly non-technical solopreneurs. Is this the right move?"

Typical tension: Contrarian (market flooded / refund risk) · First Principles (wrong goal?) · Expansionist (own the beginner entry) · Outsider ("Claude Code" means nothing) · Executor (validate with a $97 workshop first).

**Verdict pattern:** demand may be real, but tool-named framing fails outsiders; don't build the full course yet; one first step = outcome-named live workshop to validate.

---

## Important notes

- Always spawn all 5 advisors in parallel; same for peer review.
- Always anonymize for peer review.
- Chairman can disagree with the majority.
- Don't council trivial questions — just answer them.
- The visual report is the primary user-facing artifact.

---

Methodology by [Andrej Karpathy](https://x.com/karpathy). Claude Code adaptation inspired by [@olelehmann](https://x.com/olelehmann). Published by [@tenfoldmarc](https://instagram.com/tenfoldmarc). Cursor/repo adaptation for JoRap.com.
