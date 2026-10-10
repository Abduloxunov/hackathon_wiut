---
name: TrueClaim
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 14:45
direction: vehicle inspection (insurance claim / service intake)
mode: startup (B2B for motor insurers). Alternative: partner product at Toyota Royal Motors body shop / service intake
---

# TrueClaim: is this claim photo real, new and of this car?

**One line:** Car-damage photo in → authenticity verdict (screen/print recapture, reused or near-duplicate photo, edited or metadata mismatch, quality) + damage map → "accept / ask for a live retake / send to the fraud team", for insurers and body shops.

## Problem and user
- **User:** claims handler at an insurer (OSAGO/KASKO), service intake at a dealer body shop. **Payer:** the insurer.
- **Evidence the problem is real** (sources in `_research-notes-claude2.md`):
  - Humans spot AI-manipulated damage photos at about 50% accuracy, no better than chance (Milliman, Dec 2025).
  - Verisk found 1,967 duplicates in 768k claim images; one photo was reused in 44 claims.
  - Photos of a screen showing a damaged car look real to the eye (there are patents on recapture detection).
  - **Local:** the OSAGO insured sum doubles (40 → 80 M soums) on 1 Jan 2026, so bigger payouts mean a bigger fraud incentive (our inference, to verify with an insurer).
- Most teams will build "detect the dent". Almost nobody will build "is this photo evidence trustworthy?" That gives us **innovation (25%)**.

## What the product does
- **Input:** 1–N photos of a damaged car (upload or phone camera on the web page).
- **Pipeline (a system, not one model):**
  1. **Quality gate:** blur (variance of Laplacian), exposure, resolution, car present (detector).
  2. **Recapture detector:** photo of a screen or print? Moiré / frequency (FFT) features + small CNN; **trained on our own recaptures** (we photograph laptop and phone screens and prints with our phones = our dataset, our moat).
  3. **Duplicate / reuse search:** perceptual hash (pHash) + CLIP embedding nearest-neighbour against the claim-history index → "this photo, or a crop or edit of it, was already submitted in claim #…".
  4. **Metadata consistency:** EXIF present? capture time vs claim time, camera model, editing-software tag, GPS (if given) vs claimed place. Missing EXIF is only a weak signal, never proof.
  5. **Damage localisation:** detector for dent / scratch / crack / glass / lamp (trained on CC BY 4.0 Roboflow sets; CarDD only as a research benchmark, since it is non-commercial).
  6. **Decision engine:** transparent rules → risk score + reasons → **accept / live retake / manual review**. Never "fraud" as a final verdict: a human decides.
- **Output:** a report page: verdict, reasons (each check green, amber or red), damage boxes, a "retake live" QR link.
- **Live jury test (strong demo):** (a) the jury photographs any car → passes; (b) the jury photographs **our laptop screen** showing a damaged car → **flagged as recapture**; (c) the jury uploads the same photo cropped or brightened → **flagged as a duplicate of claim #…**. All three run live on the jury's own input.

## Tech
- **Models:** OpenCV, a small CNN (MobileNetV3 / EfficientNet-B0, Apache-2.0 torchvision weights) fine-tuned for recapture; open_clip ViT-B/32 (MIT) for embeddings; `imagehash` for pHash; detector for damage (RF-DETR, Apache-2.0, or YOLO11, AGPL); FAISS or a numpy index.
- **Data we can get today:**
  - recapture set: we shoot about 300–600 pairs ourselves (real car vs the same photo shown on 3–4 different screens or prints, different angles and phones); labelled by construction;
  - duplicates: synthetic edits (crop, resize, JPEG, brightness, mirror, screenshot) of CC BY images; ground truth by construction;
  - damage: Roboflow CC BY 4.0 car-damage sets.
- **Inference:** server CPU. pHash + quality take milliseconds, CLIP + CNN about 100–300 ms per image on CPU (to be measured).
- **Night / rain / local cars:** the recapture and duplicate checks don't depend on the car model. Damage detection is weaker at night; the quality gate asks for a retake. We report metrics per group only where test data exists.

## Why hard to copy
- **Our own recapture dataset** (collected on site with local phones and screens) and the measured false-alarm rate.
- **Layered pipeline** with a decision engine and failure analysis, not a single LLM call.
- **Network effect:** each insurer's claim-image index grows; duplicate detection gets stronger with every claim (and across insurers if they share hashes, privacy-safe since only hashes and embeddings are shared).

## Business
- **Payer:** insurers (OSAGO/KASKO lines), later leasing companies, car-sharing, dealer body shops.
- **Price idea (hypothesis):** per checked claim, e.g. $0.20–1 (a public comparable: VerifyAI $0.008 per photo verification, a competitor-written page). Value = avoided fraudulent payouts + faster honest claims (no physical inspection). To validate with one insurer.
- **Cost per check:** compute (CPU ms) + storage of hashes and embeddings, measured in the prototype.

## Can we build it in ~8 h?
- **MVP scope:** web upload → quality gate → recapture CNN → pHash/CLIP duplicate search over a seeded index → EXIF checks → damage detector → report. A seeded "claim history" index of about 200 CC BY images.
- **Biggest risk:** the recapture CNN generalising to unseen screens and phones. Mitigation: collect varied data in the first 2 h (all 3 team phones, 3+ screens, prints); report accuracy per held-out device.
- **Second risk:** detecting AI-generated images is unreliable for everyone. We **exclude it from the MVP** and say so (honest limitation), or show it only as an experimental signal.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
