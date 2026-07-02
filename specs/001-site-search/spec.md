# Feature Specification: Site Search

**Feature Branch**: `001-site-search`  
**Created**: 2026-07-03  
**Status**: Draft  
**Input**: User description: "Site-wide full-text search across blog and notes garden — modal UI, valid search index, ranked results"

**Platform context:** [`docs/SPEC.md`](../../docs/SPEC.md) (FR-004, SC-003)

---

## User Scenarios & Testing

### User Story 1 — Find a note or post by title (Priority: P1)

A reader opens search from the header, types part of a note title, and clicks the matching result to navigate there.

**Why this priority**: Title lookup is the most common search path and the fastest credibility test when search is reported broken.

**Independent Test**: Open `/`, trigger search modal, query a known note title substring; first result links to the correct `/notes/:slug/` page.

**Acceptance Scenarios**:

1. **Given** the homepage is loaded, **When** the user opens search and types the first four characters of a published note title, **Then** that note appears in results within one second.
2. **Given** search results are visible, **When** the user activates a result, **Then** the browser navigates to the result URL without console errors.

---

### User Story 2 — Discover content by keyword in body or tags (Priority: P2)

A reader searches for a concept word that appears in note body text or blog tags but not in the title.

**Why this priority**: Garden value is in connected ideas; body and tag matches surface notes the reader did not know existed.

**Independent Test**: Query a word known to appear only in `content` or `tags` of a specific page; that page appears in results below any title match for the same query.

**Acceptance Scenarios**:

1. **Given** a published note whose body mentions "stewardship" but title does not, **When** the user searches "stewardship", **Then** that note appears in results.
2. **Given** two notes match a query (one by title, one by body only), **When** results render, **Then** the title match ranks above the body-only match.

---

### User Story 3 — Search works after production deploy (Priority: P1)

A visitor on the live site uses search without JavaScript console errors.

**Why this priority**: A prior production failure was caused by invalid `searchindex.json` (unescaped control characters); deploy-time validity is non-negotiable.

**Independent Test**: After `pnpm run deploy`, `fetch('/searchindex.json').then(r => r.json())` resolves and `node scripts/test-search.mjs` exits 0.

**Acceptance Scenarios**:

1. **Given** a fresh production build, **When** the browser fetches `/searchindex.json`, **Then** the response parses as valid JSON with no thrown `SyntaxError`.
2. **Given** a note whose `description` contains paragraph breaks, **When** the index is built, **Then** newlines are JSON-escaped and do not break the file.

---

### Edge Cases

- What happens when the query is empty? Modal shows no results (or placeholder state); no fetch error.
- What happens when no pages match? Empty-state message displays; no broken layout.
- What happens when `searchindex.json` is missing (stale CDN)? User sees a graceful failure, not a silent blank modal.
- What happens with special characters in query (`"`, `\`, unicode)? Client-side filter does not throw; no XSS from indexed strings.
- What happens on keyboard-only use? Search modal opens, input is focusable, results are activatable, Escape closes modal.
- What happens on mobile? Search trigger meets 44px touch target; modal is usable on narrow viewports.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST expose a search modal reachable from every primary page header.
- **FR-002**: System MUST build `searchindex.json` at site root on every production build.
- **FR-003**: Index MUST include published (`draft: false`) pages from configured sections (blog and notes by default).
- **FR-004**: Index entries MUST include: section, slug, title, description, date, image, imageSM, searchKeyword, categories, tags, content.
- **FR-005**: String fields in the index MUST be emitted with JSON-safe escaping (no raw control characters in quoted strings).
- **FR-006**: Client MUST filter results by title, description, searchKeyword, tags, categories, and plain-text body content.
- **FR-007**: Client MUST rank title matches above body-only matches for the same query.
- **FR-008**: Results MUST group by section (Blog, Notes) when multiple sections are configured.
- **FR-009**: Pages with `ignoreSearch: true` MUST be excluded from the index.
- **FR-010**: Enter key on search input MUST NOT submit a form or navigate away (modal stays open).
- **FR-011**: System MUST provide an automated check (`scripts/test-search.mjs`) that validates index shape, JSON round-trip, match logic, and HTML wiring.

### Key Entities

- **Search index entry**: One searchable page; keyed by `slug` (permalink); carries display metadata and searchable plain text.
- **Search query**: User-typed string; matched client-side against index entries after index load.
- **Search result group**: Section label plus ordered list of matching entries for that section.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of production builds produce parseable `searchindex.json` (verified by `test-search.mjs`).
- **SC-002**: Querying the first four characters of any published note title returns that note in top five results.
- **SC-003**: Search modal opens and returns results in under 1 second on a warm cache (index already fetched).
- **SC-004**: Zero Content-Security-Policy or JSON parse errors in browser console during a complete search flow on homepage.
- **SC-005**: Keyboard-only user can open search, run a query, activate a result, and close the modal without using a pointer.

---

## Assumptions

1. Search is **client-side only** — no server endpoint; index size is acceptable for current garden scale (~hundreds of pages).
2. **Blog and notes** are the only indexed sections unless `search.include_all_sections` is enabled in site params.
3. **Plain text** from Hugo `.Plain` is sufficient for body search; wikilink syntax in source is stripped at index time.
4. **Images** in results are optional thumbnails; missing image does not block listing.
5. Regression tests in `search-core.mjs` mirror `assets/js/search.js`; both must stay aligned when match logic changes.

---

## Out of Scope

- Fuzzy matching, typo tolerance, or stemming
- Search across draft or unpublished content
- Server-side or incremental index updates
- Search analytics or query logging
- Indexing static pages (about, contact) unless config changes
- Highlighting matched snippets in result cards
