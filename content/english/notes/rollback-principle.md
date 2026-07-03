---
title: "Rollback Principle"
meta_title: "Rollback Principle - Undo Before You Push, Revert Before You Debug"
description: "Restore the last good state before you push - when the new state breaks, revert first, debug second."
key_concept: |
  If I can't explain the path back in one sentence, I'm not ready to ship.
  
  [[Reversibility]] is the decision frame; rollback is the rehearsed move. Last quarter I kept a bad Friday deploy live because I wanted the milestone more than the rollback conversation - the team needed "my call, here's the fix," not a speech.
examples:
  - "Bad Friday deploy - I reverted in standup, said my call, fixed Monday. Users got the old build before lunch; after-action review waited until the site was calm."
  - "The point guard ran Tuesday's inbound at halftime when the new play bled points - rollback was the drill they'd already walked, not a whiteboard invention."
shareable_lines:
  - "Restore the last good state before you push - when the new state breaks, revert first, debug second."
  - "If I can't explain the path back in one sentence, I'm not ready to ship."
  - "Reversibility is the decision frame; rollback is the rehearsed move. Last quarter I kept a bad Friday deploy live because I…"
relationships:
  - type: alternative
    wikilink: "[[Blameless After-Action Review]]"
    reason: "Rollback first; after-action review after calm - not root-cause while users are down"
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
categories: ["Leadership"]
author: "JoRap"
tags: ["Systems Thinking", "DevOps", "Safety", "Performance", "Leadership"]
aliases: ["rollback", "revert first"]
featured: false
review: true
card_sets: ["Ethics", "Focus"]
cards:
  - front: "Bad Friday deploy. What's the move? One check?"
    back: "Revert first - after-action review when calm."
  - front: "New sauce on the menu but old batch still in the warmer. Why?"
    back: "Rollback ready - ladles not meetings."
  - front: "Stricter screen-time rule tried but old routine still on the fridge. Why?"
    back: "Keep undo path - not two more weeks."
  - front: "New play bled points at halftime - Tuesday's inbound ready. Move?"
    back: "Run the drill we already walked."
draft: false
---
