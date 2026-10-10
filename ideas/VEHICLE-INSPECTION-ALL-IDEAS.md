# Vehicle inspection ideas — simple version

All vehicle-inspection ideas from Davlatyor, Muhammadjon and Bexruz, in plain words.
**Vehicle inspection** = looking at a car (photos/video) to find damage or defects: after an accident, when buying/selling a used car, when returning a rental car.

> ⚠️ This is the **most crowded** subdomain. Many teams will build "AI finds the dent". To win, our idea needs something extra that others won't have.

---

## The 4 best ideas

---

### 1. Damage Estimate — "How much will this repair cost?" (Davlatyor likes this — Tractable style)

**Story:** Dilnoza hits a pole. The front bumper and headlight are broken. She wants to know: *how much will it cost, and should I repair or replace?* Today she drives to 3 workshops and gets 3 different prices.

**Our app:**
1. She takes 4–8 photos of the car with her phone.
2. The app finds **which parts** are damaged (bumper, headlight, door…) and **how badly** (scratch, dent, crack, broken).
3. For each part: **repair or replace** + price from a local price list → total estimate.
4. Extra (if time): a **3D view** of the car with the damage marked on it.

**Jury demo:** the jury photographs any car with a scratch or dent → gets an estimate on their phone.

**Who pays:** insurance companies (faster claims), body shops, dealers (trade-in).
**Hard parts:**
- Many teams will build this → we need an extra (see #2 and the combination at the end).
- Real Tashkent repair prices — we need a price list (call 2–3 body shops, or say clearly it is a sample).
- 3D from a phone is research-level → only a stretch goal.

**Proposed by:** Davlatyor (liked Tractable), claude-1 (methods: parts + damage masks), **Bexruz/codex: RoyalScan + Vehicle Damage Evidence & Estimate Review** (his #1 pick — guided photos, only uses an approved price list, appraiser confirms).
**Real product:** Tractable — photos → repair estimate in minutes (company claim).

---

### 2. TrueClaim — "Is this damage photo real?"

**Story:** A driver sends accident photos to the insurer. Some cheat: they send a photo **from the internet**, a photo **of a screen**, an **old photo** already used in another claim, or an **AI-edited** photo. In 2026 insurers in the UK reported more fake photos made with AI tools.

**Our app:**
1. The insurer gets the photos.
2. The app checks: **photo of a screen?** · **used before?** (even if cropped) · **date/camera info makes sense?** · **damage visible?**
3. Result: ✅ accept / 📸 take a new photo now / 🔍 send to the fraud team.

**+ Davlatyor's satellite idea:** if the claim says *"hail on 5 June in Samarkand"* or *"flood damage"*, the app checks **weather records and satellite flood maps** for that date and place. *"No hail fell there that week"* = warning.

**Jury demo:** real car → passes. Photo of our laptop screen → caught. Same photo cropped → *"already used in claim #12"*.

**Who pays:** insurance companies (OSAGO, KASKO).
**Proposed by:** Muhammadjon/claude-2 (his top pick), Davlatyor/claude-1 (ClaimProof + satellite check).
**Why strong:** none of the 17 real products we studied checks if the photo itself is real → open space.

---

### 3. TradeIn PreCheck — "Is my old car worth bringing in?"

**Story:** Rustam wants to swap his old Cobalt for a new BYD. He drives to the dealer, waits an hour, and hears *"we don't accept this car"*.

**Our app:**
1. He sends 8 photos from home (front, back, sides, dashboard, tyres).
2. The app checks: all photos there? damage? reads the **km on the dashboard**, finds **windshield chips/cracks**.
3. Dealer rules decide → *"Yes, book an inspection"* or *"No, because…"*.

**Jury demo:** photograph any car + its dashboard.
**Who pays:** the dealer's sales/trade-in department (Toyota, BYD).
**Fact:** a 2025 government resolution (PKM-535) made trade-in through dealers official; ~240,000 used cars were sold in the first half of 2026.
**Proposed by:** Muhammadjon/claude-2.

---

### 4. Repaint Radar — "Was this car in an accident before?"

**Story:** A used car looks perfect. But the left door was repainted after a crash — the seller doesn't say.

**Our app:**
1. Photos of all sides.
2. The app compares the **colour of neighbouring panels** — a repainted door is slightly different.
3. Creative extra: show a **striped pattern** on a laptop/phone screen, film its reflection on the car — **bent stripes = hidden dent or filler**.

**Who pays:** used-car buyers, dealers (trade-in).
**Hard part:** lighting changes colour; we need a few cars where we *know* a panel was repainted.
**Proposed by:** Davlatyor/claude-1.

---

## Other ideas

### 5. Rental / leasing return check
Same as Handover Guard (dealer file): photos when the car is given out and when it comes back → **only new damage** shown. For car rental, car-sharing and leasing companies.

### 6. Windshield check
Photo of the windshield → chip or crack found → *"repair now (cheap) before it spreads (expensive)"*. Clear, small, easy to photograph. Part of TradeIn PreCheck (Muhammadjon).

### 7. LensCheck — "Are these photos good enough?"
Checks photos are sharp, bright and cover every side → *"retake photo 2 and 6"*. Too simple alone, but **step 1 of every idea above**. Safe backup.

---

## Weaker ideas (and why)

| Idea | Why weaker |
|---|---|
| Plain "AI finds the dent" | Every team will do it; Bexruz's research also ranks generic inspection low |
| Full 3D scan of the car | Research-level, not reliable in 8 hours |
| Underbody / EV battery check | Needs photos under the car (ramp or special cameras) |

---

## In one picture

```
 Phone photos of a car
        │
 1. Good photos?            (LensCheck)
 2. Real photo?             (screen? used before? edited?)      ← few teams do this
 3. Story matches weather?  (hail / flood records, satellite)   ← nobody else has this
 4. What is damaged?        (part + type of damage)             ← everyone does this
 5. How much does it cost?  (repair or replace × price list)
        │
 Accept / retake / send to a person + estimate
```

**Recommendation (claude-1):** combine **#1 Damage Estimate** (what Davlatyor likes, easy to understand) with **#2 TrueClaim checks** (what makes us different). Other teams stop at step 4; we add steps 2, 3 and 5.

This is the **same engine** as the best dealer ideas (Handover Guard, Warranty Check), so we can show both stories with one build.

---

## Things to know
- **Data:** HITL car parts + damage dataset is **free to use (CC0)**. CarDD is **not** free for products (needs permission). We take our own photos on site.
- **Prices:** no invented repair prices — use a real list or say it is a sample.
- A person makes the final decision; the app gives evidence and an estimate.

**Detailed files:** [TrueClaim](trueclaim.md) · [TradeIn PreCheck](tradein-precheck.md) · [LensCheck](lenscheck.md) · [claude-1 research](research-landscape-claude1.md) (ClaimProof §A, Repaint Radar §F) · [vision + context principle](principle-vision-plus-context.md) · [dealer ideas](DEALER-SERVICE-ALL-IDEAS.md)
