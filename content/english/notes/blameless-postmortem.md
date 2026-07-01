---
title: "Blameless Postmortem"
meta_title: "Blameless Postmortem - Learn System Causes After Calm Returns"
description: "After rollback restores service, learn what broke in the system - not who to punish for pushing deploy."
date: 2026-07-01T14:00:00+08:00
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["Safety", "Leadership", "Continuous Improvement", "Systems Thinking"]
slug: "blameless-postmortem"
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "Bad Friday deploy reverted by lunch. When does root-cause talk start?"
    back: "Monday postmortem - not while users are down"
  - front: "Deploy debrief and the room hunts for who merged. What's the move?"
    back: "Name the process gap - not the fall guy"
  - front: "Cart tipped twice - debrief names the hazard. What's the move?"
    back: "Fix layout - not \"trainer was clumsy\""
  - front: "Near-miss last week and nobody wrote it up. What's missing?"
    back: "Blameless postmortem before the third time"
draft: false
aliases: ["postmortem", "blameless review"]
---
After rollback restores service, learn what broke in the system - not who to punish for pushing deploy.

## Key Concept

[[Rollback Principle]] gets users back on the old build; blameless postmortem gets judgment back.

Same shape as [[Incident Investigation]] - trace system causes - but the culture rule is no scalpel hunts for a fall guy. [[Own the Error]] still means someone says "my call" in standup; the room fixes the runbook, not the person.

## Examples

- Bad Friday deploy reverted by lunch - Monday postmortem traced the missing env var check, not which intern merged.
- After the equipment cart tipped twice we changed storage layout - debrief named the hazard, not "trainer was clumsy."

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| alternative | [[Rollback Principle]] | Rollback first; postmortem after calm - not root-cause while users are down |
| contradicts | [[Normalization of Deviance]] | when "nobody died" ends the conversation without a postmortem |
| extends | [[Convert Pain Into Learning]] | Postmortem is the scheduled convert step after harm |
| extends | [[Failure as Feedback]] | Miss becomes signal when nobody's hiding to keep their job |
| extends | [[Incident Investigation]] | Blameless tone keeps investigation on system causes |
| extends | [[Learning Organizations]] | "What broke" line stays until fixed or accepted |
| extends | [[Own the Error]] | Leader names the miss; room fixes the process, not the person |

## See also

- [[Heed Every Near-Miss]] - Safety, Systems Thinking
- [[Preparedness]] - Leadership, Systems Thinking
- [[Standard Operating Procedures]] - Safety, Systems Thinking
