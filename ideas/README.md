# Ideas — collection phase

**Current phase: idea generation.** All three of us (and our agents) add ideas here. No code yet.
The lead (Davlatyor + `claude-1`) picks the final idea after the shortlist (`AGENTS.md` §1).

## How to add an idea
1. Copy [`_template.md`](_template.md) to `ideas/<short-name>.md` (kebab-case, e.g. `ideas/dealer-damage-check.md`).
2. Fill it in. Mark anything you have not checked as `(unverified)`. No invented numbers.
3. Add one row to the table below.
4. **Commit and push to `main` right away** (`git pull --rebase origin main && git add ideas && git commit -m "idea: <name>" && git push`). Idea files are the exception to "only the lead merges": push them straight to `main` so everyone sees them immediately.
5. Only edit your own idea files. To comment on someone else's idea, add a line under its **Comments** section with your agent ID.

Codex (cloud) cannot push to `main`: open a PR titled `idea: <name>` — the lead merges it quickly.

## Score (0–10 each, filled by the lead during shortlisting)
Weights from `docs/task.md`: Technical 25 · Innovation 25 · Impact 25 · Presentation/demo 15 · Business 10.
Extra filter: **can we build a working, deployed demo in ~8 h?** If not, it does not make the shortlist.

**Start here for the focus subdomain:** [DEALER-SERVICE-ALL-IDEAS.md](DEALER-SERVICE-ALL-IDEAS.md) — every dealer/service idea from all three agents, merged and credited.

## Lead likes (noted, NOT selected)
- **Just Walk Out style** (Amazon): track a person entering and everything they take. Possible fit: the service bay (car + mechanic + parts taken → job card/invoice builds itself).
- **Tractable style**: app analyses the car → detects defects/damage → **repair cost**, **3D model** of the car, damage analysis.

## Ideas
| Idea | File | Added by | Direction | One line | Score |
|---|---|---|---|---|---|
| **TrueClaim** ⭐ claude-2's top pick | [trueclaim.md](trueclaim.md) | Muhammadjon + claude-2 | vehicle inspection / insurance | Claim photo → recapture (photo-of-screen), reuse/duplicate, EXIF, quality + damage map → accept / live retake / manual review | |
| RoadProof | [roadproof.md](roadproof.md) | Muhammadjon + claude-2 | road safety | Road photo → damage detection → ticket; **before/after repair verification** via image alignment | |
| TradeIn PreCheck | [tradein-precheck.md](tradein-precheck.md) | Muhammadjon + claude-2 | dealer ops (partner: Toyota/BYD Royal Motors) | Customer's guided photos → completeness + damage + odometer OCR + dealer rules → trade-in eligibility | |
| LensCheck (fallback) | [lenscheck.md](lenscheck.md) | Muhammadjon + claude-2 | vehicle inspection | Inspection photo set → quality + angle coverage → retake list | |
| ChargeBay Watch | [chargebay-watch.md](chargebay-watch.md) | Muhammadjon + claude-2 | EV / infrastructure | Charging-area frame → bay free / charging / blocked → alert | |
| ClaimProof — trusted damage evidence (live capture + forgery checks + damage seg) | [research-landscape-claude1.md](research-landscape-claude1.md) §A | claude-1 | inspection / insurance | Jury photographs any car; we flag damage + whether photo is real | |
| Handover Diff — only *new* damage between intake and pickup | §B | claude-1 | service ops | Two walkarounds aligned per panel → change detection | |
| Junction Risk Map — near-miss metrics from our elimination code | §C | claude-1 | road safety / city | Tracks → BEV → TTC/PET → risk heatmap | |
| EV Bay Guard — ICE-ing detection without reading plates | §D | claude-1 | EV infra | EV vs ICE by model/shape + not-charging timer | |
| TyreAge — DOT date OCR + tread wear from one photo | §E | claude-1 | service / fleet | Sidewall photo → replace now/soon/OK | |
| Repaint Radar — hidden accident history + phone deflectometry | §F | claude-1 | trade-in | Panel ΔE mismatch + stripe-reflection dent check | |
| Rider Line — Ducati lean-angle coaching from video | §G | claude-1 | rider safety | Horizon tilt → lean per corner | |
| **DriveCoach** — driver + road camera, risk in context (team brainstorm) | [drive-coach.md](drive-coach.md) | Davlatyor + claude-1 | driver / road safety | Eyes off road *while* car ahead is close → alert + trip score; paired devices because browsers can't open 2 cameras | |
| TyreCheck | [tyrecheck.md](tyrecheck.md) | Muhammadjon + claude-2 | service ops + safety (partner: Toyota/BYD service intake) | Tyre photos → wear vs wear bar + **age from DOT code OCR** + cracks → replace now / soon / OK | |
| Service-Bay Tracker | [service-bay-tracker.md](service-bay-tracker.md) | Muhammadjon + claude-2 | service ops (partner: Royal Motors aftersales) | Workshop CCTV → bay state timeline + idle alerts. Weak jury-input demo | |
| PartsLens | [parts-lens.md](parts-lens.md) | Muhammadjon + claude-2 | parts / warehouse (partner) | Photo of a loose part → top-3 OEM numbers via embedding search + size check | |
| Driver Fatigue Guard | [driver-fatigue-guard.md](driver-fatigue-guard.md) | Muhammadjon + claude-2 | driver safety (fleets) | In-browser MediaPipe: eyes, yawns, phone → alert; easy but low innovation | |
| RoadGuard AI (video) | [roadguard-video.md](roadguard-video.md) | Muhammadjon + claude-2 | road safety (fleets) | Dashcam MP4 → road-damage detection → **dedup into unique events** + evidence frames → fleet report. Video sibling of RoadProof | |
| SmartFlow AI | [smartflow.md](smartflow.md) | Muhammadjon + claude-2 | city traffic | Junction video → queues per approach → **recommended** green split (advisory) + SUMO fixed-vs-adaptive benchmark. Weak jury input; overlaps claude-1 Junction Risk Map | |
| RoyalScan — Guided Vehicle Condition Inspection | [royalscan-codex.md](royalscan-codex.md) | Bexruz + codex | vehicle inspection / dealer ops | Guided phone photos + local repair rules → reviewable damage evidence, missing-view checks and traceable bodywork estimate | |
| DriveAlert — Driver Drowsiness & Distraction Monitor | [drivealert-codex.md](drivealert-codex.md) | Bexruz + codex | driver / road safety | Consented cabin camera + calibration/visibility/time rules → explained possible-attention alerts and local event report | |

Research behind the claude-2 ideas (sources, licences, local stats, deploy limits): [_research-notes-claude2.md](_research-notes-claude2.md)
Principle for all ideas — **vision + context data → decision** (weather, satellite, knowledge base): [principle-vision-plus-context.md](principle-vision-plus-context.md)
Research behind the claude-1 ideas (competitors, methods, datasets): [research-landscape-claude1.md](research-landscape-claude1.md)
