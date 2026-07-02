# Static Site CMS setup (Cloudflare Pages + GitHub)

This guide covers the content admin at `/admin` on your Hugo site. The UI is branded **Static Site CMS**; the engine is [Sveltia CMS](https://sveltiacms.app/en/docs) (a modern successor to Netlify/Decap CMS) with GitHub OAuth through Cloudflare Pages Functions. It uses the same `config.yml` model as Decap; see the [migration guide](https://sveltiacms.app/en/docs/migration/netlify-decap-cms) for details.

Branding lives in `static/admin/config.yml`:

```yaml
app_title: Static Site CMS
site_url: https://www.jorap.com
logo:
  src: /images/jorap.png
  show_in_header: true
```

## Prerequisites

- Hugo site on Cloudflare Pages
- GitHub repository for the site
- GitHub account with access to the repository

## Step 1: Create a GitHub OAuth app

1. Go to GitHub **Settings** → **Developer settings** → **OAuth Apps**
2. Click **New OAuth App**
3. Set:
   - **Application name**: e.g. “Static Site CMS”
   - **Homepage URL**: `https://www.jorap.com` (your live URL)
   - **Authorization callback URL**: `https://www.jorap.com/api/callback`
4. Register the app and note the **Client ID** and **Client Secret**

## Step 2: Cloudflare Pages credentials

This project manages plain env vars in `wrangler.toml`. Only encrypted **secrets** can be set in the Cloudflare dashboard.

1. **`GITHUB_CLIENT_ID`** — edit `wrangler.toml`, set `[vars].GITHUB_CLIENT_ID` to your OAuth app Client ID, commit, and deploy. (Client IDs are public; fine in git.)

2. **`GITHUB_CLIENT_SECRET`** — set once as an encrypted secret (pick one):
   - **Dashboard:** Pages → **jorap-com** → **Settings** → **Variables and Secrets** → **Add** → type **Secret** → name `GITHUB_CLIENT_SECRET`
   - **CLI:** `pnpm exec wrangler pages secret put GITHUB_CLIENT_SECRET --project-name jorap-com`

3. **Local dev:** copy `.dev.vars.example` → `.dev.vars` and fill both values (`.dev.vars` is gitignored).

Redeploy after changing either value.

## Step 3: CMS configuration

1. Open `static/admin/config.yml`
2. Confirm the backend matches your repo and domain, for example:

   ```yaml
   backend:
     name: github
     repo: jorap/jorap.com
     branch: master
     base_url: https://www.jorap.com
     auth_endpoint: /api/auth
   ```

3. Admin UI is loaded from `static/admin/index.html` via the Sveltia CMS bundle (`@sveltia/cms`).

## Step 4: Deploy and test

1. Push changes and wait for the Pages build
2. Open `https://www.jorap.com/admin/` and sign in with GitHub

## File layout

```
/
├── static/
│   └── admin/
│       ├── index.html    # loads Sveltia CMS
│       └── config.yml    # collections, backend & branding
├── functions/
│   └── api/
│       ├── auth.js
│       └── callback.js
└── docs/CMS_SETUP.md
```

## Troubleshooting

See [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) for redirects, Functions 404, build failures, and CMS issues.

- **Login fails**: Check OAuth callback URL (`https://www.jorap.com/api/callback`), env vars, and the **Functions** tab for `api/auth` and `api/callback`
- **Cannot save**: Confirm repo name/branch in `config.yml` and that your GitHub user can push to the repo
- **Blank admin (Cloudflare)**: The admin `index.html` uses `data-cfasync="false"` on the script so Rocket Loader does not break the CMS
- **Missing logo on login**: Confirm `assets/images/jorap.png` exists and Hugo serves it at `/images/jorap.png`

## References

- [Sveltia CMS — Getting started](https://sveltiacms.app/en/docs/start)
- [Sveltia CMS — Customization (logo, app title)](https://sveltiacms.app/en/docs/customization)
- [Migrating from Netlify or Decap CMS](https://sveltiacms.app/en/docs/migration/netlify-decap-cms)
