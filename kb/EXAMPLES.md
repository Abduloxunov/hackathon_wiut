# Actual offline retrieval examples

Generated from the current Markdown records and `retrieve.py` on 11 October 2026. These are deterministic evidence outputs, not LLM answers or verified diagnoses. Source links come from the retrieved records.

## Case: Crack without a component

Input:

```json
{
  "query": "crack"
}
```

### Retrieved evidence

Status: **needs_context**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

#### Context needed

- Which component is affected: body, windshield, side window, tyre, lamp, fluid, dashboard, engine, wiper, fuel or EV system?

Repair cost: unavailable; no verified quote in this knowledge base.

## Case: Windscreen crack

Input:

```json
{
  "query": "crack",
  "part": "windshield"
}
```

### Retrieved evidence

Status: **evidence_found**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

#### K007: Windscreen crack with visibility or edge involvement

Safelite identifies deep damage, obscured driver vision and edge-spanning cracks as reasons replacement may be needed. [Safelite: repair or replace damaged glass](https://www3.safelite.com/damaged-windshield-repair-replace)

Applicability: If visibility is impaired, do not treat a photo result as clearance to drive.

Possible causes (unconfirmed): Possible impact or spreading glass damage

Repair assessment: Glass replacement assessment

Next steps:

- Ask a glass technician to assess replacement and visibility.

Follow-up questions:

- Does it obstruct the driver view or reach the edges?

Limits:

- Commercial assessment guidance is not Uzbekistan law or a universal threshold.

Source locator: Replacement indicators. Mechanic review: pending.

Repair cost: unavailable; no verified quote in this knowledge base.

## Case: Tyre-sidewall outward bulge

Input:

```json
{
  "query": "outward sidewall bulge",
  "part": "tire"
}
```

### Retrieved evidence

Status: **evidence_found**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

#### K012: Outward tyre-sidewall bulge

Michelin links an outward sidewall bulge to internal structural damage and calls for immediate replacement. [Michelin: sidewall problems](https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems)

Applicability: Confirmed outward bulge: arrange assistance and replacement.

Possible causes (unconfirmed): Internal cord damage is the cited concern for a confirmed bulge

Repair assessment: Tyre replacement

Next steps:

- Do not continue normal driving on a confirmed bulging tyre.

Follow-up questions:

- Does it protrude outward? Could this be an inward indentation?

Limits:

- Image similarity cannot establish cord condition or distinguish every shape.

Source locator: Bulge versus indentation. Mechanic review: pending.

Repair cost: unavailable; no verified quote in this knowledge base.

## Case: Cobalt warning without confirmed engine state

Input:

```json
{
  "query": "oil pressure warning",
  "part": "dashboard",
  "vehicle": "Cobalt",
  "confirmed_manual": "S11"
}
```

### Retrieved evidence

Status: **needs_context**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

#### Context needed

- Is the warning still present with the engine running? A key-on lamp check alone does not establish a fault.

Repair cost: unavailable; no verified quote in this knowledge base.

## Case: Cobalt oil-pressure warning with required context

Input:

```json
{
  "query": "oil pressure warning",
  "part": "dashboard",
  "vehicle": "Cobalt",
  "confirmed_manual": "S11",
  "context": {
    "engine_running": true
  }
}
```

### Retrieved evidence

Status: **evidence_found**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

#### K021: Cobalt oil-pressure warning while engine is running

The Cobalt manual distinguishes the normal pre-start lamp check from a warning persisting while running; it directs safe stopping and engine shutdown. [Chevrolet Uzbekistan: Cobalt manual](https://chevrolet.uz/storage/images/exp_files_uz/17/gtUbSsqgxGKTYDVaC2TOyK8ZHnfeJvk4hiiR23wU.pdf)

Applicability: Only when the lamp persists with the engine running.

Possible causes (unconfirmed): An oil-pressure system problem is possible; exact cause is not established

Repair assessment: Engine oil-pressure assessment

Next steps:

- Stop safely, switch off the engine and arrange service.

Follow-up questions:

- Engine running or key-on only? Exact manual confirmed?

Limits:

- Not evidence of a failed pump, low oil quantity or a common Cobalt fault.

Source locator: PDF page 63 (printed 4-13). Mechanic review: pending.

Repair cost: unavailable; no verified quote in this knowledge base.

## Case: Unknown topic

Input:

```json
{
  "query": "quantum banana spaceship",
  "part": "body"
}
```

### Retrieved evidence

Status: **no_evidence**

Offline lexical candidate retrieval; scores are not probabilities.

This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.

Repair cost: unavailable; no verified quote in this knowledge base.
