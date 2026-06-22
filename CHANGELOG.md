# Changelog

Site **functionality** shipped to [jorap.com](https://jorap.com). Entries are appended automatically on commit when staged files touch code, layout, config, or build tooling (content paths are ignored). Deploys run on **Cloudflare Pages** via `pnpm run deploy`.

Commit prefix → section: `fix:` / `Fixes` → **Fixed**; `feat:` / `add:` → **Added**; otherwise → **Changed**.

---

## 2026-06-22

### Changed

- Centralized agent skills under `.cursor/skills/` (moved from `.agents/skills/`)
- Sync-upstreams and ponytail-help skill doc tweaks
- `assets/css/custom.css`
- `layouts/_partials/components/theme-switcher.html`
- `package.json`
- `scripts/installGitHooks.mjs`
- `scripts/updateChangelog.mjs`
- `assets/js/main.js`
- `assets/js/notes-graph.js`
- `data/theme.json`
- `layouts/_partials/essentials/header.html`
- `layouts/baseof.html`
- `layouts/notes/review.html`
- `themes/jorap/assets/css/generated-theme.css`


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
