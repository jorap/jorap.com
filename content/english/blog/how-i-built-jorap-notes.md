---
title: "How I Built JoRap Notes: My Journey from Expensive Hosting (and Better!)"
meta_title: "How I Built JoRap Notes: A Developer's Guide to Static Site Hosting"
description: "I lost my old PHP hosting (and a chunk of my work with it). A weekend of fumbling later, I landed on Hugo + GitHub + Cloudflare Pages - faster, and honestly better than what I was paying for."
slug: "how-i-built-jorap-notes"
date: 2024-06-14T05:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Website Building", "Hugo CMS", "GitHub", "Cloudflare Pages", "Static Sites", "JAMstack", "Self-Hosting", "PHP", "Migration", "Developer Life", "Hugo", "DevOps", "Site Migration", "Static Site Generator", "Web Hosting", "Publishing", "Digital Garden", "PKM", "Note Taking", "Blogging"]
related_notes:
  - digital-garden
  - drafting-in-public
  - the-garage-concept
  - selling-static-sites
  - note-relationships
featured: false
draft: false
---

> **TL;DR**: I lost my old PHP hosting and a chunk of my work with it. After a weekend of fumbling around, I landed on Hugo + GitHub + Cloudflare Pages, and the result is genuinely better than what I was paying $12/month for. Here's exactly how I did it - including the parts I messed up.

## The short backstory

For years I had a basic PHP hosting plan, about $12 a month, that I shared with a client. When that client moved on, suddenly I was paying the whole bill for what was effectively just my personal blog. It didn't make sense.

I'd been hearing about static site generators and the whole "JAMstack" thing for a while but never had a reason to try them. Losing my hosting setup turned out to be exactly that reason. Sometimes you don't fix something until you have to.

## What I ended up using

Three pieces, all working together:

- **Hugo** generates the site.
- **GitHub** stores the code.
- **Cloudflare Pages** builds and serves it.

That's it. There's no database, no admin panel, no PHP, no cron jobs. When I want to publish, I write a Markdown file, push it to GitHub, and ninety seconds later it's live.

### Hugo, in plain English

Hugo takes a folder of Markdown files and a theme, and spits out a folder of plain HTML. That's the whole job. No database to back up, no server-side code to keep patched, nothing to break.

Coming from years of WordPress, the speed difference was the first thing I noticed. Pages don't *load* - they just appear. There's nothing to wait for.

Setup on Windows took me about thirty minutes from download to first running page. On a Mac it's basically one command. Either way, **write down your Hugo version number** the moment you install it. Cloudflare needs to match it exactly later, and a mismatch is the most boring possible reason to spend an hour debugging a deploy.

### Cloudflare Pages, the part that surprised me

Cloudflare Pages hosts static sites. It connects directly to GitHub, watches the branch you tell it to, and rebuilds the site every time you push.

Months in, the setup has been rock solid. I keep waiting for the catch. I haven't found one yet.

### GitHub, the place I sometimes forget to push to

Standard Git workflow. Commit, push, deployed. The bonus is that GitHub is also my backup - every version of every post lives in the repo history, so I can revert anything I've ever written.

---

## Is this setup actually right for you?

Be honest with yourself before you start.

**This is great for** personal sites, blogs, portfolios, project pages, small documentation sites. Anything that's mostly text and images, mostly written by you, where "publishing" can reasonably mean "running a Git command."

**This is a bad fit for** anything with user accounts, shopping carts, real-time data, or a non-technical team that needs to update content without touching code. A marketing team is not going to learn Git to fix a typo. They shouldn't have to.

So: small personal stuff, yes. A company site with a non-technical team behind it, no. Pick something with an admin panel instead.

---

## Building the site, step by step

### Getting Hugo running

**On Windows**, the steps that worked for me:

1. Download Hugo from the GitHub releases page.
2. Extract it to `C:\hugo\bin`.
3. Add that folder to your Windows PATH.
4. Open PowerShell and run `hugo version` to confirm.

**On Mac**:

```bash
brew install hugo
```

Either way, note your version number. You'll thank yourself later.

### Creating the site

```bash
hugo new site joraps-world
cd joraps-world
git init
```

That creates a basic skeleton. The two folders you'll actually care about are `content/` (your posts) and `themes/` (how it looks).

### Picking a theme (where I lost a Saturday)

I will not pretend I made a quick decision here. There are hundreds of Hugo themes, they all look beautiful in their screenshots, and you can lose half a weekend "evaluating" them.

I eventually settled on [Hugoplate](https://github.com/zeon-studio/hugoplate). It's modern, well-maintained, and - the thing that sold me - it ships with **Tailwind CSS v4** baked in. Most Hugo themes are still on older CSS approaches, and I really didn't want to spend my time fighting a custom theme styling system every time I wanted to change a color.

What you get out of the box with Hugoplate:

- Dark mode
- Multi-author support
- A working search
- Contact form integration
- Pre-configured SEO
- A bunch of ready-made pages (About, Contact, Blog, etc.)
- A responsive design that actually holds up on mobile

To add it:

```bash
git submodule add https://github.com/zeon-studio/hugoplate.git themes/hugoplate
```

Then edit `hugo.toml` - Hugoplate uses TOML, not YAML:

```toml
baseURL = 'https://jorapdotcom.pages.dev'
languageCode = 'en-us'
title = "JoRap Notes"
theme = 'hugoplate'

[params]
  author = "JoRap"
  description = "My corner of the internet"
  logo = "/images/logo.png"
  logo_darkmode = "/images/logo-darkmode.png"
```

(Note the lowercase `hugoplate`. Theme names are case-sensitive. I learned this one the embarrassing way, with a perfectly broken site and "HugoPlate" sitting smugly in my config.)

### Writing content

Markdown is the whole interface:

- `# Big Heading`
- `## Smaller Heading`
- `**bold text**`
- `*italic text*`
- `[link text](https://example.com)`

To create a new post:

```bash
hugo new posts/my-post-name.md
```

### Previewing locally

```bash
hugo server -D
```

Opens at `http://localhost:1313`. The `-D` flag includes drafts.

---

## Putting it on the internet

### Push to GitHub

Create a new repo, then:

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/yoursite.com.git
git push -u origin main
```

I have forgotten the `git remote add origin` step more times than I'd like to admit. Git's error messages when this happens are not, let's say, beginner-friendly.

### Hook up Cloudflare Pages

1. Sign up at `pages.cloudflare.com`.
2. Connect your GitHub account.
3. Select the repo.
4. Set the build command to `hugo` and the output directory to `public`.
5. Add an environment variable `HUGO_VERSION` and set it to your exact local Hugo version.

Hit deploy. About two minutes later, your site is live at some `something.pages.dev` URL.

---

## The things that broke (and how I fixed them)

This is the section I needed when I was starting out, so it's the longest one here.

**Site looks like raw HTML.** The theme isn't loading. Nine times out of ten, the theme name in `hugo.toml` doesn't match the folder name exactly - case included.

**Cloudflare build fails.** Almost always a Hugo version mismatch. Set `HUGO_VERSION` to whatever `hugo version` prints locally.

**"Module not found" during the build.** Cloudflare Pages isn't pulling Git submodules. Turn submodule cloning on in the Pages project settings.

**Site deploys but every link is broken.** Check `baseURL` in `hugo.toml`. It needs to match the actual URL Cloudflare gave you.

**Images won't show up.** Put them in `static/images/` and reference them in your Markdown as `/images/filename.jpg`. Not `static/images/...` - Hugo handles that.

**Can't push to GitHub.** GitHub no longer accepts passwords. You need a personal access token: Settings → Developer settings → Personal access tokens. Use the token as the password when Git prompts you.

**`hugo server` says command not found.** Hugo isn't on your PATH. On Windows, add the `hugo.exe` folder to the PATH environment variable and restart your terminal.

**Changes don't show up in the browser.** Cache. Hard refresh, or run `hugo server --disableFastRender`.

---

## The day-to-day workflow

Once everything is set up, posting feels almost too simple:

```bash
hugo new posts/post-name.md
# write the post in Markdown
hugo server -D            # preview it
git add .
git commit -m "New post about whatever"
git push
```

About two minutes after the push, the site updates. No logging in, no clicking "Publish," no waiting for the WordPress dashboard to load. It's the part I missed most about old-school static publishing and didn't realize until I had it again.

---

## Backups (you don't really have to think about it)

This is the quiet superpower of the whole setup:

- Everything I write lives in GitHub. That's already a backup.
- Every change is in Git history. I can roll anything back.
- Cloudflare keeps a copy of every build.

I also occasionally download a zip of the repo just to be doubly safe, and I keep my images on Google Drive as well. But honestly, with everything in Git, I worry about backups way less than I did when I was managing a WordPress database.

If my computer died tomorrow, I could clone the repo to a new machine and be writing again in five minutes.

---

## What it costs me

No monthly hosting bill — a big change from the old $12/month PHP plan.

The only thing I actually pay for is a custom domain, about $12 a year from my registrar. Hugo, GitHub, and Cloudflare Pages handle the rest, with SSL and a global CDN included.

If you want your own domain, point it at Cloudflare from your registrar (Namecheap, GoDaddy, etc.), add it under Custom Domains in Cloudflare Pages, and wait for DNS to settle. Usually within a day.

The `*.pages.dev` URL works fine if you skip the custom domain.

---

## Why I'm sticking with it

Compared to the old PHP setup, this one is faster, more reliable, and simpler to update. The only thing I traded away is a built-in comments system, and I don't really miss it. If I ever wanted comments back, Disqus or a small Worker would do the job.

If you have the patience for an evening of setup, I genuinely think this beats most paid hosting for personal use. The first time you push a typo fix and see it live a minute later, you'll get it.

You're reading the result right now. The whole thing - every page, every post, every image - is built and served exactly the way I described above.

## A couple of useful links

- [Hugo Quick Start](https://gohugo.io/getting-started/quick-start/) - start here
- [Hugo Themes](https://themes.gohugo.io) - yes, you'll lose hours
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/) - ten minutes and you know it
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - for when Git gets weird
