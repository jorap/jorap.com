---
name: jorap-voice
description: >-
  Write and edit JoRap blog posts in the author's personal voice. Use plain words
  that land on first read.
  Use when drafting, outlining, rewriting, or polishing blog content under
  content/english/blog/, writing blog meta_title and description, matching JoRap's
  writing style, or when posts sound generic, SEO-ish, stiff, or AI-generated.
  For notes garden frontmatter, use garden-voice instead.
---

# JoRap Voice (Blog)

Keep blog posts sounding like JoRap wrote them - practical, personal, and plain-spoken - not like a content mill, a product listing, or ChatGPT with a thesaurus. **Vocabulary:** plain words only. Every word should land on first read.

**Primary test:** Would a reader think a real person typed this after using the thing? If it reads like a summary of what a good post *should* say, rewrite it.

**Notes garden** (`description`, `key_concept`, `examples`, `shareable_thought`, EP scripture) uses [garden-voice](../garden-voice/SKILL.md), not this skill.

## When to use

- Creating or expanding a blog post from an outline
- Rewriting AI-generated or stiff drafts under `content/english/blog/`
- Editing blog tone without changing facts
- Writing blog `meta_title` and `description`
- Recipe posts (instructional body + human section intros)

## Workflow

1. **Read 1-2 reference posts** in the same category before writing:
   - **Gear / reviews:** `content/english/blog/what-i-look-for-in-wireless-earphones.md`
   - **Tech / how-to:** `content/english/blog/how-i-built-jorap-notes.md`
   - **Tips:** `content/english/blog/power-of-the-mouse-wheel-click.md`
   - **Opinion:** `content/english/blog/why-i-stopped-playing-marvel-snap.md`
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
| **Skill beats lint on new drafts** | This skill and [examples.md](examples.md) are stricter than `data/voice-words.yaml`. Lint may allow words you still should not write fresh. |
| **Say it out loud** | If you wouldn't say it to a friend mid-rush, swap for the plain word |
| **Topic terms OK** | Gear names, tool names (Hugo, Cloudflare) - explain in plain English nearby |
| **Contractions** | Fine in blog body (`it's`, `don't`, `I've`) - most of the time |

Edit `data/voice-words.yaml` for words and phrases you wouldn't say out loud. Run `pnpm voice:scan` to review the whole site grouped by hit; `pnpm lint:voice` before commit catches em/en dashes and strict list matches.

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

- `description`: memorable one-breath summary - what the post is or what you learned; first person is fine. Not keyword-stuffed.
- `meta_title`: useful and specific - not clickbait, not "Ultimate Guide to…" unless the post truly is a full guide.

## Gear and reviews

No affiliate links on the site as of now. Named products you own, what you paid, what ended up in a drawer, and "I'd buy again" are all fine. Skip affiliate-marketing tone - no "game-changer", no "must-have", no breathless superlatives.

## Recipe posts (variant)

Recipe content can be more instructional - ingredients, steps, timings - but section intros should still sound human. Avoid generic food-blog filler ("This delicious recipe will tantalize your taste buds"). Keep the "why this method" parts in JoRap voice; keep the method itself scannable.

## Voice check

- [ ] Opens with experience or a concrete problem, not a generic intro
- [ ] Uses "I" and real scenarios, not "users" and "one might"
- [ ] At least one specific detail per section (number, name, place, mistake, price)
- [ ] States opinions clearly - no endless "it depends" without a take
- [ ] Plain words only - no jargon or thesaurus words you wouldn't say out loud
- [ ] Read aloud - no word you'd pause to define
- [ ] No AI-slop phrases (see `data/voice-words.yaml` phrases + examples.md)
- [ ] Sentence lengths vary - not a wall of same-shaped paragraphs
- [ ] Section headings sound like JoRap, not a product manual
- [ ] Would sound natural read aloud by a person, not narrated by a help article
- [ ] Frontmatter description sounds like the author, not an SEO bot
- [ ] Passes the swap test: couldn't paste this into a random tech blog without it feeling off
- [ ] `pnpm lint:voice` clean (dashes + AI-tell words)

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
