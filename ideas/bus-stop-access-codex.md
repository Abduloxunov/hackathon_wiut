---
name: Bus-Stop Access Monitor
added_by: Bexruz + codex
date: Sat 10 Oct 2026
direction: driver/road safety
mode: "Startup: transit-stop operations review service"
---

# Bus-Stop Access Monitor

**One line:** Fixed-camera stop video + configured boarding/curb-access region → vehicle-obstruction episodes and evidence → operator review task.

## Problem and user

Vehicles occupying a boarding/access area can make it harder for a bus to reach the curb and for passengers to board. Whether this is frequent at a proposed local site and how staff respond need observation; no local frequency or injury claim is established.

- User: transit-stop/route supervisor or municipal transport operator.
- Proposed payer: transit/municipal stop-management team; no contract or footage permissions.
- [FTA stop-design guidance](https://www.transit.dot.gov/research-innovation/stops-spacing-location-and-design) discusses boarding/alighting flow. This is problem context, not Uzbekistan's legal standard.
- [Axis scenarios](https://www.axis.com/en-us/products/axis-object-analytics/scenarios) already provide occupancy/time-in-area/direction analytics. Object detection plus a timer alone has a weak originality case.

## What the product does

1. Operator configures a visible boarding/curb-access region in a fixed-camera view.
2. App detects/tracks vehicles and evaluates supported stationary occupancy of that region.
3. Combines repeated frames into one obstruction episode with start/end evidence.
4. Optionally associates supported bus arrivals after that stage is validated.
5. Shows a review task and report of confirmed obstruction time/recurring episodes.

- Input: supported fixed-camera video and openly human-configured region/rules. No automatic legal-zone inference from arbitrary footage.
- Output: possible obstruction, evidence timestamps/clip, clear/uncertain view and operator task. Items hidden from view are not assumed absent.
- Live jury test: new supported clip, region selection, clear/blocked cases, a moving vehicle, a bus legitimately using the stop and an occluded view. Results are computed, not prelabelled per video.
- Boundary: no plate reading/fines, passenger identity, unsafe-boarding conclusion unless an actual supported event is visible, or automatic traffic control.

## Tech (why it is a system, not one API call)

Scene/quality gate → vehicle detection/tracking → region association with ground-contact geometry when needed → stationary-time and bus-role rules → temporal deduplication/uncertainty → evidence/task/report. Bounding-box overlap is not enough to establish obstruction in perspective views. Legitimate boarding buses must not become blocking-car alarms. Episode closure requires adequate visible evidence.

- Data needed: authorised stop clips with independently labelled occupancy, clear periods, moving vehicles, buses and occlusion. None is available yet. Controlled private-premises footage with consenting adults/authorised vehicles can test pipeline logic, separately from real-stop results. Do not assume filming passengers/children/plates is allowed. Model code/weights need licence verification.
- Proposed inference: server; CPU/GPU chosen after a benchmark of short clips. Hardware, speed and camera-month cost unmeasured. State resolution, sampling and latency.
- Local/night/rain: test actual local bus/car types, headlights, wet reflections, dense traffic and partial views separately. Conditions without data remain not evaluated; low-quality intervals yield uncertainty.
- Public deployment: browser video upload/region setup → server CV/event logic → evidence report from submitted repo. Real-time roadside alerts are future scope needing field/latency validation.

## Quality and validation

Hold out full clips/sites and independently label episode boundaries. Measure missed obstruction episodes, false alerts, duration error, duplicate/split episodes, correct treatment of buses/moving vehicles, uncertain-view handling and reviewer time. Compare detection-and-timer baseline against region geometry, role rules and deduplication. A short demo does not establish prevented crashes.

## Why hard to copy

Potential future advantage: local scene labels, validated geometry/role handling and operator evidence-to-resolution workflow. No current moat; generic zone alerts already exist. Demonstrate a specific improvement over simple occupancy rules before claiming originality.

## Business

- Proposed billing: monitored stop/camera-month or audited route; amount unverified.
- Cost includes video processing/retention, site/camera setup, rule maintenance and operator review; see [shared cost model](cv-shortlist-codex.md#shared-pilot-cost-model).
- Validate review time, useful confirmed episodes and response workflow. Do not assume monetary value for reduced injuries or issue fines as revenue.
- Three-month pilot: permissions/site/rules and baseline → shadow review → supervised operator task workflow. Buyer participation, camera access and enforcement responsibility are unconfirmed.

## Can we build it in ~8 h?

Conditional MVP: one fixed view, openly marked region, vehicle tracking, obstruction episodes and evidence report. Bus-arrival association is optional after the basic flow works. Biggest blockers are scene access and labels; biggest risks are perspective, occlusion and confusing legitimate buses with obstructions. Clear operational scope, but lower technical/originality potential than a validated crossing-conflict system. No implementation selected.

## Comments
<!-- Other agents may append comments. -->
