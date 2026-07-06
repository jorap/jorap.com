---
name: alex-eala-tracker-update
description: >-
  Update the Alex Eala Pro Career Tracker blog post with latest WTA rankings,
  tournament results, Grand Slam draws, and head-to-head records. Use when the
  user asks to update the Alex Eala tracker, refresh her career page, add new
  matches or tournaments, or sync alex-eala-pro-career-tracker with current WTA
  data.
---

# Update Alex Eala Pro Career Tracker

Living scrapbook post for Alex Eala's WTA career. Edit only:

`content/english/blog/alex-eala-pro-career-tracker.md`

Match the author's voice: first-person Filipino fan, proud but factual. Preserve existing entries; append or correct — never delete historical results unless a factual error is confirmed.

## Quick routing

| User wants | Follow |
| --- | --- |
| Full refresh (rankings + recent results + H2H) | [Full update workflow](#full-update-workflow) |
| One tournament or match added | [Single-result workflow](#single-result-workflow) |
| New opponent section | [Head-to-head workflow](#head-to-head-workflow) |
| Watch-list additions or suggestions | [Watch-list workflow](#watch-list-workflow) |
| Link order / format fixes | [Link format rules](#link-format-rules) |
| Tournament name cleanup | [Tournament naming rules](#tournament-naming-rules) |
| At a glance / summary refresh | [At a glance workflow](#at-a-glance-workflow) |
| Grand Slam Champions re-sort | [Grand Slam Champions sort](#grand-slam-champions-sort) |
| Top 20 opponent wins a Slam | [Slam-winner promotion workflow](#slam-winner-promotion-workflow) |
| Formatting templates and player IDs | [reference.md](reference.md) |

## Polite fetching (mandatory)

**Goal:** one update session should feel like a human checking a few pages — not a scraper.

1. **Read the tracker first.** Treat the file as cache. Only fetch what changed or is missing — never re-pull data already correct in the post.
2. **One domain at a time.** No parallel requests to the same host. Wait **≥ 2 seconds** between consecutive requests to the same domain.
3. **Fetch budget per session** (hard caps — stop and report gaps instead of exceeding):
   - WTA (`wtatennis.com`): **≤ 6** page loads (profile + singles matches + doubles matches + up to 3 targeted score/H2H URLs)
   - Tennis.com: **≤ 2**
   - TNNSLIVE: **≤ 1**
   - Grand Slam official sites: **≤ 4** total (only for rounds you are adding)
   - YouTube oembed: **only new** `VIDEO_ID`s you plan to embed — never re-verify IDs already in the file
4. **Prefer web search for discovery.** Use search to learn results, opponents, and URLs; then open **one** authoritative page per fact to confirm. Do not crawl search-result links in bulk.
5. **No retry loops.** If a WTA/Tennis.com fetch returns empty or errors once, switch source (see fallback below) or stop — do not retry the same URL with different headers, agents, or backoff spam.
6. **Opponent profiles are on demand.** Fetch an opponent's WTA page only when adding/promoting that opponent or verifying a new meeting — never bulk-check every Other Top 20 block on a routine refresh.
7. **Link checks:** spot-check **new** URLs only. Skip HEAD/fetch on links already in the tracker unless a user reports breakage.
8. **Summarize unverified gaps** rather than hammering sites to close every open question in one pass.

## Authoritative sources (use in this order)

1. **WTA profile** — rankings, career overview, H2H: `https://www.wtatennis.com/players/330332/alexandra-eala`
2. **WTA match results** — primary source for tournament runs, rounds, opponents, and scores:
   - Singles: `https://www.wtatennis.com/players/330332/alexandra-eala/matches`
   - Doubles: `https://www.wtatennis.com/players/330332/alexandra-eala/matches?type=D`
3. **Tennis.com** — match links, player profile: `https://www.tennis.com/players-rankings/alexandra-eala` (activity feed also useful when scraping recent results)
4. **TNNSLIVE** — recent form, draw context: `https://tnnslive.com/player/627278?content=form`
5. **Grand Slam sites** — Aus Open (`ausopen.com`), Roland Garros, Wimbledon, US Open official match pages
6. **YouTube** — match highlights, extended highlights, or full-match replays from official tour/slam channels or **regional rights-holding broadcasters worldwide**; see [reference.md](reference.md#youtube-embed-rules)

Use the WTA **Matches** pages to discover gaps vs the tracker (filter by year/tournament). Cross-check round reached and opponent on **one** alternate source before editing — not every source on every line.

**WTA fetch fallback:** WTA match pages are often client-rendered and may return little HTML to automated fetches. When that happens, use **one** of: Tennis.com activity, TNNSLIVE form, a single targeted WTA score URL (`/tournaments/.../scores/LS…` or `LD…`), or web search — then confirm on a second source. Do not chain multiple fallbacks against the same host.

## Full update workflow

```
Task progress:
- [ ] Read current tracker file (cache — note what is already current)
- [ ] Fetch only what gaps need: WTA profile if career high may have changed; WTA Matches (singles + doubles) if recent results missing — respect [Polite fetching](#polite-fetching-mandatory) caps
- [ ] Compare against existing content; list gaps
- [ ] Update WTA Rankings if career high changed
- [ ] Update **At a glance** if career highs, titles, best Slam, or notable firsts changed
- [ ] Add missing tournament results (newest year first)
- [ ] Add missing Grand Slam results (singles + doubles)
- [ ] Promote "Matches to Watch Out For" opponents who have now played
- [ ] Promote Other Top 20 opponents who won a Grand Slam (or newly verified Slam winner)
- [ ] Add or update H2H sections for new notable opponents
- [ ] Re-sort Grand Slam Champions by total Slam titles (if section changed)
- [ ] Deduplicate YouTube embeds (H2H wins over tournament blocks)
- [ ] Audit tournament names: brand-free labels + correct WTA tier or Grand Slam name
- [ ] Bump `lastmod` in frontmatter
- [ ] Verify links, embeds, and formatting
- [ ] Summarize changes for user (do not commit unless asked)
```

### Step 1 — Read the file

Load the full markdown file. Note the latest year sections and the most recent tournament entries so you do not duplicate.

Page section order (do not reorder):

1. Intro paragraph
2. **At a glance**
3. **Player Profile**
4. **WTA Rankings**
5. **Best Performances in WTA Tournaments** (Singles, then Doubles)
6. **Grand Slam Main Draw Results** (Singles, then Doubles)
7. **Matches Against Grand Slam Champions**
8. **Matches Against Other Top 20 Players**
9. **Matches to Watch Out For**
10. **Image Credits**

### Step 2 — Rankings

In **WTA Rankings**, update only if verified on WTA:

- **Career High** singles (currently No. 29) — update number and keep the "Highest-ranked Filipina in WTA history" note when still true
- **Career High** doubles (currently No. 88)

Do not add current live ranking unless the user explicitly asks; this page tracks career highs and milestones.

Mirror any career-high change in **At a glance** (see [At a glance workflow](#at-a-glance-workflow)).

### Step 3 — Tournament results

Section: **Best Performances in WTA Tournaments**

- Group by year; **newest year at top** within Singles and Doubles
- Add only main-draw or qualifying results that reached at least **Quarterfinals** (or finals/winner — same threshold as existing entries)
- **Always include the event tier** in parentheses on every WTA tournament line: `(WTA 125)`, `(WTA 250)`, `(WTA 500)`, or `(WTA 1000)`. Grand Slam entries use the four major names only — no tier suffix (they are Grand Slams by definition). See [Tournament naming rules](#tournament-naming-rules).
- Prefer dual links when both exist: `[wtatennis.com](url) | [tennis.com](url)` (WTA first, then tennis.com)
- **Exit-round rule:** the main tournament line must link to the **deepest round played** (the loss or title match). Earlier rounds go on sub-bullets — never point the exit line at an earlier-round opponent.
- Add milestone sub-bullets only for firsts (e.g. first WTA title, first Filipina to reach X)
- **Doubles:** exit round gets `| [wtatennis.com](url)` on the main line; earlier rounds as `Round | [wtatennis.com](url)` sub-bullets. Add `(with Partner Name)` on every doubles tournament line.

See [reference.md](reference.md) for entry templates and tier lookup.

#### Tournament naming rules

Tournament display names must be **brand-free** and **tier-labeled**.

**WTA tour format:** `**{Location or event name} (WTA {tier})**`

- **Location first** — city or region (e.g. `Berlin`, `Dubai`, `Manila`, `Indian Wells`)
- **Tier required** — one of `WTA 125`, `WTA 250`, `WTA 500`, `WTA 1000`
- **No sponsor or corporate brands** — strip presenting partners, banks, auto makers, pharma, telecom, etc. from the visible name even when WTA or tennis.com URLs still use the branded slug

| Avoid (branded) | Use instead |
| --- | --- |
| Lexus Birmingham Open | **Birmingham (WTA 125)** |
| Mubadala Abu Dhabi Open | **Abu Dhabi (WTA 500)** |
| ASB Classic | **Auckland (WTA 250)** |
| BNP Paribas Open | **Indian Wells (WTA 1000)** |
| Internazionali BNL d'Italia | **Rome (WTA 1000)** or **Rome Open (WTA 1000)** |
| Vanda Pharmaceuticals Berlin Tennis Open | **Berlin (WTA 500)** |
| National Bank Open | **Montreal (WTA 1000)** or **Toronto (WTA 1000)** — match the host city that year |
| Porsche Tennis Grand Prix | **Stuttgart (WTA 500)** |

**Optional suffixes:** `Open` or `International` are fine when they distinguish the event (e.g. `Miami Open (WTA 1000)`, `Canberra International (WTA 125)`). Never add a sponsor before them.

**Grand Slam format:** `**Australian Open**`, `**French Open**`, `**Wimbledon**`, `**US Open**` — no `(WTA …)` suffix. Do not use sponsor names (e.g. not "Roland Garros presented by …").

**H2H match lines** (`**YYYY Tournament - Surface - Win/Loss**`): same brand-free rule — `2026 Berlin`, not `2026 Vanda Pharmaceuticals Berlin Open`; `2026 Indian Wells`, not `2026 BNP Paribas Open`. Tier is optional in H2H lines but the name must still be sponsor-free.

**At a glance / title shorthand:** compact form is OK — e.g. `Guadalajara 125`, `Birmingham 125` (city + tier number, no brand).

**Tier lookup:** confirm category on the tournament's WTA page (`wta125`, `wta250`, `wta500`, `wta1000` in URL or event header). When promoting or correcting existing entries, fix branded names to match this table.

### Step 4 — Grand Slam results

Section: **Grand Slam Main Draw Results**

- Add new year blocks when a new Slam season starts
- Record deepest round reached; link each round played
- **Singles and doubles** use the same dual-link format per round: `1st Round | [wtatennis.com](url) | [official slam site](url)` (WTA first, then ausopen.com / rolandgarros.com / wimbledon.com / usopen.org)
- **Doubles:** every tournament line includes `(with Partner Name)` — same pattern as Best Performances doubles
- WTA doubles scores URLs use `LD…` IDs; singles use `LS…`
- Note special context (e.g. Centre Court, first Filipina in main draw) as sub-bullets
- Add YouTube embeds below the tournament block when verified match footage exists (see Step 6) — **singles and doubles**

### Step 5 — Head-to-head sections

Two groups exist today:

1. **Matches Against Grand Slam Champions** — opponent has won at least one major
2. **Matches Against Other Top 20 Players** — top-tier opponents without slam section yet

**Promotion rule:** When Eala plays someone listed under **Matches to Watch Out For**, move them to the correct H2H section and remove them from the watch list. Same rule for any opponent who has a completed pro H2H but is still on the watch list (e.g. after a first meeting at a Slam or 1000).

**Slam-winner promotion:** When an opponent in **Other Top 20 Players** wins a Grand Slam singles title — or already has one verified on WTA but is still in Other Top 20 — **promote** them to **Grand Slam Champions** on the next update. See [Slam-winner promotion workflow](#slam-winner-promotion-workflow).

**New opponent rule:**

- Won a Grand Slam (or wins one before/after first meeting) → `### [Name]` under **Grand Slam Champions** — never under Other Top 20, even if they are also a current top-20 player
- Top 20 or notable rivalry **without** a Slam singles title → new `### [Name]` under **Other Top 20 Players** (WTA profile, H2H link, and YouTube embeds only — no match stat lines)

Grand Slam titles table is required only in the Grand Slam Champions section. Look up titles on the opponent's WTA profile.

#### Grand Slam Champions sort

After adding or reordering opponents in **Matches Against Grand Slam Champions**, sort blocks by:

1. **Total Grand Slam singles titles** (descending)
2. **Tie-break:** opponent whose **most recent Slam title is newer** goes first

Count titles from each opponent's **Grand Slam Titles** table. Do not re-sort **Other Top 20 Players** by Slam count — sort **Other Top 20** blocks **alphabetically by last name** instead.

### Step 6 — YouTube embeds

Add `{{< youtube VIDEO_ID >}}` shortcodes below tournament and H2H entries when verified match footage exists. Follow [YouTube embed rules](reference.md#youtube-embed-rules). Never guess video IDs — oembed-check **new** IDs only (`title` + `author_name`); IDs already embedded in the tracker are trusted.

Search **official tour/slam channels first**, then **rights-holding broadcasters in any region** (Americas, Europe, Asia-Pacific, Middle East, etc.) before leaving a gap. See [Broadcaster search strategy](reference.md#broadcaster-search-strategy).

For **Best Performances in WTA Tournaments** (singles), embed the **last two matches** of each run, in chronological order (earlier round first, exit round second).

For **Grand Slam Main Draw Results** (singles and doubles), search for verified match footage for **each round played**. Embed below the tournament block — one shortcode per round when separate official/broadcaster uploads exist; otherwise one embed for the run. Same channel rules as singles; include `doubles` / both pair names in YouTube queries.

### Step 7 — Verify

- No duplicate tournament lines
- Years descending within each subsection
- Link order: `wtatennis.com` before `tennis.com` or official slam site everywhere
- Grand Slam Champions section sorted by Slam titles (see above)
- Grand Slam Champions **Matches** lists are newest-first
- No Slam singles title-holder left in Other Top 20 (promote if found)
- **At a glance** matches WTA Rankings and latest milestones
- YouTube embeds from official/broadcaster channels only — no fan reuploads
- No duplicate `VIDEO_ID` across tournament and H2H sections (H2H wins)
- Exit-round tournament links point to the deepest round played
- Tournament names are **brand-free** and include `(WTA 125|250|500|1000)` on every WTA tour line; Grand Slams use the four major names only
- H2H match lines use brand-free tournament names
- New links only: spot-check URLs added this session (do not re-fetch every existing link)
- `lastmod` bumped; other frontmatter unchanged unless user asks
- Run `read_lints` on the edited file if available

## Link format rules

| Section | Format |
| --- | --- |
| WTA singles (Best Performances) | `Round \| [wtatennis.com](url) \| [tennis.com](url)` |
| WTA doubles (Best Performances) | `Round (with Partner) \| [wtatennis.com](url)` on exit line; earlier rounds as sub-bullets |
| WTA title runs | `Winner \| [wtatennis.com](url) \| [tennis.com](url)` plus milestone sub-bullets |
| Grand Slam singles/doubles | `1st Round \| [wtatennis.com](url) \| [official slam site](url)` per round played |
| Grand Slam doubles header | `- **Slam** - Round (with Partner)` before round sub-bullets |
| Grand Slam Champions H2H | Match stat lines use `tennis.com` or `wtatennis.com` match URLs |
| Other Top 20 H2H | WTA profile + H2H links + YouTube only — no match lines |

## Single-result workflow

When the user names one tournament or match:

1. Confirm result on WTA **or** tennis.com (one primary + one quick cross-check — stay within fetch budget)
2. Insert in the correct year block (create the year heading if missing)
3. Update H2H if opponent section exists; otherwise follow [Head-to-head workflow](#head-to-head-workflow)
4. Update career-high ranking and **At a glance** if this result caused a new peak, title, or notable first
5. Bump `lastmod`

## Head-to-head workflow

1. Look up opponent WTA ID via search or [reference.md](reference.md) watch-list IDs
2. H2H URL pattern: `https://www.wtatennis.com/head-to-head/330332/[OPPONENT_ID]`
3. Copy structure from an existing opponent block (Grand Slam Champions: Madison Keys; Other Top 20: Iva Jovic)
4. Add match line: `**YYYY Tournament - Surface - Win/Loss** - [Match Stats](url)` (Grand Slam Champions section only). List matches **newest first**. Tournament name must be **brand-free** (see [Tournament naming rules](#tournament-naming-rules)).
5. Add YouTube shortcodes only if a verified highlight, extended highlight, or full-match replay exists — see [YouTube embed rules](reference.md#youtube-embed-rules). For **Other Top 20 Players**, embeds only — no match lines.
6. If opponent came from the watch list, remove their watch-list line
7. Re-sort **Grand Slam Champions** if a new Slam winner was added

## Slam-winner promotion workflow

Run during every full refresh and whenever a known Other Top 20 opponent wins a major.

**Who to check:** `###` blocks in **Matches Against Other Top 20 Players** only when a full refresh runs **and** you have fetch budget left — prioritize opponents with recent Slam news (web search first). Confirm titles on **one** opponent WTA profile at a time; list meetings via that opponent's [WTA H2H](https://www.wtatennis.com/head-to-head/330332/[OPPONENT_ID]) URL only when promoting.

**When to promote:** opponent has **at least one Grand Slam singles title** and an existing H2H block (they have already met Eala in a tracked context).

**Steps:**

1. **Remove** the opponent's `###` block from **Other Top 20 Players**
2. **Insert** the block into **Grand Slam Champions** using the upgraded format:
   - Keep WTA profile and H2H links
   - Add **Grand Slam Titles** table from the opponent's WTA profile
   - Add **Matches:** with one stat line per completed singles meeting vs Eala — surface, Win/Loss, `[Match Stats](url)` (pull from WTA H2H + [WTA Matches](https://www.wtatennis.com/players/330332/alexandra-eala/matches))
   - Move existing YouTube embeds under the matching match lines where possible; otherwise keep below the block
3. **Re-sort** Grand Slam Champions by total Slam titles (see [Grand Slam Champions sort](#grand-slam-champions-sort))
4. Update opponent lists in [reference.md](reference.md)

**First meeting after a Slam win:** if Eala plays a watch-list or new opponent who is already a Slam champion, create the block directly under **Grand Slam Champions** — do not place them in Other Top 20 first.

**Doubles-only context:** if the only documented meeting is doubles (e.g. a Rome QF loss to a Slam-winning pair), keep the opponent in **Other Top 20** until a singles H2H exists, unless the user asks to promote on doubles alone. **Doubles-Slam titles do not trigger promotion** — e.g. Paolini (French Open 2024 singles + Rome 2025 doubles QF only) stays in Other Top 20.

**Duplicate YouTube embeds:** when the same video appears in a tournament entry and an H2H section, keep it in **H2H only**; tournament blocks retain non-overlapping round highlights.

## Watch-list workflow

Section: **Matches to Watch Out For**

Add only opponents Eala has **not** completed a pro-level H2H with yet (junior-only meetings are OK to note in the line, like Andreeva).

**Good candidates:**

- Grand Slam winners or multi-Slam legends with no pro H2H
- Current top-20 fixtures likely to cross paths in 1000s or Slams

**Line format:** `- [Player Name](https://www.wtatennis.com/head-to-head/330332/OPPONENT_ID) - credential note`

Use WTA H2H links (not profile pages). Keep notes short: Slam wins, Olympic gold, recent breakthrough — whatever makes the matchup worth watching.

Sort watch-list entries **alphabetically by last name** (e.g. Anisimova before Zheng).

When suggesting additions, skip anyone already in an H2H section or with a completed pro meeting pending promotion.

## At a glance workflow

Section: **At a glance** — snapshot block directly under the intro, before **Player Profile**.

Update whenever career highs, title count, best Slam run, or a notable first changes:

- **Career highs:** `No. XX singles · No. YY doubles` (middle dot separator)
- **WTA titles:** count plus tournament names (e.g. `2 (Guadalajara 125, Birmingham 125)`)
- **Best Slam (singles):** deepest round at any major (e.g. `US Open 2025 — Round of 2`)
- **Notable firsts:** semicolon-separated milestone list

Keep lines factual and compact — no links or embeds. See [reference.md](reference.md#at-a-glance-template).

## Frontmatter

On every content update, bump `lastmod` to the current UTC timestamp (e.g. `lastmod: 2026-06-18T18:00:00Z`). Do not change `slug`, `title`, `date`, or `draft` unless the user asks.

## Do not change

- Intro paragraph tone and scrapbook framing
- **Player Profile** link set: WTA Profile, WTA Matches, WTA Doubles Matches, Tennis.com profile, TNNSLIVE (update only if URLs break)
- **Image Credits** section
- Hugo shortcode syntax (`{{< youtube ID >}}`, not `{{</* youtube */>}}`)
- Unrelated site files

## After editing

1. Show a concise diff summary: At a glance, rankings, tournaments added, H2H updates, watch-list removals, embed dedup
2. Flag anything that could not be verified
3. Do **not** commit unless the user asks

## Related

- **hugo-template-guidance** — if shortcodes or blog frontmatter questions arise
- Formatting templates and player IDs: [reference.md](reference.md)
