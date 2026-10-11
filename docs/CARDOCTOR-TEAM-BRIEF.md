# CarDoctor team brief

Prepared on 11 October 2026 from the current task board and verified local work. This is a shareable status/handoff message; it does not change assignments or approve a new shared architecture.

Team, we are building **CarDoctor**, a car-assessment assistant that combines computer vision, a sourced automotive knowledge base, retrieval and an LLM. A user provides vehicle photos, symptoms and relevant vehicle details. The system should explain visible findings, retrieve applicable guidance, cite its sources and ask about missing context. The same engine supports used-car checks, fleet triage and breakdown/accident assistance. DriveCoach and road-hole mapping are future ideas.

## How the system fits together

**Implemented MVP: photos and symptoms -> trained CV candidate boxes -> confirmed component/context -> text knowledge retrieval -> optional LLM explanation with citations and follow-up questions.**

Our current detector experiment is **RF-DETR Nano fine-tuning on CarDD** for six visible damage classes: dent, scratch, crack, shattered glass, broken lamp and flat tyre. It produces candidate labels and boxes; it cannot establish hidden mechanical faults or confirm that a car is safe to drive. The app's assigned visual-retrieval work remains part of T10. The integrated local MVP now uses this trained detector with sourced text retrieval; visual-reference retrieval remains future integration work.

For text retrieval, we have **multilingual E5 embeddings + local Qdrant + keyword/vector hybrid search**. The scoped records contain symptoms, possible causes, conditional urgency, assessment/repair type, limits and source references. The LLM is **Gemini 2.5 Flash Lite through OpenRouter**: it explains supplied evidence rather than inventing a diagnosis, price or workshop capability. Missing vehicle/manual/engine context must remain explicit.

## What is actually ready

- **CarDD:** 4,000 images and 8,740 object annotations audited; original 2,816/810/374 train/validation/test split preserved. Full converted data and a roughly 61 MB Colab ZIP are ready locally. The smoke ZIP contains 64 train and 16 validation images, with all six classes covered and no test images.
- **Training:** completed 12 total CarDD epochs on Hugging Face L4, 2,816 train / 810 validation images; best EMA selected at epoch 10 and hash-verified. Official 374-image test comparison: mAP50 0.6630 -> 0.7354; mAP50-95 0.5342 -> 0.5916; fixed-threshold macro F1 0.6306 -> 0.7135 (confidence 0.35, IoU 0.50). Improved model is live locally after 8 integration / 7 browser checks. Cracks/small defects remain weak. A separate two-epoch VehiDE seven-class pilot is running; it is not the current app detector.
- **Knowledge/RAG:** 28 sourced records, 20 sources, local E5/Qdrant hybrid retrieval and tested OpenRouter explanation. Context and source binding checks are preserved; held-out LLM factual reliability is not established.
- **App integration:** user explicitly asked this chat to complete the app while teammates prepare presentation/demo ideas. `src/app.py`, `src/pipeline.py` and `web/` now provide real photo upload, trained candidate boxes, scoped retrieval, optional Gemini explanation and MD export. Run `start-app.ps1`, open http://127.0.0.1:8766/ . Eight integration and seven real browser checks passed.
- **Delivery:** all changes remain local and unpushed as requested. Public HTTPS deployment, permitted demo photos, exported presentation and final submission still require the lead/developer. See `CARDOCTOR-APP-SETUP.md` and `CARDOCTOR-SUBMISSION-READINESS.md`.


The KB still needs automotive review, broader exact-model/manual coverage, verified local quotes and workshop coordinates/capabilities. Some Russian/Uzbek retrieval examples need further work. Dataset vehicle/incident grouping is unverified, and PIC Lab licensing-form/author-consent status has not been verified; provenance distinguishes the user's research instruction from author consent. Keep dataset/reference photos, private archives and keys out of the public repository.

## Work according to our current assignments

**Davlatyor + his developer Codex (T10):** build and deploy the shared app, including upload/context collection, visual reference retrieval, text-RAG/LLM integration and source-linked results. Define the evidence/CV interface before integrating the new helpers. Keep missing context and failed retrieval visible; show conditional findings and an evidence fallback rather than unsupported confident answers. Prioritize an end-to-end path that we can demonstrate honestly while detector training is pending.

**Muhammadjon + claude-2 (T11/T14):** collect and label consented reference and evaluation photos, recording source rights, vehicle/incident groups and relevant context such as engine/key-on state. Keep held-out evaluation photos out of the reference library. After app integration, measure retrieval top-1/top-3, latency and failures on the separate test set; publish actual measurements and examples in `docs/results.md`.

**Bexruz + Codex (T13, supporting T12):** maintain and expand the sourced KB, evaluate scoped retrieval and grounded explanations, prepare the CV training experiment and hand over the resulting artifacts. The immediate training step is the Colab smoke run; inspect its predictions before a larger full-training experiment. Research verified prices/provider details without filling unknown fields with guesses, and provide documented evidence/results for the pitch.

**Davlatyor + claude-1 (lead/T12/T4):** review the method and interfaces, prepare the seven-minute pitch and demo backup, coordinate merges and complete deployment/submission checks. The pitch should clearly distinguish implemented features, local experiments, measured results and future work.

## Immediate coordination

Work within the existing file ownership: developer in `src/`/`web/`, knowledge work in `kb/`, data/evaluation in assigned files and pitch with its owner. Agree the input/evidence/output interface before parallel integration. Keep keys in local environment configuration, share model/checkpoint artifacts through an authorized private channel, and use the lead's merge process. No automated test count or small class-covered smoke result should be presented as detector accuracy.

The next shared milestone is one real photo/symptom flowing through the app to applicable source-linked guidance, plus a completed, honestly recorded detector smoke run.

## Local handoff references

- [Current assignments](tasks.md)
- [Colab preparation results](CARDD-COLAB-PREPARATION.md)
- [Complete notebook instructions and source](../experiments/cardoctor-colab/README.md)
- [Knowledge-base guide](../kb/README.md)
- [Vector retrieval](../kb/VECTOR-RAG.md)
- [OpenRouter adapter](../kb/OPENROUTER.md)
- [Actual LLM checks and remaining issues](../kb/OPENROUTER-RESULTS.md)
- [KB coverage gaps](../kb/COVERAGE.md)
