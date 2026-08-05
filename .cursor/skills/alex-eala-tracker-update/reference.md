# Alex Eala Tracker - Reference

## Player identifiers

| Source | ID / URL |
| --- | --- |
| WTA player | `330332` - `https://www.wtatennis.com/players/330332/alexandra-eala` |
| WTA matches (singles) | `https://www.wtatennis.com/players/330332/alexandra-eala/matches` |
| WTA matches (doubles) | `https://www.wtatennis.com/players/330332/alexandra-eala/matches?type=D` |
| Tennis.com | `627278` - `https://www.tennis.com/players-rankings/alexandra-eala` |
| TNNSLIVE | `627278` |

H2H base: `https://www.wtatennis.com/head-to-head/330332/[OPPONENT_ID]`

## Player Profile links

```markdown
- [WTA Profile](https://www.wtatennis.com/players/330332/alexandra-eala/#overview)
- [WTA Matches](https://www.wtatennis.com/players/330332/alexandra-eala/matches#main-content)
- [WTA Doubles Matches](https://www.wtatennis.com/players/330332/alexandra-eala/matches?type=D)
- [Tennis.com](https://www.tennis.com/players-rankings/alexandra-eala)
- [TNNSLIVE](https://tnnslive.com/player/627278?content=form)
```

## At a glance template

```markdown
## At a glance

- **Career highs:** No. 20 singles · No. 88 doubles
- **WTA titles:** 3 (Guadalajara 125, Birmingham 125, Washington 500)
- **Best Slam (singles):** Wimbledon 2026 - Round of 16
- **Notable firsts:** First Filipina in a Grand Slam main draw; first Filipina to win a Slam main-draw match (US Open 2025); first Filipina to reach a Grand Slam fourth round in the Open era (Wimbledon 2026); first Filipina in a WTA 1000 semifinal (Miami 2025); first Filipina to win a WTA 500 title (Washington 2026); first Filipina in the WTA top 20; first Filipina in the WTA top 100
```

Update all four lines when any underlying milestone changes.

## Tournament naming

Every WTA tournament entry must show the **tier** and **no sponsor brands**.

| Tier | Label in entry |
| --- | --- |
| WTA 125 | `(WTA 125)` |
| WTA 250 | `(WTA 250)` |
| WTA 500 | `(WTA 500)` |
| WTA 1000 | `(WTA 1000)` |
| Grand Slam | No tier suffix - use `Australian Open`, `French Open`, `Wimbledon`, or `US Open` |

**Entry format:** `**{City or event name} (WTA {tier})** - {round}`

Strip sponsor names from the display label (Lexus, Mubadala, ASB, BNP Paribas, Porsche, National Bank, Vanda, etc.). URLs may keep branded slugs; visible text must not.

**H2H match lines:** `**YYYY {brand-free name} - {Surface} - {Result}**` - e.g. `2026 Berlin`, `2026 Indian Wells`, `2025 Miami Open`.

Confirm tier on the WTA tournament page before adding or correcting an entry.

## Score format

**Always list Eala's games first** in every set and match tiebreak - wins and losses, singles and doubles.

**Opponent names:** first + last on every `d.`/`l.` line and doubles pair. Examples below use full names - never shorten to surname only on result lines.

- Win: `d. Leylah Fernandez 6-3, 6-4` (Eala's games left of the hyphen in each set)
- Loss: `l. Linda Noskova 2-6, 4-6` - not the winner's `6-2, 6-4`
- Split sets: `l. Jasmine Paolini 6-3, 4-6, 2-6` (Eala won set 1, lost sets 2–3)
- Doubles pair: `l. Jasmine Paolini/Sara Errani 7-5, 3-6, 7-10`
- Match tiebreak (doubles): Eala's points first - `7-5, 3-6, 7-10` not `10-7`
- Retirements: score at stoppage from Eala's side - `6-4, 0-1 ret.`
- Walkovers (Best Performances only): `d. Paula Badosa w/o` or `l. Opponent w/o` - full name, no set scores; include match links
- Tiebreak notation unchanged: `7-6(5)` means Eala 7 games, opponent 6, TB 5–7

When copying from WTA or tennis.com, flip any set or super-tiebreak segment that lists the opponent first.

## Walkovers

A **walkover** (`w/o`, opponent withdrew before the match was played) is **not an H2H meeting**:

- **Best Performances** - list the round: `Round, d. Opponent w/o |` links (singles: WTA + tennis.com when available; doubles: WTA). No set scores.
- **Grand Slam results** - omit walkover rounds.
- Do not create or keep an H2H `###` block when walkover-only contact is the only meeting.
- Opponent stays on **Matches to Watch Out For** until the ball is struck in a pro meeting.
- **Retirements** (`ret.`) after play started still count as matches.

## Entry templates

### Tournament result (singles)

```markdown
  - **Dubai (WTA 1000)** - Quarterfinals, l. [Coco Gauff](#coco-gauff) 0-6, 2-6 | [wtatennis.com](https://...) | [tennis.com](https://...)
    - Round of 16, d. Sorana Cîrstea 7-5, 6-4 | [wtatennis.com](https://...) | [tennis.com](https://...)
```

Link opponent full name to the in-page H2H `###` anchor when that block exists (`[Coco Gauff](#coco-gauff)`). Leave unlinked when no H2H section (e.g. Sorana Cîrstea).

Embed at most **three** videos for opponents **not** in either H2H section (last three such matches in the run). Omit embeds when deep rounds were all vs H2H opponents.

Title run:

```markdown
  - **Birmingham (WTA 125)** - Winner, d. Nikola Bartunkova 5-7, 6-3, 7-5 | [wtatennis.com](https://...) | [tennis.com](https://...)
    - Second Career WTA Win
    - First career title on grass

{{< youtube VIDEO_ID >}}
```

With milestone (link-only round label also valid when tennis.com slug is missing):

```markdown
  - **Guadalajara (WTA 125)** - Winner | [wtatennis.com](https://...)
    - First Career WTA Win
```

### Doubles result

Exit round on the main line; earlier rounds as sub-bullets. Always include partner:

```markdown
  - **Abu Dhabi (WTA 500)** - Semifinals (with Janice Tjen) | [wtatennis.com](https://...)
    - Quarterfinals | [wtatennis.com](https://...)
    - Round of 16 | [wtatennis.com](https://...)

{{< youtube VIDEO_ID >}}
```

Rome-style loss note (optional sub-bullet before round links):

```markdown
  - **Rome Open (WTA 1000)** - Quarterfinals (with Coco Gauff) | [wtatennis.com](https://...)
    - Lost to defending champions Jasmine Paolini / Sara Errani
    - Round of 16 | [wtatennis.com](https://...)
    - Round of 32 | [wtatennis.com](https://...)
```

### Grand Slam result (singles)

```markdown
  - **Wimbledon**
    - 4th Round, l. [Jasmine Paolini](#jasmine-paolini) 4-6, 6-4, 3-6 | [wtatennis.com](https://...) | [tennis.com](https://...)
    - 3rd Round, d. [Iga Swiatek](#iga-swiatek) 7-6(9), 6-2 | [wtatennis.com](https://...) | [tennis.com](https://...)
    - 2nd Round, d. Maya Joint 3-6, 6-2, 6-0 | [wtatennis.com](https://...) | [tennis.com](https://...)

{{< youtube VIDEO_ID >}}
```

Same H2H in-page link rule as WTA singles: wrap full names only when a `###` block exists.

### Grand Slam result (doubles)

Same dual-link pattern as singles; include partner on the tournament line:

```markdown
  - **French Open** - 2nd Round (with Renata Zarazua)
    - 1st Round | [wtatennis.com](https://...) | [rolandgarros.com](https://...)
    - 2nd Round | [wtatennis.com](https://...) | [rolandgarros.com](https://...)

{{< youtube VIDEO_ID >}}
```

Add embeds when verified official/broadcaster footage exists - every non-H2H round (no cap); omit H2H-opponent rounds (those live in H2H sections).

### H2H section (Grand Slam champion)

```markdown
### Opponent Name

- [WTA Profile](https://www.wtatennis.com/players/XXXXXX/opponent-slug)
- [Head to Head](https://www.wtatennis.com/head-to-head/330332/XXXXXX)
- **Career High Singles:** No. XX

**Grand Slam Titles:**

| Tournament  | Year(s) |
| ----------- | ------- |
| French Open | 2020    |

**Matches:**

- **2026 Rome - Clay Court - Loss** - [Match Stats](https://...)
- **2025 Miami Open - Hard Court - Win** - [Match Stats](https://...)

List completed singles meetings **newest first**.

{{< youtube VIDEO_ID >}}
```

### H2H section (top player, no slam table)

Other Top 20 sections use the same **Matches:** format as Grand Slam Champions but **omit** the Slam titles table.

```markdown
### Opponent Name

- [WTA Profile](https://www.wtatennis.com/players/XXXXXX/opponent-slug)
- [Head to Head](https://www.wtatennis.com/head-to-head/330332/XXXXXX)
- **Career High Singles:** No. XX

**Matches:**

- **2026 Berlin (Grass)** - Quarterfinals, WIN, 6-3, 6-4 | [wtatennis.com](https://...) | [tennis.com](https://...)

List completed singles meetings **newest first**. Add official slam site link on Grand Slam meetings.

{{< youtube VIDEO_ID >}}
```

### Watch list entry

```markdown
- [Opponent Name](https://www.wtatennis.com/head-to-head/330332/OPPONENT_ID) - Career High No. XX; credential note
```

**Criteria:** no completed pro H2H yet; opponent is a Slam winner, legend, or current top-tier draw Eala is likely to meet. Remove from this list once they play - promote to the correct H2H section instead.

## Grand Slam Champions sort order

Sort `###` blocks in **Matches Against Grand Slam Champions** by total Slam singles titles (descending). Tie-break: most recent Slam title year wins.

Current order (as of last update):

| Order | Player | Titles | Latest |
| --- | --- | ---: | --- |
| 1 | Iga Swiatek | 6 | Wimbledon 2025 |
| 2 | Naomi Osaka | 4 | Australian Open 2021 |
| 3 | Elena Rybakina | 2 | Australian Open 2026 |
| 4 | Coco Gauff | 2 | French Open 2025 |
| 5 | Barbora Krejcikova | 2 | Wimbledon 2024 |
| 6 | Linda Noskova | 1 | Wimbledon 2026 |
| 7 | Madison Keys | 1 | Australian Open 2025 |
| 8 | Marketa Vondrousova | 1 | Wimbledon 2023 |
| 9 | Jelena Ostapenko | 1 | French Open 2017 |

Recompute this table whenever a new Slam champion block is added or an opponent wins another major.

## H2H section placement

| Opponent status | Section | Format |
| --- | --- | --- |
| Slam singles winner + singles H2H with Eala | **Grand Slam Champions** | Titles table + **Career High Singles** + match stat lines + YouTube |
| Top 20 / notable, no Slam singles title | **Other Top 20 Players** | WTA + H2H links + **Career High Singles** + match stat lines + YouTube |
| Slam winner, no singles H2H yet (doubles only) | **Other Top 20** until singles meeting | Match lines when singles H2H exists; YouTube only until then |
| Slam winner, no pro H2H yet | **Matches to Watch Out For** | H2H link + credential note |

When an Other Top 20 player **wins a new Slam**, promote on the next update (see Slam-winner promotion workflow in `SKILL.md`).

## Watch list - known opponent WTA IDs

Use when promoting to H2H or building watch-list links:

| Player | WTA ID | Notes |
| --- | --- | --- |
| Amanda Anisimova | 326384 | 2025 Wimbledon semifinalist |
| Bianca Andreescu | 325088 | 2019 US Open |
| Mirra Andreeva | 331809 | 2026 French Open Winner; Junior US Open 2022 context |
| Paula Badosa | 320124 | Former world No. 2; no pro H2H yet (Miami 2025 walkover only) |
| Belinda Bencic | 319001 | Olympic gold; 2026 Rome SF |
| Sofia Kenin | 320942 | 2020 Australian Open |
| Emma Navarro | 325410 | 2025 Strasbourg; top-20 American |
| Naomi Osaka | 319998 | Multi-Slam winner |
| Emma Raducanu | 328366 | 2021 US Open |
| Aryna Sabalenka | 320760 | Multi-Slam winner |
| Diana Shnaider | 330482 | 2026 Roland Garros SF; Monterrey 2025 |
| Qinwen Zheng | 328120 | 2024 AO finalist; Olympic gold; stay in Other Top 20 (no Slam singles title) |

## Existing H2H opponents (do not duplicate sections)

**Grand Slam Champions** (sorted by Slam titles): Iga Swiatek (326408), Naomi Osaka (319998), Elena Rybakina (324166), Coco Gauff (328560), Barbora Krejcikova (318314), Linda Noskova (329668), Madison Keys (316959), Marketa Vondrousova (323027), Jelena Ostapenko (319939)

**Other Top 20** (alphabetical by last name): Ekaterina Alexandrova (319007), Leylah Fernandez (326735), Iva Jovic (332285), Marta Kostyuk (326482), Magda Linette (315130), Victoria Mboko (331006), Elise Mertens (317964), Karolina Muchova (322191), Jasmine Paolini (319280), Anastasia Pavlyuchenkova (313796), Jessica Pegula (316956), Elina Svitolina (316738), Clara Tauson (327793), Donna Vekić (318516), Qinwen Zheng (328120)

Sort **Other Top 20** and **Matches to Watch Out For** alphabetically by **last name** when adding or reordering entries.

**Paolini (319280):** French Open / Wimbledon 2024 singles finalist (no Slam singles title); FO 2025 doubles champion with Errani. Singles H2H with Eala exists (Dubai 2026, Wimbledon 2026) - stay in **Other Top 20**. Do **not** promote on doubles-Slam titles alone.

## Surface labels

Use exactly: `Hard Court`, `Clay Court`, `Grass Court`

## Result labels

Use exactly: `Win`, `Loss`, or `Win (Retired)` when applicable

## Link preferences

| Content | Preferred link |
| --- | --- |
| WTA tour matches | `tennis.com` tournament match URL |
| WTA official scores | `wtatennis.com` tournament scores URL |
| Grand Slams | WTA scores first, then official slam match page |
| Player / H2H | `wtatennis.com` |
| Exit round (tournaments) | Main line links to deepest round played; earlier rounds on sub-bullets |

## YouTube embed rules

Embed only when the video shows **actual tennis** (points, games, match action). Reject news segments that announce results without match footage.

**Syntax:** each embed on its own line at **column 0** - `{{< youtube VIDEO_ID >}}` with no leading space (indented or inline shortcodes will not render in Hugo).

### Placement (priority order)

A `VIDEO_ID` appears in **one** section only. Higher priority wins.

1. **Matches Against Grand Slam Champions** - **every** verified video for **all** completed singles meetings; place under the matching match line when possible
2. **Matches Against Other Top 20 Players** - **every** verified video for **all** completed meetings; place under the matching **Matches:** line when possible
3. **Grand Slam Main Draw Results** (singles and doubles) - **every** verified video for rounds vs opponents **not** in either H2H section; **no per-run cap**. Zero embeds when all rounds were vs H2H opponents
4. **Best Performances in WTA Tournaments** (singles and doubles) - at most **three** embeds per run, **only** for opponents **not** in either H2H section; **last three** such matches in the run, earlier round first. Zero embeds when all deep rounds were vs H2H opponents (e.g. Miami 2025, Washington 2026)

**Duplicate embeds:** H2H sections win over Grand Slam and Best Performances. Those sections may have **no embeds** after dedup.

Search in this order until a verified match video is found:

1. **Official tour / slam channels** - WTA (`WTA`), LTA (`LTA`), Grand Slam channels (`Australian Open`, `Wimbledon`, `US Open Tennis Championships`, `Roland-Garros`), tournament organizers (`Tennis Canada`, `Tennis Australia`, etc.)
2. **Rights-holding broadcasters (any region)** - verified uploads from networks that hold TV/streaming rights for that event. Accept when `author_name` is a known broadcaster and the title clearly names the match (both players or player + round), tournament, and includes match footage labels such as `Highlights`, `Extended Highlights`, `Match Highlights`, `Full Match`, `REPLAY`, `H/L`, or regional equivalents.

Do **not** limit broadcaster search to one country. For every gap, search globally before omitting an embed.

### Broadcaster search strategy

Run multiple YouTube queries per missing match:

1. `[Player A] [Player B] [Tournament] [Year] highlights`
2. For **doubles:** `[Eala] [Partner] [Opponent pair or surnames] [Slam] [Year] doubles highlights` - also try partner-only pair names from the draw
3. Same query + broadcaster names from the table below (e.g. `beIN`, `Eurosport`, `Tennis Channel`, `SPOTV`)
3. Official channel scoped search: `site:youtube.com/c/WTA`, `/LTA`, `/rolandgarros`, `/Wimbledon`, etc.

Verify every candidate via oembed (`author_name` + `title`). Prefer official tour/slam uploads when both exist; otherwise use the best verified broadcaster upload.

### Broadcaster acceptance criteria

Accept when **all** are true:

- Channel is a recognized sports broadcaster or the event's official broadcast partner - not a fan account, podcast, or highlight-aggregator
- Title identifies the specific match (players, round, and/or tournament)
- Video is highlights, extended highlights, or a full-match replay - not a news segment, preview, or analysis-only clip

Reject broadcaster uploads that are clearly news wrappers (result announcements, studio segments) without sustained match action.

### Reject

- **Unofficial reupload / fan channels** - including `Tennis Stories`, `CueTV`, `Nice One`, `Guil Signe`, `LUWALHATI`, `stateofsport211`, `Next Tennis Gems`, and similar third-party compilations (even when the title copies WTA wording)
- News result clips: `TV Patrol`, `DZMM Teleradyo`, titles with `pasok`, `kampeon sa`, `umusad`, `falls short` without match highlights
- Segments titled **Play by Play** on One Sports (news show name, not match coverage)
- Interviews, vlogs, podcasts, fan reaction, or analysis without sustained match footage
- Unverified fan IDs; never guess from search snippets alone

### Verification

1. Confirm video via YouTube oembed API or fetch: `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json`
2. Check `author_name` and `title` match the intended match, round, and opponent
3. Prefer official WTA/LTA/slam uploads when both exist; otherwise use verified regional broadcaster uploads - never use unofficial reupload channels

### Known channel quick reference

Examples only - not an exhaustive list. Search other regional rights holders when these have no upload.

| Region | Channel | Typical use |
| --- | --- | --- |
| Global / tour | WTA | WTA 250–1000 `WTA Match Highlights` |
| UK / grass | LTA | Lexus Birmingham, Ilkley, Nottingham grass 125s |
| Grand Slams | Australian Open, Wimbledon, US Open Tennis Championships, Roland-Garros | Official slam highlights, extended highlights, full matches |
| Americas | Tennis Channel, ESPN | WTA / Grand Slam highlights and replays |
| Europe | Eurosport, Sky Sports Tennis, BBC Sport (Wimbledon), TNT Sports, France TV / `Roland-Garros` | Regional Grand Slam and WTA packages |
| Middle East / Asia | beIN SPORTS, beIN SPORTS Asia, SPOTV ASIA | Grand Slam and WTA `Match Highlights` / `H/L` |
| Philippines | One Sports, ABS-CBN News | One Sports: `FULL GAME HIGHLIGHTS` only. ABS-CBN: `REPLAY: … FULL MATCH` when sustained match tennis is shown - not `TV Patrol` result clips |
| Canada | Tennis Canada | National Bank Open match packages |
| Australia / NZ | Tennis Australia, Nine / Wide World of Sports | Home-tournament highlights when uploaded to YouTube |

## Threshold for inclusion

Mirror existing scope:

- **WTA tournaments:** QF or better (or title/finalist milestones worth calling out)
- **Grand Slams:** all main-draw rounds played
- **H2H:** every completed match vs opponents in those sections; add new section when a watch-list player is met or a significant new opponent appears
