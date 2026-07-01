---
title: "Rollback Principle"
meta_title: "Rollback Principle - Undo Before You Push, Revert Before You Debug"
description: "Know how to restore the last good state before you ship - and call rollback first when the new state breaks."
date: 2026-06-30T12:48:40+08:00
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["Systems Thinking", "DevOps", "Safety", "Performance", "Leadership"]
slug: "rollback-principle"
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
aliases: ["rollback", "revert first"]
---
Know how to restore the last good state before you push - and when the new state breaks, revert first, debug second.

## Key Concept

If I can't explain the path back in one sentence, I'm not ready to ship.

[[Reversibility]] is the decision frame; rollback is the rehearsed move. Last quarter I kept a bad Friday deploy live because I wanted the milestone more than the rollback conversation - the team needed "my call, here's the fix," not a speech.

## Examples

- Bad Friday deploy - I reverted in standup, said my call, fixed Monday. Users got the old build before lunch; postmortem waited until the site was calm.
- The restaurant tried a new sauce but kept the old batch in the warmer until the first table cleared their plates - rollback was ladles, not a meeting.
- We tried a stricter screen-time rule and left the old routine on the fridge for a week - Tuesday meltdowns meant revert that night, not "give it two more weeks."
- The point guard ran Tuesday's inbound at halftime when the new play bled points - rollback was the drill they'd already walked, not a whiteboard invention.

## Note Relationships

| Relationship | Wikilink | Reason |
|--------------|----------|--------|
| alternative | [[Failure as Feedback]] | Rollback is move first; root-cause learning comes after the site is calm |
| contradicts | [[Ship It]] | when milestone pride blocks calling rollback Friday night |
| contradicts | [[Sunk Cost Fallacy]] | when "we already deployed" blocks undoing a bad release |
| extends | [[Build a Reliable Default]] | Rehearsed rollback is the default when deploys go loud |
| extends | [[Own the Error]] | Revert fast, name it in the standup, fix after calm returns |
| extends | [[Preparedness]] | Practice the undo path before the alarm owns the clock |
| extends | [[Reversibility]] | Concrete undo path - not only "prefer reversible choices" |
| extends | [[Risk Management]] | Named rollback is a control layer before irreversible harm |
| extends | [[Standard Operating Procedures]] | Rollback steps belong in the runbook, not in someone's head |
| implements | [[Free Tier Hosting Stack]] | Git revert and previous Cloudflare deploy are the rollback lane |

## See also

- [[Hierarchy of Controls]] - Safety, Systems Thinking
- [[Normalization of Deviance]] - Leadership, Safety
- [[Safety by Design]] - Safety, Systems Thinking
