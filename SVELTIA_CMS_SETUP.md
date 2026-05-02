# Sveltia CMS setup (Cloudflare Pages + GitHub)

This guide covers Sveltia CMS on your Hugo site with GitHub OAuth through Cloudflare Pages Functions. Sveltia is a modern successor to Netlify/Decap CMS and uses the same `config.yml` model; see the [migration guide](https://sveltiacms.app/en/docs/migration/netlify-decap-cms) for details.

## Prerequisites

- Hugo site on Cloudflare Pages
- GitHub repository for the site
- GitHub account with access to the repository

## Step 1: Create a GitHub OAuth app

1. Go to GitHub **Settings** → **Developer settings** → **OAuth Apps**
2. Click **New OAuth App**
3. Set:
   - **Application name**: e.g. “JoRap CMS”
   - **Homepage URL**: `https://www.jorap.com` (your live URL)
   - **Authorization callback URL**: `https://www.jorap.com/api/callback`
4. Register the app and note the **Client ID** and **Client Secret**

## Step 2: Cloudflare Pages environment variables

1. Cloudflare Pages → your project → **Settings** → **Environment variables**
2. For **Production** and **Preview**, add:
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET`

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
│       └── config.yml    # collections & backend
├── functions/
│   └── api/
│       ├── auth.js
│       └── callback.js
└── SVELTIA_CMS_SETUP.md
```

## Troubleshooting

- **Login fails**: Check OAuth callback URL, env vars, and the **Functions** tab for `api/auth` and `api/callback`
- **Cannot save**: Confirm repo name/branch in `config.yml` and that your GitHub user can push to the repo
- **Blank admin (Cloudflare)**: The admin `index.html` uses `data-cfasync="false"` on the script so Rocket Loader does not break the CMS

## References

- [Sveltia CMS — Getting started](https://sveltiacms.app/en/docs/start)
- [Migrating from Netlify or Decap CMS](https://sveltiacms.app/en/docs/migration/netlify-decap-cms)
