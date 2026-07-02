# Docs

Long-form documentation for the JoRap Notes project. The repo [`README.md`](../README.md) covers quick start; everything below is reference material for humans and agents.

## Index

| File | What it covers |
| --- | --- |
| [`SPEC.md`](./SPEC.md) | Complete platform specification: users, requirements, notes garden, success criteria. Start here for *what the system is*. |
| [`../specs/`](../specs/) | Feature-specific speckit specs (plan → tasks → implement). |
| [`PRODUCT.md`](./PRODUCT.md) | Audience, voice, anti-references, design principles. Start here for *why*. |
| [`DESIGN.md`](./DESIGN.md) | Visual system: north star, tokens, typography, components, notes garden. Start here for *how it looks*. |
| [`DESIGN.json`](./DESIGN.json) | Machine-readable design sidecar (palette meta, components, narrative) for tooling. |
| [`.impeccable/design.json`](../.impeccable/design.json) | Same schema as `DESIGN.json`; consumed by the Impeccable live panel. Keep in sync when tokens change. |
| [`CMS_SETUP.md`](./CMS_SETUP.md) | One-time setup for Static Site CMS (`/admin`). |
| [`CLIENT_STATIC_SITE.md`](./CLIENT_STATIC_SITE.md) | Client template: Hugo + GitHub + Cloudflare Pages checklist. |
| [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) | Deploy, redirects, CMS, and build gotchas. |
| [`TODO.md`](./TODO.md) | Working backlog (shipped vs open). |

## Canonical URLs

- **Live site:** [https://www.jorap.com](https://www.jorap.com)
- **Apex redirect:** `jorap.com` → `www.jorap.com` via [`static/_redirects`](../static/_redirects) (both hosts must be attached in Cloudflare Pages).

## Token sources (code)

| Source | Role |
| --- | --- |
| [`data/theme.json`](../data/theme.json) | Authoritative color and font scale; edit here first. |
| [`themes/jorap/assets/css/generated-theme.css`](../themes/jorap/assets/css/generated-theme.css) | Auto-generated Tailwind `@theme` vars (`node scripts/themeGenerator.js`). |
| [`themes/jorap/assets/css/semantic-tokens.css`](../themes/jorap/assets/css/semantic-tokens.css) | Semantic aliases (`surface`, `elevated`, `ink`, `accent`, …) with dark swaps. |

When adding a new doc, drop it in this folder and link it from the table above.
