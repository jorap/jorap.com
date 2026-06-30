# Client site starter files

Copy into a new repo. Full checklist: [`docs/CLIENT_STATIC_SITE.md`](../../docs/CLIENT_STATIC_SITE.md).

Reference implementation: [jorap.com](https://github.com/jonathanrapusas/jorap.com).

## Minimum new-repo steps

1. Copy `wrangler.toml.example` → `wrangler.toml`; set `name` and OAuth vars if using CMS.
2. Copy `scripts/deploy-versions.json` from JoRap (single source of truth for tool pins).
3. Add `scripts/deployBuild.mjs` (or use bare `hugo --minify --cacheDir=$PWD/.cache` in Pages build command).
4. Connect repo to Cloudflare Pages; build command `pnpm run deploy`; output `public`.
5. Set `NODE_VERSION` / `GO_VERSION` in **Dashboard → Settings → Build → Variables**, then enable **Build cache** in the same Build section.
6. Run `scripts/setup-git-hooks.sh` to conserve builds on non-site commits.
