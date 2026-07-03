---
title: "Blameless After-Action Review"
meta_title: "Blameless After-Action Review - Learn System Causes After Calm Returns"
description: "After rollback restores service, I learn what broke in the system - not who to punish for pushing deploy."
key_concept: |
  [[Rollback Principle]] gets users back on the old build; blameless after-action review gets judgment back.
  
  Same shape as [[Incident Investigation]] - trace system causes - but the culture rule is no scalpel hunts for a fall guy. [[Own the Error]] still means someone says "my call" in standup; the room fixes the runbook, not the person.
  
  After rollback restores service, I learn what broke in the system - not who to punish for pushing deploy.
  
  Fix the runbook after rollback - not the person who pushed deploy.
examples:
  - "Bad Friday deploy reverted by lunch - Monday after-action review traced the missing env var check, not which intern merged."
  - "After the equipment cart tipped twice we changed storage layout - debrief named the hazard, not \"trainer was clumsy.\""
shareable_thought:
  - "After rollback restores service, I learn what broke in the system - not who to punish for pushing deploy."
  - "Rollback Principle gets users back on the old build; blameless after-action review gets judgment back."
  - "Own the Error still means someone says \"my call\" in standup; the room fixes the runbook, not the person."
  - "Fix the runbook after rollback - not the person who pushed deploy."
relationships:
  - type: alternative
    wikilink: "[[Rollback Principle]]"
    reason: "Rollback first; after-action review after calm - not root-cause while users are down"
  - type: contradicts
    wikilink: "[[Normalization of Deviance]]"
    reason: "when \"nobody died\" ends the conversation without an after-action review"
  - type: extends
    wikilink: "[[Measure Then Iterate]]"
    reason: "After calm, learn what broke with something you'd track next time"
  - type: extends
    wikilink: "[[Convert Pain Into Learning]]"
    reason: "After-action review is the scheduled convert step after harm"
  - type: extends
    wikilink: "[[Failure as Feedback]]"
    reason: "Miss becomes signal when nobody's hiding to keep their job"
  - type: extends
    wikilink: "[[Incident Investigation]]"
    reason: "Blameless tone keeps investigation on system causes"
  - type: extends
    wikilink: "[[Learning Organizations]]"
    reason: "\"What broke\" line stays until fixed or accepted"
  - type: extends
    wikilink: "[[Own the Error]]"
    reason: "Leader names the miss; room fixes the process, not the person"
slug: "blameless-after-action-review"
date: "2026-07-01 14:00:00+08:00"
image: "/images/note.jpg"
categories: ["Leadership"]
author: "JoRap"
tags: ["Safety", "Leadership", "Continuous Improvement", "Systems Thinking"]
aliases: ["after-action review", "blameless review", "/notes/blameless-postmortem/"]
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "Bad Friday deploy reverted by lunch. When does root-cause talk start?"
    back: "Monday after-action review - not while users are down"
  - front: "Deploy debrief and the room hunts for who merged. What's the move?"
    back: "Name the process gap - not the fall guy"
  - front: "Cart tipped twice - debrief names the hazard. What's the move?"
    back: "Fix layout - not \"trainer was clumsy\""
  - front: "Near-miss last week and nobody wrote it up. What's missing?"
    back: "Blameless after-action review before the third time"
draft: false
---
