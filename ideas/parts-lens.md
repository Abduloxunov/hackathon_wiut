---
name: PartsLens
added_by: Muhammadjon + claude-2 (from Muhammadjon's AI-generated "master plan", cleaned; numbers removed)
date: Sat 10 Oct 15:10
direction: dealer/service ops (parts identification)
mode: partner product: Toyota Royal Motors / BYD Royal Motors, Spare Parts & Warehouse; changes part look-up at the counter and the warehouse
---

# PartsLens: photo of a loose part → OEM part number, fitment and bin location

**One line:** Photo of an unpackaged part (filter, brake pad, sensor, bulb) in → top-3 matching OEM part numbers with similarity, fitment and bin location → warehouse picker or service advisor confirms.

## Problem and user
- **User:** parts-counter clerk, warehouse picker, service advisor. **Payer:** dealer parts department.
- **Pain (hypothesis):** old parts brought in by customers or mechanics without packaging or number; slow manual catalogue search. Needs a dealer interview. The source plan's "3× faster picking" is invented; do not use it.

## What the product does
- **Input:** 1–3 phone photos of the part (on a plain background, with a guide frame).
- **Output:** top-3 candidates (part number, name, image, similarity), "confirm" button; unknown → "not in catalogue".
- **Live jury test:** good, if we have physical parts on the table (a few filters, spark plugs, bulbs, fuses). The jury picks one and photographs it.

## Tech
- Segmentation / background removal → embeddings (DINOv2 or CLIP, check the licences: DINOv2 is Apache-2.0) → FAISS nearest neighbour against a catalogue gallery → re-ranking with size from a reference marker (an A4 sheet / ArUco) → open-set rejection threshold.
- **Data:** we build the gallery ourselves (photograph 20–40 real parts from 3–5 angles each). This is our dataset. Public catalogue images are copyrighted, so we don't scrape them.
- **Inference:** server CPU, embedding plus search in milliseconds to tens of ms (to be measured).

## Why hard to copy
- The catalogue gallery linked to OEM numbers and bins, which only a dealer can provide; size-aware re-ranking; open-set rejection measured on held-out parts.

## Business
- Per parts counter per month (price to validate).

## Can we build it in ~8 h?
- Yes, technically (retrieval is robust); the demo needs physical parts. **Risk:** visually identical parts with different numbers (e.g. brake pads for two models), so we always show the top 3 and the size; a human confirms.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
