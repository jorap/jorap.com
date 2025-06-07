---
title: "How I Built JoRap's World: An Introductory Guide to Free and Sustainable Website Creation"
meta_title: "How I Built JoRap's World: A Guide to Creating a Free Website"
description: "A simple guide to building a website with Hugo CMS and hosting it for free."
slug: "how-i-built-joraps-world"
date: 2024-06-14T05:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Website"]
author: "John Doe"
tags: ["Website Building", "Free Hosting", "Hugo CMS"]
draft: false
---

> **Quick Start Guide**: Want the essentials? Hugo CMS + GitHub + Cloudflare Pages = Free professional website in 1 hour. Full walkthrough below, plus [video tutorial](#companion-resources) and [interactive checklist](#companion-resources).

## Why I Chose This Tech Stack

After losing my expensive PHP hosting, I needed a simple, free solution for my personal website. I discovered that combining **Hugo CMS** with **Cloudflare Pages** creates a powerful, cost-effective setup that's perfect for personal sites and blogs.

**The Result**: A fast, professional website that costs $0 to host and takes minutes to deploy updates.

---

## The Complete Tech Stack & What Each Does

### 1. **Hugo CMS** - The Website Builder
**What it is**: A static site generator that converts your content into a complete website.

**Why I chose it**:
- **Lightning fast**: No database queries = instant page loads
- **Zero hosting costs**: Static files can be hosted anywhere for free
- **Simple content creation**: Write in Markdown (plain text with simple formatting)
- **Professional themes**: Hundreds of free, responsive designs available
- **Security**: No database = no security vulnerabilities

**What it does**: Takes your Markdown files and templates, then generates all the HTML, CSS, and JavaScript needed for your website.

### 2. **Cloudflare Pages** - The Free Hosting Platform
**What it is**: A service that hosts static websites for free with enterprise-grade performance.

**Why I chose it**:
- **Completely free**: No hidden costs or limits for personal sites
- **Global CDN**: Your site loads fast worldwide
- **Automatic deployments**: Updates your site whenever you push to GitHub
- **Custom domains**: Use your own domain name for free
- **SSL certificates**: Free HTTPS security

**What it does**: Takes your Hugo CMS-generated files and serves them to visitors from servers around the world.

### 3. **GitHub** - The Code Repository
**What it is**: A platform that stores your code and integrates with Cloudflare Pages.

**Why I use it**:
- **Version control**: Track every change to your site
- **Automatic deployments**: Push code → site updates automatically
- **Backup**: Your entire site is safely stored in the cloud
- **Collaboration**: Easy to work with others or access from any device

**What it does**: Stores your website files and triggers Cloudflare Pages to rebuild your site when you make changes.

### 4. **Markdown** - The Content Format
**What it is**: A simple way to write formatted text using plain text symbols.

**Why it's perfect**:
- **Easy to learn**: `# Heading`, `**bold**`, `*italic*` - that's most of it
- **Portable**: Works with any text editor
- **Fast to write**: No clicking buttons or complex menus
- **Version control friendly**: Git can track changes easily

**What it does**: Lets you write content quickly without worrying about HTML or complex formatting.

---

## Step-by-Step Build Process

### Setup and Installation

**Step 1: Install Hugo CMS (5 minutes)**
- **Windows**: Download from [Hugo CMS Releases](https://github.com/gohugoio/hugo/releases)
- **Mac**: Run `brew install hugo` in Terminal
- **Linux**: Run `sudo apt install hugo` or similar
- **Test installation**: Open terminal/command prompt and type `hugo version`

**Step 2: Create Your Site (2 minutes)**
```bash
# Create new site
hugo new site my-awesome-site
cd my-awesome-site

# Initialize Git repository
git init
```

**What this creates**: `content/` (pages/posts), `themes/` (design templates), `config.toml` (settings), `static/` (images/files)

### Configuration and Content

**Step 3: Choose and Install a Theme (10 minutes)**
1. **Browse themes**: Visit [Hugo CMS Themes](https://themes.gohugo.io)
2. **Pick one you like**: Look for "responsive", "modern", recently updated themes
3. **Install it**: 
```bash
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> config.toml
```

**Step 4: Configure Your Site (15 minutes)**
Edit `config.toml`:
```toml
baseURL = 'https://your-site.pages.dev'
languageCode = 'en-us'
title = 'Your Site Name'
theme = 'your-theme-name'
paginate = 5

[params]
  author = 'Your Name'
  description = 'Your site description'

[menu]
  [[menu.main]]
    name = 'Home'
    url = '/'
  [[menu.main]]
    name = 'About'
    url = '/about/'
  [[menu.main]]
    name = 'Blog'
    url = '/blog/'
```

**Step 5: Create Your First Content (20 minutes)**
```bash
# Create an About page
hugo new about.md

# Create a blog post
hugo new blog/my-first-post.md
```

### Testing and Deployment

**Step 6: Test Locally (5 minutes)**
```bash
hugo server -D
```
Visit `http://localhost:1313` to preview your site.

**Step 7: Set Up GitHub Repository (10 minutes)**
1. Create repository on GitHub.com
2. Push your code:
```bash
git add .
git commit -m "Initial site setup"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

**Step 8: Deploy to Cloudflare Pages (15 minutes)**
1. Sign up at [Cloudflare Pages](https://pages.cloudflare.com)
2. Connect GitHub and select your repository
3. Set build command: `hugo`, output directory: `public`
4. Add environment variable: `HUGO_VERSION` = `0.147.7`
5. Deploy - your site will be live at `https://your-project.pages.dev` in 2-3 minutes!

---

## Common Mistakes (And How to Avoid Them)

**Based on real beginner feedback**, here are the most frequent issues and their solutions:

**1. Theme Not Showing** - Site displays basic HTML with no styling
- Check that theme name in `config.toml` matches folder name in `themes/`
- Ensure theme was installed as Git submodule: `git submodule add [theme-url] themes/[theme-name]`
- Verify theme compatibility with your Hugo CMS version

**2. Build Fails on Cloudflare** - Deployment fails with build errors
- Set correct Hugo CMS version in environment variables (`HUGO_VERSION = 0.147.7`)
- Check that `baseURL` in config matches your Cloudflare domain
- Remove `draft: true` from content that should be published
- Ensure all theme dependencies are properly included

**3. Content Not Appearing** - Pages exist but don't show on site
- Remove `draft: true` from front matter
- Ensure files are in correct `content/` subdirectories
- Check that menu configurations point to existing pages
- Verify content files have proper front matter structure

**4. Local Server Issues** - `hugo server` command fails or shows errors
- Port conflict: Try `hugo server -p 1314` (different port)
- Check for typos in config file (invalid TOML syntax)
- Ensure you're in the correct directory (site root)
- Update Hugo CMS if version is very old

**5. Git Authentication Problems** - Can't push to GitHub repository
- Set up SSH keys or use personal access tokens
- Check repository URL is correct
- Verify you have write permissions to the repository

**6. Images Not Loading** - Images display as broken links
- Place images in `static/images/` folder
- Use absolute paths: `/images/photo.jpg`
- Check file names match exactly (case-sensitive)
- Optimize image sizes (large images slow down builds)

---

## Daily Workflow: How to Update Your Site

**Purpose**: Once set up, updating your site is incredibly simple.

1. **Write new content**: Create `.md` files in your `content/` folder
2. **Test locally**: Run `hugo server -D` to preview
3. **Publish**:
   ```bash
   git add .
   git commit -m "Add new blog post"
   git push
   ```
4. **Automatic deployment**: Cloudflare Pages rebuilds your site automatically

**Time from writing to live**: About 2 minutes after you push to GitHub.

---

## Cost Breakdown: Free vs. Optional Upgrades

**Free Tier (Complete Solution)** - Total monthly cost: **$0**
- **Hugo CMS**: Free and open source
- **GitHub**: Free for public repositories
- **Cloudflare Pages**: Free tier includes everything you need
- **SSL Certificate**: Included free
- **Global CDN**: Included free
- **Automatic deployments**: Included free

**Optional Upgrades (If You Want Them)**

**Custom Domain** ($10-15/year) - Get `yoursite.com` instead of `yoursite.pages.dev`. Worth it for professional brand presence.

**Premium Themes** ($20-100 one-time) - More sophisticated designs and additional features. Worth it if you need advanced functionality or unique styling.

**Enhanced Analytics** ($0-9/month) - Google Analytics is free, premium tools cost $9/month. Detailed visitor insights and conversion tracking. Worth it for business-level analytics.

**Professional Email** ($5-6/month) - Google Workspace ($6) or Zoho ($5) for `contact@yoursite.com` addresses. Worth it for professional communication.

**Advanced CDN Features** ($5-20/month) - Cloudflare Pro for advanced security and image optimization. Worth it for high traffic or specific security needs.

**Total potential monthly cost**: $0-50/month depending on your needs

---

## Why This Setup is Perfect for Beginners

**Benefits You Get**: Professional appearance, fast loading, SEO friendly, mobile responsive, secure (no database vulnerabilities), and scalable to handle thousands of visitors.

**Skills You'll Learn**: Basic command line usage, Git version control, Markdown writing, web deployment, and static site concepts - all essential developer skills used by professionals.

---

## Troubleshooting Common Issues

**Performance Optimization**: Use WebP image format, enable minification in Hugo CMS config for CSS/JS, and keep posts focused and well-structured.

**Security Considerations**: Configure Content Security Policy in Cloudflare settings, enable automatic HTTPS redirects, and never commit sensitive information to Git.

---

## Next Steps and Advanced Features

Once comfortable with the basics, you can explore:

1. **Custom domain**: Point your own domain to Cloudflare Pages ($10-15/year)
2. **Contact forms**: Add Netlify Forms or similar service
3. **Analytics**: Integrate Google Analytics or Cloudflare Analytics
4. **Comments**: Add Disqus or similar commenting system
5. **Search**: Implement site search functionality
6. **Custom themes**: Modify existing themes or create your own
7. **E-commerce**: Add Snipcart for simple online store functionality
8. **Multi-language sites**: Hugo CMS's built-in i18n support

---

## Conclusion

Building JoRap's World taught me that modern web development doesn't have to be complicated or expensive. With Hugo CMS and Cloudflare Pages, you get:

- **Professional results** without professional complexity
- **Zero ongoing costs** for hosting and maintenance  
- **Modern workflow** that scales as you learn and grow
- **Future-proof technology** that won't become obsolete

Whether you're building a personal blog, portfolio, or small business site, this stack provides everything you need to create something you'll be proud to share.

**Ready to start?** The entire setup takes about an hour, and you'll have a live website by the end of it. Happy building!

---

## Helpful Resources

- **Hugo CMS Documentation**: [gohugo.io/documentation](https://gohugo.io/documentation/)
- **Hugo CMS Themes**: [themes.gohugo.io](https://themes.gohugo.io)
- **Cloudflare Pages Docs**: [developers.cloudflare.com/pages](https://developers.cloudflare.com/pages/)
- **Markdown Guide**: [markdownguide.org](https://www.markdownguide.org/)
- **Git Basics**: [git-scm.com/doc](https://git-scm.com/doc)
- **Hugo CMS Community**: [discourse.gohugo.io](https://discourse.gohugo.io)
- **GitHub Learning Lab**: [lab.github.com](https://lab.github.com)
