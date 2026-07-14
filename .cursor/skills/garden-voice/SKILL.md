---
name: garden-voice
description: >-
  Write and edit JoRap notes garden frontmatter in the author's personal voice.
  Use plain words that land on first read.
  Use when drafting or polishing description, key_concept, examples, shareable_thought,
  relationships.reason on content/english/notes/, Eternal Principles scripture notes,
  or when garden prose sounds generic, dictionary-ish, or AI-generated.
  For flashcard word choice, use with flashcards skill. For blog posts, use jorap-voice instead.
---

# Garden Voice

Keep notes garden frontmatter sounding like JoRap wrote them - practical, personal, and plain-spoken. **Vocabulary:** plain words only. Every word should land on first read.

**Primary test:** Would a reader think a real person typed this after living the thing? If it reads like a summary of what a good note *should* say, rewrite it.

**Blog posts** use [jorap-voice](../jorap-voice/SKILL.md), not this skill.

## When to use

- Writing or editing `description`, `key_concept`, `examples`, `shareable_thought`, `relationships.reason` on `content/english/notes/`
- Eternal Principles / faith notes with scripture in `key_concept`
- Flashcard fronts and backs - word choice only ([flashcards](../flashcards/SKILL.md) owns shape)
- Rewriting stiff or AI-generated garden frontmatter

## When to use which (garden vs seven passes)

Blog posts use [jorap-voice](../jorap-voice/SKILL.md) and its **seven rewrite passes** (lived-in, de-AI, thinking, friend-flow, POV, credible, editor). Notes garden frontmatter uses **this skill** - same voice goal, different shape.

| You are editing | Use |
|-----------------|-----|
| `content/english/blog/` | jorap-voice - all seven passes on body prose |
| `content/english/notes/` frontmatter | garden-voice - field workflow below |
| Flashcard fronts/backs | garden-voice (words) + [flashcards](../flashcards/SKILL.md) (shape) |
| Bloated draft before splitting into fields | Seven passes on the blob, **then** split and run garden-voice per field |

**Seven passes on garden fields** - one read per pass, per field (not the whole note at once):

| Pass | Garden field | How it maps |
|------|--------------|-------------|
| 1 Lived-In | `examples`, faith gloss | Two scenes that feel different; first-person gloss after `{{< bible >}}` |
| 2 Strip AI Tells | All fields | Same as de-AI pass below + `pnpm lint:voice` |
| 3 Show Thinking | `key_concept` only | Tradeoffs in the claim stack - not open questions in `shareable_thought` |
| 4 One-Friend | Cards, note body | Frontmatter stays tighter: no contractions, third-person `description` |
| 5 Sharper POV | `key_concept` line 1 | Claim you'd argue - not a dictionary opener |
| 6 Credible | `examples`, `key_concept` | Specific scene or failure, not "good practice" |
| 7 Top-Editor | All fields | Voice check below - **cut** for density, do not lengthen for flow |

**Minimum on any garden edit:** pass **#2**, **#5** on `key_concept` line 1, **#7** (voice check). Even one-line `relationships.reason` fixes get the de-AI pass.

**Conflicts to respect:** pass #3 (reflective, open questions) and #4 (conversational) apply most to cards and body - not permission to ramble in `description`, `shareable_thought`, or `relationships.reason`.

## Workflow

1. **Read 1-2 reference notes** in the same lane before writing:
   - **PKM:** `content/english/notes/capture.md`, `rollback-principle.md`
   - **Faith / EP:** `content/english/notes/abide-in-me.md`, `the-golden-rule.md`
   - **Ethics / systems:** `content/english/notes/blameless-after-action-review.md`
   - **Flashcards (tone):** `capture.md`, `abide-in-me.md`, `the-golden-rule.md`
2. **Draft in the author's voice**, not a textbook or SEO summary.
3. **Run the de-AI pass** (below) - mandatory, even on one-line fixes.
4. **Run the voice check** (below) before finishing.
5. Before/after samples: [examples.md](examples.md).
6. Do **not** commit or push unless the user explicitly asks.

## Two registers

Wiki prose in `key_concept` can be tighter than cards, but still plain. Cards are the plainest layer.

| Field | Shape |
|-------|-------|
| `description` | Third-person, one-breath definition - memorable cold weeks later |
| `key_concept` | Plain-English claim you'd argue (line 1, no wikilinks), then 2-4 tight sentences, then wikilink stack |
| `examples` | Two scenes that *feel* different - one sentence each |
| `shareable_thought` | Exactly four complete thoughts - each a different angle, paste-ready alone |
| `relationships.reason` | Short clause, telegraphic OK |
| `cards` | Plainest - see [flashcards](../flashcards/SKILL.md) |

**Contractions** (`don't`, `it's`) - note body and cards only, not frontmatter fields above.

**Local context** (Shopee, jeepney, sideline) - only when the scene is actually from that life. Never forced.

**Faith / EP lanes** - straight tone in commentary. No dry humor in verse glosses or faith `key_concept`.

## `key_concept`

### Line 1: claim you'd argue

Open with a plain-English claim you'd defend - not a dictionary definition.

```
Grace is a gift I never earned - Christ paid what I couldn't.

I receive eternal life by believing His promise, not by climbing a moral ladder.
[[Justification]] is free and finished at faith; [[Sanctification]] belongs to the walk after.
```

Not: "Sanctification is the process whereby believers undergo moral transformation…"

**Line 1 has no wikilinks.** Stack `[[wikilinks]]` after the punch and 2-4 supporting sentences.

**Density:** punch line, blank line, then at most 2-4 tight sentences before the link stack grows.

### Faith notes need a Bible verse

Every faith note's `key_concept` includes scripture. EP spine notes follow the scripture block rules below; other faith notes still open with verse + gloss before the claim stack.

**Workplace lane** (`Workplace` tag, [[Workplace Principles]] hub): corporate-friendly - no `{{< bible >}}` shortcodes or verse citations in frontmatter. Gospel depth stays in wikilinked source notes.

### Scripture (Eternal Principles)

**Eternal Principles** notes anchor on **Jesus' words** (Matthew, Mark, Luke, John) in **NASB 1995**. Use the `{{< bible >}}` shortcode for scripture in `key_concept` - Hugo renders NASB 1995 at build time from `data/scripture-nasb1995.json`. Paul and other writers may follow as expansion, not as the primary anchor.

After each shortcode, add one **explanation bullet** in JoRap voice (first person where natural). Gloss text lives in `data/ep-verse-explanations.yaml`. Run `python3 scripts/archive/format-faith-bible-blocks.py` after bulk edits to restore shortcode + bullet shape.

```
  {{< bible ref="John 15:1-11" emphasize="5" >}}

  - Cut off from the vine, I produce nothing lasting - fruit comes from staying connected, not willpower theater.

  [Plain-English claim bullets - no wikilinks on line 1]
```

Do **not** paste full NASB paragraphs into frontmatter. Gospel quotes render **red** on the site automatically.

When quoting Bible **text** elsewhere in the garden, use **NASB 1995** wording. Run `python3 scripts/archive/apply-nasb-quotes.py` for paraphrase migrations.

## `description`

Third-person, one-breath definition - what the concept is or does; recall it cold weeks later. No `[[wikilinks]]`. ≤20 words.

Good: "Eternal life is Christ's gift received by faith alone, not wages for commandments, principles, or good works."

## `examples`

Two scenes that **feel** different - same move, different surfaces. **One sentence each.** Domain labels do not matter; duplicate vibe does.

Good pair (`capture.md`): wristband during cooldown + receipt on the jeepney.

## `shareable_thought`

**Exactly four** items. Each is a **complete thought** a reader understands alone - paste-ready for Slack or slides.

Each item must hit a **different angle** (definition, move, boundary, payoff) - not four fragments, not four restatements of the same line.

Bad: `"Growth, not the ticket."` (fragment)

Bad: four copies of `description` with tiny word swaps.

## `title` and `meta_title`

**Prefer 4 words.** Hard gate: **max 5 words**; a 5th word only when `len(title) ≥ 30` (letters, spaces, punctuation), the line is a **fixed phrase or scripture quote**, and the 5-word title beats the best 4-word trim. Never 6+ words.

Examples: `Golden Rule at Work` (4); `Integrity Without an Audience` (4); `Let Your Yes Be Yes` (5 - Matthew 5:37, phrase exempt).

`meta_title`: `Topic - Plain subtitle` - e.g. `Sanctification - Becoming Holy After Faith`. Not dictionary labels alone.

## Vocabulary

Plain speech beats smart-sounding prose.

| Rule | Detail |
|------|--------|
| **Skill beats lint on new drafts** | This skill and [examples.md](examples.md) are stricter than `data/voice-words.yaml`. Lint may allow words you still should not write fresh. |
| **Say it out loud** | If you wouldn't say it to a friend mid-rush, swap for the plain word |
| **Topic terms OK** | Theology/PKM terms when the note is *about* the term - gloss in plain English first |
| **Gloss once** | First use of a theology or PKM term: plain English in the same breath, then the term |

### Common swaps (garden)

| Instead of | Say |
|------------|-----|
| `unmerited favor` | gift you didn't earn (then "unmerited favor" if needed) |
| `distill` | boil down / shorten |
| `deploy` | push live |
| `metadata` | tags and fields |
| `contradicts` (in relationship reasons) | goes against |

Hard bans live in `data/voice-words.yaml`. Run `pnpm voice:scan` to review hits; `pnpm lint:voice` before commit catches em/en dashes and strict list matches.

**Flashcards boundary:** flashcards skill owns cue→apply structure and card count. garden-voice owns word choice. Don't turn a life cue into a "What is X?" definition card.

## De-AI pass (mandatory)

Even on a one-line `relationships.reason` fix. For each field ask:

1. Could this appear in any generic note about this topic? → add a specific detail or personal angle.
2. Is this saying something or just sounding like it's saying something? → cut or replace with a concrete claim.
3. Would JoRap actually type this? → simplify the words; add "I" in glosses and examples where natural.
4. Any word you'd pause to define? → swap for the plain word you'd say out loud.
5. `key_concept` line 1 - is it a claim you'd argue, with no wikilinks?
6. `shareable_thought` - four complete thoughts, four different angles?

If a field still feels generated, rewrite from one real scene - don't polish AI slop.

## Voice check

- [ ] `title` is 4 words preferred (5 only at ≥30 chars, phrase exempt, beats best 4-word trim; never 6+)
- [ ] `description` is third-person, one breath, ≤20 words, no `[[wikilinks]]`
- [ ] `key_concept` line 1 is a plain claim you'd argue - **no wikilinks**
- [ ] `key_concept` has 2-4 tight sentences before the link stack runs long
- [ ] Faith note includes a Bible verse in `key_concept` (skip when `Workplace` tag - workplace lane)
- [ ] EP scripture: `{{< bible >}}` shortcode, explanation bullet in JoRap voice, then claim stack
- [ ] Two `examples`, one sentence each, scenes feel different
- [ ] `shareable_thought` is exactly four complete thoughts, four different angles - no fragments
- [ ] `relationships.reason` is a clause, not a paragraph
- [ ] Cards pass [flashcards](../flashcards/SKILL.md) and plain-words test
- [ ] Theology/PKM term glossed in plain English before the wikilink stack
- [ ] No contractions in frontmatter (body/cards OK)
- [ ] `pnpm lint:voice` clean (dashes + AI-tell words)

## Do not

- Commit or push unless the user explicitly asks
- Use emoji in note frontmatter
- Use em dashes; use a normal hyphen (-), comma, or parentheses instead
- Open `key_concept` with "X is the process whereby…"
- Put wikilinks on line 1 of `key_concept`
- Write `shareable_thought` fragments or four near-duplicates
- Force Philippines/local color when the scene isn't local
