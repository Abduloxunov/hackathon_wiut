---
name: RoyalScan — Guided Vehicle Condition Inspection
added_by: Bexruz + codex
date: Sat 10 Oct 2026
direction: vehicle inspection / dealer operations
mode: partner product (proposed Toyota/BYD Royal Motors used-vehicle appraisal desk)
---

# RoyalScan — Guided Vehicle Condition Inspection

**One line:** Take guided photos of a car on a phone → receive a clear report of supported visible damage, missing evidence and estimated bodywork costs → decide what an appraiser should inspect next.

## The idea in simple words

When a dealership considers buying a used car, an employee checks its condition and works out what might need repairing. RoyalScan helps that employee collect consistent photos, find visible damage and prepare the inspection report.

The employee opens a website, follows the photo instructions and gets a report showing where the supported damage is, what evidence is missing and which findings need a bodywork specialist. When an approved repair price list is available, the report also shows an estimated cost range and explains how it was calculated.

The product's main value is a more complete, reviewable inspection. It does not promise to discover every fault or determine a car's total market value from photos.

## Problem, user and owner

- **Mode:** Partner product. Name this mode on the first slide.
- **Proposed owner and payer:** Toyota/BYD Royal Motors' used-vehicle appraisal unit. This is a proposed pilot owner, not a confirmed agreement.
- **User:** The employee photographing the car and the appraiser reviewing it.
- **Process changed:** Collecting and reviewing visible-condition evidence before a trade-in offer.
- **Problem to validate:** Inconsistent photo coverage, repeated inspection work and incomplete evidence for repair estimates. We have no partner interviews or measured local losses yet; a manager interview and a timed manual inspection are the first validation steps.

Service intake, rental returns and insurance are possible later uses. The finals prototype should demonstrate one appraisal workflow with one buyer.

## How it works

1. **Start an inspection.** Enter a case ID and select a supported vehicle variant. The public demo uses synthetic case details, with no customer records.
2. **Follow the capture guide.** The website asks for exterior angles and close-ups of relevant panels. A proposed capture checklist uses eight overview views plus defect close-ups; this is a design choice, not a measured capture-time claim. Ordinary camera upload remains a fallback if browser capture is unsupported.
3. **Check photo quality.** The system checks blur, exposure, framing and required-view coverage. It explains a retake, such as “the bumper is too dark” or “the left-side view is missing.”
4. **Find supported damage.** Computer vision locates the panel and proposes visible scratches or dents, subject to the classes actually supported by the chosen model. The worker can confirm, correct or dismiss each finding.
5. **Connect the evidence.** Compatible views are linked so the same defect is not charged twice. Uncertain matches stay separate for review. A scratch in one photo and a reflection in another must not automatically become a confirmed defect.
6. **Prepare the estimate.** Confirmed findings are matched to approved repair operations and prices. Missing prices, unclear repairability or hidden damage produce “estimate unavailable” or “specialist assessment required.”
7. **Create the report.** Export the evidence and review outcome for the appraiser. The appraiser decides on the offer or referral.

## What the report contains

Inspection ID, declared vehicle variant, submitted views, uninspected areas, annotated images and close-up crops; supported defect descriptions; worker confirmation; proposed repair operations; estimate range with price-list version and assumptions; unresolved questions; and the recommended next step.

Use evidence-based outcomes: **retake photos**, **review visible damage**, **refer to bodywork specialist**, or **no supported visible damage found in the submitted views**. That last result is not a mechanical-safety certificate. A simple overview marks the affected panels; a reconstructed 3D car is outside the MVP.

## Computer vision + context → decision

**Context data:** Required views, supported vehicle/panel definitions, authorised labour and parts prices, repair-operation rules, currency, taxes and price-list date. The appraiser provides variant information; plate recognition is unnecessary.

| Stage | What it does | Why it matters |
|---|---|---|
| Quality and coverage checks | Assess whether the submitted evidence is usable and complete | Prevents a missing or unreadable panel from becoming an apparent clean result |
| Panel and damage localisation | Finds supported panels and visible defect regions | Connects each proposed finding to a specific piece of evidence |
| Multi-view association | Links compatible observations, with uncertainty | Reduces duplicate findings and lets a worker inspect contradictory views |
| Repair-rule calculation | Combines confirmed findings with approved operation/rate records | Produces a traceable estimate rather than a price guessed by a general model |
| Review and report | Preserves corrections and unresolved findings | Turns detections into an appraisal action |

Candidate stack: a responsive web frontend, Python 3.11/FastAPI backend, task-specific damage model, image matching where useful, a small versioned rate table and HTML/PDF reporting. RF-DETR is a possible detector framework if a suitable damage-trained checkpoint can be obtained or trained; general pretrained weights do not automatically recognise scratches. SAM 2 may refine proposed regions, but does not identify damage on its own. Check the exact code, weights and data licences before choosing components and follow the lead's model restrictions.

Initial inference runs on a server. The phone captures and uploads photos. Edge/hybrid processing is a future option only after benchmarking actual hardware. A language model is optional for wording; all findings, prices and decisions must come from the structured pipeline.

## Repair cost and severity

The estimate uses a declared calculation: **approved labour hours × local labour rate + applicable parts/materials + declared taxes**. Use a range when several repair operations remain plausible. Record what the estimate excludes and require appraiser approval.

A static, versioned price table is legitimate context. It must not be a lookup of predetermined answers for specific demo photos. For the finals, a clearly labelled synthetic table can demonstrate the calculation; it cannot establish accurate local repair pricing. A real pilot requires authorised, current rates. Scraped prices are not assumed reliable or licensed.

Visible damage appearance does not establish physical dent depth, structural severity or whether a part must be replaced. Keep the model's confidence separate from severity. Until expert-labelled severity and repair-operation data exist, show the observed defect and request an expert decision rather than inventing a severity score or an automatic trade-in acceptance.

## Data and quality plan

The [Humans in the Loop car-parts/damage dataset](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/) is a candidate for exterior-part and damage labels; the publisher lists CC0 1.0 and an access form. It supplies neither local repair prices nor proof of performance on our vehicles. No suitable task checkpoint, dataset access, real car photo collection or rate card is ready yet.

Collect permitted photos from consenting owners, label damage and clean negative examples, and split development/test sets by car and capture session. Keep identifiable unconsented faces/plates and confidential records out of the inputs; photograph with plates covered and people out of frame where possible. Automatic masking is not a substitute for the challenge's consent rules. Record sources, licences, model versions and collection methods. Keep images and weights outside git in the team's agreed storage.

Test separately on daylight, low light, wet paint, glare, dirt, reflections and local Toyota/BYD variants. Include clean panels and two views of the same defect. Augmentation may help training, but cannot prove night/rain robustness. Conditions without genuine test examples remain untested.

Measure damage precision/recall, panel assignment, duplicate findings, missed views and retake accuracy. Compare single-view output with the combined report. Measure estimate error only against genuine expert-labelled quotes for the supported operations. Show sample counts, uncertain results and known failures; no accuracy or savings numbers are claimed yet.

## Business, cost and pilot

Possible pricing is a site subscription with an inspection allowance. Validate it with the appraisal manager. The initial business case is less time gathering/reviewing evidence and fewer repeated or duplicated repair items, not assumed reductions in purchase prices or guaranteed avoided losses.

Pilot budget includes people, authorised collection and labelling, price-list preparation, model/data licences, hosting, storage, integration, testing and review. Monthly cost per completed inspection is total compute/API/storage/network/support and review cost divided by completed inspections, including failed attempts and retries. Actual costs depend on hardware and utilisation and are unmeasured.

Measure full manual versus assisted inspection time, including retakes, corrections and false alerts. Calculate monthly benefit from verified net time saved and separately documented errors avoided. Subtract running costs; divide pilot investment by positive net monthly benefit for payback. If that benefit is not positive, do not claim a finite payback. Price, revenue and ROI remain assumptions until validated.

Three-month pilot: first agree permissions, panels, rates and baseline; then run the tool beside normal appraisal and audit errors; finally allow limited supervised use if quality and economics justify it. The partner must approve its data handling and operational process.

## Why it could be hard to copy

The possible advantage is an expert-labelled local vehicle dataset, reliable multi-view evidence handling, versioned local repair rules and corrections from real appraisal work. None exists as an owned asset today. Guided photos, a damage model and a report alone are readily reproducible. Demonstrate that the combined pipeline improves quality or time over a simpler baseline before claiming technological differentiation.

## Finals MVP and live demo

**MVP:** Guided photo upload, quality/coverage checks, two validated damage categories on a small supported panel set, worker review, conservative multi-view association, declared estimate calculator and shareable report. Begin with photos; video walkaround, plate recognition, tyre-depth measurement, hidden faults and broad vehicle grading are later extensions.

**Build gate:** First run a licensed damage model on fresh real examples. If weights or supported inputs cannot be obtained, a polished upload screen is not a working damage-inspection product. Keep any quality-check fallback accurately labelled as its smaller scope.

Deploy both frontend and backend from the repository to public HTTPS. The jury uploads a fresh permitted photo or captures a supported car view; the actual pipeline produces an editable finding/report. A deliberately blurred view tests retake handling. The estimate shows its source and assumptions. Any toy-car or removable-mark test is explicitly a controlled test and cannot substitute for real-damage evaluation.

Benchmark named hardware, input resolution/view count, cold-start and warm end-to-end latency, and cost per inspection. Set no capture or processing-time claim until measured. Record a backup demo and the deployed commit; follow the submitted-commit freeze rules.

**Seven-minute defence:** Problem/user 1 minute; fresh-input demo 2; pipeline, evaluation and failure examples 2; pilot budget/ROI assumptions 1.5; next steps 0.5.

**First-slide wording:** “RoyalScan — Partner product for Toyota/BYD Royal Motors' used-vehicle appraisal desk. Guided car photos become reviewable damage evidence and a traceable bodywork estimate.” Mark the partner relationship as proposed.

## Attribution and status

Standalone refinement of Bexruz's supplied inspection concept and the team's TradeIn PreCheck/LensCheck work, with the earlier damage proposal in [PR #4](https://github.com/Abduloxunov/mdb-vision-finals/pull/4). It is an idea proposal, not an implemented product, measured result or claim that existing vehicle-inspection methods were invented during the final. Lead selection remains pending.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
