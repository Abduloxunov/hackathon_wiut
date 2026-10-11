# CarDoctor — MDB Vision

CarDoctor combines a trained car-damage detector with sourced automotive retrieval and optional AI explanations. Upload a photo, confirm its component and describe symptoms. The app displays candidate regions, applicable evidence, source links, questions and a downloadable Markdown assessment.

## Run the app now

From this checkout in PowerShell:

```powershell
Set-Location D:\hakathon_wiut\finals\mdb-vision-finals
.\start-app.ps1
```

Open **http://127.0.0.1:8766/**. The older visual-reference experiment uses port 8765; the new integrated app uses 8766.

The existing Python environment is `D:\hakathon_wiut\.venv`. The trained checkpoint and E5/Qdrant index are already present locally. No download is required to run this setup. First analysis loads the two models; later analyses are faster.

Optional checkpoint override:

```powershell
.\start-app.ps1 --checkpoint D:\path\checkpoint_best_ema.pth
```

Use only trusted training checkpoints. A matching `CHECKPOINTS.json`, when present, is verified before loading. Uploads accept images only.

## AI configuration

The existing ignored `.env` supplies `OPENROUTER_API_KEY`; `.env.example` is the shareable template. Gemini 2.5 Flash Lite is accessed through OpenRouter. Select “Add an AI explanation” to make one bounded request from the backend. The browser never receives the key. Only text evidence/context goes to the LLM, not the photo. Leave the option unchecked for offline evidence. A missing key, invalid answer or provider failure retains the retrieved source guidance.

## Implemented stack

| Stage | Current implementation |
|---|---|
| CV | RF-DETR Nano 1.11.2; fine-tuned on CarDD; 384-pixel model input |
| Classes | Dent, scratch, crack, glass shatter, lamp broken, tire flat |
| Applicability | Explicit component, model, propulsion, manual and boolean context checks |
| Retrieval | Pinned multilingual E5-small + local Qdrant; BM25/vector rank fusion; explicit keyword fallback |
| Evidence | 28 Markdown records, 20 sources; source locators and conditions preserved |
| Explanation | Gemini 2.5 Flash Lite through OpenRouter; bounded JSON, record/source binding checks |
| UI / server | Responsive HTML/CSS/JavaScript; Python loopback HTTP service |
| Report | Markdown downloaded by the browser |

A damage label does not identify its component, hidden cause, severity or repair price. The user confirms the component. The background class is excluded. Scores are uncalibrated. Generated explanations remain unreviewed; valid citation IDs alone do not prove factual support.

## Measured results

The current app uses the best EMA checkpoint selected at epoch 10 from a completed 12-epoch CarDD run: **2,816 training** and **810 validation** images on NVIDIA L4. Its selected-checkpoint validation mAP@50 is **0.7397** and mAP@50-95 **0.5931**. The ten-epoch continuation training call took **1505.7 seconds**, after the original two-epoch pilot took 313.9 seconds.

Both checkpoints were then tested locally on the same **374 official test images / 785 targets**, excluded from cloud training. Test mAP@50 improved **0.6630 to 0.7354**, mAP@50-95 **0.5342 to 0.5916**, and macro F1 **0.6306 to 0.7135** at confidence 0.35 / IoU 0.50. Cracks remain weak and small-object AP declined. These are damage-box metrics, not mechanical diagnosis accuracy. [Complete comparison and per-class results](docs/CARDOCTOR-MODEL-COMPARISON.md).

The current app passes twelve pipeline tests and nine real browser workflow checks with the improved checkpoint. Earlier pilot measurements on a repeated single validation image with warm CPU models and no LLM took 0.351–0.410 seconds within the server, median 0.364 seconds. A cold browser analysis including one LLM response took 22.257 seconds. This is a small local engineering check, not a throughput or production benchmark.

See [training results](docs/CARDOCTOR-HF-RESULTS.md), [app setup and API](docs/CARDOCTOR-APP-SETUP.md), and [submission readiness](docs/CARDOCTOR-SUBMISSION-READINESS.md).

## Reproduce setup on another Windows machine

The exact local package snapshot is in `requirements-app-local.txt` (Python 3.12.10). The existing repo rule targets Python 3.11; this local build has not been verified under 3.11. Use a D: virtual environment and D: caches; avoid reinstalling packages into the current working environment during the deadline.

Copy the trusted weights separately, point `--checkpoint` at them, and set the backend-only API key locally. Build the pinned text model/index with `kb/setup_vector.py` then `kb/vector_store.py ingest` following [the vector guide](kb/VECTOR-RAG.md). Query-time model downloads are disabled. This app currently runs on the prepared Windows D: environment; Linux/public hosting requires an adapter and deployment verification.

## Tests

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B -m unittest discover -s src -p 'test_*.py'
D:\hakathon_wiut\.venv\Scripts\python.exe -B -m unittest discover -s kb -p 'test_*.py'
```

`src/browser_check.cjs` uses preinstalled Chrome and Playwright with a private D: profile. Its current real-photo test uses a private validation image; do not publish that screenshot as consent-cleared demo media. Run with the bundled Node module path described in the app setup guide.

## Sources, licences and AI use

- [RF-DETR](https://github.com/roboflow/rf-detr): official Nano/core model implementation; review the exact variant's Apache-2.0 terms. CarDoctor training changes its weights, not the dataset rights.
- [CarDD](https://github.com/CarDD-USTC/CarDD): research damage data, not repair-cost or mechanical-diagnosis labels. User authorized research use; author consent/access terms are unverified. Keep data and checkpoints private pending a rights review before redistribution or commercial use.
- [Multilingual E5-small](https://huggingface.co/intfloat/multilingual-e5-small/tree/614241f622f53c4eeff9890bdc4f31cfecc418b3): pinned MIT-published model; [Qdrant client](https://github.com/qdrant/qdrant-client): Apache-2.0. Model scores are not our accuracy measurements.
- [Source register](kb/sources.md): manufacturer and repair guidance summarized with attribution and applicability. Full manuals/articles are not redistributed. Mechanic review is pending.
- Coding assistants helped research, implementation, training orchestration, testing and documentation. The runtime LLM explains retrieved text; it is not the detector. Graph RAG, VLM observations, visual-reference retrieval, confirmed prices and workshop maps are not implemented in this integrated MVP.

## Team and delivery

Davlatyor Abduloxunov: lead / final submission; Muhammadjon Xalimov: data and measurements; Bexruz Xasanov: KB, CV experiments and integrated app built here at the user's latest instruction. Presentation/demo planning continues with teammates. This local handoff does not merge another developer's branch. Development handoff is available for review in [PR #6](https://github.com/Abduloxunov/mdb-vision-finals/pull/6). Public deployment and final submission have not been performed by this chat.

Code freeze: **11 October 2026, 13:00 Asia/Tashkent**. The lead still needs the public HTTPS demo, public repository, permitted demo media, exported deck and final form submission. [Assignments](docs/tasks.md) and [official checklist](docs/submission.md) retain the team ownership/history.

## Follow-on training status

The CarDD continuation completed and its tested checkpoint is configured in the app. [Continuation controls and code](experiments/cardoctor-hf/CONTINUATION.md).

At the user's subsequent instruction, a separate two-epoch **VehiDE native seven-class pilot** was launched on Hugging Face L4. The first attempt failed before its first epoch because of corrupt JPEGs. Strict full pixel decoding found 16 corrupt photos, which were excluded; the repaired package has 11,589 train and 2,322 validation images and was uploaded and verified for a bounded retry. Its seven labels remain separate from the tested six-class CarDD app. The repaired retry is RUNNING: [Hugging Face job](https://huggingface.co/jobs/abduloxunov/6acb26e6095c57808931b22c). Reconciled completed-job durations plus its 40-minute cap give a conservative hardware estimate/cap of $1.106639 within the authorized $2 budget. No new validation result is available yet. This estimate does not establish account billing/remaining credit or storage charges.


Kaggle follow-up: [audited datasets and private Hugging Face preparation](docs/CARDOCTOR-KAGGLE-HF-PREPARATION.md). VehiDE is a separate native seven-class experiment; it does not change the current CarDD app or its metrics.

Current implementation: [photo and text symptom pipeline](docs/CARDOCTOR-PIPELINE.md), with supported-component gating, 12 pipeline checks and 9 browser checks.
