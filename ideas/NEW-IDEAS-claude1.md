# New ideas (not in our lists yet) — claude-1, Sat 10 Oct ~19:45

From 12 new searches: YC 2026 batches, startup funding, 2026 benchmarks, city programs. Each idea is **new for our team**. Vendor/paper numbers are their claims.

---

## 1. Smoky Car Spotter + traffic emissions map ⭐ (uses Davlatyor's satellite skill)
**Story:** Tashkent is regularly among the world's most polluted cities. Old cars on low-octane AI-80 fuel and smoky buses/trucks add to it.
**Product:**
1. Street/traffic camera video → detect vehicles + **visible black exhaust smoke** (YOLO smoke detector).
2. Count vehicle types per street → estimate traffic emissions per street, per hour.
3. Check against **Sentinel-5P NO₂ satellite data** (a Brazilian study found satellite NO₂ correlates with highway traffic counts, r = 0.69).
4. Output: smoky-vehicle alerts for **fleet owners** (their own buses/trucks → send to maintenance) + an emissions map for the city.
- **Facts:** Tashkent 2024 PM2.5 average 31.5 µg/m³ (6.3× WHO); vehicles ~16% of sources (IQAir, cited secondhand), more in calm winter months; city transport emissions 212k t (2021) → 403k t (2022). ([Times CA](https://timesca.com/tashkent-choked-by-smog-what-2025-revealed-and-how-residents-are-responding/), [IQAir](https://www.iqair.com/us/newsroom/tashkent-among-the-most-polluted-cities-in-the-world-11-20-2025), [Kun.uz](https://kun.uz/en/news/2025/12/22/beyond-tashkent-air-quality-is-a-national-problem-are-policies-keeping-up?hl=en-GB))
- **Prior work:** smoky-vehicle YOLOv8 77.7% mAP on 1,034 images ([EPJ 2025](https://www.epj-conferences.org/articles/epjconf/abs/2025/28/epjconf_aimace2025_05001/epjconf_aimace2025_05001.html)); public CCTV black-smoke dataset from China ([Applied Sciences 2024](https://doaj.org/article/644cd9109bad4678b7d5455f9fd50bd8)); London CCTV traffic → NO₂ ([arXiv](https://arxiv.org/abs/2501.00056v1)); Sentinel-5P vs traffic ([EGU25 Campinas](https://meetingorganizer.copernicus.org/EGU25/EGU25-9328.html)).
- ⚠️ Fit: "road safety / automotive" is a stretch → frame as **fleet maintenance + city**. No plate reading (task rule) → fleets check their own vehicles. Jury: upload a street video.

## 2. Child Left in Car alarm
**Story:** in Tashkent summers a parked car heats up fast; a child or pet forgotten inside is in danger.
**Product:** a cheap cabin camera / old phone → after the car is locked, detects a child (or pet) still inside (movement, breathing motion) → alarm to the parent's phone.
- **Why now:** Euro NCAP scores **Child Presence Detection** and its stricter rules apply from 2026 (direct sensing of movement/breathing, all seats, children up to 6). ([Smart Eye summary](https://smarteye.se/blog/what-euro-ncap-2026-says-about-child-presence-detection/), [Euro NCAP CPD protocol](https://cdn.euroncap.com/media/83740/euro-ncap-cpd-test-and-assessment-protocol-v13.pdf))
- **Partner fit:** an aftermarket kit Toyota/BYD dealers can sell for older cars that lack the feature.
- **Jury demo:** ✅ a doll in a car seat; a judge leaves the "car" → alarm. Breathing motion = the Nanit trick.
- ⚠️ Real systems often use radar/thermal; camera fails in darkness — say so. Children in images → demo with dolls only.

## 3. Dashcam Incident Narrator (for insurers and fleets)
**Story:** after a crash, the insurer gets a dashcam clip — someone must watch it and write what happened.
**Product:** crash clip → our pipeline (detect + track vehicles, speeds, moment of impact) → a **vision-language model writes the incident report**: what happened, who hit whom, possible fault factors, severity → first notice of loss in minutes.
- **New in 2026:** AUTOPILOT-VQA benchmark for incident-centric dashcam questions (Jul 2026, CVPR 2026 competition) ([arXiv](https://arxiv.org/abs/2607.08745)); InsureVision's VisionScore licensed on 150k cameras (Jun 2026) ([fintech.global](https://fintech.global/?p=243254)); NVIDIA VLM-AutoDrive (Mar 2026).
- ⚠️ A VLM alone = "one prompt behind a UI". Our tracking + timeline must feed it (and our elimination code does tracking).
- Jury: upload a crash clip (public datasets / YouTube with permission).

## 4. Truck Overload Spotter
**Story:** overloaded trucks destroy roads (links to the road-defects idea).
**Product:** side camera at a road → truck tyres → **tyre squash (deflection)** + **lifted-axle** detection → "probably overloaded → send to the weighbridge".
- **Prior work:** lifted-axle detection with YOLO, precision 87%, recall 91.7% (Cerema, France, 2025) ([HVTT](https://hvttforum.org/wp-content/uploads/2025/07/845.pdf)); tyre deflection → load from images ([Applied Sciences 2022](https://doaj.org/article/9d26606b89a04ce6aca36b39dc52173b)); public truck wheel/rim dataset ([HF](https://huggingface.co/datasets/frmc/Truck-Wheel-Rim-Line-Dataset/blob/main/README.md)).
- ⚠️ Screening only, not legal weighing. Demo needs truck images.

## 5. Cargo Check before departure (logistics)
**Story:** Davlatyor mentioned truck fleets — badly tied cargo falls, doors open, loads overhang.
**Product:** driver photographs the loaded truck → straps present? load overhangs? doors closed? → "OK to go / fix this".
- Prior: Motive's AI Omnicam checks cargo tied down and unauthorized access ([TruckNews](https://www.trucknews.com/products/motive-unveils-ai-omnivision/)); transload (YC Spring 2026) measures items with warehouse CCTV ([YC](https://ycombinator.com/companies/transload)).
- Jury: ⚠️ needs a truck or a toy truck with straps.

## 6. Smaller signals worth knowing
- **Dream (YC Summer 2026):** pocket-sized battery AI cameras for dealers/rental/fleets — photograph every passing vehicle from all angles → condition record ([YC](https://www.ycombinator.com/companies/industry/computer-vision)). Confirms our Handover Guard direction is investable.
- **Smart school crossing:** Hwaseong (Korea) runs AI CCTV + barriers synced with signals at 36 schools; idea — speed limit drops only when children are detected near the kerb ([TRID](https://trid.trb.org/View/2509203)).
- **Noise cameras for loud exhausts:** NYC's 12 cameras caught 15,994 loud-vehicle events in 2025 ([TechSpot](https://www.techspot.com/news/114010-loud-exhaust-could-earn-you-camera-issued-fine.html)) — needs plates → task rule problem.
- **Car wash AI:** vehicle type → right wash package; damage-dispute video ([Spot AI](https://www.spot.ai/blog/car-wash-camera-system)) — weak.

## claude-1 ranking of the new ideas
1. **Smoky Car Spotter + emissions map** — local pain, satellite angle nobody else has, but weakest fit to "automotive/road safety".
2. **Child Left in Car** — simplest strong demo, regulation trend, dealer-sellable kit.
3. **Dashcam Incident Narrator** — newest tech trend (2026 benchmark), insurer buyer, reuses our tracking.
4. Truck Overload Spotter · 5. Cargo Check.
