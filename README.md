# MDB Vision — WIUT Hackathon 2026 Finals (Computer Vision track)

Finals build for team **MDB Vision**, 10–11 Oct 2026 at WIUT.
**Code freeze: Sun 11 Oct, 13:00.** Pitch: 10 min + 2 min Q&A, IB201.

## Team
| Name | GitHub | Works with |
|---|---|---|
| Davlatyor Abduloxunov (lead) | @Abduloxunov | Claude Code |
| Muhammadjon Xalimov | @muxammadjonx07-dev | ChatGPT |
| Bexruz Xasanov | @bekhruz-khasanov | |

## The task
_Announced Sat 10 Oct, 12:30 — paste the full statement into [docs/task.md](docs/task.md)._

## Layout
| Folder | What goes there |
|---|---|
| `src/` | All code (models, pipeline, demo app) |
| `notebooks/` | Experiments |
| `data/` | Small samples only — big datasets/weights stay out of git (see `.gitignore`) |
| `pitch/` | Deck, demo video, screenshots |
| `docs/` | Task statement, decisions, worklog |

## How we work (several AI agents, one repo)
See [AGENTS.md](AGENTS.md) — rules for both humans and AI (Claude Code ×2 + Codex).

Quick version:
1. `git pull` before you start anything.
2. Work on your own branch: `claude/<topic>` (Claude Code), `claude2/<topic>` (second Claude Code), `codex/<topic>` (Codex — its default prefix).
3. Small commits, push often, open a PR into `main`.
4. Log what you did in [docs/worklog.md](docs/worklog.md).
