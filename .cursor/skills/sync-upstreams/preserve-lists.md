# Preserve Lists

Files and paths that must **not** be overwritten blindly when syncing from Hugoplate or Impeccable.

## JoRap-only — never delete or replace from upstream

### Site root (not from Hugoplate)

- `content/` — all posts, pages, authors, sections
- `config/` — menus, params, module.toml, languages
- `data/` — theme.json and site data
- `hugo.toml` — site config (theme name `jorap`, baseURL, security, etc.)
- `layouts/` at repo root — site-level overrides (e.g. `layouts/_partials/basic-seo.html`)
- `assets/` at repo root — site-level JS (e.g. `assets/js/gallery-slider.js`)
- `functions/` — Cloudflare Pages Functions (auth, API)
- `docs/` — PRODUCT.md, DESIGN.md, DESIGN.json, project docs
- `static/` — static assets, admin CMS
- `_vendor/` — vendored Hugo modules
- `vercel-build.sh.disabled`, deployment config

### Theme: JoRap-only layouts (`themes/jorap/layouts/`)

```
_markup/render-heading.html
_partials/components/back-to-top.html
_partials/components/icon.html
_partials/components/image-process.html
_partials/components/image.html
_partials/components/social-share.html
_partials/essentials/self-hosted-fonts.html
_partials/essentials/theme-init.html
_partials/sections/banner.html
_partials/sections/blog-list.html
_partials/sections/features.html
_partials/sections/home-intro.html
_partials/sections/testimonials.html
about/list.html
contact/list.html
shortcodes/spotify.html
shortcodes/spotify_iframe_artist.html
shortcodes/spotify_iframe_track.html
shortcodes/youtube.html
shortcodes/youtube_time.html
```

JoRap uses `about/list.html` and `contact/list.html` instead of Hugoplate's `about.html` and `contact.html`. Do not revert to the upstream single-file layouts without explicit user approval.

### Theme: JoRap-only assets

- `themes/jorap/assets/css/semantic-tokens.css`

### Scripts: JoRap-only or customized

| File | Notes |
| --- | --- |
| `scripts/cspHashes.mjs` | JoRap-only; part of `pnpm build` |
| `scripts/projectSetup.js` | Customized for theme name `jorap` |
| `scripts/themeSetup.js` | Customized for theme name `jorap` |
| `scripts/removeDarkmode.js` | May differ from upstream |

### package.json fields to keep

- `name`, `description`, `version`, `author`, `engines`
- Custom scripts: `build` (includes cspHashes), `watch`, simplified `dev:example` variants

---

## Impeccable — preserve during skill sync

- `docs/PRODUCT.md`
- `docs/DESIGN.md`
- `docs/DESIGN.json`
- `.impeccable/` — live config, critique ignores, session journals

---

## Safe to sync from Hugoplate (review diff first)

### Shared theme layouts (examples — not exhaustive)

Most files under `themes/jorap/layouts/` that also exist in hugoplate `layouts/` can track upstream, especially:

- `_partials/essentials/` (except `self-hosted-fonts.html`, `theme-init.html`)
- `_partials/components/` (except JoRap-only list above)
- `_partials/widgets/`
- `baseof.html`, `home.html`, `list.html`, `single.html`, `blog/`, `authors/`, `404.en.html`

### Shared theme assets

Upstream can update: `assets/plugins/`, most CSS files (merge manually if JoRap customized tokens), `assets/js/main.js`.

Regenerate after CSS/token changes: `pnpm build` runs `themeGenerator.js` → `generated-theme.css`.

### Root scripts (usually safe)

- `scripts/themeGenerator.js`
- `scripts/themeUpdate.js`
- `scripts/clearModules.js`
- `scripts/removeMultilang.js`

### Agent skills

- `.agents/skills/hugo-template-guidance/` — copy wholesale from Hugoplate
- `.agents/skills/find-skills/` — copy wholesale from Hugoplate

---

## Structural differences to remember

| Hugoplate | JoRap.com |
| --- | --- |
| Theme at repo root | Theme at `themes/jorap/` |
| `theme = "hugoplate"` | `theme = "jorap"` |
| `exampleSite/` demo | Site at repo root (project-setup) |
| `pnpm update-theme` pulls from GitHub tarball to `themes/hugoplate` | **Do not run** `update-theme` as-is — it targets the wrong path/name. Use this skill instead. |
