# Team roster — humans and agents

Every agent reads this file at the start of each session or task, together with `AGENTS.md` and `docs/worklog.md`.
It answers: who else is working in this repo, what are they doing, and how do I talk to them.

**Edit this file directly on `main`** (pull → edit → commit → push right away), not on your feature branch, otherwise the others will not see your messages until your PR is merged. Keep edits to your own rows so pushes do not conflict.

## Who is who
| Agent ID | Tool | Human | Branch prefix | Runs where | Can push / open PRs? |
|---|---|---|---|---|---|
| `claude-1` | Claude Code (desktop) | Davlatyor Abduloxunov (@Abduloxunov, lead) | `claude/` | Davlatyor's PC | yes |
| `claude-2` | Claude Code | _fill in name_ (@_github_) | `claude2/` | own laptop | yes |
| `codex` | OpenAI Codex (ChatGPT) | _fill in name_ (@_github_) | `codex/` | chatgpt.com/codex or Codex CLI | yes (Create PR) |

Humans: Davlatyor (@Abduloxunov), Muhammadjon Xalimov (@muxammadjonx07-dev), Bexruz Xasanov (@bekhruz-khasanov).
Each human fills in their own row once. The lead (Davlatyor) merges PRs into `main`.

## What each agent knows
Agents do **not** share memory or chat history. Another agent only knows what is in this repo.
So anything another agent needs must be written down here, in `docs/decisions.md`, or in a PR description. Do not rely on "I told my agent".

## Current focus
Each agent keeps its own row up to date (one line, overwrite it when the focus changes).

| Agent ID | Working on now | Files / folders it owns | Updated |
|---|---|---|---|
| `claude-1` | Repo setup, waiting for the task (12:30) | `docs/`, `AGENTS.md` | Sat 10 Oct |
| `claude-2` | — | — | — |
| `codex` | — | — | — |

## Messages between agents
Use this for questions, requests and handoffs to another agent. Add new messages at the **top**.
Format: `time · from → to · message`. When you act on a message, add `✔ done (<your id>)` at the end of its line.
Use `→ all` for something everyone must know.

<!-- newest first -->
- Sat 10 Oct · claude-1 → all · Repo is ready. Read `AGENTS.md`, fill in your row above, and claim your area before writing code. Task statement goes in `docs/task.md` after 12:30.

## Handoff checklist (when you finish or stop)
1. Push your branch and open a PR. The description says what changed, how to run it, and what is unfinished.
2. Update your row in **Current focus**.
3. If someone else needs to continue, leave a message above, addressed to them.
4. Add a line to `docs/worklog.md`.
