---
target: homepage (themes/jorap/layouts/home.html)
total_score: 26
p0_count: 2
p1_count: 2
timestamp: 2026-06-18T17-10-25Z
slug: themes-jorap-layouts-home-html
---
# Design Critique: JoRap.com Homepage

**Target:** `themes/jorap/layouts/home.html` (homepage — blog-list grid with home intro)

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Active nav, theme switcher, and search work; no home-specific orientation beyond "Home" highlight |
| 2 | Match System / Real World | 2 | PRODUCT.md targets hiring decision-makers; homepage is a 12-post blog archive titled "Latest Blog Posts" |
| 3 | User Control and Freedom | 3 | Free navigation, search modal, theme toggle; no traps on a static surface |
| 4 | Consistency and Standards | 3 | Tokens, cards, and nav patterns cohere across the theme |
| 5 | Error Prevention | 3 | Static marketing surface; little to break |
| 6 | Recognition Rather Than Recall | 2 | Categories/Tags in primary nav assume blog literacy; no "start here if you're hiring" path |
| 7 | Flexibility and Efficiency of Use | 2 | Search helps power users; no curated hire shortcut or filters on home |
| 8 | Aesthetic and Minimalist Design | 2 | Visually calm skin, but 12 equal-weight cards create noise; chrome-heavy for sparse content |
| 9 | Error Recovery | 3 | N/A for primary home task |
| 10 | Help and Documentation | 2 | No onboarding, proof framing, or task-focused guidance for buyers |
| **Total** | | **26/40** | **Acceptable** — significant improvements needed before the primary audience is happy |

---

## Anti-Patterns Verdict

**Does this look AI-generated? Moderate yes — not catastrophic, but identifiable.**

**LLM assessment:** No absolute-ban hits on the live homepage (no side-stripe accents, gradient text, glassmorphism, hero-metric blocks, uppercase section eyebrows, or `01/02/03` scaffolding). What does read as template/AI grammar:

- **Identical card grid** — 12 copies of the same `blog-card` in a `md:col-6 lg:col-4` grid; icon + date + category + excerpt + outline button, repeated without curation. This is an explicit Impeccable absolute ban.
- **Second-order lane slop** — warm paper body, Inter-only, charcoal accent, elevated cards on cream: competent "Quiet Study," but it sits in the saturated warm-neutral + editorial-restraint family flagged as 2026 default.
- **HugoPlate blog-index DNA** — `home.html` renders only `blog-list`; banner/features/testimonials are commented ghosts. Restraint reads as unshipped template, not deliberate brand choice.
- **Hierarchy slop** — the real `<h1>` is "Latest Blog Posts"; the identity `<h1>` in `home-intro.html` is commented out. The DOM says "blog archive," not "hire this person."

Not dev-bro or SaaS-hero slop. It's polite blog-theme slop wearing good tokens.

**Deterministic scan:** 6 findings in `themes/jorap/layouts` (exit 2), 0 in homepage source files (`home.html`, `home-intro.html`). Built `public/index.html` adds 1 `flat-type-hierarchy` warning in shared header chrome (20px / 24px / 30px). Homepage-specific templates are clean; shared partials and shortcodes carry the noise.

**False positives (5 of 7):** `broken-image` hits in `image.html` and `style.html` are Hugo comments or template-bound `src`, not empty images at runtime. `design-system-font` on `self-hosted-fonts.html` flags dynamic Google Fonts URL for Inter, which IS documented in DESIGN.md. Spotify shortcode `12px` radius matches `rounded.xl` in DESIGN.md.

**Browser visualization:** Skipped — no browser automation available in this session. No reliable user-visible overlay was produced.

---

## Overall Impression

The skin is disciplined — warm paper, charcoal ink, thoughtful blog-card engineering — but the homepage information architecture contradicts the product brief. A hiring manager lands on a tagline that promises judgment, then gets reframed by "Latest Blog Posts" and twelve undifferentiated cards mixing tennis trackers, recipes, and Hugo how-tos. The single biggest opportunity: **make the homepage answer "why hire JoRap?" in the first fold, then curate thinking — don't firehose the archive.**

---

## What's Working

1. **Committed token system** — `DESIGN.md` "Quiet Study" palette (warm paper, charcoal accent, semantic `surface/elevated/ink`) is intentional and dark-mode-aware; not random Tailwind defaults.
2. **Subheading voice** — "Ideas, execution, and judgment, without the noise." matches Professional / idea-led / credible without performative nerd energy.
3. **Blog card engineering** — LCP-aware eager first image, configurable heading level, `motion-reduce` on hovers, accessible read-more `aria-label`; real craft exists under the grid.

---

## Priority Issues

### [P0] Homepage IA serves readers, not buyers
- **Why it matters:** PRODUCT.md primary user is a decision-maker evaluating fit for strategic/technical work. `home.html` renders only `blog-list` — the visit optimizes for blog subscribers, not client confidence.
- **Fix:** Restore a purpose-built home fold (who you are, what you do, proof, one CTA) before or instead of a raw 12-post archive. Curate 3–4 posts max with editorial framing.
- **Suggested command:** `/impeccable shape`

### [P0] Broken positioning hierarchy
- **Why it matters:** The identity `<h1>` in `home-intro.html` is commented out. The visible page `<h1>` is "Latest Blog Posts," followed by twelve card `<h2>`s. Screen readers and skimmers both get "blog archive" as the page's primary meaning.
- **Fix:** Uncomment/adapt a real `<h1>` (name + role or positioning line). Demote the archive label to `<h2>` or remove it. Pass `HeadingLevel: 3` to cards on home.
- **Suggested command:** `/impeccable clarify`

### [P1] Identical 12-card grid
- **Why it matters:** Absolute-ban pattern; no editorial judgment visible. Cognitive load fails on single focus, chunking, minimal choices, and progressive disclosure.
- **Fix:** Featured + "selected thinking" layout; asymmetric lead card; optional category filter for buyers.
- **Suggested command:** `/impeccable layout`

### [P1] Brand register fracture
- **Why it matters:** Site title "JoRap's World" (playful/hobby framing), meta description "I'm funny, but I'm not kidding." (flippant), and disabled navigation CTA undermine client-facing credibility.
- **Fix:** Align site title, meta, and About lede to the client-facing register. One sentence of hireable positioning above the fold.
- **Suggested command:** `/impeccable clarify`

### [P2] No conversion path
- **Why it matters:** `[navigation_button] enable = false` — Morgan has no obvious next step after a positive skim.
- **Fix:** Enable a restrained CTA ("Work with me" / "Get in touch") in header and home intro.
- **Suggested command:** `/impeccable onboard`

### [P3] Blog-admin nav on brand home
- **Why it matters:** Categories + Tags in main nav (5 items) plus search + theme switcher = 7+ chrome decisions before content. Blog taxonomy literacy assumed.
- **Fix:** Demote taxonomies to footer or blog subnav. Keep Home / About / Work or Blog / Contact.
- **Suggested command:** `/impeccable distill`

---

## Persona Red Flags

**Jordan (first-timer):** "JoRap's World" doesn't say what you do or for whom. No identity `<h1>`. Looks like a blog stumbled into, not a professional to hire.

**Casey (mobile):** Sticky header + utilities consume viewport. Twelve stacked equal-weight cards = long scroll before signal. Hamburger hides About.

**Morgan (hiring manager, between meetings):** Tagline promises judgment; grid delivers recipe posts and gadget reviews. No case study, client outcome, or contact CTA in first fold — "interesting, not hireable yet."

---

## Minor Observations

- `home_intro.lede` is empty — missed chance for one plain-language buyer sentence.
- Commented `banner.html` / `features.html` / `testimonials.html` suggest incomplete departure from Hugoplate marketing scaffold.
- Footer social icons use solid `bg-accent` tiles — slightly louder than "restraint" north star, but consistent.
- `mainSections = ["blog"]` reinforces blog-first mental model site-wide.
- Inter-only hierarchy is disciplined and defensible per identity-preservation, even though Inter is reflex-reject for greenfield.

---

## Questions to Consider

1. If the homepage succeeded, would Morgan **contact you** or **subscribe to your thinking** — and which outcome does a 12-post reverse-chron grid actually optimize for?
2. Is commenting out banner/features/testimonials **editorial restraint**, or **absence of a point of view** that PRODUCT.md says must be visible in 90 seconds?
3. Would you trust a strategist who curates nothing on their own front door — or does the firehose prove authenticity? For this register, curation is the product.
