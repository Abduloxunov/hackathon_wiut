# Lead's ideas, version 2 (Davlatyor, Sat 10 Oct ~19:00)

Davlatyor's own description of the ideas he wants, cleaned up by claude-1, with claude-1's notes (✚ = suggested addition, ⚠️ = risk).
**Historical brainstorm, superseded by [CarDoctor — multimodal RAG](FINAL-PICK.md) at 02:20 on Sun 11 Oct.** These descriptions and `ideas/SHORTLIST.md` remain research background; [docs/tasks.md](../docs/tasks.md) defines current build work.

---

## 1. Smart traffic lights (SmartFlow)
Junction camera video → count cars waiting on each road → **suggest** how long each green light should be.
- ✚ Same video pipeline as our **elimination task** (tracking at junctions) → we can also show near-misses (Junction Risk Map) from the same video.
- ⚠️ Only advice, never controls a real light. Jury can only upload a video. Many student projects do traffic lights → our elimination code must be the difference.

## 2. Car damage → cost → the right mechanic ("CarDoctor", working name)
**Story:** a driver photographs the car — after an accident, before buying a used car, or just to check.
1. The app finds **all defects and damage** (dents, scratches, broken lights, cracked glass, tyres).
2. For each defect: **what kind of repair** and **estimated cost**.
3. A **knowledge base of service stations / mechanics**: who fixes this type of problem (body shop, glass, tyres, paint), where, rating → the app **sends the driver to the right place** (map + route).

**Who uses it (three markets, one engine):**
| Market | What they get |
|---|---|
| Used-car buyers | Check a car before buying: hidden damage + repair cost → negotiate price |
| Drivers after an accident | Know the repair cost immediately + where to fix it |
| Logistics / truck fleets | Driver photographs a problem on the road → nearest station that can fix it |

- ✚ **Business model:** service stations pay a fee per customer we send them (marketplace) → clear money flow for the 10% Business criterion.
- ✚ **Satellite/weather layer** (Davlatyor's satellite skill): for an accident/flood claim, check the weather or Sentinel-1 flood map for that date and place.
- ✚ Optional "is this photo real?" check (from TrueClaim) — matters if insurers use the cost.
- ⚠️ Crowded idea (Tractable, many teams). The **mechanic knowledge base + routing** is what makes it ours. Data for stations: dealer service centres (Toyota/BYD Royal Motors), directories (Golden Pages lists 163 car-service companies — check terms), Yandex Maps (check terms).
- ⚠️ Real repair prices: call 3–5 Tashkent workshops for a price list, or label it "sample".
- Jury test: ✅ photograph any car in the parking lot.

## 3. Road defects map + contractor rating ("RoadProof / RoadMap")
**Story:** potholes everywhere; the city repairs every spring, but nobody knows which contractor's work lasts.
1. **Collect:** dashcams in cars + **people send photos** of road defects (we may **pay them** small rewards).
2. **Detect:** potholes, cracks → one event per defect (no duplicates from 20 frames).
3. **Map:** a digital map of all road defects.
4. Three uses:
   - **Repair:** send defects to the companies that rebuild roads.
   - **Contractor rating:** we know **who built/repaired each road and when** → history → **how durable each company's work is** → which contractors are good.
   - **Driver warning:** when a driver approaches a known pothole → *"hole ahead, slow down"*.
- ✚ **Satellites here:** free satellites (Sentinel-2, 10 m) **cannot see potholes**. But they can probably see **when a road was resurfaced** (fresh asphalt is dark, it gets lighter with age) → gives the "when was it built" date for the contractor history *(hypothesis — must test)*.
- ✚ Confirm a pothole only when several cars report it; phone motion sensor feels the bump (from the LinkedIn posts).
- ⚠️ Contractor names per road segment: need city data (open data / hokimiyat) — we may only have it for a demo area.
- Jury test: ✅ photograph any crack; ⚠️ the map needs our own collected data.

## 4. DriveCoach — driver state + driving + context
1. **Driver camera:** eyes (sleeping?), where he looks (distracted?), phone in hand.
2. **Driving motion:** how he drives (harsh braking, swerving) — phone motion sensor.
3. **Context:** GPS (speed, location), **road camera** (car ahead too close?), and the **road defects map from idea 3**.
4. **Combine everything** → one decision: *driving safely / tired / distracted / dangerous right now* → alarm + trip report.
- ✚ Links ideas 3 and 4: a distracted driver approaching a known pothole = higher alert.
- ⚠️ Phone browsers can't use both cameras at once → two devices paired with a code. Many competitors (Nauto, Samsara).
- Jury test: ✅ close your eyes / look away → alarm.

## 5. Satellites (Davlatyor: "maybe road structure and buildings — is it all implemented already?")
Yes — **extracting roads and buildings from satellite images is already done** (OpenStreetMap, Google, Microsoft building footprints). Not original as a product.
Where satellites **add value to our ideas** instead:
- Idea 3: when each road was resurfaced (contractor durability history).
- Idea 2: verify flood / weather damage claims.
- Road weather risk: freeze–thaw, flooding → where new potholes will appear.

## 6. Elimination task again (junction events)
Our elimination code (traffic event detection at junctions, `Abduloxunov/wiut-cv-traffic-events`) can be the **core of idea 1** (and Junction Risk Map). The task explicitly allows "traffic events that continue your elimination task".

## 7. Assembly worker check (factory)
Camera above a worker → does he do every step in the right order, are all parts in place? (Like Drishti, from the CV Product Field Guide.)
- ✚ Automotive fit: car assembly plants in Uzbekistan (UzAuto Motors; BYD's local plant — *verify*), or the **dealer service bay** (did the mechanic do every step, all wheel nuts tightened?).
- ✚ Fun jury demo: a judge assembles a simple kit on the table; the camera says which step is missing.
- ⚠️ Partners are dealers, not factories → frame it as **service-bay step check** for Toyota/BYD.

---

## claude-1's recommendation
| Idea | Jury phone demo | Hard to copy | Business clarity | 8 h build |
|---|---|---|---|---|
| **2. Car damage → cost → mechanic** | ✅ strong | medium (knowledge base + routing helps) | **strong (marketplace fee)** | ✅ |
| **3. Road defects map + contractor rating** | ✅ photo / ⚠️ map | **high (contractor durability idea is rare)** | medium (city is a slow buyer) | ⚠️ map needs data |
| 1. Smart traffic lights | ⚠️ video | high only with elimination code | medium | ⚠️ |
| 4. DriveCoach | ✅ strongest | low–medium | medium | ✅ |
| 7. Assembly / service-step check | ✅ fun | medium | medium | ⚠️ |

**Best single build: Idea 2.** Best "only we have this" story: Idea 3's contractor rating. Ideas 2 and 3 share the same skills (photo → defect detection → map/decision).
