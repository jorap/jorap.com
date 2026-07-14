---
title: "Hugo Page Bundles"
meta_title: "Hugo Page Bundles - When I Stop Dumping Images in /static"
description: "Most posts are a single .md with a hero in /images. Page bundles are for messier ones - screenshots, downloads, assets that belong to one post."
slug: "hugo-page-bundles"
date: "2026-06-19T06:00:00Z"
image: "/images/image-template.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Hugo", "Page Bundles", "Content Management", "Static Sites", "Markdown", "Assets", "PKM", "Static Site Generator"]
related_notes:
  - future-proofing-knowledge
  - the-garage-concept
  - digital-garden
  - git-based-cms
  - free-tier-hosting-stack
  - selling-static-sites
featured: false
draft: true
---

Most of my blog posts are a flat file: `extension-cord.md`, hero image in `/images/extension-cord.jpg`, done. That works until you publish something with six screenshots, a PDF handout, and a diagram that only makes sense next to that one post.

Then you start naming things `fb-desktop-feed-v2-final.jpg` in a shared folder and hate yourself.

A **Hugo page bundle** fixes that. It's a folder with `index.md` plus sibling files - images, downloads, whatever ships with that page. The post owns its assets. Delete the folder, delete the clutter.

---

## The mess that pushed me toward bundles

My [Facebook Favorites post](/blog/facebook-favorites-feed/) has two walkthrough screenshots - `fb-desktop-feed.jpg` and `fb-mobile-feed.jpg` - referenced from the post but still sitting as loose image files, not colocated in a bundle folder. Fine for two files. Annoying when I'm drafting three posts at once and every new screenshot lands in the same shared pile.

I didn't bundle that post when I added the captures. Single-file habit won. The next client migration probably won't get that pass - church bulletin PDFs beside the announcement page, before/after shots for a portfolio case study. Stuff you **never** want in a site-wide image dump.

That's the trigger: **more than one custom asset, or an asset that shouldn't outlive the post.**

---

## Folder structure (leaf bundle)

```
content/english/blog/my-post/
  index.md
  hero.jpg
  step-2-settings.png
  handout.pdf
```

In `index.md`, reference with relative paths:

```markdown
![Settings screen](step-2-settings.png)
```

No `/images/` guessing. No "which draft used `screenshot3.png`?" six months later.

**Leaf bundle** = one published page per folder. That's what I reach for first.

---

## Branch vs headless (the ones I rarely need)

**Branch bundle:** a section folder with `index.md` plus child pages. Useful for a tutorial series that shares a landing page. I don't use this much on JoRap - the blog is flat posts.

**Headless bundle:** resources without their own URL - image sets for shortcodes, shared partials. Niche. Hugoplate doesn't push you here on day one.

If you're blogging, assume **leaf bundle** until you have a reason not to.

---

## When I still use a plain `.md` file

Single hero image in `/images/`. No attachments. Post fits the pattern 80% of my archive already uses.

Bundles add a folder to navigate in the editor. Worth it when colocation saves confusion. Not worth it for "one jpeg and 800 words."

---

## Bottom line

Page bundles are **colocate what ships together.** I haven't moved the whole blog over - most posts are still one file. The next post with a pile of screenshots won't be.

When you migrate an old post, bundle it then. Moving six loose images into a folder takes ten minutes. Hunting them across `/static` in a year takes longer.
