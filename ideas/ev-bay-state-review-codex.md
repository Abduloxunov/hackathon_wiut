---
name: EV Bay Occupancy & Session Review
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: EV / infrastructure / automotive operations
mode: partner product (proposed BYD Royal Motors site operations)
---

# EV Bay Occupancy & Session Review

**One line:** A camera shows which charging bays are occupied; an authorised charger feed adds session state so an operator can review prolonged blocking or conflicting observations.

## Problem and user

A site operator needs to know whether a charging bay is usable. A parked car, a live charging session and a working charger are different facts. The dealership/site manager would use and potentially fund the product. The local frequency of blocked bays and the value of monitoring remain unverified; we have no site access or charger API today.

The [Open Charge Alliance's OCPP documentation](https://openchargealliance.org/protocols/open-charge-point-protocol/) establishes communication between chargers and charging-management systems. It supports a possible telemetry integration, not proof that a partner exposes a compatible feed or permits access. Camera-based parking counts alone have limited originality.

## What the product does

- **Input:** One fixed camera, operator-marked bay boundaries and optional permitted charger/session data.
- **Context data:** Bay-to-connector mapping, camera calibration, session/status timestamps, freshness limits, site grace period and operator review rules. Reservations or accessibility restrictions need real supplied records.
- **Output:** Occupied, visually clear or visibility unknown per bay; separately, session active/inactive/unknown from the feed. A timeline shows occupancy duration and the age of each observation.
- **Decision:** Ask a site worker to check a possible blocked bay or a camera/telemetry inconsistency. Show usable-space information only with explicit freshness and operating-status qualifications.

Example: the camera sees a car for a long time while a fresh authorised feed shows no active session. The app creates **review needed**, not an automatic misuse fine. A reservation, broken connector or waiting driver could explain it. If the feed is missing or stale, show **session unknown** and occupancy only.

## Tech and data

Pipeline: vehicle detection → geometric overlap with configured bays → tracking/temporal smoothing and occlusion handling → merge with fresh session data → apply declared dwell rules → operator queue. Decide how overlapping vehicles and partial visibility affect each bay; a hidden bay is not free. Initial model selection follows the [shared licence gates](refined-six-ideas-codex.md).

Camera pixels cannot reliably establish energy flow, charger health, account authorisation or EV-versus-ICE status for every vehicle. Seeing a cable is insufficient proof of charging. State explicitly which facts come from CV and which come from external records. A protocol simulator may test the state-fusion logic, but must be visibly labelled synthetic and is not a real charger integration.

Collect authorised footage of one actual bay layout, including empty/occupied transitions, adjacent traffic and occlusion. Use a private consented setting without identifiable nonconsenting faces/plates. No footage has been acquired. A tabletop/model-car demonstration can exercise geometry only, not real-site detection. Save permitted source/collection terms, model/weight licences and any status-feed permissions. OCPP's existence does not grant access to operational data.

## Evaluation and real conditions

Measure occupancy accuracy per bay, false free/occupied states, unknown coverage, dwell-duration error and false review events per camera-hour. Compare frame-only detection with temporal logic. Test moving shadows, headlights, rain, night, tall vehicles hiding neighbouring bays and a moved camera. For fusion, test stale, missing, delayed and incorrectly mapped feed messages; use actual logs for integration claims, declared simulated logs for logic tests.

Run initial video inference on a server. Record input resolution/rate, frames processed, warm/cold latency, upload cost and camera-hour cost on actual hardware. Edge processing is a later measured option. Local Toyota/BYD shapes and night performance are untested; plates are unnecessary. There are no current performance results.

## Business and pilot

Possible pricing: per monitored site/camera. Budget camera installation/network, layout setup, charger-system integration, licensing, annotation, compute/storage, maintenance and staff review. Measure worker walk/check time and confirmed bay-blocking duration. Count additional charging revenue only if real utilisation records demonstrate it; occupied hours are not automatically lost sales. Apply the [shared business protocol](refined-six-ideas-codex.md).

Three-month pilot: obtain site and data permissions, calibrate one layout, run alongside manual checks, then audit confirmed events and maintenance costs. The possible advantage is reliable camera/session reconciliation with a useful site workflow. Without authorised telemetry, this is a simpler occupancy product and should receive a lower innovation assessment.

## Can we build it in ~8 h?

Conditional MVP: uploaded fixed-camera clip, configurable bay polygons, occupancy timeline and operator review. Add explicitly synthetic session messages only to demonstrate fusion rules; do not present them as live charger data. The jury can upload a new permitted clip and mark its bays. No traffic-light control, charger switching, plate identification or fines are needed.

This refines ChargeBay Watch and EV Bay Guard from the team. Keep charger hardware-fault diagnosis as a separate future investigation rather than promising it from a camera.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
