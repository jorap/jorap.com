---
name: changelog-update
description: >
  Update CHANGELOG.md with human-readable site functionality bullets from git
  diffs and SpecStory session history. Use when the user asks to update the
  changelog, refresh CHANGELOG.md, or document shipped changes before deploy.
  One-shot edit to CHANGELOG.md only.
---

Site **functionality** shipped to [jorap.com](https://jorap.com). Deploys run on
**Cloudflare Pages** via `pnpm run deploy`.

## Scope

Log **user-facing functionality** only — not content edits, agent paths, or
raw file lists.

**Include:** `layouts/`, `assets/js`, `assets/css`, `themes/`, `scripts/`,
`config/`, `functions/`, `data/theme.json`, deploy config (`wrangler.toml`,
etc.), `package.json` / lockfile when tooling changes, `static/_headers` /
`static/_redirects`.

**Skip:** `content/`, `.specstory/`, `.cursor/`, `.agents/`, `docs/`, most
`static/`, `data/noteFileDates.json`, markdown except `CHANGELOG.md`.

## Workflow

1. Read `CHANGELOG.md` — match tone and structure of recent date sections.
2. Gather changes:
   - `git log --oneline` and `git diff` (staged, unstaged, or since last
     dated section — pick the scope the user implies).
   - **SpecStory:** scan `.specstory/history/` for sessions on the target
     date (or matching the feature). User messages and agent summaries often
     name the *why* behind diffs that commit messages hide (`Updates`, `Fixes`).
3. Group bullets under **Added**, **Changed**, or **Fixed**:
   - `fix:` / `Fixes` → **Fixed**
   - `feat:` / `add:` → **Added**
   - otherwise → **Changed**
4. Upsert under `## YYYY-MM-DD` (today unless the user names a date):
   - Merge into existing categories; do not duplicate bullets.
   - Replace any prior raw `` `path/to/file` `` bullets with readable lines.
5. Write concise bullets — what shipped and why it matters, not which files
   moved. Follow prior sections (see 2026-06-21, 2026-06-22).

## Bullet style

**Good:**

- Random note/duo shuffle buttons moved beside each dropdown
- Notes graph lazy init (IntersectionObserver) with 240-node cap on global view

**Bad:**

- `assets/js/notes-random-duo.js`
- Updated several files

## Header

Keep the intro blurb accurate. Do **not** claim auto-updates on commit — this
skill is the updater.

## Boundaries

- Edit `CHANGELOG.md` only unless the user asks otherwise.
- Do not commit unless explicitly requested.
