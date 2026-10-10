---
name: Vehicle Damage Evidence & Estimate Review
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: vehicle inspection / dealer operations
mode: partner product (proposed Royal Motors trade-in appraisal desk)
---

# Vehicle Damage Evidence & Estimate Review

**One line:** Guided car photos become a list of visible damage, missing evidence and a traceable estimate for an appraiser to review.

## Problem and user

A trade-in appraiser needs to record the car's condition and understand possible bodywork costs before making an offer. An unstructured photo folder makes it easy to miss a panel or count one scratch twice. The appraiser uses the product; the dealership's used-car unit would pay. This is a proposed owner, not an agreed partnership.

There is an established market: [Hertz announced deployment of UVeye inspection systems, starting in Atlanta](https://newsroom.hertz.com/articles/article-details/hertz-and-uveye-partner-to-modernize-vehicle-maintenance-with-ai-technology/). Those systems use dedicated cameras; their results do not establish what our phone prototype can achieve. See [checked demos](demo-reference-checks-codex.md) for NeenOpal, Intelliarts, WeProov and Carscan. We have no local interviews or measured inspection savings yet.

## What the product does

- **Input:** A guided photo set, vehicle variant entered by the appraiser, and an authorised repair rate card. Start with still photos; extracting useful frames from video is a later convenience.
- **Context data:** Vehicle/panel identifiers, required views, repair-operation definitions, local labour rates, parts prices, currency, taxes and rate-card date. A sample rate card must be labelled synthetic.
- **Output:** Each supported visible defect has an evidence crop, likely panel, uncertainty and a suggested review action. Missing or unreadable views trigger a retake. The report separates confirmed findings, uncertain candidates and uninspected areas.
- **Decision:** Request more evidence or send the car to an appraiser/bodywork specialist. The human approves any repair operation and trade-in offer.

Example: three photos may show the same bumper scratch. The system proposes one finding, links all three views and shows a repair-cost range only if a matching operation and rate exist. Otherwise it says **cost unavailable**. Confidence is not physical severity. Photos alone cannot establish dent depth, hidden damage, mechanical safety or a final repair bill.

## Tech and data

Pipeline: blur/exposure/view checks → exterior-part localisation → damage detection or segmentation → associate findings across compatible views → apply the versioned rate-card rules → structured evidence report. Cross-view matches must remain uncertain when registration fails. An LLM may explain the structured result; it must not invent defects, prices or decisions.

Candidate data: [Humans in the Loop's exterior car-part/damage dataset](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/) lists CC0 1.0 and requires an access form. It is not a repair-price dataset. No data or suitable trained weights have been acquired for this proposal. Start with a damage-trained checkpoint whose code, weights and training-data terms have been checked; a generic car detector does not detect scratches. SAM 2 can refine a proposed region, but does not by itself classify damage. Follow the [shared licence and deployment gates](refined-six-ideas-codex.md).

Collect consenting owners' cars and genuine clean/damaged examples. Split by vehicle, not near-duplicate photos. Reflective paint, dirt and stickers are important negative cases. A marked toy car is a declared controlled demo, not a test of real damage.

## Evaluation and real conditions

Measure per-class precision/recall, panel assignment, duplicate findings per inspection, missed views and retake accuracy. Compare single-photo detections with the multi-view report. Evaluate estimate error against an authorised estimator only when genuine labelled quotes are available; record uncertainty and excluded operations.

Test daylight, night, wet paint, glare and local Toyota/BYD variants separately. If a condition has no test examples, mark it untested. Use a case ID; plate recognition is unnecessary. Server inference is the initial plan. Record hardware, resolution, images per inspection, cold/warm latency and cost using the shared protocol; speed and cost are currently unmeasured.

## Business and pilot

Possible pricing: site subscription plus an inspection allowance, to be tested with the appraisal manager. Cost per inspection includes inference, storage, network, any paid APIs and human review. Benefit is verified appraiser time saved, less extra retaking and fewer duplicated repair items; do not count speculative accident avoidance. Collect a manual baseline and compare full workflow time, including corrections. Payback follows the shared formulas.

Three-month pilot: agree supported panels and rate-card permissions; label a small local validation set; run alongside normal appraisal; audit errors before extending use. The possible advantage is a local, labelled inspection set plus reliable multi-view evidence and an approved rate card. None is owned today; damage detection and PDF reports already have competitors.

## Can we build it in ~8 h?

Conditional MVP: two supported damage categories on a small panel set, quality checks, evidence report and a rate-card calculator. A suitable licensed damage checkpoint and real test photos are go/no-go requirements. The jury uploads a fresh supported car photo, gets an actual result, then deliberately submits a blurred view to test retake handling. Unsupported inputs must produce an honest limitation. A synthetic price list may demonstrate arithmetic, not real quoting accuracy.

Build this as one appraisal workflow. Insurance routing, tyre depth, glass assessment and fully automatic accept/reject are separate extensions. This refines TradeIn PreCheck and LensCheck in the repository; credit their authors rather than claiming a wholly new idea.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
