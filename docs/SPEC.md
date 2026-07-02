# JoRap Notes — Platform Specification

**Version:** 1.0.0  
**Status:** Active  
**Last updated:** 2026-07-03  
**Canonical URL:** [https://www.jorap.com](https://www.jorap.com)

This document is the **complete product and platform specification** for JoRap Notes. It defines what the system is, who it serves, what it must do, and how success is measured. Companion docs carry detail this file references rather than duplicates:

| Document | Scope |
| --- | --- |
| [`PRODUCT.md`](./PRODUCT.md) | Audience, voice, anti-references, design principles |
| [`DESIGN.md`](./DESIGN.md) | Visual system, tokens, components |
| [`.specify/memory/constitution.md`](../.specify/memory/constitution.md) | Architectural principles and governance |
| [`CMS_SETUP.md`](./CMS_SETUP.md) | Static Site CMS (`/admin`) setup |
| [`CLIENT_STATIC_SITE.md`](./CLIENT_STATIC_SITE.md) | Client-site deploy checklist |
| [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) | Build, deploy, and CMS gotchas |
| [`TODO.md`](./TODO.md) | Working backlog |
| [`../specs/`](../specs/) | Feature-specific speckit specs (user stories, FRs, checklists) |

---

## 1. Purpose

JoRap Notes is a **personal brand surface**: a static site that showcases how the author thinks, what they stand for, and the quality of their work so the right clients recognize fit and reach out with confidence.

The platform combines:

- **Blog** — long-form credibility and SEO
- **Notes garden** — atomic linked notes, graph, flashcards, and agent handoff
- **Static pages** — about, contact, portfolio framing
- **CMS** — optional git-backed authoring for non-developers

Success means visitors leave with **professional credibility**, a **distinct point of view**, and **trust** that engaging the author is a serious business choice—not a casual follow of a hobby blog.

---

## 2. Users & Scenarios

### 2.1 Primary users

| User | Goal | Typical entry |
| --- | --- | --- |
| **Prospective client / decision-maker** | Assess credibility, clarity, and fit before outreach | Search, referral, LinkedIn |
| **Reader** | Learn from essays and connected ideas | Blog post, notes graph |
| **Author (JoRap)** | Publish, maintain garden, export to agents | Git, Hugo, `/admin` |
| **Agent / LLM** | Ingest structured knowledge for drafting or maintenance | OKF bundle, Copy MD, Agent copy |

### 2.2 User scenarios (prioritized)

#### P1 — Client credibility skim

A decision-maker lands on the homepage or a blog post between meetings. They scan navigation, read one essay, and decide whether the author thinks in outcomes.

**Acceptance:** Homepage and blog feel calm, legible, and professional on laptop and mobile. Copy speaks to intelligent non-specialists. No performative dev-bro or generic SaaS landing patterns.

#### P2 — Deep read with discovery

A reader finishes a blog post and follows related notes or posts without getting lost.

**Acceptance:** Related posts appear on blog singles. Blog posts may declare `related_notes`. Breadcrumbs and back-to-top work on long reads. Search returns relevant results.

#### P3 — Notes garden exploration

A reader browses atomic notes via list, graph, backlinks, or random resurfacing.

**Acceptance:** Wikilinks resolve. Backlinks show context snippets. Graph filters (high/low/no body links, orphans) work on desktop and touch devices. Broken links surface on Issues and per-note warnings.

#### P4 — Spaced-repetition review

The author drills habit-spine flashcards in `/notes/review/`.

**Acceptance:** Cards flip with reduced-motion fallback. Progress persists in `localStorage`. Only `review: true` notes with valid `cards:` frontmatter appear in review queues.

#### P5 — Author publish workflow

The author writes Markdown, runs lint, pushes to Git; the site rebuilds and deploys.

**Acceptance:** `pnpm dev` for local preview. `pnpm run deploy` produces `public/`. Cloudflare Pages rebuilds on push. Non-deploy commits can use `[skip ci]`.

#### P6 — Agent handoff

The author copies garden context into ChatGPT or another agent for drafting, connection-finding, or maintenance.

**Acceptance:** Copy MD, Agent copy, Copy catalog, Copy hub cluster, and OKF export produce paste-ready artifacts. OKF bundle regenerates on production build.

---

## 3. System overview

### 3.1 Architecture

Static-first. No server-side rendering, database, or user accounts on the public site.

```
Markdown + assets (Git)
        │
        ▼
  Hugo build + Node tooling
  (theme, dates, OKF export, CSP hashes)
        │
        ▼
  public/  ──►  Cloudflare Pages
```

**Stack (pinned in `scripts/deploy-versions.json`):**

| Layer | Technology |
| --- | --- |
| Generator | Hugo Extended 0.163.3 |
| Theme | `themes/jorap` (forked from Hugoplate) |
| CSS | Tailwind CSS v4, semantic tokens from `data/theme.json` |
| Client JS | Vanilla modules (`assets/js/`) — search, graph (PixiJS), flashcards |
| Build | Node 22+, pnpm 11.7, Go 1.24+ |
| Hosting | Cloudflare Pages (primary) |
| CMS | Static Site CMS at `/admin` (optional) |

### 3.2 Repository layout

| Path | Role |
| --- | --- |
| `content/english/blog/` | Blog posts |
| `content/english/notes/` | Notes garden |
| `content/english/` pages | Static marketing pages |
| `layouts/` | Site-specific Hugo templates (notes tools) |
| `themes/jorap/` | Active theme |
| `assets/js/`, `assets/css/` | Site overrides |
| `static/` | `_headers`, `_redirects` (security, apex → www) |
| `scripts/` | Build, lint, export, deploy |
| `data/` | Theme tokens, note file dates |

### 3.3 Environments

| Environment | Base URL | Build |
| --- | --- | --- |
| Production | `https://www.jorap.com/` | Cloudflare Pages on git push |
| Local dev | `http://localhost:1313/` | `pnpm dev` |
| Local prod preview | `http://localhost:1313/` (production flags) | `pnpm preview` |

Apex `jorap.com` redirects to `www.jorap.com` via `static/_redirects`.

---

## 4. Content surfaces

### 4.1 Blog

**Path:** `/blog/`  
**Permalink:** `/blog/:slug/`  
**Format:** Standard Hugo frontmatter + Markdown body.

| Field | Required | Notes |
| --- | --- | --- |
| `title`, `description`, `slug`, `date` | Yes | SEO and listing |
| `categories`, `tags` | Recommended | Taxonomy and related scoring |
| `related_notes` | Optional | Slugs of garden notes to surface |
| `draft` | Yes | `false` to publish |

**Features:** RSS, related posts, Disqus comments (configured), TOC on long posts, breadcrumbs, share controls, image lightbox, structured data (Article).

### 4.2 Static pages

**Path:** `/:slug/` (e.g. `/about/`)  
**Format:** Markdown under `content/english/` with appropriate layout.

Used for about, contact, and marketing shells. Same visual system as blog.

### 4.3 Notes garden

**Path:** `/notes/`  
**Permalink:** `/notes/:slug/`

The notes garden is a **second product surface** on the same design system. It implements a personal knowledge graph with atomic notes, typed relationships, tooling pages, and agent export.

See **Section 5** for the full notes specification.

### 4.4 CMS

**Path:** `/admin/`  
**Role:** Git-backed editing for non-git authors.

Configuration and setup: [`CMS_SETUP.md`](./CMS_SETUP.md). CMS edits the same Markdown files the build consumes; there is no separate content database.

---

## 5. Notes garden specification

### 5.1 Design intent

- **One note = one claim** quotable in conversation
- **Links are first-class** — wikilinks in prose; typed relationships in frontmatter
- **Tools are meta pages** — graph, issues, review, etc. are not garden ideas
- **Agents are consumers** — OKF export and copy buttons hand off structured context

### 5.2 Page kinds (`note_kind`)

| Kind | Default | Purpose | Body prose | Relationships |
| --- | --- | --- | --- | --- |
| `note` | Yes | Atomic garden claim | Empty (frontmatter only) | Required: `extends` + `contradicts` minimum |
| `index` | No | Hub / MOC | Allowed (onboarding, lists) | Optional |
| `meta` | No | Tool surface | Allowed (tool docs) | Skip |

Utility surfaces (`note_kind: meta` or dedicated layouts) must **not** be wikilinked from content notes. `npm run lint:utility-links` enforces this.

### 5.3 Atomic note frontmatter

**Shared blog fields:** `title`, `meta_title`, `description`, `slug`, `date`, `image`, `categories`, `author`, `tags`, `featured`, `draft`

**Garden-specific fields:**

| Field | Required | Rules |
| --- | --- | --- |
| `description` | Yes (atomic) | One breath, ≤20 words, no wikilinks |
| `key_concept` | Yes (atomic) | Angle + stakes; wikilinks allowed |
| `examples` | Recommended | Exactly two plain bullets; mid-action scenes |
| `relationships` | Yes (atomic) | Typed rows; each target once; sorted a-z |
| `aliases` | Optional | Alternate wikilink targets |
| `note_kind` | Optional | `note` (default), `index`, `meta` |
| `review` | Optional | `true` for flashcard spine notes |
| `cards` | When `review: true` | Six scenario cards (front/back) |
| `card_sets` | When `review: true` | Grouping for Review UI |

**Timestamps:** Created/updated display uses filesystem mtime via `scripts/noteFileDates.js` → `data/noteFileDates.json`. No manual `lastmod` maintenance.

**Lint:** `npm run lint:garden` runs frontmatter, format, flashcard, utility-link, and voice checks.

### 5.4 Relationship types

| Type | Meaning |
| --- | --- |
| `extends` | Builds on or applies the target |
| `contradicts` | Tension, exception, or corrective |
| `implements` | Operationalizes the target |
| `alternative` | Different path to a similar goal |

Each relationship row:

```yaml
- type: extends
  wikilink: "[[Target Note]]"
  reason: "Plain one-line why"
```

### 5.5 Linking

| Mechanism | Syntax | Behavior |
| --- | --- | --- |
| Wikilink | `[[Note Title]]` | Resolves by title or `aliases` |
| Permalink | `/notes/slug/` | Canonical URL |
| Blog bridge | `related_notes` on blog posts | Surfaces garden from essays |

**Build-time checks:**

- Broken wikilinks → Hugo warning + Issues page
- Unlinked mentions → warning when note title appears without `[[wikilink]]`
- Pipe wikilinks (`[[x\|y]]`) → flagged (not supported)

### 5.6 Tool surfaces

| Tool | URL | Function |
| --- | --- | --- |
| List | `/notes/` | Filterable index, featured random note |
| Graph | `/notes/graph/` | PixiJS network; filter by link density and orphans |
| Issues | `/notes/issues/` | Broken links, pipe wikilinks, unlinked mentions |
| Backlinks | `/notes/backlinks/` | Garden-wide backlink index |
| Flashcards | `/notes/flashcards/` | Card browser by set |
| Review | `/notes/review/` | Spaced-repetition quiz flow |
| Random Duo | `/notes/random-duo/` | Two random notes + connection prompt |
| Create Note | `/notes/create/` | Topic → AI prompt for one atomic note |
| OKF Export | `/notes/okf-export/` | Bundle index and agent workflow docs |

**Per-note affordances:** outgoing links, backlinks with snippets, See also (tag-related), hover previews, Copy MD, Agent copy (OKF handoff). Hub pages add Copy hub cluster.

### 5.7 Flashcards

~20% of notes are habit-spine (`review: true`). Each carries six `cards:` with scenario cues on the front and one-breath actions on the back. `card_sets:` groups cards in Review.

**Behavior:**

- Flip animation 350ms; crossfade when `prefers-reduced-motion`
- Spaced repetition state in browser `localStorage`
- Lint: `npm run lint:cards`, `npm run audit:cards`

### 5.8 OKF interoperability

The garden aligns with [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) for agent export, not for replacing Hugo authoring.

| Live garden | OKF bundle (`/exports/okf/`) |
| --- | --- |
| `[[wikilinks]]` | Resolved markdown links |
| Hugo frontmatter | Flattened concept/hub files |
| Graph at runtime | Static viz at `/exports/okf/viz.html` |

Regenerate: `npm run export:okf` (also runs on production build).

---

## 6. Functional requirements

### 6.1 Site-wide

| ID | Requirement |
| --- | --- |
| FR-001 | The site MUST render as static HTML/CSS/JS with no server-side user sessions |
| FR-002 | All primary content MUST be authored as Markdown in Git |
| FR-003 | The site MUST support light and dark themes with persisted user preference |
| FR-004 | Full-text search MUST index blog, notes, and pages |
| FR-005 | Navigation MUST be keyboard-operable with visible focus indicators |
| FR-006 | Skip-to-content link MUST be available on all pages |
| FR-007 | RSS feeds MUST be emitted for blog and notes sections |
| FR-008 | Security headers and CSP MUST be applied via `static/_headers` |
| FR-009 | Google Analytics and Cloudflare Web Analytics MAY be configured per environment |
| FR-010 | Disqus MAY be enabled on blog singles when shortname is set |

### 6.2 Blog

| ID | Requirement |
| --- | --- |
| FR-101 | Blog posts MUST expose title, date, categories, tags, and excerpt on list views |
| FR-102 | Blog singles MUST show related posts scored by keywords, tags, and categories |
| FR-103 | Blog singles MAY declare `related_notes` to bridge into the garden |
| FR-104 | Long posts SHOULD show table of contents when headings exist |
| FR-105 | Images MUST support lightbox viewing |

### 6.3 Notes garden

| ID | Requirement |
| --- | --- |
| FR-201 | Atomic notes MUST store claim, angle, examples, and relationships in frontmatter |
| FR-202 | Wikilinks MUST resolve to note pages or aliases |
| FR-203 | Each note MUST list outgoing links and backlinks with context snippets |
| FR-204 | See also MUST suggest tag-related notes not already linked |
| FR-205 | Graph MUST visualize note nodes and link edges with filters |
| FR-206 | Issues MUST aggregate link and structure warnings garden-wide |
| FR-207 | Copy MD MUST copy the raw Hugo source of the current note |
| FR-208 | Agent copy MUST emit OKF-style markdown with resolved links |
| FR-209 | Random resurfacing MUST pick from published non-meta, non-draft notes |
| FR-210 | Utility pages MUST be excluded from graph nodes and random pickers |
| FR-211 | Hover previews MUST show target note title and description on wikilink focus |

### 6.4 Build & quality gates

| ID | Requirement |
| --- | --- |
| FR-301 | `pnpm run deploy` MUST produce a complete `public/` directory |
| FR-302 | `pnpm run lint:notes` MUST fail the build log on broken wikilinks |
| FR-303 | `pnpm run lint:garden` MUST validate frontmatter, cards, and utility links |
| FR-304 | Theme tokens MUST regenerate from `data/theme.json` before Hugo build |
| FR-305 | Note file dates MUST refresh before Hugo build |
| FR-306 | OKF bundle MUST regenerate on production deploy |

---

## 7. Non-functional requirements

### 7.1 Performance

| ID | Requirement |
| --- | --- |
| NFR-001 | First Contentful Paint SHOULD meet Core Web Vitals "good" on home, blog, and notes list |
| NFR-002 | Inter MUST be self-hosted with `font-display: swap` |
| NFR-003 | Images SHOULD use modern formats and explicit dimensions where possible |
| NFR-004 | JavaScript for graph and flashcards MUST lazy-load only on notes tool pages |

### 7.2 Accessibility

| ID | Requirement |
| --- | --- |
| NFR-101 | Primary flows MUST target WCAG 2.1 Level AA contrast and keyboard use |
| NFR-102 | Touch targets MUST be at least 44×44px on interactive controls |
| NFR-103 | Motion MUST respect `prefers-reduced-motion` |
| NFR-104 | Theme switcher MUST expose accessible name and state |

### 7.3 Security & privacy

| ID | Requirement |
| --- | --- |
| NFR-201 | CSP MUST restrict script execution to hashed inline and allowlisted sources |
| NFR-202 | No secrets MUST be committed to the repository |
| NFR-203 | Privacy policy MUST reflect active analytics and comment embeds |

### 7.4 Compatibility

| ID | Requirement |
| --- | --- |
| NFR-301 | CSS MUST target Baseline widely available features (24-month support window) |
| NFR-302 | Site MUST render on current evergreen desktop and mobile browsers |
| NFR-303 | Hugo version in CI MUST match local pin in `deploy-versions.json` |

### 7.5 Maintainability

| ID | Requirement |
| --- | --- |
| NFR-401 | One commit per publish batch SHOULD be preferred to conserve CI builds |
| NFR-402 | `[skip ci]` MUST be available for non-deploy path changes |
| NFR-403 | Functional changes SHOULD be recorded in `CHANGELOG.md` |

---

## 8. Visual & voice constraints

All surfaces inherit **The Quiet Study** design system. Full tokens and component rules: [`DESIGN.md`](./DESIGN.md).

**Hard constraints from PRODUCT:**

- Ideas before optics; professional is the baseline
- Speak to buyers, not only builders
- No performative nerd / dev-bro energy on the marketing shell
- No generic SaaS landing sameness
- No chaotic personal brand layouts
- Single accent color (charcoal/cream inversion); no second display font without PRODUCT change

Notes tool UI (graph, filters, flashcards) uses the same tokens as blog cards—no second palette.

---

## 9. Deployment & operations

### 9.1 Commands

| Command | Purpose |
| --- | --- |
| `pnpm dev` | Local dev (Tailwind watch + note dates + Hugo) |
| `pnpm run deploy` | Production build |
| `pnpm run lint:garden` | Full garden quality gate |
| `pnpm run export:okf` | Regenerate OKF bundle |
| `pnpm run test:search` | Search index smoke test |

### 9.2 Cloudflare Pages

- **Build command:** `pnpm run deploy`
- **Output directory:** `public`
- **Env vars:** `NODE_VERSION`, `GO_VERSION` (build); Hugo from `deploy-versions.json`
- **Build cache:** Enabled; Hugo cache dir `.cache`

### 9.3 Git hooks

`scripts/setup-git-hooks.sh` installs `prepare-commit-msg` to append `[skip ci]` when commits touch only non-deploy paths (`.specstory/`, `docs/`, `.cursor/`, etc.).

---

## 10. Out of scope

The following are explicitly **not** goals of this platform:

| Excluded | Reason |
| --- | --- |
| User accounts and authentication | Static-first; no server state |
| E-commerce and payments | Not a product storefront |
| Real-time collaboration | Git is the collaboration layer |
| Server-side search index updates | Search index is build-time JSON |
| Newsletter sending infrastructure | No workflow behind signup yet |
| PWA / offline (for now) | Evaluated; cost vs benefit on free tier |
| Second brand accent or display font | PRODUCT constraint |
| Wikilink pipe labels | Simplifies parser and lint |
| Non-git CMS with separate database | CMS edits Markdown in repo |

---

## 11. Success criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | A first-time client skim completes in under 3 minutes with clear credibility signal | User test / analytics bounce on `/` and `/blog/` |
| SC-002 | 95% of published wikilinks resolve without Issues warnings | `lint:notes` + Issues page empty |
| SC-003 | Search returns relevant result in top 5 for note titles and blog keywords | `test:search` + manual spot checks |
| SC-004 | Notes graph and review work on mobile touch (44px targets) | `test:responsive` + device check |
| SC-005 | Production deploy completes in under 5 minutes on typical push | Cloudflare build logs |
| SC-006 | OKF export includes 100% of published non-meta notes | Bundle index count vs Hugo section count |
| SC-007 | Lighthouse accessibility score ≥ 90 on home and one blog post | PageSpeed / Lighthouse |
| SC-008 | Zero CSP violations in browser console on primary flows | Manual + production check |

---

## 12. Assumptions

1. **Single author** — JoRap is primary content owner; multi-author Hugo support exists but is not the main workflow.
2. **English only** — `defaultContentLanguage = en`; no i18n requirement.
3. **Git literacy for publishing** — Authors using CMS still commit through git-backed Static Site CMS.
4. **Cloudflare free tier** — Build budget (~500/month) informs batch commits and `[skip ci]`.
5. **Agent consumers are assistive** — ChatGPT and similar tools draft or maintain; Hugo remains source of truth.
6. **Faith and work themes coexist** — Garden includes theological and professional notes under one voice (see jorap-voice skill).

---

## 13. Revision history

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2026-07-03 | Initial complete platform specification |

---

*When PRODUCT, DESIGN, or constitution change, update the relevant companion doc first, then align this spec's references and any affected requirements.*
