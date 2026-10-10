---
name: TyreCheck
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 15:00
direction: dealer/service ops + road safety
mode: partner product: Toyota Royal Motors / BYD Royal Motors, Service reception (service intake); changes the walk-around at car acceptance
---

# TyreCheck: tyre photo → wear, age, cracks → "replace now / soon / OK"

**One line:** Phone photos of the tread and sidewall in → tread-wear level (vs wear bar), **tyre age from the DOT date code (OCR)**, sidewall cracks → safety verdict + service offer, at service intake or for fleets.

## Problem and user
- **User:** service advisor at car acceptance; fleet / taxi owner; driver. **Payer:** dealer service (upsell plus safety), fleet operator.
- **Evidence:**
  - NHTSA estimated about 400 deaths per year in the US from tyre failures of all types, 1994–2004, with tyre ageing among the causes ([CA bill analysis](https://www.leginfo.ca.gov/pub/09-10/bill/asm/ab_0451-0500/ab_496_cfa_20090502_072803_asm_floor.html)).
  - Tyres age faster in hot climates ([NHTSA via theaiatrust](https://theaiatrust.com/tire-safety-tracking-evidence/)). **Tashkent summers are hot**, so local relevance is our inference.
  - Aged tyres can look fine to the eye; the age is hidden in the DOT code (last 4 digits = week + year) ([WLOX](https://www.wlox.com/story/27416647/cracking-a-potentially-life-saving-hidden-code-on-car-tires)).
  - Common guidance: replace at about 6 years.
- Local Uzbek tyre-crash statistics: **not found yet (unverified)**.

## What the product does
- **Input:** 2 photos per tyre: tread close-up + sidewall with the DOT code.
- **Output:** per tyre: wear class (OK / near wear bar / at wear bar), age in years from DOT, crack flag, overall verdict, and the action "book tyre replacement" (for the dealer = a service order).
- **Live jury test:** strong. We walk to any car in the WIUT parking lot (or the jury's car), photograph the tyre and get a live result.

## Tech
- **Pipeline:**
  1. quality gate (blur and glare; embossed black-on-black text needs side light, so the UI guides the user);
  2. tyre and region detection (tread vs sidewall);
  3. tread-wear classifier (EfficientNet/MobileNet fine-tuned; wear-bar relative, **no absolute mm** without a reference object);
  4. **DOT code localisation + OCR** (PaddleOCR, Apache-2.0, plus regex `\d{4}` week/year validation: week 01–53, year ≤ now);
  5. crack detector;
  6. rules → verdict.
- **Data:** our own photos of parking-lot tyres (no personal data); public tread data is scarce (a [HF demo](https://uncodespecial-tire-tread-depth.hf.space/) trained on 730 labelled tyres, licence unknown; [Ajou paper](https://aurora.ajou.ac.kr/handle/2018.oak/38263) built its own). Collecting it ourselves is the moat.
- **Inference:** server CPU.
- **Night / rain:** the phone flash at an angle helps the DOT OCR. Wet tyres cause glare, so the quality gate rejects them.

## Why hard to copy
- An own labelled dataset of local tyres (brands sold in Uzbekistan); DOT-OCR on embossed rubber is genuinely hard (glare, curvature), which makes it real engineering, not an API call.
- Integration into the dealer service order and the fleet maintenance log.

## Business
- Dealer: each "replace now" turns into a tyre sale (hypothesis: a set of tyres is a meaningful ticket). Fleets: per-vehicle subscription. Prices to be validated.
- **Caveat:** patents exist on phone tread-depth measurement (US 10295333, US 12296622), so we need an FTO check before going commercial.

## Can we build it in ~8 h?
- Wear class + DOT OCR + verdict: yes, with ~150–300 own photos collected in the first 2 h from the parking lot.
- **Biggest risk:** DOT OCR accuracy on embossed rubber. Mitigation: guided capture (frame overlay + flash), a manual-confirm fallback field.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
