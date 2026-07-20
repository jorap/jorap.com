---
title: "Sveltia CMS"
meta_title: "Sveltia CMS - When the Client Won't Touch Git"
description: "I publish via Markdown and git push. Sveltia CMS is the bridge when someone needs buttons - edits still commit to the repo, build pipeline unchanged."
slug: "sveltia-cms"
date: "2026-06-19T06:00:00Z"
image: "/images/static-vs-cms.jpg"
categories: ["Website", "Technology", "Tutorial"]
author: "JoRap"
tags: ["Sveltia CMS", "Hugo", "CMS", "Git", "Static Sites", "Content Management"]
related_notes:
  - git-based-cms
featured: false
draft: true
---

**Sveltia CMS** is a lightweight, Git-backed editor for static sites. Svelte UI in the browser. Changes commit to your repo. Hugo still builds on push.

I don't draft my own posts in Sveltia - I write Markdown in the editor and push. The site does ship a `/admin/` panel backed by Sveltia for when buttons beat Git lessons. I keep it in the toolbox for **clients who won't open VS Code** but still fit a static stack.

---

## The pass-off problem it solves

[Client site pass-off](/blog/client-site-pass-off/) is where static projects live or die. Option one: Git lesson - works for some neighbors, fails for others. Option four: git-based CMS - buttons for people who need buttons.

Picture someone who needs sermon archives or brochure typo fixes without learning YAML. "Just edit the file and commit" wasn't going to happen. WordPress felt like overhead for twice-a-month updates.

Sveltia (and tools like it) sit in the gap: **static hosting economics, CMS-shaped editing.**

---

## Git stays source of truth

The CMS doesn't replace the repo. It commits Markdown (and media) like you would - with auth, forms, and guardrails.

Cloudflare Pages still builds on push. No database appears. No PHP cron. The architecture stays static; only the **entry point** changes.

That matters when I quote hosting lean. I'm not sneaking WordPress in through the back door.

---

## What setup actually involves

Not a one-click toy. You configure:

- Which repo and branch
- Auth (often GitHub OAuth or similar)
- Media folder paths
- Collection schemas so editors see fields, not raw frontmatter

Treat it like a small production app. Staging branch first. Test commit, test build, then hand keys to the client.

I haven't rolled it out on every static job. When the fit is right, it's cheaper than re-platforming to WordPress for a four-page site.

---

## When I skip it

Solo blogger. Developer who already lives in Git. Client who happily emails copy for retainer batches.

Also skip when the job needs real CMS features - member areas, ecommerce, complex workflows. [Static vs CMS](/blog/static-site-vs-cms/) still applies. Sveltia doesn't make Hugo into WordPress.


Sveltia CMS solves the **Hugo accessibility gap** for non-technical editors.

You might not need it. Your collaborator might. Know it exists before defaulting to WordPress again - or before forcing Git on someone who'll never use it.

I'd rather configure a git CMS once than rebuild the same brochure on a LAMP stack because pass-off failed.
