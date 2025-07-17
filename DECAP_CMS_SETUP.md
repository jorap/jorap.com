# Decap CMS Setup for Cloudflare Pages

This guide will help you set up Decap CMS on your Hugo site hosted on Cloudflare Pages with GitHub OAuth authentication.

## Prerequisites

- Hugo site hosted on Cloudflare Pages
- GitHub repository for your site
- GitHub account with admin access to the repository

## Step 1: Create GitHub OAuth App

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in the details:
   - **Application name**: "Your Site CMS" (or any name you prefer)
   - **Homepage URL**: `https://your-site.pages.dev` (replace with your actual domain)
   - **Authorization callback URL**: `https://your-site.pages.dev/api/callback`
4. Click "Register application"
5. Copy the **Client ID** and generate a new **Client Secret**
6. **Important**: Keep the Client Secret secure - you'll need it for the next step

## Step 2: Configure Cloudflare Pages Environment Variables

1. Go to your Cloudflare Pages dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add these environment variables for **Production** and **Preview**:
   - **GITHUB_CLIENT_ID**: Your GitHub OAuth App Client ID
   - **GITHUB_CLIENT_SECRET**: Your GitHub OAuth App Client Secret

## Step 3: Update CMS Configuration

1. Open `static/admin/config.yml`
2. Replace the placeholder values:
   ```yaml
   backend:
     name: github
     repo: your-username/your-repo-name  # Replace with your actual GitHub repo
     branch: master  # or main, depending on your default branch
     base_url: https://your-site.pages.dev  # Replace with your actual domain
     auth_endpoint: /api/auth
   ```

## Step 4: Deploy and Test

1. Commit and push your changes to GitHub
2. Wait for Cloudflare Pages to build and deploy
3. Visit `https://your-site.pages.dev/admin/` to access the CMS
4. Click "Login with GitHub" to authenticate

## File Structure

Your project should now have these new files:
```
/
├── static/
│   └── admin/
│       ├── index.html
│       └── config.yml
├── functions/
│   └── api/
│       ├── auth.js
│       └── callback.js
└── DECAP_CMS_SETUP.md
```

## Content Management

The CMS is configured to manage:
- **Blog Posts**: Full editing capabilities for all blog posts
- **Authors**: Manage author profiles and information
- **Pages**: Static pages like Privacy Policy, etc.
- **About Page**: Direct editing of the about page
- **Homepage**: Edit banner and features sections
- **Settings**: Site configuration and metadata

## Troubleshooting

### Common Issues:

1. **"Login with GitHub" doesn't work**
   - Check that environment variables are set correctly
   - Verify OAuth app callback URL matches your domain
   - Ensure functions are deployed (check Functions tab in Cloudflare Pages)

2. **CMS loads but can't save changes**
   - Verify GitHub permissions (repo scope)
   - Check that the repository name in config.yml is correct
   - Ensure you have write access to the repository

3. **Images not uploading**
   - Images are stored in `static/images/` and committed to Git
   - Large images may take time to upload
   - Check browser console for upload errors

### Advanced Configuration

- **Custom collections**: Edit `static/admin/config.yml` to add new content types
- **Field customization**: Modify field types and validation rules
- **Media library**: Configure external media storage if needed

## Security Notes

- The `/admin/` path has `noindex` meta tag to prevent search engine indexing
- OAuth tokens are handled securely by Cloudflare Functions
- Environment variables are encrypted at rest in Cloudflare

## Support

If you encounter issues:
1. Check the browser console for JavaScript errors
2. Verify all environment variables are set
3. Test OAuth flow manually by visiting `/api/auth`
4. Review Cloudflare Pages function logs for server errors

## Next Steps

- Customize the CMS interface by modifying `config.yml`
- Add editorial workflows for content approval
- Set up backup strategies for your content
- Consider implementing media optimization for images 