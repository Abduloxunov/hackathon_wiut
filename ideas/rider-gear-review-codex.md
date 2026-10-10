---
name: Rider Gear Evidence Review
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: driver / road safety
mode: partner product (proposed Ducati rider-training programme)
---

# Rider Gear Evidence Review

**One line:** A video that shows consenting riders becomes a short list of helmet-visibility events for an instructor to review and discuss.

## Problem and user

A rider-training instructor may need to review whether riders wore helmets during a session. The proposed buyer is Ducati's training/customer-safety programme, if it operates and wants this process; neither access nor interest is established. A delivery fleet is a possible later customer, not a second finals scope.

Helmet detection is established prior art. [Chairat and colleagues' WACV 2020 paper](https://openaccess.thecvf.com/content_WACV_2020/html/Chairat_Low_Cost_High_Performance_Automatic_Motorcycle_Helmet_Violation_Detection_WACV_2020_paper.html) combines motorcyclist detection, classification and tracking. Our novelty would need to be demonstrated in a useful local coaching workflow, rather than claimed for helmet detection itself.

## What the product does

- **Input:** A short consenting-adult clip from a fixed observer camera that clearly sees the rider's head, plus the training session's review policy.
- **Context data:** Allowed camera position, session/participant pseudonyms, visibility requirements and instructor-approved duration rules. Avoid identifying faces, plates or nonconsenting people.
- **Output:** A timeline of helmet visible, likely no helmet, or head not observable, with evidence clips and uncertainty. The instructor confirms events and assigns coaching.
- **Decision:** Ask for a clearer capture or review a possible equipment-policy issue with the rider. Do not automatically fine someone or label them an unsafe person.

A forward-facing rider dashcam generally cannot inspect its own rider's helmet. A phone facing the rider or an observer camera is needed. A clothing classifier cannot certify protective material, helmet approval, fastening or fit. Those remain physical checks. Drowsiness, distraction, medical posture assessment and collision warnings are excluded from this MVP.

## Tech and data

Pipeline: detect rider/motorcycle and head area → associate each head with the right rider/passenger → classify observable helmet appearance → track over time → merge repeated observations into events → produce an instructor review queue. Missing visibility must not become a helmet violation. Use a helmet-trained model with verified weights and data permissions; ordinary object-detection weights may not cover helmets.

The paper is a method reference, not permission to reuse every linked video, dataset or checkpoint. Start with consenting adults captured in a stationary or controlled training setting, with a clearly declared collection method. Include different helmet designs, hats, passengers, occlusion and empty background negatives. Split by participant, capture session and camera location. No data has been obtained yet. Safety events must not be staged in traffic; a stationary demonstration can test appearance without claiming riding-safety validation.

## Evaluation and real conditions

Report event precision/recall, false alerts per clip-minute, missed riders, rider/head association errors and the fraction of unobservable time. Compare frame-only alerts with temporally merged events. Separate night, rain, distance and occlusion results, including local helmet styles. If the camera cannot resolve a head, abstain. A high score on adjacent frames is not evidence of generalisation to new riders.

Initial inference is uploaded-video processing on a server. Record clip length, resolution, processed frames/second, end-to-end latency and server cost per video minute on actual hardware. None is measured. Real-time protection would require suitable installed hardware, distraction/usability tests and a separate alert-latency safety assessment; a web upload demo establishes none of those.

## Business and pilot

Possible pricing is a training-site subscription. Measure instructor review time and accepted coaching events, including time spent dismissing false alerts. Pilot cost includes consented collection, labelling, camera installation if needed, hosting/storage, licences and instructor review. Do not translate helmet flags into invented avoided accidents or insurance savings. Use the [shared business protocol](refined-six-ideas-codex.md).

A three-month pilot would agree camera/consent arrangements, run alongside instructors and audit errors before expanding. A consented local dataset and a useful coaching process could become advantages. They do not exist yet. Simple helmet detection has limited originality and does not currently fit the lead's dealer/service focus as closely as parts or PDI.

## Can we build it in ~8 h?

Conditional MVP: helmet visibility on a single suitable view, tracking, event timeline and instructor confirmation. First obtain a licensed working checkpoint and representative clips. The jury can upload a new consenting clip or use a stationary webcam test with a helmet and an uncovered head; label this a controlled appearance test. Without these inputs, keep this as a secondary idea.

Nearby-hazard analysis and blind-spot warnings are separate extensions needing road-facing cameras and validated geometry. This proposal does not promise the original concept's combined gear, posture, fatigue and hazard monitor.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
