# Submission — team dashboard form

**Current submission product: CarDoctor — multimodal (visual + text) RAG.** Three modes: used-car buying check, fleet triage, breakdown/accident assistance. [Final scope](../ideas/FINAL-PICK.md) · [Assignments](tasks.md). DriveCoach and the road map are future modules.

Deadline: **Sun 11 Oct, 13:00 (code freeze)**. Resubmitting is allowed until then; the latest version counts.
At the deadline the repo is archived and the deployed site is monitored — after it, only redeploying the submitted commit is allowed.
Owner: lead (`claude-1` + Davlatyor) — task T4 in `docs/tasks.md`.

## The form (from the dashboard, 10 Oct)
| Field | What goes in | Our value |
|---|---|---|
| Prototype (deployed web version) | Public `https://` link — judges open it on their own laptops and phones | _TBD_ |
| Defence deck | File upload, **PDF or .pptx, max 50 MB** | _TBD_ (`pitch/`) |
| Repository | Public link: code, README to run it, data sources + licences | https://github.com/Abduloxunov/mdb-vision-finals (**make public first**) |
| Message to the reviewers (optional) | Free text | Draft below |

Submitting confirms the work is the team's own and complies with the T&C. Every member gets an e-mail receipt.

## Checklist before pressing Submit
- [ ] Demo URL opens on a phone over mobile data (not only on our Wi-Fi), works on an input we have never seen.
- [ ] Demo is deployed **from this repo** (frontend + backend); deployment history visible (GitHub Actions or host's deploy log).
- [ ] Repo is **public**; no secrets, no `.env`, no personal data (faces/plates without consent) anywhere in history.
- [ ] README: what it is, how to run locally, how it is deployed, architecture.
- [ ] README: **data sources with licences**, pretrained models/weights with licences, reused elimination-stage code declared, LLM/coding-assistant use declared.
- [ ] Product-performance numbers in deck and README come from our tests: visual retrieval top-1/top-3 accuracy, latency, cost per check and failure cases, with test set, hardware and date. External market facts have sources; budget assumptions are labelled. No internal idea scores or controlled demo inputs are presented as measured product quality.
- [ ] Deck exported to PDF (and .pptx), < 50 MB; first slide names the mode (Startup / Partner product).
- [ ] Recorded backup video of the demo (in case live fails).
- [ ] Note the submitted commit hash here: `________`.

## Message to the reviewers (draft)
_TBD — e.g. test inputs to try, known limitations, where to find the evaluation in the README._
