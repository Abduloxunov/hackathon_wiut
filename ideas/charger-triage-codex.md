---
name: Charger Fault Triage
added_by: Bexruz + codex
date: Sat 10 Oct
direction: EV / infrastructure
mode: startup
---

# Charger Fault Triage

**One line:** Supported charger display/model photos → extracted visible code, manufacturer-reference evidence and a structured operator support ticket or retake request.

## Problem and user
- User: charging-site staff/support desk; payer: charging operator. The hypothesis is incomplete photo-based fault reports where usable telemetry is unavailable; local prevalence is unverified.
- [ChargeLab Spark](https://chargelab.co/blog/spark-ai-launch) documents AI network monitoring and diagnostics from OCPP logs/events. This is adjacent prior art; our proposed photo-first intake must justify why those logs are unavailable or insufficient.

## What the product does
- Input: model label plus display photo from one supported charger family.
- Output: visible status/error text, exact reference mapping, evidence and ticket for a trained support operator. Unknown equipment/code returns unresolved; blurry input requests recapture.
- Live jury test: fresh photos of supported equipment, or declared display samples to test OCR; unknown codes/glare should trigger abstention. Sample screens do not demonstrate real fault diagnosis.
- Boundary: no electrical root-cause or hardware-repair claim from a photograph.

## Tech (why it is a system, not one API call)
- Model identification → screen/label rectification → OCR → confidence/code validation → versioned manufacturer-reference lookup → ticket generation. Optional LLM formatting uses retrieved evidence only.
- Data today: self-collected authorised label/display images and a permitted reference for the exact family. Access and reference rights not yet confirmed. Annotate codes, model and blur/glare, separate real/sample screens, verify model licences.
- Proposed inference: server CPU initially; speed and cost unmeasured.
- Night/rain/local equipment: real reflective/wet/dim screens need separate tests; unsupported models stay unresolved. No faces/plates required.
- Test: exact code extraction, reference-match accuracy, wrong/unknown-code abstention, retake rate and operator review time; held-out capture sessions.

## Why hard to copy
- Potential future advantage: local screen examples, hardware-version mappings and support integration. Not a current moat. OCR plus a generic chatbot alone is weak under the technology rubric.

## Business
- Proposed billing: per site/month or completed intake; price unverified.
- Cost per report includes OCR/compute, reference maintenance, storage and human review. Savings require measured support intake time/revisits, not assumed uptime improvements.
- Three-month pilot: one family/operator and approved references → shadow triage → supervised ticket use. No operator partnership established.

## Can we build it in ~8 h?
- Conditional MVP: one family, a small documented code set, fresh capture, quality rejection and source-backed ticket.
- Biggest risk: inaccessible chargers or undocumented screens; without real examples this may remain a weak sample-screen OCR demonstration.

## Comments
<!-- other agents may append comments -->
