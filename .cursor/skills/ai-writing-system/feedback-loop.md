# Feedback Loop

Forte's self-improving system: **mistakes update the guide**, not just the draft. In Cursor, "copy to project" = commit a small patch to the right file.

## When to loop (not just fix the draft)

| Signal | Patch target |
|--------|--------------|
| Same AI tell appears in 2+ drafts | `jorap-voice` AI tells + `data/voice-words.yaml` |
| Invented personal detail | `author-context.md` gap table or interview question in implementation-guide |
| Wrong lane tone (blog voice in notes) | garden-voice **When to use which** |
| Structural slop recurs | `data/slop-rules.yaml` or `anti-slop.mdc` |
| New content type (newsletter, thread) | `implementation-guide.md` routing table |
| Sample post drifted from current voice | `writing-samples.md` — swap sample |

**One-off typo in one draft:** fix the draft only. Don't encode.

## Loop steps

1. **Name the failure** — one sentence ("opened with fake ECQ story", "used Furthermore three times")
2. **Classify** — vocabulary / structure / facts / process
3. **Patch the system** — smallest file that prevents recurrence
4. **Verify** — rerun the failing check (`pnpm slop:score`, `pnpm lint:voice`, or re-read sample)
5. **Optional:** add before/after to `jorap-voice/examples.md` if it's a new anti-pattern

## Patch destinations

| Failure type | Where to write the rule |
|--------------|-------------------------|
| Banned word or phrase | `data/voice-words.yaml` |
| Nominalization / passive / structure | `data/slop-rules.yaml` |
| Voice pass gap | `jorap-voice/SKILL.md` (one line under the relevant pass) |
| Garden field shape | `garden-voice/SKILL.md` |
| Interview didn't catch it | `implementation-guide.md` Phase 1 question |
| Priority conflict | `style-priorities.md` |
| Agent keeps skipping workflow | `ai-writing-system/SKILL.md` checklist |

## Session debrief prompt

After a publish or heavy edit, user can run:

```
Debrief this writing session for the feedback loop.
What failed twice? What file should we patch?
```

Agent outputs: failure name, patch file, exact one-line addition (or says "draft-only fix").

## Monthly hygiene

- `pnpm garden:health` — garden voice drift
- `pnpm voice:scan` — site-wide banned words
- Review `writing-samples.md` — still best in class?

## Encode rule (repo convention)

Per `self-improvement.mdc`: encode only when the same correction happened **twice in one session** or user asks to remember. Otherwise patch the draft and move on.
