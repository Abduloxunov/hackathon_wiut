---
name: LensCheck
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 14:45
direction: vehicle inspection
mode: startup (insurers, dealers, service centres). Could also be partner product: Toyota Royal Motors service intake
---

# LensCheck: inspection photo-set quality and completeness check

**One line:** A set of car-inspection photos in → per-photo quality (blur, exposure, glare, duplicates) + angle coverage (front, rear, left, right, 4 corners, odometer, VIN plate) → "complete / retake these 3 shots", before the set goes to an inspector or insurer.

## Problem and user
- **User:** service-intake advisor, insurance agent, used-car buyer. **Payer:** the organisation doing the inspections.
- **Why:** incomplete or bad photo sets cause repeat visits and disputes at handover, trade-in and claims. Trade-in through dealers is now formalised (PKM-535, 22 Aug 2025), so more photo inspections are expected (inference).
- Evidence still to collect: interview a service advisor at Toyota / BYD Royal Motors about repeat-inspection rates.

## What the product does
- **Input:** 4–12 photos from a phone.
- **Output:** checklist of required angles (✔ / missing), per-photo issues with a reason ("too dark", "motion blur", "same angle as #3"), completeness score, a retake list.
- **Live jury test:** the jury takes 4–6 photos of any car (or a toy car or a car picture); we show what is missing or bad.

## Tech
- OpenCV for blur, exposure and glare; pHash for duplicates; **viewpoint classifier** (CLIP zero-shot prompts "front of a car", "rear-left corner of a car", … then a small linear probe on our own labelled shots); detector to check a car is present and centred.
- **Data:** our own phone photos of team members' and volunteers' cars (no plates, or plates blurred); public car-view sets if the licence allows.
- **Inference:** server CPU, about 100 ms per photo expected (to be measured).

## Why hard to copy
- Weak on its own: easy to rebuild. Its value is as the **first stage of TrueClaim / HandoverGuard** or as the **fallback** if damage detection fails.

## Business
- $50–200 per site per month (hypothesis). Value = fewer repeat inspections.

## Can we build it in ~8 h?
- Yes (strategy doc rates it 9/10). **This is the safe fallback.**
- **Risk:** low innovation score.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
