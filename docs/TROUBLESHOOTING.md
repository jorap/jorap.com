# Troubleshooting Cloudflare Functions 404 Error

## Current Issue
Getting "404 Not Found" when accessing `/api/auth` endpoint.

## Quick Checks

### 1. Verify Functions Are Deployed
1. Go to your Cloudflare Pages dashboard
2. Select your project (`jorap.com`)
3. Go to **Functions** tab
4. You should see `api/auth` and `api/callback` listed

### 2. Check Environment Variables
1. Go to **Settings** → **Environment Variables**
2. Ensure these are set for **Production**:
   - `GITHUB_CLIENT_ID` = your GitHub OAuth app client ID
   - `GITHUB_CLIENT_SECRET` = your GitHub OAuth app client secret

### 3. Test Functions Deployment
Visit: `https://jorap.com/api/test`
- If this works: Functions are deployed, OAuth issue
- If this fails: Functions deployment issue

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
- **Solution**: Set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in Cloudflare Pages

### OAuth App Configuration
- **Cause**: Incorrect callback URL in GitHub OAuth app
- **Solution**: Update callback URL to `https://jorap.com/api/callback`

### DNS/Domain Issues
- **Cause**: Custom domain not properly configured
- **Solution**: Try using the `.pages.dev` domain first

## Step-by-Step Verification

1. **Test Functions**: Visit `https://jorap.com/api/test`
2. **Check OAuth Flow**: Visit `https://jorap.com/api/auth`
3. **Test CMS**: Visit `https://jorap.com/admin/`

## Next Steps

1. Push this code to GitHub
2. Wait for Cloudflare Pages to deploy
3. Test the `/api/test` endpoint first
4. If test works, set up environment variables
5. Test OAuth flow

## Contact Support

If issues persist:
- Check Cloudflare Pages status
- Review function deployment logs
- Verify domain configuration
- Test with `.pages.dev` domain instead of custom domain 