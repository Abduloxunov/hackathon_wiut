# Computer vision toolbox — the building blocks

Use this when proposing ideas: a good idea combines **3–4 tasks** in one pipeline and ends in a decision. One model behind a UI scores low (task statement: "a single prompt to a general-purpose model … scores low on both technology criteria").

## 15 basic tasks
| # | Task | Question it answers | Typical pretrained models | Car / dealer example |
|---|---|---|---|---|
| 1 | Classification | What is this image? (one label) | ResNet, EfficientNet, ViT | Tyre: OK / worn / replace |
| 2 | Detection | What objects, where? (boxes) | YOLO, RT-DETR | Cars, people, phones in a frame |
| 3 | Segmentation | Exactly which pixels? (masks) | YOLO-seg, Mask R-CNN, SAM 2 | Exact scratch outline → area in cm² |
| 4 | Keypoints / pose | Where are specific points? | MediaPipe, YOLO-pose, RTMPose | Car corners, wheel centres, driver's eyes/head |
| 5 | Tracking | Same object over time? | ByteTrack, BoT-SORT, SAM 2 | Car enters bay 10:02, leaves 11:15 |
| 6 | OCR | What does it say? | PaddleOCR, docTR, TrOCR | VIN, odometer, tyre DOT code, part numbers |
| 7 | Depth estimation | How far is each pixel? (one photo) | Depth Anything, ZoeDepth | Dent depth, distance to car ahead |
| 8 | Embeddings / retrieval | What does it look like? Seen it before? | DINOv2, CLIP | Reused claim photo; matching catalogue part |
| 9 | Anomaly detection | Anything unusual? (no defect labels) | PatchCore, PaDiM (anomalib) | Odd spot on a new car at PDI |
| 10 | Change detection | What differs between two images? | Alignment + diff, Siamese nets | New scratch between check-in and check-out |
| 11 | Action recognition | What is the person doing? | VideoMAE, SlowFast, rules on pose | Did the mechanic tighten all nuts? |
| 12 | 3D reconstruction | What is the 3D shape? | COLMAP, DUSt3R, Gaussian Splatting | 3D car model from a phone video |
| 13 | Image forensics | Is this photo real? | ELA, noise residuals, AI-image detectors | Screen recapture, edits, AI-generated |
| 14 | Open-vocabulary / VLM | Find anything described in words | Grounding DINO, SAM 3, Florence-2, GPT/Gemini vision | "find the oil leak", no training |
| 15 | Generation / synthetic data | Create images | Stable Diffusion, inpainting | Synthetic damaged cars for training/testing |

## Every product = 4 layers
1. **Perceive** — detect, segment, OCR, keypoints, embeddings.
2. **Measure** — geometry turns pixels into real units (cm, m, s, km/h, area, angle).
3. **Reason** — over time and history: compare, count, accumulate, thresholds, "seen before?".
4. **Decide / act** — accept/reject, alert, price, work order.

Value (and the jury's Technical + Innovation score) lives in layers 2–4. Rarer, stronger tools: embeddings (8), change detection (10), forensics (13), depth (7), anomaly (9).

Real products that combine these (17 products with demo videos, task chips and the 4-layer pipeline): **CV Product Field Guide** https://claude.ai/artifact/FTG1Hy1L9pFLsSVV812q14 (private to Davlatyor until shared). Products: SafelyYou, Peloton Guide/IQ, Sportsbox AI, Drishti, Amazon Just Walk Out, FIFA semi-automated offside, John Deere See & Spray, Buildots, Hayden AI, AMP Robotics, UVeye, Tractable, Nanit, Trax, Verkada AI search, Mobileye, Be My AI. None of them uses image forensics (13) or generation (15) → open gap.
