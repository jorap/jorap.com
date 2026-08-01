---
title: "The Optimized Mindset I Got From Applied Math (Operations Research)"
meta_title: "Applied Math and OR - The Mindset That Stuck"
description: "I picked Applied Math with an OR track partly to dodge the CS quota. Twenty years later, the useful part isn't the formulas - it's how I frame constraints."
slug: "optimized-mindset-applied-math-or"
date: "2026-07-30T00:00:00Z"
image: "/images/note.jpg"
categories: ["Education", "Opinion", "Developer Life"]
author: "JoRap"
tags: ["Applied Mathematics", "Operations Research", "UP Los Baños", "Computer Science", "Education", "Decision Making", "Career", "Mindset", "Constraints", "Tradeoffs"]
related_notes:
  - there-is-no-perfect-solution
  - reversibility
  - minimum-effective-dose
  - low-hanging-fruit
level_depth: 4
featured: false
draft: true
---

I'll say the quiet part out loud: I didn't walk into **Applied Mathematics** at UP Los Baños because I had a burning love for Operations Research.

I wanted **Computer Science**. CS was the crowded door - quota, long waitlists, the program everyone in my batch was aiming at. Applied Math with an **Operations Research** track was the side entrance. Still math-heavy. Still quantitative. Fewer people fighting for the same slot.

That was the strategy. Not a life mission. A move on a crowded board.

I was good at math in high school. I liked puzzles. I could picture myself building software. What I couldn't picture was sitting on a waitlist for two years while my blockmates posted about which CS professor was brutal this semester. Applied Math let me enroll, stay on campus, and keep the CS diploma on the horizon without pretending I'd always dreamed of inventory models.

I finished the BS in 2001, picked up a **Graduate Diploma in Computer Science** in 2003, and eventually left teaching for web work. The diploma is what employers read on paper. The OR track is what still runs in the background when I'm picking a stack, planning a week, or arguing with myself about whether a problem needs a clever model or a blunt fix.

---

## What Operations Research actually taught me

OR sounds like a factory word. It isn't only factories.

At its core, OR is **decision math under limits**. You have an objective (cheaper, faster, fewer errors). You have constraints (budget, time, people, laws, physics, your kid's attention span). You look for the best move you can actually take, not the best move in a world with infinite money and no sleep.

Linear programming was the poster child. Maximize profit subject to labor hours and raw materials. Minimize shipping cost subject to delivery windows. Draw the feasible region. Find the corner that wins.

I still remember the first time a professor drew the feasible region on the board and said the optimum had to live on a corner. That felt unfair and then inevitable - like someone had snuck a rule into the universe. You could stare at the interior all day. The answer was on the edge.

We did simplex by hand long enough to respect the algorithm, then let the machine do the grinding. That's where the Fortran came in.

Queuing theory was the humbling one. Add one server, watch the line shrink - until demand shifts and you're back in the same lecture hall wondering why the model lied. Inventory models did the same trick with spreadsheets: elegant on paper, sensitive to the assumptions you smuggled in without noticing. Change the holding cost by ten percent and your "optimal" reorder point jumps like you cheated.

There was programming in the mix too - **Fortran**, which in 1999 was already programming history with a grade attached. Not because anyone thought we'd ship production code in it. The numerical courses needed something that could chew through a problem set without hand-simulating every pivot. I wrote my share of `.f` files in the lab, debugged off-by-one loops at midnight, turned them in, and filed the experience under "applied means applied, not romantic."

Network flows, transportation problems, little factory stories on exams - the coursework loved a plant that made widgets in Manila and shipped them to Cebu. I never visited that plant. I did visit the idea that every story problem hides a graph if you squint.

None of that made me a career OR analyst. I don't spend Tuesdays tuning simplex tables. What stuck was the **shape of the thinking**:

- Name the goal before you optimize anything.
- List the real constraints, including the ones that sound petty.
- Separate "impossible" from "expensive" from "annoying."
- Check whether a small change in inputs flips the answer.

That's the optimized mindset, for me. Not "always find the global maximum." More like **don't waste cleverness on the wrong problem**.

---

## The dodge worked - and not how I expected

The CS quota dodge paid off on paper. I got the diploma. I taught for a while - math and computer subjects, the kind of job where you learn to explain the same idea five ways because the fifth face in the row still looks lost. Teaching paid the bills and kept me near computers without a corporate badge.

The web shift didn't arrive as a revelation. It arrived as **XOOPS**.

The first CMS I actually liked gave me theme control that WordPress and Joomla didn't hand a tinkerer easily. I could bend layouts without feeling like I was breaking someone else's guardrails. Knowing XOOPS well enough to ship real sites helped me **land a job** that moved me from teacher toward web developer for real. Open source wasn't philosophy yet. It was the only stack I could afford to break on my own machine.

From there the path looks obvious in hindsight. Someone taught me **ASP**. I went hunting for ASP-built software, found mostly proprietary locks, and drifted toward **PHP** and **XAMPP** - especially the portable build you could run on locked-down lab PCs. I burned Linux CDs at an IT training company where I was the resident evangelist. **MEPIS**, **Ubuntu**, **Red Hat** before Fedora was the name. DistroWatch was my sport.

What I didn't expect was how often OR framing beats raw coding speed once you're actually shipping.

**Drupal vs WordPress** wasn't a purity contest. I compared Joomla, WordPress, and Drupal on real small sites after XOOPS had already shown me what theme control could feel like. Drupal won on architecture in my notebook. WordPress won in my bank account. Job listings in my market, client budgets, how fast I could ship a theme without fighting the CMS - **paid work exists** beat elegant routing every time. I still remember **WordCamp Asia in Manila**, roughly fourteen hundred people in a ballroom, Matt Mullenweg telling old Philippines WordCamp stories like folklore. I wasn't there to worship a platform. I was there because the feasible region had shifted.

**Hugo over WordPress** for my own site was the same move in reverse, years later. Objective: cheap hosting, fast builds, fewer moving parts. Constraint: I still need flashcards, graph view, and a notes garden in one repo. The "optimal" personal stack isn't the one with the most features. It's the one I'll actually maintain on **one to two hours a month**. A git push goes live in about ninety seconds. I pin `HUGO_VERSION` because mismatch is the most boring deploy failure on earth. Case-sensitive theme folder names taught me that the embarrassing way.

Even the open-source story fits. Free software got me in the door. Freedom kept me when corporate images blocked installers. That's not ideology. That's **feasible region** thinking with a student budget - the same move as picking portable XAMPP because the lab wouldn't let you install anything permanent.

---

## Where the mindset shows up outside work

Parenting made OR less abstract.

My son Davis says math is **hard**. Kumon reading won over Kumon math in our house. I could have outsourced the subject I'm strongest in. I did a Kumon math trial years ago myself - my answers were right; the feedback was **you could do it faster**. I didn't want that voice in his head at six.

So home runs **tablet quiz games** on the site's randomizer (`grade-1-quiz`, `grade-1-math-quiz`), then one optional printed line. Handwriting practice includes **postcards to lola**. Minimum effective dose, not maximum worksheet throughput.

That's OR with feelings as a constraint. Objective: he stops treating numbers like punishment. Constraint: six years old, short attention, reading already feels like winning. The "optimal" curriculum on a brochure isn't optimal if it kills the subject for a decade. I'd rather he meet math through a game he can close than a franchise clock he learns to dread.

Same with screen rules. He has a **dedicated kids phone** in kids mode - kitchen charger, not his room - because I learned the hard way what happens when a six-year-old finds Messenger on an unlocked handset. The constraint isn't "zero screens." It's **no surprises on my daily driver**.

My own habits get the same treatment. Writing happens after breakfast when the Hugo folder is open. Phone rules are kitchen charger, grayscale after nine, logged-out feeds. I'm not optimizing for perfect health or perfect focus. I'm optimizing for **defaults I can keep** when commute season hits and sleep gets thin. Supplement stack bookmarked. McGill Big Three bookmarked too - which tells you how often "optimal on paper" survives contact with a tired Tuesday.

---

## When the model is wrong

The mindset has a failure mode. I know it because I live in it.

Not every decision is a linear program. Some problems don't have a clean objective function. "Maximize career growth" falls apart the week your kid is sick and the client wants a quote in ten minutes. Relationships, faith, grief - you can't reduce those to constraints without lying to yourself. Our family story has a testimony shape to it. That didn't fit any spreadsheet I learned in college, and pretending it would have made me worse at both math and prayer.

OR also trained a bad habit: **treating people like variables**. Headcount isn't a continuous decision variable. Your spouse's patience isn't a slack constraint you get to spend down because the spreadsheet says the project is feasible. Pia sang on a studio vocal for a church recording during COVID. I could model studio time. I couldn't model what it cost her to walk into a room and sing anyway.

And models lie when you lie to them. I skipped sleep to "save time" plenty of years. The queue didn't shrink. The error rate climbed. The fix wasn't a better algorithm. It was closing the laptop.

There's a softer failure mode too: **analysis as procrastination**. I've spent a week comparing tools when the real constraint was "ship the ugly version Friday." Waiting for the perfect solution is itself a choice - usually the choice to keep the mess you already have. OR gave me language for tradeoffs. It didn't automatically cure the urge to research my way out of starting.

The useful carryover isn't worship of optimization. It's **respect for tradeoffs** - and the humility to rerun the problem when the inputs change.

---

## What I'd tell someone picking a major today

If you're staring at quota lists and side doors like I was, here's the honest version.

**Pick the door you can walk through that keeps the next door open.** Applied Math wasn't my dream label. It was a feasible move toward CS and toward work that used my head. The OR track gave me language for decisions I was already making badly - stack picks, client quotes, whether to push back on a deadline.

You don't need to love every course. Fortran at midnight will not be the highlight reel. You need a few ideas that still fire twenty years later. For me, those ideas were: **state the goal, name the limits, pick a move you can live with, revisit when reality shifts.**

If you're already in a major that feels like a compromise, mine it for transferable shape. The widget factory on the exam might be fiction. The habit of asking "what are we maximizing, and what's actually fixed?" is not.

The CS quota was the push. The mindset was the pull I didn't know I was buying.
