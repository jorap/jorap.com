---
title: "Webhooks"
meta_title: "Webhooks"
description: "The server pings my app when something happens - push the event instead of polling every minute."
key_concept: |
  HTTP callbacks when something happens - push events instead of polling.
  
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
    reason: "Callbacks are one pipe in a personal API"
slug: "webhooks"
date: "2026-06-22 06:00:00+00:00"
image: "/images/note.jpg"
categories: ["Productivity"]
author: "JoRap"
tags: ["PKM", "Tools"]
featured: false
review: true
card_sets: ["Focus", "Review"]
cards:
  - front: "Refreshing the form inbox every five minutes waiting for submissions."
    back: "Webhook on submit - push, don't poll."
  - front: "Front desk keeps polling for new appointment submissions."
    back: "Webhook to calendar - instant on submit."
  - front: "Bus tracker tab open again - school alert should tell me when it's late."
    back: "Webhook to my phone - close the tab."
  - front: "Manager refreshing RSVP page every ten minutes before the event."
    back: "Webhook to team chat - push on submit."
draft: false
---
