---
name: SmartFlow AI (adaptive traffic-light recommendations)
added_by: Muhammadjon + claude-2 (from Muhammadjon's "SmartFlow AI Full Guide"; cleaned + re-scoped for the CV track)
date: Sat 10 Oct 15:50
direction: driver/road safety (city traffic). The task lists "traffic events that continue your elimination task"
mode: startup (B2G: city traffic management / Tashkent traffic centre, integrators)
---

# SmartFlow AI: junction video → queues per approach → recommended green split

**One line:** Junction camera video in → vehicle detection + tracking → queue length, waiting time, arrivals per approach → **recommended** phase / green-time split with safety limits, plus a SUMO simulation that compares fixed-time vs adaptive on the same demand. **Advisory only: it never controls a real signal.**

## ⚠️ Fit with this hackathon: read first
The source guide puts **SUMO simulation first and CV last** ("add CV only if time remains"). For a **Computer Vision** track judged on the jury's own input, that order is risky:
- if the CV module is missing, it is a traffic-control project, not CV;
- the jury can't hand us an intersection; they can only upload a junction video;
- SUMO on a public web host is heavy (native binary, long runs).

**Re-scope proposal:** make the **CV queue estimator** the core (jury uploads any junction clip → queues per drawn approach lane → recommended split + explanation), and use SUMO only offline to measure the controller (fixed vs adaptive, same seeds), with the results shown as charts. This also connects to claude-1's *Junction Risk Map* (re-uses our elimination-stage tracking code).

## Problem and user
- Fixed-time signals give green to an empty approach while the queue grows on another (hypothesis; there is no Tashkent data yet).
- **User / payer:** city traffic management, road-infrastructure operators, integrators. Demand must be checked through interviews.

## Pipeline
1. **CV:** video → YOLO (vehicle classes) → ByteTrack → per-approach polygons / stop lines → queue length (stopped tracks), waiting time, arrival rate.
2. **Controller (rule-based, explainable, no RL):** `priority = a·queue + b·wait + c·arrivals`, with coefficients tuned and tested, not universal.
3. **Safety constraints:** min/max green, yellow, all-red clearance, pedestrian phases, no conflicting greens, max wait cap (fairness).
4. **Simulation (offline):** SUMO + TraCI on one junction; scenarios: normal, one-sided jam, surge; several seeds.
5. **Dashboard:** video with boxes + queues per approach, current/next phase with a reason that matches the code, fixed-vs-SmartFlow metric charts.

## Metrics (only from real runs)
- CV: count / queue-length error vs hand-counted frames.
- Control (SUMO): mean delay, mean/max queue, wait per approach (fairness), stops per vehicle, throughput. Same routes and seeds for both modes; report settings, duration and repeats; **if there is no improvement, say so**.

## Never claim
"X% fewer jams" without measurement; ready for city roads; no accidents; any weather. Real deployment needs permits, traffic engineers, certified controllers and fail-safe modes.

## Why hard to copy
- Our own tracking pipeline from the elimination stage + calibrated queue estimation + a reproducible simulation benchmark. Adaptive signals in general are a well-known topic (SCOOT/SCATS and many student projects), so **innovation is moderate**.

## Can we build it in ~8 h?
- CV queue estimator + rule controller + dashboard: yes. A full SUMO comparison is also possible, but both together are tight.
- **Risks:** weak jury input; simulation ≠ reality; heavy deploy; moderate innovation. Ranked below TrueClaim / TyreCheck / RoadProof by claude-2.

## Resources
[SUMO docs](https://sumo.dlr.de/docs/) · [SUMO traffic lights](https://sumo.dlr.de/daily/userdoc/Simulation/Traffic_Lights.html) · [TraCI tutorial](https://github.com/eclipse-sumo/sumo/blob/main/docs/web/docs/Tutorials/TraCI4Traffic_Lights.md?plain=1) · [Ultralytics tracking](https://docs.ultralytics.com/modes/track/). Check licences: SUMO is EPL-2.0, YOLO AGPL-3.0.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
