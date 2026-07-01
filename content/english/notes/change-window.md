---
title: "Change Window"
meta_title: "Change Window - Schedule Risky Changes When Rollback Help Is Awake"
description: "Schedule risky changes when the people who can revert are reachable - not Friday night when everyone's offline."
date: 2026-07-01T14:00:00+08:00
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["Safety", "DevOps", "Systems Thinking", "Leadership"]
slug: "change-window"
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "Client site ready Friday 5pm. When do we push?"
    back: "Tuesday standup - rollback crew is awake"
  - front: "Wedding weekend - marketing wants a Hugo bump. What's the move?"
    back: "Queue edits - no version bumps until Monday"
  - front: "Bad deploy last Friday - nobody could revert until Monday. What's the rule now?"
    back: "Change window - staffed hours only"
  - front: "Risky deploy and I'm the only one who knows git revert. What's missing?"
    back: "Window plus shared runbook - not heroics at midnight"
draft: false
aliases: ["deploy window", "release window"]
---
Schedule risky changes when rollback help is awake - not Friday night when everyone's offline.

## Key Concept

[[Rollback Principle]] fails when the people who can revert are asleep or at a wedding.

A change window is boring calendar hygiene: deploy Tuesday morning, freeze before holidays, keep the old build one click away. Not fear of shipping - matching risk to coverage. PKM parallel: [[Maintenance Window]] is scheduled garden prune; change window is scheduled production risk.

## Examples

- We stopped Friday-night client deploys after the bad release - Tuesday standup owns rollback if it goes loud.
- Wedding weekend freeze: marketing edits queue, no Hugo version bumps until Monday.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| alternative | [[Maintenance Window]] | PKM prune schedule vs production deploy schedule |
| contradicts | [[Ship It]] | when milestone pride ships Friday at 5:01 |
| extends | [[Preparedness]] | Window assumes rehearsed undo path and someone on call |
| extends | [[Risk Management]] | Time-box exposure to staffed hours |
| extends | [[Rollback Principle]] | Risky push only when revert crew is reachable |
| extends | [[Standard Operating Procedures]] | Written deploy windows belong in the runbook |

## See also

- [[Client Site Handoff]] - Website Building
- [[Free Tier Hosting Stack]] - DevOps, Website Building
- [[Selling Static Sites]] - Website Building
