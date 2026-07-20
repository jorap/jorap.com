---
title: "Password Managers"
meta_title: "Why I Use Bitwarden (and a Password Manager at All)"
description: "I reused one password for years until a site leak scared me straight. Bitwarden on every family phone now - one afternoon to migrate, boring ever since."
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
featured: false
draft: true
---

I used the same password on half the internet for years. Not because I didn't know better - because changing fifty logins felt like a weekend I'd never get back.

Then a site I forgot I had an account on showed up in a breach email. Nothing catastrophic happened. That wasn't the point. **One leak, one password, every door** - I finally felt how dumb the shortcut was.

---

## What I actually use

**Bitwarden** on my laptop, phone, and browser. Family plan so Pia has her own vault and we share the household logins (streaming, utilities) without texting passwords in Messenger.

I picked it because it's open source, the free tier was enough to try, and I could export everything if I wanted to leave. I haven't wanted to leave.

KeePass people will tell you local-only is purer. They're not wrong. I wanted sync that didn't require me to babysit a file on Dropbox. Bitwarden won on **low friction for the whole house.**

1Password is polished if you're already paying for polish. LastPass had its breach moment - I wouldn't start there today.

---

## The migration afternoon

I didn't move everything at once. That way lies quitting at login number thirty.

**Top twenty first:** email, bank, GCash, social, the shopping sites I actually use. Generate a new random password for each. Save. Move on.

**Master password:** a long passphrase I can say out loud once and type without thinking. Not a clever string of symbols I'll forget in a month.

**2FA on the vault itself:** authenticator app on my phone. SMS is better than nothing; app is better than SMS.

**Emergency access:** Pia knows the master exists and where the recovery codes live. Morbid, useful.

The annoying part wasn't Bitwarden. It was every site that wanted email verification before it would let me change the password. Budget an afternoon. Bring snacks.

---

## What broke along the way

- **Autofill fighting the browser.** Chrome wanted to save passwords too. I turned browser save off for new logins so I wasn't double-storing garbage.
- **Shared Netflix-style logins.** Family sharing in Bitwarden fixed the "what's the password again?" thread. Worth the paid tier by itself.
- **Old me still typing the old password.** Muscle memory dies slow. The manager filling the field is the whole point - stop typing.

---

## "What if Bitwarden gets hacked?"

The vault is encrypted before it leaves your machine. They'd get blobs, not your logins - **if** your master password is strong and your vault has 2FA.

That's not "don't worry about anything." That's **don't reuse passwords** and **don't pick a weak master** because you're tired.

Browser password save is better than `password123`. It's not cross-device, not shareable with family, and I can't audit what's reused from one screen.

---

I still forget passwords sometimes - I forget which *account* I'm in, not the string. The manager handles the string. My job is one good master and not skipping 2FA because it's Tuesday.

If you're still recycling one password everywhere, pick a manager this week, migrate your email and bank first, and stop pretending your brain is a spreadsheet.
