---
name: PDI Evidence Checklist Assistant
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: dealer / service operations
mode: partner product (proposed Toyota/BYD Royal Motors pre-delivery team)
---

# PDI Evidence Checklist Assistant

**One line:** Photos of a supported vehicle are checked against its delivery checklist, so a worker knows which visible items need attention before handover.

## Problem and user

Pre-delivery inspection, or PDI, is the check before giving a new vehicle to its buyer. The delivery inspector uses the app; the dealership's delivery or aftersales unit would pay. The proposed problem is incomplete visual evidence or the wrong checklist for a vehicle variant. We need an interview and actual checklist to establish local frequency and cost.

[UVeye's deployment announcement with Hertz](https://newsroom.hertz.com/articles/article-details/hertz-and-uveye-partner-to-modernize-vehicle-maintenance-with-ai-technology/) demonstrates commercial interest in systematic vehicle inspection. It does not prove our specific checklist problem or a phone's ability to inspect an underbody.

## What the product does

- **Input:** Vehicle model/variant selected by the worker, authorised checklist, reference views and fresh photos from matching angles.
- **Context data:** The variant's expected visible equipment, allowed configuration, required evidence views and supervisor-approved sign-off rules. Use a case ID and synthetic job details in the public demo.
- **Output:** Every supported item is marked evidence present, possible mismatch, not observed or unreadable. A worker confirms whether the item passes. A report lists unresolved items with supporting crops.
- **Decision:** Retake a view, check a specific item or send the checklist to the supervisor for delivery sign-off.

For example, a wheel-centre cap may be expected on a particular variant. If its area is hidden, the result is **not observed**, not **missing**. A visibly different wheel may be flagged for reference checking; a model should not decide whether it is an authorised option.

## Tech and data

Pipeline: image quality and view matching → locate selected components → align relevant regions with the correct reference → compare appearance/presence → combine observations with the checklist. A reference-based anomaly model can flag differences; it cannot automatically name every mechanical defect. Candidate building blocks are DINOv2 retrieval, LightGlue with appropriately licensed feature extraction, and SAM 2 region refinement. Check exact code and checkpoint licences; see the [shared gates](refined-six-ideas-codex.md).

There is no assumed universal PDI dataset. Collect reference views of one consenting vehicle variant with permission to use its checklist. Label both normal configuration changes and genuine discrepancies. Safe removable props may test a checklist in a declared controlled experiment; they are not evidence that real manufacturing faults can be detected. Public exterior-part images may help localisation, but do not provide variant-specific pass/fail labels.

## Evaluation and real conditions

Measure checklist-item accuracy, wrong passes, false alerts, unobserved-item handling and inspection time including human corrections. Keep vehicles/capture sessions separate between development and testing. Compare the full pipeline with a simple reference-image difference baseline. Include approved options, reflections, dirt, viewpoint changes and deliberate blocked views.

Panel-gap measurement in millimetres needs calibrated geometry and suitable captures. Paint quality needs controlled illumination. Torque, internal fitment and hidden underbody defects are outside the phone MVP. An underbody extension requires dedicated access and capture equipment. Plate-to-customer lookup is unnecessary for this demo and would add personal/confidential data.

Initially run inference on a server, with guided capture in the browser. Benchmark actual hardware and report latency/cost per completed checklist, including retakes. Test daylight, night, rain/wet paint and local variants; otherwise label those conditions untested. In poor light, request a well-lit capture rather than issuing a pass.

## Business and pilot

Possible buyer: the delivery/aftersales manager, with site subscription pricing. Count inspector time saved, reduced repeat capture and fewer checklist omissions, measured against existing PDI. Add onboarding/reference collection, technician annotation, hosting, licences, storage and review time to pilot cost. Extra alerts can make the process slower; include that cost in the comparison. Use the [shared ROI formulas](refined-six-ideas-codex.md); no savings or price are validated yet.

A three-month pilot starts with one variant and a small authorised checklist, runs in parallel with normal inspection, and expands only after supervisor review of wrong passes. The potential advantage is an accurate variant-specific reference library and integration with real delivery sign-off. Generic anomaly detection or a checklist UI is easy to copy; we have no proprietary reference library today.

## Can we build it in ~8 h?

Conditional MVP: one variant, three clearly visible checklist items, guided photos and an unresolved-item report. Acquire references and prove the comparison works before building the UI. The jury can supply a fresh view of the supported vehicle or safely change/obscure a supported item. Arbitrary cars must return unsupported variant, not invented checklist results. Without access to a matching vehicle and references, this is a weak finals choice.

This is a focused evidence assistant. Automatic vehicle release, full mechanical inspection and service-bay worker tracking are separate products. It builds on the team's existing dealer/PDI research, credited in the [comparison](refined-six-ideas-codex.md).

## Comments
<!-- other agents: `- <agent ID>: comment` -->
