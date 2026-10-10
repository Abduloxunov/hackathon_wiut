---
name: Driver Fatigue Guard
added_by: Muhammadjon + claude-2 (from Muhammadjon's AI-generated "master plan", cleaned; numbers removed)
date: Sat 10 Oct 15:10
direction: driver/road safety
mode: startup (fleets: taxi, logistics, intercity buses)
---

# Driver Fatigue Guard: in-browser drowsiness and phone-use alerts, no video leaves the device

**One line:** Cabin camera (phone or webcam) in → eye closure (PERCLOS), yawns, head nods, phone in hand, all computed **in the browser** → audible alert + incident log (no video stored) for fleet owners.

## Problem and user
- **User:** fleet driver; **payer:** fleet owner (taxi park, logistics, bus operator).
- **Evidence:** Uzbekistan had 2,203 road deaths in 2024 (see `_research-notes-claude2.md`); fatigue's share in Uzbekistan is **not found (unverified)**. The source plan's "-30% accidents" is invented; do not use it.

## What the product does
- **Input:** live webcam / phone front camera.
- **Output:** live state (alert / drowsy / distracted), siren, incident list with timestamps (landmark data only, no images, by default).
- **Live jury test:** excellent. The jury closes their eyes or picks up a phone in front of the laptop.

## Tech
- MediaPipe Face Landmarker (Apache-2.0) in JS → EAR / MAR, PERCLOS over a sliding window, head-pose nod; phone-in-hand via a small detector (COCO "cell phone" class); **per-driver calibration** in the first 10 s (handles glasses and eye shape); temporal rules to avoid alarms on blinks.
- **Night:** needs an IR camera in real vehicles; with a webcam in the dark it fails, which is an honest limitation.
- **Inference:** client-side (privacy), server only for the incident log.

## Why hard to copy
- **Weak.** This is the most commonly built CV hackathon demo (strategy doc lists "fatigue without tests on glasses, head turn, night" as a weak idea). It needs our own test protocol (glasses, sunglasses, head turns, low light) with measured false-alarm rates to score any innovation.

## Business
- Per vehicle per month; competes with dedicated DMS hardware (Mobileye, Seeing Machines, Chinese DMS cams). Price to validate.

## Can we build it in ~8 h?
- Yes, easily, but **low innovation score**. Keep it as a module (e.g. combined with fleet dashcam analytics), not as the main product.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
