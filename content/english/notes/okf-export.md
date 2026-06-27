---
title: "OKF Export"
meta_title: "OKF Export - Agent-Readable Notes Bundle"
description: "Open Knowledge Format v0.1 export of the notes garden — plain markdown for agents and tools outside Hugo."
slug: "okf-export"
note_kind: "meta"
date: 2026-06-27T08:00:00Z
image: "/images/note.jpg"
categories: ["Productivity", "Ideas", "Tips"]
author: "JoRap"
tags: ["Notes", "Meta", "PKM", "OKF"]
featured: false
draft: false
aliases: ["OKF", "OKF Export"]
---

**OKF export** = the same garden, flattened for agents — markdown paths, required `type`, no Hugo build.

The live site stays the authoring surface (`[[wikilinks]]`, graph, flashcards). This bundle is the handoff copy: OKF v0.1, regenerated on production build and via `npm run export:okf`.

## Browse the bundle

- **[OKF graph](/exports/okf/viz.html)** — Google's reference OKF visualizer (Cytoscape.js force layout, search, backlinks)
- [Bundle index](/exports/okf/index.md) — all concepts and hubs (`okf_version: "0.1"`)
- [Update log](/exports/okf/log.md) — recent garden changes from git
- [Example concept: PKM](/exports/okf/concepts/pkm.md)
- [Example hub: Maps of Content](/exports/okf/hubs/maps-of-content/index.md)

Raw `.md` links show plain markdown in the browser — fine for agents. Use **OKF graph** for the visual network.

## What changes in export

| Live garden | OKF bundle |
|-------------|------------|
| `[[wikilinks]]` | `[Title](/concepts/slug.md)` |
| Hub/MOC pages | `hubs/{slug}/index.md` (no frontmatter) |
| Graph, Review, Flashcards | Omitted |
| Draft notes | Omitted |
| Canonical URL | `resource:` on each concept |

Regenerate bundle + graph: `npm run export:okf` (runs automatically on `pnpm build`).

Spec: [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Graph viewer adapted from [Google's OKF reference visualizer](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf#visualize).
