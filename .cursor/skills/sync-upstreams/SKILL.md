---
name: sync-upstreams
description: Sync JoRap.com with local upstream checkouts of Hugoplate (Hugo theme) and Impeccable (design skills). Use when the user asks to update the theme, pull upstream changes, sync hugoplate/impeccable, refresh agent skills, or merge upstream into jorap.com.
---

# Sync Upstreams

JoRap.com is a **project-setup** Hugo site (`theme = "jorap"` in `hugo.toml`) forked from [Hugoplate](https://github.com/zeon-studio/hugoplate). Design work uses the [Impeccable](https://github.com/pbakaus/impeccable) skill in `.cursor/skills/impeccable/`.

Unless noted otherwise, paths below are **relative to the jorap.com repo root**. Upstream checkouts live as sibling folders one level up (`../hugoplate`, `../impeccable`).

Local source checkouts (sibling folders — one level up from jorap.com):

| Upstream | Path (from jorap.com root) |
| --- | --- |
| Hugoplate | `../hugoplate` |
| Impeccable | `../impeccable` |

**Never blind-copy the whole repo.** JoRap has site-specific theme files, scripts, content, Cloudflare Functions, and design context that upstream does not have. Sync selectively and review diffs.

## Quick routing

| User wants | Follow |
| --- | --- |
| Update Hugo theme / Hugoplate | [Hugoplate sync](#hugoplate-sync) |
| Update Impeccable skill / design commands | [Impeccable sync](#impeccable-sync) |
| Update both | Hugoplate first, then Impeccable, then verify build |
| Understand what not to overwrite | [preserve-lists.md](preserve-lists.md) |

---

## Pre-flight (both upstreams)

1. In each source repo, fetch and pull latest:

```bash
cd ../hugoplate && git pull
cd ../impeccable && git pull
```

2. In jorap.com, confirm clean working tree or stash first:

```bash
git status
```

3. Package manager here is **pnpm** (`pnpm-lock.yaml`).

---

## Hugoplate sync

Hugoplate's theme lives at its repo root (`layouts/`, `assets/`). JoRap vendors it as **`themes/jorap/`** (renamed from `hugoplate`).

### Path mapping

| Hugoplate source | JoRap.com target |
| --- | --- |
| `layouts/` | `themes/jorap/layouts/` |
| `assets/` | `themes/jorap/assets/` |
| `scripts/` | `scripts/` (selective — see preserve list) |
| `.agents/skills/` | `.agents/skills/` |
| `AGENTS.md` | Review for new agent rules; merge relevant sections only |

Do **not** copy `exampleSite/`, `theme.toml`, or hugoplate's `package.json` wholesale.

### Recommended workflow

```
Task progress:
- [ ] Pull hugoplate
- [ ] Diff theme (layouts + assets)
- [ ] Merge shared files; skip JoRap-only paths
- [ ] Diff and merge root scripts
- [ ] Sync .agents/skills if changed
- [ ] pnpm install (if package.json deps changed)
- [ ] pnpm build
- [ ] Review git diff; summarize for user
```

**Step 1 — Diff theme folders** (run from jorap.com root):

```bash
HUGO=../hugoplate
diff -rq "$HUGO/layouts" themes/jorap/layouts
diff -rq "$HUGO/assets" themes/jorap/assets
```

**Step 2 — Copy only safe upstream files.** For files that exist in both repos and should track upstream, copy individually after reviewing the diff. Example:

```bash
HUGO=../hugoplate
cp "$HUGO/layouts/_partials/essentials/header.html" themes/jorap/layouts/_partials/essentials/header.html
```

For bulk sync of files that are **identical in purpose** and not in the preserve list, `rsync` with excludes:

```bash
HUGO=../hugoplate

rsync -av --delete \
  --exclude-from=.cursor/skills/sync-upstreams/hugoplate-rsync-excludes.txt \
  "$HUGO/layouts/" themes/jorap/layouts/

rsync -av \
  --exclude-from=.cursor/skills/sync-upstreams/hugoplate-rsync-excludes.txt \
  "$HUGO/assets/" themes/jorap/assets/
```

Use `--delete` on `layouts/` only when the user explicitly wants orphan upstream files removed. Default: **no `--delete`** — add new upstream files, update changed shared files, leave JoRap-only files alone.

**Step 3 — Root scripts.** Compare and merge:

```bash
diff -rq ../hugoplate/scripts scripts
```

Safe to take upstream as-is: `themeGenerator.js`, `themeUpdate.js`, `clearModules.js`, `removeMultilang.js`.

Merge carefully (JoRap uses theme name `jorap`): `projectSetup.js`, `themeSetup.js`, `removeDarkmode.js`.

Never remove: `scripts/cspHashes.mjs` (JoRap-only; wired into `pnpm build`).

**Step 4 — Agent skills from Hugoplate:**

```bash
HUGO=../hugoplate
mkdir -p .agents/skills
rsync -av "$HUGO/.agents/skills/" .agents/skills/
```

**Step 5 — package.json.** Merge `devDependencies` from hugoplate into jorap.com. Keep JoRap-specific `name`, `description`, `version`, `author`, `engines`, and custom scripts (`build` with `cspHashes.mjs`, `watch`, etc.).

**Step 6 — Verify:**

```bash
pnpm install
pnpm build
```

If build fails, fix merge conflicts in theme templates or CSS before finishing.

### Hugo modules

After a theme sync, consider refreshing Hugo modules:

```bash
pnpm update-modules
```

---

## Impeccable sync

Impeccable installs into `.cursor/skills/impeccable/`. JoRap design context lives in `docs/PRODUCT.md` and `docs/DESIGN.md` — **never overwrite these** during a skill update.

### Recommended workflow

```
Task progress:
- [ ] Pull impeccable
- [ ] Build skill bundle
- [ ] Link or update into .cursor/skills/
- [ ] Preserve docs/PRODUCT.md, docs/DESIGN.md, .impeccable/
- [ ] Smoke-check skill loads
```

**Step 1 — Build the bundle** (requires Node ≥24 and bun in the impeccable repo):

```bash
cd ../impeccable
bun install
bun run build:skills
```

**Step 2 — Link into jorap.com** (from jorap.com root; preferred for local dev — symlinks track the checkout):

```bash
node ../impeccable/cli/bin/cli.js link \
  --source=../impeccable \
  --providers=cursor \
  --force -y
```

If the project uses a **copied** install (not symlinked), either:

- Re-run `link` with `--force` (replaces with symlinks), or
- Run `npx impeccable update --force -y` to pull the latest published bundle from impeccable.style

**Step 3 — Preserve project context.** Do not touch:

- `docs/PRODUCT.md`, `docs/DESIGN.md`, `docs/DESIGN.json`
- `.impeccable/` (live mode config, critique ignores, session state)
- Any user-created pins or local hook overrides

**Step 4 — Verify.** Confirm `.cursor/skills/impeccable/SKILL.md` exists and `node .cursor/skills/impeccable/scripts/load-context.mjs` resolves `docs/PRODUCT.md`.

---

## After any sync

1. Show `git diff --stat` and call out files that need manual review.
2. Summarize what changed (theme templates, CSS, scripts, skills).
3. Note anything skipped from [preserve-lists.md](preserve-lists.md).
4. Do **not** commit unless the user asks.

## Related skills

- **hugo-template-guidance** — after syncing `.agents/skills/` from Hugoplate, use for Hugo/Tailwind conventions.
- **impeccable** — for design work after refreshing the skill; reads `docs/PRODUCT.md` / `docs/DESIGN.md`.
