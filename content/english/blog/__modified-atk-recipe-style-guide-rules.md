---
title: "Modified ATK Recipe Style Guide Rules"
meta_title: "Modified ATK Recipe Rules - How I Write Recipes for AI and Humans"
description: "I borrowed America's Test Kitchen's recipe discipline and changed the parts that fight a personal blog. My modified rules keep AI drafts consistent without turning adobo into a textbook."
slug: "modified-atk-recipe-style-guide-rules"
date: "2026-07-30T01:30:00Z"
image: "/images/Chicken-Adobo.jpg"
categories: ["Food", "Writing", "AI"]
author: "JoRap"
tags: ["Recipe Writing", "Style Guide", "America's Test Kitchen", "AI", "Filipino Recipes", "Instant Pot", "Cursor", "Food Blog", "Writing Tips"]
related_notes:
  - standard-operating-procedures
  - habit-formation
  - intellectual-sourcing
featured: false
draft: true
---

Ask AI to format a recipe on Monday and Wednesday and you'll get two different shapes. Different heading levels. Vinegar in the marinade on one draft, "add later" on the other. Both readable. Neither matches what I actually cook.

I fixed that the same way I fixed WordPress build drift: **a short rules doc the model reads before it types.** For recipes, I started from America's Test Kitchen's house style - the one test cooks and editors argue about for eleven years until it sounds normal - then cut the parts that only make sense on a magazine page.

---

## Why ATK at all

ATK recipes are boring on purpose. That's a compliment.

The test kitchen cares about **repeatability**: same words, same order, same cues, so a home cook in Boston and a home cook in Batangas hit the same result if they follow the steps. Imperative verbs. Times and temperatures in the step where they matter. Visual doneness cues when a clock lies. Equipment named when size changes the outcome.

I don't run a test kitchen. I cook for my family on weeknights, mostly in an **8-quart Instant Pot**, mostly Filipino comfort food. But I still want the **method** to read like one author wrote every recipe on the site - not like a new food blogger every Tuesday.

The ATK frame gave me that spine. I just had to loosen the collar for a personal site and for AI.

---

## What I kept from ATK

These survive unchanged in my doc:

1. **Imperative steps.** "Brown chicken skin-side down" - not "you should brown" or "the chicken is browned."
2. **One action per sentence** when the action is fussy. Don't bury "flip" and "add vinegar" in the same line if timing matters.
3. **Times and heat in the step.** "High pressure 10 minutes" lives in Step 4, not a vague intro.
4. **Visual cues alongside clocks.** "Until sauce coats the back of a spoon" still shows up even when I give eight minutes.
5. **Ingredient list separate from method.** Amounts in the list; no re-measuring mid-paragraph unless it's a split add (vinegar later, sweetener at the end).
6. **Yield stated plainly.** "Feeds 4-6 with leftovers" beats silence.
7. **Equipment when it changes the result.** "8-quart Instant Pot" and "separate skillet for browning" are not optional color - they're how I stopped burn notices.

That's the ATK part my brain already agreed with before I wrote anything down.

---

## What I modified (and why)

### Articles in steps - keep them

ATK drops "the" and "a" to save magazine pages. Online space is cheap. My steps use normal English: "Transfer **the** browned chicken to **the** Instant Pot." Reads aloud better. AI defaults to articles anyway; fighting that was wasted editing.

### Metric first, volume second

I write **milliliters and grams first**, then the measuring cup or spoon I'd actually grab: `160 ml soy sauce, about ⅔ cup`. Philippines kitchen, US-published cookbooks, one post. The metric number is the source of truth; the volume is the practical shortcut.

For tiny amounts (peppercorns, xanthan gum), I give spoons **and** grams when I've weighed them. Salt in a braise gets leeway. Baking soda does not.

### "Why" lives outside the steps

ATK uses a tight "Why This Recipe Works" headnote. I split it:

- **Section intro** in my voice - the burn notice story, the supermarket that stopped stocking boneless thighs, the rice cooker I don't use anymore.
- **Steps stay scannable** - no memoir between "seal the lid" and "natural release 10 minutes."

AI loves blending story into step 3. The rule says: story above the `## How I run it` heading, not inside it.

### Local names stay

Patis, malagkit, kalamansi, cane vinegar - the word I'd say in the kitchen, with a plain English gloss once if it's not obvious. I don't swap everything to "fish sauce" just to sound generic.

### Optional means optional

Sweetener, xanthan gum, pan-crisp at the end - labeled **Optional** in the ingredient list and called out again in the step. ATK would fold or cut; I keep them because my family actually uses them.

### Failures belong in the intro, not the steps

"Don't brown in the Instant Pot" is a hard rule in my adobo because I earned it. It goes in the section intro or a short callout, not as a four-sentence detour in Step 2.

---

## The rules doc I paste for AI

This is the block in my Cursor project next to the jorap-voice skill. Same idea as the WordPress rules doc in [Consistent AI output for WordPress builds](/blog/consistent-ai-output-wordpress-builds/) - context the model sees every recipe session.

```
RECIPE STYLE (modified ATK - JoRap blog)

STRUCTURE
- Frontmatter: title, description, slug, categories include Food + Recipes when applicable
- Opening: personal hook (why I cook this, what failed before) - first person, 2-4 short paragraphs
- Section intros: human voice; steps: instructional only
- Ingredients grouped (Protein / Marinade / Liquids / Optional)
- Method: numbered steps under ## How I run it (or equivalent personality H2)
- Close: what I actually serve with, what I'd cook again - no "hope you enjoy"

INGREDIENTS
- Metric first, practical volume in parentheses (160 ml, about ⅔ cup)
- Spell out fractions (½ not 1/2 in prose lists)
- Filipino/local names OK with one plain-English gloss
- Optional items labeled Optional in the heading

STEPS
- Imperative mood, present tense
- Articles OK (the, a)
- One critical action per sentence when timing matters
- Times, pressure level, and heat in the step they apply to
- Name equipment when size or type changes outcome (8-quart Instant Pot, separate skillet)
- No "you should" / "it is recommended"

VOICE SPLIT
- Intro + section headers: JoRap voice (specific failures, what I'd skip, dry asides)
- Steps: ATK-scannable - no jokes, no "delicious", no restating the heading

FACTS
- Match existing JoRap recipe posts for Instant Pot liquid ratios unless the user gives new tested numbers
- No dollar or peso amounts
- Don't invent brand preferences not in author context

OUTPUT
- Markdown only, Hugo frontmatter at top
- draft: true unless user says publish
```

I still read every draft. Models invent confident liquid ratios. The doc cuts **shape** drift, not factual QA.

---

## How this changed my last adobo pass

Before the doc, a Cursor session gave me vinegar in the marinade and "stir well" in step 3. That's not how I cook adobo - vinegar goes in last, unstirred for two minutes, or the pot tastes sharp the whole pressure cook.

After the doc, the skeleton matched [Instant Pot chicken adobo](/blog/instant-pot-chicken-adobo/): marinade without vinegar, brown in a separate pan, liquid totals tuned for an 8-quart, sweetener optional at reduction. I only edited voice in the intro and one timing note I'd updated since publish.

That's the win. Not prettier adjectives. **Same recipe twice.**

---

## When I break my own rules

Holiday baking with Pia's family - I still weigh flour and follow ATK-no-articles in my head because that's how the borrowed cookbook reads. A guest post for someone else's site would follow their guide, not mine.

For jorap.com food posts, this modified ATK sheet is the default. If a rule fights a tested result, the result wins and the doc gets a footnote. Style guides serve the food, not the other way around.

---

I keep three recipe posts live that follow this sheet: [chicken adobo](/blog/instant-pot-chicken-adobo/), [arroz caldo (Instant Pot)](/blog/instant-pot-arroz-caldo/), and the older [rice cooker arroz caldo](/blog/set-it-forget-it-arroz-caldo/) I don't cook anymore but won't delete. New recipes get the rules doc first, a human pass second, lint third. Same pot, same voice, same step shape - that's the whole point.
