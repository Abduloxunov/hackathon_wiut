# Final pick — Davlatyor (Sun 11 Oct, 00:30)

## ✅ FINAL DECISION (02:20): build **CarDoctor — multimodal (visual + text) RAG**. Three modes: used-car buying check · fleet triage · breakdown/accident. Scored vs jury criteria ≈7.5 vs pothole map ≈7.1 vs DriveCoach (common). DriveCoach + road map = next modules.
Architecture: photos → image embeddings (CLIP/DINOv2) + zero-shot detection → vector DB #1 (visual symptom library: warning lights, smoke colours, leak colours, damage types) · words → multilingual text embeddings → vector DB #2 (repair knowledge + known issues of popular Uzbek models) · LLM answers ONLY from retrieved items with citations · workshop KB + map. Vision must visibly do the work (show matched symptom + similarity before LLM text).

## (superseded) DECISION (00:40): build **DriveCoach**. CarDoctor = "next module" slide.
Reason: Davlatyor is the only developer; DriveCoach runs on pretrained models (MediaPipe face landmarks, COCO car detector) with **no training data**; strongest live demo; the lead's favourite. CarDoctor needs 3–4 trained models + LLM key + workshop database — not feasible solo by 13:00.


Two ideas chosen by the lead. Both serve the **same customer: drivers and fleets (taxi, delivery, trucks)**.
Code freeze **Sun 11 Oct 13:00**.

---

## A. CarDoctor — "what's wrong with my car, and where do I fix it?"
The driver (or fleet) **shows and tells**:
- **Photos / video** of the car: body damage, **exhaust smoke**, **leak under the car**, **dashboard warning lights**.
- **Words** (typed or spoken): *"the engine makes a knocking sound"*, *"I can't speed up"*, *"white smoke from the exhaust"*.

The system:
1. **Computer vision** reads what it can SEE:
   - body damage → part + severity (segmentation);
   - **exhaust smoke colour** → white / blue / black (coolant / oil / fuel-mixture problems — standard mechanic knowledge, to cite);
   - **puddle colour under the car** → green/orange (coolant), brown/black (engine oil), red (transmission/power-steering), clear (water from A/C — normal);
   - **dashboard warning lights** → which light (research: YOLO on 18 light classes, F1 0.91 on 15 — University at Buffalo);
   - (optional) a short video of the engine bay.
2. **LLM** turns the driver's words + the CV findings into **likely causes** — constrained by our **knowledge base** (symptom → cause → urgency → repair type). The LLM never invents; it picks from the knowledge base and explains.
3. **Decision:** urgency (*stop driving now / fix this week / can wait*), rough cost range, and **the right workshop** (body shop, engine, electrics, tyres, glass…) from our **workshop knowledge base** → map + route.

**Why not "one prompt behind a UI" (jury rule):** our own CV models (damage, smoke colour, puddle colour, warning lights) + a symptom knowledge base + workshop matching. The LLM is only the conversation layer.
**Business:** workshops pay per customer sent; fleets pay per vehicle per month.
**Jury demo:** ✅ photograph a car / a printed dashboard light / a coloured liquid on paper; type "white smoke and it overheats" → diagnosis + workshop.

## B. DriveCoach — "is this driver driving safely right now?"
Combines many signals, not only sleepiness:
- **Driver camera:** eyes closed (PERCLOS), looking away, head pose, phone in hand, yawning.
- **Road camera:** car ahead too close (headway), lane drift.
- **Phone sensors:** GPS speed, harsh braking / swerving (accelerometer).
- **Context:** known road dangers (potholes map — future), time of day, trip length.
→ **one decision in context**: looking away *while* the car ahead is close = critical; same glance on an empty road = low.
→ live alarm + trip report + driver score for the fleet.

**Jury demo:** ✅ judge looks away / closes eyes → alarm; the alarm becomes critical only when the road video shows a close car.
**Known limit:** phone browsers can't open both cameras at once → laptop camera (driver) + phone (road) paired with a code.

---

## How they fit together — one product for fleets
```
            FLEET COPILOT (working name)
   ┌──────────────────────┬──────────────────────────┐
   │ WHILE DRIVING         │ WHEN THE CAR HAS A PROBLEM│
   │ DriveCoach            │ CarDoctor                 │
   │ driver + road + GPS   │ photos + words → cause    │
   │ → alarm, trip score   │ → urgency, cost, workshop │
   └──────────────────────┴──────────────────────────┘
            one fleet dashboard · one customer
```

## Split (superseded — see docs/tasks.md: Davlatyor is the only developer)
| Who | Area |
|---|---|
| Davlatyor + claude-1 | Architecture, DriveCoach fusion logic (rules), integration, pitch |
| Muhammadjon + claude-2 | CarDoctor CV: damage seg, smoke colour, puddle colour, warning lights |
| Bexruz + codex | Web app + deploy (public https), workshop + symptom knowledge base, LLM layer |

## Risks
- Two modules in ~12 h is tight → **if behind at 10:30 Sun, cut to the stronger one** and show the other as "next step".
- LLM: paid API cost must be in the cost model; no API keys in git.
- Faces: only our own team on camera (consent). No plates.
