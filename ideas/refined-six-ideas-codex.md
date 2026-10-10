# Six supplied CV concepts — refined proposals

Author: Bexruz + codex, 10 Oct 2026. These are proposals for lead review, not a product selection or an implementation. No real inputs, partner access, trained task-specific weights, measured metrics or validated revenue are available for this batch. The lead's dealer/service focus remains in force. Road-safety concepts are alternatives requested by Bexruz; adopting one would require a lead decision.

## Read the six proposals

| Supplied concept | Refined product | Actual decision | Essential context beyond CV |
|---|---|---|---|
| Damage, condition and cost inspector | [Vehicle Damage Evidence & Estimate Review](vehicle-damage-review-codex.md) | Retake or appraiser/bodywork review | Supported vehicle/panels, authorised repair operations and dated rate card |
| Pre-delivery / service-bay inspection | [PDI Evidence Checklist Assistant](pdi-evidence-assistant-codex.md) | Complete evidence or supervisor sign-off | Variant-specific references and approved checklist |
| Motorcycle gear, posture, fatigue and hazards | [Rider Gear Evidence Review](rider-gear-review-codex.md) | Instructor reviews a helmet-visibility event | Camera visibility and coaching policy |
| Dashcam hazard mapper | [Road Hazard Tickets & Follow-up](road-hazard-tickets-codex.md) | Confirm a unique maintenance ticket | Genuine location/time, route importance and maintenance rules |
| Photo-to-OEM/inventory search | [Parts Order Verification](parts-order-verification-codex.md) | Recheck a possible wrong part before release | Expected order, trusted identifiers and fitment records |
| EV charging/parking monitor | [EV Bay Occupancy & Session Review](ev-bay-state-review-codex.md) | Operator checks blocking or conflicting evidence | Bay geometry, fresh charger/session records and dwell policy |

Every proposal uses computer vision as a necessary evidence source, combines it with declared context and ends in an action. Extra models are justified by the workflow, not added merely to make the architecture look complicated.

## Which should we explore first?

This is a conditional feasibility order among these six, not jury scores, a replacement for the previous all-branch ranking, or evidence that the team has chosen a build.

| Order | Proposal | Why consider it | Go/no-go evidence before building |
|---|---|---|---|
| 1 | Damage Evidence & Estimate Review | Direct partner fit, clear visual result, traceable business decision | Licensed damage-trained checkpoint works on fresh real photos; supported car/panels available; authorised rate card for any real price claim |
| 2 | Parts Order Verification | Focused dealer workflow; OCR and visual evidence can catch different errors | Actual parts, trusted identities, lookalikes and permitted order/fitment records |
| 3 | Road Hazard Tickets, photo-first | Best fallback road-safety option in this batch; actionable output without pretending GPS exists | Working licensed detector and permitted fresh road images; real GPS before promising a map |
| 4 | PDI Evidence Checklist | Strong dealer fit and useful checklist context | One supported variant, matching references and an approved visible checklist |
| 5 | EV Bay Occupancy & Session Review | Feasible occupancy demo; real session fusion could add value | Permitted fixed-view footage; access to fresh telemetry for charging-state claims |
| 6 | Rider Gear Evidence Review | Relevant road-safety use and Ducati angle | Helmet-trained weights, suitable consenting clips and a credible instructor user; no assumption that a forward dashcam sees its rider |

The first idea follows Bexruz's recommended damage-plus-cost direction, but does not make cost estimation a model guess. Without the required inputs, its position drops. Parts can move first if physical samples and records become available. Road tickets are the most practical road-safety alternative here. PDI and EV require more site-specific setup; rider gear alone has substantial prior art and a weaker fit with the lead's focus.

The team's existing **Warranty Evidence** and **Handover Guard** remain strong candidates outside this six-idea batch. See the [lead's combined digest](DEALER-SERVICE-ALL-IDEAS.md) and [Codex's prior refinements in PR #3](https://github.com/Abduloxunov/mdb-vision-finals/pull/3). Do not merge every feature into one finals product: pick one owner, workflow, measurable outcome and demo. Adding damage, fraud, parts, telemetry and safety alerts at once would make credible validation harder.

## Shared engineering and licence gates

1. Obtain a real input and a working baseline before building screens. A pretrained general detector is not automatically a damage, helmet or road-defect detector. A segmentation tool does not diagnose the region it outlines.
2. Record exact code version, checkpoint source/hash, model terms, training/evaluation data terms and attribution separately. Prefer the lead's suggested permissive building blocks where suitable, but check the actual artifact. Repository licensing does not automatically cover all weights or data. Follow the lead's restrictions on Ultralytics and original SuperPoint/SuperGlue. Commercial/catalogue access requires its own permissions.
3. No downloaded weights, datasets or videos go into git. Share authorised assets through the team's agreed storage and document sources, licences and generation/collection methods. Public availability does not imply consent or reuse rights. Exclude unconsented identifiable faces/plates and confidential customer records; public demos use synthetic case/order details.
4. Initial architecture: browser capture/upload → server inference → deterministic evidence/context rules → review report. A public frontend and backend must actually run from the submitted repository. Any LLM explains structured findings only; include its cost and prevent unsupported assertions.
5. Guided capture, abstention and human review are product features. Make unsupported inputs, missing references, stale telemetry and low visibility visible. Never turn absence of evidence into a safety certificate, fraud conclusion or automatic financial approval.

## Shared measurement protocol

Record actual hardware (CPU/GPU/RAM), deployment tier, model/version, resolution and image count or video duration. Measure cold start separately from warm operation. Report upload, decode, inference and report time, including end-to-end median/p95 over the stated sample count. For video, distinguish processed frames/second from real-time stream capacity and include queueing. Public-demo latency includes the network; model-only speed is insufficient.

Build an independently labelled small test set, keep cars/routes/riders/parts and capture sessions separated as appropriate, and retain clean negatives and hard cases. Report sample counts per condition, false positives, missed cases and unknown coverage. Compare one relevant simple baseline with the full pipeline and show failure examples. Night, rain and local-domain quality need separate evidence; absent coverage is **untested**, not robust. Synthetic or prop tests must be declared and cannot establish real-world accuracy. All proposed quality and speed metrics remain unmeasured.

## Shared budget, unit cost and ROI

Choose currency and date and list every source/assumption. Obtain actual hosting quotes and partner baselines before putting financial figures in the deck. No budget, selling price, payback or customer agreement is validated here.

- **Pilot build cost:** people-hours × agreed rates + collection/annotation + equipment/setup + catalogue/data/model licences + integration and testing.
- **Monthly operating cost:** compute + storage/network + paid API usage + support/maintenance + staff review. Include idle hosting; do not count only GPU seconds.
- **Unit cost:** monthly operating cost / successfully completed inspections, queries, video minutes or camera-hours. Define the unit and utilisation, and show low-utilisation sensitivity. Include failed uploads and retries in costs.
- **Validated monthly benefit:** completed eligible tasks × net minutes saved × labour cost/minute + separately documented errors/interventions avoided. Subtract correction/false-alert burden and avoid double counting. Do not assume every flag prevents a crash, claim payment or lost sale.
- **Net monthly benefit:** validated benefit minus incremental operating cost. **Pilot payback months:** pilot build cost / positive net monthly benefit; if benefit is zero or negative, there is no finite payback. Subscription gross margin is price minus fully allocated delivery cost; partner labour savings are not startup revenue.

For each proposal, obtain the buyer's existing-process baseline, run shadow review before operational decisions and confirm applicable local data/workplace/sector rules with the partner. A three-month plan is conditional: month 1 secure permissions/inputs and baseline; month 2 shadow pilot and error audit; month 3 limited supervised use and ROI review. The proposal is not regulatory clearance.

## Demo, defence and freeze

Deploy early, test the actual public HTTPS site on another phone/laptop, and accept a new jury input for the supported scope. Reports must come from actual inference and context processing. A displayed synthetic rate card or telemetry feed is a declared test input, not a disguised live integration. Keep a recorded backup, failure examples and an architecture diagram. State the chosen mode on slide 1.

Use the challenge's seven minutes: problem/user 1, live demo 2, architecture/quality 2, budget/ROI 1.5, pilot steps 0.5. Every member should understand the code, attribution and limitations for Q&A. Submit the source/data-licence list and deployment from this repository; record the deployed commit and deployment history. Code freeze is Sun 11 Oct 13:00 Tashkent; after it only redeploying the submitted commit is allowed.

## Attribution and references

Original six concepts and demo suggestions: Bexruz's supplied message. Earlier team contributions: TradeIn PreCheck, RoadProof, RoadGuard, PartsLens, ChargeBay Watch (Muhammadjon/claude-2); dealer/PDI, EV Bay Guard and rider research (Davlatyor/claude-1); earlier parts, repair, warranty and handover refinements (Bexruz/codex, [PR #2](https://github.com/Abduloxunov/mdb-vision-finals/pull/2) and [PR #3](https://github.com/Abduloxunov/mdb-vision-finals/pull/3)). These are focused refinements, not six claimed inventions.

See [demo/reference checks](demo-reference-checks-codex.md). Competitors and borrowed methods are attributed there and in each proposal. Local data, integration and domain rules are potential future advantages; none should be called an existing hard-to-copy moat without evidence.
