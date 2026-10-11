# CarDoctor app setup and integration

Verified on the prepared Windows D: environment on 11 October 2026. This is the working app built following the user's explicit direction to complete the app here while teammates handle presentation/demo planning. Existing task ownership remains in the task board; coordinate this local implementation with the lead's developer before merging another branch.

## Start and use

```powershell
Set-Location D:\hakathon_wiut\finals\mdb-vision-finals
.\start-app.ps1
```

Open http://127.0.0.1:8766/ . Upload JPEG/PNG/WebP under 8 MB, choose the actual affected component, add symptoms and analyze. For glass in a door, choose Side window; a glass-shatter category alone does not establish windshield versus side window. The page displays candidate boxes/scores, sources and exact applicability conditions. Enable the AI explanation only when needed; it makes one bounded backend request. Download the assessment as Markdown.

The current running server was launched by this chat. If port 8766 is occupied by that server, use the existing tab; do not start a second copy. A second app process sharing the local Qdrant directory can encounter its exclusive lock. The older experimental visual-reference app remains separate on port 8765.

## Runtime configuration

- Python: `D:\hakathon_wiut\.venv\Scripts\python.exe` (3.12.10).
- Default weights: `experiments/cardoctor-hf/.runtime/downloaded-continuation-12/checkpoint_best_ema.pth`.
- Override: `--checkpoint D:\path\trusted-weights.pth`, or environment `CARDOCTOR_CHECKPOINT` before starting.
- E5/Qdrant/cache/temp: `kb/.runtime/`, all on D:. Override `CARDOCTOR_KB_RUNTIME` with a prepared D: index.
- OpenRouter: ignored root `.env`, using `.env.example`; key remains backend-only.
- Local port override: `--port 8767`.
- Photos are decoded in memory, EXIF orientation applied, metadata omitted from the returned preview. This app does not store uploaded photos or assessments on the server. The browser chooses where downloaded MD reports are saved.
- No model/image download occurs at analysis time. Startup needs local trained weights and the pinned embedding index. If vector setup is unavailable, the response explicitly names sourced keyword fallback.

## Local API

`GET /api/health`: checkpoint availability, name and transient request token. No credential is returned.

`POST /api/analyze`: JSON with `X-CarDoctor-Token` from the same local server; host restricted to localhost/127.0.0.1 at the selected port. No CORS is enabled.

```json
{
  "image": "data:image/jpeg;base64,<encoded JPEG>",
  "query": "shattered side window glass",
  "part": "side_window",
  "vehicle": "",
  "propulsion": "",
  "confirmed_manual": "",
  "context": {},
  "threshold": 0.35,
  "retriever": "hybrid",
  "use_llm": false
}
```

`context` accepts only boolean `engine_running` and `parking_brake_released`. A vehicle model name does not confirm a manual's year/variant. Damage threshold range is 0.1–0.9. Files are limited to 8 MB and 24 million pixels, with a 2,000-pixel maximum preview side. Detector input is internally 384 pixels. A single analysis lock protects CPU/index use; overlapping requests return 429.

Responses include detections, preview dimensions/image, routed compatible CV label, retrieval bundle, optional explanation, source records, timing, model SHA-256, warnings and Markdown report. The highest-scoring compatible category routes retrieval; all valid candidate boxes are shown. Class 6 is background and excluded. Component selection is explicit. Incompatible CV categories do not overwrite the component; guidance can still retrieve from the user's symptom text.

An explanation request is skipped for missing context/no evidence. Citation IDs must belong to the retrieved record and bound source. Unavailable/invalid LLM output returns deterministic evidence, with no automatic paid retry. Conditions and limits remain visible outside generated prose.

## Verification

Eight pipeline tests pass: background filtering/class routing, component mismatch, no paid request with missing context, corrupt-image rejection, typed context/threshold checks, vector fallback, no-detection wording and concurrent-request rejection.

Seven real browser checks passed: initial health, real trained-model photo detection, real hybrid evidence/source links, one live OpenRouter response, MD download, 390px mobile layout and no JavaScript errors. The browser's first test used a windshield selection for a side-window photo; subsequent real HTTP checks correctly selected Side window and retrieved K008. This illustrates why component confirmation matters.

Real HTTP checks also rejected a missing anti-CSRF token (403) and invalid Host (400). Three warm no-LLM requests were measured; see the HF results guide. Private QA screenshots/reports are under `kb/.runtime/app-browser-check` and `kb/.runtime/app-check`.

Browser test command, using installed packages and no downloads:

```powershell
$env:NODE_PATH='C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
node src/browser_check.cjs
```

The browser script now defaults to offline evidence. Set `CARDOCTOR_TEST_LLM=1` only for an intentional paid live explanation check. The earlier live explanation test already passed. It uses private validation media; do not publish its screenshots as permission-cleared demo assets. Check source/component applicability when rehearsing.

## Deployment boundary

This server listens on loopback and is not a public HTTPS deployment. The current runtime enforces D: paths on Windows. A cloud/Linux runtime adapter, production server/gateway, secret injection, model/index provisioning and external URL checks are still needed for public hosting. The local anti-CSRF token is not user authentication or a public paid-call quota. Do not claim deployment is finished from the local link.

Nothing has been committed or pushed. The source changes are local and reviewable. Keep `.env`, private datasets, `.runtime`, weights and QA photos out of Git. Public weight/data redistribution rights are not established by a successful training run.


Current default was tested on all 374 official test images and passed 8 integration / 7 real browser checks after replacement. [Results and limitations](CARDOCTOR-MODEL-COMPARISON.md). Pilot weights remain preserved in `downloaded-output-attempt-2/` for rollback. Native VehiDE seven-class checkpoints are a separate experiment and are rejected by this app adapter.

## Pipeline update

Photo or text symptoms are now accepted. The visual model is skipped for unsupported components and text-only checks, with explicit status. Reports include context, warning provenance and stage timings; source cards include repair-assessment text and follow-up questions. See [the current pipeline](CARDOCTOR-PIPELINE.md). Verification: 12 pipeline tests and 9 real browser checks passed; no paid LLM call was needed for these checks.
