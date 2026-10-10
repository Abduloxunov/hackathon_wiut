---
name: DriveCoach — driver + road, risk in context
added_by: Davlatyor (team brainstorm) + claude-1 (technical research)
date: Sat 10 Oct 15:50
direction: driver / road safety
mode: startup (fleets, insurers, driving schools) — or partner product for Toyota/BYD Royal Motors fleet/after-sales
---

# DriveCoach — "are you driving right, right now?"

**One line:** camera on the driver + camera on the road → risk judged **in context** (eyes off road *while* the car ahead is close) → live alert + trip score + clips for the fleet owner / insurer.

Research split (10 Oct): **claude-1 = technical** (this file). **Davlatyor = market/users** (YouTube demos of Nauto/Samsara/Lytx/Netradyne, who pays in Uzbekistan) → add under "Market" below.

## Prior art — be honest, it exists
| Who | What | Method | Source |
|---|---|---|---|
| **CarSafe** (Dartmouth, 2012–13) | Same idea on an Android phone: front cam = drowsy/distracted, rear cam = following distance, lane weaving | Phones could not stream both cameras → **switched** between them, filled the blind gap with inertial sensors; ~8 fps; 12-driver trial, precision 83% / recall 75% | [MobiSys'13 PDF](https://www.cs.dartmouth.edu/~campbell/carsafe.pdf), [Dartmouth news](https://home.dartmouth.edu/news/2012/09/dartmouth-smartphone-app-targets-driver-safety) |
| **Nauto** | Dual-facing AI dashcam for fleets | Distraction logged separately from harsh events; alerts escalate with distraction length (2–5 s); "Predictive Fusion" of risks — method not published | [Nauto blog](https://www.nauto.com/blog/introducing-nauto-prevent), [CCJ](https://www.ccjdigital.com/business/article/14936954/in-cab-fleet-tech-nauto-prevent-monitors-distracted-driving), [FleetRabbit](https://fleetrabbit.com/blogs/post/nauto-ai-camera-integration) (vendor claims) |
| Samsara, Lytx, Netradyne | Fleet AI dashcams | (not re-checked today — Davlatyor's market research) | |
| Research: gaze × risk | Gaze fused with collision prediction; gaze mapped onto road actors | Scene-graph CNN with gaze → TTC per road user (CAC 2025) | [BIT](https://pure.bit.edu.cn/en/publications/a-visual-attention-informed-scene-graph-approach-for-predicting-r/), [VT](https://sanghani.cs.vt.edu/research-publication/driver-gaze-fixation-and-pattern-analysis-in-safety-critical-events) |

**So our novelty cannot be "two cameras".** It has to be: (1) **no hardware, runs in a browser link** (phones + laptop), (2) an **explicit, explainable context-risk model** (published rules + measured thresholds — Nauto's is a black box), (3) **local**: Tashkent taxi/delivery fleets, driving-school exam practice, Uzbek roads.

## Critical technical constraint (found today)
- **A phone browser cannot open front + rear camera at the same time.** iOS Safari kills the first track when the second is requested; Android browsers allow one stream at a time ([Dynamsoft](https://www.dynamsoft.com/codepool/getusermedia-multiple-camera.html), [WebKit bug 238492](https://bugs.webkit.org/show_bug.cgi?id=238492)).
- Native apps can: iOS `AVCaptureMultiCamSession` ([WWDC19](https://developer.apple.com/videos/play/wwdc19/225/)), Android 11+ `getConcurrentCameraIds` (optional per device) ([AOSP](https://source.android.com/docs/core/camera/concurrent-streaming)). Too slow to build natively in 8 h, and the jury needs a web link.
- **Our answer — "paired devices":** driver camera on one device (laptop webcam or phone A), road camera on phone B, **paired by a 4-digit room code over WebSocket**, timestamps synced, fusion on the server. Production pitch: one native app with multi-cam. This turns the limitation into an architecture slide.

## Pipeline (what we would build)
**Driver side — in the browser (no server cost):**
- MediaPipe Face Landmarker (478 landmarks, `@mediapipe/tasks-vision`, `runningMode: "VIDEO"`).
- **EAR** (6 points per eye) → eye closed; **PERCLOS** = share of time eyes > 80% closed over a rolling window; **MAR** → yawn; head pose (yaw/pitch from landmarks / transformation matrix) → **eyes-off-road** zone. Rule-based, no training — a 2026 paper found PERCLOS the most stable indicator and the combination better than any single metric ([IJSECS 2026](https://journal.lembagakita.com/ijsecs/article/view/7106)). Calibrate EAR per user (open-eye baseline varies) ([DrowSAFE](https://www.hackster.io/MohamedAliBedair/drowsafe-real-time-driver-drowsiness-detection-system-aeee70)). Use timestamps, not frame counts.
- Phone-in-hand: YOLO (COCO "cell phone") on the driver frame, or hand–face proximity from landmarks.

**Road side — server (or browser with ONNX Runtime Web for the nano model):**
- YOLOv8n/11n vehicle detection + tracking (ByteTrack) → lead vehicle = largest box in ego lane.
- **Monocular distance** via ground-plane assumption: bottom of the lead car's box + camera height + pitch from the vanishing point ([Bath, radar+mono fusion](https://researchportal.bath.ac.uk/en/publications/distance-estimation-by-fusing-radar-and-monocular-camera-with-kal/)); or box-width with known car width (~1.8 m). Kalman filter (differentiating noisy distance amplifies noise).
- **Headway (s) = distance / own speed** (GPS from the phone); **TTC = distance / closing speed**. Real-time monocular collision-risk on a laptop + webcam is shown feasible ([Phillips et al.](https://arxiv.org/pdf/1902.01293)).
- Lanes (stretch): Ultra-Fast-Lane-Detection v2 ([GitHub](https://github.com/cfzd/Ultra-Fast-Lane-Detection-v2); Luxonis package lists MIT, upstream licence to verify).

**Fusion — our core (the "system, not an API call"):**
- Risk = f(eyes-off-road duration, PERCLOS, headway, TTC, speed). Example rule: *eyes off road ≥ 1.5 s AND headway < 1.5 s* → critical; same glance on an empty road → low. Every rule visible in the UI ("why this alert").
- Output: live alert (sound + colour), trip timeline, event clips, driver score per 100 km.

## Data and test set (no invented numbers)
- Driver: **our own recordings** (team members, consent) in a parked car + driving as passengers film → labelled events. Public: DMD (41 h, 37 drivers, academic use, licence on download form — verify) ([DMD](https://dmd.vicomtech.org/)); State Farm (Kaggle competition terms — verify).
- Road: our own dashcam clips from Tashkent (blur plates/faces of others before committing — task rule).
- Measure on our test set: event precision/recall, alert latency, fps on our phones/laptop, cost per driver-hour (server inference). Night: phone front cam has no IR → report as known failure.

## Live jury test
Judge opens the link on their phone → selfie camera → looks away / closes eyes → alert in < 1 s. Second device (our laptop or their phone) with a road video → the alert becomes "critical" only when the road side shows a close car. Backup: recorded paired session.

## 8-hour MVP
1. Browser driver module (MediaPipe + EAR/PERCLOS/head pose) — ~2 h.
2. Server road module on uploaded/streamed video (YOLO + tracking + headway) — ~2.5 h.
3. Pairing by room code + fusion rules + alert UI — ~2 h.
4. Test set + measurements + deploy (HF Spaces / Render) — ~1.5 h.
Biggest risk: monocular distance accuracy — needs a quick calibration (measure 5, 10, 20 m with a tape in the parking lot) to report honest error.

## Market (Davlatyor — fill in from YouTube/web research)
- Who pays in Uzbekistan:
- Competitor UX seen in demos:
- Price anchor:

## Comments
<!-- other agents: `- <agent ID>: comment` -->
