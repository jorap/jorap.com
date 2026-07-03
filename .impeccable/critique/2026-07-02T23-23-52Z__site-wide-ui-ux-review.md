---
target: site-wide UI/UX review
total_score: 30
p0_count: 0
p1_count: 3
timestamp: 2026-07-02T23-23-52Z
slug: site-wide-ui-ux-review
---
# Design Critique: JoRap.com (Site-Wide UI/UX)

**Target:** Site-wide UI/UX review — marketing shell (home, blog), notes garden (list, single, graph, review, flashcards), shared chrome (header, footer, tokens)

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Notes list count uses `aria-live`; review shows progress; theme switch lacks live-region announcement |
| 2 | Match System / Real World | 3 | Homepage speaks to buyers; notes chrome assumes garden literacy (OKF, orphans, hubs) |
| 3 | User Control and Freedom | 3 | Skip link + `#main`, clear filters, review exit, graph reset/present escape |
| 4 | Consistency and Standards | 3 | Strong semantic tokens; minor radius drift (`0.375rem`, `999px` vs DESIGN.md scale) |
| 5 | Error Prevention | 3 | Review reset has no confirm; otherwise sensible constraints |
| 6 | Recognition Rather Than Recall | 2 | Notes toolbar (7–9 pills), graph filter wall (11+), icon-only search |
| 7 | Flexibility and Efficiency of Use | 4 | Review keyboard shortcuts, graph power controls, wikilink preview, random tools |
| 8 | Aesthetic and Minimalist Design | 3 | Homepage calmer post-proof removal; notes tool surfaces are dense |
| 9 | Error Recovery | 3 | Empty states on filter/search; issues panel guides fixes |
| 10 | Help and Documentation | 3 | Inline hints on graph/review; no first-run orientation for the garden |
| **Total** | | **30/40** | **Good** — credible editorial shell; notes IA is the main load bottleneck |

---

## Anti-Patterns Verdict

**Does this look AI-generated? Low–moderate — structure is template-adjacent; craft is human.**

**LLM assessment:** Copy and token discipline read intentional, not generated. The warm-paper + Inter + elevated-card stack is a documented second-order training lane ("Quiet Study") — competent and on-brief for client-safe editorial, not a distinctive POV. No gradient text, hero metrics, or eyebrow scaffolding. Card grids serve real archives (blog, notes), not filler feature rows. The notes garden is the clearest human signature: graph, flashcards, issues lint, OKF export — product UI built on the same tokens, not a theme skin.

**Deterministic scan:** `layouts/`, `themes/jorap/layouts/`, `assets/css/custom.css` — **19 findings** (2 warning, 17 advisory). Warnings: `design-system-font` on self-hosted-fonts `%s` snippet (false positive), `broken-image` on Hugo `image.html` partials (template false positive). Advisories: `design-system-radius` drift (`0.375rem`, `999px` pill radii, Spotify embed `12px`). No slop-family hits (gradient text, side stripes, eyebrows).

**Browser visualization:** Not available in this session (no browser automation MCP; dev server not running). No reliable user-visible overlay.

---

## Overall Impression

JoRap.com is a **coherent restrained-editorial system** that mostly delivers on PRODUCT.md: calm hierarchy, hireable tone, ideas before optics. Since the June homepage critique, real fixes landed — skip link, `#main` landmark, duplicate scope/proof removed, blog curation shifted toward site owners. The ceiling now is **audience split and information density**: the marketing shell courts clients while the notes garden toolbar courts the author/power user. A buyer who clicks "Notes" meets OKF, Issues, and eleven graph filters before they meet an idea. That's the single biggest UX risk on an otherwise polished site.

---

## What's Working

1. **Token architecture is production-grade.** Semantic `surface / elevated / ink / accent` variables, dark-mode prose fixes in `custom.css`, and paired functional colors keep light/dark readable without `dark:` sprawl in every partial. Contrast checks pass: `ink-muted` ~10.2:1 and `ink-faint` ~5.1:1 on surface — placeholders and meta lines clear AA.

2. **Long-form reading is cared for.** `.content` capped at ~70ch, `text-wrap: balance/pretty` on home headings, article-title ramp on singles, collapsible mobile TOC on blog posts, sticky desktop TOC — the reading stack matches the "Quiet Study" north star.

3. **Notes tools respect accessibility baselines.** 44px touch targets on filters and graph controls, `prefers-reduced-motion` on card hovers and flashcard flip, `aria-pressed` on graph filters, keyboard legend on review, skip link with focus ring — more than most Hugo personal sites ship.

---

## Priority Issues

**[P1] Notes toolbar overload — author tools mixed with reader navigation**
- **Why it matters:** Seven to nine equal-weight pills (All, Graph, Backlinks, Issues, Flashcards, Review, Random Duo, Create, OKF) exceed working-memory limits and signal "dev garden" to a client skim — directly conflicts with PRODUCT.md anti-reference (performative nerd energy on the marketing shell).
- **Fix:** Split into two tiers: **Read** (All, Graph, Backlinks, Flashcards) always visible; **Author** (Issues, Create, OKF, Review) behind a "Tools" menu or footer-only on note singles. Keep counts on All/Issues.
- **Suggested command:** `/impeccable distill layouts/_partials/notes/toolbar.html`

**[P1] Graph filter wall — 11+ simultaneous choices**
- **Why it matters:** First visit to `/notes/graph/` presents two rows of rank + relationship filters with no hierarchy. Extraneous cognitive load; most users need All + maybe Orphans.
- **Fix:** Default to one row (All, Top/Middle/Bottom, Orphans, Hubs); tuck relationship filters (Extends, Contradicts, etc.) into a "Relationships" disclosure matching the notes-list Refine pattern.
- **Suggested command:** `/impeccable layout layouts/notes/graph.html`

**[P1] Dual identity — "JoRap Notes" vs "Jonathan Rapusas"**
- **Why it matters:** Hero h1 is the person's name; header shows logo alt + `site.Title` "JoRap Notes", `title_suffix`, and copyright all say product. Referrals expecting a freelancer see a notes app brand — trust friction at the front door.
- **Fix:** Header brand line: person name (or "Jonathan Rapusas") with "Notes" as a nav item only; demote "JoRap Notes" to notes-section subbrand and metadata where needed.
- **Suggested command:** `/impeccable clarify layouts/_partials/essentials/header.html`

**[P2] Homepage credibility gap — proof removed, nothing replaced**
- **Why it matters:** Disabling `home_proof` fixed duplication (good), but buyers still get capability copy in scope + blog grid with no outcome evidence (quote, logo strip, one metric). Peak-end rule: they leave informed but not convinced.
- **Fix:** One proof block when real evidence exists — single testimonial, client outcome, or "selected work" strip. Keep `home_proof` off until then.
- **Suggested command:** `/impeccable shape themes/jorap/layouts/_partials/sections/home-proof.html`

**[P2] Icon-only search in header**
- **Why it matters:** Search button has `aria-label` but no visible text — fine for repeat visitors, opaque for Jordan (first-timer) and low-vision users who don't tab immediately.
- **Fix:** Add "Search" text label at `md:` breakpoint or persistent tooltip on focus.
- **Suggested command:** `/impeccable adapt layouts/_partials/essentials/header.html`

---

## Persona Red Flags

**Jordan (client first-timer):** Lands on a strong hero, then header still says "JoRap Notes." Clicks Notes → toolbar shows "OKF" and "Issues | 12" with no explanation. Graph page hint mentions ⌘/Ctrl-click — assumes desktop literacy. Abandon risk at notes threshold, not homepage.

**Alex (notes power user):** Toolbar density is acceptable; review keyboard shortcuts and graph present mode are excellent. No red flags on primary flows — would want Issues count one click away (keep it, just tier it).

**Sam (keyboard/screen reader):** Skip link and focus rings work. Graph canvas is `role="img"` with mouse-first interaction — keyboard users cannot traverse nodes. Theme switch updates state without `aria-live` announcement. Search modal relies on vendor `z-index: 9999` stacking.

**Morgan (buyer evaluating hire):** Homepage lede and scope read professional. Writing grid now targets site owners (improved). No social proof, no portfolio imagery, notes garden visible in main nav — risks "interesting blogger, unclear consultant."

---

## Minor Observations

- Mobile abbreviations ("Duo", "Create") save space but increase recall cost vs desktop labels.
- Blog mobile TOC is collapsible; notes mobile TOC is always expanded — inconsistent pattern.
- `.btn` `text-transform: capitalize` fights sentence-case labels in a few places.
- `0.375rem` (6px) radius appears on graph frames and selects but isn't in DESIGN.md rounded scale — document or tokenize.
- `heading-title-case` + `text-transform: capitalize` can mishandle proper nouns (e.g. "WordPress").

---

## Questions to Consider

- What if Notes nav said "Ideas" to buyers and hid author tools unless you're on a note you own?
- Does the graph page need all relationship filters on first paint, or only after someone clicks a node?
- What would one line of client proof do to the homepage's conversion story — and do you have it?
