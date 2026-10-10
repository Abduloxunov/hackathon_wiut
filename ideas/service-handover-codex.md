---
name: Service Handover Guard
added_by: Bexruz + codex, refining team intake/handover/capture ideas
date: Sat 10 Oct 2026
direction: dealer/service operations
mode: "Partner product: proposed Royal Motors service-reception unit"
---

# Service Handover Guard

**One line:** Guided arrival and departure car images → corresponding-panel comparison and evidence gaps → retake or human review before handover.

## Problem and user

A customer notices a mark after collecting a serviced car. The reception team needs an organised record of what was visible at intake. Existing photographs may omit an area or be too blurry to compare. Frequency, dispute cost and review time at Royal Motors are unverified hypotheses.

- User/owner: service-reception advisor and handover reviewer.
- Proposed payer: Royal Motors aftersales department; no partner commitment.
- [Dealerware's July 2026 documentation](https://support.dealerware.com/hc/en-us/articles/53458053275283-Vehicle-Walkaround-Inspection) describes guided zones, photo comparison and reports, and states that automatic AI damage detection is not in that initial release. This establishes a workflow and one supplier's scope, not a globally unique gap.
- Credits: claude-1's Handover Diff; claude-2's LensCheck; Bexruz's Workshop Intake screenshot.

## What the product does

1. Advisor captures required supported exterior zones; the app checks quality and coverage.
2. Departure capture follows the same zones with view guidance.
3. The app pairs corresponding views and attempts alignment.
4. It shows possible changed regions with side-by-side evidence, or asks for a retake.
5. A human confirms the report before closing handover.

- Input: paired supported panel images and a declared vehicle/case identifier. No customer records or plate reading are needed for the prototype.
- Output: possible change, no supported visible change, missing view, unalignable view or review required. "No visible change" is not an all-clear for hidden damage.
- Live jury test: fresh permitted paired photos; change camera angle/lighting, omit a view, or use a labelled controlled visible change. Controlled sample panels are disclosed and do not prove real-car performance.
- Boundary: no blame assignment, repair cost, accident history or mechanical/structural certification.

## Tech (why it is a system, not one API call)

Quality/exposure gate → zone/panel localisation → reference-view matching → feature correspondence and alignment with confidence → supported local change analysis → coverage/uncertainty rules → evidence report. An optional language model may explain computed findings; it does not decide what changed by itself.

Reflection, cleaning, dirt and camera movement can create apparent changes. Alignment failure must return uncertain/retake rather than produce a damage score. Perspective/image scale alone must not become physical damage area or depth without calibration.

- Data needed: own authorised matched car captures, unchanged pairs under varied conditions, labelled visible changes and mismatched-view negatives. None is available yet. Exterior-part public images may support localisation but cannot validate paired comparison. Code/weights need separate licence verification.
- Proposed inference: server, initially evaluate CPU for bounded photo cases; GPU only if benchmarking justifies it. Hardware, speed and cost are unmeasured.
- Local/night/rain: evaluate local vehicles, glossy finishes, actual low light/wet panels and glare separately; unsupported conditions remain not evaluated. No unconsented faces/plates.
- Public demo: browser capture/upload → server processing → annotated evidence/retake page from submitted repo.

## Quality and validation

Split by car/panel and capture session. Measure false change flags on unchanged pairs, detection of labelled supported changes, view-pairing and alignment success, correct retake decisions, reviewer time and total case latency. Compare with manual side-by-side review and a basic aligned image-difference baseline. Report sample counts and failure examples, not guessed accuracy.

## Why hard to copy

Potential future advantage: matched local evidence, calibrated uncertainty and workflow integration. Basic damage detection and comparisons already exist. No proprietary dataset or defensible moat has been established.

## Business

- Proposed pricing: site subscription or completed handover case; amount unverified.
- Cost per case: inference/storage/network + human review/retake labour; use [shared cost model](cv-shortlist-codex.md#shared-pilot-cost-model).
- Value to validate: case review time, incomplete-record rate and evidenced dispute/revisit work. Do not claim an assumed dispute-reduction percentage.
- Three-month pilot: first secure permissions/checklist and baseline; then shadow-review matched cases; finally supervised use with an operational comparison. Integration and buyer approval remain unconfirmed.

## Can we build it in ~8 h?

Conditional scope: a small supported zone set, guided photo upload, matching/alignment gates, one visible-change category and report. Biggest blocker is matched real imagery; biggest technical risk is reflections/viewpoint variation. Select only after fresh-pair feasibility tests. No build is approved by this proposal.

## Comments
<!-- Other agents may append comments. -->
