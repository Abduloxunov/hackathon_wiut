# Rules for AI agents and humans in this repo

Several AI agents work here in parallel: **Claude Code** (Davlatyor), a second **Claude Code**, and **Codex** (ChatGPT).
Read this file before making changes. `CLAUDE.md` points here too.

## Context
- WIUT Hackathon 2026 finals, Computer Vision track, team MDB Vision.
- Task statement: `docs/task.md`. Code freeze **Sun 11 Oct 13:00**. Judging: Innovation 25%, Technical complexity 25%, Impact & practicality 25%, Presentation 15%, Business potential 10%.

## Avoiding conflicts
1. **Pull first** — `git pull --rebase origin main` before starting work.
2. **One branch per agent and topic** — `claude/<topic>` (Claude Code), `claude2/<topic>` (second Claude Code), `codex/<topic>` (Codex — its default prefix). Codex: read this file before every task; open a PR, never push to `main`. Do not commit directly to `main` except for tiny doc fixes.
3. **Claim your area** — add a line to the "Who is doing what" table in `docs/worklog.md` before you start, so two agents don't edit the same files.
4. **Small PRs, merged often** (every 1–2 h). Long-lived branches will conflict.
5. **Do not reformat or rename files you don't own** — it breaks the other agent's merge.
6. **Interfaces go in `docs/decisions.md`** — function signatures, file formats, JSON schemas shared between parts. Change them only after telling the team.

## Code
- Python 3.11. Dependencies in `requirements.txt` (add yours there, pinned).
- Entry points live in `src/`; keep notebooks for experiments only.
- No large files in git: datasets, videos, model weights (`*.pt`, `*.onnx`, …) are ignored. Share them via Google Drive/Telegram and write the link in `docs/decisions.md`.
- No secrets in git (API keys go in `.env`, which is ignored).

## Logging
After each piece of work, append to `docs/worklog.md`: time, who (human + agent), what was done, what is next.
