---
title: "How I Built JoRap's World: A Complete Guide to Free Website Creation"
meta_title: "How I Built JoRap's World: A Guide to Creating a Free Website"
description: "A simple guide to building a website with Hugo and hosting it for free."
slug: "how-i-built-joraps-world"
date: 2024-06-14T05:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Website"]
author: "John Doe"
tags: ["Website Building", "Free Hosting", "Hugo CMS"]
draft: false
---

## Why I Chose This Tech Stack

After losing my expensive PHP hosting, I needed a simple, free solution for my personal website. I discovered that combining **Hugo** with **Cloudflare Pages** creates a powerful, cost-effective setup that's perfect for personal sites and blogs.

**The Result**: A fast, professional website that costs $0 to host and takes minutes to deploy updates.

---

## The Complete Tech Stack & What Each Does

### 1. **Hugo** - The Website Builder
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

**What it does**: Takes your Hugo-generated files and serves them to visitors from servers around the world.

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

### Step 1: Install Hugo (5 minutes)

**Purpose**: Get the tool that will build your website.

1. **Windows**: Download from [Hugo Releases](https://github.com/gohugoio/hugo/releases)
2. **Mac**: Run `brew install hugo` in Terminal
3. **Linux**: Run `sudo apt install hugo` or similar

**Test installation**: Open terminal/command prompt and type `hugo version`

### Step 2: Create Your Site (2 minutes)

**Purpose**: Set up the basic structure for your website.

```bash
# Create new site
hugo new site my-awesome-site
cd my-awesome-site

# Initialize Git repository
git init
```

**What this creates**:
- `content/` - Where your pages and blog posts go
- `themes/` - Where design templates live
- `config.toml` - Main settings file
- `static/` - Images, CSS, JavaScript files

### Step 3: Choose and Install a Theme (10 minutes)

**Purpose**: Give your site a professional look without designing from scratch.

1. **Browse themes**: Visit [Hugo Themes](https://themes.gohugo.io)
2. **Pick one you like**: Look for "responsive" and "modern" themes
3. **Install it**: Most themes provide installation commands like:

```bash
git submodule add https://github.com/theme-author/theme-name.git themes/theme-name
echo "theme = 'theme-name'" >> config.toml
```

**Pro tip**: Start with popular themes like "Ananke" or "PaperMod" - they're well-documented and beginner-friendly.

### Step 4: Configure Your Site (15 minutes)

**Purpose**: Customize basic settings and branding.

Edit `config.toml`:

```toml
baseURL = 'https://your-site.pages.dev'
languageCode = 'en-us'
title = 'Your Site Name'
theme = 'your-theme-name'

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

### Step 5: Create Your First Content (20 minutes)

**Purpose**: Add actual pages to your website.

**Create an About page**:
```bash
hugo new about.md
```

Edit `content/about.md`:
```markdown
---
title: "About Me"
date: 2024-06-14
---

# Welcome to my site!

This is where I share my thoughts and projects. Built with Hugo and hosted on Cloudflare Pages.

## What I do
- Web development
- Writing about tech
- Building cool projects
```

**Create a blog post**:
```bash
hugo new blog/my-first-post.md
```

### Step 6: Test Locally (5 minutes)

**Purpose**: See how your site looks before publishing.

```bash
hugo server -D
```

Visit `http://localhost:1313` to see your site. The `-D` flag includes draft posts.

### Step 7: Set Up GitHub Repository (10 minutes)

**Purpose**: Store your code and enable automatic deployments.

1. **Create repository**: Go to GitHub.com → New repository
2. **Push your code**:
```bash
git add .
git commit -m "Initial site setup"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Step 8: Deploy to Cloudflare Pages (15 minutes)

**Purpose**: Make your site live on the internet for free.

1. **Sign up**: Go to [Cloudflare Pages](https://pages.cloudflare.com)
2. **Connect GitHub**: Authorize Cloudflare to access your repositories
3. **Create project**: 
   - Select your repository
   - Build command: `hugo`
   - Build output directory: `public`
   - Environment variable: `HUGO_VERSION` = `0.112.0` (or latest)
4. **Deploy**: Click "Save and Deploy"

**Result**: Your site will be live at `https://your-project.pages.dev` in 2-3 minutes!

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

## Why This Setup is Perfect for Beginners

### Cost Breakdown
- **Hugo**: Free and open source
- **GitHub**: Free for public repositories
- **Cloudflare Pages**: Free tier includes everything you need
- **Total monthly cost**: $0

### Benefits You Get
1. **Professional appearance**: Modern, responsive themes
2. **Fast loading**: Static sites load in milliseconds
3. **SEO friendly**: Clean URLs and fast loading help with search rankings
4. **Mobile responsive**: Works perfectly on all devices
5. **Secure**: No database means no security vulnerabilities
6. **Scalable**: Can handle thousands of visitors without issues

### Skills You'll Learn
- **Basic command line usage**: Essential developer skill
- **Git version control**: Used by all professional developers
- **Markdown writing**: Popular format used everywhere
- **Web deployment**: Understanding how sites go live
- **Static site concepts**: Foundation for modern web development

---

## Troubleshooting Common Issues

### Theme Not Showing
- Check that theme name in `config.toml` matches folder name in `themes/`
- Ensure theme was installed as Git submodule, not just downloaded

### Build Fails on Cloudflare
- Set correct Hugo version in environment variables
- Check that `baseURL` in config matches your Cloudflare domain

### Content Not Appearing
- Remove `draft: true` from front matter
- Ensure files are in correct `content/` subdirectories

---

## Next Steps and Advanced Features

Once comfortable with the basics, you can explore:

1. **Custom domain**: Point your own domain to Cloudflare Pages
2. **Contact forms**: Add Netlify Forms or similar service
3. **Analytics**: Integrate Google Analytics or Cloudflare Analytics
4. **Comments**: Add Disqus or similar commenting system
5. **Search**: Implement site search functionality
6. **Custom themes**: Modify existing themes or create your own

---

## Conclusion

Building JoRap's World taught me that modern web development doesn't have to be complicated or expensive. With Hugo and Cloudflare Pages, you get:

- **Professional results** without professional complexity
- **Zero ongoing costs** for hosting and maintenance
- **Modern workflow** that scales as you learn and grow
- **Future-proof technology** that won't become obsolete

Whether you're building a personal blog, portfolio, or small business site, this stack provides everything you need to create something you'll be proud to share.

**Ready to start?** The entire setup takes about an hour, and you'll have a live website by the end of it. Happy building!

---

## Helpful Resources

- **Hugo Documentation**: [gohugo.io/documentation](https://gohugo.io/documentation/)
- **Hugo Themes**: [themes.gohugo.io](https://themes.gohugo.io)
- **Cloudflare Pages Docs**: [developers.cloudflare.com/pages](https://developers.cloudflare.com/pages/)
- **Markdown Guide**: [markdownguide.org](https://www.markdownguide.org/)
- **Git Basics**: [git-scm.com/doc](https://git-scm.com/doc)
