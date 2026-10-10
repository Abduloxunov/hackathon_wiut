---
name: ChargeBay Watch
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 14:45
direction: EV/infrastructure
mode: partner product: BYD Royal Motors, EV charging / after-sales; or startup for charging-network operators
---

# ChargeBay Watch: is the charging bay free, and who is blocking it?

**One line:** CCTV frame or photo of a charging area in → per-bay state (free / EV charging / car parked but not plugged in / blocked by a non-EV) → live availability + "blocked bay" alert to the operator.

## Problem and user
- **User:** charging-network operator, dealer service lot, mall parking. **Payer:** the operator.
- **Evidence:**
  - Uzbekistan had 1,399 public chargers on 1 May 2025, 820 of them in Tashkent (2.5× growth in a year), with a target of 4,000 by end of 2026.
  - Every public parking lot must have an EV charging space (one source, unverified).
  - Bays blocked by non-charging cars are a known problem elsewhere ("ICE-ing"); in Tashkent it is still **unverified** (needs local evidence).

## What the product does
- **Input:** fixed-camera frame + a one-time bay layout (the operator draws bay polygons on the first frame).
- **Output:** bay state, occupancy timeline, "plugged in?" (cable or connector visible), alert for "occupied > N min without charging".
- **Live jury test:** the jury photographs any parking area; we draw bays in the UI and show states. Weaker than a real camera feed.

## Tech
- Vehicle detection + polygon overlap; cable/plug detection (small custom model on our own photos, the risky part); EV vs ICE via fine-grained model classification (BYD / Tesla / … via CLIP), unreliable, so it stays an amber signal.

## Why hard to copy
- Bay-geometry calibration workflow + time logic; integration with charger status APIs (OCPP) would be a real moat, but not in 8 h.

## Business
- $50–150 per site per month (hypothesis, from the strategy doc).

## Can we build it in ~8 h?
- Occupancy: yes. Plug detection and EV-vs-ICE: high risk. The demo depends on a camera scene, and **the jury input is weak**. Rated below TrueClaim and RoadProof.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
