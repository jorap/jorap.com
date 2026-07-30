# Writing to Learn (Zinsser) — discovery layer

William Zinsser's *Writing to Learn* pairs with *On Writing Well* ([zinsser.md](zinsser.md)). OWW teaches **clear sentences**; WTL teaches **why writing is how you learn the subject** — and how exploratory drafts become finished posts. JoRap voice still owns person, scene, and connection; use WTL when **drafting**, **expanding outlines**, or **tech/how-to posts where the take wasn't clear until you wrote**.

**JoRap deltas:** blog posts are mostly Type B (discover the take) finished as Type A (clear enough to help a reader). WTL's classroom examples apply to **your** reasoning on Hugo, deploy, gear, faith — not student lab reports.

## Core idea

Writing, thinking, and learning are one process. Putting half-formed ideas into sentences is like defrosting the windshield: the shape gathers until you see what you meant.

| Fear WTL addresses | JoRap move |
|--------------------|------------|
| Fear of writing | Draft in `__` files; passes fix prose — you don't need a perfect first sentence |
| Fear of "hard" subjects | Write your way into the topic; plain words are the route in |
| Teacher owns the right answer | Your post is the take you earned by writing, not a syllabus recap |

**Writing across the curriculum** (WTL's frame): every subject has a literature of clear models. Read how others wrote it; imitate structure, then shed the skin. Same for blog categories — read 1–2 reference posts before drafting (SKILL.md workflow).

## Type A vs Type B

| | Type A (explanatory) | Type B (exploratory) |
|---|---------------------|---------------------|
| **Purpose** | Transmit what you already know | Find out what you know and want to say |
| **When** | Polishing, manuals, tight how-to steps | First draft, outline expansion, stuck on the take |
| **Method** | Think → write → "Did I say it?" → rewrite | Follow the sentence; the road reveals itself |
| **JoRap** | Final publishable post, recipe steps | `__` drafts, interview notes → first prose |

Both need grammar and order. "Free writing" is a search mechanism, not permission to publish slop. Type B discovers; Type A (plus seven passes) delivers.

**Type A loop** (memos, clear instructions, final sections):

1. What do I want to say?
2. Say it.
3. Put yourself in the reader's mind — clear to someone who knows nothing?
4. What must come next? Does it follow logically?
5. Repeat until done.

The hard part is thinking, not typing.

## Writing to learn on the blog

Use WTL when the post is **reasoning toward** something:

- **Outlines** (`__wifi-router.md`, etc.): each section should be prose that forces one real scene or failure — not bullets waiting for facts.
- **How-to / migration / stack posts**: write how you approached the problem before you tidy the steps; readers learn from the trip, not only the destination.
- **Opinion posts**: one honest doubt or near-miss per major section — then land the take (pass #3).

**Fuzzy thinking** is the main enemy (WTL, Gustavus faculty). Rambling, vague goals ("better communication", "world peace"), hedging without a point — fix by writing until the claim is **specific** enough to disagree with.

**Failure papers** (philosophy): a post that explains why you *couldn't* get where you wanted can still be progress — better than faking a proof. JoRap: "I almost bought X", "I still don't know Y", "this broke twice" — credibility, not weakness.

## Process over product

- Essence of writing is **rewriting** — meaning is elusive; revise until one read suffices.
- Shift from "finished essay with topic sentences" to **successive rethinkings** — same as JoRap passes and `pnpm slop:score`.
- Writing is **linear**: if B follows A and C follows B, you reach Z. Messy material still needs **narrative order** — several flashbacks OK if the reader never gets lost.
- Give the reader only what they need — prior knowledge of the subject is not required; **arrangement** is.

**Don't over-explain emotion.** If the material is already heavy, resist telling the reader why it's moving. Leave room for their reaction (WTL on Shanghai/Venice pieces — same rule for faith, family, loss, awe).

## Models and imitation

Writing is learned by imitation. Students feel guilty; professionals know you absorb how language works, then move beyond the model.

- Assign yourself **models**: reference posts, clear science writers, a paragraph you admire in the discipline.
- In tech posts: name who wrote clearly about the same problem — not to copy voice, but to see how they sequenced ideas.

## Crotchets (overlap with OWW)

WTL Part I, Chapter 5 restates principles OWW owns — use [zinsser.md](zinsser.md) for craft detail. WTL names these explicitly; worth a skim when `pnpm slop:score` stays high:

| Principle | One line |
|-----------|----------|
| **Information vs noise** | Ambiguity, redundancy, jargon, pomposity, clutter pollute the message — entropy wins unless you guard it |
| **Obscurity** | Deliberate murk is snobbery; simple style is harder thinking |
| **Concept nouns** | "Consideration", "capacity", "tendency" — death of vigorous prose; turn into verbs and people |
| **Active verbs** | Picture who did what, when |
| **Visible detail** | Anglo-Saxon nouns readers can see — house, cord, error message |
| **Brevity** | Rudeness to waste the reader's time; well-organized minds write short |
| **Enjoyment** | Reader should believe the writer is having a good time — even when the work was hard (craft + will) |

Paul Klee (WTL): **"exactitude winged by intuition"** — good blog prose: precise facts, human surprise.

## Map to JoRap workflow

| Stage | WTL emphasis |
|-------|----------------|
| Outline → draft | Type B; one sentence after another until the take appears |
| Pass #3 Show thinking | Tradeoffs, second-guesses, what you still don't know |
| Pass #6 Credible | Specifics from writing the problem, not from sounding expert |
| Pass #7 Top editor | Linear flow; cut self-indulgent facts; stop when done |
| Expanding outlines | Writing forces scenes — swap test fails on bullet dumps |
| Voice check | Did writing discover anything, or only decorate what you already knew? |

## Pre-publish WTL skim (with Zinsser + voice check)

- [ ] Did drafting **change** what I thought? (If not, was the post already fully known, or did I skip Type B?)
- [ ] Is the reasoning **visible** — steps a reader could follow, not just conclusions?
- [ ] Any section still fuzzy? Write one more sentence that names the actual claim or failure.
- [ ] Narrative order: can a reader go A → B → C without a map?
- [ ] Emotional peaks: did I explain why it's moving, or trust the scene?
- [ ] Zest: would a reader think I cared about this topic? (Not performative — earned.)

Then [zinsser.md](zinsser.md) bracket test, JoRap likability/connection lenses, and `pnpm lint:voice` / `pnpm lint:slop` / `pnpm slop:score`.
