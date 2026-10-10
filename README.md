# CarDoctor — MDB Vision, WIUT Hackathon 2026 Finals

Finals build for team **MDB Vision**, 10–11 Oct 2026 at WIUT.
**Code freeze: Sun 11 Oct, 13:00.** Defence: **7 min + 3 min Q&A, hard stop**, IB201.

## Team
| Name | GitHub | Works with |
|---|---|---|
| Davlatyor Abduloxunov (lead) | @Abduloxunov | Own Codex for development (`dav/`); Claude Code (`claude-1`) for review/pitch |
| Muhammadjon Xalimov | @muxammadjonx07-dev | Claude Code (`claude-2`) |
| Bexruz Xasanov | @bekhruz-khasanov | Codex (`codex`) |

## Current product — CarDoctor
The lead selected **CarDoctor — multimodal (visual + text) RAG** on Sun 11 Oct at 02:20. A driver supplies car photos, symptoms, and the car model; the planned system retrieves visual matches and sourced repair knowledge, then produces a first assessment, urgency, an indicative cost range, and suitable workshops.

Three modes share one engine: **used-car buying check**, **fleet triage**, and **breakdown/accident assistance**. DriveCoach and the road map are future modules, outside the current build.

Planned flow: photos → visual reference retrieval; words/model → repair-knowledge retrieval; combined evidence → explanation with citations → workshop matching and map. Model candidates (CLIP/DINOv2 and multilingual text embeddings) are recorded in the final pick; exact implementation choices and shared interfaces remain to be confirmed by the developer.

The decision and assignments are documented; this README does not claim a completed deployment, measured accuracy, or verified repair prices. Add run instructions, deployment details, data/model licences, and measured results when available.

- [Final selection and scope](ideas/FINAL-PICK.md)
- [Build assignments](docs/tasks.md)
- [CarDoctor rationale and limits](docs/justification-cardoctor.md)
- [Recorded decisions and shared interfaces](docs/decisions.md)

## The task
Full statement: [docs/task.md](docs/task.md).

## Research
Everything we researched before building — 44 ideas, the CV methods for each, evidence, models, datasets, licences and our decision: **[docs/RESEARCH.md](docs/RESEARCH.md)**.

## Layout
| Folder | What goes there |
|---|---|
| `src/` | Product code (models, retrieval pipeline, demo app), owned by T10 |
| `notebooks/` | Experiments |
| `data/` | Small samples only — big datasets/weights stay out of git (see `.gitignore`) |
| `pitch/` | CarDoctor deck, demo video, screenshots (T12) |
| `kb/` (planned) | Sourced repair knowledge, local price evidence, workshop records (T13) |
| `ideas/` | Earlier proposals and research, plus the final CarDoctor selection |
| `docs/` | Task statement, decisions, worklog |

## How we work (several AI agents, one repo)
Binding rules for humans and agents: [AGENTS.md](AGENTS.md). Lead = Davlatyor + `claude-1`.

| File | Purpose |
|---|---|
| [docs/tasks.md](docs/tasks.md) | Task board — who does what (lead assigns) |
| [docs/team.md](docs/team.md) | Roster, current focus, messages between agents |
| [docs/decisions.md](docs/decisions.md) | Approved decisions and shared interfaces |
| [docs/worklog.md](docs/worklog.md) | History of what was done |
| [docs/submission.md](docs/submission.md) | Submission form + checklist |
