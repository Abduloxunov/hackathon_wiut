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

## Ideas
| Idea | File | Added by | Direction | One line | Score |
|---|---|---|---|---|---|
| **TrueClaim** ⭐ claude-2's top pick | [trueclaim.md](trueclaim.md) | Muhammadjon + claude-2 | vehicle inspection / insurance | Claim photo → recapture (photo-of-screen), reuse/duplicate, EXIF, quality + damage map → accept / live retake / manual review | |
| RoadProof | [roadproof.md](roadproof.md) | Muhammadjon + claude-2 | road safety | Road photo → damage detection → ticket; **before/after repair verification** via image alignment | |
| TradeIn PreCheck | [tradein-precheck.md](tradein-precheck.md) | Muhammadjon + claude-2 | dealer ops (partner: Toyota/BYD Royal Motors) | Customer's guided photos → completeness + damage + odometer OCR + dealer rules → trade-in eligibility | |
| LensCheck (fallback) | [lenscheck.md](lenscheck.md) | Muhammadjon + claude-2 | vehicle inspection | Inspection photo set → quality + angle coverage → retake list | |
| ChargeBay Watch | [chargebay-watch.md](chargebay-watch.md) | Muhammadjon + claude-2 | EV / infrastructure | Charging-area frame → bay free / charging / blocked → alert | |

Research behind the claude-2 ideas (sources, licences, local stats, deploy limits): [_research-notes-claude2.md](_research-notes-claude2.md)
| ClaimProof — trusted damage evidence (live capture + forgery checks + damage seg) | [research-landscape-claude1.md](research-landscape-claude1.md) §A | claude-1 | inspection / insurance | Jury photographs any car; we flag damage + whether photo is real | |
| Handover Diff — only *new* damage between intake and pickup | §B | claude-1 | service ops | Two walkarounds aligned per panel → change detection | |
| Junction Risk Map — near-miss metrics from our elimination code | §C | claude-1 | road safety / city | Tracks → BEV → TTC/PET → risk heatmap | |
| EV Bay Guard — ICE-ing detection without reading plates | §D | claude-1 | EV infra | EV vs ICE by model/shape + not-charging timer | |
| TyreAge — DOT date OCR + tread wear from one photo | §E | claude-1 | service / fleet | Sidewall photo → replace now/soon/OK | |
| Repaint Radar — hidden accident history + phone deflectometry | §F | claude-1 | trade-in | Panel ΔE mismatch + stripe-reflection dent check | |
| Rider Line — Ducati lean-angle coaching from video | §G | claude-1 | rider safety | Horizon tilt → lean per corner | |
