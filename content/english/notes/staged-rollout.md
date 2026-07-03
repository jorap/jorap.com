---
title: "Staged Rollout"
meta_title: "Staged Rollout - Ship to a Slice Before Everyone Is the Test"
description: "I ship to a small slice first so rollback stays cheap if the new state bleeds."
key_concept: |
  Full-blast deploy turns every user into a test subject.
  
  Staged rollout - preview branch, one table section, scrimmage Tuesday - keeps [[Reversibility]] real. [[Safety by Design]] at release time: harm hits fewer people before you commit the whole lane.
  
  I ship to a small slice first so rollback stays cheap if the new state bleeds.
examples:
  - "Cloudflare preview branch caught the broken layout before main - rollback was not touching production."
  - "New inbound play ran in scrimmage Tuesday before Friday's game - point guard reverted to last week's call at halftime without reinventing."
shareable_thought:
  - "I ship to a small slice first so rollback stays cheap if the new state bleeds."
  - "Full-blast deploy turns every user into a test subject."
  - "Staged rollout - preview branch, one table section, scrimmage Tuesday - keeps Reversibility real."
  - "Safety by Design at release time: harm hits fewer people before you commit the whole lane."
relationships:
  - type: alternative
    wikilink: "[[Preparedness]]"
    reason: "Rehearse on a slice vs rehearse the undo drill on paper"
  - type: contradicts
    wikilink: "[[Ship It]]"
    reason: "when blasting to everyone beats waiting for the small-slice signal"
  - type: extends
    wikilink: "[[Reversibility]]"
    reason: "Small blast radius makes undo cheap"
  - type: extends
    wikilink: "[[Risk Management]]"
    reason: "Limit exposure before you bet the whole lane"
  - type: extends
    wikilink: "[[Rollback Principle]]"
    reason: "Staged slice is where you practice undo before everyone's affected"
  - type: extends
    wikilink: "[[Safety by Design]]"
    reason: "Fewer people hit before the hazard is proven safe"
  - type: implements
    wikilink: "[[Free Tier Hosting Stack]]"
    reason: "PR preview deploy before Pages merges to main"
slug: "staged-rollout"
date: "2026-07-01 14:00:00+08:00"
image: "/images/note.jpg"
categories: ["Leadership"]
author: "JoRap"
tags: ["Safety", "Systems Thinking", "DevOps", "Risk Management"]
aliases: ["canary deploy", "gradual rollout"]
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "New layout ready on my branch. What's the deploy move?"
    back: "Preview branch - rollback doesn't touch production"
  - front: "New inbound play for Friday's game. When do we run it?"
    back: "Scrimmage Tuesday - revert at halftime if it bleeds"
  - front: "New screen-time rule for the whole house. What's the move?"
    back: "One kid one week - old routine on the fridge"
  - front: "New sauce for every table tonight. What stays in the warmer?"
    back: "Old batch until first table clears"
draft: false
---
