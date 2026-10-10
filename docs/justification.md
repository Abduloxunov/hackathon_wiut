# Why DriveCoach — problem, beneficiaries, evidence (for the pitch, T12)

**Historical DriveCoach evaluation; not the current T12 pitch brief.** CarDoctor was selected at 02:20 on Sun 11 Oct. Use [justification-cardoctor.md](justification-cardoctor.md) and [FINAL-PICK](../ideas/FINAL-PICK.md) for the current product. DriveCoach is a future module.

Compiled by claude-1, Sun 11 Oct 01:00. Use ONLY these sourced numbers in the deck.

## Problem
| Fact | Source |
|---|---|
| Uzbekistan 2024: 9,364 crashes, 2,203 deaths, 8,901 injured | [Kun.uz 1 Feb 2025](https://kun.uz/en/news/2025/02/01/one-third-of-accidents-in-2024-involved-cargo-and-passenger-transport) |
| 3,045 crashes (32.5%) involved cargo and passenger transport; Damas = 1,592 (52.3% of those) | same (Transport Minister) |
| 351 crashes (3.7%) from breaking work/rest schedules → fatigue / falling asleep → 189 deaths, 285 injuries (official; likely under-reported — our inference) | same |
| 2025: 2,188 deaths (Road Safety Service) | [Kun.uz Dec 2025](https://kun.uz/en/news/2025/12/30/do-investments-save-lives-a-data-driven-look-at-traffic-safety-in-uzbekistan) |
| Drowsy driving: 4–6× near-crash/crash risk; eyes off road > 2 s cumulative: ≥ 2× risk (re-analysis: OR 1.6) | [NHTSA DOT HS 810 594 / VTTI 100-Car](https://www.nhtsa.gov/document/810594driverinattentionnearcrashcrashriskpdf), [case-crossover re-analysis](https://trid.trb.org/view/1122843) |

## Why now
- EU GSR: drowsiness warning (DDAW) mandatory for all new cars from 7 Jul 2024; advanced distraction warning (ADDW) for all new vehicles from 7 Jul 2026 ([summary](https://captaincompliance.com/education/addw-systems-explained-eus-driver-distraction-mandate/); verify against Reg. (EU) 2019/2144).
- Uzbekistan's existing fleet (4.55 M private passenger cars, Apr 2026 — [Kursiv/stat.uz](https://uz.kursiv.media/en/2026-06-24/uzbek-national-fleet-nears-five-mln-vehicles-despite-subtle-market-slowdown/)) is mostly older models without these systems → retrofit gap (our inference).

## Who benefits / pays
Commercial fleets first (taxi parks, Damas routes, cargo), then insurers. Yandex Go reports 11 bn soums on safety in 2025 and monitors speeding/route deviation — no fatigue monitoring mentioned in its published policy ([source](https://weproject.media/articles/detail/yandex-uzbekistan-predstavil-politiku-bezopasnosti-yandex-taxi/)).

## Evidence monitoring helps
- VTTI field study, 7 fleets, 3.8 M miles: high-severity event rates −64% and −37% in two fleets with monitoring/coaching ([source](https://pubs.lib.uiowa.edu/driving/article/28094/galley/136386/view)).
- SWOV (NL, 1997, 840 vehicles, older recorders): ≈20% accident reduction, wide confidence intervals ([source](https://www.swov.nl/en/node/14246)).
- Vendor claims (40–80%) — do NOT use.

## Weak points + answers
| Weakness | Answer |
|---|---|
| Competitors (Nauto, Samsara, Seeing Machines) | Expensive hardware for US/EU; we are a phone-only retrofit for old local vehicles |
| "Common hackathon demo" | Context fusion (glance away WHILE car ahead is close), honest measured test set, "monitoring unavailable" state |
| Driver privacy | Video stays on the phone; only events go to the fleet; coaching first |
| Night (no IR on phones) | Stated as known failure; IR camera in pilot |

## One-line pitch
"Europe now requires driver-attention warnings in every new car. Uzbekistan's 4.5 million existing cars have none. DriveCoach retrofits it with a phone — starting with commercial fleets, involved in a third of crashes."
