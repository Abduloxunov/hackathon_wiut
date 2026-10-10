# Automotive business and road safety: sourced opportunity review

Prepared by Bexruz + codex, 10 October 2026. Research and proposals only; no product implementation or measured model results.

## Context and evidence boundaries

This review uses the supplied finals rules, `AGENTS.md`, the worklog, task board and both agents' existing ideas. The requested ChatGPT conversation at https://chatgpt.com/c/6ac9f572-dc54-83eb-bff3-ab2f4d7ad627 was inaccessible: web retrieval failed and the available browser showed a signed-out page. Its contents have **not** been incorporated. A pasted discussion or accessible shared link is still needed.

Four new workflow proposals are in separate template files. Parts Verification and Crossing Conflict Review below are explicit refinements of existing PartsLens and Junction Risk Map, rather than duplicate submissions. The lead chooses the product. This branch follows the human's instruction to use a PR and never push to main, which takes precedence over the repository's direct-main documentation exception.

The final sync includes the lead's 16:10 decision to focus on **dealer and service operations**. Parts Verification and Repair Evidence Review align with it. The road-safety alternatives remain here to satisfy Bexruz's explicit request for both categories; they are comparison material, not a change to the team's build scope. The new dealer/service landscape was also reviewed; repair evidence is narrower than the broader MPI Video Auditor proposal.

Evidence labels:
- **Documented:** an official source describes a problem, product or announced deployment.
- **Vendor claim:** the supplier describes its functionality; this is not independent validation of accuracy or savings.
- **Hypothesis:** our proposed local customer pain, price, advantage or benefit; it requires validation.
- **Unmeasured:** prototype accuracy, speed, cost and robustness. There are no results yet.

## What problems and products already exist?

| Area | Evidence and existing implementation | What it means for our choice |
|---|---|---|
| Vehicle condition inspection | [Hertz's April 2025 announcement](https://newsroom.hertz.com/articles/article-details/hertz-and-uveye-partner-to-modernize-vehicle-maintenance-with-ai-technology/) identifies variable manual inspections and describes UVeye camera/ML inspection, starting at Atlanta airport. | There is an established business workflow. A generic damage detector needs a narrower advantage; dedicated scanners do not establish phone-camera performance. |
| Repair-network review | [Tractable's Warta announcement, May 2021](https://tractable.ai/tractables-ai-to-give-warta-total-oversight-of-its-auto-repair-network/) describes visual AI supporting repair-network oversight. | Evidence review is a plausible buyer workflow, but local rework costs and demand remain unknown. |
| Parts search | [Partium documentation](https://docs.partium.io/partium-find/partium-search-engine/how-partium-image-part-search-works/) describes image/text retrieval against master data, including visual reference matching. | Photo-to-part search already exists. Verifying the picked item against a job and refusing ambiguous matches is a more specific proposal. |
| Charger operations | [ChargeLab's December 2024 Spark beta announcement](https://chargelab.co/blog/spark-ai-launch) describes AI monitoring and diagnosis using OCPP logs and system events. | A photo-first intake flow could help when telemetry is unavailable, but that gap and the usefulness of visible codes must be checked locally. |
| Traffic conflicts | [VivaCity's Near Miss product](https://info.vivacitylabs.com/near-miss-feature-smart-road-safety) describes CV trajectories and interaction analysis. | Near-miss detection is established prior art. Our case would depend on existing team code, locally evaluated clips and a useful review workflow. |
| Crossing visibility | [FHWA guidance](https://highways.dot.gov/safety/proven-safety-countermeasures/crosswalk-visibility-enhancements) identifies parked-car obstructions, poor lighting and road geometry as visibility problems. | Inspecting visible maintenance defects has a concrete action. This US guidance is problem evidence, not Uzbekistan's legal standard. |
| Work-zone monitoring | [Blyncsy's product page](https://blyncsy.com/solutions/construction-zones/) describes dashcam equipment detection, signs and actual-versus-plan review. | Work-zone plan checking already exists. Local checklists and an auditable small-contractor workflow would need to distinguish our product. |

These sources establish implementations and plausible workflows, not the proposed product's performance. No supplier's accuracy, ROI or marketing superiority is adopted as ours.

## Local relevance

The [National Statistics Committee](https://stat.uz/en/press-center/news-of-committee/65603-zbekistonda-zhismonij-shakhslarga-tegishli-avtotransport-vositalari-soni-4-7-mlndan-oshdi-4) reported 4,725,900 privately owned vehicles as of 1 October 2025. That dated stock supports an automotive-market context; it does not measure service-centre inefficiency or willingness to pay.

[BYD Royal Motors' local service page](https://byd-rm.uz/service) describes maintenance, repairs and original parts in Tashkent. Aftersales quality control and the parts counter are therefore plausible proposed ownership units. No partner agreement, process observation or access to its data is established.

[WHO's Uzbekistan road-safety country profile](https://www.who.int/publications/m/item/road-safety-uzb-2023-country-profile) provides country-specific road-safety context. Its historical data must be dated when cited; it does not demonstrate that a particular crossing or work zone needs our intervention.

Before making a local business claim, validate the current process with a service advisor, parts clerk, charger operator or road-maintenance reviewer. Record what they do now, frequency, review time, error/revisit rate, available evidence and who controls the budget. Interviews have not been conducted in this research.

## Six project candidates

### 1. Repair Evidence Review — automotive business

**Mode:** proposed partner product, BYD Royal Motors aftersales quality-control unit. **Process:** review of visible bodywork evidence before a repair case is closed.

Input: a declared repair checklist plus corresponding before/after panel photos. Output: an evidence packet identifying visible change in the requested region, unchanged-looking regions, missing views and cases requiring review. It supports a reviewer; it cannot certify structural repairs, paint quality or roadworthiness from photographs.

Pipeline: photo-quality gate → panel/region matching → image registration with an alignment-confidence gate → local change analysis → checklist coverage → evidence report. Reflection, camera movement and cleaning are alternative explanations for change. An unalignable pair returns a retake request.

Live jury input: fresh paired photos and a chosen visible region; the jury can supply mismatched views or leave a requested view out. Testing painted sample panels is permissible if declared, but does not establish real-car repair performance.

Measure alignment success, false change flags on unchanged panels, detection of labelled visible changes, checklist coverage and reviewer time. Split by physical panel/car and capture session, not random neighbouring frames. Local paired repair images are the main data risk.

Potential advantage: locally annotated matched panels, uncertainty handling and the repair-review integration. None is a defensible moat yet. Related to Handover Diff, but asks whether the requested repair has sufficient visual evidence rather than whether a customer caused new damage.

Full proposal: [repair-evidence-codex.md](repair-evidence-codex.md).

### 2. Parts Verification — automotive business; refinement of PartsLens

**Mode:** proposed partner product, Royal Motors parts and warehouse unit. **Process:** check a picked part against the requested item before it reaches the technician.

Input: expected item record, reference catalogue and new photos of the actual item/label. Output: likely match, contradiction, ambiguous match or outside catalogue, with the exact evidence for a clerk to confirm.

Pipeline: part crop → visual embedding retrieval → OCR of printed/stamped identifiers → identifier and catalogue checks → uncertainty/rejection gate. Similar shape must not override a conflicting part number. Exact vehicle fitment requires an authoritative catalogue; it cannot be inferred from appearance alone.

Live jury input: photograph a physical item, a similar-looking substitute or an unknown item. The prototype needs actual parts on the table and separately photographed references. It can support a bounded catalogue while correctly rejecting unsupported items.

Measure false acceptance of wrong parts first, correct retrieval on supported items, unknown-item rejection and retake rate. Use new capture sessions and unfamiliar objects as negatives. Include glare, worn markings and visually similar variants.

Potential advantage: dealer-specific reference records, measured rejection and job integration. Partium already offers visual/semantic search; basic embeddings are easy to reproduce. This is an extension of [PartsLens](parts-lens.md), credited to claude-2, not a separate new idea file.

### 3. Charger Fault Triage — automotive/EV business

**Mode:** startup selling to charging-site operators. **Process:** structure an incoming fault report before technical support reviews it.

Input: fresh photos of a supported charger display and model label. Output: visible status/error text, the matching manufacturer-reference passage and a support ticket, or a request for a better photo. Unsupported equipment and undocumented codes remain unresolved.

Pipeline: model identification → display/label rectification → OCR → validated code matching → versioned manufacturer reference lookup → grounded report. An optional LLM formats evidence but cannot invent a code meaning. A photo does not establish the electrical root cause or permission to repair hardware.

Live jury input: fresh photographs of supported equipment or a separately declared printed/display sample, then a glare/unknown-code case. Sample screens test capture/OCR only, not real fault diagnosis or field reliability.

Measure exact code extraction, correct reference matching, abstention on unfamiliar codes and support-review time. Biggest dependencies are readable displays, licensed reference material and access to a real supported charger family.

Potential advantage: locally labelled screen examples and hardware-specific mappings where network telemetry is unavailable. Validate that operators actually lack usable telemetry; Spark already handles logs. Full proposal: [charger-triage-codex.md](charger-triage-codex.md).

### 4. Crossing Conflict Review — road safety; refinement of Junction Risk Map

**Mode:** startup selling to road-safety consultants or municipal traffic-engineering teams. **Process:** find interactions worth reviewing in a static-camera clip and assess changes after an intervention.

Input: a new consent-compliant clip plus a marked crossing/conflict zone; calibrated ground-plane geometry when needed. Output: tracks, candidate conflict timestamps, evidence clips and event counts relative to observed traffic exposure. Counts from unequal observation periods are not directly comparable.

Pipeline: road-user detector → tracking → camera/zone setup → conflict-zone occupancy timing → event selection → reviewer queue. Track uncertainty and occlusion must suppress unreliable calculations. No legal fault assignment or unsupported prediction of crashes.

A useful measure is **post-encroachment time (PET)**: time between one road user leaving a conflict location and another arriving there. [FHWA's SSAM report](https://www.fhwa.dot.gov/publications/research/safety/08051/02.cfm) explains trajectory-based surrogate measures; its simulation method and historical defaults do not automatically validate camera estimates or a universal danger threshold. TTC projects continued motion toward a possible collision; it is more sensitive to trajectory assumptions.

Live jury input: unseen static-camera video and a zone selection. Measure event precision/recall against independently labelled clips, PET timing error and processing speed. Separate staged/synthetic sequences from real-world evaluation. No assumption that public CCTV is consent-compliant.

Potential advantage: team elimination code, if actually accessible and reusable, plus locally labelled events and a review pipeline. Existing code has not been inspected in this research. VivaCity already offers near-miss analysis. This refines claude-1's Junction Risk Map rather than creating another duplicate file.

### 5. Crosswalk Visibility Audit — road safety

**Mode:** startup selling to road-maintenance contractors/municipal asset teams. **Process:** turn approach imagery into a maintenance-review ticket.

Input: guided photos/short video approaching a known crossing. Output: annotated evidence of supported visible issues such as faded marking appearance or an obscured sign, capture gaps, and a proposed maintenance ticket for human approval.

Pipeline: crossing/sign localisation → view and quality gate → region-level appearance/occlusion analysis → evidence aggregation → maintenance category. For an MVP, choose one issue and constrain capture; a vague all-purpose road-safety score is difficult to validate. Arbitrary photos cannot establish sight distance in metres, illumination in lux or sign retroreflectivity.

Live jury input: new supported crossing imagery, including a poor view that should request recapture. A printed-image test can test capture mechanics, but is not proof of physical road visibility assessment.

Measure issue precision/recall, false tickets and abstention on unassessable views. Collect empty local crossings without unconsented people/plates, subject to safe lawful access; annotate site-level held-out examples. Wet/night capture requires separate evaluation; digitally darkened images are only a stress test.

Potential advantage: local capture protocol, labelled defects and linking ticket creation to later matched-view repair evidence. Road-asset vision is established; local data must be collected before claiming it as an advantage. Full proposal: [crosswalk-audit-codex.md](crosswalk-audit-codex.md).

### 6. Work-Zone Evidence Audit — road safety

**Mode:** startup selling to roadworks contractors. **Process:** supervisor review of visible temporary traffic-control setup against a supplied checklist.

Input: approach images/video plus expected visible signs/barriers/cones. Output: evidence-backed checklist, absent/not-observed/uncertain items and a correction ticket. Items outside the camera view are not automatically missing.

Pipeline: item detector → frame deduplication/tracking → view-coverage check → supported checklist reconciliation → evidence report. Start with a structured checklist, not arbitrary engineering drawing interpretation. Metric spacing requires calibration; the MVP does not certify legal compliance.

Live jury input: change a controlled physical layout or upload a new supported scene. Small props/synthetic scenes must be declared and scored separately from real roadworks. No entering an active work zone to manufacture demo footage.

Measure supported-item detection, false missing-item alarms, correct uncertainty handling and time to review a setup. Compare real and staged scenes separately. Local plans, expert labels and footage permissions are the main dependencies.

Potential advantage: locally validated checklist rules and evidence-to-correction tracking for small contractors. Blyncsy already offers equipment detection and plan-versus-reality checks. Full proposal: [workzone-audit-codex.md](workzone-audit-codex.md).

## Which should we shortlist?

These are engineering judgments, not jury scores or measured feasibility:

| Candidate | Best reason to pursue | Condition before choosing | Main weekend risk |
|---|---|---|---|
| Parts Verification | Bounded catalogue; strong fresh-photo jury test; a decision with observable errors | Physical parts, references and permission to use identifiers/catalogue data | Look-alikes and insufficient wrong-item negatives |
| Repair Evidence Review | Specific aftersales workflow and visual evidence trail | Real matched before/after images and an agreed review task | Alignment/reflections can masquerade as change |
| Charger Fault Triage | Clear support-intake action without a telemetry integration | One accessible charger family and usable manufacturer references | OCR-only prototype may have limited technical originality |
| Crossing Conflict Review | Highest technical potential if elimination code is available | Working reusable tracker, compliant clips and event labels | Calibration/tracking errors and weak live-input access |
| Crosswalk Visibility Audit | Direct maintenance action; local evidence can be collected | Supported issue detectable on real local imagery today | Reliable defect labels and localisation are not assured |
| Work-Zone Evidence Audit | Distinct contractor workflow and inspectable checklist | Suitable scene data and a supervisor's checklist | Toy-only demonstration and existing direct competition |

**Provisional recommendation:** Parts Verification for automotive business if physical parts are available; Crossing Conflict Review for road safety if the elimination pipeline and compliant videos already exist. Otherwise investigate a narrowly scoped Crosswalk Visibility Audit. Repair Evidence Review is commercially interesting but should not be chosen without matched imagery. None is guaranteed buildable in eight hours.

Before committing, run a small feasibility check on new real inputs, verify all data/model licences, deploy a minimal upload path, and ask the prospective process owner whether the output changes a real decision. No implementation has been started.

## How the selected idea meets the finals requirements

- **Technical complexity (25%):** show the capture gates, CV stages, retrieval/geometry/rules, uncertainty handling, evidence trail and evaluation. An LLM may explain computed findings; it must not substitute for them.
- **Innovation (25%):** identify what exists already, show an ablation against a simple baseline and explain the specific integration/data advantage. A weekend prototype does not automatically possess a moat.
- **Impact (25%):** name the process owner, payer, current method and pilot KPI. A three-month pilot should progress from permissions/baseline collection, to shadow review, to supervised workflow use with an operational comparison. Partner deployment and municipal procurement remain unconfirmed.
- **Presentation (15%):** public phone/laptop upload, a fresh supported jury input, an honest uncertainty/failure example and a recorded backup. Deploy frontend/backend from the submitted repo and record the running commit before freeze.
- **Business (10%):** obtain actual review time and operating costs, state proposed prices as assumptions and separate operational savings from unproven safety outcomes.

## Data, evaluation and deployment common to all candidates

Use self-collected authorised images where possible, recording ownership, consent, collection method and permitted use. Avoid capturing unconsented faces/plates in the first place; later blurring alone is not evidence of permission. Public visibility is not automatically permission for this challenge. Catalogue images, manuals, model code and model weights each need their own licence review. [CarDD's original terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf) require permissions; do not treat an unofficial permissive mirror as authorisation. No data or weights have been downloaded by this research.

Hold out objects/sites and capture sessions. Include unfamiliar inputs, similar negatives, blur, glare, local equipment/vehicles, actual night and wet conditions when available. Label synthetic/staged cases separately. Report sample count, ground-truth method, errors and limits. Where no night/rain examples exist, write **not evaluated** and return uncertain/retake when evidence is inadequate.

Initial proposed architecture: mobile browser capture/upload → server-side CV and task logic → evidence/result display. Server CPU is a candidate for bounded photo retrieval/OCR; video detection may need a GPU. Hosting, model, hardware, speed and cost are not selected or measured. Benchmark end-to-end upload-to-result time and p50/p95 latency on the chosen hardware, including queueing/cold starts; record video processing rate at a stated resolution.

Cost per case = compute/API + allocated storage/network + human-review labour + expected retake cost. Monthly pilot cost also includes people, collection/annotation, integration, infrastructure and licences. Proposed billing bases: per completed inspection/review or per active counter/site/camera-month, depending on buyer workflow; prices are unverified.

Monthly net benefit = measured review-time savings + evidenced error/revisit savings − recurring product cost. Avoid double counting saved work. Payback = initial pilot investment / positive monthly net benefit. If net benefit is zero or negative, no positive payback is established. Do not monetise prevented crashes without defensible evidence.

## Second-pass shortlist: all team ideas and supplied screenshots

Bexruz requested a fresh comparison across all researched ideas, not just the screenshots. He confirmed that **physical parts, paired car captures, and usable traffic code/videos are not currently available to his team**. Therefore no candidate below is approved for implementation or guaranteed ready to demonstrate. Product merit and present build readiness must be distinguished.

Reviewed the full team landscape, TrueClaim, RoadProof, dealer/service research and all eleven screenshot concepts. The strongest narrowed candidates are:

| Candidate | Concrete decision and proposed buyer | Why shortlist it | Required evidence / main risk |
|---|---|---|---|
| **Service Handover Guard** (Workshop Intake + Handover Diff + LensCheck) | Proposed Royal Motors service reception: document arrival, compare departure and request review of possible changes | Guided capture, matching, quality/coverage gates and evidence comparison serve one process | Access to a car and genuinely matched views; reflections/angle changes cause false alarms; cannot assign blame |
| **Warranty Evidence Review** (narrowed WarrantyProof / TrueClaim) | Proposed Royal Motors warranty desk: find reused submitted images, conflicting identifiers and missing views; request evidence or manual review | Historical-image retrieval + OCR/record consistency + completeness creates an inspectable review system | Authorised seeded image history and supported part records; a repeated image can be legitimate; no reliable universal real/fake verdict |
| **Parts Verification** (PartsLens refinement) | Proposed Royal Motors parts counter: compare picked item with requested catalogue entry | Bounded task, strong fresh-photo test and observable wrong-item errors | Real items/reference records are currently absent; appearance cannot establish fitment or authenticity |
| **Service Video Evidence Auditor** (narrowed MPI Video Auditor) | Proposed Royal Motors aftersales supervisor: check whether the named component and required evidence views appear before sending a recommendation | Links recommendation to timestamped visual evidence, rather than just summarising a video | Own supported technician clips and labels; start with evidence coverage, not mechanical diagnosis or guessed depth |
| **Crossing Conflict Review** (Junction Risk Map + Pedestrian Risk Analyzer) | Startup for traffic consultants: find candidate interactions in fixed-camera clips and prepare exposure-aware reports | Tracking, zone timing, event uncertainty and review form the strongest road-safety technical case | Existing pipeline/compliant footage not available yet; calibrated geometry and independent event labels needed |
| **Road Repair Evidence** (RoadProof refinement) | Startup for road-maintenance contractors: create defect ticket, then check whether a matched follow-up view adequately documents the same spot | A closed ticket-and-follow-up workflow is stronger than a generic pothole map | Genuine paired sites are absent; photos show surface appearance, not structural quality or repair durability |

### Additional primary-source checks

- [Dealerware's July 2026 support article](https://support.dealerware.com/hc/en-us/articles/53458053275283-Vehicle-Walkaround-Inspection) documents guided zone photos, comparison and reports; it explicitly says automatic AI damage detection is not in that initial release. This establishes a workflow and one supplier's stated scope, not a globally unoccupied market.
- [Truepic's warranty article](https://www.truepic.com/blog/snapshot-impact-of-image-authenticity-for-the-auto-warranty-industry) describes reused images/objects and recapture as evidence issues. Its savings/fraud figures are vendor claims and are not used to predict our results. Image similarity finds a review lead, not proof of fraud or repeated physical-object identity.
- [myKaarma's August 2026 MPI article](https://mykaarma.com/blog/the-multi-point-inspection-process-step-by-step/) describes linking recommendations to visual evidence and AI review of clarity/completeness. A generic video grader therefore has direct prior art. Our proposed narrower experiment links a supported recommendation to specific component views and timestamped evidence gaps.
- [Partium](https://docs.partium.io/partium-find/partium-search-engine/how-partium-image-part-search-works/), [VivaCity](https://info.vivacitylabs.com/near-miss-feature-smart-road-safety) and [Blyncsy](https://blyncsy.com/pavement-inspection-asset-inventory/) remain relevant competitors for parts search, conflicts and road assets. No claim of global novelty is supported.

### What no ready inputs changes

Previously Parts Verification was recommended **if physical parts were available**. That condition is not met. It remains a strong bounded product but should not be selected today on assumed access.

Service Handover Guard is my strongest dealer-service concept **if access to a car and matched captures can be secured**. Warranty Evidence Review is worth the first data-access check when hardware is unavailable: its duplicate/consistency stages can be explored using authorised images and explicitly seeded records. Such experiments are not evidence of actual fraud detection or local warranty savings. Crossing Conflict Review remains the strongest road-safety technical option only if suitable clips and a working baseline can be obtained.

The [Humans in the Loop original dataset page](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/) now appears in primary-source search with explicit **CC0 1.0** terms. It lists exterior car-panel parts and damage annotations. This may support initial localisation experiments after access/content checks; it is **not** a spare-parts identity catalogue, a matched before/after set or warranty history. Access is through a form and has not been requested. Image contents still need challenge-specific privacy review. Previously inaccessible licence information is now partially resolved; no dataset has been downloaded.

The original [RoadDamageDetector README](https://github.com/sekilab/RoadDamageDetector/blob/master/README.md?plain=1) distinguishes MIT code from CC BY-SA image terms and describes privacy processing. Those statements should not be blanket-applied to every RDD2022 release or external pretrained weight file; verify the exact asset used. Missing weight licences are unresolved, not automatically inherited from a library.

### Feasibility gates before a build choice

1. Obtain and inspect authorised, relevant inputs; record provenance/licences/consent and avoid forbidden faces/plates. Do not assume a public photo or later blur proves permission.
2. Define one supported decision and failure/uncertainty outputs. Test on new captures or independently labelled held-out inputs.
3. Compare against a simple baseline: manual side-by-side review, exact duplicate hash, identifier-only matching or existing detector. The more elaborate pipeline must show why it helps.
4. Measure error rate, review/retake workload and speed on actual hardware. Deploy the upload/result flow early; do not invent thresholds, FPS, savings or completed integration.
5. Select after the evidence check. Local data and workflow integration are potential future advantages; they are not existing moats.

Lower-priority choices for this deadline: generic car inspection, generic driver coaching/fatigue, lot counting, uncalibrated tyre/chain-depth measurement, repaint/history inference, live motorcycle blind-spot protection, generic visibility scoring, charger OCR without real screens, and work-zone auditing without real scenes. These may be useful products, but currently lack a clear combination of distinguishable technology and accessible validation inputs. Camera-visible hand/tool motion alone does not establish that a bolt was tightened to the correct torque; EV shape/occupied bay alone does not establish a charging session; absence of metadata alone does not establish manipulation.

## Comments

<!-- other agents may append comments here -->
