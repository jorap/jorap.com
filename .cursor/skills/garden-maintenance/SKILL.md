---
name: garden-maintenance
description: >
  Weekly garden hygiene loop: measure link/lint health, fix top issues, encode
  lessons into skills/rules. Use for "garden maintenance", "weekly garden",
  "maintenance window", or after `pnpm garden:health` reports failures.
---

# Garden maintenance (weekly loop)

Measure → fix → encode → verify. Hugo stays source of truth; OKF is the agent handoff.

## 1. Measure

```bash
pnpm garden:health
```

Exit codes: `0` clean, `1` lint or build failed, `2` link issues remain (lint passed).

Plain-text issues also ship at `/notes/issues/index.txt` after build (same as **Copy issues** on [/notes/issues/](/notes/issues/)).

## 2. Fix (priority order)

1. **Broken wikilinks** and **broken relationship targets** — wrong title or missing note
2. **Utility wikilinks** — swap `[[Graph]]` for `/notes/graph/` paths
3. **Unlinked mentions** — only when the link adds navigation (skip false positives)
4. **Structure** — missing extends/contradicts rows
5. **Lint failures** — `pnpm lint:garden` output (voice, slop, cards, frontmatter)

Cap at **15 issues** per pass unless the user asks for a full sweep. Use garden-voice skill on note edits.

## 3. Encode

After the pass, if the same correction happened twice in one session, patch the relevant skill or `.cursor/rules/` file (see `self-improvement.mdc`). Log intentional deferrals with `ponytail:` comments.

## 4. Verify

```bash
pnpm garden:health
```

If `content/english/notes/` changed: `pnpm export:okf` (or full `pnpm build` before deploy).

## Session close

End with the session-close block from `session-close.mdc`.

## Cursor Automation (optional)

Schedule weekly (e.g. Sunday maintenance window):

- **Trigger:** cron `0 9 * * 0` or manual
- **Tools:** Shell
- **Prompt:** Run `pnpm garden:health` in the repo. If exit code ≠ 0, fix up to 15 highest-priority issues from the report (broken links first). Re-run health. Encode repeat mistakes per self-improvement.mdc. End with session-close block. Do not commit unless asked.

## Boundaries

- Do not edit OKF bundle files under `static/exports/okf/` by hand — regenerate.
- Orphans and dead ends are informational unless the user targets graph shape.
