# JoRap Notes

Personal blog and digital garden at [www.jorap.com](https://www.jorap.com). Built with Hugo, Tailwind CSS v4, and the `jorap` theme.

**Docs:** [`docs/README.md`](docs/README.md) - product voice, design system, deploy, CMS, troubleshooting.

## Requirements

Versions are pinned in [`scripts/deploy-versions.json`](scripts/deploy-versions.json). Local dev typically uses [mise](https://mise.jdx.dev/) (see [`.mise.toml`](.mise.toml)).

| Tool | Version |
|------|---------|
| Hugo Extended | 0.163.3 |
| Node.js | 22+ |
| pnpm | 11.7.0 |
| Go | 1.24+ |
| Python | 3.8+ (deploy + garden lint/export scripts) |

## Platforms (Windows, Linux, macOS)

All `package.json` scripts run through Node — no Bash-only entry points. Use PowerShell, cmd, or Git Bash on Windows; any shell on Linux and macOS.

| Concern | How this repo handles it |
|---------|--------------------------|
| Toolchain | [mise](https://mise.jdx.dev/) + [`.mise.toml`](.mise.toml) installs Hugo, Node, Go, and pnpm on all three OSes (`mise install`) |
| Python scripts | `node scripts/runPython.mjs` resolves `python3`, `python`, or Windows `py -3`; set `PYTHON` to override |
| Local binaries | `spawnUtil.mjs` finds `node_modules/.bin` shims (`.cmd` on Windows) |
| Tailwind + Hugo | `postinstall` symlinks or copies `tailwindcss` when Windows blocks symlinks |
| Git hooks | `pnpm setup:hooks` — pure Node, no `sh` required |
| Filename lint | `pnpm lint:filenames` / `pnpm test:filenames` — pure Node, no Python or shell |

More troubleshooting: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md#local-dev).

## Quick start

```bash
git clone https://github.com/jonathanrapusas/jorap.com.git
cd jorap.com
mise install          # optional — pinned Hugo, Node, Go, pnpm
pnpm install
pnpm dev
```

Open http://localhost:1313

## Local production preview

Test the same build Cloudflare Pages ships — minified Hugo output, CSP hashes, `_headers`, and Functions (not `pnpm dev`, which includes drafts and future-dated posts).

```bash
pnpm install
pnpm local              # build + serve (alias: pnpm run preview:prod)
```

Open http://127.0.0.1:8788

Or in two steps:

```bash
pnpm run deploy         # production build → public/
pnpm run serve          # wrangler pages dev on port 8788
```

**Needs:** Hugo Extended, Node 22+, pnpm, Go, and Python 3.8+ (OKF export step). `mise install` or manual installs all work on Windows, Linux, and macOS. First `serve` may download wrangler via `npx` if it is not installed locally.

CMS OAuth locally: copy `.dev.vars.example` → `.dev.vars` and fill GitHub OAuth values.

## Common commands

| Command | What it does |
|---------|----------------|
| `pnpm dev` | Dev server (Tailwind watch + note dates + Hugo) |
| `pnpm local` | Production build + local serve (Cloudflare parity) |
| `pnpm run deploy` | Production build to `public/` |
| `pnpm run serve` | Serve `public/` with wrangler (after deploy) |
| `pnpm run preview:prod` | Same as `pnpm local` |
| `pnpm run preview` | Hugo prod-mode server with watch (includes drafts/future) |
| `pnpm run lint:notes` | Garden wikilink lint via Hugo build |
| `pnpm run lint:cards` | Flashcard frontmatter lint |
| `pnpm lint:filenames` | Cross-platform filename safety (git-tracked) |
| `pnpm test:filenames` | Filename lint self-check (no git) |
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

- **Settings → Build → Variables** - set `NODE_VERSION` and `GO_VERSION` (build-time vars; `wrangler.toml [vars]` are runtime-only). Hugo is pinned in [`scripts/deploy-versions.json`](scripts/deploy-versions.json).
- **Settings → Build → Build cache → Enable.**

```bash
pnpm setup:hooks   # auto [skip ci] for .specstory / docs-only commits
```

Client site template: [`docs/CLIENT_STATIC_SITE.md`](docs/CLIENT_STATIC_SITE.md). Functional changes go in [`CHANGELOG.md`](CHANGELOG.md) via the `changelog-update` Cursor skill.

## Theme upstream

To sync Hugoplate or Impeccable upstreams, use the `sync-upstreams` Cursor skill - not the old Hugoplate one-shot setup scripts.

## License

MIT
