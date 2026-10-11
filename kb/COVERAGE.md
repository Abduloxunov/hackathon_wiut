# Knowledge coverage and open gaps

## Current record inventory

| Component | Records | Scope |
|---|---|---|
| Body paint/plastic/dents | K001-K005 | Generic material/repair assessment |
| Windscreen | K006-K007 | Generic glass assessment |
| Side-window glass | K008 | Generic, actual glass material required |
| Tyre | K009-K015 | Generic tyre guidance |
| Underbody/cabin fluids | K016-K018 | Candidate sources; colour is not a diagnosis |
| EV/hybrid incidents | K019-K020 | Requires confirmed EV/PHEV/HEV powertrain |
| Cobalt warnings | K021-K022 | Exact model and confirmed S11 manual |
| Lacetti warnings | K023-K024 | Exact model and confirmed S14 manual |
| Nexia wipers | K025 | Exact model and confirmed S12 manual |
| Damas refuelling | K026 | Exact model and confirmed S13 manual |
| Lamps | K027-K028 | Generic cover/function/condensation assessment |

## Requested vehicle coverage

| Vehicle | What we can currently support | Missing evidence |
|---|---|---|
| Cobalt | Two official-manual records, when edition applies | Exact model-year/variant metadata; common-fault frequency; MCM-specific content |
| Nexia | One official-manual wiper record, when edition applies | Generation-specific faults and prevalence |
| Damas | One official-manual refuelling precaution | Generation-specific fault records; fuel-leak diagnostics |
| Gentra | Generic component records only | Verified Gentra manual; do not substitute Lacetti automatically |
| Spark | Generic component records only | Official manual content was not successfully retrieved in this pass |
| BYD Song/Yuan | Generic component guidance; general EV/hybrid incident records when powertrain confirmed | Exact regional model/year/variant manual and manufacturer-specific fault records |
| Lacetti | Two additional official-manual warning records | Edition applicability; not automatically Gentra |

An owner's manual establishes operating guidance, not that a fault is common or caused by a particular part. No frequency or prevalence claim is made. A BYD model name alone does not establish EV versus plug-in-hybrid configuration. Generic component records can help any model only within their stated material/function limits.

## Connecting the CarDD labels

The planned dataset has six damage categories. These are observations, not diagnoses. Class IDs must come from the actual COCO category metadata; never assume a numerical order.

| Observed category | Candidate component/records | Additional context |
|---|---|---|
| `dent` | Body K005 | Panel, paint condition, attachments and hidden damage |
| `scratch` | Body K001-K003 | Actual component/material and coating depth |
| `crack` | Body K004; windscreen K006-K007; tyre K011/K014 only when component independently confirmed | Component and geometry; do not treat the class as automatic tyre/glass damage |
| `glass shatter` | Side window K008 only when that component is confirmed | Which glazing, actual glass material; windscreen shattering needs separate assessment |
| `lamp broken` | Lamp K027 | Function, attachment, beam aim and replacement applicability |
| `tire flat` | Tyre K009 | Pressure, puncture location, driving-flat history |

The retriever normalises `glassshatter`, `lampbroken`, `tireflat`, spaces, hyphens and underscores to canonical label names. Providing a label increases a candidate's retrieval score within the selected component; it is not proof that the selected record applies. Tyre bulges, fluid colour, engine warnings and high-voltage condition are **not trained CarDD outputs**. Their records require user context or a separately evaluated perception pipeline.

## Priority expansion

1. Have an automotive reviewer correct/approve the current records and their conditional actions. Mark each review with reviewer identity, date and reviewed edition.
2. Obtain exact regional manuals for Gentra, Spark and target BYD variants; record editions and applicability before adding faults. Capture engine/key-on state for dashboard cases.
3. Collect consented reference/test photos with incident/vehicle grouping and source rights. Keep evaluation photos out of the reference library.
4. Gather comparable written quotes or documented approved calls from 3-5 actual repair shops. Distinguish parts, labour, taxes, repair/replacement and quote validity. Populate prices only after verification.
5. Verify individual workshop capabilities, addresses and coordinates before mapping or nearest-provider suggestions.
6. Evaluate retrieval relevance and grounded LLM answers on held-out real questions; refine search terms after native Uzbek/Russian review.

## Rights and freshness

The KB contains short factual paraphrases with links, not redistributable manual PDFs or scraped full articles. Public availability is not an open content licence. Provider capabilities and contacts are provider-published claims checked on 11 October 2026, not independently validated endorsements. Source validity, link availability, local applicability and provider data need periodic review before use beyond the prototype. No images were downloaded or added in this pass.
