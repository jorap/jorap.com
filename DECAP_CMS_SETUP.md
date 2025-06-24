# Decap CMS Setup - Fresh Installation

This is a fresh, simplified Decap CMS setup for your Hugo site.

## 🎯 What's Included

- **Basic Admin Interface**: Available at `/admin/`
- **GitHub Authentication**: Uses your GitHub account for login
- **Blog Collection**: Edit your blog posts
- **Simple Configuration**: Minimal setup, maximum reliability

## 🔧 Setup Steps

### Step 1: Create GitHub OAuth App

1. **Go to:** [GitHub Settings > Developer settings > OAuth Apps](https://github.com/settings/applications/new)
2. **Fill in:**
   - **Application name:** `JoRap CMS`
   - **Homepage URL:** `https://www.jorap.com`
   - **Authorization callback URL:** `https://www.jorap.com/admin/`
3. **Click "Register application"**
4. **Copy the Client ID** (you'll need this)

### Step 2: Deploy Your Site

1. **Commit and push** your changes to GitHub
2. **Deploy to Cloudflare Pages** (or your hosting platform)
3. **Wait for deployment** to complete

### Step 3: Login to CMS

1. **Visit:** `https://www.jorap.com/admin/`
2. **Click "Login with GitHub"**
3. **Authorize the application** on GitHub
4. **Start editing your content!**

## 📝 How to Use

- **Create new blog posts** using the visual editor
- **Edit existing posts** by clicking on them
- **Save drafts** or publish immediately
- **Upload images** through the media section

## 🛠 Troubleshooting

### If login doesn't work:
1. **Check GitHub OAuth App** callback URL is exactly: `https://www.jorap.com/admin/`
2. **Clear browser cache** and try again
3. **Make sure you have push access** to the `jorap/jorap.com` repository

### If you can't see your content:
1. **Check the folder paths** in `static/admin/config.yml`
2. **Verify your content files** are in `content/english/blog/`

## ✅ That's It!

This simple setup should work reliably without complex OAuth configurations or custom functions. 