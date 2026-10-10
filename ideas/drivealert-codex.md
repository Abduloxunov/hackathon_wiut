---
name: DriveAlert — Driver Drowsiness & Distraction Monitor
added_by: Bexruz + codex
date: Sat 10 Oct 2026
direction: driver / road safety
mode: startup (fleet safety teams and driver-training operators)
---

# DriveAlert — Driver Drowsiness & Distraction Monitor

**One line:** A consenting driver's camera feed → visible eye/head signals tracked over time → an explained possible-drowsiness or attention warning and an event timeline for review.

## The idea in simple words

DriveAlert watches for sustained eye closure, repeated yawn-like movements and extended head turns. A normal blink should not trigger an alarm. If a supported pattern persists while the camera has a clear view, the app gives a warning and explains which observations caused it.

The important improvement is knowing when the camera cannot assess the driver. Dark footage, sunglasses, a blocked face or a moved camera produce **monitoring unavailable**, rather than “driver awake” or “driver asleep.” The session report includes both detected events and time when monitoring was unavailable.

## Problem, user and buyer

- **Mode:** Startup. The first slide names this mode.
- **User:** A consenting driver or training participant; a safety instructor/manager reviews the summary.
- **Potential payer:** A delivery/logistics fleet safety manager or driver-training operator. Choose one segment for the pilot; a Royal Motors fleet-service channel is a possible later route, not a confirmed partner.
- **Process changed:** Finding reviewable visual attention events and deciding where coaching or a camera-position check is needed.
- **Problem to validate:** Whether the buyer needs additional coaching evidence, accepts local processing and can tolerate the false-alert burden. No local fatigue statistics, customer agreement or accident-reduction evidence are assumed.

This is an established product category, not a new invention. [LogisFleet's driver-monitoring page](https://logisfleet.com/driver-safety-monitoring) and [Samsara's drowsiness product page](https://www.samsara.com/products/cameras/drowsiness-detection) describe camera-based behaviour alerts and fleet review. [LG/Ambarella's announcement](https://www.ambarella.com/news/lg-and-ambarella-join-forces-to-advance-ai-driven-in-cabin-vehicle-safety-solutions/) describes a dedicated in-cabin system and states it was in production with an automotive OEM. These are supplier descriptions; their hardware performance and claimed benefits do not transfer to our webcam prototype.

## User flow and outputs

1. Open the public HTTPS app, consent to camera processing and start a stationary demo/training session, or select a permitted video file.
2. Check camera position and visibility. Capture a short neutral, open-eye baseline for the individual/camera. Recalibrate after the camera moves or the session changes.
3. Show whether tracking is usable, the observed eye/head indicators and how long the current candidate event has persisted. A landmark overlay is optional; it is not the product's main result.
4. When an evaluated temporal rule triggers, show an explained warning. For example: “Possible drowsiness: sustained eye-closure pattern.” Optional audio requires user enablement and browser testing.
5. Merge repeated observations into one event, with onset/end, measured duration, reason and observability. Show an event timeline and local session summary.
6. A reviewer can confirm or dismiss a coaching event and note camera problems. The MVP exports a local report; uploading pseudonymous event summaries to a fleet dashboard is an optional, separately consented extension.

The wording stays tied to observations. Yawning does not prove fatigue. Head direction is only a rough attention proxy, not proof of eye gaze or distraction: mirror checks, turns and conversations can look similar. No facial identity recognition, medical diagnosis, automatic employment decision or guarantee of safety is included.

## Computer vision + context → action

**Context data:** Camera position, individual open-eye/neutral-head baseline, frame timestamps, visibility confidence, session type and published alert rules. The prototype has no road/speed context; it cannot infer that a head turn was dangerous. If a later fleet supplies permitted vehicle-motion information, its accuracy/freshness must be checked before using it for alert context.

Pipeline: face detection/landmarks → estimate eye opening, mouth movement and head-direction change → observability checks → timestamp-based temporal state machine → explained alert → event review.

- **Eye closure:** Compare eye-landmark geometry with the session baseline. Track continuous estimated closure duration and distinguish it from normal blinks.
- **Mouth movement:** Identify sustained/repeated yawn-like openings as supporting observations. Speech, eating and facial expressions are negative cases, not automatically yawns.
- **Head direction:** Compare with a camera-relative baseline. Do not equate head pose with precise gaze or label every glance a violation.
- **Temporal logic:** Use elapsed time, not frame counts. Require persistence, use separate enter/exit thresholds to reduce rapid switching, and apply event merging/cooldown to limit repeated alarms. Choose thresholds on development data, publish them and evaluate on held-out sessions; they are not medically validated limits.
- **Unavailable state:** Missing/low-quality observations suspend or end candidate events. Do not count unseen eyes as closed or carry a timer through a long tracking gap. An eye-closure fraction over a window must report its observable duration and missing coverage; it is an estimated indicator, not an automatically validated PERCLOS measurement.

This makes the contribution a measured temporal/visibility system rather than a single face-model call or an LLM judgement. A numerical crash-risk or fatigue score is excluded until there is appropriate validation; the MVP shows event evidence and uncertainty instead.

## Proposed implementation and inference location

Use a responsive JavaScript/React interface and MediaPipe Face Landmarker for both live camera frames and decoded local-video frames. [Google's web guide](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/web_js) documents face landmarks, optional transformation outputs and video processing. Its synchronous calls can block the UI; isolate inference in a tested worker or otherwise bound processing so the interface remains responsive. The landmarker itself is not a fatigue detector.

Proposed inference is **on the user's device in the browser**. The video-file mode selects a local file for processing; it need not transmit it to a server. Host the frontend and pinned model/runtime assets; an optional API stores only explicitly approved event summaries. OpenCV/Python can support offline labelling/evaluation, but is not required for the browser inference path.

Check exact library/checkpoint licences, asset versions and attribution. Do not assume the documentation's licence covers every model artifact. No relevant dependencies or weights are installed as part of this idea request. Test actual browser/device compatibility, camera permissions, initial model download, background-tab behaviour, sound activation and mobile throttling before making live-operation claims.

## Privacy and data plan

Default design: raw frames and landmarks are transient, no face video is recorded/uploaded, and no person is identified. Verify this in implementation through network/storage inspection; a privacy promise is not established by an idea document. Session exports use pseudonyms, and sharing/retention require explicit participant permission. A participant can stop the camera and clear the local session.

Collect consenting adults in a parked car, training room or stationary webcam setting. Label observable events and their onset/end: natural blinks, sustained eye closure, yawn-like movement, speaking, short/long head turns, occlusion and unusable visibility. Scripted awake volunteers simulate these signs; this validates signal/event detection, not detection of genuinely sleepy drivers. Never induce fatigue or dangerous behaviour while driving to create a demo.

No recordings have been collected yet. A public driver dataset is a future candidate only after checking its original usage terms and compliance with the challenge's consent rules. Public availability is insufficient. Document collection/generation methods and licences; store authorised footage outside git. Split by person and full session/device so adjacent frames or the same participant do not leak into the final test. Calibration is part of the user procedure, not test-label tuning.

## Evaluation and real conditions

Measure precision/recall for each observable event, false alerts per observable hour, onset/duration error, alert delay, event duplicates and unavailable coverage. Define how labelled/predicted events are matched and report sample counts. Compare a single-frame baseline with temporal logic, then test the effect of calibration and unavailable handling. Include ordinary blinks, speech, mirror-like glances, eyewear, different camera angles and face shapes. Report condition-specific errors and unknowns, not only an overall score.

Separate **scripted sign detection**, **actual fatigue detection** and **crash prevention**. Only the first is an achievable initial evaluation; the others require appropriate real-world studies. Do not borrow a competitor's accuracy, count every alert as a prevented accident or claim medical-grade drowsiness detection.

Low light, sunglasses, masks, glare, vibration and head occlusion can defeat an ordinary visible-light webcam. Night use may require appropriate IR equipment and new validation. Rain matters indirectly through lighting, reflections and in-cabin visibility; test genuine examples rather than promising robustness from augmentation. Local fleet camera placement and consenting local participants need specific validation. Motorcycle helmets make a rider version a separate, harder project; exclude it from this MVP.

Benchmark actual laptop/phone model, browser/version, camera resolution, model version, processing rate, frame gaps and camera-to-alert latency including the rule's persistence time. Measure long-session thermal/battery behaviour. Record cold model load separately from warm inference. No speed, quality, night-performance or real-time reliability numbers exist yet.

## Business and three-month pilot

Possible pricing: per active device/vehicle subscription, subject to buyer validation. Browser inference reduces server video processing but still has model delivery, device/battery, support and update costs. Include camera/mount or IR hardware when needed, collection/labelling, browser QA, hosting, optional logging, licences, integration and reviewer time in the pilot budget.

The first measurable benefit is review/coaching time and accepted useful events, with false-alert and driver-acceptance costs included. A shadow pilot should compare existing safety-review work with the assisted process. Monthly unit cost is total running/support/review cost divided by monitored device-hours, including idle subscriptions and unsuccessful sessions. Calculate payback only from validated positive net benefit. Crash reduction, lower premiums and revenue are unverified, so none is used as a guaranteed ROI assumption.

Month 1: interview one buyer, agree consent and review policy, collect stationary data and establish the baseline. Month 2: run supervised training/shadow assessment on agreed hardware and audit false alerts/unavailable periods. Month 3: consider a limited supervised fleet study only after partner safety/privacy review and applicable requirements are checked. A web demo is not approval for operational safety use; production mounting, human factors and in-vehicle validation are separate work.

## Finals MVP and differentiation

MVP: one-face live-camera mode, local-video mode, session calibration, eye-closure events, conservative head-away candidates, visibility state, explained alerts and a local timeline/report. Treat yawn-like observations as a secondary feature if time allows. Phone-use detection, road-camera fusion, fatigue diagnosis and a full fleet dashboard are outside the first build.

The jury can test a consenting stationary volunteer: normal blink, sustained eye closure, brief versus sustained turn, speaking and blocked camera. Show both an event and an unavailable case. A new video is processed by the same actual pipeline; scripted filenames or prerecorded results are forbidden. Deploy from the submitted repository, test another laptop/phone and record a backup and deployed commit before the freeze.

This has a strong fresh-input demo but **modest originality** as a standalone idea. The potential advantage is a documented local test set, fewer nuisance alerts, reliable observability handling and a privacy-preserving coaching workflow. Those advantages must be measured; client-side processing and eye landmarks alone are easy to copy. No proprietary data or validated advantage exists today.

**First-slide wording:** “DriveAlert — Startup for fleet safety teams. On-device visual attention signals become explained alerts and reviewable coaching events.”

## Attribution and status

Refines Bexruz's supplied description and Muhammadjon/claude-2's [Driver Fatigue Guard](driver-fatigue-guard.md). It also overlaps the driver-camera portion of Davlatyor/claude-1's [DriveCoach](drive-coach.md); this proposal does not add that idea's road-camera/collision context. Existing supplier systems and MediaPipe are credited above. User-supplied image-proxy links were treated as illustrations, not technical or licence evidence; original provider pages were checked instead.

Proposal only; no product code, datasets, measurements or partner commitment. Road safety is a requested alternative to the lead's dealer/service focus, not a change of team selection.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
