---
title: "Password Managers"
meta_title: "Why I Use Bitwarden (and a Password Manager at All)"
description: "I put off a password manager for years because migrating felt like a weekend I'd never get back. Bitwarden on the free plan now - one afternoon to migrate, boring ever since."
slug: "password-managers"
date: "2026-06-18T06:08:00Z"
image: "/images/feature-desktop.jpg"
categories: ["Technology", "Security", "Tips"]
author: "JoRap"
tags: ["Password Manager", "Bitwarden", "Security", "Privacy", "Two-Factor Authentication", "Credentials", "Online Safety", "Data Breach", "Passkeys", "Cybersecurity"]
related_notes:
  - local-first-software
  - commonplace-book
  - literature-notes
  - evergreen-vs-fleeting-notes
  - note-relationships
  - analog-capture-tools
level_depth: 3
featured: false
draft: true
---

I knew I should use unique passwords long before I actually did. The blocker wasn't ignorance - it was **fifty logins and no afternoon to burn**. Glad I finally burned one afternoon.

Eventually I stopped waiting for the perfect weekend and moved the important accounts first.

---

## What I actually use

**Bitwarden** on my laptop, phone, and browser. **Free plan** - enough for my own vault across devices. I didn't need family sharing or paid tiers to get started.

I picked it because it's open source, the free tier was enough to try, and I could export everything if I wanted to leave. I haven't wanted to leave.

KeePass people will tell you local-only is purer. They're not wrong. I wanted sync that didn't require me to babysit a file on Dropbox. Bitwarden won on **low friction for one person.**

1Password is polished if you're already paying for polish. LastPass had its breach moment - I wouldn't start there today.

---

## The migration afternoon

I didn't move everything at once. That way lies quitting at login number thirty.

**I did the top twenty first:** email, bank, GCash, social, the shopping sites I actually use. Generate a new random password for each. Save. Move on.

**Master password:** a long passphrase I can say out loud once and type without thinking. Not a clever string of symbols I'll forget in a month.

**2FA on the vault itself:** authenticator app on my phone. SMS is better than nothing; app is better than SMS.

The annoying part wasn't Bitwarden. It was every site that wanted email verification before it would let me change the password. Budget an afternoon. Bring snacks.

GCash wanted OTP, then email, then OTP again. Bank wanted a branch call. Social was easy. The important accounts are the slow ones - do those first while you still have patience.

---

## What broke along the way

- **Autofill fighting the browser.** Chrome wanted to save passwords too. I turned browser save off for new logins so I wasn't double-storing garbage.
- **Old me still typing the old password.** Muscle memory dies slow. The manager filling the field is the whole point - stop typing.

---

## "What if Bitwarden gets hacked?"

The vault encrypts before it leaves your machine. They'd get blobs, not your logins - **if** your master password is strong and your vault has 2FA.

That's not "don't worry about anything." That's **don't reuse passwords** and **don't pick a weak master** because you're tired.

Browser password save is better than `password123`. It's not cross-device, and I can't audit what's reused from one screen.

---

I still forget passwords sometimes - I forget which *account* I'm in, not the string. The manager handles the string. My job is one good master and not skipping 2FA because it's Tuesday.

If you've been putting off a password manager because migration sounds like a weekend project, pick one this week, move email and bank first, and stop pretending your brain is a spreadsheet.

The master password is the one string you actually have to remember. Make it long and sayable. Everything else can be random because the vault holds it - glad Bitwarden still holds mine.
