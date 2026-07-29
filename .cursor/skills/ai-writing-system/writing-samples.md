# Writing Samples

Forte Step 1: samples teach the model what "on voice" means. These are **calibration anchors** — read 1–2 in the same lane before drafting.

## Selection criteria (when adding a sample)

Pick pieces that:

1. **Sound like you on a good day** — not your most popular post if it's old voice
2. **Match the lane** you're drafting (gear ≠ faith ≠ PKM)
3. **Have specifics** — names, failures, durations, places
4. **Span lengths** — one short tip, one medium post, one long piece
5. **Avoid** outline-only wiki exports, tracker tables, duplicate angles

Verify paths: `node scripts/ai-writing-samples-check.mjs`

## Blog — gear and reviews

| File | Why it's here |
|------|---------------|
| `content/english/blog/what-i-look-for-in-wireless-earphones.md` | Gold standard opener, opinionated checklist, drawer graveyard |
| `content/english/blog/extension-cord.md` | Practical pick, honest mistake, Philippines-adjacent grounding |

## Blog — tech and how-to

| File | Why it's here |
|------|---------------|
| `content/english/blog/how-i-built-jorap-notes.md` | Build story, Hugo deploy specifics, understated humor |
| `content/english/blog/mouse-wheel-click.md` | Short tip shape, one problem one fix |

## Blog — opinion and culture

| File | Why it's here |
|------|---------------|
| `content/english/blog/why-i-stopped-playing-marvel-snap.md` | Clear take, visible thinking, no fake balance |
| `content/english/blog/why-i-focused-on-open-source.md` | Values essay without lecture tone |

## Blog — family and faith

| File | Why it's here |
|------|---------------|
| `content/english/blog/miracle-isaiah-david.md` | Personal narrative, faith without genericize |

## Blog — food (recipe variant)

| File | Why it's here |
|------|---------------|
| `content/english/blog/instant-pot-arroz-caldo.md` | Human section intros + scannable steps |

## Notes — PKM

| File | Why it's here |
|------|---------------|
| `content/english/notes/capture.md` | Tight `description`, arguable `key_concept` |
| `content/english/notes/rollback-principle.md` | Claim-first, two-scene `examples` |

## Notes — faith

| File | Why it's here |
|------|---------------|
| `content/english/notes/abide-in-me.md` | Scripture + first-person gloss without sermon tone |

## Do not use as voice samples

| File | Why |
|------|-----|
| `content/english/blog/alex-eala-pro-career-tracker.md` | Data tracker — headings are machine-matched |
| `content/english/blog/__interesting-facts-about-jorap.md` | Facts ledger, not prose voice |
| Any `__` draft with wiki footer | Outline until rewritten |
| Posts with heavy tables/stats only | Structure ≠ voice |

## Lane → read before drafting

| Drafting… | Read these two |
|-----------|----------------|
| Gear / buying guide | wireless earphones + extension cord |
| Hugo / dev / workflow | how-i-built-jorap-notes + mouse-wheel-click |
| Opinion / games / culture | marvel snap + open source |
| Family / faith blog | miracle-isaiah-david + (gear sample for pacing) |
| Recipe | instant-pot-arroz-caldo + mouse-wheel-click (brevity) |
| PKM note | capture + rollback-principle |
| Faith note | abide-in-me + capture (density) |
