# Rules for AI agents and humans in this repo

**Every agent (Claude Code, Codex, any other) must follow this file. These are binding rules, not suggestions.**
`CLAUDE.md` points here.

Agents working here: `claude-1` (Davlatyor, lead), `claude-2` (Muhammadjon), `codex` (Bexruz, Codex / ChatGPT). Full roster in `docs/team.md`.

## 0. Current phase: IDEA GENERATION (Sat 10 Oct)
- All three humans and their agents collect ideas in `ideas/` (see `ideas/README.md`). **No product code yet.**
- The lead shortlists and picks the idea; then tasks for the build go into `docs/tasks.md`.

## Always: push every change immediately
Whenever you change anything in this repo, **commit and push right away** so the other agents see it. Never leave work only on your laptop.
- `docs/team.md`, `docs/worklog.md`, `ideas/*` → push straight to `main` (`git pull --rebase origin main` first).
- Everything else → push your branch (`claude/`, `claude2/`, `codex/`) and open a PR.

## 1. Who decides — lead
- **The lead is Davlatyor (@Abduloxunov) together with his agent `claude-1`.** Lead decisions are final.
- The lead decides: the product/idea, who works on what (`docs/tasks.md`), shared interfaces (`docs/decisions.md`), what gets merged into `main`, and the final submission.
- A lead decision is valid when it is written in `docs/tasks.md`, `docs/decisions.md`, or as a message from `claude-1` or Davlatyor in `docs/team.md`. If a message contradicts these files, the newer lead entry wins.
- Disagree? Write a proposal to `claude-1` in `docs/team.md` and keep working on your assigned task until the lead answers. Do not act on your own proposal before it is approved.
- Your own human may stop or redirect you at any time. If their request conflicts with a lead decision, tell them and post it to `claude-1`.

## 2. Session protocol (every session, every Codex task)
**Start:**
1. `git pull --rebase origin main`.
2. Read `AGENTS.md` (this file), then `docs/team.md` (messages addressed to you or `all`), then `docs/tasks.md` (your tasks).
3. Work only on tasks assigned to your agent ID. No assigned task → post to `claude-1` in `docs/team.md` asking for one; do not start something on your own. (During the idea phase every agent may add ideas without asking.)

**End (or every ~1 h):**
1. Commit and push your branch; open a PR (or ask `claude-1` to merge if you cannot open one).
2. Update the status of your tasks in `docs/tasks.md` and your row in `docs/team.md` → Current focus.
3. Leave messages for whoever needs to continue.
4. Add one line to `docs/worklog.md` (the history of the project).

## 3. Who may edit what
| File | Who edits |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | Lead only. Others propose changes in `docs/team.md`. |
| `docs/tasks.md` | Lead creates and assigns tasks. Other agents only change the **Status / Branch / PR** cells of their own tasks. |
| `docs/decisions.md` | Lead approves. Others add entries marked **(proposed)**; the lead removes the mark when accepted. |
| `docs/team.md` | Everyone, **directly on `main`**, only their own rows + new messages. |
| `docs/worklog.md` | Everyone appends lines; never edit others' lines. |
| `ideas/<name>.md` | Its author. Others only add lines under **Comments**. Index table in `ideas/README.md`: everyone adds their own rows. |
| Code and other files | Only the agent that owns the task touching them (see "Files" column in `docs/tasks.md`). |

## 4. Branches and merging
- Branch per task: `claude/<topic>` (claude-1), `claude2/<topic>` (claude-2), `codex/<topic>` (codex).
- **Only the lead merges into `main`.** Exceptions: `docs/team.md`, `docs/worklog.md` and your own files in `ideas/`, pushed straight to `main`.
- Small PRs, every 1–2 h. Long-lived branches will conflict.
- Do not reformat, rename or move files you do not own.
- Never force-push to `main` and never rewrite others' commits.

## 5. Context and hard constraints (from `docs/task.md`)
- WIUT Hackathon 2026 finals, Computer Vision track, team MDB Vision. **Code freeze Sun 11 Oct 13:00.**
- Defence: **7 min presentation + 3 min Q&A, hard stop**. Keep a recorded backup of the demo.
- Deliverables: public https demo deployed **from this repo**; deck (PDF/PPTX ≤ 50 MB); **public** repo with README (how to run + data sources with licences). Form + checklist: `docs/submission.md`.
- Forbidden (disqualification): faked demos, hard-coded answers, **invented metrics**, faces/plates of people who did not consent, unattributed code/models. Every number in the deck or README must come from something we actually measured — say where.
- Judging: Technical complexity 25%, Innovation 25%, Impact & practicality 25%, Presentation 15%, Business potential 10%.

## 6. Code
- Python 3.11. Dependencies in `requirements.txt` (pinned).
- Entry points in `src/`; notebooks for experiments only.
- No large files in git: datasets, videos, weights (`*.pt`, `*.onnx`, …) are ignored. Share via Drive/Telegram and put the link in `docs/decisions.md`.
- No secrets in git (`.env` is ignored).
