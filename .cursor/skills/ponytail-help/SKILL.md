---
name: ponytail-help
description: >
  Quick-reference card for all ponytail modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /ponytail-help,
  "ponytail help", "what ponytail commands", "how do I use ponytail".
---

# Ponytail Help

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/ponytail lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/ponytail` | The ladder enforced: YAGNI → stdlib → native → one line → minimum. Default. |
| **Ultra** | `/ponytail ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ponytail** | `/ponytail` | Lazy mode itself. Simplest solution that works. |
| **ponytail-review** | `/ponytail-review` | Diff review for over-engineering: `L42: yagni: factory, one product. Inline.` |
| **ponytail-audit** | `/ponytail-audit` | Whole-repo audit: ranked `delete:` / `shrink:` list, biggest cut first. |
| **ponytail-debt** | `/ponytail-debt` | Ledger of `ponytail:` comment shortcuts (ceiling + upgrade path). |
| **ponytail-gain** | `/ponytail-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **ponytail-help** | `/ponytail-help` | This card. |

In Cursor, attach skills by name or ask in chat (e.g. `ponytail audit this repo`).

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `/ponytail`.
`/ponytail off` also works.

## JoRap defaults

- Always-on rule: `.cursor/rules/ponytail.mdc`
- All project skills live in `.cursor/skills/` (ponytail, Hugo, JoRap voice, etc.)
- **Exclude from audits** unless you say otherwise: `pixi.js`, `assets/js/notes-graph.js` (Obsidian graph parity)

## More

Full docs + examples: https://github.com/DietrichGebert/ponytail
