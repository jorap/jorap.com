---
title: "Modified ATK Recipe Style Guide Rules"
meta_title: "Modified ATK Recipe Rules - How I Write Recipes for AI and Humans"
description: "I borrowed America's Test Kitchen's recipe discipline and changed the parts that fight a personal blog. My modified rules keep AI drafts consistent without turning adobo into a textbook."
slug: "modified-atk-recipe-style-guide-rules"
date: "2026-07-30T01:30:00Z"
image: "/images/Chicken-Adobo.jpg"
categories: ["Food", "Writing", "AI"]
author: "JoRap"
tags: ["Recipe Writing", "Style Guide", "America's Test Kitchen", "AI", "Filipino Recipes", "Instant Pot", "Food Blog", "Writing Tips"]
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

ATK recipes are boring on purpose. That's a compliment - and earned.

What I love is the precision underneath. They don't publish on the first good batch. Test cooks run versions in the kitchen, staff taste and argue, and ATK fans cook drafts at home before a recipe hits the magazine or the site. The flat tone is what you get when a dish has already survived people who will tell you the chicken is dry.

That discipline shows up on the page: **repeatability** - same words, same order, same cues, so a home cook in Boston and a home cook in Batangas hit the same result if they follow the steps. Imperative verbs. Times and temperatures in the step where they matter. Visual doneness cues when a clock lies. Equipment named when size changes the outcome.

I don't run a test kitchen. I cook for my family on weeknights, mostly in an **8-quart Instant Pot**, mostly Filipino comfort food. But I still want the **method** to read like one author wrote every recipe on the site - not like a new food blogger every Tuesday.

The ATK frame gave me that spine. I just had to loosen the collar for a personal site and for AI.

---

## What I kept from ATK

These survive unchanged in my doc:

1. **Imperative steps.** "Brown chicken skin-side down" - not "you should brown" or "the chicken is browned."
2. **One action per sentence** when the action is fussy. Don't bury "flip" and "add vinegar" in the same line if timing matters.
3. **Times and heat in the step.** "High pressure 10 minutes" lives in Step 4, not a vague intro.
4. **Visual cues alongside clocks.** "Until sauce coats the back of a spoon" still shows up even when I give eight minutes.
5. **Ingredient list separate from method.** Amounts live in the ingredients block; steps repeat them on add lines only (see below).
6. **Yield stated plainly.** "Feeds 4-6 with leftovers" beats silence.
7. **Equipment when it changes the result.** "8-quart Instant Pot" and "separate skillet for browning" are not optional color - they're how I stopped burn notices.

That's the ATK part my brain already agreed with before I wrote anything down.

---

## What I modified (and why)

### Articles in steps - keep them

ATK drops "the" and "a" to save magazine pages. Online space is cheap. My steps use normal English: "Transfer **the** browned chicken to **the** Instant Pot." Reads aloud better. AI defaults to articles anyway; fighting that was wasted editing.

### Metric first, volume second

I write **milliliters and grams first**, then the measuring cup or spoon I'd actually grab: `160 ml soy sauce, about 2/3 cup`. Philippines kitchen, US-published cookbooks, one post. The metric number is the source of truth; the volume is the practical shortcut.

Same format on **add lines** in the method - when soy sauce actually hits the pot, the step says `160 ml soy sauce (about 2/3 cup)`, not "soy sauce from above."

For tiny amounts (peppercorns, xanthan gum), I give spoons **and** grams when I've weighed them. Salt in a braise gets leeway. Baking soda does not.

Fractions stay as digits with a slash (`1/2` not `½`) so AI and copy-paste don't fight Unicode.

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

### Repeat amounts on add lines only

ATK magazine steps assume you're glancing at a printed ingredient list beside you. On a phone, scrolling up from step 3 to find "how much soy again?" is how I skip a clove of garlic.

So when a step **adds** something to the pot, pan, or bowl, it spells the same amounts as the ingredients list - metric first, volume in parentheses. Prep steps don't repeat ("mince the ginger"). Transfer steps don't repeat ("transfer the browned chicken"). Reserve steps don't repeat ("add the reserved marinade"). Something already combined earlier stays combined - you don't re-list every item in the marinade when you pour it in.

Still no scroll-up shorthand on add lines: not "from the list above," not "as listed," not a bare ingredient name when you're measuring into the pot.

Bad add line: `Combine the marinade from the list above (soy sauce, garlic, peppercorns, bay leaves).`

Good add line: `Combine 160 ml soy sauce (about 2/3 cup), 10-11 cloves crushed garlic, 1 1/3 tsp whole black peppercorns, and 4 dried bay leaves. Add 2 kg bone-in, skin-on chicken thighs and coat thoroughly.`

Good transfer line: `Transfer the browned chicken to the Instant Pot. Add the reserved marinade, 160 ml water (about 2/3 cup), and 105-110 ml vinegar (about 7 tbsp) last.`

That's the biggest shape change since I first wrote this sheet. ATK's "don't repeat" rule made sense on paper. On a phone in the kitchen, repeat on add lines wins.

---

## Voice split (where JoRap ends and ATK begins)

| Zone | Voice |
|------|--------|
| Opening, section intros, close | JoRap - failures, what I'd skip, dry asides |
| Ingredients + numbered steps | ATK-scannable - imperative, no jokes, no "delicious" |

I polish the opening and close in my normal blog voice, but I don't roughen the steps. Food-blog filler ("This delicious recipe will tantalize your taste buds") dies in the intro, not in step 4. The method stays boring on purpose.

---

## The rules doc I paste for AI

This post is the rationale; the block below is what I paste at the top of a recipe chat. Same idea as the WordPress rules doc in [Consistent AI output for WordPress builds](/blog/consistent-ai-output-wordpress-builds/) - context the model sees before it types.

Before I publish, I still read the intro and close aloud and fact-check liquid ratios against what I actually cooked. Models invent confident numbers. The doc cuts **shape** drift, not kitchen QA.

```
RECIPE STYLE (modified ATK - JoRap blog)

STRUCTURE
- Header metadata: title, description, slug, categories include Food + Recipes when applicable
- Opening: personal hook (why I cook this, what failed before) - first person, 2-4 short paragraphs
- Section intros: human voice; steps: instructional only
- Ingredients grouped (Protein / Marinade / Liquids / Optional)
- Method: numbered steps under ## How I run it (or equivalent personality H2)
- Close: what I actually serve with, what I'd cook again - no "hope you enjoy"

INGREDIENTS
- Metric first, practical volume in parentheses (160 ml, about 2/3 cup)
- Fractions as digits with slash (1/2 not ½)
- Filipino/local names OK with one plain-English gloss
- Optional items labeled Optional in the heading

STEPS
- Imperative mood, present tense
- Articles OK (the, a)
- One critical action per sentence when timing matters
- Amounts on add lines match ingredients: metric first, practical volume in parentheses (160 ml, about 2/3 cup)
- Repeat amounts only when adding to the pot, pan, or bowl - not prep, reserve, or transfer steps
- No "from the list above" on add lines
- Times, pressure level, and heat in the step they apply to
- Name equipment when size or type changes outcome (8-quart Instant Pot, separate skillet)
- No "you should" / "it is recommended"

VOICE SPLIT
- Intro + section headers: JoRap voice (specific failures, what I'd skip, dry asides)
- Steps: ATK-scannable - no jokes, no "delicious", no restating the heading

FACTS
- Match my existing recipe posts for Instant Pot liquid ratios unless I've tested new numbers
- No dollar or peso amounts
- Don't invent gear or brand picks I haven't actually used

OUTPUT
- Markdown only, with title and description metadata at top
```

---

## How this changed my last adobo pass

Before the doc, an AI draft gave me vinegar in the marinade, "stir well" in step 3, and "combine the marinade from the list above" on the add line. That's not how I cook adobo - vinegar goes in last, unstirred for two minutes, or the pot tastes sharp the whole pressure cook. And I shouldn't have to scroll up to find how much soy sauce I'm pouring.

After the doc, the skeleton matched [Instant Pot chicken adobo](/blog/instant-pot-chicken-adobo/): marinade without vinegar, brown in a separate pan, liquid totals tuned for an 8-quart, sweetener optional at reduction, amounts spelled out on every add line. I only edited voice in the intro and one timing note I'd updated since publish.

That's the win. Not prettier adjectives. **Same recipe twice.**

---

I keep three recipe posts live that follow this sheet: [chicken adobo](/blog/instant-pot-chicken-adobo/), [arroz caldo (Instant Pot)](/blog/instant-pot-arroz-caldo/), and the older [rice cooker arroz caldo](/blog/set-it-forget-it-arroz-caldo/) I don't cook anymore but won't delete. Match those for shape and Instant Pot ratios unless I've tested new numbers. New recipes get the rules doc first, a human pass second, a fact-check third. Same pot, same voice, same step shape - that's the whole point.
