---
name: Road Hazard Tickets & Follow-up
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: road safety / road maintenance
mode: startup (fleet road-evidence service; maintenance teams as pilot users)
---

# Road Hazard Tickets & Follow-up

**One line:** Road photos or dashcam clips become reviewable, nonduplicated road-defect tickets; genuine location data can put those tickets on a map.

## Problem and user

A fleet already drives many routes, but someone still has to find useful defect evidence inside its recordings. Its operations/safety manager would use and potentially pay for the service; a maintenance team receives approved tickets. Municipal sales and response arrangements require validation, so do not assume a city contract.

There is real deployment evidence: [Hawaiʻi DOT's Eyes on the Road programme](https://hidot.hawaii.gov/highways/next-steps-for-eyes-on-the-road/) uses dash cameras with the University of Hawaiʻi and Blyncsy to send roadway-condition information to maintenance staff. This supports the workflow's relevance, not our accuracy or a proven local buyer. [Bentley's Blyncsy page](https://www.bentley.com/en/products/blyncsy/) provides a product video; the supplied Putrajaya clip is catalogued in [demo checks](demo-reference-checks-codex.md).

## What the product does

- **Input:** A road photo or short clip; optional timestamped GPS/GPX; operator-entered route and road context.
- **Context data:** Route ID, GPS accuracy/time offset, road category, operator-supplied lane exposure/traffic importance and maintenance rules. Weather history is optional and must have a declared source and terms; do not add it without a demonstrated decision benefit.
- **Output:** Supported defect type, evidence frame, timestamp, uncertainty, repeated sightings grouped into a ticket and a transparent review priority. Coordinates appear only when genuine GPS or a clearly labelled user location is supplied.
- **Decision:** A manager confirms the ticket and sends it for maintenance review. A later matched revisit can flag a possible repair or persistent issue for human confirmation.

Example: a pothole appearing in several frames should create one proposed ticket. With no location, show an unlocated ticket and clip timestamp. Never invent coordinates from the scene. Nearby holes must remain separate when the association is uncertain.

## Tech and data

Pipeline: road/visibility checks → road-damage detector → camera-motion-aware frame association → GPS synchronisation and location uncertainty → duplicate review → ticket/report. Compare follow-up views only if the same location and relevant road patch can be matched. A missing detection in a poor new view does not prove repair.

Start with potholes and one crack class, subject to working weights. Debris, standing water and faded markings require their own labels/models and tests; RDD does not provide all these classes. [RDD2022's original Figshare record](https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547) is a candidate. Its [publisher API](https://api.figshare.com/v2/articles/21431547) returned **CC BY 4.0**, DOI `10.6084/m9.figshare.21431547.v1`, checked 10 Oct 2026. Record attribution and modifications for the exact release. [RoadDamageDetector](https://github.com/sekilab/RoadDamageDetector) has MIT code; code terms do not relicense datasets or downloaded weights.

No suitable checkpoint, local footage or GPS file has been acquired. Only process images that meet the challenge's consent/privacy rules: use empty-road close-ups or appropriately approved data; exclude identifiable nonconsenting faces/plates before inclusion. Declare any synthetic data and collection method. Do not assume elimination-stage code is available or reusable until inspected and attributed.

## Evaluation and real conditions

Split tests by route and full recording, not adjacent frames. Measure class precision/recall, false tickets per kilometre when real distance is known (otherwise per clip-minute), event merges/splits, localisation error and coverage of unknown locations. Test repeat sightings and two close defects. Compare frame detections with deduplicated tickets. Follow-up evaluation needs actual matched repaired/unrepaired examples.

Test night, wet roads, shadows, puddles and local pavement; mark absent conditions untested. Image-box size is not pothole depth or physical danger. Priority combines confirmed category with declared road context and uncertainty; it is an operator policy, not a validated crash predictor.

Server processing is the initial deployment. Measure upload/decode/inference/report latency, video throughput and cost per analysed minute on named hardware. Continuous edge alerts are a later benchmarked option. There are no measured speed, cost or quality results yet.

## Business and pilot

Potential price: a fleet subscription with footage allowance. Pilot costs cover camera/GPS access, consented collection, labelling, hosting, storage, map-provider terms and review. Measure time to create usable unique tickets and maintenance-team acceptance. Do not claim avoided crashes or repaired roads without follow-up evidence. Apply the [shared ROI and pilot gates](refined-six-ideas-codex.md).

Three-month pilot: agree routes and ticket format, validate local footage, operate alongside manual review and revisit accepted issues. The possible advantage is local annotated repeat-pass footage plus ticket/maintenance integration. Blyncsy already establishes this category; a generic pothole detector is easy to copy.

## Can we build it in ~8 h?

Photo → evidence ticket is the fallback MVP. Add short-video deduplication only after the detector works, and mapping only with real synchronised coordinates. The jury can upload a new permitted road image/clip. A map backed by sample coordinates must be labelled a synthetic location demonstration. This directly refines Muhammadjon/claude-2's RoadProof and RoadGuard; choose one combined scope rather than presenting them as three separate inventions.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
