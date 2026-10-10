# Focus subdomain: Dealer & service operations

**Research snapshot from the idea phase.** The selected product is now [CarDoctor](../ideas/FINAL-PICK.md), serving used-car buyers, fleets and drivers with workshop matching. The wider subdomain ideas below are background research, not current assignments.

Chosen by the lead (Davlatyor + claude-1), Sat 10 Oct. Research: `ideas/subdomain-dealer-service-claude1.md`. CV tasks numbered as in `docs/cv-toolbox.md`.

## What a dealership is
The official seller of a brand (task partners: Toyota Royal Motors, BYD Royal Motors, Ducati). It is several businesses in one: new-car sales, used cars / trade-in, **service (main profit)**, parts, body shop, warranty (repairs paid back by the importer/manufacturer).

## Life of a car at the dealer
Arrival from factory → **PDI** (pre-delivery inspection) → stock yard → sale (+ **trade-in**) → delivery → years of service: **check-in** walkaround → **multipoint inspection** (technician photos/videos) → customer approves → work in a **bay** with **parts** → **check-out** → if under warranty, **warranty claim** to the importer.

## Map: areas × problem × our idea
| Area | Pain | Who pays | Our idea | CV tasks | Context data (non-CV) | Jury can test live on own phone? | Existing players |
|---|---|---|---|---|---|---|---|
| **Check-in / check-out** | "You scratched my car" disputes | Dealer service dept | **Handover Diff**: two walkarounds aligned per panel → only new damage | 3, 4, 10, (12) | Job timeline, who handled the car | ✅ photograph a car twice | myKaarma (manual tags), DealerWare (AI diff "not in this release") |
| **Multipoint inspection videos** | Customers distrust upsell; managers can't watch thousands of videos | Dealer / customer trust | **MPI Video Auditor**: is the recommended repair visible? | 2, 3, 7, 11, 14 | Service manual limits (pad mm, tread mm), mileage | ⚠️ needs part close-ups | TruVideo, myKaarma (grade video quality only) |
| **Warranty** | Reused photos, wrong parts, padded labour; est. 10–20% of warranty spend (industry estimate, no primary study) | **Importer's warranty dept** | **WarrantyProof**: reused? real? right part? VIN/odometer match? | 6, 8, 13, 3 | Claim history, parts catalogue, VIN decode, weather/flood records | ✅ upload a "claim" photo, try a recaptured screen | Truepic, ServiceCPQ, Tavant |
| **Parts counter** | Wrong part ordered, counterfeits | Parts dept | **PartsLens**: photo → top-3 OEM numbers (+ packaging check) | 8, 6 | Catalogue, VIN fitment | ✅ photograph any part | nyris, team neusta |
| **Service bays** | Idle bays, long waits | Service manager | **Service-bay tracker / "Just Walk Out" for the bay** | 2, 5, 11 | Job cards, bookings | ❌ needs CCTV | SKAIVISION, PitCrew |
| **PDI / stock yard** | Factory/transport damage found late | Dealer, logistics | PDI damage + anomaly check | 3, 9 | Delivery docs | ✅ | UVeye, Camcom |
| **Trade-in** | Overpaying for hidden damage/repaint | Used-car dept | TradeIn PreCheck / Repaint Radar | 3, 6, 10 | Market prices, history | ✅ | autobiz Noa, VerifyAI |
| **Tyres (service upsell)** | Old/worn tyres missed | Service dept | TyreCheck: wear + DOT age + cracks | 3, 6, 7 | Heat/UV exposure, mileage | ✅ photograph any tyre | UVeye Artemis (hardware), Anyline |
| **Ducati (motorcycles)** | Chain/sprocket wear checked by hand | Ducati service | Chain Check: stretch + tooth wear vs coin | 3, 4 | Service bulletin limits | ✅ if a bike is nearby | none found |

## How to choose
Score each on: jury live test ✅, uses rare tasks (8, 10, 13), context data available, buildable in ~8 h, clear payer (Partner mode: name the unit + the process it changes).
