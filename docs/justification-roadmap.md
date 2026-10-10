# Is the pothole map + driver warning (+ contractor rating) idea valid? — claude-1, Sun 11 Oct 01:40

## Problem
| Fact | Source |
|---|---|
| Government (Feb 2022): **25% of accidents caused by poor road conditions and disorganised infrastructure** (2021 data, >10,000 accidents) | [gov.uz](https://old.gov.uz/en/news/view/33554) |
| President's office: "one of the main disadvantages is the **poor quality of roads being built. New roads quickly degrade and require repairs**" | [president.uz](https://president.uz/en/lists/view/6651) |
| Tashkent inspectors listed **816,023 m²** of streets needing repair; the hokimiyat tells residents to send **photos of bad repairs to Xalq nazorati** (and to stop patching potholes themselves) | [Anhor.uz](https://anhor.uz/news/road-repair/), [UzDaily](https://www.uzdaily.uz/en/tashkent-authorities-urge-residents-to-avoid-unauthorized-road-repairs/) |
| A road complaint on Xalq nazorati was passed between **4 agencies in 15 days**; columnists: nobody supervises trench backfills after utility works | [Anhor.uz](https://anhor.uz/columnists/o-kamerah-luzhah-i-razbitih-dorogah/) |
| 2025 laser survey of 3,100 km of international highways: about **one-third** in satisfactory / insufficient / poor condition | [TRID](https://trid.trb.org/View/2670910) |
| 58 trillion soums spent on roads since 2016 (2,000 km new, 100,000 km repaired) | [president.uz](https://president.uz/en/lists/view/6651) |
| Cost to drivers (US): potholes ≈ $3 bn/year, ~$300 average repair (AAA 2016); UK: 5,761 collisions from defective road surface 2013–2022, 91 fatal | [CBS/AAA](https://www.cbsnews.com/detroit/news/aaa-pothole-damage-costs-drivers-3-billion-every-year), [World Highways](https://www.worldhighways.com/wh9/news/uks-pothole-crisis-causing-vehicle-damage-and-crashes) |

## Who benefits
City road department / hokimiyat (find and prioritise defects, check contractors), drivers (warnings, less car damage), fleets (route around bad roads), the 58-trillion-soum road budget (spend on contractors whose work lasts).

## What already exists (be honest)
- **Waze** has a pothole report type, crowd confirmation, expiry, and government partnerships (Selangor, Malaysia: 19,000+ reports, fix within 5 days) ([Waze help](https://support.google.com/waze/answer/13739290), [Autobuzz](https://autobuzz.my/2017/12/13/report-pothole-waze-selangor-government-will-fix-5-days/)).
- **Yandex Navigator** (dominant in Uzbekistan) — road events are accidents, road works, cameras, "other"; **no pothole category found** in its help pages ([Yandex](https://yandex.com/support/m-maps/en/events)).
- Many hackathon pothole maps (OpenPotholeMap with driver alerts, PotholeGO with rewards) — see `ideas/research-winners-github-claude1.md`.
- **Contractor durability rating: no one found doing it end to end** (one search, not proof).

## Weak points
| Weakness | Answer |
|---|---|
| Crowded (Waze, hackathon maps) | Automatic detection from dashcams (no manual reporting) + **contractor durability** + fits the existing Xalq nazorati photo flow |
| Buyer is the government (slow) | Start with fleets (route quality) and road contractors (prove their work lasts) |
| Contractor-per-road data needed | Demo with one district; in a pilot, from hokimiyat tender records |
| Map needs coverage (many drivers) | Fleets' dashcams cover main routes daily |
| Wet roads, shadows look like cracks; RDD2022 is dry/daylight; weights licence unclear (AGPL / CC BY-SA) | Quality gate + honest per-condition results |

## Verdict
**Valid, with the strongest LOCAL evidence of the three** (government's own words on road quality, the 25% figure, Xalq nazorati flow). Weaker on originality (pothole maps are common) — the **contractor rating** is the original part. Buildable tonight with a pretrained road-damage detector + map + GPS warning.

## All three ideas compared
| | DriveCoach | Car damage | Pothole map + contractor rating |
|---|---|---|---|
| Local problem evidence | strong (2,203 deaths; commercial = 32.5% of crashes; falling asleep = 4.2% of accidents Q1 2026) | medium | **strongest** (gov: 25% of accidents from roads; "new roads quickly degrade") |
| Proof the tech helps | independent studies | disputed | indirect (Waze/Selangor fixes) |
| Originality | medium (fusion) | medium (workshop routing) | low for the map, **high for contractor rating** |
| Data needed tonight | none | a lot | pretrained detector (licence check) + our own photos |
| Live jury demo | ✅✅ | ✅ | ✅ photo of a crack → pin on map → warning |
| Buyer speed | fleets (fast) | drivers/fleets | city (slow) / fleets |
