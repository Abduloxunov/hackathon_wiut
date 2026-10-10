# All team ideas on one page: problem → idea → how we solve it

Compiled by Muhammadjon + claude-2, Sat 10 Oct, from `ideas/`, claude-1's four digests and Bexruz's codex branches (some not merged yet).
**Who:** 🟦 Muhammadjon (claude-2) · 🟥 Davlatyor (claude-1, lead) · 🟩 Bexruz (codex). The final choice is the lead's.

Every idea follows the same rule: **no invented numbers**, a person makes the final decision, and faces/plates of non-consenting people are blurred.

---

## A. "Can we trust this photo?": inspection, dealer, insurance
*All three of us arrived here independently. One engine (photo quality → which car part → compare with another photo or with all past photos → read text → decide with reasons) powers A1–A5.*

### A1. TrueClaim / ClaimProof: is this claim photo real? (🟦 Muhammadjon, 🟥 Davlatyor)
- **Problem:** drivers send fake damage photos to insurers: taken from the internet, of a screen, reused from an old claim, or AI-edited. Humans spot AI-edited damage photos only about 50% of the time; one photo was found in 44 claims (Milliman, Verisk). The OSAGO payout limit doubles in 2026.
- **Idea:** a trust check for every claim photo + damage map → *accept / retake live / send to fraud team*.
- **How:** quality gate → screen-recapture detector (trained on our own photos of screens) → duplicate search (perceptual hash + CLIP embeddings over past claims) → EXIF/date check → damage detector → rule engine with visible reasons. Davlatyor's extra: check the claim story against weather or satellite records ("no hail fell there that week").
- **Demo:** a real car passes; a photo of our laptop screen is flagged; the same photo cropped shows "already used in claim #12".

### A2. Warranty Check: is this warranty claim honest? (🟦🟥🟩 all three)
- **Problem:** dealers ask Toyota/BYD to pay for warranty repairs with photos; sometimes the same photo is reused or shows the wrong part.
- **Idea:** the same engine as A1, for the importer's warranty department.
- **How:** reuse search + screen check + **OCR of part number, VIN and odometer** compared with the claim form → ✅ fine / ⚠️ more photos / 🔍 human review.

### A3. Handover Guard / Daily Fleet Check: who scratched the car? (🟥 Davlatyor, 🟩 Bexruz)
- **Problem:** customer and service centre (or taxi park and driver) argue about whether a scratch is new. Nobody can prove it.
- **Idea:** photos at drop-off and at pick-up → show **only new damage**.
- **How:** guided 8-photo walkaround → match each pair by panel (anchor parts: wheels, lights, handles) → align → change detection → filter out reflections and light changes → "new scratch on rear-left door".
- **Demo:** photograph a car, stick a small sticker on it, photograph again, and the app finds only the sticker.

### A4. Repair Check: was the repair really done? (🟩 Bexruz)
- **Problem:** the customer paid for a dent repair, and the manager can't verify every job.
- **Idea:** before/after photo of the repaired spot → "changed / not changed" → manager closes the job.
- **How:** the same alignment + comparison as A3, limited to the area named in the work order.

### A5. Damage Estimate / RoyalScan: how much will the repair cost? (🟥 Davlatyor, 🟩 Bexruz)
- **Problem:** after a crash, people visit three workshops and get three different prices.
- **Idea:** phone photos → which parts are damaged and how badly → repair or replace → estimate (Tractable-style).
- **How:** car-part segmentation + damage segmentation → overlap = "dent on front bumper" → severity → price from a **real** local price list (or a clearly marked sample). 3D view is only a stretch goal.

### A6. TradeIn PreCheck: is my old car eligible for trade-in? (🟦 Muhammadjon)
- **Problem:** customers drive to the dealer only to hear "we don't accept this car". Trade-in via dealers became official in 2025 (PKM-535).
- **Idea:** 8 photos from home → eligibility verdict before the visit.
- **How:** photo completeness → damage + windshield chips → odometer OCR from the dashboard photo → dealer rules (age, damage) → "book inspection" or "not eligible because…". No price guess.

### A7. Repaint Radar: was this car in an accident before? (🟥 Davlatyor)
- **Problem:** a used car looks perfect, but a door was repainted after a crash.
- **Idea:** find repainted panels and hidden dents from photos.
- **How:** colour difference between neighbouring panels; a striped pattern shown on a phone/laptop screen and filmed on the car body, where bent reflected stripes mean a dent or filler.

### A8. PDI Checklist: is the new car ready for delivery? (🟩 Bexruz)
- **Problem:** small defects on new cars are found by the customer, not before handover.
- **Idea:** photos of the new car vs the delivery checklist → what needs attention.
- **How:** guided photos per checklist item → quality + damage check → checklist with evidence photos.

### A9. LensCheck: are these inspection photos good enough? (🟦 Muhammadjon)
- **Problem:** blurry, dark or missing photos cause repeat inspections and disputes.
- **Idea:** check each photo set before it is sent → "retake photo 2 and 6".
- **How:** blur (Laplacian), exposure, glare, duplicates, angle classifier (front/rear/sides/corners). **Step 1 of every idea in group A** and the safe backup plan.

---

## B. Service centre and parts

### B1. TyreCheck / TyreAge: are these tyres safe? (🟦 Muhammadjon, 🟥 Davlatyor)
- **Problem:** old tyres can look fine but are risky (common advice: replace at about 6 years; heat speeds ageing). The age is hidden in the DOT code on the sidewall.
- **Idea:** photograph a tyre → *replace now / soon / OK*.
- **How:** guided capture (side light for embossed text) → read DOT week/year by OCR → tread wear vs wear bar (classifier) → crack check → verdict + service offer.
- **Demo:** walk to any car in the parking lot.

### B2. PartsLens / Parts Order Verification: which part is this? (🟦 Muhammadjon, 🟩 Bexruz)
- **Problem:** loose parts without a box or number; the wrong part gets picked for an order.
- **Idea:** photo of a part → top-3 catalogue matches; or "picked part = ordered part?".
- **How:** background removal → image embeddings (DINOv2/CLIP) → nearest-neighbour search in our own photo catalogue → size check with a reference marker → a human confirms.

### B3. Service-Bay Tracker: which repair bay is idle? (🟦 Muhammadjon)
- **Problem:** bays stand idle while cars wait for parts; nobody has objective numbers.
- **Idea:** workshop camera → bay state timeline + idle alerts.
- **How:** car/person detection + tracking + drawn bay zones + a state machine (empty / car in / on lift / idle). Weak for the jury test: no workshop video.

### B4. Ducati Chain Check (🟥 Davlatyor)
- **Problem:** a stretched motorcycle chain is a safety and service issue.
- **Idea:** photo of the chain next to a coin → stretch → *replace now / soon*.
- **How:** detect the coin (known size) for scale → measure the link pitch → compare with the spec. Needs a motorcycle for the demo.

---

## C. Roads and driver safety
*Our edge here: the elimination-stage traffic code. Weak spot: the jury mostly has to give us a video, not a photo.*

### C1. RoadProof / Road Hazard Tickets: was the pothole really fixed? (🟦 Muhammadjon, 🟩 Bexruz)
- **Problem:** Tashkent repairs ~816,000 m² of road each spring; residents complain about poor patching; photo complaints (Xalq Nazorati) are checked by hand.
- **Idea:** road photo → repair ticket; after the repair, a photo of the same spot → *fixed / partly / not fixed*.
- **How:** quality gate → road-damage detector (RDD2022 classes) → priority rules → ticket; for pairs: feature matching + homography to align the photos → compare the damage in the same area.

### C2. RoadGuard (video): hours of dashcam video → a short list of road problems (🟦 Muhammadjon)
- **Problem:** fleets have dashcams, but nobody watches the footage.
- **Idea:** upload a video → list of unique road-damage events with time, photo and priority.
- **How:** frames → detector → tracking / IoU + time matching so **one pothole = one event** → evidence frame + CSV/JSON report. We measure duplicates and wrong merges ourselves.

### C3. Junction Risk Map / Crossing Conflicts: which crossing is dangerous before someone dies? (🟥 Davlatyor, 🟩 Bexruz)
- **Problem:** the city learns about a dangerous junction only after a real crash.
- **Idea:** junction video → near-misses → map of dangerous spots + clips.
- **How:** our elimination-stage detection + tracking → bird's-eye-view projection → time-to-collision / post-encroachment time (two road users at the same spot < ~1–2 s apart) → heatmap. **Hardest for others to copy.**

### C4. DriveCoach: are you driving safely right now? (🟥 Davlatyor)
- **Problem:** looking away for 2 s is harmless on an empty road and dangerous behind a braking car.
- **Idea:** driver camera + road camera → risk judged **together** → alert + trip score for the fleet.
- **How:** browser MediaPipe (eye closure, PERCLOS, head pose, phone) + road YOLO + distance/headway estimate; two devices paired by a room code (browsers can't open two cameras); explainable fusion rules.

### C5. Driver Fatigue Guard / DriveAlert: sleepy or distracted driver (🟦 Muhammadjon, 🟩 Bexruz)
- **Problem:** tired or distracted drivers.
- **Idea:** camera on the driver → alarm when eyes close, yawning or phone use.
- **How:** in-browser face landmarks → EAR/PERCLOS/yawn + phone detector + per-driver calibration. Bexruz's extra: if the camera can't see (dark, sunglasses), it says "monitoring unavailable" instead of guessing. Common idea → low innovation alone.

### C6. SmartFlow: smarter traffic-light timing (🟦 Muhammadjon)
- **Problem:** fixed-time lights give green to empty roads while queues grow elsewhere.
- **Idea:** junction video → queues per direction → **recommended** green times (advice only).
- **How:** detection + tracking → queue length / waiting time → rule-based controller with safety limits → compare fixed vs adaptive in the SUMO simulator.

### C7. Bus-Stop Access Monitor (🟩 Bexruz)
- **Problem:** cars parked at bus stops block buses from reaching the kerb.
- **Idea:** stop camera → "bus bay blocked" events for the operator.
- **How:** car/bus detection in a drawn bus-bay zone + time rules. No plate reading.

### C8. Crosswalk Audit / Work-Zone Audit (🟩 Bexruz)
- **Problem:** faded crossings, hidden signs, roadworks without cones/signs.
- **Idea:** photos → list of safety defects for the city/contractor.
- **How:** detection of markings, signs and cones + a checklist of rules per site.

### C9. Rider Line / Rider Gear Review: Ducati riders (🟥 Davlatyor, 🟩 Bexruz)
- **Problem:** rider skill and safety gear.
- **Idea:** riding video → lean angle per corner, with coaching; or "helmet visible?" for instructors.
- **How:** horizon-tilt estimation per frame → lean angle; helmet detector on riders who agreed. Needs a motorcycle for the demo.

---

## D. Electric vehicles and infrastructure
*Weakest group for this hackathon: the jury has no charging-station camera to test with.*

### D1. ChargeBay Watch / EV Bay Guard / EV Bay Occupancy: is the charger free? (🟦🟥🟩 all three)
- **Problem:** charging spots are blocked by petrol cars or by EVs that finished charging long ago. There are 1,399 public chargers (820 in Tashkent), with 4,000 planned by end of 2026.
- **Idea:** camera → each spot: free / charging / parked not plugged / blocked → alert.
- **How:** car detection in drawn bay zones + time rules; EV vs petrol by car model/shape (no plate reading); plug/cable check; Bexruz adds the charger's own session data.

### D2. Charger Fault Triage (🟩 Bexruz)
- **Problem:** staff don't know what a charger error code means.
- **Idea:** photo of the charger screen → error explained → support ticket.
- **How:** OCR of the error code and label → look-up in the manufacturer manual → ticket, or "photo too blurry, retake".

### D3. EV battery underbody check (🟥 Davlatyor)
- **Problem:** hidden damage to the battery pack under the car.
- **Idea:** photos of the underbody at service intake → scratches/dents on the battery recorded.
- **How:** damage detection on underbody photos. Needs a ramp or a special camera.

---

## Summary
| Group | Best idea | Jury can test with a phone? | Hard to copy? |
|---|---|---|---|
| A. Trust the photo | TrueClaim + Warranty Check + Handover Guard (one engine) | ✅ | medium–high |
| B. Service & parts | TyreCheck | ✅ | medium |
| C. Roads & drivers | RoadProof + Junction Risk Map | ⚠️ mostly video | high (elimination code) |
| D. EV | ChargeBay Watch | ❌ | low–medium |

Detailed files: the per-idea files in `ideas/`, [dealer](DEALER-SERVICE-ALL-IDEAS.md), [inspection](VEHICLE-INSPECTION-ALL-IDEAS.md), [road safety](ROAD-SAFETY-ALL-IDEAS.md), [EV & other](EV-AND-OTHER-ALL-IDEAS.md) digests (claude-1), [claude-2 research](_research-notes-claude2.md).
