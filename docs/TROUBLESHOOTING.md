# Troubleshooting

Common deploy, redirect, CMS, and build issues for JoRap Notes on Cloudflare Pages.

**Canonical URL:** [https://www.jorap.com](https://www.jorap.com) - apex `jorap.com` should 301 to `www` (see [Redirects](#redirects-apex--www)).

---

## Redirects (apex → www)

### Symptom

`https://jorap.com` returns 404 or serves without redirecting to `www`.

### Checks

1. **Both domains in Pages** - Workers & Pages → **jorap-com** → **Custom domains** must list `jorap.com` **and** `www.jorap.com`.
2. **`static/_redirects`** - committed rules must copy to `public/_redirects` after `pnpm run deploy`. JoRap uses `301!` force redirects for apex → www.
3. **Deploy includes the file** - inspect latest deployment → **Assets** → confirm `_redirects` exists at site root.

### Fix

Add or restore apex rules in `static/_redirects`, redeploy, then test:

```bash
curl -sI https://jorap.com/ | head -5   # expect 301 → www.jorap.com
curl -sI https://www.jorap.com/ | head -5
```

If DNS is wrong, fix registrar/Cloudflare DNS before debugging redirects.

---

## Cloudflare Functions 404 (`/api/auth`)

### Symptom

CMS login fails; `https://www.jorap.com/api/auth` returns 404.

### Quick checks

1. Pages dashboard → **Functions** tab → `api/auth` and `api/callback` listed.
2. `wrangler.toml` - `[vars].GITHUB_CLIENT_ID` set (not empty).
3. Secret `GITHUB_CLIENT_SECRET` set (dashboard or `pnpm exec wrangler pages secret put GITHUB_CLIENT_SECRET --project-name jorap-com`).
4. Redeploy after credential changes.

### Test

Visit `https://www.jorap.com/api/auth` - expect a redirect to GitHub with a real `client_id=`, not `undefined`.

### OAuth app URLs (GitHub)

| Field | Value |
| --- | --- |
| Homepage URL | `https://www.jorap.com` |
| Authorization callback URL | `https://www.jorap.com/api/callback` |

Full CMS setup: [`CMS_SETUP.md`](./CMS_SETUP.md).

---

## Build failures

### Hugo version mismatch

Cloudflare may not have Hugo on PATH. This repo pins via [`scripts/deploy-versions.json`](../scripts/deploy-versions.json) and installs with [`scripts/ensureHugo.mjs`](../scripts/ensureHugo.mjs) inside `pnpm run deploy`.

### Tailwind / CSS errors

Dev uses `pnpm dev` (Tailwind watch + Hugo). Production runs the same pipeline in `scripts/deployBuild.mjs`. Run `pnpm run deploy` locally to reproduce CI failures.

**`binary "tailwindcss" is not a Node.js script` (common on Windows + pnpm):** run `node scripts/fix-tailwind-bin.js` after `pnpm install`. On Windows, Hugo resolves `tailwindcss.cmd` first; the shim must point at `..\@tailwindcss\cli\dist\index.mjs` in a form Hugo’s wrapper parser understands.

**`js.Build failed: Could not resolve "@pixi/…"` (common on Windows):** pnpm’s default nested `node_modules` layout breaks Hugo’s esbuild for PixiJS. This repo sets `nodeLinker: hoisted` in [`pnpm-workspace.yaml`](../pnpm-workspace.yaml) (pnpm 11+ no longer reads `node-linker` from `.npmrc`). Delete `node_modules` and run `pnpm install` after pulling; reinstall if errors persist.

### CSP header missing in production

Cloudflare Pages drops header values over ~2 KB. `scripts/cspHashes.mjs` rewrites `public/_headers` after build. See comments in [`static/_headers`](../static/_headers).

---

## CMS admin blank or broken

- **Rocket Loader:** admin `index.html` uses `data-cfasync="false"` on the CMS script.
- **Login loop:** verify OAuth callback URL matches `www` canonical host.
- **Cannot save:** `static/admin/config.yml` `repo` and `branch` must match GitHub (`master` for JoRap).

---

## Local dev

| Issue | Fix |
| --- | --- |
| Port in use | Dev: Hugo `1313`; local deploy: wrangler `8788` (`PORT` / `HOST` env vars) |
| Styles missing | Ensure Tailwind watch is running (`pnpm dev`, not bare `hugo`) |
| CMS OAuth locally | Copy `.dev.vars.example` → `.dev.vars` with OAuth credentials |

### Local production preview (Windows, Linux, macOS)

Same pipeline as Cloudflare Pages — use this before pushing, not `pnpm dev`:

```bash
pnpm local              # build + serve at http://127.0.0.1:8788
# or: pnpm run deploy && pnpm run serve
```

`pnpm dev` and `pnpm preview` pass `--buildDrafts` and `--buildFuture` to Hugo, so drafts and future-dated posts appear locally but not on the live site.

**Toolchain:** Hugo Extended, Node 22+, pnpm, Go (mise + [`.mise.toml`](../.mise.toml)), Python 3.8+ for OKF export and garden lint scripts (`node scripts/runPython.mjs` resolves `python` / `python3` / `py -3` on Windows). Run in PowerShell or Git Bash.

### Cross-platform filename checks

Filename safety lint is pure Node — no Python or shell required:

```bash
pnpm test:filenames   # self-check (works without git)
pnpm lint:filenames   # scan git-tracked paths (needs git)
```

`node scripts/lint-filenames.mjs --walk` scans the working tree including untracked files (skips `node_modules`, `public`, `.cache`).

---

## Still stuck

1. Retry latest deployment in Pages dashboard.
2. Compare build log with local `pnpm run deploy`.
3. Test `.pages.dev` preview URL to isolate DNS vs app issues.
4. Check [Cloudflare status](https://www.cloudflarestatus.com/).
