# CarDoctor submission readiness

Current local status, 11 October 2026. Code freeze: **13:00 Asia/Tashkent**. This complements the lead's official `docs/submission.md`; it does not submit or change assignments.

## Ready and verified

- Working responsive local app: http://127.0.0.1:8766/ . Optional photo or symptom description, candidate boxes for supported exterior components, sourced retrieval, optional LLM explanation, context questions and MD export.
- Completed 12 total CarDD epochs; best EMA selected at epoch 10, downloaded and hash-verified, configured in the app after tests. Pilot retained for rollback.
- Current checkpoint validation mAP50 0.7397 / mAP50-95 0.5931 on 810 images. Official 374-image test mAP50 0.7354 / mAP50-95 0.5916; macro F1 0.7135 at confidence 0.35 / IoU 0.50. [Full comparison](CARDOCTOR-MODEL-COMPARISON.md).
- Twelve pipeline checks; nine real browser checks. Earlier pilot engineering samples measured warm repeated single-image offline median 0.364 seconds and cold example with LLM 22.257 seconds; these are not current-checkpoint latency benchmarks or service SLAs.
- 28 source records, 20 sources, offline fallback and backend-only OpenRouter configuration. [Current pipeline and verified scope](CARDOCTOR-PIPELINE.md).
- Runnable instructions, source attribution, measured package snapshot, training results and shareable project brief.

## Remaining before submission

| Item | Current state | Next concrete action |
|---|---|---|
| Public HTTPS app | Not deployed by this chat | Lead/developer selects host, ports Windows runtime, provisions private weights/index and backend secret; verify from a second device |
| GitHub delivery | User authorized publication through [PR #6](https://github.com/Abduloxunov/mdb-vision-finals/pull/6); lead merge pending | Lead reviews/merges the local app and KB, verifies public repository/history and records submitted commit |
| Presentation | Teammates are preparing it | Include real pipeline and validation numbers with limits; export accepted deck format via the presentation owner |
| Permitted live demo media | Private CarDD QA only verified here | Use team-owned/consented car photos with faces/plates removed before public showing |
| Backup demo | Not recorded here | Record a real successful run plus the missing-context/fallback behavior |
| Final form | Not submitted | Lead fills HTTPS URL, public repo, deck and exact commit; check the official form/checklist |

No PDF was created; Markdown is the requested documentation format. The event accepts an exported deck; teammates handle that artifact.

## Suggested deadline sequence

1. Immediately rehearse the real local flow using two consent-cleared photos. Warm both models before recording. Correctly identify component; test a poor/no-detection photo without claiming it proves no damage.
2. In parallel with teammates' pitch preparation, resolve deployment and integration with the developer. Transfer source files separately from secrets/weights/private data. This chat has not sent any team message.
3. Freeze feature scope to photo localization, source evidence, cited explanation and report. Verified prices, maps, graph RAG, visual-reference search and hidden-fault diagnosis are future work in this MVP.
4. Verify the public app URL, an honest recorded fallback and the chosen final repository commit. Then submit the official form before 13:00, leaving time to reopen all links.

## Demo story the app can support

A driver shows a damaged door/window, chooses the correct component and describes what happened. CarDoctor identifies visible candidate regions, retrieves applicable published guidance and explains it with source links. It asks about facts the photo cannot establish. The user exports the report to discuss with a technician. Show source details and conditions, not just generated text.

Distinguishing claim: the pipeline includes a task-specific trained detector and explicit retrieval/context controls. It does not simply send the image to a general chat model. Its LLM receives retrieved text; the photo stays local. Do not claim “better than ChatGPT” without a comparison study.

## Pitch-safe wording

“We fine-tuned a small pretrained damage detector for 12 total epochs on 2,816 CarDD training images and selected its best checkpoint using 810 validation images. On the separate 374-image test split, mAP50 was 0.735 and mAP50-95 0.592. Crack and small-defect performance remains limited, and field reliability has not been established. We combine candidate damage boxes with scoped source retrieval and a cited language explanation.”

Describe five service entries as a contact directory, not five verified workshops. Prices and coordinates are absent. Roadworthiness, mechanical diagnosis and repair cost are not established by the photo. Dataset access/redistribution terms and native-language retrieval/automotive review remain work to resolve before broader release.
