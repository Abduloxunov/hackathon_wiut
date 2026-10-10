---
name: Subdomain research — Dealer & service operations (claude-1)
added_by: Davlatyor + claude-1
date: Sat 10 Oct 16:05
direction: dealer / service operations
---

# Dealer & service operations — what exists, methods, gaps

Vendor numbers = their claims, unverified. Not for the deck.

| Area | Who / what | Method | Source |
|---|---|---|---|
| Service-bay analytics | SKAIVISION (Reynolds & Reynolds invested Dec 2024; case: Fred Anderson Toyota, ~30 cameras), PitCrew (Leverege) | Existing CCTV → detect car arrival in bay, work start/end, technician count per bay → cycle time, idle time, wait time | [Auto Remarketing](https://www.autoremarketing.com/?p=70219), [SKAIVISION case](https://skaivision.lovable.app/case-studies/fred-anderson-toyota-raleigh), [Leverege](https://www.leverege.com/blogpost/turn-your-existing-bay-cameras-into-a-profit-engine-4-ways-ai-can-supercharge-service-center-operations), [IoT For All](https://www.iotforall.com/automotive-service-bays-with-ai-and-computer-vision) |
| Stock-yard / lot | MyDealerLot (beacons + LPR + drone, 2016), Manheim Lot Vision, Conexio Fleet Watch | Drone flights / beacons / phone GPS to locate cars; drone + AI research (ICAART 2025) | [RFID Journal](https://www.rfidjournal.com/?p=70981), [WardsAuto](https://www.wardsauto.com/news/archive-wards-manheim-uses-new-locator-system-to-track-millions-of-vehicles/793032/), [SciTePress 2025](https://scitepress.org/Papers/2025/132849/132849.pdf) |
| Parts identification | team neusta case (2026), nyris, HK EMSD trial | **ViT embeddings of catalogue images → nearest-neighbour search** + verification score; read stamped numbers (OCR). nyris automotive benchmark top-1 only 32.49% → shortlist matters | [team neusta](https://www.team-neusta.de/en/cases/2026/ai-powered-part-search), [nyris benchmark](https://benchmark.nyris.io/models/automotive_v1), [EMSD](https://inno.emsd.gov.hk/en/it-solutions/index_id_2747.html) |
| Pre-delivery inspection | UVeye, Camcom, Ombrulla (78 checkpoints, 10 cameras, industrial vehicles), Intelli PDI (checklist app) | Drive-through camera arches; damage seg; auto PDI report | [UVeye FVL](https://uveye.com/finishedvehiclelogistics/), [Camcom](https://camcom.ai/automotive-aftermarket-vehicle-inspection), [Ombrulla](https://ombrulla.com/usecases/ai-visual-inspection-pdi-industrial-vehicles) |
| Undercarriage / tyres | UVeye Helios (5 floor cameras), Artemis (tyres), Atlas (arch); GM + Volvo dealers | Semantic segmentation of rust, leaks, texture anomalies | [The Batch](https://www.deeplearning.ai/the-batch/auto-diagnosis), [Unite.AI](https://www.unite.ai/amir-hever-co-founder-ceo-of-uveye-interview-series/) |
| Video multipoint inspection (MPI) | AutoLoop, Kenect, TruVideo, myKaarma | Technician films the issue → sent to customer → approve repair; **AI grades video quality**; Niello fixed-ops director: "I'm not gonna look at 10,000 videos" | [Dealership Guy 2026](https://news.dealershipguy.com/p/how-niello-co-s-fixed-ops-director-employs-ai-to-help-monitor-mpi-videos-2026-04-14), [myKaarma](https://mykaarma.com/news/how-ai-based-technology-helps-technicians-videos-make-the-grade-spur-service-revenue-growth/), [Kenect](https://kenect.com/product/video-multi-point-inspection-ai) |
| Engine bay / leaks | Patents (UV + camera leak localisation vs engine layout), Oxmaint | Leak/stain seg; belt cracks; **no evidence of fluid-level reading from photos** | [USPTO 12480836](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12480836), [Oxmaint](https://oxmaint.com/industries/fleet-management/ai-visual-fluid-leak-detection-for-fleets) |
| Brake pads | Research: improved AlexNet defect detection; wear = worn pixel area / disc area | Lab/production settings only | [IJAME](https://journal.ump.edu.my/ijame/article/view/11712) |
| Showroom | V-Count, FPT Smart Showroom (LPR on arrival → CRM), Assert AI (no faces) | Zone dwell time; plate → CRM | [V-Count](https://v-count.com/industries/car-showrooms/), [FPT](https://www.businesswire.com/news/home/20251209837418/en/FPT-Drives-the-Accelerated-Smart-Showroom) |
| Counterfeit parts | BMW + KURZ SCRIBOS holograms, Brembo QR, Ennoventure | Packaging security features verified by phone; image comparison vs genuine DB (no independent accuracy) | [BMWBlog](https://www.bmwblog.com/?p=504074), [Brembo](https://www.bremboparts.com/america/en/support/car/after-sales-service/recognize-original-products-247245), [Ennoventure](https://ennoventure.com/blogs/how-to-spot-counterfeit-auto-parts/) |
| Step verification | IndustReal (WACV 2024) — procedure step recognition incl. **missing steps**, code + data public; MDPI 2020 missing-action 3D CNN | Detect assembly-state per frame → which steps completed, in which order | [IndustReal](https://github.com/TimSchoonbeek/IndustReal), [arXiv 2310.17323](https://arxiv.org/pdf/2310.17323) |
| VIN tampering | Patents (compare VIN plates dash/door/frame), forensic X-ray / ultrasonic | Image-only is weak vs re-welded plates | [USPTO 10410182](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10410182) |

**Local signal:** BYD Seal 6 buyer in Tashkent, car at service 4 days, parts "coming from China" (kun.uz, 12–13 Mar 2026) — service capacity/parts is a real pain ([kun.uz](https://kun.uz/ru/news/2026/03/13/3-raza-vyshla-iz-stroya-za-10-dney-v-tashkente-kuplennyy-byd-seal-6-okazalsya-brakovannym)). Single anecdote, not a statistic.

## Gaps / idea seeds (not yet developed)
1. **MPI video auditor** — AI checks every technician video: is the claimed problem actually visible (worn pad, leak, cracked belt)? Protects customers from fake upsell and dealers from bad videos. Nobody publishes this check.
2. **Service step verifier** — bay camera confirms each job step happened (e.g. all 5 wheel nuts torqued, oil cap back on) — IndustReal method applied to car service.
3. **Parts photo → catalogue match + counterfeit flag** for the parts counter (embeddings + OCR of stamped numbers + packaging check).
4. **Bay digital twin from existing CCTV** for BYD/Toyota service in Tashkent — measures real capacity (queue, idle bays) before buying more lifts.
