# Troubleshooting Cloudflare Functions 404 Error

## Current Issue
Getting "404 Not Found" when accessing `/api/auth` endpoint.

## Quick Checks

### 1. Verify Functions Are Deployed
1. Go to your Cloudflare Pages dashboard
2. Select your project (`jorap.com`)
3. Go to **Functions** tab
4. You should see `api/auth` and `api/callback` listed

### 2. Check OAuth credentials

Plain vars come from `wrangler.toml`; secrets from the dashboard or Wrangler CLI.

1. **`wrangler.toml`** — `[vars].GITHUB_CLIENT_ID` must be your GitHub OAuth app Client ID (not empty).
2. **Secret** — `GITHUB_CLIENT_SECRET` must be set:
   - Dashboard → Pages → **jorap-com** → **Settings** → **Variables and Secrets** → add secret `GITHUB_CLIENT_SECRET`, or
   - `pnpm exec wrangler pages secret put GITHUB_CLIENT_SECRET --project-name jorap-com`
3. Redeploy after changes.

Visit `https://www.jorap.com/api/auth` — the redirect URL must show a real `client_id=`, not `client_id=undefined` or empty.

### 3. Test Functions Deployment
Visit: `https://jorap.com/api/auth`
- If you get a redirect to GitHub: Functions are deployed
- If you get 404: Functions deployment issue — check the **Functions** tab in the dashboard

## Solutions

### Solution 1: Force Redeploy
1. Go to **Deployments** tab in Cloudflare Pages
2. Click **Retry deployment** on the latest deployment
3. Or make a small change to trigger new deployment

### Solution 2: Check Build Logs
1. Go to **Deployments** tab
2. Click on the latest deployment
3. Check the **Build log** for errors
4. Look for function deployment messages

### Solution 3: Manual Function Check
1. In Cloudflare Pages dashboard
2. Go to **Functions** tab
3. Check if `api/auth` and `api/callback` are listed
4. Check routes are correct: `/api/auth` and `/api/callback`

### Solution 4: GitHub OAuth App Setup
If functions work but OAuth fails:
1. Go to GitHub → Settings → Developer settings → OAuth Apps
2. Check your OAuth app settings:
   - Homepage URL: `https://jorap.com`
   - Authorization callback URL: `https://jorap.com/api/callback`

## Common Issues

### Functions Not Deploying
- **Cause**: Code syntax errors or build issues
- **Solution**: Check deployment logs for errors

### Environment Variables Not Set
- **Cause**: Missing GitHub OAuth credentials
- **Solution**: Set `GITHUB_CLIENT_ID` in `wrangler.toml` `[vars]` and `GITHUB_CLIENT_SECRET` as a Pages secret (dashboard or `wrangler pages secret put`). Redeploy.

### OAuth App Configuration
- **Cause**: Incorrect callback URL in GitHub OAuth app
- **Solution**: Update callback URL to `https://jorap.com/api/callback`

### DNS/Domain Issues
- **Cause**: Custom domain not properly configured
- **Solution**: Try using the `.pages.dev` domain first

## Step-by-Step Verification

1. **Test Functions**: Visit `https://jorap.com/api/auth` (expect GitHub OAuth redirect)
2. **Check OAuth Flow**: Complete the redirect flow from step 1
3. **Test CMS**: Visit `https://jorap.com/admin/`

## Next Steps

1. Push this code to GitHub
2. Wait for Cloudflare Pages to deploy
3. Test `/api/auth` (expect GitHub redirect)
4. Set up environment variables if OAuth fails
5. Test OAuth flow and CMS

## Contact Support

If issues persist:
- Check Cloudflare Pages status
- Review function deployment logs
- Verify domain configuration
- Test with `.pages.dev` domain instead of custom domain 