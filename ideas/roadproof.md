---
name: RoadProof
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 14:45
direction: driver/road safety (road condition)
mode: startup (B2B/B2G: city road services, hokimiyat, road contractors, fleet operators)
---

# RoadProof: from road photos to repair tickets and repair verification

**One line:** Road photo (phone or dashcam frame) in → quality check → road-damage detection → priority → inspection ticket; plus **before/after repair verification** so the city can check that a contractor really fixed the pothole.

## Problem and user
- **User:** road-maintenance inspector, district hokimiyat, road contractor; residents report through the existing channel. **Payer:** the city or road organisation.
- **Evidence** (sources in `_research-notes-claude2.md`):
  - Tashkent's spring repair campaign covers about 816,000 m² of road.
  - In March 2025 the hokimiyat asked residents to send photos of poor repairs via *Xalq Nazorati*, so photo reports already flow into a manual process.
  - Critics report practically no quality control at road acceptance.
- **The twist that makes it ours:** the bare pothole detector is a cliché (see `docs/strategy.md` §2 / strategy doc "weak ideas"). **Repair verification** (same spot before vs after: is the damage gone, is the patch rough or uneven?) targets the real complaint, contractor accountability.

## What the product does
- **Input:** a road photo (jury can take one in the parking lot or show any image), or a pair of photos (before / after) of the same spot.
- **Output:** detections + priority + ticket (JSON / PDF), or for a pair: "damage resolved / partly resolved / not resolved" with an aligned side-by-side view.
- **Live jury test:** any road photo from the jury's phone; a before/after pair we prepare **plus** one the jury takes.

## Tech
- **Pipeline:**
  1. quality gate (blur, exposure, "is this a road" via CLIP zero-shot);
  2. road-damage detector (RDD2022 classes: longitudinal, transverse and alligator cracks, potholes);
  3. for pairs: feature matching (ORB/SIFT + RANSAC homography) to align the views, then compare detections and the damaged-area share in the aligned region;
  4. decision engine → priority / verification verdict;
  5. ticket with GPS from EXIF if present.
- **Data:** RDD2022 (licence conflict: CC BY-SA 4.0 vs CC BY 4.0, **read figshare**); ready weights exist ([HF nsr51324](https://huggingface.co/nsr51324/Road_Damage_Object_Detection), no licence on the card, so treat as AGPL via Ultralytics); **local test set** from our own Tashkent photos + Mapillary (CC BY-SA).
- **Inference:** server CPU (YOLO11n at 640 px; speed to be measured).
- **Night / rain:** RDD2022 is mostly daytime and dry; wet asphalt and puddles cause false positives. The quality gate flags night images; we report metrics only for the groups we actually have.

## Why hard to copy
- A local Tashkent test set; repair verification with image alignment (a system, not a detector); the ticket format fits the existing Xalq Nazorati flow.

## Business
- **Payer:** city / road service. Pilot price hypothesis $500–2,000 / month (see `docs/strategy.md` §6, assumptions only).
- **Value:** inspector hours saved; fewer disputed repairs.

## Can we build it in ~8 h?
- **MVP:** single-photo detection + priority + ticket; before/after verification on aligned pairs.
- **Biggest risk:** detector transfer to local roads; alignment failure when the before and after viewpoints differ a lot (then we ask for a retake from the guide marker).

## Comments
<!-- other agents: `- <agent ID>: comment` -->
