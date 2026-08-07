---
name: jorap-voice
description: >-
  Write and edit JoRap blog posts in the author's personal voice. Use plain words
  that land on first read.
  Use when drafting, outlining, rewriting, or polishing blog content under
  content/english/blog/, writing blog meta_title, description, image_prompt, and
  social_media_intro, matching JoRap's writing style, or when posts sound generic,
  SEO-ish, stiff, or AI-generated.
  Runs seven rewrite passes (lived-in, de-AI, thinking, friend-flow, POV, credible,
  editor) plus likability and connection lenses before publish. Posts always open and close
  from an attitude of gratitude (understated, earned - not performative thanks). Craft backbone: Zinsser
  On Writing Well (zinsser.md) and Writing to Learn (writing-to-learn.md). Read author-context.md
  and the facts ledger before personal posts. For notes garden frontmatter, use garden-voice instead.
---

# JoRap Voice (Blog)

Keep blog posts sounding like JoRap wrote them - practical, personal, and plain-spoken - not like a content mill, a product listing, or ChatGPT with a thesaurus. **Vocabulary:** plain words only. Every word should land on first read.

**Primary test:** Would a reader think a real person typed this after using the thing? If it reads like a summary of what a good post *should* say, rewrite it.

**Craft backbone:** William Zinsser — *On Writing Well* for sentence craft ([zinsser.md](zinsser.md)); *Writing to Learn* for drafting and reasoning ([writing-to-learn.md](writing-to-learn.md)). OWW: clarity, clutter, unity, lead/ending. WTL: writing as thinking, Type A/B drafts, fuzzy-thinking fixes, linear narrative. This skill handles JoRap's person, scene, and connection.

**Notes garden** (`description`, `key_concept`, `examples`, `shareable_thought`, EP scripture) uses [garden-voice](../garden-voice/SKILL.md), not this skill. See garden-voice **When to use which** for how these seven passes map to per-field garden work.

**Author context** - who JoRap is in the archive (family, stack, gear, gaps). See [author-context.md](author-context.md). Canonical ledger: `content/english/blog/__interesting-facts-about-jorap.md` (always draft; never publish). Read before posts that touch personal facts; don't contradict the ledger or invent unmapped pop-culture/sports picks. On archive reviews or new personal facts, update the ledger and sync `author-context.md` quick anchors.

## When to use

- **New post from a topic or notes** — start with [ai-writing-system](../ai-writing-system/SKILL.md) (interview → framework → draft), then run this skill on the draft
- Creating or expanding a blog post from an outline
- Rewriting AI-generated or stiff drafts under `content/english/blog/`
- Editing blog tone without changing facts
- Writing blog `meta_title`, `description`, `image_prompt`, and `social_media_intro`
- Recipe posts (instructional body + human section intros) — read [recipe-style.md](recipe-style.md)

## Workflow

1. **Read [author-context.md](author-context.md)** and skim the relevant sections of `content/english/blog/__interesting-facts-about-jorap.md` when the post might mention family, faith, Philippines context, gear, work stack, games, or worship. Match ledger facts; don't invent gap-table topics.
2. **Read 1-2 reference posts** in the same category before writing:
   - **Gear / reviews:** `content/english/blog/what-i-look-for-in-wireless-earphones.md`
   - **Tech / how-to:** `content/english/blog/how-i-built-jorap-notes.md`
   - **Tips:** `content/english/blog/mouse-wheel-click.md`
   - **Opinion:** `content/english/blog/why-i-stopped-playing-marvel-snap.md`
3. **Draft in the author's voice**, not a generic blogger voice.
4. **Score before and after** — `pnpm slop:score path/to/draft.md` before passes; rerun after. The per100w score should drop.
5. **Run the seven rewrite passes** (below) - mandatory, even on small edits. Skim all seven on every edit; deep-rewrite any section that fails more than one pass.
6. **Run the likability lens** (below) - mandatory before publish.
7. **Run the connection lens** (below) - mandatory before publish.
8. **Run the voice check** (below) before finishing.
9. On full rewrites or outline expansion, skim [writing-to-learn.md](writing-to-learn.md) (Type B → Type A, reasoning visible) then [zinsser.md](zinsser.md) — bracket test, unity, lead/ending, read aloud.
10. For before/after samples and anti-patterns, see [examples.md](examples.md).

## Voice pillars

| Pillar | What it means |
|--------|----------------|
| **Experiential** | Write from lived use - drawers full of failed gear, weekends lost to themes, borrowed laptops for taxes. |
| **Opinionated** | State preferences plainly. "I want buttons. Real ones." Not "some users may prefer physical controls." |
| **Practical** | Lead with what matters day to day. Cut specs, marketing fluff, and features nobody actually uses. |
| **Honest** | Include what broke, what you'd skip, what ended up in a drawer. Credibility beats polish. |
| **Reflective** | Show how you actually thought it through - tradeoffs you weighed, the option you almost picked, what you're still watching. Then land the take. |
| **Grounded** | Real context - family, commute, home office, Philippines (Shopee, jeepney, local sellers) when relevant. Not forced, just natural. |
| **Understated humor** | Dry asides, not jokes-for-the-sake-of-jokes. "The most boring possible reason to spend an hour debugging." |
| **Grateful** | Open and close from thanks - for what worked, who helped, what you still have, or the lesson the mess taught. Attitude, not a thank-you banner. |
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

- **Specifics**: durations (90 minutes, 10 minutes under pressure), model names, exact failures ("third batch of chicken steamed instead of seared"). No currency amounts - say "budget tier" or "cheap" instead of dollar figures.
- **Contractions**: it's, don't, I've, won't, that's - most of the time.
- **Sentence variety**: one-word sentences. Short punches. Then a longer sentence that actually explains something.
- **Imperfect rhythm**: not every paragraph needs three sentences. Not every section needs the same shape.
- **A real take**: end sections with what *you* do, not what "one should consider."
- **Lived friction**: what annoyed you, what you got wrong, what you'd skip next time.
- **Visible thinking**: the near-miss ("I almost bought the outdoor-rated one for indoor use"), the tradeoff you accepted, one small observation that tipped you - not endless hedging.

## Seven rewrite passes

One read of the draft per pass. On a full rewrite, run all seven in order. On a light polish, at minimum run **#2 Strip the AI Tells**, **#5 Sharper Point of View**, and **#7 Top-Editor Pass**.

### 1. Lived-In Voice

Rewrite from someone who has actually done the work. Cut generic advice, corporate phrasing, and unnecessary adjectives. Swap in specific observations, hard-won lessons, and real details. Keep the tone relaxed and conversational.

- Could this paragraph appear in any buying guide? Add a memory, a mistake, or what you actually do.
- Generic "check the label" → the time the cord ran warm on a 25-foot run.

### 2. Strip the AI Tells

Remove every sign of AI writing. Kill repetitive sentence shapes, predictable transitions, filler, and over-explaining. Vary sentence length so it reads spontaneous.

See **AI tells** below. If a section still feels generated after this pass, rewrite it from one real memory - don't polish slop.

### 3. Show the Thinking

Reveal how a real person works through the topic. Add tradeoffs, second-guesses, small observations, and open questions where they fit. Make it feel reflective, not committee-polished. (WTL: fuzzy thinking is the enemy; writing should show how you got to the answer, not only the answer.)

- Name what you almost did, what you ruled out, or what you're still unsure about - then say what you picked anyway.
- One honest doubt per post is enough. Don't hedge every sentence into mush.
- A section that explains why you *couldn't* solve it yet beats faking certainty.

### 4. One-Friend Flow

Rewrite as if you're explaining it to one sharp friend. Plain language, mixed short and long sentences, smooth transitions. Clarity and connection over formality.

- Read aloud. Would you actually say this mid-rush?
- Cut corporate phrasing and words you'd pause to define. Contractions are fine.

### 5. Sharper Point of View

Rewrite with a clearer opinion. Add conviction, personality, and plain expressive language. Drop the neutral, corporate, committee-approved tone.

- "Some users may prefer…" → "I want…" / "Skip…"
- Fake balance on every point → pick a side when you have one.
- Recognizable voice beats perfect writing. Small imperfections are fine - personality over polish.

### 6. Make It Credible

Every line should feel grounded and real. Read as a skeptical reader - flag anything exaggerated, generic, overly certain, or written to sound smart. Replace vague claims with concrete details, examples, and practical explanations a reader would actually believe.

- Add at least one specific per section: number, name, place, failure - not currency.
- "Good battery life" → "still had juice after a full workday and a grocery run."

### 7. Top-Editor Pass

Edit like a great editor prepping to publish. Sharpen clarity, flow, and pull. Cut anything generic or artificial. Protect the core message.

JoRap editor bias: **roughen** over-polish, don't smooth into a help article. Cut summary sandwiches and symmetrical nothingburgers (Zinsser: when you're ready to stop, stop — no "In sum…" cranking). Land the closing on what you'd buy again or actually do - not "hope this helps."

### AI tells - remove these

- **Hollow openers**: "When it comes to…", "In the world of…", "X has become increasingly important…"
- **Significance inflation**: "plays a key role", "it's important to remember" - unless something is actually life-or-death, dial it down.
- **Written to impress**: sentences that sound smart but say little - cut the adjectives and land the claim.
- **Transition spam**: Furthermore, Additionally, Moreover, That said, With that in mind - cut most of them. Start the next thought.
- **Parallelism disease**: three bullets that all start with "Ensures…" / "Provides…" / "Delivers…" - rewrite as plain speech.
- **Summary sandwiches**: don't announce what you'll say, say it, then restate it. Say it once, well.
- **Fake balance**: "While X has benefits, Y also has drawbacks" on every point - pick a side when you have one.
- **Abstract nouns**: "functionality", "utilization", "optimization" → what does it actually *do*?
- **No subject**: "It is recommended to…" → "I'd get…" / "Skip…"
- **Thesaurus voice**: delve, tapestry, harness - plus hollow phrase patterns in `data/voice-words.yaml`.
- **Over-polish**: if every sentence is grammatically perfect and emotionally flat, roughen one or two.

### Quick de-AI check

After the seven passes, one final skim. For each paragraph:

1. Could this appear in any generic blog post about this topic? → pass #1 or #6.
2. Is this saying something or just sounding like it's saying something? → cut or replace with a concrete claim.
3. Would JoRap actually type this sentence? → pass #4 or #5.
4. Any word you'd pause to define? → swap for the plain word you'd say out loud.

## Likability lens (reserved person, likable page)

JoRap in person can be reserved. On the page, likable does not mean nice or performative warmth. It means **useful, honest, human, and respectful** - competence with the door open.

| Pillar | Reader feels… | You write… |
|--------|----------------|------------|
| **Useful** | "That saved me a click." | A real pick or takeaway - early enough to matter |
| **Honest** | "They're not selling me." | What broke, what you'd skip, what wasn't easy |
| **Human** | "A person typed this." | One scene, mistake, or dry observation per major unit |
| **Respectful** | "They didn't talk down to me." | Plain words, no lecture, no fake hype |

Run after the seven passes (or after #2, #5, #7 on a light polish). Not every paragraph needs all four; the **post** should.

**Quick check:**

1. Did they get a **useful** takeaway?
2. Did I admit at least one **honest** friction?
3. Is there one **human** specific (name, place, failure, duration)?
4. Would I **respect** a friend's time if I sent them this?

If yes to all four, you're in the zone - even when the tone stays cool and direct. Notes garden uses the same four pillars mapped to fields - see [garden-voice](../garden-voice/SKILL.md) **Likability lens**.

## Connecting with readers

Everyone can *communicate* (publish words). Few posts *connect* (reader feels seen, helped, and willing to trust the take). JoRap voice aims for connection, not coverage. Frame from John Maxwell's *Everyone Communicates, Few Connect*: influence follows connection; connection is mostly skill, not charisma.

**Reader lens (before you write):** Ask what they are silently checking:

| They wonder… | JoRap answer on the page |
|--------------|---------------------------|
| Do you care about me? | Open on *their* friction, not your credentials. Ask yourself: "What brought them here?" |
| Can you help me? | Useful takeaway early - a pick, a skip, a step - not a tour of everything you know |
| Can I trust you? | Honest friction + lived specifics. Don't posture expertise you haven't earned |

**Five principles → writing moves**

| Principle | On the page |
|-----------|-------------|
| **It's about them** | First 400 characters serve the reader's problem, not your bio or a topic definition |
| **Beyond words** | Pair the claim with something felt or done - annoyance, mistake, duration, place (passes #1, #3, #6) |
| **Energy** | You own their attention: hook hard, cut coasting, end before you wear out your welcome |
| **Common ground** | Start where they already are (drawer full of dead earphones, Hugo version mismatch) before the lesson |
| **Live it** | Only recommend what you'd buy again; admit what landed in the drawer (credibility over polish) |

**Five practices → draft checklist**

1. **Common ground** - Could this open on any blog? Add a scene only you lived.
2. **Keep it simple** - One main point per section; plain words; say it once (no summary sandwich).
3. **Make it an experience** - Vary rhythm; one dry aside; responsibility for boredom is yours, not theirs.
4. **Inspire action** - Close on what *they* would do Monday, not what you admire in theory.
5. **Align words and life** - If you wouldn't follow your own advice, soften the claim or add the caveat.

**Connection vs communication (quick test)**

- **Communicates:** "Here are ten things to consider when choosing extension cords."
- **Connects:** "I grabbed the indoor cord for the patio run once. Rain taught me the rest."

Run this after the likability lens. If the post informs but doesn't connect, rewrite the opening and closing first - those two places carry most of the bond.

## Slop gate (structural)

Vocabulary is `pnpm lint:voice` (`data/voice-words.yaml`). Structure is `pnpm lint:slop` (`data/slop-rules.yaml`). Mechanical form is `pnpm slop:score` (nominalizations, passive voice, phrasal verbs, long-sentence ratio — lower per100w is cleaner). Run all three before `draft: false`.

**Publish blockers** - CI fails if any of these ship:
- `Expanded from` / `Idea captured from ideas.jorap.com` footer still in body
- `image-template.jpg` as hero image
- Body under 80 words
- `users should` / `it is recommended` in prose

**Warn before publish** - fix when you can:
- `## Bottom line` (especially on opinion, faith, family, games posts)
- `## Further reading` with 3+ links
- Three parallel bullets sharing the same first word
- Empty `##` sections with no body
- Opinion/faith/family/games posts with no `I`/`my` in the first 400 characters

**Wiki exports:** posts expanded from ideas.jorap.com are outlines until each section has one real scene (date, place, mistake, name). Delete the footer after rewrite.

**Swap test (mandatory):** could this paragraph run on any blog about this topic? Rewrite until no.

**One failure rule:** every H2 section needs something that went wrong, surprised you, or you'd skip next time.

## Tone

- **First person**: "I", "my", "what I look for" - this is a personal site, not a brand blog.
- **Direct address** when giving advice: "Be honest with yourself before you start."
- **Conversational but edited** - sounds like someone talking, but sentences are tight. No filler paragraphs.
- **Confident, not preachy** - share what works for you; don't lecture.
- **Attitude of gratitude** - every post **starts and ends** from thanks. Friction hooks are fine; entitlement and complaint-only openers are not. Close the same way: appreciate what earned its keep, who tipped you, or what the failure taught. Quiet and specific - never a curtain-call thank-you.

## Structure patterns

### Opening

Hook with a relatable situation, frustration, or small story - not a dictionary definition or "In today's world…" **and** land the first beat in gratitude (even when the scene is messy).

Good patterns:
- Personal history that narrows to the point ("I've been through a lot of wireless earphones…")
- A problem everyone recognizes ("Every couple of years someone tells me they're going mobile-only…")
- A near-miss or turning point ("I almost deleted Facebook…")
- Grateful frame inside the hook ("I'm glad I kept the boring pair - the flashy ones died in a drawer.")

Gratitude here means posture: glad something still works, glad you learned, glad someone helped. Not "I'm so grateful for the opportunity to share…"

### Body

- Use `---` between major sections on longer posts.
- **H2 headings with personality** - "All-day comfort, not 'good for an hour'" not "Comfort Considerations".
- Mix short punchy sentences with longer explanatory ones.
- Numbered lists for checklists; prose for arguments and stories.
- **Bold** for the one phrase that carries the section's point.

### Closing

Land on what you actually use, what you'd buy again, or a plain recommendation - **and** end from gratitude for that pick, lesson, or person. No "happy reading", "hope this helps", or "thanks for reading".

### Frontmatter

Field order (always use this order; `pnpm lint:blog` enforces it):

1. `title`, `meta_title`, `description`, `social_media_intro`, `slug`, `date`, `image`, `image_prompt`
2. `categories`, `author`, `tags`, `related_notes` (when used)
3. `level_depth` (required: integer 1–5)
4. `aliases`, `lastmod` (only when needed)
5. `featured`, `draft`

- `description`: memorable one-breath summary - what the post is or what you learned; first person is fine. Not keyword-stuffed.
- `meta_title`: useful and specific - not clickbait, not "Ultimate Guide to…" unless the post truly is a full guide.
- `social_media_intro`: max **200 characters**. Paste-ready social caption whose job is to get someone to open the comments and click through to the article on jorap.com. Same voice as the post: specific, uneven, human. Not a summary of the article. Not engagement bait.
  - **Shape (pro social playbook):** **hook → payoff → CTA**. Line 1 stops the scroll (scene, friction, sharp take). Mid names what they get if they click (checklist, fix, skip, story beat). End is a dull, loud destination line - logistics after desire, never before.
  - **Preferred closers** (pick one; keep plain): `Full article in the comments.` / `Article in the comments.` / `Write-up in the first comment.` / `Checklist in the comments.` Also fine: `post linked in comments`, `full article - link in comments`.
  - **Must make the article obvious** - reader should know an article (post / write-up / piece) is linked in the comments, not a vague "link" that could be anything.
  - **Must say** that link lives in the comments (comments are where they go; the article URL is what they click). When posting for real, put the jorap.com URL in the **first comment** - caption points there; comment holds the click (Facebook especially throttles links in the post body).
  - **Must motivate the click** - name the payoff so scrolling past costs them something. Hook alone is not enough; closer alone is not enough. Why open comments *and* why tap the article URL, in one breath.
  - **Must pull** - one concrete hook from the post (scene, take, friction). Do **not** open on the article itself.
  - **Must not sound AI / creator-template** - no hollow openers, no "excited to share", no "check out my latest", no emoji spam, no hashtag walls, no "Thoughts?" closer. Reject article-first soft openers: "Here's an article attached in the comments about…", "I wrote a post about…", "New article in the comments:…". Those announce format before interest and burn the char budget.
  - Count characters before finishing. Soften or cut until ≤200. Spend chars on the hook and payoff; keep the CTA short.
- `slug`: always set - filename without `__` prefix (e.g. `slug: "wifi-router"`). Keep when the URL should differ from the filename (rare; add `aliases` for the old path).
- `image_prompt`: one paste-ready prompt for generating the hero image (Midjourney / Flux / similar). Specific scene that matches the post - subject, setting, light, mood, what to exclude. Photorealistic unless the post needs otherwise. No text, logos, watermarks, or brand marks in frame unless the post is literally about that object and the mark is unavoidable. Not a caption; not SEO keywords. Keep until `image` points at a real file, then leave it as the generation record.
- `level_depth`: max Depth of Understanding rung the post *reaches* (not the reader): 1 Recognize, 2 Explain, 3 Use, 4 Connect, 5 Create. Scrapbooks/catalogs → 1; how-to/recipes/lived criteria → 3; stack tradeoffs/systems → 4; inventing or shipping a new thing → 5.

### Publishing

To publish a draft (`__post-name.md`):

1. Drop the `__` prefix from the filename.
2. Set `draft: false`.
3. Keep `slug` in frontmatter (see **Frontmatter** above).
4. Do **not** commit or push unless the user explicitly asks.

## Gear and reviews

No affiliate links on the site as of now. Named products you own, what ended up in a drawer, and "I'd buy again" are all fine. **No currency values** - no dollar amounts, peso figures, or "what I paid." Use relative terms (budget, premium, cheap, annual renewal) instead. Skip affiliate-marketing tone - no "game-changer", no "must-have", no breathless superlatives.

## Recipe posts (variant)

Read [recipe-style.md](recipe-style.md) before drafting or editing any food post. Full rationale lives in `content/english/blog/__modified-atk-recipe-style-guide-rules.md`.

Recipe content is more instructional - ingredients, steps, timings - but section intros stay human. Avoid food-blog filler ("This delicious recipe will tantalize your taste buds").

| Zone | Rule |
|------|------|
| **Voice** | JoRap in opening, section intros, close; ATK-scannable in ingredients and steps |
| **Measurements** | Metric first, practical volume in parentheses (`160 ml, about 2/3 cup`) - same in ingredients **and** steps |
| **Fractions** | Digits with slash (`1/2` not `½`) |
| **Steps** | Imperative, articles OK, times/heat in the step they apply to, equipment when size matters; **repeat amounts on add lines only** (not prep/reserve/transfer) |
| **Facts** | Match existing JoRap recipe posts for Instant Pot ratios; no invented brands or currency |

Models invent confident liquid ratios. The style doc cuts shape drift - author still QA's numbers.

## Voice check

- [ ] Opens with experience or a concrete problem, not a generic intro
- [ ] Opening carries an attitude of gratitude (earned, specific - not performative thanks)
- [ ] Closing lands the same gratitude posture (what you'd keep / who helped / what the mess taught)
- [ ] Uses "I" and real scenarios, not "users" and "one might"
- [ ] At least one specific detail per section (number, name, place, mistake) - not currency
- [ ] Shows thinking somewhere - a tradeoff, near-miss, or honest doubt - then lands a take
- [ ] States opinions clearly - no endless "it depends" without a take
- [ ] Plain words only - no jargon or thesaurus words you wouldn't say out loud
- [ ] Read aloud - no word you'd pause to define
- [ ] No AI-slop phrases (see `data/voice-words.yaml` phrases + examples.md)
- [ ] `pnpm lint:slop` clean on publish (`draft: false`)
- [ ] `pnpm slop:score` per100w dropped after voice passes (or ≤2.0 on final draft)
- [ ] Sentence lengths vary - not a wall of same-shaped paragraphs
- [ ] Section headings sound like JoRap, not a product manual
- [ ] Would sound natural read aloud by a person, not narrated by a help article
- [ ] Frontmatter description sounds like the author, not an SEO bot
- [ ] `social_media_intro` ≤200 chars, shape is hook → payoff → CTA, makes clear an article is linked in comments, names why to click, sounds human - you'd open comments and tap it (no article-first opener)
- [ ] `image_prompt` is a usable generation prompt for this post's hero (specific scene, no text/logos)
- [ ] Passes the swap test: couldn't paste this into a random tech blog without it feeling off
- [ ] Personal facts match the ledger (`__interesting-facts-about-jorap.md`); no invented pop-culture or sports picks from gap tables
- [ ] Likability lens: useful takeaway, honest friction, human specific, respectful tone (not performative warmth)
- [ ] Connection lens: reader problem first, beyond-words specific, earns trust (not just informs)
- [ ] `pnpm lint:voice` clean (dashes + AI-tell words)
- [ ] WTL skim: reasoning visible, narrative order, draft changed what you thought ([writing-to-learn.md](writing-to-learn.md))
- [ ] Zinsser skim: bracket test, unity, lead/ending, read aloud ([zinsser.md](zinsser.md))
- [ ] Recipe posts: [recipe-style.md](recipe-style.md) - metric-first amounts, `1/2` fractions, voice split, amounts on add lines only

## Do not

- Commit or push unless the user explicitly asks
- Add engagement bait ("Let me know in the comments!", "What do you think?")
- Pad with obvious filler or restate the heading in the first sentence
- Use emoji in post body
- Use em dashes; use a normal hyphen (-), comma, or parentheses instead
- Over-hedge every claim ("might potentially perhaps")
- Write listicle intros that promise "10 game-changing tips"
- Turn personal gear picks into affiliate-marketing tone
- Mention currency values (dollar amounts, peso, "what I paid") - use relative cost instead
- Fake gratitude theater ("I'm so grateful for the opportunity…", "Thanks for reading!", curtain-call blessings) - gratitude is attitude in the open and close, not a banner

## Expanding outlines

When a post is only an outline (see `__extension-cord.md`, `__wifi-router.md`):

1. Keep the outline's intent and section order.
2. Write each section as prose-first - not bullet dumps unless it's a genuine checklist. Use Type B drafting ([writing-to-learn.md](writing-to-learn.md)): one sentence after another until the section's real point appears.
3. Add the personal thread: why this topic, what you learned, what you'd tell a friend.
4. Preserve Hugo frontmatter; set `draft: true` until the user publishes.
5. **Draft filenames** use a `__` prefix (e.g. `__wifi-router.md`) so drafts sort apart in the file tree. Set `slug` to the intended publish URL (e.g. `slug: "wifi-router"`). See **Publishing** above and `archetypes/blog.md` for field order.
