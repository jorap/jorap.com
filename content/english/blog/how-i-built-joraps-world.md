---
title: "How I Built JoRap's World: My Journey from Expensive Hosting to Free (and Better!)"
meta_title: "How I Built JoRap's World: A Developer's Guide to Free Static Site Hosting"
description: "My actual experience building a website with Hugo CMS and hosting it for free - mistakes included!"
slug: "how-i-built-joraps-world"
date: 2024-06-14T05:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Website"]
author: "JoRap"
tags: ["Website Building", "Free Hosting", "Hugo CMS"]
draft: false
---

> **TL;DR**: I lost my old PHP hosting, losing years of work I'd built up. I discovered Hugo + GitHub + Cloudflare Pages = genuinely better than what I was paying for. Here's exactly how I did it (and where I messed up).

## Why I Had to Start Over (The Backstory)

So here's the thing - I was paying around $12/month for some basic PHP hosting, sharing it between a client project and my personal site. Everything was going fine until my client decided to stop hosting their site, leaving me with the full hosting bill for what was essentially just my personal blog.

Like many developers, I found myself in that frustrating position where paying for hosting just didn't make sense anymore. That's when I decided to explore static site generators and the JAMstack approach I'd been hearing about. Sometimes the best solutions come from being forced to find them!

## What I Ended Up Using (And Why It's Better)

### Hugo - The Site Generator Thing

I'd heard about Hugo but hadn't used it in production before. Coming from traditional WordPress/PHP setups, Hugo's approach was refreshing - it takes your content (written in Markdown) and generates static HTML files at build time.

The advantages are clear: no database, no server-side processing, no security vulnerabilities to patch. Just static files served blazingly fast from a CDN. The performance difference compared to my old dynamic site was immediately noticeable.

**Learning curve**: If you're coming from a development background, Hugo feels pretty natural to pick up. The templating system makes sense once you get the hang of it, and the documentation is helpful. Setting it up on Windows took about 30 minutes including theme configuration - your experience may vary!

**Important note**: Keep track of your Hugo version from the start. You'll need it later when setting up deployment, and version mismatches will cause build failures (trust me on this one!).

### Cloudflare Pages - Free Hosting That Doesn't Suck

This is where the magic happens. Cloudflare Pages hosts static sites for free. Not "free for 3 months then we charge you" - genuinely free. I've been using it for months now and haven't paid a cent.

The best part? It's connected to GitHub, so whenever I push changes to my code, the site updates automatically. No FTP, no manual uploads, nothing. Just push and it's live.

### GitHub - Where My Code Lives

I use GitHub to store all my website files. The Git workflow is standard - commit changes, push to main, and Cloudflare automatically rebuilds and deploys the site. The GitOps approach is clean and gives you full version control over your content and configuration.

The CI/CD integration is seamless once configured properly. Just make sure your build settings match your local environment to avoid deployment failures.

## Is This Right for You? (Personal Sites vs Companies)

Before diving into the technical details, let's be clear about when this approach works well and when it doesn't.

**This setup is perfect for personal websites**, blogs, portfolios, and small projects. Here's why:

**Why it's great for personal sites:**
- Zero ongoing costs (perfect when it's just for you)
- Simple workflow once you get it set up
- Fast loading (your visitors will thank you)
- You own everything (no platform can shut you down)
- Forces you to keep things simple and focused
- Great for learning new skills

**But here's why companies shouldn't use this:**
- **No dynamic features** - no user accounts, shopping carts, forms that save to databases
- **Limited collaboration** - non-technical team members can't easily edit content
- **No built-in analytics** - you'd need to add Google Analytics separately
- **Technical barrier** - your marketing team isn't going to learn Git to update the blog
- **No admin panel** - everything happens through code and command line
- **Content approval workflows** are basically non-existent
- **No advanced SEO tools** built-in like you'd get with WordPress plugins

Basically, if you need anything more complex than "here's some text and images I want to share with the world," you'll want something else. Companies usually need CMSs that non-technical people can use, user management, forms, e-commerce, etc.

But for personal sites? This approach delivers more than you'd expect while costing absolutely nothing.

Now, let's get into how to build it.

## How I Built This Thing

### Getting Hugo Running

**Windows setup takes a few more steps**, so here's what worked for me:

1. Downloaded Hugo from their GitHub releases page
2. Extracted it to `C:\hugo\bin`
3. Added that to my Windows PATH (Google "add to PATH Windows" if you're not familiar with this)
4. Opened PowerShell and typed `hugo version` to confirm everything worked

**Write down your version number** - you'll need it for deployment later.

**Mac users have a simpler route** - just run this:
```bash
brew install hugo
```

### Creating the Site

With Hugo installed, creating a new site is straightforward:

```bash
hugo new site joraps-world
cd joraps-world
git init
```

This creates a bunch of folders. The important ones are `content/` (where your posts go) and `themes/` (how it looks).

### Picking a Theme (This Took Forever)

You know how it goes - I spent way too long browsing themes. Like, embarrassingly long. There are hundreds of them and they all look amazing in the screenshots, making it nearly impossible to choose.

After much deliberation (okay, procrastination), I went with [Hugoplate](https://github.com/zeon-studio/hugoplate) because it's modern, actively maintained, and has something that caught my eye - **Tailwind CSS 4 integration**. Most Hugo themes still use older CSS approaches or older Tailwind versions, but Hugoplate gives you the latest Tailwind CSS v4.0 right out of the box.

The Tailwind CSS 4 integration turned out to be really helpful. It meant customizing the design was much easier - no fighting with complex CSS files or learning a theme's specific styling system. Want to change a color? Just update the Tailwind classes. Need responsive design? Tailwind takes care of it.

**What else comes with Hugoplate:**
- Dark mode support out of the box
- Multi-author support
- Search functionality built-in
- Contact form integration
- SEO optimization pre-configured
- 15+ pre-designed pages (About, Contact, Blog, etc.)
- Mobile-responsive design that works well

It's basically a complete website starter kit rather than just a theme. Perfect for someone who wants a professional-looking site without spending weeks on design and configuration.

To add the theme to your site:

```bash
git submodule add https://github.com/zeon-studio/hugoplate.git themes/hugoplate
```

Then I had to edit `hugo.toml` (Hugoplate uses TOML configuration):

```toml
baseURL = 'https://jorapdotcom.pages.dev'
languageCode = 'en-us'
title = "JoRap's World"
theme = 'hugoplate'

[params]
  author = "JoRap"
  description = "My corner of the internet"
  logo = "/images/logo.png"
  logo_darkmode = "/images/logo-darkmode.png"
  # Lots more configuration options available
```

### Writing Content

This is where Markdown comes in. It's like writing a text message but with some special symbols:

- `# Big Heading`
- `## Smaller Heading`
- `**bold text**`
- `*italic text*`
- `[link text](https://example.com)`

I create new posts with:
```bash
hugo new posts/my-post-name.md
```

### Testing Everything

Before putting it live, you can run:
```bash
hugo server -D
```

This starts a local server at `http://localhost:1313` so you can see how everything looks. The `-D` flag shows draft posts too.

## Deploying to the Internet

Once you're happy with how your site looks locally, it's time to get it online.

### GitHub Setup

First, create a new repository on GitHub and push your code:

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/yoursite.com.git
git push -u origin main
```

**Pro tip**: It's easy to forget the remote origin step (happened to me twice!). Git error messages can be pretty cryptic when this happens.

### Cloudflare Pages Magic

With your code on GitHub, setting up Cloudflare Pages is surprisingly simple:

1. Sign up at pages.cloudflare.com
2. Connect it to your GitHub account
3. Select your repository
4. Set build command to `hugo` and output directory to `public`
5. Add environment variable `HUGO_VERSION` with your version number

**Important**: Make sure your Hugo version matches what you have locally, or the build will fail. This can save you from some frustrating deployment attempts!

Hit deploy and boom - live website in about 2 minutes.

## Common Problems and Solutions

Here are some common issues you might run into (and how to fix them):

### Theme Issues
**Problem**: Site looks like basic HTML instead of the theme.
**Solution**: Check your theme name in the config file. In my case, I had written `HugoPlate` instead of `hugoplate`. Theme names are case sensitive!

**Problem**: Theme not loading at all.
**Solution**: Make sure you've actually downloaded the theme files and they're in the right `themes/` folder. Also check that your `hugo.toml` theme name matches the folder name exactly.

### Build and Deployment Failures
**Problem**: Cloudflare couldn't build my site.
**Solution**: Different Hugo versions between local and Cloudflare servers. Always set the `HUGO_VERSION` environment variable in Cloudflare Pages to match your local version.

**Problem**: "Module not found" errors during build.
**Solution**: If you're using Git submodules for themes, make sure Cloudflare Pages is configured to clone submodules. Check your repository settings.

**Problem**: Build succeeds but site is broken.
**Solution**: Check your `baseURL` in `hugo.toml` - it should match your Cloudflare Pages URL exactly.

### Content and Media Issues
**Problem**: Images not loading.
**Solution**: Images go in `static/images/` and you reference them as `/images/filename.jpg` in your content. Not `static/images/filename.jpg`.

**Problem**: Links between pages broken.
**Solution**: Use relative URLs without the domain name. Hugo handles the full URL generation automatically.

### Git and GitHub Authentication
**Problem**: Can't push to GitHub (authentication failed).
**Solution**: GitHub changed how authentication works. You need to set up a personal access token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with repo permissions
3. Use the token as your password when Git asks for credentials

**Problem**: Accidentally committed large files.
**Solution**: Use `git rm --cached filename` to remove from Git without deleting locally, then add the file to `.gitignore`.

### Local Development Issues
**Problem**: `hugo server` command not found.
**Solution**: Hugo isn't in your system PATH. On Windows, make sure the Hugo executable location is added to your PATH environment variable.

**Problem**: Changes not showing up in browser.
**Solution**: Clear your browser cache, or use `hugo server --disableFastRender` to force full rebuilds.

## The Daily Workflow

When you want to write a new post, the process is pretty straightforward:

1. Create the post file:
   ```bash
   hugo new posts/post-name.md
   ```
2. Write the content in Markdown
3. Preview locally:
   ```bash
   hugo server -D
   ```
4. When you're happy with it, deploy:
   ```bash
   git add .
   git commit -m "New post about whatever"
   git push
   ```
5. Site updates automatically in ~2 minutes

This workflow feels so much smoother than the traditional CMS experience - no logging into admin panels, waiting for pages to load, or fighting with editors.

## Backup Strategy (Don't Skip This)

Here's the beautiful thing about this setup - **you get automatic backups without thinking about it**:

**What's automatically backed up:**
- All your content and code lives in GitHub (that's your primary backup)
- Every change you make is version controlled (you can revert anything)
- Cloudflare keeps copies of your built site

**What I do for extra safety:**
- Occasionally download a zip of my GitHub repo to my computer
- Keep important images in multiple places (Google Drive + GitHub)
- My markdown files are just text, so they're tiny and easy to backup

**If disaster strikes:**
- Lost computer? Clone your GitHub repo to a new machine
- Accidentally deleted something? Git history has everything
- Cloudflare goes down? Your GitHub repo can deploy to Netlify or Vercel in minutes

This is way more robust than my old WordPress setup where I constantly worried about database backups.

## What This Costs Me

**Current monthly cost: $0**

Everything I use is free:
- Hugo: Open source
- GitHub: Free for public repos (which is fine for a personal site)
- Cloudflare Pages: Free forever for personal use
- SSL certificate: Included
- Global CDN: Included

**Upgrades I already have:**
- Custom domain ($12/year)

**Setting up a custom domain** is straightforward if you want it:
1. Buy domain from any registrar (Namecheap, GoDaddy, etc.)
2. In Cloudflare Pages, go to Custom Domains and add yours
3. Update your domain's nameservers to Cloudflare's
4. Wait for DNS propagation (usually 24 hours max)

But the free `.pages.dev` subdomain looks professional enough for most personal sites.

## Why This Setup Works So Well

Compared to the old PHP setup that was slow, unreliable, and costly, this approach offers:
- Much faster loading (static files are served instantly)
- Better reliability (Cloudflare's infrastructure is solid)
- Zero ongoing costs
- Simpler update process
- More professional appearance

The main trade-off is no built-in comments system, but you can always add Disqus or similar if you need that functionality.

## If You Want to Try This

**Realistic time estimate**: 1-2 hours for initial setup and deployment. Most time will be spent on theme customization and content structure decisions.

**What you need to know**: Basic familiarity with static site generators, Git workflow, and markdown. If you're comfortable with modern development tooling, this should be straightforward.

**Potential gotchas**: Hugo version mismatches between local and deployment environments, and theme-specific configuration quirks.

## Some Helpful Resources

- [Hugo Quick Start](https://gohugo.io/getting-started/quick-start/) - start here
- [Hugo Themes](https://themes.gohugo.io) - browse these for hours like I did
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/) - learn the basics in 10 minutes
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - for when Git inevitably confuses you

## Final Thoughts

Sometimes the best solutions come from necessity. What started as a cost-cutting measure turned into discovering a setup that's actually better than what I was paying for.

If you're in a similar situation - tired of hosting costs, or just want something simple and fast - this approach is worth considering. The worst that can happen is you spend a few hours learning something new.

The developer experience has been great - clean separation of content and presentation, version control for everything, and a deployment pipeline that just works. It's the kind of setup that makes you wonder why anyone deals with traditional CMS headaches.

**Want to see the result?** You're looking at it right now. This entire site is built with the exact setup described above, and it runs for free.

Pretty cool, right?
