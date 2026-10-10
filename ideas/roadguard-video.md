---
name: RoadGuard AI (dashcam video → road events)
added_by: Muhammadjon + claude-2 (from Muhammadjon's "RoadGuard AI Hackathon Playbook" + poster; cleaned)
date: Sat 10 Oct 15:30
direction: driver/road safety (road condition, fleets)
mode: startup (fleets: taxi parks, logistics, trucking; later city road services)
---

# RoadGuard AI: dashcam video → unique road-damage events with evidence frames

**One line:** Dashcam MP4 in → road-damage detection per frame → **repeated detections of the same pothole merged into one event** → event table (time, class, confidence, evidence frame, priority) + annotated video + CSV/JSON report for the fleet operator.
Sibling of [RoadProof](roadproof.md) (photo + repair verification): same detector, different input and buyer.

## Problem and user
- **User / payer:** fleet operator who controls routes and repair costs (taxi, logistics, trucks); later the city or road contractors.
- Dashcam footage exists but stays raw: nobody watches hours of it. The product turns it into a short list of actionable events.
- **Careful promise:** no "prevents accidents", no pothole depth, no coordinates without real GPS.

## Competitors (verify the pages before the deck)
- Fleet AI dashcams: [Motive](https://gomotive.com/products/dashcam/), [Samsara](https://www.samsara.com/products/cameras), focused on driver behaviour, not road condition.
- Road damage: [RoadBounce PotholeGuard](https://roadbounce.com/pothole-guard/), open-source [iWatchRoad](https://github.com/smlab-niser/iWatchRoad) (reference only, attribute if used).
- Our angle: affordable, local, measured event logic; not "we invented YOLO".

## What the product does (pipeline)
`MP4 → OpenCV frame reader (every N-th frame, N stated) → road-damage detector → event association / dedup (class + IoU/position + time gap) → priority score (confidence × relative box size × number of confirming frames) → annotated MP4 + events JSON/CSV + dashboard`

**Event format (proposal):**
```json
{"event_id": "e_0007", "class_name": "pothole", "first_seen_ts": 12.34, "last_seen_ts": 13.10,
 "n_frames": 9, "max_conf": 0.81, "bbox_xyxy": [412, 530, 690, 701], "evidence_frame": "frames/e_0007.jpg",
 "priority_score": 0.74, "source_video": "upload_abc.mp4", "gps": null}
```
`gps` is filled only from a real synchronised GPS track (e.g. GPX upload).

## MVP must-haves
1. MP4 upload with size/duration/format checks.
2. Real detection of the supported damage classes on the uploaded video.
3. Output video with boxes + confidence.
4. Event table: time, class, confidence, evidence frame.
5. Dedup of repeated detections across neighbouring frames.
6. Measured FPS and total processing time (hardware stated).
7. Public HTTPS site processing **new** input.
8. README: run, architecture, data, licences, known failures.

Optional, only after the full flow works: GPS map (only with real GPS), PDF/CSV export, more classes, live camera.

## Quality: what to measure
- Detector: precision / recall / F1 / mAP on a held-out set split **by video/source**, not by neighbouring frames.
- **Event logic (our own contribution):** how often one pothole is split into several events (duplicates) and how often different potholes are merged. Measure it on a few hand-labelled clips. This is the metric nobody else will have.
- Night / rain / Uzbek roads: claim nothing that wasn't tested; list failure examples.

## Tech
- YOLO nano/small with **road-damage weights** (a COCO model does NOT detect potholes): RDD2022 ([repo](https://github.com/sekilab/RoadDamageDetector); licence conflict, see `_research-notes-claude2.md`) or ready weights ([HF nsr51324](https://huggingface.co/nsr51324/Road_Damage_Object_Detection), no licence on the card).
- OpenCV, optional ByteTrack. Tracking cars ≠ merging road damage; our own association logic does that.
- Streamlit/Gradio for the MVP, or FastAPI + simple UI. One process, SQLite/files, no microservices.
- Suggested layout: `app.py`, `src/video_reader.py`, `src/detector.py`, `src/events.py`, `src/report.py`, `models/README.md`, `tests/`, `LICENSES.md`.

## Live jury test
- Weaker than photo ideas: the jury must give us a **video**. They can film 10–20 s from a car or phone on the street, or upload any road video from YouTube or their phone. Processing time on CPU must be short (cap the upload at ~30 s, every N-th frame).

## Why hard to copy
- Event dedup + priority logic with measured duplicate/merge rates; a local Tashkent clip test set; fleet-report format. The detector itself is not a moat.

## Business
- Per vehicle per month or per hour of processed video; pilot = process an agreed volume of one fleet's footage, hand-check a sample, measure precision, unique events, speed, cost per video hour. All prices are hypotheses.

## Can we build it in ~8 h?
- Yes if road-damage weights work in hour 1–3 (otherwise fine-tune a small model on an RDD2022 subset).
- **Risks:** CPU video processing time on free hosting; licence of weights and data; the jury-input demo.

## Implementation notes (from Muhammadjon's "RoadGuard AI Full Guide", cleaned)
- **Order of work:** prove the weights detect road damage on our own clip **before** building any UI → video + detections → events → report → public site. With only ~12 h, drop fine-tuning, the map and auth.
- **Video edge cases:** timestamp = frame_idx / FPS. Handle unknown or zero FPS (fall back to the container duration / frame count); cap file size and duration; delete uploads after processing.
- **Event association:** primary = tracker IDs (ByteTrack via Ultralytics `model.track`); fallback = IoU + time-window matching; a gap tolerance of a few frames so one pothole isn't split when a detection drops for 1–2 frames. Keep first/last ts, max conf, best frame.
- **Threshold:** choose the confidence threshold on a validation split, not a hard-coded 0.5.
- **Metrics:** never mix frame-level and event-level numbers. Report both: frame-level P/R/F1 (state the IoU criterion, e.g. IoU ≥ 0.5) and mAP variant (mAP@0.5 or @0.5:0.95); event-level = duplicates left + wrong merges on hand-counted clips. Small test → say "preliminary test on N images".
- **UI disclaimer (put it on the page):** *"Automatic analysis results require human review and are not an engineering assessment of road safety."*
- **UI minimum:** title + description, MP4 upload with limits, Start analysis + progress, original + annotated video, event table (event, time, class, conf, evidence frame), filter by class/priority, CSV/JSON download, limitations + model version + licences section.

| Risk | Mitigation |
|---|---|
| Model finds no potholes | test weights on our clip first; no UI before that |
| Many false positives | tune threshold on validation; show failure examples |
| Many duplicates | tracking + measured dedup |
| Video too slow | lower resolution / every N-th frame; state the trade-off |
| Deploy fails | file-size limit, test the public URL, backup recording |
| Licence unsuitable | check model, code, weights and data licences separately |
| Business value unproven | interviews / tiny pilot; label value as hypothesis |
| Deck over-promises | separate implemented features from plans |

**Pitch line (use only for implemented parts; otherwise "we plan to"):** *"RoadGuard AI turns dashcam footage into reviewable road-damage events. A computer-vision model detects supported damage classes, our video pipeline links repeated detections across frames, and the web app produces timestamped evidence and an exportable report, measured on a documented test set, with human review where it is still required."*

## ⚠️ Do not reuse from the poster
"Processing time 42.3 s", "FPS 12.5", the confidence values in the mock table, "Precision/Recall … day good / rain satisfactory / night average": all **illustrative, not measured**. RDD2022 has **47,420** images (paper), not "more than 10,000", and its licence is not simply "open".

## Comments
<!-- other agents: `- <agent ID>: comment` -->
