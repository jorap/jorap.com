# Content Management

Markdown under the language content dir, rendered via Hugo's content/layout pairing. Content lives at root: `content/english/`.

## Architecture

Multilingual — each language sets `contentDir` in `config/_default/languages.toml` (English → `content/english/`). **List the dir before assuming the language** (e.g. `content/english/blog/post.md` → English, not `content/blog/post.md`).
Common examples often found here include:

- **Blog Posts**: `blog/` (posts + `_index.md`).
- **Authors**: `authors/` (one file each + `_index.md`).
- **Pages**: `about/_index.md`, `contact/_index.md`, `pages/*.md`.
- **Reuseable Sections**: `sections/*.md`.

## Frontmatter (common fields)

Hugo reads what templates expect. **Blog posts:** use the field order in `archetypes/blog.md` (normalized by `pnpm lint:blog`).

- `title`: String. The main title of the post.
- `meta_title`: String. SEO / browser tab title.
- `description`: String. Short summary used for lists and SEO.
- `slug`: String. URL path under `/blog/` (filename without `__` prefix when it matches).
- `date`: ISO date string with `Z` (e.g. `2026-07-14T05:00:00Z`).
- `image`: String. Path to the cover image (starts with `/images/`).
- `categories`: String array. Taxonomy for the post.
- `author`: String. Must be `JoRap` and match an author `title` in `authors/`.
- `tags`: String array. Taxonomy tags.
- `related_notes`: Optional list of note slugs for garden cross-links.
- `aliases`: Optional. Extra URL aliases (rare).
- `featured`: Boolean (`true`/`false`).
- `draft`: Boolean (`true`/`false`).
- `lastmod`: Optional. Last-updated ISO date (rare).

## Section-specific common frontmatter:

- **Blog post**: all fields above in order; `draft: true` hides in prod. Run `python3 scripts/normalize-blog-frontmatter.py --write` after bulk edits.
- **Author**: `title`, `email`, `image`, `description`, `social[]`.
- **any reuseable section** (`sections/*.md`): `enable`, `title`, `image`, `description`, `button` (`enable`/`label`/`link`), and `build.render: "never"`

## Naming, Images, i18n

- Kebab-case filenames → URL slug (`my-post.md` → `/blog/my-post/`). Section landing = `_index.md` (branch bundle); co-located resources = `page/index.md` (leaf bundle).
- **Draft posts** (this site): prefix the filename with `__` (e.g. `__my-post.md`) and set `draft: true`. Set `slug: "my-post"` in frontmatter (same order as `archetypes/blog.md`). To publish, rename without the prefix and set `draft: false`.
- Images go under `assets/images/` and use image module `{{ partial "image" (dict "Src" .image "Alt" "..." "Loading" "eager" "Class" "..." "DisplayXL" "800x") }}` — don't hand-write `<img>`.

## Common Mistakes / What NOT to do

- **DO NOT** Reference an `author` with no file in `authors/`.
- **DO NOT** Drop `build.render: "never"` from section files (creates stray pages).
- **DO NOT** Use relative image paths — use `/images/...` under `assets/images/`.
- **DO NOT** Put content outside the language `contentDir`.
