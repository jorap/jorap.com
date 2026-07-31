# Agent instructions (JoRap.com)

Portable baseline for AI coding agents. **Do not duplicate** rule or skill bodies here — they live in one canonical tree shared by Cursor and Kilo Code.

## Canonical locations

| Kind | Path | Tools |
|------|------|--------|
| Rules | `.cursor/rules/*.mdc` | Cursor (native), Kilo (`instructions` in `kilo.jsonc`) |
| Skills | `.cursor/skills/*/SKILL.md` | Cursor (native), Kilo (`skills.paths` in `kilo.jsonc`) |

Kilo Code loads this file plus the paths above via root [`kilo.jsonc`](kilo.jsonc). There is no `.kilo/skills` or `.kilo/rules` copy in this repo.

## When you add or change rules or skills

1. Edit only under `.cursor/rules/` or `.cursor/skills/`.
2. Run `pnpm lint:agent-config` — must pass before commit.
3. Do not create parallel copies under `.kilo/`, `.kilocode/`, or `.agents/`.

Skill folders must include `SKILL.md` with `name` matching the directory name and a `description` field (Agent Skills spec).

## Repo-specific reminders

- **Deploy discipline:** see `.cursor/rules/deploy-commits.mdc` — batch site publishes; `[skip ci]` for tooling-only commits.
- **Filenames:** cross-platform safe paths — `pnpm lint:filenames`.
- **Git:** do not commit unless the user asks — `.cursor/rules/git-commits.mdc`.
- **Voice:** blog → `jorap-voice` skill; notes garden → `garden-voice` skill.
