---
title: "Staged Rollout"
meta_title: "Staged Rollout - Ship to a Slice Before Everyone Is the Test"
description: "Ship the change to a small slice first - rollback stays cheap if the new state bleeds."
date: 2026-07-01T14:00:00+08:00
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["Safety", "Systems Thinking", "DevOps", "Risk Management"]
slug: "staged-rollout"
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "New layout ready - push straight to main or preview branch first?"
    back: "Preview branch - rollback doesn't touch production"
  - front: "New inbound play for Friday's game. When do we run it?"
    back: "Scrimmage Tuesday - revert at halftime if it bleeds"
  - front: "New screen-time rule for the whole house. What's the move?"
    back: "One kid one week - old routine on the fridge"
  - front: "New sauce for every table tonight. What stays in the warmer?"
    back: "Old batch until first table clears"
draft: false
aliases: ["canary deploy", "gradual rollout"]
---
Ship the change to a small slice first - rollback stays cheap if the new state bleeds.

## Key Concept

Full-blast deploy turns every user into a test subject.

Staged rollout - preview branch, one table section, scrimmage Tuesday - keeps [[Reversibility]] real. [[Safety by Design]] at release time: harm hits fewer people before you commit the whole lane.

## Examples

- Cloudflare preview branch caught the broken layout before main - rollback was not touching production.
- New inbound play ran in scrimmage Tuesday before Friday's game - point guard reverted to last week's call at halftime without reinventing.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| alternative | [[Preparedness]] | Rehearse on a slice vs rehearse the undo drill on paper |
| contradicts | [[Ship It]] | when blasting to everyone beats waiting for the small-slice signal |
| extends | [[Reversibility]] | Small blast radius makes undo cheap |
| extends | [[Risk Management]] | Limit exposure before you bet the whole lane |
| extends | [[Rollback Principle]] | Staged slice is where you practice undo before everyone's affected |
| extends | [[Safety by Design]] | Fewer people hit before the hazard is proven safe |
| implements | [[Free Tier Hosting Stack]] | PR preview deploy before Pages merges to main |

## See also

- [[Build a Reliable Default]] - Systems Thinking
- [[Hierarchy of Controls]] - Safety, Systems Thinking
- [[The Garage Concept]] - Website Building
