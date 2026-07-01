---
title: "Webhooks"
meta_title: "Webhooks"
description: "HTTP callbacks when something happens - push events instead of polling."
key_concept: |
  Push events beat polling when the site needs to rebuild the moment content lands in git.
  
  [[Git-Based CMS]] and [[Free Tier Hosting Stack]] - push rebuild when markdown lands.
examples:
  - "New appointment hits the calendar the second the patient submits - webhook beats staff polling the inbox every five minutes."
  - "School alert webhook fires when the bus is late - push to my phone instead of refreshing the tracker tab."
relationships:
  - type: contradicts
    wikilink: "[[Local-first Software]]"
    reason: "when the opposite frame fits better"
  - type: extends
    wikilink: "[[Building a Personal API]]"
    reason: "Named in notes that link here"
slug: "webhooks"
date: "2026-06-22 06:00:00+00:00"
image: "/images/note.jpg"
categories: ["Ideas", "Tips"]
author: "JoRap"
tags: ["PKM", "Tools"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "Form submit hits my script instantly instead of me refreshing the inbox every five minutes"
    back: "HTTP callback when something happens"
  - front: "New appointment hits the calendar the second the patient submits"
    back: "webhook beats staff polling the inbox every five."
  - front: "School alert webhook fires when the bus is late. What's the move?"
    back: "push to my phone instead of refreshing the."
  - front: "RSVP form submission pings the team chat instantly. What's the move?"
    back: "push event instead of the manager refreshing the."
draft: false
---
