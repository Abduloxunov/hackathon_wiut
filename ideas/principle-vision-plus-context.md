---
name: Principle — vision + context data → decision
added_by: Davlatyor (from his pheromone-trap work) + claude-1
date: Sat 10 Oct 16:55
direction: all
---

# Principle: don't stop at computer vision — fuse context data

**Origin (Davlatyor's work):** camera counts insects in pheromone traps → combined with weather, a knowledge base of insect life stages (egg → larva → moth) → decision/action (spray now / wait).
**Why it matters for the jury:** "Is it a system and not a call to someone else's model?" and "Name your advantage: data, model, pipeline, integration or domain knowledge" (docs/task.md). Extra data sources make the idea hard to copy in a weekend.

| Trap system | Car / road version |
|---|---|
| CV counts insects | CV measures damage, wear, tread, objects |
| Weather | Temperature, UV, rain/hail/flood history |
| Insect life-stage model | Wear / ageing models (brakes, tyres, rubber) from km, heat, road type |
| Satellite | Sentinel-1 radar flood maps (works through clouds), Sentinel-2, land-surface temperature |
| Decision: spray / wait | Approve claim / replace now / repair this road first |

## Fusion ideas (ranked)
1. **Claim check with weather + satellite** (extends TrueClaim / ClaimProof / WarrantyProof): photo authenticity + damage type, then "did this hail/flood actually happen there on that date?" (weather archive, Sentinel-1 flood map). Mismatch = fraud signal. Uses Davlatyor's satellite experience.
2. **Tyre / rubber ageing for a hot climate**: DOT date OCR + crack detection + tread depth + local heat/UV exposure → remaining safe months (a wear model, like the insect stage model).
3. **Road repair priority**: dashcam pothole detection + freeze–thaw cycles from weather + traffic volume → ranked repair list for the city.

## Open data (check licences before use)
- Copernicus Sentinel-1 / Sentinel-2 — free and open (Copernicus licence).
- Weather archives: Open-Meteo, ERA5 (Copernicus Climate Data Store) — verify terms.
