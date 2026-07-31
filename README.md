# JoRap Notes

Personal blog and digital garden at [www.jorap.com](https://www.jorap.com). Built with Hugo, Tailwind CSS v4, and the `jorap` theme.

**Docs:** [`docs/README.md`](docs/README.md) - product voice, design system, deploy, CMS, troubleshooting.

## Requirements

Versions are pinned in [`scripts/deploy-versions.json`](scripts/deploy-versions.json).

| Tool | Version | Used for |
|------|---------|----------|
| Hugo **Extended** | 0.163.3 | Site build (Tailwind via `css.TailwindCSS`) |
| Node.js | 22.22.2+ | Scripts, Tailwind CLI, wrangler |
| pnpm | 11.7.0 | Dependencies (`packageManager` in `package.json`) |
| Go | 1.24+ | Hugo modules |
| Python | 3.8+ | Deploy OKF export, garden lint/export scripts |
| Git | any recent | Clone, hooks, CMS |

All `package.json` scripts run through Node — no Bash-only entry points.

## Local setup

### 1. Clone the repo

```bash
git clone https://github.com/jonathanrapusas/jorap.com.git
cd jorap.com
```

### 2. Install the toolchain

**Recommended on Linux, macOS, and Windows:** [mise](https://mise.jdx.dev/) reads [`.mise.toml`](.mise.toml) and installs pinned Hugo Extended, Node, Go, and pnpm.

<details>
<summary><strong>Linux</strong></summary>

**mise (recommended)**

```bash
# Install mise — see https://mise.jdx.dev/getting-started.html
curl https://mise.run | sh
# Restart your shell, then:
cd jorap.com
mise trust
mise install
```

**Manual installs** (if you skip mise)

| Tool | Example |
|------|---------|
| Hugo Extended | [GitHub releases](https://github.com/gohugoio/hugo/releases) (`hugo_extended_*_linux-amd64.tar.gz` or `arm64`) |
| Node 22 | [nodejs.org](https://nodejs.org/) or your distro package manager |
| pnpm 11 | `corepack enable && corepack prepare pnpm@11.7.0 --activate` |
| Go 1.24+ | [go.dev/dl](https://go.dev/dl/) or `sudo apt install golang-go` |
| Python 3.8+ | Usually `python3` via `sudo apt install python3` |

Use any shell (bash, zsh, fish). Open a **new terminal** in the repo so `mise` shims are on `PATH`.

</details>

<details>
<summary><strong>macOS</strong></summary>

**mise (recommended)**

```bash
brew install mise          # or: curl https://mise.run | sh
cd jorap.com
mise trust
mise install
```

**Manual installs** (if you skip mise)

| Tool | Example |
|------|---------|
| Hugo Extended | `brew install hugo` (Homebrew ships Extended) |
| Node 22 | `brew install node@22` or [nodejs.org](https://nodejs.org/) |
| pnpm 11 | `corepack enable && corepack prepare pnpm@11.7.0 --activate` |
| Go 1.24+ | `brew install go` |
| Python 3.8+ | `brew install python` (macOS may also ship `python3`) |

Works in Terminal.app, iTerm, or any zsh/bash shell. After `mise install`, open a new tab or run `mise activate` in the current session.

</details>

<details>
<summary><strong>Windows</strong></summary>

**mise (recommended)**

```powershell
# Install mise — see https://mise.jdx.dev/getting-started.html
winget install -e --id jdx.mise
# Restart the terminal; ensure %LOCALAPPDATA%\mise\shims is on PATH (winget/Scoop usually handle this)
cd jorap.com
mise trust
mise install
```

**Manual installs** (if you skip mise)

| Tool | Example |
|------|---------|
| Hugo Extended | [GitHub releases](https://github.com/gohugoio/hugo/releases) (`hugo_extended_*_windows-amd64.zip`) — add `hugo.exe` to `PATH` |
| Node 22 | [nodejs.org](https://nodejs.org/) or `winget install OpenJS.NodeJS.LTS` |
| pnpm 11 | `corepack enable` then `corepack prepare pnpm@11.7.0 --activate` |
| Go 1.24+ | [go.dev/dl](https://go.dev/dl/) or `winget install GoLang.Go` |
| Python 3.8+ | [python.org](https://www.python.org/downloads/) or `winget install Python.Python.3.12` — enable “Add to PATH” |

Use **PowerShell**, **cmd**, or **Git Bash**. Scripts resolve Python as `python`, `python3`, or `py -3`; set `PYTHON` if needed.

**Windows notes**

- **Put the toolchain on PATH first** — local builds do **not** auto-download Hugo (`scripts/ensureHugo.mjs` only fetches Hugo in CI). If `hugo`, `node`, `pnpm`, or `python` is “not recognized”, finish `mise install` (or manual installs above) and open a **new terminal** in the repo. Confirm `%LOCALAPPDATA%\mise\shims` is on PATH if you use mise.
- **No symlink or Developer Mode setup** — `postinstall` writes a Tailwind shim (`scripts/fix-tailwind-bin.js`) including a Hugo-parseable CRLF `tailwindcss.cmd`.
- **Hoisted installs** — `nodeLinker: hoisted` in [`pnpm-workspace.yaml`](pnpm-workspace.yaml) so Hugo’s `js.Build` can resolve PixiJS deps on Windows (pnpm 11 ignores `node-linker` in `.npmrc`). Tailwind is still fixed by the postinstall shim, not symlinks.
- **Do not skip postinstall** — `pnpm install --ignore-scripts` skips the Tailwind shim. Run `node scripts/fix-tailwind-bin.js` before building, or reinstall without `--ignore-scripts`.
- **After pulling dependency fixes** — see **What to do on Windows** below. An existing isolated `node_modules` layout will not migrate on its own; delete it before reinstalling.

**What to do on Windows** (after `git pull`, or if Pixi/Tailwind build errors persist):

```powershell
git pull
Remove-Item -Recurse -Force node_modules
pnpm install
node scripts/fix-tailwind-bin.js --self-check
pnpm run deploy
```

After `pnpm install`, confirm:

- `node_modules\.modules.yaml` contains `"nodeLinker": "hoisted"`
- `node_modules\.bin\tailwindcss.cmd` is ~3 lines with `fix-tailwind-bin-shim` and `%~dp0\..\@tailwindcss\cli\dist\index.mjs` (not pnpm’s 900-byte wrapper)
- `node_modules\.bin\tailwindcss` (no extension) should **not** exist — Windows uses `.cmd` only

`PYTHONIOENCODING=utf-8` is no longer required (scripts set UTF-8 for Python), but leaving it set is harmless.

Verify toolchain (optional, before deploy):

```powershell
hugo version    # must include "extended" and v0.163.x
node -v
pnpm -v
py -3 --version
go version
```

| Symptom | Fix |
|---------|-----|
| `hugo` / `pnpm` / `python` not recognized | Install tools (mise recommended); restart the terminal |
| `binary "tailwindcss" is not a Node.js script` | Follow **What to do on Windows** above |
| `Could not resolve "@pixi/…"` or other `js.Build failed` | Follow **What to do on Windows** above |
| Hugo version mismatch on local build | `mise install`, or install the pinned version from [`scripts/deploy-versions.json`](scripts/deploy-versions.json) |

First production preview may download wrangler via `npx` when you run `pnpm run serve`.

</details>

### 3. Install dependencies

From the repo root (Linux, macOS, or Windows):

```bash
pnpm install
```

`postinstall` runs `fix-tailwind-bin.js` so Hugo can execute Tailwind under pnpm (all platforms).

Optional — git hooks that auto-append `[skip ci]` for non-deploy commits:

```bash
pnpm setup:hooks
```

### 4. Verify the toolchain

```bash
hugo version          # must include "extended" and v0.163.x
node -v               # v22.22.2 or newer
pnpm -v               # 11.7.0
go version            # go1.24 or newer
python3 --version     # Windows: py -3 --version
node scripts/fix-tailwind-bin.js --self-check
```

Quick build smoke test (same command Cloudflare Pages runs):

```bash
pnpm run deploy
```

### 5. Run the site

**Development** (drafts + future-dated posts, live reload):

```bash
pnpm dev
```

Open http://localhost:1313

**Production preview** (matches Cloudflare Pages — minified output, CSP hashes, `_headers`, Functions):

```bash
pnpm local              # build + serve (alias: pnpm run preview:prod)
```

Open http://127.0.0.1:8788

Or in two steps:

```bash
pnpm run deploy         # production build → public/
pnpm run serve          # wrangler pages dev on port 8788
```

CMS OAuth locally: copy [`.dev.vars.example`](.dev.vars.example) → `.dev.vars` and fill GitHub OAuth values.

### Cross-platform notes

| Concern | How this repo handles it |
|---------|--------------------------|
| Toolchain versions | [mise](https://mise.jdx.dev/) + [`.mise.toml`](.mise.toml), or manual installs per table above |
| Python scripts | `node scripts/runPython.mjs` — tries `python3`, `python`, then Windows `py -3`; set `PYTHON` to override |
| Local binaries | `spawnUtil.mjs` resolves `node_modules/.bin` (`.cmd` / `.ps1` on Windows) |
| Tailwind + Hugo + pnpm | `postinstall` + `deployBuild.mjs` fix Tailwind bin; `pnpm-workspace.yaml` hoists deps for `js.Build` on Windows |
| Git hooks | `pnpm setup:hooks` — pure Node |
| Safe filenames | `pnpm lint:filenames` / `pnpm test:filenames` — pure Node |

More troubleshooting: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md#local-dev).

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
