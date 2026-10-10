# Driver & road safety ideas — simple version

All driver/road-safety ideas from Davlatyor, Muhammadjon and Bexruz, in plain words.
**Driver & road safety** = cameras that make driving and roads safer: the driver, the road surface, junctions, the city.

**Why it matters in Uzbekistan:** 2,203 people died on the roads in 2024. In early 2026, speeding caused 32.9% of crashes and ignoring traffic signals 22.4% (sources: [AKIpress](https://akipress.com/news:838901:2,203_people_die_in_traffic_accidents_in_Uzbekistan_in_2024), [Kun.uz](https://kun.uz/en/news/2026/01/15/traffic-deaths-remain-high-across-uzbekistan-despite-prevention-efforts), collected by Muhammadjon).

**Our advantage here:** our **elimination task was traffic event detection** at junctions. The task says we may reuse that code ("traffic events that continue your elimination task"). Other teams don't have it.

**Our problem here:** most road ideas need **video from a street camera**. The jury can't easily test them with their own phone — they can only upload a video.

---

## The 4 best ideas

---

### 1. RoadProof — "Was the pothole really fixed?"

**Story:** Every spring Tashkent repairs about 816,000 m² of roads. People complain that contractors patch badly, and nobody checks. The city even asks residents to send photos of bad repairs (Xalq Nazorati) — but a person looks at every photo by hand.

**Our app:**
1. Someone photographs a road → the app finds **potholes and cracks** → makes a repair ticket.
2. After the repair, someone photographs **the same spot again**.
3. The app lines up the two photos → *"fixed" / "partly fixed" / "not fixed"*.

**Jury demo:** photograph any crack in the parking lot → ticket. Before/after pair → verdict.
**Who pays:** city road department (hokimiyat), road contractors.
**Hard part:** wet roads and shadows look like cracks; the public dataset (RDD2022) is mostly dry daytime roads.
**Proposed by:** Muhammadjon/claude-2.
**Why strong:** "find the pothole" is common; **checking the repair** is the real problem and few do it.

---

### 2. Junction Risk Map — "Which crossing is dangerous before someone dies?"

**Story:** A crossing in Chilonzor has many near-crashes every day, but the city only learns after a real crash.

**Our app:**
1. Upload a video from a junction camera.
2. The app follows every car and person (our elimination code).
3. It measures **near-misses**: two road users reaching the same spot less than ~1–2 seconds apart.
4. Result: a **map of dangerous spots** + short video clips of each near-miss.

**Jury demo:** upload any junction video (or film the street from a window) → near-miss clips.
**Who pays:** city traffic department, road-safety consultants, insurers.
**Hard part:** the jury can't make a junction on their phone; measuring real distances needs the camera set up once.
**Proposed by:** Davlatyor/claude-1 (Junction Risk Map), Bexruz/codex (Crossing Conflict Review).
**Why strong:** **hardest for other teams to copy** — it's built on our own elimination work. Real companies do this (VivaCity), so it is a real need.

---

### 3. DriveCoach — "Are you driving safely right now?" (Davlatyor's brainstorm)

**Story:** A taxi driver looks at his phone for 2 seconds. On an empty road — not dangerous. With a car braking in front — very dangerous.

**Our app:**
1. One camera looks at the **driver** (eyes closed? looking away? phone in hand?).
2. Another camera looks at the **road** (car in front too close?).
3. The app judges danger **together**: looking away *while* the car ahead is close = alarm.
4. Trip report for the taxi/delivery company.

**Jury demo:** a judge looks at the laptop camera, closes their eyes or looks away → instant alarm. Very easy.
**Who pays:** taxi and delivery fleets, insurers, driving schools.
**Hard part:** a phone browser can't use both cameras at once → we pair two devices with a code. Many competitors exist (Nauto, Samsara); a 2013 university app did the same idea.
**Proposed by:** Davlatyor + claude-1.

---

### 4. RoadGuard — "Turn hours of dashcam video into a short list of road problems"

**Story:** A delivery company has dashcams in 50 cars. Nobody watches the videos.

**Our app:**
1. Upload a dashcam video.
2. The app finds road damage frame by frame.
3. The same pothole seen in 20 frames becomes **one event** (not 20 alarms).
4. Report: list of problems with time, photo and priority.

**Borrowed from the LinkedIn posts:** confirm a pothole only when **several cars** report it; use the phone's **motion sensor** to feel the bump the camera sees; after **rain**, warn about flooded roads.
**Who pays:** fleets, then the city.
**Proposed by:** Muhammadjon/claude-2.

> #1 and #4 use **the same detector** (photo vs video).

---

## Other ideas

### 5. SmartFlow AI — smarter traffic lights
Junction video → count queues on each road → **suggest** how long each green light should be. Tested in a traffic simulator. Only advice — never controls a real light.
**Problem:** lots of simulation work, little computer vision; many student projects do this.
**Proposed by:** Muhammadjon/claude-2.

### 6. Driver Fatigue Guard — sleepy-driver alarm
Laptop/phone camera watches the eyes → closed too long → alarm. Runs in the browser, no video leaves the device.
**Problem:** the **most common hackathon demo** — low innovation. Good as part of DriveCoach.
**Proposed by:** Muhammadjon/claude-2.

### 7. Bus-Stop Access Monitor
Camera at a bus stop → cars parked in the bus area → the bus can't reach the kerb → ticket for the operator.
**Proposed by:** Bexruz/codex.

### 8. Rider Line — Ducati motorcycle coaching
Helmet/phone video → how far the rider leans in each corner → coaching.
**Problem:** needs a motorcycle and riding video.
**Proposed by:** Davlatyor/claude-1.

---

## Weaker ideas (and why)

| Idea | What it does | Why weaker |
|---|---|---|
| Crosswalk Visibility Audit | Photos of a crossing → faded paint, hidden sign | Narrow; existing products (Blyncsy) |
| Work-Zone Audit | Roadworks photos → missing cones/signs | Needs real roadworks to test |
| Road Debris / Blocked Sidewalk | Video → objects on the road or sidewalk | Hard to test safely |
| Traffic sign reading | Camera reads speed signs | Every new car already does it |

(All weaker ideas from Bexruz/codex except the last.)

---

## In one picture

```
                        ROAD SAFETY
      ┌──────────────────┬──────────────────┬───────────────────┐
   THE ROAD           THE JUNCTION        THE DRIVER          THE CITY
   RoadProof (photo)  Junction Risk Map   DriveCoach          SmartFlow (lights)
   RoadGuard (video)  (our elimination    Fatigue Guard       Bus-Stop Monitor
                       code ★)            Rider Line (Ducati)
   jury: ✅ photo      jury: ⚠️ video      jury: ✅ live cam    jury: ⚠️ video
```

**Recommendation (claude-1):**
- If we choose road safety: **RoadProof with repair checking** (easy jury demo + real Tashkent problem), and show **Junction Risk Map** as the "hard to copy" part built on our elimination code.
- **DriveCoach** has the best live demo but many competitors.
- Compared with the dealer ideas: road safety has a stronger "only we have this" story (elimination code), but a weaker phone demo and a slower buyer (the city).

---

## Things to know
- **Faces and plates:** street videos contain people and cars → blur faces/plates in anything we show (task rule).
- **Data:** RDD2022 road-damage dataset — check the licence (CC BY-SA vs CC BY). Our own Tashkent photos = our test set.
- **Never claim** "prevents accidents" or "X% fewer jams" without our own measurement.

**Detailed files:** [RoadProof](roadproof.md) · [RoadGuard video](roadguard-video.md) · [SmartFlow](smartflow.md) · [Driver Fatigue Guard](driver-fatigue-guard.md) · [DriveCoach](drive-coach.md) · [claude-1 research](research-landscape-claude1.md) (Junction Risk Map §C, Rider Line §G) · Bexruz's files on branches `codex/cv-shortlist` and `codex/idea-research` (PRs #2, #3).
