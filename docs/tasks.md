# Task board (workload)

**Owned by the lead (Davlatyor + `claude-1`).** The lead adds tasks and assigns owners.
Other agents only update **Status**, **Branch** and **PR** of their own tasks. Edit on `main`.
Rules: `AGENTS.md` §1–3.

Status: `todo` → `doing` → `review` (PR open) → `done` · `blocked` (say why in Notes).
Agent IDs: `claude-1` (Davlatyor), `claude-2` (Muhammadjon), `codex` (Bexruz).

**Phase now: idea generation** — everyone adds ideas to `ideas/`. Build tasks come after the lead picks the idea.

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
| T4 | Make repo public + final submission (link, deck, repo) | claude-1 | `docs/submission.md` | todo | | | Before Sun 13:00; checklist in `docs/submission.md` |
