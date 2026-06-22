# Changelog

Site **functionality** shipped to [jorap.com](https://jorap.com). Update via the `changelog-update` Cursor skill (git diffs + SpecStory session history). Deploys run on **Cloudflare Pages** via `pnpm run deploy`.

Commit prefix → section: `fix:` / `Fixes` → **Fixed**; `feat:` / `add:` → **Added**; otherwise → **Changed**.

---

## 2026-06-22

### Added

- Shortest wikilink path on random duo and single-note random sections; path included in AI prompt when found
- Notes graph: top/middle/bottom rank filters, relationship-type filters, and color-by-tag mode
- Notes graph lazy init (IntersectionObserver) with 240-node cap on the global view
- Skip-to-content link, nav dropdown keyboard navigation, and accessible theme-switcher button partial
- Semantic warning/error/success/graph-weak theme tokens (replacing hardcoded banner and status colors)
- `changelog-update` Cursor skill for human-readable changelog entries (SpecStory + git diffs)

### Changed

- Random note/duo shuffle buttons moved to each dropdown; duo “shuffle both” beside the shortest-path toolbar
- Agent skills centralized under `.cursor/skills/` (moved from `.agents/skills/`)
- Notes review card labels: sentence case and larger type
- Graph hub/weak percentile config replaced with `graph_tail_percentile`
- Touch targets (44px) and focus-visible rings on filters, buttons, footer social icons, and nav CTA
- Flashcard flip respects `prefers-reduced-motion`
- Changelog: agent skill replaces commit-time file-path hook

---

## 2026-06-21

### Added

- Expanded notes list filters (status, featured, cards, issues, stale) with counts
- `notes-random-core.js` shared module for random-note features
- `scripts/ensureHugo.mjs` for pinned Hugo Extended in CI and deploy

### Changed

- Notes graph: filter suffix behavior and mobile toolbar stickiness
- Hugo **0.163.3** across Cloudflare, Wrangler, and `deploy-versions.json`
- Asset pipeline: fingerprint/integrity handling in `style.html` partials

### Fixed

- Local graph and notes display issues on some viewports
- Cloudflare deploy env alignment (`deferred-media.js`, wrangler config)

---

## 2026-06-20

### Added

- Interactive notes graph rebuilt on **PixiJS** (force-directed, filters, present mode)
- Asset fingerprint partial for cache-safe JS/CSS URLs
- `scripts/ensureHugo.mjs`; deploy build hardening in `deployBuild.mjs`
- `_redirects` entry for graph/flashcards routes

### Changed

- Notes flashcards routes and toolbar (`flashcards.md`, layouts)
- `custom.css` graph panel, filter chips, and touch-target utilities

### Fixed

- Hugo template/build errors blocking production graph page
- Graph boot failure on strict CSP / missing `unsafe-eval` handling

---

## 2026-06-19

### Changed

- Home intro and navigation params (`config/_default/params.toml`)
- Blog random-notes script behavior (`blog-random-notes.js`)

---

## 2026-05-28 – 2026-06-03

### Added

- `static/_headers` for long-cache immutable assets on Cloudflare
- `layouts/_partials/basic-seo.html` SEO partial

### Changed

- Blog card component and `module-overrides.css` polish
- TOC behavior fix

### Fixed

- Production deploy and TOC regressions (May 14 revert cycle resolved)

---

## 2026-05-02 – 2026-05-04

### Added

- `docs/PRODUCT.md` and `docs/DESIGN.md` (Impeccable design system)
- Inter-only typography stack; semantic color tokens via `tw-theme.js`

### Changed

- Dark mode prose and Tailwind v4 token wiring
- Impeccable critique/polish pass on marketing shell

### Fixed

- Image processing and Tailwind build errors

---

## Earlier

Site bootstrapped from Hugoplate with the `jorap` theme fork, notes garden, flashcards, and Cloudflare Pages deploy. See git history before 2026-05-02 for incremental theme and tooling work.
