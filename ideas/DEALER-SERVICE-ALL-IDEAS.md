# All ideas — Dealer & service operations (team digest)

Compiled by claude-1 for Davlatyor, Sat 10 Oct 17:40, after pulling everything.
Sources: `main` + unmerged branches `codex/cv-shortlist` (PR #3), `codex/idea-research` (PR #2), `claude2/strategy`.
Agents: **claude-1** = Davlatyor · **claude-2** = Muhammadjon · **codex** = Bexruz.

## 0. How to read this
- Ideas are grouped by **area of the dealership** (where in the car's life the photo is taken).
- Several ideas are the **same idea proposed independently** by different agents. They are merged into one card; each author is credited.
- ✅ / ⚠️ / ❌ = can the jury test it live on their own phone (task requirement).
- Nothing here is selected yet. The lead decides.

## 1. Overview — 9 areas, 14 proposals
| # | Area | Idea (merged name) | Proposed by | Jury live test | claude-1 score* |
|---|---|---|---|---|---|
| 1 | Check-in / check-out | **Handover Guard** | claude-1 (Handover Diff), codex (Service Handover Guard), claude-2 (LensCheck as first stage) | ✅ | 7.8 |
| 2 | Warranty desk | **Warranty Evidence** | claude-1 (WarrantyProof), codex (Warranty Evidence Review), claude-2 (TrueClaim core) | ✅ | 8.0 |
| 3 | Insurance / body-shop intake | **TrueClaim** | claude-2 (TrueClaim), claude-1 (ClaimProof) | ✅ | (insurance variant of #2) |
| 4 | Repair quality control | **Repair Evidence Review** | codex | ✅ | ~7 |
| 5 | Parts counter / warehouse | **Parts Verification / PartsLens** | claude-2 (PartsLens), codex (Parts Verification) | ✅ if physical parts | 6.3 |
| 6 | Trade-in | **TradeIn PreCheck** | claude-2 (+ windshield chip idea), claude-1 (Repaint Radar) | ✅ | 6.9 |
| 7 | Tyres at service intake | **TyreCheck** | claude-2 (TyreCheck), claude-1 (TyreAge) | ✅ | 7.0 |
| 8 | Photo-set quality | **LensCheck** | claude-2 | ✅ | fallback only |
| 9 | Workshop bays | **Service-Bay Tracker** | claude-2, (claude-1 "Just Walk Out for the bay") | ❌ | 5.8 |
| — | Technician videos | MPI Video Auditor | claude-1 | ⚠️ | 6.9 |
| — | Pre-delivery inspection | PDI anomaly check | claude-1 | ✅ (new cars rarely at hand) | 5.5 |
| — | Ducati | Chain Check | claude-1 | ⚠️ needs a bike | 5.9 |

\* claude-1's estimate with jury weights (Tech 25, Innov 25, Impact 25, Demo 15, Business 10). Bexruz/codex deliberately gives **no numeric scores** (qualitative only).

---

## 2. The ideas

### 2.1 Handover Guard — check-in / check-out ✅
**Authors:** claude-1 "Handover Diff" ([§B](research-landscape-claude1.md)) · codex "Service Handover Guard" ([file on PR #3](https://github.com/Abduloxunov/mdb-vision-finals/blob/codex/cv-shortlist/ideas/service-handover-codex.md)) · claude-2 LensCheck as the capture stage.
**One line:** guided photos at drop-off and at pick-up → same panels lined up → only *new* visible changes shown → retake or human review before handing the car back.
**User / payer:** service-reception advisor; dealer aftersales (Royal Motors).
**Pipeline:** quality gate → zone/panel localisation → match the same view → alignment (LightGlue) with confidence → local change analysis → coverage rules → evidence report. Low alignment confidence = "retake", never a damage score (codex rule).
**Jury test:** photograph a car, put tape/sticker on a panel, photograph again → only the new mark flagged; change angle/light → should NOT flag.
**Evidence:** DealerWare docs say AI damage diff is "not in this initial release" (codex correctly notes: one supplier's scope, not proof of a global gap).
**Risks:** reflections, dirt, lighting, viewpoint → false changes. **No matched real car pairs yet** (codex: blocker).
**Boundaries (codex):** no blame, no repair cost, "no visible change" ≠ all-clear.

### 2.2 Warranty Evidence — importer's warranty desk ✅
**Authors:** claude-1 "WarrantyProof" ([deep dive §C](subdomain-dealer-service-deep-dive.md)) · codex "Warranty Evidence Review" ([PR #3](https://github.com/Abduloxunov/mdb-vision-finals/blob/codex/cv-shortlist/ideas/warranty-evidence-codex.md)) · claude-2 TrueClaim core.
**One line:** part photos + claim record + past submissions → reused image? identifier/VIN/odometer conflict? missing views? → request more evidence or manual review.
**User / payer:** warranty-review officer; Toyota Central Asia FZE (warranty 3 y / 100,000 km) or BYD Royal Motors warranty dept.
**Pipeline:** quality gate → part localisation → **PDQ/pHash + DINOv2 embedding search** over claim history → local correspondence check → **OCR** of part number / VIN / odometer vs record → completeness rules → report. claude-1 adds: recapture/AI-image signal; weather + Sentinel-1 flood check for water-damage claims.
**Jury test:** upload a photo; upload a cropped/rotated/recompressed copy → "possible reuse of claim #…"; photo of a laptop screen → flagged; wrong part number → conflict.
**Evidence:** reused turbo/rim photos across 29 claims, $350k (Truepic case); 10–20% of warranty spend = industry estimate, no primary study.
**Codex cautions:** similarity ≠ fraud; missing EXIF ≠ manipulation; **exclude universal AI-generated detection from the MVP**; seeded claim history must be declared synthetic.
**Risks:** no real claims → synthetic history; false matches between genuinely similar parts.

### 2.3 TrueClaim — insurer / body-shop intake ✅ (claude-2's top pick)
**Authors:** claude-2 ([trueclaim.md](trueclaim.md)) · claude-1 ClaimProof.
**One line:** car-damage photo → recapture check + reuse search + EXIF consistency + quality + damage map → accept / live retake / fraud team.
**Payer:** insurers (OSAGO/KASKO); dealer body shop as partner variant.
**Strong demo (3 live tests):** real car passes; **photo of our laptop screen → recapture**; cropped/brightened copy → duplicate of claim #….
**Own data = moat:** 300–600 recapture pairs shot on site with team phones + screens/prints.
**Local hook (claude-2, to verify):** OSAGO insured sum doubles 40 → 80 M soums from 1 Jan 2026 → bigger fraud incentive.
**Note:** same engine as 2.2 — warranty desk vs insurer is a go-to-market choice.

### 2.4 Repair Evidence Review — after a bodywork repair ✅
**Author:** codex ([PR #2](https://github.com/Abduloxunov/mdb-vision-finals/blob/codex/idea-research/ideas/repair-evidence-codex.md)).
**One line:** requested repairs checklist + before/after panel photos → evidence coverage + visible-change flags → reviewer closes the case.
**Payer:** BYD Royal Motors aftersales quality control. **Bexruz found the real site: [byd-rm.uz/service](https://byd-rm.uz/service).** Prior art: Tractable × Warta repair-network oversight.
**Note:** same alignment/change engine as 2.1, opposite question ("did the requested change happen?" vs "did an unwanted change happen?").

### 2.5 Parts Verification / PartsLens — parts counter ✅ (needs physical parts)
**Authors:** claude-2 PartsLens ([parts-lens.md](parts-lens.md)) · codex Parts Verification ([PR #3](https://github.com/Abduloxunov/mdb-vision-finals/blob/codex/cv-shortlist/ideas/parts-verification-codex.md)).
**One line:** photo of a part (+ label close-up) → top-3 catalogue matches + OCR'd number vs requested item → match / conflict / unknown → worker confirms.
**Pipeline:** background removal → DINOv2 embeddings + FAISS → OCR → size re-rank with a reference marker (A4/ArUco) → open-set rejection.
**Data:** we photograph 20–40 real parts ourselves; don't scrape catalogue images (copyright).
**Blocker (codex):** no physical parts or trusted records yet. nyris benchmark top-1 = 32.5% → always top-3.

### 2.6 TradeIn PreCheck — remote trade-in pre-assessment ✅
**Authors:** claude-2 ([tradein-precheck.md](tradein-precheck.md)) · claude-1 Repaint Radar.
**One line:** customer's 8 guided photos → completeness + damage map + odometer OCR + dealer rules → "eligible, book inspection" / "not eligible because…". No price estimate.
**Evidence:** Cabinet Resolution PKM-535 (22 Aug 2025) formalises trade-in via dealers; ~240k used-car sales in H1 2026.
**Extensions:** windshield chip/crack detection (claude-2); panel colour mismatch = repaint (claude-1).
**Note:** shares ~70% of the pipeline with TrueClaim and LensCheck.

### 2.7 TyreCheck — tyres at service intake ✅
**Authors:** claude-2 ([tyrecheck.md](tyrecheck.md)) · claude-1 TyreAge.
**One line:** tread + sidewall photos → wear vs wear bar, **age from DOT code (OCR)**, cracks → replace now / soon / OK → service order.
**Demo:** walk to any car in the WIUT parking lot. Data: ~150–300 own photos in the first 2 h.
**Context data (claude-1):** heat/UV exposure → rubber ageing in Tashkent summers.
**Risks:** DOT text is faint black-on-black (flash at an angle helps); patents on phone tread-depth (FTO check before commercial).

### 2.8 LensCheck — photo-set quality & completeness ✅ (fallback)
**Author:** claude-2 ([lenscheck.md](lenscheck.md)).
Blur/exposure/glare/duplicates + viewpoint classifier (CLIP zero-shot + linear probe) → "retake these 3 shots". Weak alone; **the first stage of 2.1 / 2.2 / 2.3 / 2.6** and the safe fallback.

### 2.9 Service-Bay Tracker ❌ (weak jury test)
**Authors:** claude-2 ([service-bay-tracker.md](service-bay-tracker.md)) · claude-1 "Just Walk Out for the bay" (lead likes it).
CCTV → bay state timeline (empty / car / on lift / idle) → utilisation + idle alerts. Real competitors: SKAIVISION, PitCrew. **Jury cannot test it on their phone; no licensed workshop footage.**

### 2.10 Smaller claude-1 seeds
- **MPI Video Auditor:** is the recommended repair visible in the technician video (pads, tread, leaks)? Pad thickness from photos has no published accuracy → risky.
- **PDI anomaly check:** anomalib PatchCore on new-car panels. Competes with UVeye arches.
- **Ducati Chain Check:** chain stretch vs coin scale. Unoccupied niche; needs a motorcycle.

---

## 3. What the three agents agree on
1. **The strongest cluster is "photo evidence that decides money"**: Handover (2.1), Warranty (2.2), TrueClaim (2.3), Repair Evidence (2.4). All three agents proposed versions of it independently.
2. **They share one engine:** quality gate → view/part localisation → alignment or retrieval → change / reuse / identifier checks → rules → evidence report + human review.
3. **Honest limits everyone wrote down:** no invented numbers; similarity ≠ fraud; human makes the final call; AI-generated-image detection is experimental, not a verdict.
4. **The common blocker is data:** no real matched car pairs, claims or parts → we must **collect our own on site** (team cars, screens, a few parts) and declare synthetic data.

## 4. Important facts found by teammates
- **BYD Royal Motors** has a real service site: [byd-rm.uz/service](https://byd-rm.uz/service) (codex).
- **CarDD's original licence requires permission** → don't use it in the product; HITL car parts+damage is CC0 (codex).
- **OSAGO insured sum 40 → 80 M soums from 1 Jan 2026** (claude-2; verify).
- **PKM-535 (22 Aug 2025)** formalises trade-in through dealers (claude-2).
- **Licences:** prefer Apache 2.0 (RF-DETR, SAM 2, DINOv2, LightGlue + GlueFactory SuperPoint, anomalib, PaddleOCR); Ultralytics YOLO = AGPL-3.0 (claude-1, claude-2).
- **RoadGuard poster numbers are AI-made, not measured** — never in the deck (claude-2).

## 5. Pending in git (lead action)
- PR #1 `codex/local-setup`, PR #2 `codex/idea-research`, PR #3 `codex/cv-shortlist` — open, not merged.
- Branch `claude2/strategy` — strategy (RoadProof) + proposed `POST /api/analyze` contract — not merged.

## 6. Other subdomains (for completeness, one line each)
Road safety: RoadProof / RoadGuard video (claude-2), Junction Risk Map (claude-1), Crossing Conflict Review + Bus-Stop Access Monitor + Crosswalk/Workzone audits (codex), DriveCoach (Davlatyor + claude-1), Driver Fatigue Guard (claude-2), Rider Line (claude-1). EV: ChargeBay Watch (claude-2), EV Bay Guard (claude-1), Charger Triage (codex).
