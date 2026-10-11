# Task board (workload)

**Owned by the lead (Davlatyor + `claude-1`).** The lead adds tasks and assigns owners.
Other agents only update **Status**, **Branch** and **PR** of their own tasks. Edit on `main`.
Rules: `AGENTS.md` §1–3.

Status: `todo` → `doing` → `review` (PR open) → `done` · `blocked` (say why in Notes) · `superseded` (replaced by the final scope).
Agents: Davlatyor's own Codex (developer, `dav/`), `claude-1` (Davlatyor, reviewer/pitch), `claude-2` (Muhammadjon), `codex` (Bexruz).

**Phase now: BUILD (Sun 11 Oct). Product = CarDoctor (multimodal RAG) — decided 02:20; DriveCoach superseded** (`ideas/FINAL-PICK.md`). Code freeze 13:00. **Latest handoff (02:40): Davlatyor builds with his own Codex (`dav/`).** claude-1 reviews methods and handles the pitch, without product-code ownership. Others support data, testing, knowledge base and pitch.

## Open decisions (lead) — after the idea phase
- [x] Product / idea — **CarDoctor (multimodal RAG)**, lead decision Sun 11 Oct 02:20. RoadProof, LensCheck, and the earlier DriveCoach build choice are superseded.
- [ ] Exact model selection, data schemas, and API interfaces — developer to confirm in `docs/decisions.md`.
- [ ] Mode on slide 1: Startup or Partner product.

## Tasks
| ID | Task | Owner | Files | Status | Branch | PR | Notes |
|---|---|---|---|---|---|---|---|
| T1 | Paste finals task statement | claude-2 | `docs/task.md` | done | `claude2/task-statement` | merged by claude-1 | |
| T2 | Collaboration rules, task board | claude-1 | `AGENTS.md`, `docs/tasks.md`, `docs/team.md` | done | `main` | | |
| T3 | Earlier RoadProof strategy + `POST /api/analyze` proposal | claude-2 | `docs/strategy.md`, `docs/decisions.md` | superseded | `claude2/strategy` | | Historical proposal; remote branch exists. Not the approved CarDoctor interface. |
| T5 | Collect ideas in `ideas/` (each agent: at least 2–3) | all | `ideas/` | done | `main` | | Research archived in `docs/RESEARCH.md`; final product selected. |
| T6 | Deep research: Dealer & service operations subdomain → new ideas | claude-1 + Davlatyor | `ideas/subdomain-dealer-service-*.md` | done | `main` | | Completed research informed CarDoctor; current build work is T10–T14. |
| T10 | CarDoctor app: visual retrieval (CLIP/DINOv2 + vector DB), text RAG, LLM with citations, workshop map, web UI, deploy | Davlatyor + own Codex | `src/`, `web/` | doing | `dav/` (topic branch to be recorded) | | Product developer per 02:40 lead handoff |
| T11 | Photos: reference library + test set — team cars' dashboards at key-on (all warning lights), coloured liquids on paper (leak colours: green, brown/black, red, clear), visible car damage in parking lot (no plates/faces). Name files by label; note source | Muhammadjon (+claude-2) | Drive/Telegram → `data/README.md` | todo | | | Our own data = moat |
| T12 | Pitch deck (7 min): CarDoctor — problem (used-car fraud, repair distrust, fleets), 3 modes, live demo, RAG architecture, measured results, business (workshop lead fee, fleet subscription, per-report), DriveCoach + road map as next modules — use `docs/justification-cardoctor.md` | claude-1; Bexruz (+codex) supports | `pitch/` | todo | `codex/pitch` (support) | | claude-1 handles deck per 02:40; coordinate support with lead. Numbers only from our tests. |
| T13 | Knowledge base with sources: common faults of Cobalt, Nexia, Damas, Gentra, Spark, BYD Song/Yuan; symptom → cause → urgency → repair type; Tashkent repair price ranges (call 3–5 shops, note date); workshop list (dealer service centres + shops: name, type, address, coords) — as CSV/JSON | Bexruz (+codex) | `kb/` (PR) | doing | `codex/cardoctor-docs` | [#6](https://github.com/Abduloxunov/mdb-vision-finals/pull/6) | Cite every row |
| T14 | Measurements: retrieval top-1/top-3 accuracy on T11 test photos, latency, cost per check; failure cases | Muhammadjon (+claude-2) | `docs/results.md` | todo | `claude2/results` | | After first build |
| T4 | Make repo public + final submission (link, deck, repo) | claude-1 | `docs/submission.md` | todo | | | Before Sun 13:00; checklist in `docs/submission.md` |
