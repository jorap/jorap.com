---
title: "Change Window"
meta_title: "Change Window - Schedule Risky Changes When Rollback Help Is Awake"
description: "I ship risky changes when someone awake can roll back, not Friday night when everyone's offline."
key_concept: |
  [[Rollback Principle]] fails when the people who can revert are asleep or at a wedding.
  
  A change window is boring calendar hygiene: deploy Tuesday morning, freeze before holidays, keep the old build one click away. Not fear of shipping - matching risk to coverage. PKM parallel: [[Maintenance Window]] is scheduled garden prune; change window is scheduled production risk.
examples:
  - "We stopped Friday-night client deploys after the bad release - Tuesday standup owns rollback if it goes loud."
  - "Wedding weekend freeze: marketing edits queue, no Hugo version bumps until Monday."
shareable_lines:
  - "I ship risky changes when someone awake can roll back, not Friday night when everyone's offline."
  - "Rollback Principle fails when the people who can revert are asleep or at a wedding."
  - "A change window is boring calendar hygiene: deploy Tuesday morning, freeze before holidays, keep the old build one click away."
  - "PKM parallel: Maintenance Window is scheduled garden prune; change window is scheduled production risk."
relationships:
  - type: alternative
    wikilink: "[[Maintenance Window]]"
    reason: "PKM prune schedule vs production deploy schedule"
  - type: contradicts
    wikilink: "[[Ship It]]"
    reason: "when milestone pride ships Friday at 5:01"
  - type: extends
    wikilink: "[[Preparedness]]"
    reason: "Window assumes rehearsed undo path and someone on call"
  - type: extends
    wikilink: "[[Risk Management]]"
    reason: "Time-box exposure to staffed hours"
  - type: extends
    wikilink: "[[Rollback Principle]]"
    reason: "Risky push only when revert crew is reachable"
  - type: extends
    wikilink: "[[Standard Operating Procedures]]"
    reason: "Written deploy windows belong in the runbook"
slug: "change-window"
date: "2026-07-01 14:00:00+08:00"
image: "/images/note.jpg"
categories: ["Leadership"]
author: "JoRap"
tags: ["Safety", "DevOps", "Systems Thinking", "Leadership"]
aliases: ["deploy window", "release window"]
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
---
