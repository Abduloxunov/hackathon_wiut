---
name: Crosswalk Visibility Audit
added_by: Bexruz + codex
date: Sat 10 Oct
direction: driver / road safety
mode: startup
---

# Crosswalk Visibility Audit

**One line:** Guided crossing-approach imagery → supported visible marking/sign issue evidence → maintenance-review ticket or request for a better view.

## Problem and user
- User: road-maintenance inspector; payer: contractor or municipal asset-maintenance team. Local inspection frequency/cost and procurement path are unverified.
- [FHWA](https://highways.dot.gov/safety/proven-safety-countermeasures/crosswalk-visibility-enhancements) identifies poor lighting, parked-car obstructions and geometry as crossing-visibility problems. This supports the problem, not a local legal threshold. [Blyncsy](https://blyncsy.com/solutions/construction-zones/) lists road-asset/marking products as prior art.

## What the product does
- Input: guided approach photos/short video of a known crossing, with site identified by the inspector.
- Output: annotated supported issue (start with either faded marking appearance or sign occlusion), capture gaps and proposed maintenance category. Human approval precedes a real maintenance decision.
- Live jury test: unseen supported crossing imagery with a changed view or poor capture; explicit uncertainty on unassessable inputs.
- Boundary: arbitrary JPEGs cannot establish lux, retroreflectivity or sight distance in metres. The output is visual evidence for review.

## Tech (why it is a system, not one API call)
- Crossing/sign localisation → view/quality gate → supported appearance/occlusion analysis → multi-view evidence aggregation → ticket. Detection feasibility must be established first; no ready local model is assumed.
- Data today: own empty local crossing imagery where safe lawful access is possible, avoiding unconsented people/plates; issue labels with an inspector if available. Hold out entire sites/capture sessions. Public image/dataset and model licences require verification. Controlled or synthetic obstructions are declared separately.
- Proposed inference: server, CPU/GPU to be selected after a feasibility benchmark; speed/cost unmeasured.
- Night/rain/local setting: separate actual wet/night/site tests. Digital darkening is only a stress test; untested conditions are reported as such.
- Test: supported-issue precision/recall, false tickets, localisation errors and correct abstention on poor views. Photo appearance is not objective engineering measurement.

## Why hard to copy
- Potential future advantage: local issue labels, capture protocol, evidence-to-ticket workflow and later matched-view repair follow-up. No proprietary dataset exists yet; generic road-asset vision already exists.

## Business
- Proposed billing: per audited site/route or contractor subscription; price unverified.
- Cost includes capture/annotation, inference, storage and human review. Pilot benefit is measured inspection/review time and ticket usefulness; no prevented-crash claim.
- Three-month pilot: limited sites and agreed labels → shadow audits → inspector-approved tickets with operational comparison. Municipal procurement is not confirmed.

## Can we build it in ~8 h?
- Conditional MVP: one issue, guided views, annotated evidence and a ticket report; no broad safety score.
- Biggest risk: too few genuine defect examples and no reliable local detector/labels. Decide only after real-input feasibility testing.

## Comments
<!-- other agents may append comments -->
