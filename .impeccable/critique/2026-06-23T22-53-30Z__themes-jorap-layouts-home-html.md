---
target: homepage (themes/jorap/layouts/home.html)
total_score: 27
p0_count: 1
p1_count: 2
timestamp: 2026-06-23T22-53-30Z
slug: themes-jorap-layouts-home-html
---
# Design Critique: JoRap.com Homepage

**Target:** `themes/jorap/layouts/home.html` (and partials: `home-intro`, `home-scope`, `home-proof`, `home-writing`; content in `config/_default/params.toml`)

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Theme switch syncs `aria-checked`; no live region announces mode change |
| 2 | Match System / Real World | 3 | Hero speaks to buyers; header/meta still say "JoRap Notes" product |
| 3 | User Control and Freedom | 3 | Clean exits; static page with no traps |
| 4 | Consistency and Standards | 2 | Dual identity (person vs product); scope + proof share identical `<dl>` template and overlapping copy |
| 5 | Error Prevention | 3 | Minimal interaction surface on homepage |
| 6 | Recognition Rather Than Recall | 3 | Four-item nav + dual CTAs are clear; search is icon-only |
| 7 | Flexibility and Efficiency of Use | 2 | No skip-to-main link; `baseof.html` `<main>` lacks `id="main"` in source |
| 8 | Aesthetic and Minimalist Design | 2 | Scope + proof repeat the capability story; five identical blog-card shells |
| 9 | Error Recovery | 3 | N/A for primary home task |
| 10 | Help and Documentation | 3 | Lede frames positioning; no guided "start here if hiring" lane |
| **Total** | | **27/40** | **Acceptable (high)** — credible shell, proof and audience gaps remain |

---

## Anti-Patterns Verdict

**Does this look AI-generated? Moderate yes — copy is human; structure still template-shaped.**

**LLM assessment:** The writing passes the slop test. "Usually on the same project" and the 2013 freelancing anchor sound edited by a person. The layout does not: hero → two-column `<dl>` blocks → blog grid is Hugoplate starter geometry with renamed section titles. Scope ("Work I Take On") and proof ("What You Actually Get") use the same markup pattern and tell overlapping stories — WordPress/static sites appear in both columns, migrations in scope mirror deployments in proof. Five blog cards with identical `btn-outline-primary` "Read more" affordances create visual sameness. "Quiet Study" (warm paper `#f5f3f0`, Inter-only, elevated cards) is competent editorial restraint — a second-order training-data lane per brand register — not a distinctive POV. No hero imagery: acceptable for an ideas-led brand per PRODUCT.md, but the page has no visual proof of work either.

**Deterministic scan:** Homepage markup (`home.html`, four `home-*` partials, `public/index.html`) — **0 findings**, exit 0. Broader `themes/jorap/layouts` + `assets` — **12 findings** (7 warning, 5 advisory): `broken-image` on Hugo `image.html` partial (template false positive), `design-system-font` on self-hosted-fonts `%s` snippet and vendored Swiper, `layout-transition` in Swiper CSS, `design-system-radius` in Spotify shortcodes and module-overrides. None originate in `sections/home-*` partials.

**Browser visualization:** No browser automation MCP available; `.impeccable/live/config.json` absent. Live-server injection not attempted. No reliable user-visible overlay available.

---

## Overall Impression

The homepage reads as a professional attempting to speak to clients, not a raw blog index. Person-first h1, buyer-facing lede, and calmer card grid are real improvements. The ceiling is **proof and audience alignment**: copy asserts judgment, but scope/proof say the same thing twice, the blog grid is developer-to-developer ("How I Built JoRap Notes," "Hugoplate Theme Review"), and "JoRap Notes" in the header fights "Jonathan Rapusas" in the hero. A decision-maker skimming between meetings leaves interested but unconvinced they'd reach out.

---

## What's Working

1. **The lede's closing clause is genuinely differentiated.** "Web development, technical support, and training — usually on the same project" communicates multi-hat value in one line. It's the strongest sentence on the page.

2. **Hierarchy repair holds.** Jonathan Rapusas is h1; Selected Posts is h2; cards are h3. Person before archive.

3. **Token architecture is maintainable.** Semantic `surface / elevated / ink / accent` intermediates keep dark mode paired without `dark:` sprawl in every partial. Card hover respects `prefers-reduced-motion`.

---

## Priority Issues

**[P0] Scope + proof are the same story twice**
- **Why it matters:** A client skimming both columns concludes the site is disorganized or padded — trust dip at the exact moment you're selling clarity.
- **Fix:** Merge into one section with a different structure, or replace proof with hard evidence (client quote, outcome metric, logo strip). Capability labels from the provider are not proof.
- **Suggested command:** `/impeccable distill themes/jorap/layouts/home.html`

**[P1] Blog curation signals developer peer, not buyer**
- **Why it matters:** Four of five `post_slugs` are build logs and theme reviews. A VP evaluating a consultant has no entry point; the grid undermines the hero's client register.
- **Fix:** Curate `post_slugs` toward client problems (migrations, hiring a freelancer, WordPress vs static). Demote peer-content on the homepage.
- **Suggested command:** `/impeccable clarify config/_default/params.toml`

**[P1] "JoRap Notes" vs "Jonathan Rapusas" — dual identity**
- **Why it matters:** Header logo alt, `<title>`, and `title_suffix` say "JoRap Notes"; hero says a person's name. Referrals expecting a freelancer see a notes product.
- **Fix:** Pick one primary identity for the marketing shell (likely the person for buyer traffic) and demote "JoRap Notes" to subbrand where Notes Garden lives.
- **Suggested command:** `/impeccable clarify layouts/_partials/essentials/header.html`

**[P2] No skip link or main landmark in source**
- **Why it matters:** Keyboard users tab through full header + search + theme toggle on every page load. WCAG 2.4.1 bypass blocks are a stated AA target in PRODUCT.md.
- **Fix:** Add visually hidden "Skip to content" link targeting `#main`; give `<main>` an `id="main"` in `baseof.html`.
- **Suggested command:** `/impeccable polish themes/jorap/layouts/baseof.html`

**[P2] No social proof on homepage**
- **Why it matters:** Self-reported skills since 2005 don't close a calendar invite. One client sentence beats three capability bullets.
- **Fix:** Wire testimonials partial or one outcome line into home-proof; retire capability-only `<dl>` if proof can't be evidenced.
- **Suggested command:** `/impeccable shape themes/jorap/layouts/_partials/sections/home-proof.html`

---

## Persona Red Flags

**Jordan (First-Timer / potential client):** Lands on "Jonathan Rapusas" but the browser tab and header say "JoRap Notes" — immediate "which brand am I hiring?" confusion. Scrolls past two columns of similar bullet lists and can't tell which section answers "can you do my project?" vs "why trust you?" Selected Posts titles ("Hugoplate Theme Review," "Power of the Mouse Wheel Click") read as insider blog, not consultant credibility.

**Casey (Mobile, distracted):** Five stacked blog cards with identical chrome mean a long thumb scroll before any CTA repeat. Primary "Get in touch" sits only in hero — no sticky or mid-page re-entry for someone who skimmed the posts first.

**Sam (Accessibility-dependent):** No skip link in `baseof.html` source. Search button is icon-only (has `aria-label`, acceptable). Theme switcher uses `role="switch"` with `aria-checked` — improved, but no `aria-live` region when mode changes. `<main>` in source lacks `id="main"` for bypass target.

**Morgan (VP evaluating a consultant — project persona):** Hero copy passes the "stakeholder room" test. Then scope and proof both list WordPress/Hugo/migrations — reads as résumé padding, not outcomes. No client names, no "saved X hours," no "migrated Y without downtime." Blog grid confirms technologist identity, not strategic partner. Would bookmark, not email.

---

## Minor Observations

- `heading-title-case` on h2s title-cases every word ("Work I Take On") — slightly formal for JoRap voice.
- Featured first card is 8-col + `aspect-video`; siblings are 4-col — good hierarchy, but four smaller cards still feel like a uniform grid after the hero calm.
- Duplicate CTA: hero "Get in touch" + nav outline "Get in touch" — fine for recognition, slightly redundant visually.
- Inter is documented and intentional in DESIGN.md; brand register reflex-reject does not apply to committed identity.
- Warm paper body bg is the 2026 cream-band tell at OKLCH-adjacent values, but it's a committed design system choice — polish, not greenfield palette swap.

---

## Questions to Consider

- What if proof were one sentence from a real client instead of three self-labeled skills?
- Does the homepage need five posts, or would two buyer-relevant pieces plus "View all" feel more curated?
- What would change if the header said "Jonathan Rapusas" and "JoRap Notes" lived only on `/notes/`?
