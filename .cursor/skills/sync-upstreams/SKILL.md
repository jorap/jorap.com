---
name: sync-upstreams
description: Sync JoRap.com with local upstream checkouts of Hugoplate (Hugo theme) and Impeccable (design skills). Use when the user asks to update the theme, pull upstream changes, sync hugoplate/impeccable, refresh agent skills, or merge upstream into jorap.com.
---

# Sync Upstreams

JoRap.com is a **project-setup** Hugo site (`theme = "jorap"` in `hugo.toml`) forked from [Hugoplate](https://github.com/zeon-studio/hugoplate). Design work uses the [Impeccable](https://github.com/pbakaus/impeccable) skill in `.cursor/skills/impeccable/`.

Unless noted otherwise, paths below are **relative to the jorap.com repo root**. Upstream checkouts live as sibling folders one level up (`../hugoplate`, `../impeccable`).

| Upstream | Path (from jorap.com root) |
| --- | --- |
| Hugoplate | `../hugoplate` |
| Impeccable | `../impeccable` |

**Never blind-copy or bulk-rsync the theme.** JoRap forked Hugoplate’s CSS token system, fonts, homepage, blog layout, and many partials. Sync = **triage diffs → apply only safe changes → build → summarize**.

## Quick routing

| User wants | Follow |
| --- | --- |
| Update Hugo theme / Hugoplate | [Hugoplate sync](#hugoplate-sync) |
| Update Impeccable skill / design commands | [Impeccable sync](#impeccable-sync) |
| Update both | Hugoplate first, then Impeccable, then verify build |
| What not to overwrite | [preserve-lists.md](preserve-lists.md) |

---

## Pre-flight (both upstreams)

1. Pull upstream checkouts:

```bash
cd ../hugoplate && git pull
cd ../impeccable && git pull
```

2. Confirm clean working tree in jorap.com (or stash first):

```bash
git status
```

3. Package manager: **pnpm** (`pnpm-lock.yaml`).

---

## Hugoplate sync

Hugoplate’s theme lives at repo root (`layouts/`, `assets/`). JoRap vendors it as **`themes/jorap/`**.

### Path mapping

| Hugoplate source | JoRap.com target |
| --- | --- |
| `layouts/` | `themes/jorap/layouts/` |
| `assets/` | `themes/jorap/assets/` |
| `scripts/` | `scripts/` (selective) |
| `.agents/skills/` (upstream) | `.cursor/skills/` |
| `AGENTS.md` | Review; merge relevant sections only |

Do **not** copy `exampleSite/`, `theme.toml`, or hugoplate’s `package.json` wholesale.

### Workflow — triage before apply

```
Task progress:
- [ ] Pull hugoplate
- [ ] Run triage report (classify every diff)
- [ ] Read diff for each CANDIDATE / ADD-ONLY file
- [ ] Copy or cherry-pick ONLY approved files — one at a time
- [ ] Diff root scripts; update only Tier-3 matches
- [ ] Sync Hugoplate agent skills into `.cursor/skills/`; restore JoRap local notes
- [ ] pnpm build
- [ ] Summarize: applied / skipped / needs manual review
```

**Do not** run bulk `rsync` on `layouts/` or `assets/` as the default step. The exclude list ([hugoplate-rsync-excludes.txt](hugoplate-rsync-excludes.txt)) blocks known JoRap paths but is not sufficient on its own — upstream “shared” files still break JoRap when they revert the semantic token system.

### Step 1 — Triage report

Run the classifier (read-only):

```bash
bash .cursor/skills/sync-upstreams/triage-hugoplate.sh
```

Output columns: `STATUS`, `path`, `reason`

| Status | Action |
| --- | --- |
| **BLOCKED** | Never copy — on preserve/exclude list ([preserve-lists.md](preserve-lists.md) Tier 1) |
| **SKIP** | Would regress JoRap (CDN fonts, old tokens, `hugoplate` theme name) |
| **MANUAL** | JoRap customization detected — skip unless user wants a hand merge |
| **CANDIDATE** | May be safe — **must read full diff** before copying |
| **ADD-ONLY** | New upstream file JoRap lacks — add if not JoRap-specific |

Also list structural diffs:

```bash
HUGO=../hugoplate
diff -rq "$HUGO/layouts" themes/jorap/layouts
diff -rq "$HUGO/assets" themes/jorap/assets
diff -rq ../hugoplate/scripts scripts
```

### Step 2 — Decide per file (agent judgment)

For each **CANDIDATE** or **ADD-ONLY** row:

1. Read the full diff: `diff -u themes/jorap/path ../hugoplate/path`
2. Apply [preserve-lists.md](preserve-lists.md) Tier 2 red flags — if any match, **skip**
3. If the change is a small, isolated bugfix with no token/markup regression, copy **that file only**:

```bash
cp ../hugoplate/layouts/_partials/widgets/widget-wrapper.html themes/jorap/layouts/_partials/widgets/widget-wrapper.html
```

4. If only part of a file is useful, cherry-pick hunks manually — do not overwrite the whole file

**Safe apply examples** (when diff confirms no JoRap regression):

- New file under `assets/plugins/` JoRap doesn’t override
- Typo fix in a widget partial JoRap still uses verbatim
- Root script matches upstream and JoRap has no local edits (`diff -q` clean on JoRap side)

**Never auto-apply** (even if triage says CANDIDATE — re-classify as SKIP/MANUAL):

- Any file under `assets/css/` or `assets/js/main.js`
- `home.html`, `baseof.html`, `blog/single.html`, essentials partials
- Files whose diff swaps semantic tokens (`text-ink`, `bg-surface`) for Hugoplate tokens (`text-text`, `bg-body`, `dark:*`)

### Step 3 — Root scripts

```bash
diff -rq ../hugoplate/scripts scripts
```

| File | Rule |
| --- | --- |
| `themeGenerator.js`, `clearModules.js` | Copy only if `diff -q` shows JoRap differs **and** diff has no JoRap-specific logic |
| `projectSetup.js`, `themeSetup.js`, `removeDarkmode.js`, `removeMultilang.js` | Removed from JoRap (one-time Hugoplate migrations already applied); do not restore |
| `cspHashes.mjs`, `lint-*.py`, `noteFileDates.js`, `wire-notes-obsidian.py`, etc. | Never touch |
| `scripts/archive/*.py` | One-off migrations (already applied); do not restore to `scripts/` |

### Step 4 — Agent skills

```bash
HUGO=../hugoplate
rsync -av "$HUGO/.agents/skills/" .cursor/skills/
```

Then restore JoRap-only lines upstream removed, e.g. the `__` draft-post note in `.cursor/skills/hugo-template-guidance/references/content-management.md`.

### Step 5 — package.json

Merge **new** `devDependencies` from Hugoplate. Keep JoRap `name`, `description`, `version`, `author`, `engines`, and all custom scripts (`build` with `cspHashes`, `watch`, etc.).

### Step 6 — Verify

```bash
pnpm install   # only if devDependencies changed
pnpm build
```

If build fails, revert the last copied file and mark it MANUAL.

### Emergency bulk rsync (user explicitly requests only)

Only when the user asks to “rsync everything” **and** triage report shows zero MANUAL/SKIP rows for the target tree. Still use excludes:

```bash
HUGO=../hugoplate
rsync -av --exclude-from=.cursor/skills/sync-upstreams/hugoplate-rsync-excludes.txt \
  "$HUGO/layouts/" themes/jorap/layouts/
```

Never use `--delete` unless the user explicitly wants orphan files removed.

### Hugo modules

After applying theme changes:

```bash
pnpm update-modules
```

---

## Impeccable sync

Installs into `.cursor/skills/impeccable/`. Never overwrite `docs/PRODUCT.md`, `docs/DESIGN.md`, `.impeccable/`.

### Workflow

```
Task progress:
- [ ] Pull impeccable
- [ ] Build skill bundle
- [ ] Link into .cursor/skills/
- [ ] Verify context script
```

**Step 1 — Build** (prefer bun; fallback to npm + node):

```bash
cd ../impeccable
# bun install && bun run build:skills   # if bun available
npm install && node scripts/build.js --skip-root-sync
```

**Step 2 — Link** (from jorap.com root):

```bash
node ../impeccable/cli/bin/cli.js link \
  --source=../impeccable \
  --providers=cursor \
  --force -y
```

**Step 3 — Verify:**

```bash
node .cursor/skills/impeccable/scripts/context.mjs
```

Must resolve `docs/PRODUCT.md`.

---

## After any sync

1. Show `git diff --stat` — only files you intentionally changed
2. Report three lists:
   - **Applied** — what was copied/cherry-picked and why
   - **Skipped** — BLOCKED / SKIP / MANUAL with one-line reason each
   - **Review** — anything the user should eyeball in the browser
3. Do **not** commit unless the user asks

If **zero** files pass triage, say so — “already in sync” or “no safe upstream changes” is a valid outcome.

## Related skills

- **hugo-template-guidance** — Hugo/Tailwind conventions after agent skill sync
- **impeccable** — design work; reads `docs/PRODUCT.md` / `docs/DESIGN.md`
