# Content voice review plan

Site-wide pass over **published** blog posts and the notes garden so prose matches [jorap-voice](../.cursor/skills/jorap-voice/SKILL.md): plain words, personal tone, no AI tells.

**Scope (2026-07-03):**

| Area | Count | In scope |
|------|------:|----------|
| Published blog posts | 15 | Yes |
| Draft blog stubs (`__*.md`) | 37 | No — skip until promoted |
| Atomic notes | 200 | Yes |
| Meta / index / hub notes | 14 | Yes — lighter pass (hubs, MOCs) |

**Default execution model:** **Claude Sonnet 5 (Thinking)**  
**Escalation model:** **Claude Opus 4.8 (Thinking)**  
**Mechanical / script work:** **Composer 2.5 Fast** (or terminal only — no model spend)

---

## Model roles

| Phase | Model | Why |
|-------|--------|-----|
| 0 — Baseline lint | None (scripts) | Free; catches structure before paid tokens |
| 1 — Auto-fixes | **Composer 2.5 Fast** | Dashes, formatting, deterministic patches |
| 2 — Prose review (bulk) | **Claude Sonnet 5 (Thinking)** | Best quality-per-dollar for voice + rewrites |
| 3 — Escalation | **Claude Opus 4.8 (Thinking)** | Flagship posts + notes that still sound stiff after Sonnet |
| 4 — Publish batch | **Composer 2.5 Fast** | Changelog, commit message, `[skip ci]` only if non-deploy |

Do **not** use Composer or GPT Codex for prose rewrites. Do **not** run Opus on every file — reserve it for ~10–20% escalations.

---

## Phase 0 — Baseline (no model)

Run from repo root. Fix anything that fails before opening a writing chat.

```bash
pnpm lint:garden
pnpm lint:voice
pnpm voice:scan
```

Record `voice:scan` output — it is the prioritized hit list for Phase 2.

**Exit criteria:** `lint:garden` and `lint:voice` pass (or only known waivers documented below).

---

## Phase 1 — Mechanical fixes

**Model:** **Composer 2.5 Fast** (or run scripts yourself)

| Task | Command / action |
|------|------------------|
| Em/en dashes → hyphens | `python3 scripts/notes-voice-sanitize.py` (drop `--check`) |
| Frontmatter / shareable lines | Fix `lint-notes-frontmatter.py` failures; use `fix-shareable-thought-review.py` only for listed keys |
| Format drift | `python3 scripts/normalize-notes-format.py` (verify mode first) |
| Flashcard shape | `pnpm lint:cards` — fix before voice-editing card text |

**Exit criteria:** Phase 0 commands green again. No prose rewriting in this phase.

---

## Phase 2 — Prose review (Sonnet)

**Model:** **Claude Sonnet 5 (Thinking)**  
**Skills:** `@jorap-voice` (+ `@flashcards` when editing `cards:`)

**Batch size:** 10–12 atomic notes **or** 2–4 blog posts per chat. New chat per batch.

**Prompt (copy per batch):**

```text
Review these files with jorap-voice (+ flashcards for any cards: fields).

For each file:
1. Flag stiff, generic, or AI-sounding phrases.
2. Rewrite only what needs it — keep facts, links, and structure.
3. Run the de-AI pass from jorap-voice.
4. Do not change note_kind, categories, tags, or wikilinks unless broken.

When done, list files touched and anything I should read manually.
```

### 2A — Published blogs (15 files, ~4 Sonnet sessions)

Do these first — highest traffic, sets voice reference for notes.

| Session | Files |
|---------|--------|
| B1 | `how-i-built-jorap-notes.md`, `top-reasons-create-maintain-your-own-website.md`, `getting-started-with-rss-feeds-beginners-guide.md` |
| B2 | `what-i-look-for-in-wireless-earphones.md`, `top-reasons-why-you-still-need-use-desktop-laptop.md`, `facebooks-hidden-gem-how-favorites-feed-transforms-your-social-media-experience.md` |
| B3 | `consistent-ai-output-wordpress-builds.md`, `hugoplate-theme-review.md`, `power-of-the-mouse-wheel-click.md` |
| B4 | `alex-eala-pro-career-tracker.md`, `miracle-isaiah-david.md`, `dnpap-song-resources.md`, `power-of-worship-pads-enhancing-your-worship-experience.md`, `set-it-forget-it-arroz-caldo.md`, `instant-pot-chicken-adobo.md` |

After B1, skim one rewritten post — if voice is off, fix the prompt before continuing.

### 2B — Hub / meta notes (14 files, 1 Sonnet session)

| Session | Files |
|---------|--------|
| M1 | `getting-started.md`, `maps-of-content.md`, `flashcards.md`, `mental-models.md`, `pkm.md`, `eternal-principles.md`, `workplace-principles.md`, `systems-for-growth.md`, `graph.md`, `backlinks.md`, `create.md`, `review.md`, `issues.md`, `okf-export.md`, `random-duo.md`, `pressure-reveals-weakness.md` |

Hubs: tighten `description`, relationship reasons, and any body copy — not full rewrites of linked atomic notes.

### 2C — Atomic notes by category (~17 Sonnet sessions)

Use `voice:scan` hits to order files **within** each category (worst first).

| Session | Category | ~Files |
|---------|----------|-------:|
| N1 | Productivity | 68 → split **N1a** (34) + **N1b** (34) |
| N2 | Leadership | 57 → **N2a** (28) + **N2b** (29) |
| N3 | Faith | 53 → **N3a** (26) + **N3b** (27) |
| N4 | Growth | 25 → **N4a** (13) + **N4b** (12) |
| N5 | Thinking | 12 |
| N6 | Tips | 10 |

To build each batch file list:

```bash
pnpm voice:scan | less   # prioritize flagged paths
# or list by category:
rg -l 'categories: \["Productivity"\]' content/english/notes/*.md | sort
```

**Per-note checklist (Sonnet applies; you spot-check):**

- [ ] `description` ≤ 20 words, sounds like you
- [ ] `key_concept` / shareable lines: plain, self-contained
- [ ] `relationships.reason`: specific, not template filler
- [ ] Body (if any): no em dashes, no AI tells
- [ ] `cards:` fronts/back: plain words, one idea per card

**Exit criteria:** `pnpm lint:voice` clean; spot-read ~3 random notes per category.

---

## Phase 3 — Escalation (Opus)

**Model:** **Claude Opus 4.8 (Thinking)**  
**Only when:** Sonnet pass done and the file still fails the jorap-voice primary test (“would a reader think a real person typed this?”).

**Always escalate:**

- All of session **B1** (flagship technical narrative)
- `free-grace.md`, `capture.md`, `the-golden-rule.md` (voice reference notes)
- Any file still flagged by `pnpm voice:scan` after Sonnet

**Prompt:**

```text
This file already had a Sonnet + jorap-voice pass but still sounds stiff or AI-generated.
Rewrite for voice only — same facts and links. Use jorap-voice de-AI pass. Show diff summary.
```

**Budget cap:** ~25–40 files max (~15% of corpus). If more than that need Opus, fix the Sonnet prompt first.

---

## Phase 4 — Ship

**Model:** **Composer 2.5 Fast** for changelog/commit helper only.

1. `pnpm lint:garden && pnpm lint:voice`
2. Hugo build smoke: `hugo --gc`
3. One deploy commit (content paths → **no** `[skip ci]`)
4. Optional: `@changelog-update` for `CHANGELOG.md` in a separate `[skip ci]` commit

---

## Session log (fill as you go)

| Date | Model | Batch | Files | Escalate to Opus? |
|------|--------|-------|-------|-------------------|
| 2026-07-03 | Sonnet 5 Thinking | B1 | `how-i-built-jorap-notes.md`, `top-reasons-create-maintain-your-own-website.md`, `getting-started-with-rss-feeds-beginners-guide.md` | No — all pass voice check as-is; "deploy" hits are legit tool-lane terms, not swapped |
| 2026-07-03 | Sonnet 5 Thinking | B2 | `what-i-look-for-in-wireless-earphones.md`, `top-reasons-why-you-still-need-use-desktop-laptop.md`, `facebooks-hidden-gem-...md` | No — all pass voice check as-is; zero voice-scan hits |
| 2026-07-03 | Sonnet 5 Thinking | B3 | `consistent-ai-output-wordpress-builds.md`, `hugoplate-theme-review.md`, `power-of-the-mouse-wheel-click.md` | No — "deploy"/"navigate" hits are literal tool/topic usage, not AI-tell phrasing |
| 2026-07-03 | Sonnet 5 Thinking | B4 | `alex-eala-pro-career-tracker.md` (data page), `miracle-isaiah-david.md`, `dnpap-song-resources.md`, `power-of-worship-pads-...md`, `set-it-forget-it-arroz-caldo.md`, `instant-pot-chicken-adobo.md` | No — all 15/15 published blogs pass voice check with zero rewrites |
| 2026-07-03 | Sonnet 5 Thinking | M1a | `getting-started.md`, `maps-of-content.md`, `flashcards.md`, `mental-models.md`, `pkm.md`, `eternal-principles.md`, `workplace-principles.md`, `systems-for-growth.md` | No — fixed `pkm.md` duplicate-scene examples (team manager/nurse → team manager/recipe app); rest pass as-is |
| 2026-07-03 | Sonnet 5 Thinking | M1b | `graph.md`, `backlinks.md`, `create.md`, `review.md`, `issues.md`, `okf-export.md`, `random-duo.md`, `pressure-reveals-weakness.md` | No — fixed bookend-duplicate `key_concept`/`shareable_thought` in `create.md`, `random-duo.md`, `pressure-reveals-weakness.md`; rest pass as-is |
| 2026-07-03 | Sonnet 5 Thinking | N1a | `building-a-second-brain.md`, `the-second-brain-workflow.md`, `evergreen-notes.md`, `linking-by-meaning.md`, `note-relationships.md`, `metadata-strategy.md`, `taxonomy.md`, `context-aware-capture.md`, `free-tier-hosting-stack.md`, `git-based-cms.md`, `the-garage-concept.md`, `maintenance-window.md` | No — all voice-scan word hits are legitimate on-topic/schema vocabulary (CODE method, relationship types, Cloudflare deploy terms); zero rewrites |
| 2026-07-03 | Sonnet 5 Thinking | N1b (Productivity, remaining 45) | `active-knowledge-curation.md`, `analog-capture-tools.md`, `anti-fragile-systems.md`, `atomic-notes.md`, `building-a-personal-api.md`, `capture.md`, `client-site-pass-off.md`, `commonplace-book.md`, `creative-blocks.md`, `creative-output.md`, `daily-notes.md`, `digital-garden.md`, `digital-minimalism.md`, `digital-serendipity.md`, `drafting-in-public.md`, `evergreen-vs-fleeting-notes.md`, `future-proofing-knowledge.md`, `getting-things-done.md`, `graph-view-analytics.md`, `gtd-vs-para.md`, `inbox-zero.md`, `information-diet.md`, `intellectual-sourcing.md`, `layered-reading.md`, `literature-notes.md`, `local-first-software.md`, `mind-mapping.md`, `mobile-capture-workflows.md`, `network-analysis.md`, `para-method.md`, `periodic-knowledge-review.md`, `process-over-outcomes.md`, `read-later-queue.md`, `selling-static-sites.md`, `signal-vs-noise.md`, `slow-productivity.md`, `spaced-repetition.md`, `static-site-client-scope.md`, `synthesis-as-a-goal.md`, `the-12-week-year.md`, `the-collectors-fallacy.md`, `the-feynman-technique.md`, `the-knowledge-lifecycle.md`, `the-trusted-inbox.md`, `weekly-review-checklists.md` | No — fixed bookend-duplicate `key_concept`/`shareable_thought`/`examples` in 13 files (`analog-capture-tools.md`, `creative-blocks.md`, `creative-output.md`, `daily-notes.md`, `getting-things-done.md`, `intellectual-sourcing.md`, `layered-reading.md`, `local-first-software.md`, `mind-mapping.md`, `process-over-outcomes.md`, `signal-vs-noise.md`, `spaced-repetition.md`, `the-knowledge-lifecycle.md`); rest pass as-is. **N1 (Productivity) complete.** |
| 2026-07-03 | Sonnet 5 Thinking | N2 (Leadership, all 54 non-spine files) | `accountability.md`, `attention-to-detail.md`, `blameless-after-action-review.md`, `break-the-escalation-cycle.md`, `build-a-reliable-default.md`, `change-window.md`, `coaching-ethics.md`, `complete-the-cycle.md`, `composure.md`, `control-the-rhythm.md`, `convert-pain-into-learning.md`, `develop-dont-endanger.md`, `duty-of-care.md`, `eliminate-before-managing.md`, `energy-protects-judgment.md`, `ethical-leadership.md`, `execution.md`, `expect-the-counter.md`, `finish-strong.md`, `follow-their-lead.md`, `follow-through.md`, `forgiveness-at-work.md`, `golden-rule-at-work.md`, `heed-every-near-miss.md`, `hierarchy-of-controls.md`, `incident-investigation.md`, `integrity-without-an-audience.md`, `integrity.md`, `leadership.md`, `learning-organizations.md`, `life-before-achievement.md`, `listen-before-fixing.md`, `name-the-feeling.md`, `normalization-of-deviance.md`, `outcomes-over-pitch-decks.md`, `own-the-error.md`, `plain-commitments-at-work.md`, `preparedness.md`, `priorities-before-the-inbox.md`, `psychological-safety.md`, `reconcile-before-the-review.md`, `reliability.md`, `reversibility.md`, `risk-management.md`, `rollback-principle.md`, `safety-by-design.md`, `safety-comes-first.md`, `servant-leadership.md`, `set-calm-boundaries.md`, `share-what-you-learn.md`, `situational-control.md`, `slow-the-moment.md`, `staged-rollout.md`, `stay-effective-in-new-conditions.md` | No — fixed 19 files: bookend-duplicate `key_concept`/`shareable_thought` in 16 (`attention-to-detail.md`, `build-a-reliable-default.md`, `coaching-ethics.md`, `composure.md`, `control-the-rhythm.md`, `duty-of-care.md`, `ethical-leadership.md`, `finish-strong.md`, `follow-their-lead.md`, `normalization-of-deviance.md`, `own-the-error.md`, `preparedness.md`, `reliability.md`, `safety-comes-first.md`, `situational-control.md`, `stay-effective-in-new-conditions.md`), duplicate-scene `examples` in 2 (`attention-to-detail.md`, `reconcile-before-the-review.md`), and a broken-grammar duplicated clause in 2 (`risk-management.md`, `safety-by-design.md` had "[[X]] names named rollback is..." repeating the prior sentence verbatim). Rest pass as-is. **N2 (Leadership) complete.** |
| 2026-07-03 | Sonnet 5 Thinking | N4 (Growth 25, Thinking 12, Tips remainder 1) | `adaptability.md`, `attention-economy.md`, `continuous-improvement.md`, `create-regular-connection.md`, `decision-quality.md`, `deep-work.md`, `deliberate-practice.md`, `discipline.md`, `emotional-regulation.md`, `failure-as-feedback.md`, `growth-mindset.md`, `habit-formation.md`, `habit-stacking.md`, `lean-startup.md`, `notice-the-good.md`, `quarterly-planning.md`, `recovery.md`, `resilience.md`, `self-control.md`, `ship-it.md`, `standard-operating-procedures.md`, `sustainable-performance.md`, `systems-for-growth.md`, `systems-thinking.md`, `versatility.md`, `context-aware-capture.md` (new from Tips), `behavioral-economics.md`, `compounding.md`, `first-principles-thinking.md`, `low-hanging-fruit.md`, `mental-models.md`, `minimum-effective-dose.md`, `minimum-viable-product.md`, `pareto-principle.md`, `second-order-thinking.md`, `strategic-foresight.md`, `sunk-cost-fallacy.md`, `there-is-no-perfect-solution.md` (other 9 Tips files already reviewed in N1b) | No — fixed 21 files. Systemic pattern in Growth/Thinking: many short "aphorism" notes had a `key_concept` with 2-3 paragraphs that all restated the identical clause almost verbatim (e.g. `habit-formation.md`, `habit-stacking.md`, `recovery.md`, `quarterly-planning.md` said the same line 3-4x with only word swaps). Rewrote the redundant paragraph(s) in `adaptability.md`, `attention-economy.md`, `deep-work.md`, `deliberate-practice.md`, `discipline.md`, `habit-formation.md`, `habit-stacking.md`, `lean-startup.md`, `quarterly-planning.md`, `recovery.md`, `resilience.md`, `ship-it.md`, `standard-operating-procedures.md`, `sustainable-performance.md`, `systems-thinking.md`, `versatility.md`, `behavioral-economics.md`, `compounding.md`, `first-principles-thinking.md`, `mental-models.md`, `strategic-foresight.md`, `there-is-no-perfect-solution.md`; also replaced `quarterly-planning.md`'s 4 near-identical template cards (same back text "Week ten finally bit" x4) with 4 distinct cards; fixed a broken-quote formatting bug in 2 `context-aware-capture.md` cards; fixed an "a identity verdict" grammar typo in `failure-as-feedback.md`. Rest pass as-is. **N4 (Growth, Thinking) complete.** |
| 2026-07-03 | Sonnet 5 Thinking | N3 (Faith, all 51 non-spine files) | `abide-in-me.md`, `ask-seek-knock.md`, `assurance.md`, `by-their-fruits.md`, `childlike-faith.md`, `christianity-and-politics.md`, `discipleship.md`, `dont-worry.md`, `eternal-rewards.md`, `faith-and-works.md`, `faithful-steward.md`, `faithfulness.md`, `forgiveness.md`, `free-grace.md`, `fruits-of-the-spirit.md`, `gentleness.md`, `goodness.md`, `grace.md`, `grateful-obedience.md`, `great-commission.md`, `heart-righteousness.md`, `humility-and-service.md`, `joy.md`, `judge-not.md`, `judgment-seat.md`, `justification.md`, `kindness.md`, `let-your-light-shine.md`, `let-your-yes-be-yes.md`, `loss-of-reward.md`, `love-god.md`, `love-your-enemies.md`, `love-your-neighbor.md`, `mercy.md`, `patience.md`, `peace.md`, `peacemakers.md`, `reconciliation-before-worship.md`, `render-unto-caesar.md`, `repent-and-believe.md`, `sanctification.md`, `secret-devotion.md`, `seek-the-kingdom-first.md`, `standing-vs-fellowship.md`, `take-up-your-cross.md`, `the-beatitudes.md`, `the-golden-rule.md`, `the-narrow-way.md`, `the-wise-builder.md`, `treasure-in-heaven.md`, `turn-the-other-cheek.md` (excludes `eternal-principles.md`, `success-is-stewardship.md`, already reviewed in M1a) | No — fixed 5 files: near-duplicate example scene in `free-grace.md` (two "listed good deeds like a heaven ticket" examples, one swapped for a birthday/kid scene, plus the matching duplicate flashcards); a desc-vs-key_concept near-restatement closing line in `by-their-fruits.md`, `patience.md`, and `seek-the-kingdom-first.md`; and a verbatim-repeated clause ("stop throwing more anger after sunk hurt") appearing twice in the same `key_concept` in `turn-the-other-cheek.md`. Rest pass as-is — this category's heavy cross-note theological repetition (Free Grace, Judgment Seat, standing vs fellowship, etc.) is intentional interlinking, not a voice violation. **N3 (Faith) complete.** |

---

## Cost control

- **~22 Sonnet chats** (4 blog + 1 meta + ~17 note batches) is the planned spend.
- **~5–8 Opus chats** for escalations.
- Stop mid-category and recalibrate if Sonnet rewrites feel generic — re-read `jorap-voice` reference notes before continuing.

---

## Out of scope

- `content/english/blog/__*.md` draft stubs
- Theme/layout/CSS (`layouts/`, `assets/`)
- Alex Eala tracker **data** updates (use `alex-eala-tracker-update` skill separately)
