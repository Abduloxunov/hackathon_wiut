# Hackathon winners + GitHub + new models — check against our ideas (claude-1, Sat 10 Oct ~19:20)

10 searches. Goal: what already exists for the lead's ideas (`LEAD-IDEAS-V2.md`), and what is new.
Repo numbers are self-reported by their authors (unverified).

## Bottom line
| Idea | Already done by others? | Our gap |
|---|---|---|
| 2. Car damage → cost → mechanic | **Damage + cost: many GitHub repos.** Photo → nearby body-shop quotes existed in the US (BodyShopBids 2011, DingIt 2012, an unnamed 2025 app, CCC Repair Cost Predictor). | **In Uzbekistan nobody combines photo AI + routing to the right workshop.** Local apps (AvtoMall, Avten) book services but have no damage AI. |
| 3. Road defects map + contractor rating | **Pothole maps: very many** (Devpost: OpenPotholeMap with driver alerts, PotholeGO with rewards, Plotholes). Commercial: PaveX, DromoTrax, RoadBotics, CivicScan. | **Linking defects to the contractor and tracking durability — no company found doing it end to end.** US road warranties (2–7 years) exist, so the need is real. |
| 1. Smart traffic lights | **Crowded:** many student/hackathon projects (UrbanGrid 2025, Adaptive-Traffic-Signal-Timer on GitHub) and papers. | Only our elimination code would make it different. |

## Idea 2 — car damage → cost → mechanic
**Open-source to learn from (check licences before using code/weights):**
- [AkshatRathore3311/AI-vehicle-damage](https://github.com/AkshatRathore3311/AI-vehicle-damage) — YOLO11-seg, 6 damage classes, cost range + uncertainty + itemised labour/parts (its cost accuracy claim has unclear ground truth).
- [cloudwhynot/car-damage-detection-yolo](https://github.com/cloudwhynot/car-damage-detection-yolo) — YOLO26 seg, car parts + defects, severity = damage area / part area, PDF report, Gradio, Docker.
- [ifas-123/car-damage-detection-insurance-system](https://github.com/ifas-123/car-damage-detection-insurance-system) — YOLOv8s, cost from damage type + size + **brand tier**, Streamlit + SQLite.
- [sf9393/vehicle-damage-inspection-system](https://github.com/sf9393/vehicle-damage-inspection-system) — YOLOv8-seg; names weights `abdullahg7/cardd-yolov8s` (MIT) — **but trained on CarDD, whose licence needs permission**.
- [GitHub topic: car-damage-detection](https://github.com/topics/car-damage-detection).
- Google Gemini competition: [CarServe](https://ai.google.dev/competition/projects/carserve) — photos + price data → Gemini → estimate. This is the "one prompt behind a UI" pattern the jury scores low.

**Photo → body-shop matching (prior art):** [BodyShopBids](https://tech.co/?p=41266) (2011, Chicago, quotes from nearby shops within 24 h), [DingIt](https://digitaldealer.com/news/dingit-releases-iphone-app-for-auto-body-shop-estimates/30608/) (2012), [unnamed app, Repairer Driven News, Sep 2025](https://www.repairerdrivennews.com/2025/09/11/mobile-app-provides-nearby-collision-estimates-to-consumers-following-crash/), CCC Repair Cost Predictor via Carwise ([source](https://www.repairerdrivennews.com/2/)). Lesson: always present the cost as a **range**, confirmed by the shop in person.

**Uzbekistan market (our gap):**
- [AvtoMall](https://mwm.ai/apps/avtomall/6755456954) — App Store, first release 30 May 2026: parts + service booking (tyres, wash, repair, diagnostics, EV charging), partners incl. KIA. **No damage AI.** → possible partner/competitor.
- [Avten](https://awards.gov.uz/en/ecosystem/startups-directory/3647) — Qarshi, founded Mar 2026, pre-seed: nearest car service + roadside help by GPS. 0 users listed.
- [Auto.uz](https://app.dealroom.co/companies/auto_uz) — car marketplace + pre-purchase inspections.
- Repair shops mostly advertise informally (OLX).

## Idea 3 — road defects + contractor rating
- Devpost: [OpenPotholeMap](https://devpost.com/software/openpotholemap) (phone camera, live map, driver alerts, export for authorities), [PotholeGO](https://devpost.com/software/potholego) (points/badges for reports — like our reward idea), [Plotholes](https://devpost.com/software/plothole) (311 data + heatmaps + safer routes), [PotPlot](https://devpost.com/software/potplot).
- Winner: [Olomouc Region Hackathon 2025](https://www.geoinformatics.upol.cz/kat/news-en) — predicts road-damage risk from live sensor data.
- [Pothole Patrol, ETHGlobal](https://ethglobal.com/showcase/pothole-patrol-9v0u8) — YOLOv8 on phones; prize winner.
- Commercial: [PaveX (Purdue, 3,400+ miles since Jan 2025)](https://www.purdue.edu/newsroom/2025/Q3/ai-tech-from-startup-pavex-improves-consistency-speed-and-cost-of-road-condition-assessments/), [CivicScan (UW, phone on windshield)](https://www.geekwire.com/2025/eyes-and-ai-on-the-road-uw-grads-platform-scans-for-pavement-defects-to-speed-repair-lower-costs/), [RoadBotics / FM Conway](https://fmconway.co.uk/our-services/consultancy/roadbotics), [Pavewise (contractor-side quality)](https://www.enr.com/articles/62582-tech-consultant-launches-data-driven-paving-platform).
- **Contractor warranties exist:** contractors warrant pavement 2–7 years (sometimes up to 20) and fix construction defects at their cost ([Pavement Interactive](https://pavementinteractive.org/reference-desk/qc-qa/specifications/performance-specifications/)); agencies track warranty pavements with condition data ([FHWA study](https://highways.dot.gov/media/56986)). **No startup found that links AI defect data to the responsible contractor end to end** (one search — not proof).
- GitHub road damage: [VivekVagale/road-hazard](https://github.com/VivekVagale/road-hazard) (YOLO11 on RDD2022-India; **splits by blocks of 25 frames to avoid train/test leakage** — copy this practice), [oracl4/RoadDamageDetection](https://github.com/oracl4/RoadDamageDetection) (YOLOv8-small weights on CRDDC2022), [watchiravitdon-lgtm/road-damage-detector-final-V.2](https://github.com/watchiravitdon-lgtm/road-damage-detector-final-V.2) (location from EXIF). RDD2022: 47,420 images, 6 countries; licence unclear (CC BY vs CC BY-SA) — check [sekilab/RoadDamageDetector](https://github.com/sekilab/RoadDamageDetector).

## Idea 1 — smart traffic lights
- [UrbanGrid (lablab.ai, Jan 2025)](https://lablab.ai/submissions/cm6bs5bhh000p2a6mf0dxplqx) — YOLOv11 accident detection + plates + signal timing by vehicle count.
- [mihir-m-gandhi/Adaptive-Traffic-Signal-Timer](https://github.com/mihir-m-gandhi/Adaptive-Traffic-Signal-Timer) — YOLO density → signal timing (2020).
- 2026 papers claim ~30–45% less waiting ([ISSF 2026](https://www.atlantis-press.com/proceedings/issf-26/126025031), [EAI 2026](https://publications.eai.eu/index.php/ismla/article/view/12670)) — simulation claims, not ours to quote.

## New models (nothing big found for Sep–Oct 2026)
Latest vision-specific releases in Roboflow's catalogue ([source](https://blog.roboflow.com/best-open-source-computer-vision-models/)): **RF-DETR Segmentation** (Oct 2025, **Apache 2.0**, detection + instance seg + keypoints), **YOLO26** (Oct 2025, AGPL-3.0, faster on CPU), **SAM 3** (Nov 2025, custom Meta licence, text-prompted segment + track). → **RF-DETR-Seg is the cleanest choice for our damage/defect segmentation.**

## Automotive CV hackathons 2026
[FPT Automotive Hackathon (Vietnam, Aug 2026)](https://fpt.com/en/news/fpt-news/fpt-to-chuc-automotive-hackathon-dau-tien-tong-giai-thuong-250-trieu-dong), [1st India CV Hackathon 2026](https://www.startupgrantsindia.com/1st-india-computer-vision-hackathon-2026) — winners not published in results.
