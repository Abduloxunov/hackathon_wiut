---
name: Parts Order Verification
added_by: Bexruz + codex, refining Bexruz's supplied concept
date: Sat 10 Oct 2026
direction: dealer / service operations
mode: partner product (proposed Royal Motors parts counter)
---

# Parts Order Verification

**One line:** A fresh part photo and its printed label are checked against the expected order, so a parts worker can investigate a mismatch before handing it to a mechanic.

## Problem and user

Two parts may look almost identical but fit different vehicle variants. The counter worker uses this assistant; the dealership's parts/aftersales manager would pay. We need records or interviews to establish local wrong-pick frequency and correction costs. There is no assumed access to Toyota/BYD/Ducati catalogues.

[Partium's documentation](https://docs.partium.io/partium-find/partium-search-engine/how-partium-image-part-search-works/) shows that image/text part search combined with catalogue master data already exists. Our proposed improvement is a small, auditable verification step for a known order, rather than claiming universal part recognition from a photo.

## What the product does

- **Input:** Expected part/order record, fresh photos of the part and its label, and an authorised small catalogue/reference gallery.
- **Context data:** OEM identifiers and supersessions, vehicle model/year/variant and applicable fitment records, expected quantity and inventory bin. The public demo uses a declared synthetic order, never real customer/VIN records.
- **Output:** Ranked candidate matches, readable label text, specific agreement/conflict with the order and missing evidence. The result is supported match for worker confirmation, mismatch requiring review, or unknown.
- **Decision:** Recheck the label/part or consult the authoritative fitment record before release. No automatic stock write or purchase order is required.

For example, a photo resembles a brake component but its label differs from the expected code. The app highlights the code conflict even when visual similarity is high. If no trusted code or fitment record exists, it cannot certify compatibility. It also cannot establish authenticity or internal quality from appearance.

## Tech and data

Pipeline: crop and quality check → OCR of label/markings → visual embedding retrieval against known references → compare identifiers and fitment rules → combine evidence with an unknown-state threshold → worker review. DINOv2 is a candidate for visual embeddings; select a licensed OCR implementation and verify its exact checkpoint. Optional masks isolate the part from packaging. Dimensions require a calibration object and geometry; do not treat unscaled pixel size as a reliable physical measurement.

Build a small reference set from the team's own or authorised photographed parts, with a verified identity for every catalogue entry. Capture different sessions/backgrounds and near-identical alternatives. Keep new query photos separate from the reference photos. Include out-of-catalogue objects, unreadable labels and deliberately mismatched orders. A gallery made from household objects can test retrieval only; it is not automotive fitment validation. No parts or authorised records are available yet.

Catalogue access does not automatically allow copying its images or redistributing its records. Record catalogue permission, collection/consent, model/code/weight terms and attribution under the [shared rules](refined-six-ideas-codex.md). The exterior car-part dataset is not a database of loose OEM components. Never scrape a commercial catalogue as an assumed licence workaround.

## Evaluation and real conditions

Measure top-1/top-3 retrieval, exact identifier-reading accuracy, mismatch recall, wrong-match release suggestions and unknown rejection. Report results separately for label readable, label unreadable, lookalikes and unfamiliar objects. Compare image-only retrieval, OCR-only matching and the combined pipeline. Hold out capture sessions, and explain that the MVP covers only its enrolled catalogue.

Start with server inference and a phone capture UI. Benchmark warm/cold query latency, catalogue size, input resolution and cost per verified query. Night, grease, reflective packaging and local supplier labels need separate tests; poor visibility triggers a retake. No plate recognition is needed. Nothing is measured yet.

## Business and pilot

Possible pricing is a site subscription, including catalogue onboarding. Measure search/verification time and documented wrong picks intercepted, with review time and false alerts included. Costs include photographing/cataloguing parts, access/licence fees, expert labelling, compute/storage and updating supersessions. Do not count every flag as a prevented return. Use the [shared budget and payback formulas](refined-six-ideas-codex.md).

Three-month pilot: agree one category, obtain authoritative records, enrol references and operate beside the normal parts check. Audit worker-confirmed mismatches and monitor catalogue changes. The possible advantage is a trusted local reference/fitment library and correction feedback; today it is a proposed data asset, not a moat we already possess.

## Can we build it in ~8 h?

Conditional MVP: a small known catalogue, fresh-photo search, label OCR and expected-order comparison. The jury supplies a new photo of an enrolled part, an unknown object or a different order code. Actual OEM compatibility is shown only for entries with trusted records. Without physical parts and records, this loses its strongest business claim.

Credit PartsLens by Muhammadjon/claude-2 and Bexruz/codex's earlier [Parts Verification proposal in PR #3](https://github.com/Abduloxunov/mdb-vision-finals/pull/3). This is a refinement of those ideas. Broad stock counting, universal identification and automatic ordering are excluded.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
