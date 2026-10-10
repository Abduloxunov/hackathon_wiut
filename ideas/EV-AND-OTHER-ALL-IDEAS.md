# EV, infrastructure & other ideas — simple version

The last subdomain from the task (**EV & infrastructure**) + ideas that don't fit the other three files (motorcycles, fleets, parking) + **new ideas Bexruz pushed this evening**.

---

## Part 1 — EV & infrastructure

**Why it matters:** Uzbekistan had **1,399 public chargers** on 1 May 2025 (820 in Tashkent) — 2.5× more than a year before — and plans **4,000 by end of 2026**. BYD sales nearly doubled in Q1 2026. (Sources: [Daryo](https://daryo.uz/en/2025/05/04/uzbekistan-sees-2-5-fold-surge-in-ev-charging-stations-1216442/), [Kun.uz](https://kun.uz/en/news/2026/05/05/uzbekistan-to-expand-ev-charging-network-to-4000-stations-by-end-of-2026), collected by Muhammadjon.)

**The common problem:** most EV ideas need a **fixed camera at a charging station**. The jury can't easily test that with their own phone.

---

### 1. ChargeBay Watch — "Is the charger free, or is someone blocking it?"

**Story:** Jasur drives his BYD to a charger in a mall. A petrol car is parked in the charging spot. Or an EV finished charging an hour ago and its owner is still shopping.

**Our app:**
1. A camera watches the charging spots.
2. For each spot: *free / charging / parked but not plugged in / blocked by a petrol car*.
3. Alert to the operator: *"Spot 3 blocked for 25 min"*. Drivers see free chargers on a map.

**Jury demo:** weak — photograph a parking area, draw the spots, see their state.
**Who pays:** charging operators, malls, dealers with chargers (BYD Royal Motors).
**Hard part:** telling EV from petrol car by its look; seeing if a cable is plugged in.
**Proposed by:** Muhammadjon/claude-2, Davlatyor/claude-1 ("EV Bay Guard" — **without reading plates**, to follow the task rule), Bexruz/codex ("EV Bay Occupancy & Session Review" — adds the charger's own data).

### 2. Charger Fault Triage — "The charger shows an error — what now?"

**Story:** A charger screen shows *"Error E-07"*. The staff member doesn't know what it means and calls support.

**Our app:** photograph the charger screen and its label → the app reads the error code → finds it in the manufacturer manual → creates a support ticket (or *"photo too blurry, retake"*).

**Jury demo:** photo of a charger screen (we'd need a real one or a printed sample).
**Who pays:** charging operators.
**Hard part:** we need real charger screens and their manuals.
**Proposed by:** Bexruz/codex.

### 3. EV battery underbody check (idea seed)
At service intake, photograph **under the BYD** → scratches/dents on the battery pack found and recorded. A real case: BYD said a Tang's motor tore off after hitting something under water (July 2026).
**Hard part:** photos under a car need a ramp or a special camera.
**Proposed by:** Davlatyor/claude-1.

---

## Part 2 — Other areas (not in the task's list, but allowed)

### 4. Daily Fleet Check — taxi/delivery cars (new, claude-1)
**Story:** A taxi park has 100 cars and many drivers. A car comes back scratched — which driver did it?
**Our app:** each driver takes 8 photos at the start and end of the shift → the app shows **only new damage** + who had the car.
**Note:** it is **Handover Guard** (dealer file) sold to taxi/delivery fleets instead of dealers — same engine, one more customer.

### 5. Motorcycles (Ducati is a partner)
- **Rider Gear Review** (Bexruz/codex): video of riders (who agreed) → helmet visible or not → list for the riding instructor.
- **Ducati Chain Check** (claude-1): photo of chain + coin → chain stretch → *replace now / soon*.
- **Rider Line** (claude-1): riding video → lean angle per corner → coaching.
**Problem for all three:** we need a motorcycle (and a rider) for the demo.

### 6. Parking
- Find cars parked illegally (on sidewalks, in bus lanes).
**Problem:** needs reading **number plates** of people who didn't agree → forbidden by the task. Only works for counting/occupancy, which is already common.

---

## Part 3 — New from Bexruz this evening (on his branches, not merged yet)

| Idea | What it does | Same as |
|---|---|---|
| **RoyalScan** | Guided phone photos of a used car → damage report, missing photos, **repair cost estimate** from an approved price list → appraiser decides | Damage Estimate in the vehicle-inspection file (the Tractable-style idea Davlatyor likes) |
| **DriveAlert** | Driver camera → sleepy/distracted warning. **New smart part:** if the camera can't see well (dark, sunglasses, face covered) it says *"monitoring unavailable"* instead of guessing | Driver Fatigue Guard / DriveCoach |
| Vehicle Damage Evidence & Estimate | Same direction as RoyalScan | Damage Estimate |
| PDI Evidence Checklist | Photos of a new car vs its delivery checklist → what needs attention before handover | PDI check (dealer file) |
| Road Hazard Tickets | Road photos/dashcam → non-duplicated road-defect tickets on a map | RoadProof / RoadGuard |
| Parts Order Verification | Picked part vs ordered part | PartsLens (dealer file) |
| EV Bay Occupancy & Session Review | See #1 above | ChargeBay Watch |
| Rider Gear Review | See #5 above | — |

**Good sign:** Bexruz's newest proposals land on the same ideas as the other two agents → the team is converging.

---

## Quick comparison of all four subdomains

| Subdomain | Best idea | Jury phone test | Hard to copy? | Buyer |
|---|---|---|---|---|
| Dealer & service | Handover Guard + Warranty Check | ✅ | medium–high (photo trust checks) | dealer / importer |
| Vehicle inspection | Damage Estimate + TrueClaim checks | ✅ | medium (crowded) | insurer / dealer |
| Road safety | RoadProof + Junction Risk Map | ⚠️ video | **high** (our elimination code) | city (slow) |
| EV & infrastructure | ChargeBay Watch | ❌ needs fixed camera | low–medium | charging operator |

**claude-1's view:** EV is the **weakest** for this hackathon (no phone demo, needs real chargers). The strongest direction remains the **"trust the photo" engine** (dealer + inspection), with road safety as the alternative that uses our elimination code.

**Detailed files:** [ChargeBay Watch](chargebay-watch.md) · [dealer ideas](DEALER-SERVICE-ALL-IDEAS.md) · [vehicle inspection](VEHICLE-INSPECTION-ALL-IDEAS.md) · [road safety](ROAD-SAFETY-ALL-IDEAS.md) · Bexruz's new files: branches `codex/royalscan-idea`, `codex/refined-cv-ideas` (PR #4).
