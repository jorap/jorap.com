---
name: jorap-voice
description: >-
  Write and edit JoRap blog posts and notes garden prose in the author's personal
  voice. Use plain words that land on first read.
  Use when drafting, outlining, rewriting, or polishing blog content under
  content/, notes frontmatter (description, key_concept, examples, relationship
  reasons), flashcard fronts and backs on content/english/notes (with flashcards
  skill), when the user asks to match their writing style, sound more human, or
  when posts sound generic, SEO-ish, stiff, or AI-generated.
---

# JoRap Voice

Keep blog posts sounding like JoRap wrote them - practical, personal, and plain-spoken - not like a content mill, a product listing, or ChatGPT with a thesaurus. **Vocabulary:** plain words only. Every word should land on first read.

**Primary test:** Would a reader think a real person typed this after using the thing? If it reads like a summary of what a good post *should* say, rewrite it.

## When to use

- Creating or expanding a post from an outline
- Rewriting AI-generated or stiff drafts
- Editing for tone without changing facts
- Writing `meta_title` and `description` frontmatter
- **Notes garden** - `description`, `key_concept`, `examples`, `relationships.reason` on `content/english/notes/`
- **Flashcards** - cue fronts and apply backs on spine notes (use with [flashcards](../flashcards/SKILL.md); flashcards skill wins on shape, jorap-voice wins on word choice)

## Workflow

1. **Read 1-2 reference pieces** in the same category before writing. Good defaults:
   - Gear/reviews: `content/english/blog/what-i-look-for-in-wireless-earphones.md`
   - Tech/how-to: `content/english/blog/how-i-built-jorap-notes.md`
   - Tips: `content/english/blog/facebooks-hidden-gem-how-favorites-feed-transforms-your-social-media-experience.md`
   - Opinion: `content/english/blog/top-reasons-why-you-still-need-use-desktop-laptop.md`
   - **Notes - PKM:** `content/english/notes/capture.md`, `progressive-layers.md`
   - **Notes - faith:** `content/english/notes/free-grace.md`, `sanctification.md`
   - **Notes - ethics/systems:** `content/english/notes/the-golden-rule.md`, `blameless-after-action-review.md`
   - **Flashcards:** `capture.md`, `free-grace.md`, `the-golden-rule.md`
2. **Draft in the author's voice**, not a generic blogger voice.
3. **Run the de-AI pass** (below) - mandatory, even on small edits.
4. **Run the voice check** (below) before finishing.
5. For before/after samples and anti-patterns, see [examples.md](examples.md).

## Voice pillars

| Pillar | What it means |
|--------|----------------|
| **Experiential** | Write from lived use - drawers full of failed gear, weekends lost to themes, borrowed laptops for taxes. |
| **Opinionated** | State preferences plainly. "I want buttons. Real ones." Not "some users may prefer physical controls." |
| **Practical** | Lead with what matters day to day. Cut specs, marketing fluff, and features nobody actually uses. |
| **Honest** | Include what broke, what you'd skip, what ended up in a drawer. Credibility beats polish. |
| **Grounded** | Real context - family, commute, home office, Philippines (Shopee, jeepney, local sellers) when relevant. Not forced, just natural. |
| **Understated humor** | Dry asides, not jokes-for-the-sake-of-jokes. "The most boring possible reason to spend an hour debugging." |
| **Plain words** | No college jargon, no thesaurus swaps. If a simpler word works, use it. |

## Vocabulary

Plain speech beats smart-sounding prose. Every word should land on first pass.

| Rule | Detail |
|------|--------|
| **Everyday default** | Plain words first - but see `data/voice-words.yaml` for what lint actually flags |
| **Say it out loud** | If you wouldn't say it to a friend mid-rush, swap for the plain word |
| **Topic terms OK** | See decision tree below - gear names, tool names, theology/PKM terms when they're the subject |
| **Gloss once** | First use of a theology or PKM term: plain English in the same breath, then the term |

### Topic terms - when jargon is OK

| Lane | Where | Rule |
|------|-------|------|
| **Faith** | `key_concept`, `description` | Theology terms OK after a plain gloss: "declared right with God - justification" |
| **PKM** | `key_concept`, `description` | Plain verbs when you can; PKM terms OK when the note is *about* the term |
| **Tools** | blog body, tech notes | Product names OK (Hugo, Cloudflare) - still explain in plain English nearby |
| **Cards** | `cards.front` / `cards.back` | Plainest layer. Term on the back only if it *is* the immediate move |

### Common swaps (garden)

| Instead of | Say |
|------------|-----|
| `unmerited favor` | gift you didn't earn (then "unmerited favor" if needed) |
| `distill` | boil down / shorten |
| `deploy` | push live |
| `metadata` | tags and fields |
| `contradicts` (in relationship reasons) | goes against |

Hard bans live in `data/voice-words.yaml` - not every row above is linted.

### Scripture quotes

**Eternal Principles** notes anchor on **Jesus' words** (Matthew, Mark, Luke, John) in **NASB 1995**. Open `key_concept` with the Jesus quote and reference; Paul and other writers may follow as expansion, not as the primary anchor. Commentary and paraphrase stay JoRap voice. Canonical wording lives in `data/scripture-nasb1995.json`. Run `python3 scripts/apply-jesus-quotes.py` after bulk edits to spot-check spine notes.

After each scripture line in EP `key_concept`, add a **plain-language gloss** in JoRap voice on the next line (blank line between verse and gloss). Glosses live in `data/ep-verse-explanations.yaml`. Run `python3 scripts/apply-verse-explanations.py` after bulk edits.

Each verse is its **own paragraph** with the **full NASB 1995 text** and citation suffix. On the site, verse paragraphs render on their **own line, right-aligned**; glosses and commentary stay left-aligned. Gospel quotes (Matthew, Mark, Luke, John) render **red** automatically — Paul and other writers stay default ink.

```
  [Full NASB 1995 verse text] Ref NASB1995

  [1-2 sentence gloss - plain words, first person where natural]

  [Commentary, wikilinks, cross-refs...]
```

Frontmatter shape is unchanged: one verse per paragraph block, blank line before the gloss. Hugo adds `scripture-verse` at build time — do not hand-write HTML in notes.

Run `python3 scripts/normalize-verse-paragraphs.py` after bulk edits to pull canonical wording from `data/scripture-nasb1995.json` and split inline refs into standalone verse paragraphs.

When quoting Bible **text** elsewhere in the garden, use **NASB 1995** wording. Run `python3 scripts/apply-nasb-quotes.py` for paraphrase migrations.

**Vocab test:** Read a paragraph aloud. Any word you'd pause to define? Replace it before finishing.

Edit `data/voice-words.yaml` for words and phrases you wouldn't say out loud. Run `pnpm voice:scan` to review the whole site grouped by hit; `pnpm lint:voice` before commit catches em/en dashes and strict list matches.

See [examples.md](examples.md) for vocabulary swaps, garden samples, and anti-patterns.

## Sound human, not AI

AI writing is smooth, balanced, and empty. JoRap writing is specific, uneven, and earned.

### Human markers - include these

- **Specifics**: prices ($30-$60), durations (90 minutes, 10 minutes under pressure), model names, exact failures ("third batch of chicken steamed instead of seared").
- **Contractions**: it's, don't, I've, won't, that's - most of the time.
- **Sentence variety**: one-word sentences. Short punches. Then a longer sentence that actually explains something.
- **Imperfect rhythm**: not every paragraph needs three sentences. Not every section needs the same shape.
- **A real take**: end sections with what *you* do, not what "one should consider."
- **Lived friction**: what annoyed you, what you got wrong, what you'd skip next time.

### AI tells - remove these

- **Hollow openers**: "When it comes to…", "In the world of…", "X has become increasingly important…"
- **Significance inflation**: "plays a key role", "it's important to remember" - unless something is actually life-or-death, dial it down.
- **Transition spam**: Furthermore, Additionally, Moreover, That said, With that in mind - cut most of them. Start the next thought.
- **Parallelism disease**: three bullets that all start with "Ensures…" / "Provides…" / "Delivers…" - rewrite as plain speech.
- **Summary sandwiches**: don't announce what you'll say, say it, then restate it. Say it once, well.
- **Fake balance**: "While X has benefits, Y also has drawbacks" on every point - pick a side when you have one.
- **Abstract nouns**: "functionality", "utilization", "optimization" → what does it actually *do*?
- **No subject**: "It is recommended to…" → "I'd get…" / "Skip…"
- **Thesaurus voice**: delve, tapestry, harness - plus hollow phrase patterns in `data/voice-words.yaml`.
- **Over-polish**: if every sentence is grammatically perfect and emotionally flat, roughen one or two.

### De-AI pass (mandatory)

Read the draft aloud (or simulate it). For each paragraph ask:

1. Could this appear in any generic blog post about this topic? → add a specific detail or personal angle.
2. Is this saying something or just sounding like it's saying something? → cut or replace with a concrete claim.
3. Would JoRap actually type this sentence? → if not, simplify the words and add "I".
4. Any word you'd pause to define? → swap for the plain word you'd say out loud.

If a section still feels generated, rewrite it from scratch using one real memory or opinion - don't polish AI slop.

## Tone

- **First person**: "I", "my", "what I look for" - this is a personal site, not a brand blog.
- **Direct address** when giving advice: "Be honest with yourself before you start."
- **Conversational but edited** - sounds like someone talking, but sentences are tight. No filler paragraphs.
- **Confident, not preachy** - share what works for you; don't lecture.

## Structure patterns

### Opening

Hook with a relatable situation, frustration, or small story - not a dictionary definition or "In today's world…"

Good patterns:
- Personal history that narrows to the point ("I've been through a lot of wireless earphones…")
- A problem everyone recognizes ("Every couple of years someone tells me they're going mobile-only…")
- A near-miss or turning point ("I almost deleted Facebook…")

### Body

- Use `---` between major sections on longer posts.
- **H2 headings with personality** - "All-day comfort, not 'good for an hour'" not "Comfort Considerations".
- Mix short punchy sentences with longer explanatory ones.
- Numbered lists for checklists; prose for arguments and stories.
- **Bold** for the one phrase that carries the section's point.

### Closing

Land on what you actually use, what you'd buy again, or a plain recommendation. No "happy reading" or "hope this helps."

### Frontmatter

- `description`: memorable one-breath **definition** - what the concept is or does; you should recall it cold weeks later. First person is fine when it states the claim plainly. Not keyword-stuffed, no `[[wikilinks]]`.
- `meta_title`: useful and specific - not clickbait, not "Ultimate Guide to…" unless the post truly is a full guide.

## Notes garden (variant)

Notes use **two registers**. Wiki prose can be denser; cards must stay plain.

| Field | Voice | Pattern |
|-------|-------|---------|
| `description` | Memorable definition, one breath | "Eternal life is Christ's gift by faith alone - not wages for good works." / "Save what resonates into one inbox - then empty it weekly." |
| `key_concept` | Punch line, then expansion with wikilinks | Line 1: short claim. Blank line. Then lanes, links, "first X, then Y" |
| `examples` | Two scenes, different domains, same move | Sports + jeepney, deploy + kitchen, coffee + sideline - not two variants of one scene |
| `shareable_thought` | Four self-contained ideas from `description` + `key_concept` | Each item is a complete thought a reader understands alone - paste-ready for Slack or slides. No fragments, cross-note pointers, examples, or wikilinks |
| `relationships.reason` | Short clause, telegraphic OK | "Rollback first; after-action review after calm - not root-cause while users are down" |
| `cards` | Plainest layer - see [flashcards](../flashcards/SKILL.md) | Cue → apply. No definition backs, no truncated fragments |

**Reference notes by type:** PKM `capture.md`; faith `free-grace.md`, `sanctification.md`; ethics `the-golden-rule.md`; systems `blameless-after-action-review.md`.

**Flashcards boundary:** flashcards skill owns cue→apply structure and card count. jorap-voice owns word choice. Don't turn a good life cue into a "What is X?" definition card.

### `key_concept` shape

```
[[Free Grace]] settles where I spend forever.

Sanctification settles who I'm becoming on the way. [[Grateful Obedience]] names the posture: grow from thanks, not to earn acceptance.
```

Not: "Sanctification is the process whereby believers undergo moral transformation…"

### `title` (notes)

**4 words.** A 5th word is allowed only when `len(title) ≥ 30` (letters, spaces, punctuation), the line is a **fixed phrase or scripture quote**, and the 5-word title beats the best 4-word option you can write. Otherwise trim.

Examples: `Golden Rule at Work` (4); `Integrity Without an Audience` (4); `Let Your Yes Be Yes` (5 — Matthew 5:37, phrase exempt); `There Is No Perfect Solution` (5 — stable slug, phrase exempt).

### `meta_title` (notes)

`Topic - Plain subtitle` - e.g. `Sanctification - Becoming Holy After Faith`. Not dictionary labels alone.

## Recipe posts (variant)

Recipe content can be more instructional - ingredients, steps, timings - but section intros should still sound human. Avoid generic food-blog filler ("This delicious recipe will tantalize your taste buds"). Keep the "why this method" parts in JoRap voice; keep the method itself scannable.

## Voice check

### Notes garden

- [ ] `title` is 4 words (5 only at ≥30 chars, phrase exempt, beats best 4-word trim)
- [ ] `description` reads in one breath — memorable definition, ≤20 words, no `[[wikilinks]]`
- [ ] `key_concept` opens with a punch, not a dictionary definition
- [ ] Two `examples` from different life surfaces (not two tweaks of one scene)
- [ ] `shareable_thought` are four self-contained ideas from `description` and `key_concept` - each gets the point across alone; no fragments, duplicates, cross-note pointers, examples, or "Tension with…"
- [ ] `relationships.reason` is a clause, not a paragraph
- [ ] Cards pass [flashcards](../flashcards/SKILL.md) *and* plain-words test - no definition backs, no fragments
- [ ] Theology/PKM term glossed in plain English before the wikilink stack
- [ ] EP scripture: each NASB verse is its own `key_concept` paragraph; gloss on the next line (site renders verses right-aligned — no HTML in frontmatter)
- [ ] `pnpm lint:voice` clean (dashes + AI-tell words)

### Blog posts

Before finishing, verify:

- [ ] Opens with experience or a concrete problem, not a generic intro
- [ ] Uses "I" and real scenarios, not "users" and "one might"
- [ ] At least one specific detail per section (number, name, place, mistake, price)
- [ ] States opinions clearly - no endless "it depends" without a take
- [ ] Plain words only - no jargon or thesaurus words you wouldn't say out loud
- [ ] Read aloud - no word you'd pause to define
- [ ] No AI-slop phrases or thesaurus words (see examples.md)
- [ ] No AI-slop phrases (see `data/voice-words.yaml` phrases + examples.md)
- [ ] Sentence lengths vary - not a wall of same-shaped paragraphs
- [ ] Section headings sound like JoRap, not a product manual
- [ ] Would sound natural read aloud by a person, not narrated by a help article
- [ ] Frontmatter description sounds like the author, not an SEO bot
- [ ] Passes the swap test: couldn't paste this into a random tech blog without it feeling off

## Do not

- Add engagement bait ("Let me know in the comments!", "What do you think?")
- Pad with obvious filler or restate the heading in the first sentence
- Use emoji in post body
- Use em dashes; use a normal hyphen (-), comma, or parentheses instead
- Over-hedge every claim ("might potentially perhaps")
- Write listicle intros that promise "10 game-changing tips"
- Turn personal gear picks into affiliate-marketing tone

## Expanding outlines

When a post is only an outline (see `__extension-cord.md`, `__wifi-router.md`):

1. Keep the outline's intent and section order.
2. Write each section as prose-first - not bullet dumps unless it's a genuine checklist.
3. Add the personal thread: why this topic, what you learned, what you'd tell a friend.
4. Preserve Hugo frontmatter; set `draft: true` until the user publishes.
5. **Draft filenames** use a `__` prefix (e.g. `__wifi-router.md`) so drafts sort apart in the file tree. Set `slug` to the publish name without the prefix (e.g. `slug: "wifi-router"`). To publish: drop the `__` prefix from the filename, set `draft: false`, and remove the `slug` line if it matches the filename.
