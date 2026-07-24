---
note_kind: "meta"
title: "OKF Export"
meta_title: "OKF Export - Agent-Readable Notes Bundle"
description: "Same garden flattened for agents - markdown paths, required type, no Hugo build."
key_concept: |
  - Authoring stays in Hugo; OKF is the agent-readable pass-off copy outside the site.
  - Level 1: You write notes in Hugo on the site - OKF is a flat copy outside the site that other tools can read, like photocopying your notebook for a friend who uses a different app.
  - Level 2: OKF export is the agent-readable pass-off - authoring stays in Hugo, flat copy lives outside for other tools.
  - Level 3: Authoring stays in Hugo; OKF is the structured export agents and scripts can ingest without parsing the site.
  - Level 4: Keep Hugo as source of truth - regenerate OKF when the garden changes so external tools read current text.
  - Level 5: [[Building a Personal API]] and automation assume a stable export format - OKF is the handoff layer, not a second place to edit.
  - Same garden, flattened - markdown paths, required type field, no Hugo build step.
  - Regenerated on production build and via npm run export:okf.
shareable_thought:
  - "Same garden flattened for agents."
  - "Markdown paths, required type, no Hugo build."
  - "Authoring stays in Hugo; OKF is the agent-readable pass-off copy outside the site."
  - "Same garden, flattened - markdown paths, required type field, no Hugo build step."
slug: "okf-export"
date: "2026-06-27 08:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["Notes", "Meta", "PKM", "OKF"]
aliases: ["OKF", "OKF Export"]
featured: false
draft: false
---

[Open Knowledge Format (OKF) graph](/exports/okf/viz.html) — visual network of the exported bundle.

## ChatGPT workflow

Three lanes - all copy-paste friendly:

| Goal | Where | What to paste |
|------|-------|---------------|
| **Create** a new atomic note | [Create Note](/notes/create/) | Copy prompt → ChatGPT → paste the markdown file back into `content/english/notes/` |
| **Find connections** between notes | Any note page (Random Note section) or [Random Duo](/notes/random-duo/) | Copy prompt - includes both note bodies + shortest wikilink path when one exists |
| **Give context** on existing notes | **Copy MD** or **Agent copy** on any note (upper right) | Paste into ChatGPT as background before asking questions |

**Copy MD** copies the full Hugo file (frontmatter + `[[wikilinks]]`) - ready to save or edit. **Agent copy** copies the Open Knowledge Format (OKF) version with resolved markdown links, better when the model doesn't know your wikilink titles.

For the whole garden at once: **Copy catalog** on this page, or open [Bundle index](/exports/okf/index.md).

## Workflow combos

Each row maps to a site button plus a ChatGPT ask.

| Combo | Copy from site | Ask ChatGPT |
|-------|----------------|-------------|
| **Expand a hub (Maps of Content, MOC)** | **Copy hub cluster** on a hub page (e.g. [Maps of Content](/notes/maps-of-content/), [Eternal Principles](/notes/eternal-principles/)) + **Copy catalog** here | *What atomic notes are missing from this cluster? Output Hugo markdown files.* |
| **Garden maintenance** | **Copy issues** on [Issues](/notes/issues/) + **Copy MD** on 3-5 affected notes | *Fix broken links, add extends/contradicts rows, keep voice plain.* |
| **Flashcard pass** | **Copy MD** on a `review: true` spine note + **Copy MD** on [Flashcards](/notes/flashcards/) for format rules | *Write six new scenario cards - cue on front, one-breath action on back.* |
| **Blog from note** | **Copy MD** on the source note | *Distill this into an 800-word blog post. Keep JoRap voice. No extra ## sections.* |
| **Post-Create siblings** | [Create Note](/notes/create/) prompt output (lists siblings automatically) | Run each sibling title as a new Create Note session |
| **Orphan hunt** | Filter [Graph](/notes/graph/) for orphans → **Copy MD** on 2-3 orphans + **Copy catalog** | *What wikilinks and relationship rows would connect these to the rest of the garden?* |

**Standing context:** paste **Copy catalog** once into a ChatGPT project. Add **Copy MD** or **Copy hub cluster** per session.

## Browse the bundle

- [Open Knowledge Format (OKF) graph](/exports/okf/viz.html) - Cytoscape force layout, search, backlinks
- [Bundle index](/exports/okf/index.md) - all concepts and hubs (`okf_version: "0.1"`)
- [Update log](/exports/okf/log.md) - recent garden changes from git
- [Example concept: Personal Knowledge Management (PKM)](/exports/okf/concepts/pkm.md)
- [Example hub: Maps of Content](/exports/okf/hubs/maps-of-content/index.md)

## What changes in export

| Live garden | Open Knowledge Format (OKF) bundle |
|-------------|------------|
| `[[wikilinks]]` | `[Title](/concepts/slug.md)` |
| Hub/Maps of Content (MOC) pages | `hubs/{slug}/index.md` (no frontmatter) |
| Graph, Review, Flashcards | Omitted |
| Draft notes | Omitted |
| Canonical URL | `resource:` on each concept |

Regenerate bundle + graph: `npm run export:okf` (runs automatically on `pnpm build`).

Spec: [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Graph viewer adapted from [Google's OKF reference visualizer](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf#visualize). Pairs with [[Create Note]], [[Random Duo]], and [[Getting Started]].
