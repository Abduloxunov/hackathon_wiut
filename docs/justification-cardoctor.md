# Is the car-damage idea (CarDoctor: photo → damage → cost → right workshop) valid? — claude-1, Sun 11 Oct 01:20

Same check as `docs/justification.md` (DriveCoach). Survey numbers are perceptions, not measured overcharging.

## Problem
| Fact | Source |
|---|---|
| Uzbekistan 2024: 9,364 crashes → each one needs a damage check and a repair | [Kun.uz](https://kun.uz/en/news/2025/02/01/one-third-of-accidents-in-2024-involved-cargo-and-passenger-transport) |
| Used-car market: ~240,000 used passenger cars sold in H1 2026 | [Kun.uz Aug 2026](https://kun.uz/en/news/2026/08/05/uzbekistans-car-market-rebounds-in-june-as-ev-sales-surge) |
| Used-car fraud is real enough that parliament passed fines for **odometer tampering** (lower house Jan 2026, Senate May 2026; final signature not confirmed) | [Kun.uz Jan 2026](https://kun.uz/en/news/2026/01/29/parliament-passes-law-imposing-fines-for-odometer-tampering-in-used-cars), [May 2026](https://kun.uz/en/news/2026/05/19/senate-approves-administrative-penalties-for-odometer-tampering-in-used-car-market) |
| Insurance market grew 37.8% in 2025 (13.46 trn soums); compulsory motor cover limit doubled 40 → 80 M soums from 1 Jan 2026 | [UzDaily](https://www.uzdaily.uz/en/uzbekistans-insurance-market-grows-378-in-2025/), [Times CA](https://timesca.com/from-reform-to-roadblocks-the-uneven-evolution-of-motor-insurance-in-central-asia/) |
| Repair-price distrust (US): 2/3 of drivers don't trust repair shops; top reasons unnecessary services (76%) and overcharging (73%) | [AAA via VehicleServicePros](https://www.vehicleservicepros.com/industry-news/press-release/20845948/AAA.com/autorepair) |
| UK: 45% have no idea what common repairs should cost (ClickMechanic survey — vendor) | [DJS Research](https://djsresearch.co.uk/insights/motorists-sceptical-of-repair-costs-survey-finds-02331) |
| Uzbekistan: repair shops mostly advertise informally (OLX); new booking apps (AvtoMall May 2026, Avten Mar 2026) have **no damage AI** | see `ideas/research-winners-github-claude1.md` |

## Who benefits
Used-car buyers (avoid hidden damage, negotiate), drivers after an accident (know a fair range, find the right shop), truck/taxi fleets (quick triage on the road), workshops (get matched customers — they pay per lead), insurers (faster first estimate).

## The weak spot — be honest in the pitch
- **Photo-only estimates are contested.** Body-shop owners say automated estimates miss hidden damage (e.g. a misaligned frame); one 2019 summary says Tractable fully estimated only ~25% of cases without a human ([The Batch](https://www.deeplearning.ai/the-batch/wreck-recognition)).
- Insurers "lost faith in touchless estimating" and moved to **triage** and reviewing estimates; CCC said use was still "a tiny fraction of the potential" (2022) ([RDN](https://www.repairerdrivennews.com/2022/11/28/use-of-its-ai-powered-estimating-system-still-at-a-tiny-fraction-of-the-potential-ccc-tells-investors/)).
- No independent accuracy benchmark found; no Uzbek KASKO penetration data found.
- Needs local repair prices + workshop data we don't have yet; needs trained damage models (CarDD licence needs permission).

→ Position as **"first look + fair range + right workshop"**, never "exact price". The workshop confirms in person.

## Verdict
**Valid problem, real beneficiaries — but weaker than DriveCoach** on (a) proof the AI part works well enough, and (b) what we can build alone by 13:00. Best as DriveCoach's "next module" for fleets.

| | DriveCoach | CarDoctor |
|---|---|---|
| Problem evidence | strong (deaths, crash-risk studies, EU mandate) | medium (fraud law, distrust surveys — mostly US/UK) |
| Proof the tech helps | independent studies (VTTI, SWOV) | contested (photo estimates miss hidden damage) |
| Data we need tonight | none (pretrained models) | damage training data, prices, workshops |
| Live demo | ✅✅ | ✅ |
