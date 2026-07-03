---
target: site-wide UI/UX review (follow-up)
total_score: 32
p0_count: 0
p1_count: 1
timestamp: 2026-07-02T23-29-02Z
slug: site-wide-ui-ux-review
---
# Design Critique: JoRap.com (Site-Wide UI/UX) — Follow-up

**Target:** Site-wide UI/UX review after toolbar distill, graph layout, and polish pass

**Changes shipped:**
- Notes toolbar tiered: Read (All, Graph, Backlinks, Flashcards, Random Duo) + Tools `<details>` (Issues, Review, Create, OKF)
- Graph filters: rank/hub row visible; relationship filters in Relationships disclosure; Reset on primary row
- Polish: disclosure CSS aligned with notes-list-refine, focus rings on summaries, auto-open Relationships when a rel filter activates, fixed `notes-graph-toolbar` closing tag

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Unchanged; theme switch still lacks live-region announcement |
| 2 | Match System / Real World | 3 | Notes chrome less author-heavy at first glance; OKF still opaque to buyers |
| 3 | User Control and Freedom | 3 | Tools and Relationships use native `<details>` — keyboard-friendly disclosure |
| 4 | Consistency and Standards | 4 | Toolbar Tools and graph Relationships mirror notes-list Refine pattern |
| 5 | Error Prevention | 3 | Unchanged |
| 6 | Recognition Rather Than Recall | 3 | Toolbar down to ~5 visible + 1 Tools; graph primary row ~8 choices (was 11+ simultaneous) |
| 7 | Flexibility and Efficiency of Use | 4 | Author tools still one click inside Tools; graph rel filters unchanged for power users |
| 8 | Aesthetic and Minimalist Design | 4 | Notes index/graph toolbar rows breathe; less equal-weight pill noise |
| 9 | Error Recovery | 3 | Unchanged |
| 10 | Help and Documentation | 3 | Graph intro updated to point at Relationships disclosure |
| **Total** | | **32/40** | **Good (upper band)** — notes IA fixed; marketing identity gaps remain |

---

## Anti-Patterns Verdict

**LLM assessment:** The notes surfaces no longer read as "dev tool first." Progressive disclosure matches the existing Refine control — one pattern, not a new widget family. Warm editorial shell unchanged.

**Deterministic scan:** Changed files — **0 slop-family hits**; only pre-existing radius advisories in `custom.css`.

**Browser visualization:** Not run.

---

## Overall Impression

The two P1 notes-garden issues are resolved without removing capability. A client landing on `/notes/` sees five navigation pills plus Tools instead of nine competing actions. Graph first paint is one filter row plus a single Relationships affordance. The remaining gap from the prior critique is **marketing shell** (dual identity, social proof, search label) — intentionally out of scope for this pass.

---

## What's Working

1. **Progressive disclosure reuse** — Tools and Relationships follow the same `<details>` + btn-summary pattern as list Refine; no new component tax.
2. **Issue count preserved** — Tools summary shows `| N` when issues exist; Issues link keeps full count inside the panel.
3. **Power-user path intact** — Relationship filter click auto-opens the disclosure; Review/Issues/OKF remain reachable in two clicks max.

---

## Priority Issues (remaining)

**[P1] Dual identity — "JoRap Notes" vs "Jonathan Rapusas"** — unchanged from prior critique.

**[P2] Homepage credibility gap** — no social proof block yet.

**[P2] Icon-only search** — header search still icon-only.

**[P3] Graph primary row still has 8 filters** — acceptable for power users; could further group rank tiers later if needed.

---

## Persona Red Flags (updated)

**Jordan:** Notes toolbar no longer shows OKF at top level. Tools menu still requires curiosity. Graph page is calmer.

**Alex:** Tools adds one click for Issues — acceptable trade for cleaner default.

**Sam:** `<details>` summaries have focus-visible rings; Tools auto-opens on author pages via `open` attribute.

**Morgan:** Notes garden less intimidating; homepage/marketing gaps unchanged.

---

## Delta from Prior Run (30 → 32)

| Area | Before | After |
|------|--------|-------|
| Notes toolbar visible choices | 7–9 | 5–6 + Tools |
| Graph filters at first paint | 11+ | 8 + Relationships |
| Consistency heuristic | 3 | 4 |
| Recognition heuristic | 2 | 3 |
| Aesthetic heuristic | 3 | 4 |

---

## Questions to Consider

- Is Tools the right label, or "Author" / "Maintain" for your voice?
- Should Tools stay closed on Issues page even when `open` is set — or is auto-open on author routes the right signal?
