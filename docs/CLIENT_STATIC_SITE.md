# Client static site template (Hugo + GitHub + Cloudflare Pages)

JoRap.com is the reference implementation. Clone this pattern for freelance client sites: one GitHub repo, one Cloudflare Pages project, client-owned accounts at scale.

## New client checklist

### 1. GitHub

- [ ] Create repo (private is fine on GitHub free).
- [ ] Copy or generate site from this template (see [`templates/client-site/`](../templates/client-site/)).
- [ ] If theme is a submodule: **Settings → enable submodules** in Cloudflare later.

### 2. Cloudflare Pages

- [ ] **Workers & Pages → Create → Connect to Git** → pick the repo.
- [ ] Production branch: `master` (or your default; JoRap uses `master`).
- [ ] Build command: `pnpm run deploy` (or `npm run deploy` if no pnpm).
- [ ] Build output directory: `public`.
- [ ] **Settings → Build → Variables** — set `NODE_VERSION` and `GO_VERSION`. These are *build-time* vars; `wrangler.toml [vars]` are runtime-only and won't apply at build. Hugo version is handled in-repo by `scripts/ensureHugo.mjs`.
- [ ] **Settings → Build → Build cache → Enable** (one-time; or `curl` the API — see below).
- [ ] **Settings → Git → Submodule cloning → Enable** (if theme is a submodule).

Enable build cache without the dashboard:

```bash
curl https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME \
  -X PATCH -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"build_config":{"build_caching":true}}'
```

### 3. `wrangler.toml` (committed in repo)

Copy [`templates/client-site/wrangler.toml.example`](../templates/client-site/wrangler.toml.example). Set:

| Field | Source |
|-------|--------|
| `name` | Cloudflare Pages project name |
| `pages_build_output_dir` | `public` (Hugo default) |
| `GITHUB_CLIENT_ID` (optional) | GitHub OAuth app, if using `/admin` CMS |

Tool versions are pinned once in [`scripts/deploy-versions.json`](../scripts/deploy-versions.json) (the single source of truth `ensureHugo.mjs` reads). Don't duplicate them into `wrangler.toml`.

### 4. Build pipeline (minimum)

```
edit markdown → git push → Cloudflare builds → live on CDN
```

Production build must run Hugo with a cache dir so Cloudflare can reuse `.cache` between builds:

- JoRap pattern: `scripts/deployBuild.mjs` runs `hugo --minify --cacheDir .cache` plus any pre-steps (Tailwind, CSP, etc.).
- Simple Hugo-only sites: `hugo --minify --cacheDir=$PWD/.cache`

Pin tool versions. Version drift between laptop and Cloudflare is the most common deploy failure.

### 5. DNS

- [ ] Add **both** apex and `www` as custom domains in Pages (e.g. `jorap.com` and `www.jorap.com`).
- [ ] Point domain DNS to Cloudflare (registrar or CF DNS).
- [ ] Pick **www** or **apex** as canonical and redirect the other in `static/_redirects` (Hugo copies it to `public/_redirects`).

JoRap pattern (apex → www):

```
http://example.com/* https://www.example.com/:splat 301!
https://example.com/* https://www.example.com/:splat 301!
```

Both hostnames must be attached in Pages or the redirect target will 404.

### 6. Optional CMS (`/admin`)

See [`CMS_SETUP.md`](./CMS_SETUP.md). Needs Pages Functions + GitHub OAuth app per client.

### 7. Handoff doc (one page)

Give the client:

- GitHub org/repo URL
- Cloudflare account login (their account, not yours)
- Domain registrar login
- Build command + env vars list
- Who to email when the site is down

## Free tier headroom

Re-read [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/) before quoting clients:

| Limit | Typical brochure site |
|-------|------------------------|
| ~500 builds/month (per CF account) | Fine if you batch commits |
| 20,000 files per deploy | Trim theme image bloat |
| 1 concurrent build | Stagger multi-client deploys |
| Unlimited bandwidth | Don't over-optimize bandwidth |

**Scale rule:** pilot on your account; move production to **client-owned Cloudflare + GitHub** before you host many clients on one account.

## Save builds

- Batch content edits into one commit before `git push`.
- Use `[skip ci]` for commits that don't change the site (`.specstory`, internal `docs/`, editor config). See [`.cursor/rules/deploy-commits.mdc`](../.cursor/rules/deploy-commits.mdc).
- Run `scripts/setup-git-hooks.sh` once per clone to auto-append `[skip ci]` for non-deploy paths.

## Astro / 11ty on the same rails

| SSG | Output dir | Build command | CF caches |
|-----|------------|---------------|-----------|
| Hugo | `public` | `pnpm run deploy` or `hugo --minify --cacheDir=$PWD/.cache` | `.cache` |
| Astro | `dist` | `npm run build` | `node_modules/.astro` |
| 11ty | `_site` | `npx @11ty/eleventy` | `.cache` |

Same GitHub → Cloudflare flow; only output directory and build command change.

## Files to copy from JoRap.com

| File | Purpose |
|------|---------|
| `wrangler.toml` | Pages project config (name, output dir, CMS vars) |
| `scripts/deploy-versions.json` | Single source of truth for tool pins |
| `scripts/deployBuild.mjs` | Canonical build (adapt pre-steps per site) |
| `scripts/ensureHugo.mjs` | CI Hugo install when PATH is wrong |
| `static/_headers` | Security headers + long-cache fingerprinted assets |
| `static/_redirects` | www canonicalization + legacy paths |
| `netlify.toml` | Optional Netlify mirror (same env vars) |

Strip JoRap-specific pieces (notes garden, CMS functions, OKF export) unless the client needs them.

## Related

- Garden note: [Free Tier Hosting Stack](/notes/free-tier-hosting-stack/)
- Blog walkthrough: [How I Built JoRap Notes](/blog/how-i-built-jorap-notes/)
- Troubleshooting: [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)
