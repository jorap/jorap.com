# Preserve Lists

JoRap has **forked** Hugoplate’s theme — not just added a few partials. Upstream sync is a **diff triage**, not a copy.

See [SKILL.md](SKILL.md) for the full workflow. Use [triage-hugoplate.sh](triage-hugoplate.sh) to classify changes before applying anything.

---

## Tier 1 — Never overwrite from upstream

### Site root (not from Hugoplate)

- `content/`, `config/`, `data/`, `hugo.toml`
- Root `layouts/`, `assets/`, `functions/`, `docs/`, `static/`, `_vendor/`
- Deployment config (`vercel-build.sh.disabled`, etc.)

### Theme layouts — JoRap-owned

JoRap uses different page structures, semantic markup, and partials. **Do not take upstream wholesale** for:

| Path | Why |
| --- | --- |
| `home.html` | JoRap homepage uses `sections/home-*` partials, not Hugoplate banner/features |
| `baseof.html` | Shell wiring for JoRap header/footer/scripts |
| `blog/single.html` | Mobile TOC, social share, semantic tokens, icon partial |
| `_partials/essentials/head.html` | `theme-init.html`, theme name `jorap`, CSP-friendly head |
| `_partials/essentials/header.html` | Nav dropdown JS hooks, semantic classes |
| `_partials/essentials/style.html` | Self-hosted fonts — **not** Google Fonts CDN |
| `_partials/essentials/script.html` | JoRap script bundle order |
| `_partials/essentials/footer.html` | JoRap footer markup |
| `_partials/essentials/self-hosted-fonts.html` | JoRap-only |
| `_partials/essentials/theme-init.html` | FOUC-free dark mode bootstrap |
| `_partials/components/blog-card.html` | JoRap card design + semantic tokens |
| `_partials/components/theme-switcher.html` | Works with `theme-init` |
| `_partials/components/icon.html`, `image.html`, `image-process.html`, `social-share.html`, `back-to-top.html` | JoRap-only |
| `_partials/sections/*` | JoRap homepage/section partials |
| `about/list.html`, `contact/list.html` | JoRap replaced upstream `about.html` / `contact.html` |
| `shortcodes/spotify*`, `youtube*` | JoRap-only |
| `_markup/render-heading.html` | JoRap heading anchors |

Also block: `about.html`, `contact.html` (upstream layouts JoRap intentionally removed).

### Theme assets — JoRap design system

| Path | Why |
| --- | --- |
| `assets/css/**` | JoRap semantic token system (`text-ink`, `bg-surface`, etc.) |
| `assets/css/semantic-tokens.css` | Maps palette → semantic utilities; auto dark mode |
| `assets/css/generated-theme.css` | Regenerate via `pnpm build` / `themeGenerator.js` |
| `assets/js/main.js` | Nav dropdown handlers + guarded Swiper init |

### Scripts — JoRap-only or customized

| File | Notes |
| --- | --- |
| `scripts/cspHashes.mjs` | JoRap-only; part of `pnpm build` |
| `scripts/projectSetup.js`, `scripts/themeSetup.js` | Theme name `jorap` |
| `scripts/removeDarkmode.js` | May differ from upstream |
| All `scripts/*.py`, `noteFileDates.js`, `responsive-*.mjs` | JoRap-only |

### package.json fields to keep

- `name`, `description`, `version`, `author`, `engines`
- Custom scripts: `build` (includes `cspHashes`), `watch`, note/anki scripts

---

## Tier 2 — Manual merge only (read diff, cherry-pick hunks)

Apply upstream changes **only when the diff is a clear bugfix** and does not touch JoRap fork signals.

**Red flags in a diff → skip or merge by hand:**

- Switches `text-ink` / `bg-surface` ↔ `text-text` / `bg-body` / `dark:*`
- Removes `theme-init`, `self-hosted-fonts`, or JoRap partial references
- Adds Google Fonts CDN, Font Awesome, or social CDN preconnects
- Changes `theme-name` to `hugoplate`
- Large structural rewrites of pages JoRap customized

**Examples that may be worth cherry-picking:**

- Accessibility fix in a widget JoRap still uses unchanged
- Hugo template syntax fix that doesn’t alter JoRap markup/classes
- New upstream partial that JoRap doesn’t conflict with ( rare )

When in doubt: **skip**.

---

## Tier 3 — Usually safe (still read diff first)

### New upstream files JoRap doesn’t have

- Add if path is not JoRap-specific and not in Tier 1
- Example: new plugin under `assets/plugins/` if JoRap doesn’t override it

### Root scripts (identical purpose, no JoRap edits)

- `scripts/themeGenerator.js`
- `scripts/clearModules.js`
- `scripts/removeMultilang.js`

If JoRap’s copy already matches upstream (`diff -q`), skip.

### Agent skills from Hugoplate

- `.cursor/skills/hugo-template-guidance/` — sync from Hugoplate `$HUGO/.agents/skills/`, then **re-apply JoRap local notes** (e.g. `__` draft-post convention in `content-management.md`)
- `.cursor/skills/find-skills/` — sync wholesale from upstream

### package.json

- Merge new `devDependencies` from Hugoplate only
- Never replace JoRap scripts block

---

## Impeccable — preserve during skill sync

- `docs/PRODUCT.md`, `docs/DESIGN.md`, `docs/DESIGN.json`
- `.impeccable/` — live config, critique ignores, session journals

Verify with `node .cursor/skills/impeccable/scripts/context.mjs` (not `load-context.mjs`).

---

## Structural differences

| Hugoplate | JoRap.com |
| --- | --- |
| Theme at repo root | Theme at `themes/jorap/` |
| `theme = "hugoplate"` | `theme = "jorap"` |
| `exampleSite/` demo | Site at repo root (project-setup) |
| Old Tailwind token names + `dark:` twins | Semantic tokens in `semantic-tokens.css` |
| Google Fonts CDN | Self-hosted fonts partial |
| `pnpm update-theme` | **Do not run** — wrong path/name. Use this skill. |

---

## What went wrong (2025 sync lesson)

Bulk `rsync` of `layouts/` + `assets/` copied Hugoplate’s old token CSS while JoRap layouts still used `text-ink`, `bg-surface`, etc. — breaking typography, dark mode, prose, nav, and fonts. **Default workflow must triage diffs, not rsync.**
