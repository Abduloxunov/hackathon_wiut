# Hugging Face full-data pilot results

Historical pilot record. The later 12-epoch continuation completed, and the app now uses its validation-selected checkpoint. Both were tested on the official test split; see [current comparison](CARDOCTOR-MODEL-COMPARISON.md) and [continuation completion](../experiments/cardoctor-hf/CONTINUATION.md).

Verified 11 October 2026, Asia/Tashkent. Completed job: https://huggingface.co/jobs/abduloxunov/6acb137b095c57808931ad0d . The older job ending `7019128b` failed before its first training batch because the runtime image lacked a C compiler; its logs/source remain preserved.

## Data and training

2,816 train and 810 validation images, original CarDD split and six categories. No official test images were uploaded in the training archive. Original test count: 374. Archive SHA-256: `af1d7c23552168128d8e242249de5f06d07deedd351c71bb0a20082cd43170ff`.

RF-DETR Nano 1.11.2, official pretrained initialization, two epochs, 384-pixel input, batch 2, accumulation 2, LR 1e-4, seed 42, BF16 on NVIDIA L4. CUDA assignment preflight passed after installing GCC in the cloud container. No smoke optimizer was resumed. All five checkpoint byte counts and SHA-256 hashes matched the downloaded files on D:.

Training call: 313.9 seconds (5 min 14 s). Bootstrap elapsed: 389.12 seconds (6 min 29 s), excluding scheduling and local archive upload/download. Fast completion comes from a small pretrained model, modest input resolution and only two epochs; it is not evidence of convergence.

## Actual validation metrics

| Epoch (human numbering) | mAP@50 | mAP@50–95 | mAP@75 |
|---|---:|---:|---:|
| 1 | 0.584400 | 0.480928 | 0.496490 |
| 2 | 0.663052 | 0.538297 | 0.552045 |

Raw source: `experiments/cardoctor-hf/.runtime/downloaded-output-attempt-2/metrics.csv`; final logged overall table agrees. mAP aggregates detection performance over classes/IoU thresholds, not the fraction of photographs diagnosed correctly. Validation was used for checkpoint selection; it is not a held-out final test result. Per-class/domain performance and calibration remain unverified. Vehicle grouping and near-duplicate leakage have not been established; earlier exact-image duplicate audit passed.

## Selected checkpoint

`checkpoint_best_ema.pth`, 120,973,364 bytes.

SHA-256: `fbae8f302223f484e8b6148492e7a251f0ae6f75ec487f48f498b1c2083d0397`.

The app originally defaulted to this pilot checkpoint; it is retained for rollback. Other outputs are two optimizer checkpoints, best-total weights and last EMA weights, plus training config, provenance, data audit, environment, GPU/matcher checks and logs. They are private ignored runtime files, not Git assets.

## Real app inference check

Private validation image `000187.jpg` produced a glass-shatter candidate with score 0.959 and box `[270.6, 227.5, 826.4, 619.5]`. Its selected component was subsequently corrected to `side_window` in the HTTP checks; scoped retrieval returned K008. This is one qualitative integration example, not accuracy validation. The image is private QA material, not an authorized public demo photo.

Three warm HTTP analyses of this same image with E5/Qdrant retrieval and no LLM took 0.364, 0.410 and 0.351 server seconds; median 0.364. They exclude upload transfer/browser rendering and are not a broad latency benchmark. The earlier cold browser workflow with one OpenRouter explanation took 22.257 server seconds, including model initialization and the LLM. Conditions differ; do not present these as comparable steady-state benchmarks.

## Cost and remaining work

The job is completed; no additional GPU training run was started. The submitted 75-minute hardware limit plus conservative failed-attempt estimate stayed below the user's $2 cap. Actual billed credits have not been audited; configured caps and wall-clock estimates are not a billing statement.

Next: review diverse permission-cleared photos and per-class errors; establish final test evaluation and vehicle grouping; evaluate text retrieval/LLM factual support independently. Preserve this successful checkpoint and focus the deadline effort on an honest working demo rather than another unmeasured training run.
