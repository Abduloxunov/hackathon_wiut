---
name: Service-Bay Tracker
added_by: Muhammadjon + claude-2 (from Muhammadjon's AI-generated "master plan", cleaned; numbers removed)
date: Sat 10 Oct 15:10
direction: dealer/service ops
mode: partner product: Toyota Royal Motors / BYD Royal Motors, Aftersales (service director); changes how bay utilisation and repair stages are tracked
---

# Service-Bay Tracker: where is each car in the workshop, and which bay is idle?

**One line:** Workshop CCTV in → per-bay state timeline (empty / car in bay / car on lift / bay active vs idle) → utilisation dashboard + "bay idle > N min with a car inside" alerts for the service director.

## Problem and user
- **User:** service director / foreman. **Payer:** the dealer (aftersales).
- **Pain (hypothesis, to confirm with Royal Motors service):** bays idle while a car waits for parts or a mechanic; no objective utilisation numbers; customers ask "when is my car ready?".
- Evidence: not yet. **Interview a service advisor** before claiming any utilisation gain. The source plan's "+12% throughput" is invented; do not use it.

## What the product does
- **Input:** video from a fixed workshop camera (or a recorded clip); operator draws bay polygons once.
- **Output:** per-bay state timeline, idle-time totals, alerts, optional customer ETA hint.
- **Live jury test:** weak. The jury cannot bring a workshop. They can upload a clip, or we point a laptop camera at a toy-car "bay" on the table. **This is the main weakness for the "jury input" requirement.**

## Tech
- Vehicle + person detection, tracking (ByteTrack), polygon zones, state machine with time hysteresis; "on lift" via vertical box offset vs the bay floor line. Supervision-style zone logic.
- **Data:** no public workshop footage with a clear licence found yet; we would need to film at a dealer (permission + no faces, so blur them).
- **Inference:** edge box per site or server; CPU is enough at 1–2 fps.

## Why hard to copy
- The state logic + integration with the dealer DMS (work orders). Without DMS integration it is easy to rebuild.

## Business
- Per bay per month SaaS (price to validate).

## Can we build it in ~8 h?
- The pipeline yes; **real data and the jury demo, no**. Ranks low on the "jury input" filter.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
