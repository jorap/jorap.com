# On Writing Well (Zinsser) — JoRap backbone

William Zinsser's *On Writing Well* is the craft layer under [jorap-voice](SKILL.md). Zinsser teaches **how** to write clear nonfiction; JoRap voice teaches **who** is writing and **why** anyone should care. Use both: Zinsser on every sentence; JoRap on every scene and take.

For drafting and reasoning — writing as learning — see Zinsser's *Writing to Learn*: [writing-to-learn.md](writing-to-learn.md).

**JoRap deltas** (where this site goes past Zinsser): roughen over-polish; no currency in prose; connection lens (Maxwell) and likability lens; swap test for personal blog, not magazine assignment voice; `pnpm lint:voice` / `pnpm lint:slop` as mechanical gates.

## The transaction

Good nonfiction sells **who you are**, not just the topic. Enthusiasm, baggage, and a human on the page beat "personalizing" tricks.

| Zinsser | JoRap move |
|---------|------------|
| Write in first person when you can | Default on this blog — see **Tone** in SKILL.md |
| Be yourself; fake "style" is a toupee | Pass #5; don't sound like a brand blog |
| Readers want the real person behind the tension | Pass #1 lived-in + pass #6 credible |
| Writing is an act of ego — use its energy | State the take; don't hide behind "one" |

## Simplicity and clutter

Clear thinking and clear writing are the same job. Clutter is the enemy — weeds that sprout overnight.

**Bracket test** (Zinsser's Yale trick): mentally bracket every word that isn't doing new work. Read the sentence without the brackets. Cut what survives fine without them. First drafts can often lose half their length.

| Cut | Example |
|-----|---------|
| Hollow inflation | "at this point in time" → "now"; "experiencing pain" → "it hurts" |
| Fat prepositions | "face up to" → "face"; "free up" → "free" |
| Redundant adjectives | "personal friend", "tall skyscraper" |
| Concept nouns + "is" | "The reaction was incredulous laughter" → "People laughed in disbelief" |
| Qualifier hedges | "a bit", "sort of", "rather", "quite", "very", "pretty much" |
| Announcement phrases | "It is interesting to note" — if it's interesting, make it interesting |
| Journalese | "famed", "upcoming", "staffers", "beef up", "firing off a memo" |

Overlap with `data/voice-words.yaml` and pass #2 — skill is stricter than lint on fresh drafts.

## Unity (before you draft)

Decide once, then stick to it unless the material pulls you somewhere better — then **rewrite the opening** to match.

- **Pronoun:** first person (JoRap default)
- **Tense:** mostly past or mostly present — don't hop
- **Mood:** casual friend, not brochure + memoir + guidebook in one piece
- **Scope:** one corner of the subject — Tolstoy didn't write "about war"; he wrote about one man
- **One provocative thought** for the reader at the end — not five

Travel-writing rule applies everywhere: agglomeration of detail is not a free pass. Every fact must **do work**.

## Lead and ending

**Lead:** First sentence must earn the second. Hook with freshness, paradox, humor, or a concrete scene — not the future archaeologist, the man from Mars, or "one day not long ago."

**Ending:** When you're done, stop. No "In sum…", "What insights have we gleaned…", or third-grade outline summary. Prefer a short wrap, a full-circle echo, or a quote with finality. JoRap: land on what you'd buy again or actually do — aligns with Zinsser's "nearest exit."

Cut the first three paragraphs if they're throat-clearing; the real voice often starts at paragraph four (Zinsser's editor move). JoRap: same for generic intros — pass #7.

## Bits and pieces (sentence craft)

Run on pass #7 and when `pnpm slop:score` is high.

| Tool | Rule |
|------|------|
| **Verbs** | Active, precise — "Joe saw him" not "he was seen by Joe" |
| **Adverbs** | Most are redundant with the verb ("grinned widely") |
| **Adjectives** | Only when the noun doesn't already carry the meaning |
| **Qualifiers** | Kill timid hedges — be bold or be quiet |
| **Mood changers** | Start with "but" / "yet" when direction shifts — orient the reader early |
| **Contractions** | Warmth; fine for JoRap blog body |
| **Paragraphs** | Short puts air around the text — but don't chop one thought into verbless stumps |
| **Read aloud** | Ears catch what eyes forgive |
| **Quickest fix** | Stuck on a phrase? Ask if the sentence needs it at all — delete and move on |

## Rewriting

Rewriting **is** writing. Fluency (word processor, AI) is not quality. Professional writers rewrite sentences many times; gratitude, not punishment.

After draft: reshape for narrative flow, orient the reader after every time/tone shift, read aloud from start to finish. Computer = gift for cut/paste and reorder — use it.

## Trust your material

Don't separate "fact" and "color." The good story on page 9 belongs in the lead. Don't slow-motion nudge the reader toward significance — let a precise fact (4.3 seconds for a double play; oil still leaking from the Arizona) do the marveling.

Don't over-explain what readers can infer. Skip "surprisingly", "predictably", "of course" before the fact.

## Sound of your voice

**Breezy** ≠ conversational. Breezy = "believe you me", "your better half", talking down. **Effortless** (E. B. White) = hard work on grammar and cadence that *reads* relaxed.

- Never say on the page what you wouldn't say to a sharp friend mid-rush (JoRap pass #4)
- Clichés are taste failures — listen for them on read-aloud
- Imitate good models, then shed them — voice emerges when clutter goes

## Humor (when it fits)

Humor is a **tool**, not a genre — heighten crazy truth so readers see it. Control: stick to the form you're parodying; one joke per type; understatement beats exclamation points. JoRap: dry asides in **Understated humor** pillar — same lane, cooler temperature.

## Map to the seven passes

| Pass | Zinsser emphasis |
|------|------------------|
| 1 Lived-in | Transaction, trust material, humanity |
| 2 Strip AI | Clutter, journalese, concept nouns |
| 3 Thinking | Unity of mood; one point; visible mind |
| 4 One-friend | Audience: write for yourself, master craft for reader |
| 5 POV | Be yourself; sell your subject through conviction |
| 6 Credible | Concrete detail; don't inflate; reader does own marveling |
| 7 Top editor | Rewriting, bracket test, lead/ending, read aloud |

## Pre-publish Zinsser skim (with voice check)

- [ ] Every word doing **new** work? (bracket test)
- [ ] Unity: one pronoun, one tense dominant, one mood, one main point?
- [ ] Lead earns sentence two; ending stops without summary cranking?
- [ ] Active verbs; adverbs/adjectives/defensive qualifiers pruned?
- [ ] Sounds like a person, not breezy or bureaucratic?
- [ ] Read aloud — any clog or lost reader between sentences?

Then run JoRap **likability**, **connection**, and `pnpm lint:voice` / `pnpm lint:slop` / `pnpm slop:score`.
