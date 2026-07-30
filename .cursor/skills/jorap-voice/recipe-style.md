# Recipe style (modified ATK)

JoRap food posts borrow America's Test Kitchen discipline for repeatability, then loosen what only makes sense on a magazine page. Full rationale: `content/english/blog/__modified-atk-recipe-style-guide-rules.md`.

**When to load:** any draft or edit under `content/english/blog/` that has ingredients, method steps, or Instant Pot timings.

## Voice split

| Zone | Voice |
|------|--------|
| Opening, section intros, close | JoRap - failures, what I'd skip, dry asides |
| Ingredients + numbered steps | ATK-scannable - imperative, no jokes, no "delicious" |

Story above `## How I run it` (or equivalent personality H2). Not inside step 3.

## Measurements

- **Metric first**, practical volume in parentheses: `160 ml, about 2/3 cup`
- Same format on **add lines** in steps when an ingredient hits the pot, pan, or bowl
- **Fractions as digits with slash** (`1/2` not `½`)
- Tiny amounts: spoons and grams when weighed; salt in a braise gets leeway, baking soda does not
- No dollar or peso amounts

## Steps repeat amounts on add

When a step **adds** an ingredient to the pot, pan, or bowl being cooked or served, spell the **same amounts** as the ingredients section - metric first, practical volume in parentheses.

Do **not** repeat amounts for:

- Prep-only steps (mince, chop, rinse) before anything hits the heat
- Remove, reserve, transfer, or stir steps
- Something already combined in an earlier step (`reserved marinade`, not the full list again)

Still avoid scroll-up shorthand: no "from the list above," "as listed," or bare names on an **add** line.

Bad (add line): `Combine the marinade from the list above (soy sauce, garlic, peppercorns, bay leaves).`

Good (add line): `Combine 160 ml soy sauce (about 2/3 cup), 10-11 cloves crushed garlic, 1 1/3 tsp whole black peppercorns, and 4 dried bay leaves. Add 2 kg bone-in, skin-on chicken thighs and coat thoroughly.`

Good (prep line): `Mince the fresh ginger and chop the garlic. Rinse the glutinous rice until the water runs clear.`

Good (transfer line): `Transfer the browned chicken to the Instant Pot. Add the reserved marinade, 160 ml water (about 2/3 cup), and 105-110 ml vinegar (about 7 tbsp) last.`

## Rules block (paste context for recipe sessions)

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
- Match existing JoRap recipe posts for Instant Pot liquid ratios unless the user gives new tested numbers
- No dollar or peso amounts
- Don't invent brand preferences not in author context

OUTPUT
- Markdown only, Hugo frontmatter at top
- draft: true unless user says publish
```

## Reference posts

Match shape and ratios unless the user gives new tested numbers:

- `content/english/blog/instant-pot-chicken-adobo.md`
- `content/english/blog/instant-pot-arroz-caldo.md`
