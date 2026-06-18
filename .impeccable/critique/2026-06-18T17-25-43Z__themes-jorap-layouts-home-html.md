---
target: homepage (themes/jorap/layouts/home.html)
total_score: 28
p0_count: 1
p1_count: 2
timestamp: 2026-06-18T17-25-43Z
slug: themes-jorap-layouts-home-html
---
# Design Critique: JoRap.com Homepage (Re-run)

**Target:** `themes/jorap/layouts/home.html` — post full-pass implementation

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Nav, search, theme switcher work; no "evaluating a consultant" orientation beyond content |
| 2 | Match System / Real World | 3 | Identity h1, buyer lede, CTAs align with PRODUCT.md — structure still blog-index with auto-picked posts |
| 3 | User Control and Freedom | 3 | Clean escape hatches; no traps |
| 4 | Consistency and Standards | 3 | Tokens cohere; minor fractures (logo_text "JoRap.com", footer Categories/Tags) |
| 5 | Error Prevention | 3 | Static home is safe; contact form action="#" is a dead end site-wide |
| 6 | Recognition Rather Than Recall | 3 | 4-item nav, dual CTAs, fixed hierarchy — no explicit "start here if hiring" lane |
| 7 | Flexibility and Efficiency of Use | 2 | Search helps power users; no buyer filter or work shortcut |
| 8 | Aesthetic and Minimalist Design | 3 | 4-card asymmetric grid calmer than 12; still four identical blog-card shells |
| 9 | Error Recovery | 3 | N/A for primary home task |
| 10 | Help and Documentation | 2 | Lede frames positioning; zero proof, outcomes, or guided next step beyond reading |
| **Total** | | **28/40** | **Good (low)** — meaningful fix pass; not yet "Morgan would reach out" |

**Delta from prior run:** 26 → 28 (+2). P0 hierarchy and brand register largely resolved.

---

## Anti-Patterns Verdict

**Does this look AI-generated? Moderate yes — improving, not cleared.**

**LLM assessment:** No longer raw Hugoplate blog-archive slop. Remaining tells:
- **Identical card grid (soft ban)** — same blog-card × 4; asymmetric sizing helps layout, not pattern
- **Positioning triads** — "Ideas, execution, and judgment" + "judgment, not just code" sit in saturated consultant-voice band
- **Quiet Study second-order** — warm paper, Inter, elevated bordered cards: competent, not distinctive
- **"Selected writing" vs ByDate.Reverse** — label implies curation; implementation is chronology

**Deterministic scan:** Exit 0, **0 findings** on `home.html`, `home-intro.html`, `blog-list.html`, and built `public/index.html`. Clean vs 6 findings pre-fix.

**Browser visualization:** Skipped — no browser automation available.

---

## Overall Impression

The full pass fixed the biggest structural sins: hierarchy, register, nav noise, and card overload. The homepage now reads as a professional personal brand attempting to speak to buyers — not a default blog index. The ceiling now is **proof and intent**: copy asserts judgment, but the grid still auto-surfaces whatever published last (currently hobby/tech mix), and CTAs land on a contact form wired to `#`. The next leap is showing outcomes, not just describing them.

---

## What's Working

1. **Hierarchy repair is real** — Jonathan Rapusas is h1; Selected writing is h2; cards are h3. Person first, not archive first.
2. **Buyer-facing register landed** — JoRap title, meta, About, and lede speak to stakeholders.
3. **Conversion scaffolding exists** — Home CTAs + nav button; 4-post cap + featured column meaningfully reduce noise.

---

## Priority Issues

### [P0] No proof layer — still not hireable in 90 seconds
- **Why:** PRODUCT.md success requires demonstrated credibility. Intro asserts judgment; home shows no outcomes, clients, or artifacts.
- **Fix:** Add proof fold: 2–3 outcome bullets, logos, or case-study teaser before/alongside writing.
- **Command:** `/impeccable shape`

### [P1] "Selected writing" is chronological, not curated
- **Why:** `ByDate.Reverse` with no manual pick list. Featured post may be hobby content under hiring register.
- **Fix:** `featured_slugs` or `params.home_blog.posts` in config; pin buyer-relevant lead posts.
- **Command:** `/impeccable layout`

### [P1] Contact is a conversion cliff
- **Why:** Contact page is front matter only; `contact_form_action = "#"`. CTAs route to a stub.
- **Fix:** Wire Formspree/Airform; add expectations copy (what to include, response time).
- **Command:** `/impeccable onboard`

### [P2] Homepage IA still blog-first under the hood
- **Why:** `home.html` renders only blog-list; banner/features remain commented ghosts.
- **Fix:** Split home into intro + proof + curated writing; archive lives on /blog.
- **Command:** `/impeccable shape`

### [P3] Residual blog-admin chrome
- **Why:** Footer still exposes Categories/Tags; logo_text "JoRap.com" vs header "JoRap".
- **Fix:** Demote taxonomies to blog contexts; align logo fallback text.
- **Command:** `/impeccable distill`

---

## Persona Red Flags

**Jordan (first-timer):** Name and lede help — largest visual below fold may still be a hobby blog card. "What does he do for clients?" unanswered.

**Casey (mobile):** Sticky header + utilities compete with intro on short viewport. Four stacked cards = long scroll before proof.

**Morgan (hiring manager):** Copy says "organizations"; grid may show tennis tracker and gadget posts. Interesting thinker, not yet verified operator.

---

## Minor Observations

- Duplicate "Get in touch" (intro + nav) both point to stub contact
- `mainSections = ["blog"]` reinforces reader-not-buyer mental model
- About page is solid — home links via secondary CTA only, not as proof
- Featured `lg:col-8` layout is a real upgrade; card pattern repetition persists

---

## Questions to Consider

1. If "Selected writing" is reverse-chronological, what are you selecting for — and would Morgan notice?
2. You fixed what the site says; when does it show what you've done for someone else?
3. Is four identical cards editorial restraint, or four chances for the wrong post to veto a hiring decision?
