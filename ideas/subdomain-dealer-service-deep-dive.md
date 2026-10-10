---
name: Deep dive — all 9 areas of Dealer & service operations
added_by: Davlatyor + claude-1
date: Sat 10 Oct 17:20
direction: dealer / service operations
---

# Deep dive: all 9 areas (claude-1, 16 more searches)

Builds on `docs/domain-dealer-service.md` (map) and `ideas/subdomain-dealer-service-claude1.md` (competitors). Vendor numbers = their claims.

## 1. Local market facts (for the deck — all sourced)
| Fact | Source |
|---|---|
| 4,552.3 thousand passenger cars owned by individuals (1 Apr 2026), +344.6k in a year | [stat.uz via Kursiv](https://uz.kursiv.media/en/2026-06-24/uzbek-national-fleet-nears-five-mln-vehicles-despite-subtle-market-slowdown/) |
| New passenger cars sold H1 2026: 157,000 (+3.5% y/y); used: ~240,000 (−18% y/y) | [kun.uz, Aug 2026](https://kun.uz/en/news/2026/08/05/uzbekistans-car-market-rebounds-in-june-as-ev-sales-surge) |
| BYD Uzbekistan: 7,799 cars Q1 2026 (+93%), 10,927 Jan–Apr → 4th nationally | [kun.uz, Mar 2026](https://kun.uz/en/news/2026/03/28/uzauto-motors-loses-market-share-amid-rising-competition), [daryo.uz](https://daryo.uz/en/2026/04/20/uzautomotors-market-share-falls-below-80-as-byd-and-rivals-expand-in-uzbekistans-auto-sector/) |
| Chinese brands 17.8% share Jan–Jul 2026 (11.6% a year earlier); UzAuto 47.8% Jan–Apr (was ~90% two years ago) | [The Star, Aug 2026](https://www.thestar.com.my/news/world/2026/08/13/uzbekistan-car-sales-down-36-pct-in-jan-july), [kun.uz May 2026](https://kun.uz/en/news/2026/05/28/uzauto-motors-loses-its-majority-grip-on-uzbekistans-car-market-cb66be) |
| Toyota distributor for UZ/TJ/TM: Toyota Central Asia FZE; warranty 3 years / 100,000 km | [Devex](https://www.devex.com/organizations/toyota-central-asia-fze-127212) |
| "Royal Motors" listed as Toyota showroom + Toyota repair, Zargar st 3/1, Tashkent (directory; authorised status not verified); no BYD link found | [Golden Pages](https://www.goldenpages.uz/rubrics/?Id=103161) |
| BYD Seal 6 owner: car at service 4 days, parts "from China" (one case) | [kun.uz, Mar 2026](https://kun.uz/ru/news/2026/03/13/3-raza-vyshla-iz-stroya-za-10-dney-v-tashkente-kuplennyy-byd-seal-6-okazalsya-brakovannym) |
| Competition Committee ordered UzAuto Motors to stop charging for work not actually carried out (date not confirmed) | [OCCRP (ru)](https://www.occrp.org/ru/novosti/antimonopolnyi-komitet-uzbekistana-obvinil-uzauto-motors-v-zavysenii-cen-na-avtomobili) |
| OSAGO mandatory; KASKO voluntary; no public data found on photo fraud in UZ claims | [gross.uz](https://gross.uz/en/press_center/blog/201) |
| Andijan flood + mudflow 14 Jul 2024 mapped from Sentinel-1 (15 Jul) | [Sentinel Asia](https://sentinel-asia.org/EO/2024/article20240714UZ.html) |

**Implication:** the BYD service base is growing fast (sales nearly doubling) → service capacity, warranty volume and check-in disputes grow with it.

## 2. Model / licence choices (important: repo will be public, product story is commercial)
| Need | Use | Licence | Note |
|---|---|---|---|
| Detection | **RF-DETR** (core + standard weights) | Apache 2.0 | XL/2XL "plus" models have other terms ([Roboflow](https://blog.roboflow.com/rf-detr-is-free-to-use-commercially/)) |
| Detection (alt.) | Ultralytics YOLO11 | **AGPL-3.0** | OK for a fully public repo, but commercial closed use needs Enterprise licence ([Ultralytics forum](https://community.ultralytics.com/t/yolov11-agpl-license-for-on-premises-use/1529)) → say this in Business slide |
| Segmentation | **SAM 2** | Apache 2.0 | SAM 3 has a new licence — check ([Roboflow](https://roboflow.com/model-licenses/segment-anything-2)) |
| Embeddings / near-duplicates | **DINOv2** | Apache 2.0 (changed from CC-BY-NC) | SSCD (Meta copy detection) licence unverified; **PDQ** hash (Meta) for fast exact-ish dupes ([SSCD paper](https://arxiv.org/pdf/2202.10261), [pdqhash](https://pypi.org/project/pdqhash/)) |
| AI-generated image check | UniversalFakeDetect (CLIP ViT-L/14 + linear head) | licence unverified | Generalises GAN→diffusion ([README](https://raw.githubusercontent.com/WisconsinAIVision/UniversalFakeDetect/main/README.md)) |
| Screen recapture | own classifier (moiré/FFT features) | — | Few detection datasets; survey [Hussain et al.](https://uia.brage.unit.no/uia-xmlui/handle/11250/3033411); DLC-2021 for documents |
| Image alignment | **LightGlue + Glue Factory SuperPoint** | Apache 2.0 | **Avoid original SuperPoint/SuperGlue** (non-commercial) ([glue-factory](https://github.com/cvg/glue-factory)) |
| Anomaly | **anomalib** PatchCore | Apache 2.0 | Trains on normal images only ([Datature guide](https://datature.io/blog/visual-anomaly-detection-with-anomalib-a-hands-on-guide-2026)) |
| Weather | Open-Meteo historical | data CC BY 4.0; free API = non-commercial | Commercial plan → cost model ([licence](https://open-meteo.com/en/licence)) |
| Satellite | Copernicus Sentinel-1/2 | free & open | |

## 3. The 9 areas
### A. Check-in / check-out (Handover Diff)
- **Pain:** "you scratched my car". Competitors: myKaarma = manual tags; DealerWare = side-by-side photos, **AI diff "not in this initial release"** ([DealerWare](https://support.dealerware.com/hc/en-us/articles/53458053275283-Vehicle-Walkaround-Inspection)).
- **Method:** guided capture of 8 fixed views → car-part segmentation → per-panel alignment (LightGlue homography) → damage seg in both → diff masks → "new since check-in" with time window. Stretch: 3D lift (CrashSplat).
- **Data:** CarDD (licence to verify), HITL parts+damage **CC0**; own before/after pairs (stick removable tape = synthetic "new scratch"!).
- **Context data:** job timeline (who had the car when).
- **Jury test:** ✅ photograph a car, add a sticker/tape, photograph again → only the new mark flagged.
- **Risk:** reflections on glossy paint → false diffs; lighting change between photos.

### B. Technician video audit (MPI Video Auditor)
- **Pain:** upsell distrust; "I'm not gonna look at 10,000 videos" ([Dealership Guy](https://news.dealershipguy.com/p/how-niello-co-s-fixed-ops-director-employs-ai-to-help-monitor-mpi-videos-2026-04-14)).
- **Method:** VLM/open-vocab to find the part in the video → specialist measures: tread depth (vendor CNN ±1.5 mm on 90% — [QBurst](https://www.qburst.com/en-us/resources/case-studies/tire-inspection-system), claim), pad thickness (patent stage only — [US12117059](https://patents.google.com/patent/US12117059)), leaks (seg).
- **Jury test:** ⚠️ needs close-ups of brakes/tyres; tyres feasible in parking lot.
- **Risk:** pad thickness from video has **no published accuracy** → hard to prove.

### C. Warranty (WarrantyProof)
- **Pain:** est. 10–20% of warranty spend lost (industry estimate) ([AutoSuccess](https://www.autosuccessonline.com/warranty-fraud-in-the-dealer-network-costs/)); reused turbo/rim photos, 29 claims, $350k ([Truepic](https://www.truepic.com/blog/snapshot-impact-of-image-authenticity-for-the-auto-warranty-industry)).
- **Method:** PDQ hash + DINOv2 embeddings vs all past claim photos (reuse) → recapture + AI-image check (forensics) → part match (embeddings vs catalogue + part-number OCR) → VIN / odometer OCR vs claim → weather/flood check for water-damage claims.
- **Payer:** Toyota Central Asia FZE (warranty 3y/100k km) / BYD importer warranty dept → Partner mode: "warranty dept, claim approval process".
- **Jury test:** ✅ upload a claim photo; re-upload a cropped/rotated copy → "reused"; photo of a laptop screen → "recaptured".
- **Risk:** we have no real claim data → synthetic claim set (declared).

### D. Parts counter (PartsLens)
- **Method:** DINOv2 embedding search over catalogue photos → top-3 + OCR of stamped numbers. nyris benchmark top-1 only 32.49% → show top-3 ([nyris](https://benchmark.nyris.io/models/automotive_v1)).
- **Data:** Kaggle "50 types of car parts" (licence unverified), Roboflow car_sparePart 1,590 imgs CC BY 4.0, LSCP 84k imgs/12 types ([arXiv](https://arxiv.org/abs/2311.11754)).
- **Jury test:** ✅ any part. **Risk:** OEM catalogue images not public → low realism.

### E. Service bays (tracker / "Just Walk Out" for the bay)
- **Method:** fixed CCTV zones → car in bay, people count, timeline (SKAIVISION/PitCrew pattern).
- **Jury test:** ❌ needs CCTV; only recorded video. Lowest live score.

### F. PDI / stock yard
- **Method:** anomalib PatchCore on normal panels → anomaly map; damage seg.
- **Jury test:** ✅ but new cars rarely at hand. Competes with UVeye/Camcom arches.

### G. Trade-in (TradeIn PreCheck / Repaint Radar)
- **Market:** ~240k used-car sales in H1 2026 ([kun.uz](https://kun.uz/en/news/2026/08/05/uzbekistans-car-market-rebounds-in-june-as-ev-sales-surge)) — big.
- **Method:** guided photos → damage + odometer OCR + panel colour mismatch (ΔE Lab) → price adjustment vs market (OLX/avtoelon listings — scraping terms to check).
- **Jury test:** ✅. **Risk:** repaint detection needs ground truth.

### H. Tyres (TyreCheck)
- **Method:** tyre seg → polar unwrap → DOT code OCR (Kazmi et al. pipeline: Hough circle → unwrap → CNN; [Aston](https://research.aston.ac.uk/en/publications/an-efficient-industrial-system-for-vehicle-tyre-tire-detection-an/)) or VLM read (Roboflow 2026 tutorial: RF-DETR crop + multimodal LLM → accept / review / retake — [Roboflow](https://blog.roboflow.com/automated-tire-sidewall-ocr/)); tread depth CNN; cracks classifier.
- **Data:** tyre defect sets: Mendeley 1,854 imgs (CC BY 4.0 per mirror), TyreNet 1,698, Roboflow (CC BY 4.0 / PD) ([Mendeley](https://data.mendeley.com/datasets/bn7ch8tvyp), [TyreNet](https://data.mendeley.com/datasets/32b5vfj6tc)); public demo trained on 730 tyres ([HF demo](https://uncodespecial-tire-tread-depth.hf.space/)).
- **Context data:** heat/UV exposure (Open-Meteo) → rubber ageing.
- **Jury test:** ✅ any tyre in the parking lot. **Risk:** DOT text is faint black-on-black.

### I. Ducati chain check
- **Method:** chain seg + coin scale → pitch measurement → stretch %; Ducati bulletin: kit ≤ 20,000 km ([NHTSA TSB](https://static.nhtsa.gov/odi/tsbs/2019/MC-10169798-0001.pdf)).
- **Jury test:** ⚠️ needs a motorcycle. Unoccupied niche.

## 4. Scoring (claude-1 estimate, 0–10; weights from task: Tech 25, Innov 25, Impact 25, Pres/demo 15, Business 10)
| Area | Tech | Innov | Impact | Demo | Business | Weighted | 8 h feasible |
|---|---|---|---|---|---|---|---|
| **C. Warranty** | 8 | 9 | 7 | 8 | 8 | **8.0** | yes |
| **A. Check-in/out** | 8 | 7 | 8 | 9 | 7 | **7.8** | yes |
| H. Tyres | 7 | 6 | 7 | 9 | 6 | 7.0 | yes |
| G. Trade-in | 7 | 6 | 7 | 8 | 7 | 6.9 | yes |
| B. MPI audit | 7 | 8 | 7 | 5 | 7 | 6.9 | risky |
| D. Parts | 6 | 6 | 6 | 8 | 6 | 6.3 | yes |
| I. Ducati chain | 6 | 8 | 5 | 4 | 5 | 5.9 | risky |
| F. PDI | 6 | 4 | 6 | 6 | 6 | 5.5 | yes |
| E. Service bays | 7 | 5 | 7 | 2 | 7 | 5.8 | demo weak |

## 5. Recommendation
**C (Warranty trust) + A (check-in/out diff) share one engine**: alignment, damage seg, embeddings, forensics. Pitch: "**Evidence engine for the service desk**" — one product, two moments where photos decide money: (1) check-in/out disputes with the customer, (2) warranty claims to the importer. Tyres (H) as a small add-on if time allows.
