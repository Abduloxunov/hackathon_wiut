---
name: Repair Evidence Review
added_by: Bexruz + codex
date: Sat 10 Oct
direction: vehicle inspection / service ops
mode: partner product (proposed BYD Royal Motors aftersales quality-control unit)
---

# Repair Evidence Review

**One line:** Requested visible bodywork repairs + before/after panel photos → evidence coverage, visible-change flags and review/retake decisions before a repair case is closed.

## Problem and user
- User: aftersales quality reviewer; proposed payer/owner: BYD Royal Motors aftersales. Local demand and process access are unverified.
- [BYD Royal Motors](https://byd-rm.uz/service) documents a local repair/service operation. [Tractable/Warta](https://tractable.ai/tractables-ai-to-give-warta-total-oversight-of-its-auto-repair-network/) documents visual-AI repair-network review as prior art. Neither proves our customer's review costs.

## What the product does
- Input: structured repair checklist and corresponding panel images before/after.
- Output: requested region with visual evidence, unchanged-looking region, missing view or uncertain/retake. A reviewer decides whether to close the case.
- Live jury test: supply fresh paired photos, change the requested region, omit a view or deliberately mismatch angles.
- Boundary: visible evidence review does not certify mechanical repair, paint quality or roadworthiness.

## Tech (why it is a system, not one API call)
- Quality gate → panel/region match → registration with confidence threshold → local change analysis → checklist coverage → evidence report. Low alignment confidence must stop change scoring.
- Data today: own authorised panel samples or consented car close-ups, with labelled changed/unchanged regions. Actual matched repair imagery is not yet available. Synthetic defects/sample panels are declared separately and cannot prove repair performance. Model/weight licences need verification before selection.
- Proposed inference: server; CPU versus GPU depends on chosen pipeline. Speed, hardware and cost are unmeasured.
- Night/rain/local cars: evaluate separate real captures and reflection/cleaning negatives; unavailable conditions remain untested. No plate recognition.
- Test: held-out panels/cars and sessions; false change flags, labelled visible-change detection, alignment failures, evidence coverage and reviewer time.

## Why hard to copy
- Potential future advantage: matched local repair evidence, calibrated failure handling and integration into case closure. None exists yet.
- Related to claude-1's Handover Diff, but the decision is requested-repair evidence coverage rather than attribution of new damage. Basic before/after comparison is established prior art.

## Business
- Proposed billing: service-site subscription or per reviewed case; price unverified.
- Cost per case: compute/storage + review/retake labour. Pilot ROI needs baseline review time and actual rework figures; no savings claim yet.
- Three-month pilot: agreed checklist and permissions → shadow review of labelled cases → supervised use with time/error comparison. Integration and partner participation unconfirmed.

## Can we build it in ~8 h?
- Conditional MVP: one visible repair category, guided matched views, one-region comparison and evidence report.
- Biggest risk: no real matched imagery; glare and camera changes could dominate the signal. Do not select until a feasibility check works on new real pairs.

## Comments
<!-- other agents may append comments -->
