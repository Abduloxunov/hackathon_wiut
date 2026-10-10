# MDB Vision — WIUT Hackathon 2026 Finals (Computer Vision track)

Finals build for team **MDB Vision**, 10–11 Oct 2026 at WIUT.
**Code freeze: Sun 11 Oct, 13:00.** Defence: **7 min + 3 min Q&A, hard stop**, IB201.

## Team
| Name | GitHub | Works with |
|---|---|---|
| Davlatyor Abduloxunov (lead) | @Abduloxunov | Claude Code (`claude-1`) |
| Muhammadjon Xalimov | @muxammadjonx07-dev | Claude Code (`claude-2`) |
| Bexruz Xasanov | @bekhruz-khasanov | TBD |

## The task
Full statement: [docs/task.md](docs/task.md).

## Layout
| Folder | What goes there |
|---|---|
| `src/` | All code (models, pipeline, demo app) |
| `notebooks/` | Experiments |
| `data/` | Small samples only — big datasets/weights stay out of git (see `.gitignore`) |
| `pitch/` | Deck, demo video, screenshots |
| `ideas/` | Idea collection (current phase) — one file per idea |
| `docs/` | Task statement, decisions, worklog |

## How we work (several AI agents, one repo)
Binding rules for humans and agents: [AGENTS.md](AGENTS.md). Lead = Davlatyor + `claude-1`.

| File | Purpose |
|---|---|
| [docs/tasks.md](docs/tasks.md) | Task board — who does what (lead assigns) |
| [docs/team.md](docs/team.md) | Roster, current focus, messages between agents |
| [docs/decisions.md](docs/decisions.md) | Approved decisions and shared interfaces |
| [docs/worklog.md](docs/worklog.md) | History of what was done |
