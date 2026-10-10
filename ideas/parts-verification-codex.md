---
name: Parts Verification
added_by: Bexruz + codex, refining claude-2 PartsLens
date: Sat 10 Oct 2026
direction: dealer/service operations
mode: "Partner product: proposed Royal Motors parts-and-warehouse unit"
---

# Parts Verification

**One line:** Requested catalogue item + picked part/label photographs → likely match, conflicting identifier, ambiguous or unknown → worker confirmation before technician handoff.

## Problem and user

A warehouse worker needs to check that a picked part matches the requested item. Similar shapes, missing packaging or worn labels can make this difficult. Local error frequency and time cost need observation; no wrong-part rate is established.

- User/owner: parts-counter clerk or warehouse picker; technician confirms if necessary.
- Proposed payer: Royal Motors parts department; no commitment or catalogue access.
- [Partium documentation](https://docs.partium.io/partium-find/partium-search-engine/how-partium-image-part-search-works/) describes image/text search and visual comparison with master records. Search is established prior art; our proposed decision is picked-item verification.
- Credits: claude-2's [PartsLens](parts-lens.md) and Bexruz's parts-identification screenshot.

## What the product does

1. Worker selects a requested item in the supported reference catalogue.
2. Takes a fresh part photograph and label/number close-up.
3. App searches reference appearance and reads the identifier.
4. Compares both with the requested item and exposes contradictions.
5. Worker reviews evidence before the handoff.

- Input: fresh part/label photos and trusted requested-item record with reference images/identifiers.
- Output: likely match, conflicting identifier, ambiguous candidate set, outside catalogue, unreadable evidence or retake. An appearance match never overrides a conflicting identifier.
- Live jury test: photograph a supported physical part from a new angle, a look-alike wrong item and an unknown object; change the requested item. Results come from the actual photos and records.
- Boundary: exact vehicle fitment requires authoritative vehicle/catalogue data; identity/compatibility does not establish product authenticity or safety. No counterfeit verdict from appearance alone.

## Tech (why it is a system, not one API call)

Capture-quality gate → object localisation/background isolation → visual embedding retrieval → OCR of printed/stamped identifiers → authoritative record checks → ambiguity/open-set rejection → evidence comparison. Optional reference-marker dimensions require actual calibrated geometry; no guessed scale from an arbitrary image. Human confirmation is explicit.

- Data needed: real parts with independently verified records; own authorised reference captures from multiple views; fresh sessions plus visually similar and out-of-catalogue negatives. User currently has none. Exterior car-panel datasets are not a spare-part identity catalogue. Do not scrape copyrighted catalogue imagery without permission; check code/weights separately.
- Proposed inference: server CPU for a bounded gallery, benchmark encoder/OCR and whole case; GPU only if justified. Speed/cost unmeasured.
- Local/night/rain: test local markings/languages, grease, worn numbers, glare, dim/wet surfaces. Unreadable/unsupported input returns uncertain. No plate/customer recognition.
- Public deployment: browser camera/upload and requested-item selection → server search/OCR → explainable comparison page from submitted repo.

## Quality and validation

Prioritise false acceptance of a wrong part. Measure supported-item retrieval, OCR errors, look-alike rejection, unfamiliar-item rejection, retake rate, worker review time and latency. Split reference/query captures by session and include new unknown physical objects. Compare identifier-only matching and visual-retrieval-only baselines; show the contradiction gate's contribution.

## Why hard to copy

Potential future advantage: dealer-specific catalogue/gallery, measured confusing-item behaviour and job integration. No current moat. Generic visual search is easy to reproduce; a bounded gallery is a disclosed prototype scope, not universal recognition.

## Business

- Proposed billing: per active counter/month or completed verification; price unverified.
- Cost: compute/storage/reference upkeep plus review/retake labour; see [shared model](cv-shortlist-codex.md#shared-pilot-cost-model).
- Validate checking time, returned wrong items and interruption/revisit costs. Do not assume visual matching prevents every installation error.
- Three-month pilot: permissioned catalogue/items and manual baseline → shadow verification → supervised counter use with measured operational comparison. Inventory/repair-order integration is future scope.

## Can we build it in ~8 h?

Conditional MVP: small declared catalogue, physical items, new-photo retrieval, readable identifier check, mismatch/unknown/retake output. Biggest blocker is acquiring parts/records; biggest technical risk is visually identical variants with unreadable numbers. Previously recommended only if physical items were available; that condition is currently unmet. No build selected.

## Comments
<!-- Other agents may append comments. -->
