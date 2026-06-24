---
target: homepage (themes/jorap/layouts/home.html)
total_score: 27
p0_count: 1
p1_count: 2
timestamp: 2026-06-23T15-11-36Z
slug: themes-jorap-layouts-home-html
---
# Design Critique: JoRap.com Homepage

**Target:** `themes/jorap/layouts/home.html`

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Theme toggle works visually but does not announce light/dark state to assistive tech |
| 2 | Match System / Real World | 3 | Hero speaks to buyers; "JoRap Notes" site title and nav still read as a blog product |
| 3 | User Control and Freedom | 3 | Clean exits; no traps on the static homepage |
| 4 | Consistency and Standards | 2 | Dual identity (Jonathan Rapusas vs JoRap Notes); scope and proof use identical `<dl>` templates |
| 5 | Error Prevention | 3 | Minimal interaction surface; contact form dead-end is site-wide, not home-specific |
| 6 | Recognition Rather Than Recall | 3 | Four-item nav and dual CTAs are clear; search is icon-only |
| 7 | Flexibility and Efficiency of Use | 2 | No skip-to-main link; no buyer shortcut beyond reading |
| 8 | Aesthetic and Minimalist Design | 2 | Scope + proof repeat the same capability story; five identical blog-card shells |
| 9 | Error Recovery | 3 | N/A for primary home task |
| 10 | Help and Documentation | 3 | Lede frames positioning; no guided "start here if hiring" lane |
| **Total** | | **27/40** | **Acceptable (high)** — credible shell, proof gap remains |

---

## Anti-Patterns Verdict

**Does this look AI-generated? Moderate yes — copy is human; structure still template-shaped.**

**LLM assessment:** The writing passes the slop test. "Usually on the same project" and the 2013 freelancing anchor sound edited by a person, not generated. The layout does not: hero → two-column services blocks → blog grid is Hugoplate starter geometry with renamed section titles. Scope and proof are the same `<dl>` pattern twice; "Work I Take On" and "What You Actually Get" frame different angles but the content overlaps (WordPress/static sites vs web development, migrations vs technical support). Five blog cards with identical `btn-outline-primary` "Read more →" buttons create a visual thicket. "Quiet Study" (warm paper, Inter, elevated cards) is competent editorial restraint — second-order training-data lane per brand register — not a distinctive POV.

**Deterministic scan:** `home.html` and built `public/index.html` — **0 findings**, exit 0. Broader `themes/jorap/layouts` + `assets` scan — **12 findings** (7 warning, 5 advisory): `broken-image` on Hugo `image.html` partial (template false positive), `design-system-font` on self-hosted-fonts `%s` snippet and vendored Swiper, `layout-transition` in Swiper CSS, `design-system-radius` in Spotify shortcodes and module-overrides. None originate in `sections/home-*` partials.

**Browser visualization:** Live server started on port 8400 and stopped cleanly. No Human-tab overlay — `live-inject` requires `.impeccable/live/config.json`; Puppeteer not installed for URL scan. No reliable user-visible overlay available.

---

## Overall Impression

The homepage cleared the structural sins from the prior critique: person-first h1, buyer-facing lede, calmer card grid. It now reads as a professional attempting to speak to clients, not a raw blog index. The ceiling is **proof and audience alignment**: copy asserts judgment, but scope/proof say the same thing twice, the blog grid is developer-to-developer ("How I Built JoRap Notes," "Hugoplate Theme Review"), and "JoRap Notes" in the header fights "Jonathan Rapusas" in the hero. Morgan the VP leaves interested but unconvinced she'd reach out.

---

## What's Working

1. **The lede's closing clause is genuinely differentiated.** "Web development, technical support, and training — usually on the same project" communicates multi-hat value in one line. It's the strongest sentence on the page and sits in the third paragraph.

2. **Hierarchy repair holds.** Jonathan Rapusas is h1; Selected Posts is h2; cards are h3. Person before archive.

3. **Token architecture is maintainable.** Semantic `surface / elevated / ink / accent` intermediates keep dark mode paired without `dark:` sprawl in every partial.

---

## Priority Issues

**[P0] Scope + proof are the same story twice**
- **Why it matters:** A client skimming both columns concludes the site is disorganized or padded — trust dip at the exact moment you're selling clarity.
- **Fix:** Merge into one section with a different structure, or replace proof with hard evidence (client quote, outcome, logo strip). Capability labels from the provider are not proof.
- **Suggested command:** `/impeccable distill themes/jorap/layouts/home.html`

**[P1] Blog curation signals developer peer, not buyer**
- **Why it matters:** Four of five `post_slugs` are build logs and theme reviews. A VP evaluating a consultant has no entry point; the grid undermines the hero's client register.
- **Fix:** Curate `post_slugs` toward client problems (migrations, hiring a freelancer, WordPress vs static). Drop or demote peer-content on the homepage.
- **Suggested command:** `/impeccable clarify config/_default/params.toml` (curation + section framing)

**[P1] "JoRap Notes" vs "Jonathan Rapusas" — dual identity**
- **Why it matters:** Header logo, footer copyright, and `title_suffix` say "JoRap Notes"; hero says a person's name. Referrals expecting a freelancer see a notes product.
- **Fix:** Pick one primary identity for the marketing shell (likely the person for buyer traffic) and demote "JoRap Notes" to section/subbrand where Notes Garden lives.
- **Suggested command:** `/impeccable clarify themes/jorap/layouts/_partials/essentials/header.html`

**[P2] No social proof on homepage**
- **Why it matters:** Self-reported skills since 2005 don't close a calendar invite. One client sentence beats three capability bullets.
- **Fix:** Wire `testimonials` partial or one outcome line into home-proof; retire capability-only `<dl>` if proof can't be evidenced.
- **Suggested command:** `/impeccable bolder themes/jorap/layouts/_partials/sections/home-proof.html`

**[P2] Value prop is typographically subordinate to the name**
- **Why it matters:** "Ideas, execution, and good sense, without the noise." is the differentiating line but renders smaller than the h1 name label.
- **Fix:** Give the subheading comparable visual weight, or lead with outcome-first headline and name as supporting identity.
- **Suggested command:** `/impeccable typeset themes/jorap/layouts/_partials/sections/home-intro.html`

---

## Persona Red Flags

**Jordan (first-timer):** Lands on a huge name with no immediate "what can you do for me." "JoRap Notes" in the header reads as a tool, not a person. Blog grid dominates the lower half — leaves thinking personal blog, not service provider.

**Morgan (VP, 30-second skim):** 0–15s: name + generic consultant tagline. 15–22s: lede creates brief interest ("same project"). 22–40s: scope + proof feel like rereading the same list. 40s+: technical posts (JoRap Notes build, Hugoplate review). Never sees a client name or outcome. Exit: "capable, not sure he's worked at my level."

**Casey (mobile):** `text-h1-sm` (~55px) name consumes viewport width on 375px. Proof section stacks below scope — the more persuasive frame may sit below fold. Featured card `aspect-video` pushes blog content down on short viewports.

---

## Minor Observations

- `availability = "Only open to remote work."` repeats role line and sits above CTAs before trust is established — belongs on Contact/About.
- Five identical "Read more →" outline buttons when card titles are already links — visual noise.
- `home-writing` mixes Bootstrap grid (`row`, `lg:col-8`) with Tailwind elsewhere — Hugoplate inheritance, inconsistent layout system.
- No skip-to-main-content link in base template — keyboard users tab through full nav every load.
- Theme-wide detector noise (Swiper, Spotify shortcodes) is not homepage-specific; ignore or scope detector to built `public/` for CI.

---

## Questions to Consider

- Who is this homepage actually for — Morgan or your developer peers? The nav (Notes, Categories, Tags), brand (JoRap Notes), and curation currently answer "peers."
- If proof were one real client sentence instead of three capability bullets, would Morgan need the scope column at all?
- The site says "without the noise" — what would remain if you took that literally: name, lede, one testimonial, one best post?
