# MDB Vision — Research Dossier (WIUT Hackathon 2026 Finals, Computer Vision track)

**What this is:** the evidence of the research our team did before building. In the 12 hours after the task announcement (Sat 10 Oct 12:30 → Sun 11 Oct 01:45) the three of us and our AI agents (Claude Code ×2, OpenAI Codex) researched the problem space, collected **44 product ideas** across all four task directions, mapped each idea to computer-vision methods, checked prior art, models, datasets and licences, gathered local (Uzbekistan) evidence, sorted the ideas, and validated the three finalists.

Team: Davlatyor Abduloxunov (lead, developer) · Muhammadjon Xalimov · Bexruz Xasanov.
Detailed working notes live in [`ideas/`](../ideas) and [`docs/`](.); this file is the summary. **All numbers are from the linked sources; vendor numbers are marked as claims.**

---

## Contents
1. [Process](#1-process)
2. [The CV toolbox we evaluated ideas with](#2-the-cv-toolbox)
3. [All 44 ideas — methods and verdict](#3-all-44-ideas)
4. [The three finalists — validity checks](#4-the-three-finalists)
5. [Final decision](#5-final-decision)
6. [Methods, models and licences](#6-methods-models-and-licences)
7. [Datasets and licences](#7-datasets-and-licences)
8. [Uzbekistan facts](#8-uzbekistan-facts)
9. [Prior art and competitors](#9-prior-art-and-competitors)
10. [Principles we adopted](#10-principles-we-adopted)
11. [Index of detailed files](#11-index-of-detailed-files)

---

## 1. Process
| Step | What we did | Output |
|---|---|---|
| 1 | Read the task; listed the judging weights (Tech 25, Innovation 25, Impact 25, Presentation 15, Business 10) and hard rules (no fake metrics, no unconsented faces/plates, public deploy from repo) | [`docs/task.md`](task.md), [`docs/submission.md`](submission.md) |
| 2 | Landscape research: what real products and research exist, and **how** they work | [`ideas/research-landscape-claude1.md`](../ideas/research-landscape-claude1.md), [`ideas/_research-notes-claude2.md`](../ideas/_research-notes-claude2.md), [`ideas/_research-notes-codex.md`](../ideas/_research-notes-codex.md) |
| 3 | Built a shared **CV toolbox** (15 tasks, 4 product layers) to judge ideas | [`docs/cv-toolbox.md`](cv-toolbox.md) |
| 4 | Each agent proposed ideas (one file per idea, same template) | `ideas/*.md` |
| 5 | Deep dive on the focus subdomain (dealer & service): 9 areas, local facts, licences, scoring | [`ideas/subdomain-dealer-service-deep-dive.md`](../ideas/subdomain-dealer-service-deep-dive.md) |
| 6 | Plain-language digests per subdomain | `ideas/*-ALL-IDEAS.md` |
| 7 | Lead sorted every idea (Consider / Maybe / not) in an interactive sorter | [`tools/idea-sorter.html`](../tools/idea-sorter.html), [`ideas/SHORTLIST.md`](../ideas/SHORTLIST.md) |
| 8 | New-idea search (YC 2026, 2026 benchmarks, city programs) + GitHub / hackathon-winner check | [`ideas/NEW-IDEAS-claude1.md`](../ideas/NEW-IDEAS-claude1.md), [`ideas/research-winners-github-claude1.md`](../ideas/research-winners-github-claude1.md) |
| 9 | Validity checks (problem, beneficiaries, evidence, weak points) for the 3 finalists | [`docs/justification.md`](justification.md), [`docs/justification-cardoctor.md`](justification-cardoctor.md), [`docs/justification-roadmap.md`](justification-roadmap.md) |
| 10 | Decision and build plan | [`ideas/FINAL-PICK.md`](../ideas/FINAL-PICK.md), [`docs/tasks.md`](tasks.md) |

About 150 web searches across the three agents; sources are linked in each file.

---

## 2. The CV toolbox
Every idea was described as a combination of these tasks (numbers used in the table below) and the **4 layers** every product needs: **Perceive → Measure → Reason → Decide**.

| # | Task | # | Task | # | Task |
|---|---|---|---|---|---|
| 1 | Classification | 6 | OCR | 11 | Action recognition |
| 2 | Detection | 7 | Depth estimation | 12 | 3D reconstruction |
| 3 | Segmentation | 8 | Embeddings / retrieval | 13 | Image forensics |
| 4 | Keypoints / pose | 9 | Anomaly detection | 14 | Vision-language models |
| 5 | Tracking | 10 | Change detection | 15 | Generation / synthetic data |

We studied 17 real products to see how they combine these tasks (SafelyYou, Peloton Guide/IQ, Sportsbox AI, Drishti, Amazon Just Walk Out, FIFA semi-automated offside, John Deere See & Spray, Buildots, Hayden AI, AMP Robotics, UVeye, Tractable, Nanit, Trax, Verkada, Mobileye, Be My AI). **None of them uses forensics (13) or generation (15)** — an open gap we noted.

---

## 3. All 44 ideas
Legend — **Jury test:** ✅ the jury can test it with their own phone · ⚠️ needs an uploaded video / props · ❌ needs a fixed camera. **Status:** ⭐ final · 🟢 Consider · 🟡 Maybe · ⚪ researched, not shortlisted · 🔴 rejected (rule conflict).
By: C1 = Davlatyor + claude-1 · C2 = Muhammadjon + claude-2 · CX = Bexruz + codex.

### 3.1 Dealer & service operations
| # | Idea | What it does | CV tasks | Extra data | Jury | By | Status |
|---|---|---|---|---|---|---|---|
| 1 | Handover Guard | Photos at drop-off vs pick-up → only **new** damage | 3, 4 (anchors), 10, (12) | job timeline | ✅ | C1, CX | 🟡 |
| 2 | Warranty Check | Claim photos → reused? recaptured? part/VIN/km match? | 6, 8, 13, 3 | claim history, catalogue, flood/weather | ✅ | C1, C2, CX | ⚪ |
| 3 | Repair Check | Before/after → requested repair visible? | 3, 10 | repair checklist | ✅ | CX | 🟡 |
| 4 | TyreCheck | Tread wear + **DOT date OCR** + cracks → replace now/soon/OK | 3, 6, 7, 1 | heat/UV exposure | ✅ | C2, C1 | ⚪ |
| 5 | PartsLens / Parts Verification | Part photo → top-3 catalogue matches + number OCR | 8, 6, 2 | catalogue, fitment | ✅ (needs parts) | C2, CX | 🟡 |
| 6 | PDI Checklist | New-car photos vs delivery checklist | 3, 9 | variant checklist | ⚠️ | CX, C1 | 🟡 |
| 7 | Service-Bay Tracker ("Just Walk Out" for the workshop) | CCTV → bay busy/idle, job timeline | 2, 5, 11 | job cards | ❌ | C2, C1 | ⚪ |
| 8 | Technician Video Check | Is the recommended repair visible in the mechanic's video? | 2, 3, 7, 14 | service limits | ⚠️ | C1 | 🟡 |
| 9 | LensCheck | Photo set sharp / bright / all sides covered → retake list | 1, 8 + image quality | — | ✅ | C2 | ⚪ (stage 1 of others) |

### 3.2 Vehicle inspection
| # | Idea | What it does | CV tasks | Extra data | Jury | By | Status |
|---|---|---|---|---|---|---|---|
| 10 | Damage Estimate (Tractable-style; RoyalScan) | Photos → damaged parts + severity → repair/replace × price → estimate | 3, 1, (12) | price list | ✅ | C1, CX | 🟢 |
| 11 | TrueClaim / ClaimProof | Is the damage photo real (screen, reused, edited)? + weather/satellite story check | 13, 8, 3 | weather archive, Sentinel-1 flood maps | ✅ | C2, C1 | ⚪ |
| 12 | TradeIn PreCheck | Customer's 8 photos → damage, km OCR, windshield → eligible / not | 3, 6, 1 | dealer rules | ✅ | C2 | 🟢 |
| 13 | Repaint Radar | Panel colour mismatch + phone deflectometry → hidden repairs | 3, 10 (colour ΔE) | — | ✅ | C1 | ⚪ |
| 14 | Windshield Check | Chip / crack → repair now | 2, 3 | — | ✅ | C2 | 🟡 |
| 15 | 3D scan / plain dent finder | Phone video → 3D car with damage | 12, 3 | — | ⚠️ | C1 | ⚪ |

### 3.3 Driver & road safety
| # | Idea | What it does | CV tasks | Extra data | Jury | By | Status |
|---|---|---|---|---|---|---|---|
| 16 | RoadProof / Road Hazard Tickets | Road photo → defects → ticket → **repair verified** by second photo | 2, 3, 10 | GPS, contractor records | ✅ | C2, CX | 🟢 |
| 17 | Junction Risk Map / Crossing Conflict Review | Junction video → tracks → near-miss (TTC/PET) → danger map | 2, 5, geometry | — | ⚠️ | C1, CX | 🟢 |
| 18 | **DriveCoach** | Driver camera + road camera + GPS/IMU → risk **in context** | 4, 2, 5, 11 | GPS, accelerometer | ✅ | C1 (lead's brainstorm) | ⭐ |
| 19 | RoadGuard (dashcam video) | Dashcam → defects → one event per pothole → report | 2, 5 | GPS, crowd confirmation | ⚠️ | C2 | 🟡 |
| 20 | SmartFlow AI | Junction video → queues → suggested green split (advisory) | 2, 5 | SUMO simulation | ⚠️ | C2 | 🟢 |
| 21 | Driver Fatigue Guard / DriveAlert | Eyes, yawns, phone → alarm; "monitoring unavailable" when it can't see | 4 | — | ✅ | C2, CX | 🟡 (merged into 18) |
| 22 | Bus-Stop Access Monitor | Cars blocking the bus stop → operator ticket | 2, 5 | — | ❌ | CX | ⚪ |
| 23 | Rider Line (Ducati) | Lean angle per corner from video | 4 / horizon estimation | — | ⚠️ | C1 | ⚪ |
| 24 | Rider Gear Review | Helmet visible? → instructor review | 2 | — | ⚠️ | CX | ⚪ |
| 25 | Crosswalk Visibility Audit | Faded markings / hidden signs → ticket | 2, 3 | — | ⚠️ | CX | ⚪ |
| 26 | Work-Zone Audit | Missing cones/signs at roadworks | 2 | checklist | ⚠️ | CX | ⚪ |
| 27 | Road Debris / Blocked Sidewalk | Objects on road / sidewalk | 2, 3 | — | ⚠️ | CX | ⚪ |
| 28 | Wrong-Way Entry Review | Wrong direction in one-way area | 2, 5 | — | ❌ | CX | ⚪ |
| 29 | Reversing-Zone Conflict | Person behind reversing car in yard | 2, 5 | — | ⚠️ | CX | ⚪ |
| 30 | School-Gate Drop-Off Review | Double-parking at school gates | 2, 5 | — | ❌ | CX | ⚪ (privacy) |
| 31 | Traffic sign reading | Speed-limit signs | 2, 1 | — | ✅ | (LinkedIn) | ⚪ (commodity) |

### 3.4 EV, infrastructure & other
| # | Idea | What it does | CV tasks | Extra data | Jury | By | Status |
|---|---|---|---|---|---|---|---|
| 32 | ChargeBay Watch / EV Bay Guard | Charger bay free / charging / blocked; EV vs ICE **without plates** | 2, 1 (fine-grained) | charger session data | ❌ | C2, C1, CX | ⚪ |
| 33 | Charger Fault Triage | Charger screen photo → error code → ticket | 6 | manuals | ⚠️ | CX | ⚪ |
| 34 | EV battery underbody check | Underbody photo at intake | 3, 9 | — | ❌ | C1 | ⚪ |
| 35 | Daily Fleet Check | Shift start/end photos → new damage + who had the car | 3, 10 | shift log | ✅ | C1 | ⚪ (= #1 for fleets) |
| 36 | Ducati Chain Check | Chain + coin → stretch | 3, 4 | service bulletin limits | ⚠️ | C1 | ⚪ |
| 37 | Parking violations | Cars on sidewalks / bus lanes | 2, 6 | — | ❌ | team | 🔴 needs unconsented plates |

### 3.5 Later ideas (lead's v2 + new-idea search)
| # | Idea | What it does | CV tasks | Extra data | Jury | By | Status |
|---|---|---|---|---|---|---|---|
| 38 | **CarDoctor** (car damage + symptoms → cause → right workshop) | Photos/video (damage, **exhaust smoke colour**, **leak colour**, **dashboard warning lights**) + driver's words → LLM constrained by knowledge base → urgency, cost range, workshop | 3, 1, 2, 14 | symptom KB, workshop KB, map | ✅ | Lead (v2) | Finalist, not built (§4.2) |
| 39 | Road defects map + **contractor rating** + driver warning | Crowd/dashcam defects → map → warn drivers; durability per contractor | 2, 3, 5 | contractor records, Sentinel-2 resurfacing dates (hypothesis) | ✅ / ⚠️ | Lead (v2) | Finalist, not built (§4.3) |
| 40 | Smoky Car Spotter + emissions map | Visible exhaust smoke + traffic counts → emissions per street; checked vs Sentinel-5P NO₂ | 2, 1 | satellite NO₂ | ⚠️ | C1 | ⚪ (weak track fit) |
| 41 | Child Left in Car alarm | Child/pet still in locked car → alarm | 2, 4 / motion | — | ✅ (doll) | C1 | ⚪ |
| 42 | Dashcam Incident Narrator | Crash clip → tracking → VLM incident report | 2, 5, 14 | — | ⚠️ | C1 | ⚪ |
| 43 | Truck Overload Spotter | Tyre deflection + lifted axle → probably overloaded | 3, 4, 2 | — | ⚠️ | C1 | ⚪ |
| 44 | Cargo Check / Service-step check | Load secured? / every service step done? | 2, 3, 11 | checklist | ⚠️ / ✅ | C1, Lead | ⚪ |

Lead's sort (Sat 10 Oct, 18:45): 🟢 Consider = #10, #12, #16, #17, #18, #20 · 🟡 Maybe = #1, #3, #5, #6, #8, #14, #19, #21.

---

## 4. The three finalists
### 4.1 DriveCoach (#18) — **chosen**
| Evidence | Source |
|---|---|
| Uzbekistan 2024: 9,364 crashes, 2,203 deaths; **32.5% involved cargo/passenger transport** (Damas = 52.3% of those) | [Kun.uz](https://kun.uz/en/news/2025/02/01/one-third-of-accidents-in-2024-involved-cargo-and-passenger-transport) |
| 351 crashes (3.7%) from breaking work/rest rules → fatigue, 189 deaths (2024); **4.2% of accidents from falling asleep (Q1 2026)** | same; [Kun.uz 2025](https://kun.uz/en/news/2025/12/30/do-investments-save-lives-a-data-driven-look-at-traffic-safety-in-uzbekistan) |
| Drowsy driving 4–6× crash risk; eyes off road > 2 s ≥ 2× (re-analysis OR 1.6) | [NHTSA / VTTI 100-Car](https://www.nhtsa.gov/document/810594driverinattentionnearcrashcrashriskpdf), [re-analysis](https://trid.trb.org/view/1122843) |
| EU: drowsiness warning mandatory in all new cars from Jul 2024, distraction warning from Jul 2026 | [summary](https://captaincompliance.com/education/addw-systems-explained-eus-driver-distraction-mandate/) |
| Monitoring + coaching: high-severity events −64% / −37% in two fleets (VTTI, 3.8 M miles); ≈ −20% accidents (SWOV) | [VTTI](https://pubs.lib.uiowa.edu/driving/article/28094/galley/136386/view), [SWOV](https://www.swov.nl/en/node/14246) |
| Prior art: Dartmouth CarSafe (2013, phone, both cameras switched, P 83% / R 75%); Nauto, Samsara, Lytx | [CarSafe](https://www.cs.dartmouth.edu/~campbell/carsafe.pdf), [Nauto](https://www.nauto.com/blog/introducing-nauto-prevent) |

**Methods:** MediaPipe Face Landmarker (478 landmarks) → EAR, PERCLOS, MAR, head pose (driver); detector + tracker for the lead vehicle → ground-plane distance → headway / TTC with GPS speed, Kalman smoothing (road); explainable fusion rules (risk in context); "monitoring unavailable" state. Phone browsers cannot open both cameras at once → two paired devices. Details: [`ideas/drive-coach.md`](../ideas/drive-coach.md), [`docs/justification.md`](justification.md).

### 4.2 CarDoctor (#38) — strong, not built (data-heavy)
Problem evidence: 240k used-car sales in H1 2026; odometer-tampering fines passed (2026); insurance market +37.8% (2025); 2/3 of drivers don't trust repair shops (AAA, US). Weak spot: photo-only estimates are disputed (miss hidden damage; insurers moved to triage). Local gap: Uzbek service apps (AvtoMall, Avten) have no damage AI. → [`docs/justification-cardoctor.md`](justification-cardoctor.md).

### 4.3 Road defects map + contractor rating (#39, with #16) — strong, not built
Problem evidence (strongest locally): 25% of accidents from poor roads/infrastructure (gov, 2021 data); president's office: "new roads quickly degrade"; 816,023 m² of Tashkent streets listed for repair; Xalq nazorati photo complaints bounce between agencies. Prior art: Waze pothole reports (Selangor: 19k+ fixed); Yandex Navigator has no pothole category; **no contractor-durability product found**. → [`docs/justification-roadmap.md`](justification-roadmap.md).

| | DriveCoach | CarDoctor | Road map |
|---|---|---|---|
| Local evidence | strong | medium | strongest |
| Proof tech helps | independent studies | disputed | indirect |
| Original part | context fusion | workshop routing | contractor rating |
| Data needed tonight | none | a lot | pretrained detector + own photos |
| Live demo | ✅✅ | ✅ | ✅ |

---

## 5. Final decision
**Build DriveCoach** (Sun 11 Oct, 00:40). Reasons: one developer; runs on pretrained models (no training data needed); strongest live demo; independent evidence that monitoring helps; clear buyer (commercial fleets). CarDoctor and the road map are shown as next modules of a fleet platform. → [`ideas/FINAL-PICK.md`](../ideas/FINAL-PICK.md).

---

## 6. Methods, models and licences
| Need | Model / method | Licence | Used for |
|---|---|---|---|
| Face landmarks, eyes, head pose | **MediaPipe Face Landmarker** (`@mediapipe/tasks-vision`) | Apache 2.0 | DriveCoach driver module (in browser) |
| Drowsiness metrics | EAR (6 points/eye), **PERCLOS** (share of time eyes > 80% closed, rolling window), MAR (yawn) — rule-based, per-user calibration | method | #18, #21 ([IJSECS 2026](https://journal.lembagakita.com/ijsecs/article/view/7106)) |
| Object detection | **RF-DETR** (core + standard weights) | Apache 2.0 | vehicles, phones, defects |
| Object detection (alt.) | Ultralytics YOLO11 / YOLO26 | **AGPL-3.0** (commercial use needs Enterprise licence) | fallback |
| Segmentation | **SAM 2**; RF-DETR Segmentation | Apache 2.0 | damage, defects |
| Open-vocabulary | Grounding DINO + SAM 2 ("Grounded SAM 2"); SAM 3 (custom Meta licence) | check per model | zero-shot prototyping |
| Tracking | ByteTrack / BoT-SORT | MIT / AGPL (check) | road module, junctions |
| Monocular distance / TTC | ground-plane + vanishing-point pitch, Kalman filter | method | headway ([Bath](https://researchportal.bath.ac.uk/en/publications/distance-estimation-by-fusing-radar-and-monocular-camera-with-kal/), [Phillips et al.](https://arxiv.org/pdf/1902.01293)) |
| Lane detection | Ultra-Fast-Lane-Detection v2 | MIT (Luxonis package; upstream to verify) | lane drift |
| Embeddings / near-duplicates | **DINOv2** (Apache 2.0), PDQ hash (Meta), SSCD (licence unverified) | | #2, #5, #11 |
| Image alignment | **LightGlue + Glue Factory SuperPoint** | Apache 2.0 | #1, #3, #16 — **avoid original SuperPoint/SuperGlue (non-commercial)** |
| Anomaly detection | anomalib PatchCore | Apache 2.0 | #6, #34 |
| OCR | PaddleOCR | Apache 2.0 | DOT codes, VIN, km, part numbers |
| AI-image detection | UniversalFakeDetect (CLIP ViT-L/14 + linear head) | licence unverified | #11 (experimental only) |
| 3D | CrashSplat (Gaussian Splatting + 2D-mask lifting), DUSt3R | check | #15 |
| Weather / satellite | Open-Meteo (data CC BY 4.0; free API non-commercial); Copernicus Sentinel-1/2/5P (free & open) | | #11, #39, #40 |

---

## 7. Datasets and licences
| Dataset | Content | Licence status |
|---|---|---|
| Humans in the Loop — car parts & damages | 1,812 images, polygons | **CC0** ([page](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/)) |
| CarDD | 4,000 images, 6 damage classes | **original licence requires permission** ([terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf)) — not used in product |
| VehiDE | 13,945 images, 8 classes | licence unknown |
| RDD2022 | 47,420 road images, 6 countries | unclear (CC BY vs CC BY-SA) — verify at [sekilab](https://github.com/sekilab/RoadDamageDetector) |
| DMD (driver monitoring) | 41 h, 37 drivers, RGB/depth/IR | academic use via form — verify ([DMD](https://dmd.vicomtech.org/)) |
| State Farm distracted driver | ~22k images, 10 classes | Kaggle competition terms |
| Tyre datasets | Mendeley 1,854 imgs (CC BY 4.0 per mirror), TyreNet 1,698 | verify |
| Car parts | LSCP 84k imgs / 12 types; Roboflow car_sparePart 1,590 (CC BY 4.0) | verify |
| **Our own data** | team-recorded, consented driver & road clips (task T11) | ours — the test set we measure on |

---

## 8. Uzbekistan facts
| Fact | Source |
|---|---|
| 4,552.3 thousand private passenger cars (1 Apr 2026) | [Kursiv / stat.uz](https://uz.kursiv.media/en/2026-06-24/uzbek-national-fleet-nears-five-mln-vehicles-despite-subtle-market-slowdown/) |
| H1 2026: 157,000 new and ~240,000 used passenger cars sold | [Kun.uz](https://kun.uz/en/news/2026/08/05/uzbekistans-car-market-rebounds-in-june-as-ev-sales-surge) |
| BYD: 7,799 cars Q1 2026 (+93%); Chinese brands 17.8% share Jan–Jul 2026 | [Kun.uz](https://kun.uz/en/news/2026/03/28/uzauto-motors-loses-market-share-amid-rising-competition), [The Star](https://www.thestar.com.my/news/world/2026/08/13/uzbekistan-car-sales-down-36-pct-in-jan-july) |
| Road deaths: 2,203 (2024), 2,188 (2025); Q1 2026 causes: speeding 32.9%, ignoring signals 22.4%, falling asleep 4.2% | [AKIpress](https://akipress.com/news:838901:2,203_people_die_in_traffic_accidents_in_Uzbekistan_in_2024), [Kun.uz](https://kun.uz/en/news/2026/01/15/traffic-deaths-remain-high-across-uzbekistan-despite-prevention-efforts) |
| 1,399 public EV chargers (May 2025), target 4,000 by end-2026 | [Daryo](https://daryo.uz/en/2025/05/04/uzbekistan-sees-2-5-fold-surge-in-ev-charging-stations-1216442/), [Kun.uz](https://kun.uz/en/news/2026/05/05/uzbekistan-to-expand-ev-charging-network-to-4000-stations-by-end-of-2026) |
| Insurance market 13.46 trn soums in 2025 (+37.8%); compulsory motor cover limit 40 → 80 M soums from 2026 | [UzDaily](https://www.uzdaily.uz/en/uzbekistans-insurance-market-grows-378-in-2025/) |
| Toyota distributor: Toyota Central Asia FZE (warranty 3 y / 100,000 km); BYD Royal Motors service site byd-rm.uz | [Devex](https://www.devex.com/organizations/toyota-central-asia-fze-127212), [byd-rm.uz](https://byd-rm.uz/service) |
| Tashkent PM2.5 2024 average 31.5 µg/m³ (6.3× WHO); vehicles ~16% of sources (IQAir, secondhand) | [Times CA](https://timesca.com/tashkent-choked-by-smog-what-2025-revealed-and-how-residents-are-responding/) |
| Andijan flood + mudflow 14 Jul 2024 mapped from Sentinel-1 | [Sentinel Asia](https://sentinel-asia.org/EO/2024/article20240714UZ.html) |

---

## 9. Prior art and competitors
| Area | Players (examples) |
|---|---|
| Driver monitoring | Nauto, Samsara, Lytx, Netradyne, Seeing Machines; research: CarSafe (Dartmouth 2013) |
| Damage inspection / estimates | Tractable, UVeye, Ravin, Click-ins, CCC, autobiz Noa; GitHub: [AI-vehicle-damage](https://github.com/AkshatRathore3311/AI-vehicle-damage), [car-damage-detection-yolo](https://github.com/cloudwhynot/car-damage-detection-yolo) |
| Photo → body-shop matching | BodyShopBids (2011), DingIt (2012), CCC Repair Cost Predictor; Uzbekistan: AvtoMall, Avten (no damage AI) |
| Dealer service | SKAIVISION, PitCrew, myKaarma, DealerWare (AI diff "not in this release"), TruVideo |
| Photo authenticity | Truepic, PZU PhotoDetective, SAS (2026 warnings on AI-edited claim photos) |
| Road condition | Waze (pothole reports), RoadBotics, PaveX, CivicScan, Lvl5; Devpost: OpenPotholeMap, PotholeGO |
| Traffic / junctions | VivaCity (near-miss), Hayden AI (bus lanes), many adaptive-signal student projects |
| EV bays | PoGo + Intelli-Park, Zevtron + SpotGenius (ANPR-based) |
| New in 2026 | YC S26 "Dream" (pocket AI cameras for dealer condition records); InsureVision VisionScore on 150k cameras; AUTOPILOT-VQA dashcam benchmark |

---

## 10. Principles we adopted
1. **A system, not one API call** — at least 3–4 CV tasks + our own measure/reason layers.
2. **Vision + context data → decision** (from the lead's pheromone-trap work: CV + weather + knowledge base) — [`ideas/principle-vision-plus-context.md`](../ideas/principle-vision-plus-context.md).
3. **Honest numbers only** — every metric measured on our own test set, split by session/scene (no neighbouring-frame leakage), with known failure cases (night, glasses, glare).
4. **Privacy** — no unconsented faces or plates; only team members on camera.
5. **Licences checked** — prefer Apache 2.0 (MediaPipe, RF-DETR, SAM 2, DINOv2, LightGlue + GlueFactory SuperPoint, anomalib, PaddleOCR).
6. **A human makes the final call** — the system gives evidence and alerts.

---

## 11. Index of detailed files
| File | Content |
|---|---|
| [`docs/task.md`](task.md) | Task statement |
| [`docs/cv-toolbox.md`](cv-toolbox.md) | 15 CV tasks, 4 layers |
| [`docs/domain-dealer-service.md`](domain-dealer-service.md) | Dealer & service domain map |
| [`docs/justification.md`](justification.md) · [`-cardoctor`](justification-cardoctor.md) · [`-roadmap`](justification-roadmap.md) | Finalist validity checks |
| [`ideas/README.md`](../ideas/README.md) | Index of every idea file |
| [`ideas/DEALER-SERVICE-ALL-IDEAS.md`](../ideas/DEALER-SERVICE-ALL-IDEAS.md) · [`VEHICLE-INSPECTION`](../ideas/VEHICLE-INSPECTION-ALL-IDEAS.md) · [`ROAD-SAFETY`](../ideas/ROAD-SAFETY-ALL-IDEAS.md) · [`EV-AND-OTHER`](../ideas/EV-AND-OTHER-ALL-IDEAS.md) | Plain-language digests |
| [`ideas/research-landscape-claude1.md`](../ideas/research-landscape-claude1.md) | Landscape, methods, datasets |
| [`ideas/subdomain-dealer-service-deep-dive.md`](../ideas/subdomain-dealer-service-deep-dive.md) | 9-area deep dive, licences, scoring |
| [`ideas/research-winners-github-claude1.md`](../ideas/research-winners-github-claude1.md) | GitHub repos, hackathon winners, new models |
| [`ideas/NEW-IDEAS-claude1.md`](../ideas/NEW-IDEAS-claude1.md) | New ideas (YC 2026, benchmarks, city programs) |
| [`ideas/_research-notes-claude2.md`](../ideas/_research-notes-claude2.md), [`ideas/_research-notes-codex.md`](../ideas/_research-notes-codex.md) | Teammates' research notes |
| [`ideas/LEAD-IDEAS-V2.md`](../ideas/LEAD-IDEAS-V2.md), [`ideas/SHORTLIST.md`](../ideas/SHORTLIST.md), [`ideas/FINAL-PICK.md`](../ideas/FINAL-PICK.md) | Lead's direction, sort, final pick |
| [`docs/worklog.md`](worklog.md) | Timeline of all work |
