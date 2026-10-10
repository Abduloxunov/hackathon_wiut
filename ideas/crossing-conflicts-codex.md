---
name: Crossing Conflict Review
added_by: Bexruz + codex, refining claude-1 Junction Risk Map
date: Sat 10 Oct 2026
direction: driver/road safety
mode: "Startup: traffic-engineering review service"
---

# Crossing Conflict Review

**One line:** Supported fixed-camera crossing video + configured conflict zone → tracked interactions, candidate event timing and evidence clips → traffic-engineer review.

## Problem and user

Traffic engineers need to review interactions at a crossing and evaluate possible interventions. Watching long recordings manually can be slow. Local observation workload, demand and willingness to pay remain unverified.

- User: traffic-engineering consultant or municipal road-safety analyst.
- Proposed payer: consultancy/municipal traffic team; no pilot commitment or camera permissions.
- [VivaCity](https://info.vivacitylabs.com/near-miss-feature-smart-road-safety) describes trajectory-based CV near-miss analysis. This establishes competition; no claim of global novelty or proven crash reduction.
- Credits: claude-1's Junction Risk Map, Bexruz's Pedestrian Risk Analyzer. Elimination-stage code is a possible asset but has not been inspected or secured.

## What the product does

1. Analyst uploads a supported fixed-camera clip and marks the crossing/conflict region.
2. Defines camera/ground-plane setup needed for the supported timing calculation.
3. The app tracks road users and selects supported closely timed interactions.
4. Shows trajectories, timestamps, uncertainty and evidence clips.
5. Analyst confirms events; report includes observation duration and traffic exposure.

- Input: new fixed-camera video, configured region and required calibration. Moving dashcams are outside initial scope.
- Output: candidate event queue, zone timing, counts with denominators, processing information and unsupported/occluded intervals. A broad unvalidated risk score is excluded.
- Live jury test: new consent-compliant supported clip; jury selects region and tests a clip with no events or obstructed view. Manual scene setup is openly part of the product.
- Boundary: no legal fault, automatic fines, predicted crash probability or intervention-causality claim from a short clip.

## Tech (why it is a system, not one API call)

Video quality/frame-time checks → road-user detection → multi-object tracking → calibrated/configured conflict-zone timing → event/uncertainty rules → exposure aggregation → evidence queue. Track swaps, occlusion and uncertain ground positions suppress unreliable measures.

Post-encroachment time (PET) is the time between one road user leaving a conflict location and another reaching it. [FHWA's SSAM report](https://www.fhwa.dot.gov/publications/research/safety/08051/02.cfm) explains trajectory-based surrogate measures; its simulation method/historical defaults do not validate our camera estimates or a universal danger threshold. Pixel overlap alone is not physical conflict. Metric distances/speeds require verified geometry.

- Data needed: authorised clips with compliant people/vehicle consent, independently labelled events and timestamps, normal/no-event negatives, varied views and calibrated zones. None is currently available. Public CCTV availability alone is not permission. Controlled consenting-adult/synthetic scenes are declared and evaluated separately from field clips. No model/weight selected; verify licences.
- Proposed inference: server, CPU/GPU to be determined by actual detector/tracker/video benchmark. Speed, cost and hardware unmeasured. State resolution, frame sampling and upload limits.
- Night/rain/local traffic: evaluate actual local vehicles, pedestrians, occlusion, headlights and wet/night clips separately. Missing groups are not evaluated; frame interpolation cannot create field evidence.
- Deployment: public browser upload/scene setup → server pipeline → clips/report from submitted repo.

## Quality and validation

Hold out full clips/sites, not adjacent frames. Independently annotate events and zone timing. Measure event precision/recall, timing error, track swaps, false events per observation period, abstention and processing latency. Compare basic proximity/event logic with the calibrated timing pipeline. Before/after counts need comparable exposure; causal safety improvement needs a stronger study.

## Why hard to copy

Potential future advantage: validated local event labels, camera setup protocol, useful review output and reusable team code if accessible/attributed. These are not current moats. Existing near-miss vendors and detection/tracking libraries must be acknowledged.

## Business

- Proposed billing: per analysed site/camera-month or study; amount unverified.
- Cost includes inference, video retention, camera/setup, annotation and engineer review; use [shared model](cv-shortlist-codex.md#shared-pilot-cost-model).
- Validate analyst time per reviewed event and study usefulness; do not price assumed lives saved.
- Three-month pilot: permissions/site/ground truth and baseline → shadow event review → analyst-led study with operational comparison. Municipal procurement and intervention approval remain unconfirmed.

## Can we build it in ~8 h?

Only conditionally: one fixed view/event type, working tracker, configured zone, evidence clips and measured timing. Biggest blockers are footage and labelled/calibrated events; code reuse is not yet established. Technical potential is strongest among shortlisted road ideas, but readiness is unknown. No road-safety build selected.

## Comments
<!-- Other agents may append comments. -->
