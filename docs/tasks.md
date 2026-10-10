# Task board (workload)

**Owned by the lead (Davlatyor + `claude-1`).** The lead adds tasks and assigns owners.
Other agents only update **Status**, **Branch** and **PR** of their own tasks. Edit on `main`.
Rules: `AGENTS.md` §1–3.

Status: `todo` → `doing` → `review` (PR open) → `done` · `blocked` (say why in Notes).
Agent IDs: `claude-1` (Davlatyor), `claude-2` (Muhammadjon), `codex` (Bexruz).

**Phase now: BUILD (Sun 11 Oct). Product = CarDoctor (multimodal RAG) — decided 02:20; DriveCoach superseded** (`ideas/FINAL-PICK.md`). Code freeze 13:00. **Davlatyor is the only developer** (with claude-1). Others: data, testing, pitch, research.

## Open decisions (lead) — after the idea phase
- [ ] Product / idea — proposal from claude-2: RoadProof, fallback LensCheck (`claude2/strategy`, not pushed yet).
- [ ] Mode on slide 1: Startup or Partner product.

## Tasks
| ID | Task | Owner | Files | Status | Branch | PR | Notes |
|---|---|---|---|---|---|---|---|
| T1 | Paste finals task statement | claude-2 | `docs/task.md` | done | `claude2/task-statement` | merged by claude-1 | |
| T2 | Collaboration rules, task board | claude-1 | `AGENTS.md`, `docs/tasks.md`, `docs/team.md` | done | `main` | | |
| T3 | Strategy + `POST /api/analyze` contract proposal | claude-2 | `docs/strategy.md`, `docs/decisions.md` | review | `claude2/strategy` | | Push the branch — not on GitHub yet |
| T5 | Collect ideas in `ideas/` (each agent: at least 2–3) | all | `ideas/` | doing | `main` | | Use `ideas/_template.md` |
| T6 | Deep research: Dealer & service operations subdomain → new ideas | claude-1 + Davlatyor | `ideas/subdomain-dealer-service-*.md` | doing | `main` | | Lead's chosen focus |
| T10 | CarDoctor app: visual retrieval (CLIP/DINOv2 + vector DB), text RAG, LLM with citations, workshop map, web UI, deploy | claude-1 + Davlatyor | `src/`, `web/` | doing | `claude/cardoctor` | | Only developer |
| T11 | Photos: reference library + test set — team cars' dashboards at key-on (all warning lights), coloured liquids on paper (leak colours: green, brown/black, red, clear), visible car damage in parking lot (no plates/faces). Name files by label; note source | Muhammadjon (+claude-2) | Drive/Telegram → `data/README.md` | todo | | | Our own data = moat |
| T12 | Pitch deck (7 min): CarDoctor — problem (used-car fraud, repair distrust, fleets), 3 modes, live demo, RAG architecture, measured results, business (workshop lead fee, fleet subscription, per-report), DriveCoach + road map as next modules — use `docs/justification-cardoctor.md` | Bexruz (+codex) | `pitch/` | todo | `codex/pitch` | | Numbers only from our tests |
| T13 | Knowledge base with sources: common faults of Cobalt, Nexia, Damas, Gentra, Spark, BYD Song/Yuan; symptom → cause → urgency → repair type; Tashkent repair price ranges (call 3–5 shops, note date); workshop list (dealer service centres + shops: name, type, address, coords) — as CSV/JSON | Bexruz (+codex) | `kb/` (PR) | todo | `codex/kb` | | Cite every row |
| T14 | Measurements: retrieval top-1/top-3 accuracy on T11 test photos, latency, cost per check; failure cases | Muhammadjon (+claude-2) | `docs/results.md` | todo | `claude2/results` | | After first build |
| T4 | Make repo public + final submission (link, deck, repo) | claude-1 | `docs/submission.md` | todo | | | Before Sun 13:00; checklist in `docs/submission.md` |
