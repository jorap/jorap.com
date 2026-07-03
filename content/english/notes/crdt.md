---
title: "CRDT"
meta_title: "CRDT"
description: "CRDTs let two offline devices merge edits without me picking last-write-wins by clock alone."
key_concept: |
  Conflict-free replicated data types (CRDTs) let two devices edit the same note without picking a winner by timestamp alone.
  
  [[Local-first Software]] wants merge-without-master; they're one way to get there.
examples:
  - "Two phones edited the grocery list offline; both merged without picking a winner by clock."
  - "Camp notes synced from two laptops after the hike - no \"your version lost\" fight."
relationships:
  - type: contradicts
    wikilink: "[[Building a Personal API]]"
    reason: "when the opposite frame fits better"
  - type: extends
    wikilink: "[[Local-first Software]]"
    reason: "Merge without a master server"
slug: "crdt"
date: "2026-06-22 06:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["PKM", "Tools"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "My wife and I edited the grocery list on two phones offline and both items stayed"
    back: "no \"your version overwrote mine\" argument in aisle."
  - front: "Two coaches edited the same lineup offline at a tournament and both changes merged"
    back: "No \"you must sync first\" fight at the bench"
  - front: "Two shift leads updated the patient board offline and both notes merged when Wi‑Fi came back"
    back: "No lost pass-off over who synced last"
  - front: "Two phones edited the same list offline and both changes merged"
    back: "No \"you must sync first\" fight"
draft: false
---
