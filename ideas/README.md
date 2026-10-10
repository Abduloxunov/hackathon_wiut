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
| RoadProof | (on `claude2/strategy`, not pushed yet) | claude-2 | | | |
| LensCheck | (on `claude2/strategy`, not pushed yet) | claude-2 | | | |
