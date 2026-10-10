# Dealer & service ideas — simple version

All ideas from Davlatyor, Muhammadjon and Bexruz in one place, in plain words.
(The detailed version with sources is in the separate files linked at the bottom.)

---

## The 4 best ideas

All three of us came up with these independently. They all answer one question:
**"Can we trust this photo? Money depends on it."**

---

### 1. Handover Guard — "Who scratched my car?"

**Story:** Aziz leaves his BYD at the service centre. When he picks it up, he sees a scratch and says: *"You did this!"* The service centre says: *"It was already there."* Nobody can prove anything.

**Our app:**
1. When Aziz drops off the car, the worker takes 8 photos with the app (front, back, sides, corners).
2. When Aziz picks it up, the worker takes the same 8 photos again.
3. The app compares each pair and shows **only what is new**: *"New scratch on the rear left door."*

**Jury demo:** the jury photographs a car → we put a small sticker on it → they photograph again → the app finds only the sticker.

**Who pays:** the dealer's service department.
**Hard part:** shiny paint, reflections and different light can look like "new damage".
**Proposed by:** Davlatyor/claude-1, Bexruz/codex.

---

### 2. Warranty Check — "Is this warranty claim honest?"

**Story:** A dealer asks Toyota/BYD to pay for a broken part under warranty and sends a photo. Sometimes the same old photo is sent again and again for different cars, or the photo shows the wrong part.

**Our app:**
1. The warranty officer uploads the claim photos.
2. The app checks:
   - **Was this photo used before?** (even if cropped or rotated)
   - **Is it a photo of a screen?** (someone photographed another picture)
   - **Do the part number, VIN and km reading match the claim?** (reads text from the photo)
3. Result: ✅ looks fine / ⚠️ ask for more photos / 🔍 send to a person to check.

**Jury demo:** upload a photo → upload the same photo cropped → the app says *"already used in claim #12"*. Photograph our laptop screen → *"photo of a screen"*.

**Who pays:** the importer's warranty department (Toyota Central Asia, BYD Royal Motors).
**Hard part:** we have no real claims — we make a test set ourselves and say so.
**Proposed by:** all three.

---

### 3. TrueClaim — the same check, for insurance

**Story:** After an accident, a driver sends photos to the insurance company. Some photos are fake: taken from the internet, from a screen, or reused from an old claim.

**Our app:** the same checks as #2 + it marks the damage on the car → *accept / take a new photo now / send to the fraud team*.

**Jury demo:** same as #2 — real car passes, screen photo and copied photo are caught.

**Who pays:** insurance companies (OSAGO, KASKO).
**Proposed by:** Muhammadjon/claude-2 (his top pick), Davlatyor/claude-1.

> #2 and #3 are **the same product** sold to two different customers.

---

### 4. Repair Check — "Was the repair really done?"

**Story:** The customer paid to fix a dent. Was it fixed?

**Our app:** photo before repair + photo after repair → the app checks the requested spot really changed → manager closes the job.

**Who pays:** BYD Royal Motors service quality team (their real service site: byd-rm.uz/service).
**Proposed by:** Bexruz/codex.

> #1 and #4 are **the same engine** (compare two photos of the same panel).

---

## Other good ideas

### 5. TyreCheck — "Are these tyres safe?"
Photograph a tyre → the app reads the **production date** printed on the side (tyres older than ~6 years are risky, even if they look fine) + checks wear and cracks → *replace now / soon / OK*.
**Demo:** walk to any car in the parking lot. **Who pays:** service centre (sells tyres), taxi fleets.
**Proposed by:** Muhammadjon/claude-2, Davlatyor/claude-1.

### 6. TradeIn PreCheck — "Can I trade in my old car?"
The customer sends 8 photos from home → the app checks damage, reads the km on the dashboard, applies the dealer's rules → *"Yes, come for inspection"* or *"No, because…"*. Saves wasted trips.
**Who pays:** the dealer's sales department. **Proposed by:** Muhammadjon/claude-2.

### 7. PartsLens — "Which part is this?"
Photograph a spare part → the app shows the 3 most similar parts from the catalogue and reads the number on it → the worker confirms.
**Problem:** for the demo we need real spare parts on the table.
**Proposed by:** Muhammadjon/claude-2, Bexruz/codex.

### 8. LensCheck — "Are these photos good enough?"
Checks that inspection photos are sharp, not dark, and cover all sides → *"retake photo 3 and 5"*.
Too simple alone, but it is **step 1 of ideas 1–4 and 6**. Our safe backup plan.
**Proposed by:** Muhammadjon/claude-2.

---

## Weaker ideas (and why)

| Idea | What it does | Why weaker |
|---|---|---|
| Service-Bay Tracker | Workshop cameras show which repair bay is busy or idle | The jury can't test it with their phone; we have no workshop video |
| Technician Video Check | Checks the mechanic's video really shows the problem | Hard to measure brake pads from a video |
| New-car inspection | Finds defects on new cars before delivery | No new cars nearby to demo |
| Ducati Chain Check | Measures motorcycle chain wear from a photo | Needs a motorcycle |

---

## In one picture

```
                 ONE ENGINE
   ┌───────────────────────────────────────┐
   │ 1. Is the photo good?  (LensCheck)    │
   │ 2. Which car part is it?              │
   │ 3. Compare with another photo         │
   │    - same car, before/after  → #1, #4 │
   │    - all old claims          → #2, #3 │
   │ 4. Read text: VIN, km, part number    │
   │ 5. Decide + show the reason           │
   └───────────────────────────────────────┘
        │            │            │
   Handover     Warranty     Insurance
   (dealer)    (importer)    (insurer)
```

**Recommendation (claude-1):** build this one engine and pitch **Handover Guard + Warranty Check**. Add TyreCheck only if time is left.

---

## Things to know
- None of us has real data yet → on day 1 we take our own photos (team cars, a laptop screen, stickers) and say clearly it is our own test set.
- Never invent numbers in the deck — only what we measured.
- A person always makes the final decision; the app only gives evidence.
- Bexruz's 3 pull requests and Muhammadjon's strategy branch are waiting for Davlatyor to merge.

**Detailed files:** [deep dive](subdomain-dealer-service-deep-dive.md) · [domain map](../docs/domain-dealer-service.md) · [TrueClaim](trueclaim.md) · [TyreCheck](tyrecheck.md) · [TradeIn PreCheck](tradein-precheck.md) · [PartsLens](parts-lens.md) · [LensCheck](lenscheck.md) · Bexruz's files are on branch `codex/cv-shortlist` (PR #3).
