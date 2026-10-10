---
name: Research landscape + 7 ideas (claude-1)
added_by: Davlatyor + claude-1
date: Sat 10 Oct 15:25
direction: all
---

# What exists (web research, 10 Oct) → where the gaps are → our ideas

All vendor numbers below are **their claims, not verified**. Do not put them in the deck as facts.

## 1. Landscape — what others built and HOW

| Area | Who / what | Method (what a developer needs) | Source |
|---|---|---|---|
| Damage detection | Roboflow tutorial | 2 instance-seg models: **car parts** + **damage**, intersect masks → "scratch on front-left door" | [Roboflow](https://blog.roboflow.com/assess-car-damage-with-computer-vision/) |
| Damage → cost | IEEE Access 2023 | Semantic seg of damaged panels + structured vehicle data → cost regression, trained on historical claims | [DOAJ](https://doaj.org/article/87b59058090841b2a0819b32022830e9) |
| Video damage | AAAI 2020 (Ant Financial) | Video detection + segmentation over many frames instead of single photos | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7110) |
| Live-guided video claim | Tractable AI Inspection | Phone **web app**, guided video, asks the user for extra shots live, fraud checks | [Coverager](https://coverager.com/new-ai-solution-accurately-assesses-vehicle-condition-in-minutes/) |
| Before/after handover | Damage iD, VerifyAI | Side-by-side video, new inspection compared against previous record → "new damage" | [Auto Rental News](https://www.autorentalnews.com/news/damage-id-introduces-side-by-side-video-comparison), [VerifyAI](https://verify.switchlabs.dev/use-cases/vehicle-damage-inspection) |
| Walkaround alignment | Patent US 12373935 | Track **anchor parts** (wheels, handles, lights) across frames to align two walkarounds and register damage positions | [Justia](https://patents.justia.com/patent/12373935) |
| 3D damage | CrashSplat (2025) | Gaussian Splatting from SfM poses; **lift 2D damage masks into 3D** via projection + Z-buffer, no training. Code public | [arXiv 2509.23947](https://arxiv.org/abs/2509.23947v1), github.com/DragosChileban/CrashSplat |
| 3D vehicle recon | BRUM; drive-through rig | DUSt3R instead of COLMAP for sparse views; 3DGUT for lens distortion; DISK + LightGlue matching | [arXiv 2507.12095](https://arxiv.org/html/2507.12095v1), [arXiv 2603.26638](https://arxiv.org/pdf/2603.26638) |
| Zero-shot damage | Grounded SAM 2 / SAM 3 | Text prompt → Grounding DINO boxes → SAM 2 masks (+ video tracking). Subtle damage needs validation | [Grounded SAM 2](https://docsearch.algolia.com/mcp/docs/repo/idea-research/grounded-sam-2), [Roboflow](https://blog.roboflow.com/open-vocabulary-segmentation/) |
| **AI-faked claim photos** | Admiral, PZU PhotoDetective, SAS (May 2026) | Problem is new and growing: AI-edited plates/damage. Counter-measures: multi-angle shots, reference object, native files, **live video**, AI-image detectors | [SAS 2026](https://www.sas.com/en_us/news/press-releases/2026/may/synthetic-images-ai-insurance-fraud.html), [Debevoise Jan 2026](https://www.debevoise.com/insights/publications/2026/01/use-of-ai-generated-images-for-fake-insurance), [PZU](https://www.qorusglobal.com/innovations/30701-photodetective-detecting-ai-generated-and-internet-sourced-fraud), [Digital Trends](https://digitaltrends.com/computing/ai-images-are-now-being-abused-to-fake-evidence-for-vehicle-insurance-fraud) |
| Repaint / hidden accident | iSOS Paintreader, Oto Dedektif, Heydealer (thermal robot) | Panel-to-panel **colour/surface mismatch**; Heydealer: thermal camera on robot arm | [Gust iSOS](https://gust.com/companies/isos-llc), [Herald](https://mbiz.heraldcorp.com/article/10869543), [VahanBazaar](https://vahanbazaar.in/buyer-tools/ai-vahan-inspection) |
| Fault from dashcam | Sompo Japan + Genext, Nexar | Dashcam + GPS → reconstruct scene → compare with past accidents → **fault %**; Nexar: map all cars + AI timeline | [Insurance Business](https://insurancebusinessmag.com/asia/news/breaking-news/ai-to-assist-in-determining-whos-at-fault-in-car-accidents-157846.aspx), [Nexar](https://data.getnexar.com/blog/nexar-releases-first-ever-ai-vision-technology-to-reconstruct-car-accident-scenes) |
| Potholes | Lvl5/Payver, iWatchRoad, Pothole Patrol | YOLO on dashcam + GPS (OCR timestamp ↔ GPS log) → OpenStreetMap; pay drivers, sell to city; YOLOv8 **in browser** | [ForConstructionPros](https://www.forconstructionpros.com/construction-technology/article/21029732/pothole-repairs-lvl-up), [arXiv 2508.10945](https://arxiv.org/abs/2508.10945), [ETHGlobal](https://ethglobal.com/showcase/pothole-patrol-9v0u8) |
| Tyre tread | Anyline, Goodyear PoC | Phone → 3D tread model / CNN regression of depth; classes Good / Worn / Change now | [Anyline](https://anyline.com/news/anyline-tire-tread-scanner-smartphones), [Taazaa](https://www.taazaa.com/success-story/mobile-app-for-tire-tread-analysis) |
| EV bay ICE-ing | PoGo + Intelli-Park, Zevtron + SpotGenius | ANPR + fuel-type lookup; "blocked" = parked but not charging; Raspberry Pi cam every 10 s | [EVPowered](https://evpowered.co.uk/news/you-shall-not-park-pogo-charge-partners-with-intelli-park-to-prevent-iceing/), [Power Systems Design](https://www.powersystemsdesign.com/articles/zevtron-partners-with-spotgenius-to-monitor-ev-charging-spaces-with-vision-ai-technology/8/23036) |
| Helmet | WACV 2020, Roboflow datasets | YOLO helmet/no-helmet per rider; single GPU server + clients | [WACV](https://openaccess.thecvf.com/content_WACV_2020/html/Chairat_Low_Cost_High_Performance_Automatic_Motorcycle_Helmet_Violation_Detection_WACV_2020_paper.html) |
| Gap & flush | Cognex, Zebra, Ulsan | Gap = 2D; flush needs 3D (laser lines / stereo / specular reflection) | [Zebra](https://www.zebra.com/ap/en/resource-library/use-case-library/verifying-correct-gap-and-flush.html), [Cognex](https://www.cognex.com/industries/automotive/chassis-systems) |
| Warning lights | CarVet, CarEazy, UB research | YOLOv5, 18 classes. Mostly LLM-wrapper apps → **low tech score, avoid** | [hunted.space](https://hunted.space/product/carvet) |

**Open datasets (check licence before use):** CarDD 4,000 imgs / 6 damage classes ([arXiv](https://arxiv.org/pdf/2211.00945), cardd-ustc.github.io — official licence unconfirmed; Roboflow mirror says CC BY 4.0); VehiDE 13,945 imgs / 8 classes (licence unknown); **Humans in the Loop car parts + damages, 1,812 imgs, CC0** ([link](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/)); Pixemantic Vehicle Damage-29 ([IEEE DataPort](https://ieee-dataport.org/documents/pixemantic-vehicle-damage-29)).

## 2. Gaps nobody covers well
1. **Trust of the photo itself** — damage AIs assume the photo is real; in 2026 generative edits are the new fraud (SAS, Admiral). Detectors exist, but are not combined with capture + damage in one flow.
2. **Phone walkaround + 3D + damage** — CrashSplat-style 3D is research only; no phone product found (search, 10 Oct).
3. **Local context** — no product tuned to Uzbek roads, local fleet (Cobalt, Nexia, Damas, BYD boom) or local insurers.
4. **Privacy-by-design** — EV/parking products rely on reading plates; the task forbids non-consented plates.

## 3. Ideas (ranked by my estimate: score × buildable in ~8 h)

### A. "ClaimProof" — trusted damage evidence from a phone (insurer / dealer) ★ top pick
- **What:** web app on the jury's phone: **live-guided capture** with random challenge (e.g. "now show the left headlight", random angle order, timestamp watermark) → **authenticity checks** (screen-recapture detection via FFT moiré, EXIF/C2PA presence, noise-residual/ELA, AI-image classifier) → **damage + part segmentation** → report "front bumper: scratch, authentic: yes, confidence".
- **Why new:** combines anti-fraud capture + forgery forensics + damage AI in one pipeline; directly answers the 2026 fraud wave.
- **Live jury test:** jury walks to any car (or photo on a laptop screen → we flag "recaptured screen"!). Very demoable.
- **Methods:** YOLOv8/11-seg on CarDD + HITL parts (CC0); parts∩damage mask logic; FFT/moiré + JPEG-grid features; open AI-image detector (check licence); browser capture via getUserMedia.
- **Business:** insurer pays per claim; partner product inside Toyota/BYD Royal Motors body shop / trade-in desk.
- **Risk:** AI-image detection accuracy — measure on our own test set (real vs edited in Gemini/SD), report honestly.

### B. "Handover Diff" — who made this scratch? (service centre / rental / dealer)
- **What:** walkaround video at intake and at pickup → align panels with part segmentation + anchors (wheels, lights) → **change detection** → only *new* damage shown, with timestamps.
- **Methods:** part seg; per-panel homography (LightGlue/SuperPoint or ORB); SAM 2 tracking; diff on aligned crops; optional CrashSplat 3D lift as stretch.
- **Partner:** Toyota/BYD service reception — dispute reduction. Can be combined with A.

### C. "Junction Risk Map" — continue our elimination pipeline (city / insurer)
- **What:** from any traffic video: tracks → BEV homography → **near-miss surrogate metrics** (TTC, PET) → risk heatmap per junction + clips.
- **Why hard to copy:** our elimination-stage code and zones (declared in README) — the task explicitly allows it and lists it as a direction.
- **Live jury test:** jury uploads any intersection video. Needs GPU for speed.

### D. "EV Bay Guard" without reading plates (charging operator / mall)
- **What:** CCTV → bay occupancy → **EV vs ICE by make/model/shape classification (no plate reading)** + "parked but not charging" timer → alert.
- **Why new:** privacy-preserving version of ANPR products; fits the no-plates rule.
- **Risk:** EV vs ICE look-alikes (hybrids); data for local BYD models.

### E. "TyreAge" — tyre safety from one photo (service upsell / fleet)
- **What:** sidewall photo → **OCR of DOT date code** (week/year → tyre age) + tread wear class + crack detection → "replace now / soon / OK".
- **Methods:** text detection (PaddleOCR/docTR) on curved sidewall (polar unwrap), CNN wear classifier, coin/reference scale.
- **Demo:** jury photographs any tyre in the parking lot. Simple, practical; innovation moderate.

### F. "Repaint Radar" — hidden accident history for trade-in (dealer / buyer)
- **What:** 4–8 walkaround photos → per-panel colour in Lab under white-balance from a reference → **panel-to-panel ΔE mismatch** + reflection-distortion ("orange peel") texture score → flag repainted panels.
- **Creative extra:** **phone deflectometry** — show a stripe pattern on a laptop/phone screen, film its reflection on the panel; bent stripes = dent/filler. (No product found doing this with phones — search, 10 Oct.)
- **Risk:** lighting; needs our own ground truth (a few cars with known repaint).

### G. "Rider Line" — Ducati rider coaching from a phone/helmet video
- **What:** horizon-tilt estimation → lean angle per corner; lane position; overlay on map. Ducati Link gets lean from bike CAN, not camera ([MoreBikes](https://www.morebikes.co.uk/?p=23007)).
- **Risk:** we need riding video with consent; demo by jury is hard. Lower priority.

## 4. My recommendation
**A (ClaimProof), with B's before/after diff as the second module.** Strongest on innovation (2026 problem), technical depth (capture + forensics + seg pipeline), and the live jury test works on their phones. C is our safest "hard to copy" fallback.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
