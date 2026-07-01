---
title: "Rollback Principle"
meta_title: "Rollback Principle - Undo Before You Push, Revert Before You Debug"
description: "Know how to restore the last good state before you push - and when the new state breaks, revert first, debug second."
key_concept: |
  If I can't explain the path back in one sentence, I'm not ready to ship.
  
  [[Reversibility]] is the decision frame; rollback is the rehearsed move. Last quarter I kept a bad Friday deploy live because I wanted the milestone more than the rollback conversation - the team needed "my call, here's the fix," not a speech.
examples:
  - "Bad Friday deploy - I reverted in standup, said my call, fixed Monday. Users got the old build before lunch; postmortem waited until the site was calm."
  - "The point guard ran Tuesday's inbound at halftime when the new play bled points - rollback was the drill they'd already walked, not a whiteboard invention."
relationships:
  - type: alternative
    wikilink: "[[Blameless Postmortem]]"
    reason: "Rollback first; postmortem after calm - not root-cause while users are down"
  - type: alternative
    wikilink: "[[Failure as Feedback]]"
    reason: "Rollback is move first; root-cause learning comes after the site is calm"
  - type: contradicts
    wikilink: "[[Ship It]]"
    reason: "when milestone pride blocks calling rollback Friday night"
  - type: contradicts
    wikilink: "[[Sunk Cost Fallacy]]"
    reason: "when \"we already deployed\" blocks undoing a bad release"
  - type: extends
    wikilink: "[[Build a Reliable Default]]"
    reason: "Rehearsed rollback is the default when deploys go loud"
  - type: extends
    wikilink: "[[Change Window]]"
    reason: "Risky push only when revert crew is reachable"
  - type: extends
    wikilink: "[[Own the Error]]"
    reason: "Revert fast, name it in the standup, fix after calm returns"
  - type: extends
    wikilink: "[[Preparedness]]"
    reason: "Practice the undo path before the alarm owns the clock"
  - type: extends
    wikilink: "[[Reversibility]]"
    reason: "Concrete undo path - not only \"prefer reversible choices\""
  - type: extends
    wikilink: "[[Risk Management]]"
    reason: "Named rollback is a control layer before irreversible harm"
  - type: extends
    wikilink: "[[Staged Rollout]]"
    reason: "Small slice first keeps rollback cheap before everyone's affected"
  - type: extends
    wikilink: "[[Standard Operating Procedures]]"
    reason: "Rollback steps belong in the runbook, not in someone's head"
  - type: implements
    wikilink: "[[Free Tier Hosting Stack]]"
    reason: "Git revert and previous Cloudflare deploy are the rollback lane"
slug: "rollback-principle"
date: "2026-06-30 12:48:40+08:00"
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["Systems Thinking", "DevOps", "Safety", "Performance", "Leadership"]
aliases: ["rollback", "revert first"]
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "Bad Friday deploy. What's the move? One check?"
    back: "Postmortem waited until the site was calm"
  - front: "The restaurant tried a new sauce but kept the old batch in the warmer until the first table cleared their plates"
    back: "Rollback was ladles, not a meeting"
  - front: "We tried a stricter screen-time rule and left the old routine on the fridge for a week"
    back: "Not \"give it two more weeks.\""
  - front: "The point guard ran Tuesday's inbound at halftime when the new play bled points"
    back: "Not a whiteboard invention"
draft: false
---
