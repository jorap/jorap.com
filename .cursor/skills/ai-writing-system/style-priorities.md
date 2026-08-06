# Style Priorities

Forte's **prioritization problem**: style guides grow until rules conflict. When they do, **higher number wins**.

Use when a draft feels "correct" by checklist but wrong on read — or when shortening would break a lower rule.

## Priority stack

| Rank | Rule | Source |
|------|------|--------|
| 1 | **No invented facts** — match author-context / facts ledger; `[NEEDS SCENE]` not fake anecdotes | author-context.md |
| 2 | **Plain words** — every word lands on first read; no thesaurus voice | jorap-voice Vocabulary |
| 3 | **De-AI** — kill hollow openers, transition spam, summary sandwiches | jorap-voice pass #2 |
| 4 | **Lived-in** — specifics, failures, durations; swap test fails generic paragraphs | jorap-voice pass #1, #6 |
| 5 | **Point of view** — "I want" / "Skip" over "users should" | jorap-voice pass #5 |
| 6 | **Visible thinking** — tradeoff or near-miss, then land the take | jorap-voice pass #3 |
| 7 | **Likability** — useful, honest, human, respectful (not performative warmth) | jorap-voice likability lens |
| 8 | **Structure** — H2 personality, `---` breaks, no `## Bottom line` on opinion posts | jorap-voice Structure |
| 9 | **Mechanical lint** — dashes, slop rules, voice-words.yaml | `pnpm lint:*` |
| 10 | **Meta / SEO** — `description` memorable, not keyword-stuffed; `social_media_intro` ≤200 chars, link-in-comments hook; `image_prompt` paste-ready hero generation | frontmatter |

## Conflict examples

| Conflict | Winner | Action |
|----------|--------|--------|
| Clever H2 vs plain words | Plain (2) | Rename heading |
| Longer explanation vs cut redundancy | De-AI (3) | Cut the restate |
| "Accurate" generic advice vs personal take | POV (5) | Rewrite with "I" |
| Invented vivid anecdote vs thin section | Facts (1) | `[NEEDS SCENE]` or cut |
| Grammar-perfect vs spontaneous rhythm | De-AI (3) + lived-in (4) | Roughen one sentence |
| Keyword-rich meta vs voice meta | Facts + plain (1–2) | First-person one-breath description |

## Garden notes — field overrides

For `content/english/notes/` frontmatter, **field shape** can outrank blog-body habits:

| Field | Priority note |
|-------|---------------|
| `description` | Third person, no contractions — beats pass #4 friend-flow |
| `key_concept` line 1 | Arguable claim (5) beats reflective questions (3) |
| `shareable_thought` | Exactly four thoughts — shape beats brevity |
| `examples` | Two one-sentence scenes (4) — not one long paragraph |

See garden-voice **When to use which** for pass mapping.

## When to update this stack

Only after the same conflict bites twice in one session. Patch [feedback-loop.md](feedback-loop.md), not this file, for one-off mistakes.
