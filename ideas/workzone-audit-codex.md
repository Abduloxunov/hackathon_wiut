---
name: Work-Zone Evidence Audit
added_by: Bexruz + codex
date: Sat 10 Oct
direction: driver / road safety
mode: startup
---

# Work-Zone Evidence Audit

**One line:** Roadworks approach photos/video + expected visible equipment checklist → evidence-backed setup review and correction ticket.

## Problem and user
- User: contractor site supervisor; payer: roadworks contractor. Repeated manual setup checks and incomplete evidence are local hypotheses, not measured findings.
- [Blyncsy](https://blyncsy.com/solutions/construction-zones/) already documents equipment/sign detection and actual-versus-plan work-zone review. The problem is plausible but this idea is not globally new.

## What the product does
- Input: structured checklist of expected signs/cones/barriers and approach imagery.
- Output: observed, absent with adequate view, not observed due to missing view, or uncertain; evidence frames and correction ticket for supervisor review.
- Live jury test: change a controlled physical setup or submit unseen supported imagery. Miniature props/synthetic scenes are labelled; they do not establish real roadworks performance.
- Boundary: no legal compliance certificate. Local rules need expert verification; calibrated geometry is needed for metric spacing.

## Tech (why it is a system, not one API call)
- Supported-item detection → tracking/frame deduplication → capture-coverage gate → checklist reconciliation → evidence report. Start from a structured checklist rather than interpreting arbitrary engineering drawings.
- Data today: authorised supervisor imagery or controlled physical arrangements if accessible. No footage permissions or local expert checklist secured yet. Record sources/licences and staged examples separately; verify model licences.
- Proposed inference: server; CPU/GPU, speed and cost unmeasured.
- Night/rain/local signs: test actual local supported assets and conditions; no extrapolation from toy scenes or foreign sign classes. Avoid nonconsented faces/plates; do not enter live work zones for demo collection.
- Test: item precision/recall, false missing-item alarms, correct not-observed handling and supervisor review time; hold out setups/sites and sessions.

## Why hard to copy
- Potential future advantage: local approved checklists, representative site data and correction-history integration. No current moat. Blyncsy is direct prior art, including plan comparison.

## Business
- Proposed billing: contractor subscription/per active site; price unverified.
- Cost includes collection/annotation, inference/storage and reviewer labour. ROI needs measured supervisor time and revisits, not invented safety savings.
- Three-month pilot: approved scope/checklist and permissions → shadow inspections → supervised correction workflow. Buyer commitment unconfirmed.

## Can we build it in ~8 h?
- Conditional MVP: one setup type, a few equipment classes, checklist evidence and uncertainty handling.
- Biggest risk: a toy-only demo, absent real labels, or unsupported detector classes. Do not choose without credible real-scene access.

## Comments
<!-- other agents may append comments -->
