# Selected computer-vision ideas for the finals

Prepared by Bexruz + codex, Saturday 10 October 2026. This is a recommendation shortlist, not the lead's final build decision. It contains only computer-vision products for automotive business or road safety.

## Recommendation

**Service Handover Guard is the strongest overall product concept if matched car photos can be obtained. Crossing Conflict Review has the strongest road-safety technical potential if suitable clips and a baseline tracker can be obtained.** Warranty Evidence Review is worth the first digital-data feasibility check when physical inputs are unavailable. Parts Verification is a strong bounded alternative once real items and trusted records are available. Bus-Stop Access Monitor is the clearest additional road-operations candidate, with a weaker originality case than calibrated conflict analysis.

Bexruz confirmed that physical parts, matched car captures and usable traffic inputs are not currently ready. Therefore none of these is represented as ready to build or proven feasible in eight hours. No customer interviews, measured accuracy, speed, operating costs, savings or partner commitments exist for these proposals.

| Selected idea | Direction / mode | Input → decision | Why selected | Gate before choosing |
|---|---|---|---|---|
| [Service Handover Guard](service-handover-codex.md) | Automotive business; proposed partner product at Royal Motors service reception | Guided arrival/departure photos → possible change / evidence gap / retake / human review | Capture, correspondence, alignment and evidence comparison serve a specific intake/handover process | Real matched images; test unchanged panels under changed lighting/angles |
| [Warranty Evidence Review](warranty-evidence-codex.md) | Automotive business; proposed partner product at Royal Motors warranty desk | Submitted part photos + declared history + record → reuse/identifier/coverage evidence → request more evidence or review | Retrieval, OCR and completeness create an auditable decision pipeline | Authorised reference/history images and supported records; false-positive evaluation |
| [Parts Verification](parts-verification-codex.md) | Automotive business; proposed partner product at Royal Motors parts/warehouse | Picked item photos + requested catalogue record → likely match / mismatch / ambiguous / unknown | Bounded reference set and observable wrong-item errors; fresh-photo demo | Real parts, trusted identifiers and similar/unknown negatives |
| [Crossing Conflict Review](crossing-conflicts-codex.md) | Road safety; startup for traffic consultants/municipal engineers | Fixed-camera clip + conflict zone → candidate events, timing and evidence review | Tracking, geometry, event timing, uncertainty and exposure-aware summaries | Compliant clips, independently labelled events and a working tracker |
| [Bus-Stop Access Monitor](bus-stop-access-codex.md) | Road safety; startup for transit/municipal operations | Fixed stop-camera clip + boarding region → obstruction episode → operator review task | Clear intervention, temporal evidence and repeat-observation workflow | Appropriate scene/camera geometry and labelled obstruction episodes |

These refine existing team concepts rather than claiming new authorship of all underlying ideas: claude-1's Handover Diff/Junction Risk Map/WarrantyProof; claude-2's LensCheck/TrueClaim/PartsLens; Bexruz's screenshot proposals. The bus-stop workflow came from the subsequent Codex road-safety research. Their original files remain unchanged.

## Why these fit the rubric

- **Technical complexity (25%):** multiple necessary CV stages, task logic, uncertainty and error analysis. Each must be compared with a simple baseline so complexity has a demonstrated purpose.
- **Innovation (25%):** established competitors are named in each proposal. Distinction must come from measured handling of ambiguity, local data or useful integration. None has an established moat today.
- **Impact (25%):** each names a process owner and an action. Local frequency, pain and buyer commitment still require validation.
- **Presentation (15%):** a publicly reachable phone/laptop upload flow must process a fresh supported jury input. A recorded backup helps when technical problems occur; it does not replace live processing.
- **Business (10%):** measure the current process, pilot operating costs and review burden; prices and ROI are assumptions until supported.

The lead's present build focus is dealer/service operations. The three automotive proposals align with it; road-safety proposals are alternatives included at the human's explicit request. This document does not change assignments, interfaces or the build scope.

## Shared data and engineering rules

Use authorised inputs with recorded ownership, collection/generation method, consent and licence. Avoid forbidden unconsented faces/plates. Public availability or later blurring alone does not establish permission. Verify model code, weights, catalogue images and manuals separately. No datasets, weights, videos or credentials go into git.

[Humans in the Loop's original page](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/) declares CC0 exterior-part and damage images. It may support initial localisation after access/content checks; it is not a spare-part identity catalogue, paired handover set or warranty history. Access has not been requested. [CarDD's original terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf) require permissions; a permissive mirror is not sufficient authorisation.

Hold out objects/vehicles/sites and capture sessions rather than randomly splitting adjacent frames. Separate controlled/synthetic examples from field results. Test relevant local equipment/vehicles plus blur, glare, occlusion and unfamiliar inputs. Actual night/wet examples need their own results; absent evidence is labelled **not evaluated**.

Proposed deployment: browser upload and required human setup → server CV/task logic → evidence/result page. CPU/GPU, provider and model are not selected. Measure upload-to-result time, p50/p95 latency, memory and cold-start behaviour on the actual hardware; for video report resolution, frame sampling and processing rate. Deploy frontend and backend from the submitted repo, record the commit and deployment history, and respect Sun 11 October 13:00 freeze; afterwards only redeploy the submitted commit.

## Shared pilot cost model

Proposed billing units are stated in each idea; no dollar or UZS price has been validated.

- Cost per case = compute/API + allocated network/storage + reviewer labour + expected retake work.
- Camera-month cost = hosting/processing + media retention + event-review labour + site/camera maintenance allocation.
- Pilot budget also includes people, collection/annotation, reference maintenance, integration, hardware and licences.
- Monthly net benefit = measured review-time savings + evidenced error/revisit savings − recurring total cost. Avoid double counting saved work.
- Payback = initial pilot investment / positive monthly net benefit. Zero/negative benefit does not establish positive payback. Do not monetise prevented crashes or avoided fraud without evidence.

## Decision process before building

1. Secure relevant authorised inputs and verify the exact asset licences.
2. Define one supported decision, labels and uncertainty behaviour.
3. Test a working baseline on fresh/held-out inputs, including difficult negatives.
4. Measure error and human review/retake workload, demonstrate the upload-to-result path, and benchmark the actual hardware.
5. Validate the output with the process owner; the lead then selects one product and assigns build work.

Conditional preferred order for the dealer/service focus: handover if matched captures are available; warranty evidence if usable digital records are available; parts if physical references are available. Road choices: crossing conflicts for greater technical potential; bus-stop access for a narrower operational task. This is qualitative judgment, not invented jury scores.

## Comments
<!-- Other agents may append comments. -->
