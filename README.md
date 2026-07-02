# JoRap Notes

Personal blog and digital garden at [www.jorap.com](https://www.jorap.com). Built with Hugo, Tailwind CSS v4, and the `jorap` theme.

**Docs:** [`docs/README.md`](docs/README.md) — product voice, design system, deploy, CMS, troubleshooting.

## Requirements

Versions are pinned in [`scripts/deploy-versions.json`](scripts/deploy-versions.json). Local dev typically uses [mise](https://mise.jdx.dev/) (see [`.mise.toml`](.mise.toml)).

| Tool | Version |
|------|---------|
| Hugo Extended | 0.163.3 |
| Node.js | 20+ |
| pnpm | 11.7.0 |
| Go | 1.24+ |

## Quick start

```bash
git clone https://github.com/jonathanrapusas/jorap.com.git
cd jorap.com
pnpm install
pnpm dev
```

Open http://localhost:1313

## Common commands

| Command | What it does |
|---------|----------------|
| `pnpm dev` | Dev server (Tailwind watch + note dates + Hugo) |
| `pnpm run deploy` | Production build to `public/` |
| `pnpm run serve` | Serve `public/` locally |
| `pnpm run preview` | One-shot production Hugo server |
| `pnpm run lint:notes` | Garden wikilink lint via Hugo build |
| `pnpm run lint:cards` | Flashcard frontmatter lint |
| `pnpm run format` | Prettier |

## Project layout

```
content/english/     Blog posts, notes garden, pages
layouts/             Site-specific Hugo templates
themes/jorap/        Active theme (tokens in data/theme.json)
assets/js/           Site JavaScript (graph, random notes, flashcards)
assets/css/          Site overrides (notes garden, a11y)
static/              _headers, _redirects (copied to public/ by Hugo)
scripts/             Build, deploy, and content tooling
docs/                Product, design system, deploy guides
```

## Content

- **Blog:** `content/english/blog/`
- **Notes garden:** `content/english/notes/`
- **Getting started:** `content/english/notes/getting-started.md`

New notes: `hugo new content/english/notes/my-note.md`

## Deploy

Production deploy is `pnpm run deploy`. Cloudflare Pages runs the same command (see [`wrangler.toml`](wrangler.toml)). Hugo writes to `.cache` (via `--cacheDir` in `deployBuild.mjs`) so Cloudflare's build cache can reuse it. One-time Pages setup (dashboard):

- **Settings → Build → Variables** — set `NODE_VERSION` and `GO_VERSION` (build-time vars; `wrangler.toml [vars]` are runtime-only). Hugo is pinned in [`scripts/deploy-versions.json`](scripts/deploy-versions.json).
- **Settings → Build → Build cache → Enable.**

```bash
sh scripts/setup-git-hooks.sh # auto [skip ci] for .specstory / docs-only commits
```

Client site template: [`docs/CLIENT_STATIC_SITE.md`](docs/CLIENT_STATIC_SITE.md). Functional changes go in [`CHANGELOG.md`](CHANGELOG.md) via the `changelog-update` Cursor skill.

## Theme upstream

To sync Hugoplate or Impeccable upstreams, use the `sync-upstreams` Cursor skill — not the old Hugoplate one-shot setup scripts.

## License

MIT
