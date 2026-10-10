---
name: TradeIn PreCheck
added_by: Muhammadjon + claude-2
date: Sat 10 Oct 14:45
direction: dealer/service ops (trade-in, used-vehicle intake)
mode: partner product: Toyota Royal Motors or BYD Royal Motors, Sales / Trade-in unit; changes the trade-in pre-assessment process
---

# TradeIn PreCheck: remote trade-in pre-assessment from customer photos

**One line:** A customer sends 8 guided photos from home → angle completeness + damage map + odometer reading (OCR) + eligibility rules → "eligible for trade-in, book inspection" or "not eligible because …", before the customer drives to the dealer.

## Problem and user
- **User:** trade-in manager at the dealer; the customer who wants to swap their old car for a new Toyota or BYD. **Payer:** the dealer.
- **Evidence:**
  - Cabinet Resolution PKM-535 (22 Aug 2025) formalises trade-in and trade-up through dealers, with technical identification of the vehicle.
  - Dealers set conditions such as foreign car ≤ 7 years and no serious damage (one source, unverified).
  - The Central Bank links falling used-car prices to growing demand for new cars (sources in `_research-notes-claude2.md`).
- **Pain (hypothesis, to confirm with a dealer):** wasted visits by ineligible cars; slow manual pre-check over WhatsApp/Telegram photos.

## What the product does
- **Input:** guided photo set (front, rear, sides, 4 corners, dashboard with odometer, tyres).
- **Output:** pre-check card: completeness, damage list with boxes and panel, odometer value, eligibility verdict by the dealer's rules, "book inspection" button. **No price estimate:** we have no reliable market data, and the strategy doc warns against it.
- **Live jury test:** the jury photographs any car in the parking lot plus its dashboard.

## Tech
- LensCheck stage (quality + viewpoint) → damage detector (CC BY 4.0 Roboflow sets) → odometer OCR (PaddleOCR, Apache-2.0, on the cluster crop) → rules engine (dealer-configurable YAML) → card.
- **Inference:** server CPU.
- **Night / rain:** photos are usually taken in daylight; the quality gate rejects dark shots.

## Why hard to copy
- Dealer-specific rules + integration into the dealer's trade-in workflow; a local dataset of Uzbek-market cars (Chevrolet Cobalt, Gentra, Nexia, Damas, BYD Song).

## Business
- Per-dealer SaaS (hypothesis $100–300 per site per month). Value = fewer wasted visits, faster trade-in funnel, more new-car sales.

## Can we build it in ~8 h?
- MVP feasible if the damage detector works; the OCR on varied dashboards is a risk.
- **Overlap:** shares 70% of the pipeline with TrueClaim and LensCheck. One core engine, three go-to-market stories.

## Comments
<!-- other agents: `- <agent ID>: comment` -->
- claude-2: variant from Muhammadjon's AI master plan, "Toyota Trade-In Clean-Glass & Body Inspector": adds **windshield chip/crack detection** and a repair-cost matrix. The glass part is a good extension (a clear, photographable defect). The cost matrix needs a real Tashkent price list, and the plan's metrics are invented (see `_research-notes-claude2.md`, last section).
