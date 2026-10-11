# VehiDE two-epoch trial: completion and evaluation

The separate seven-class [Hugging Face job](https://huggingface.co/jobs/abduloxunov/6acb26e6095c57808931b22c) completed successfully on 11 October 2026. This is a separate research trial; the production candidate in the local CarDoctor app remains the tested six-class CarDD checkpoint.

## What trained

RF-DETR Nano 1.11.2 started from its official generic pretrained weights with a new seven-class head and fresh optimizer. It ran two epochs on NVIDIA L4, BF16, 384-pixel input, batch size 2 and gradient accumulation 2, learning rate 0.0001 and seed 42. Prepared splits contain 11,589 training photos / 29,982 boxes and 2,322 validation photos / 6,030 boxes. No independent test split was supplied or uploaded.

All seven native labels are retained: `be_den`, `mat_bo_phan`, `mop_lom`, `rach`, `thung`, `tray_son`, `vo_kinh`. Their taxonomy is not the six-class CarDD schema. In particular, the app's crack and flat-tyre labels do not have a verified direct mapping. English glosses in the [dataset audit](CARDOCTOR-KAGGLE-HF-PREPARATION.md) are explicitly inferences.

The original VehiDE attempt failed on corrupt JPEG pixels. Strict full-resolution and draft RGB decoding excluded 14 invalid training photos and two validation photos, with all associated targets. Original files and split membership remain preserved; the repaired archive has SHA-256 `34403a305826df583bda7b195f1e586179b36a8178e7c41a9fcb4754a650fcce`.

## Completion evidence

HF reports COMPLETED; durable RUN-STATUS reports `completed_training: true`, exit code 0. Logs show both full 5,796-microbatch training loops and 1,161 validation batches per epoch. Saved best-EMA metadata is epoch 1 (zero-based), corresponding to human epoch 2. Saved training arguments contain all seven expected class names, batch size 2, accumulation 2 and two epochs.

Training call: 1,240.6 seconds (about 20.7 minutes). Bootstrap: 1,317.15 seconds. Reported HF total including scheduling: 1,332 seconds. These measure this run, not generic training speed.

Downloaded best EMA is 120,987,764 bytes, SHA-256 `a9c31584f8fd98656a23f317ef9e385e0d280e3525ad10b9437ebd5fe6664d6d`. Best total is 120,981,300 bytes, SHA-256 `7590e1d689b4f6d63d7cca506152bbddd14f954781baabb1d78988c120e808d6`. Both match the cloud checkpoint inventory. Weights remain in private HF storage and ignored D: runtime files, outside Git.

## Trainer-reported validation

| Human epoch | EMA mAP50 | EMA mAP50-95 | Trainer maximum macro F1 |
|---|---:|---:|---:|
| 1 | 0.3375 | 0.2148 | 0.3735 |
| 2 | 0.3843 | 0.2437 | 0.4221 |

Values come from `metrics.csv` columns `val/ema_mAP_50`, `val/ema_mAP_50_95` and `val/F1`. Trainer F1 selects the best macro F1 over 101 validation confidence thresholds from 0 to 1, as verified in RF-DETR 1.11.2 `training/callbacks/coco_eval.py`; it is not the independently measured fixed-0.35 F1 below. Validation selected the checkpoint and is not independent test evidence.

## Local evaluation protocol

`experiments/cardoctor-hf/evaluate_vehide.py` loads the verified best EMA with its saved native labels and evaluates all 2,322 original-size decoded validation photos on CPU FP32 with four Torch threads. Model and API downloads are disabled; no GPU training or paid LLM request occurs.

COCO bbox AP uses IoU 0.50:0.05:0.95, all candidate scores (prediction threshold 0), and the standard maximum of 100 detections per category per image. Background predictions are excluded. Fixed precision/recall/F1 uses confidence 0.35 and IoU 0.50, greedily matching within each image/class by descending score with one match per target. Macro F1 averages seven class F1 values; micro F1 aggregates instance counts. These are localization/class metrics rather than image accuracy or diagnosis accuracy.

The source starts annotation IDs at zero. COCOeval uses zero as an unmatched sentinel; a synthetic perfect-box check produced AP 0 with annotation ID 0 and AP 1 with ID 1. The evaluator therefore uses positive annotation identities 1..N only in its local ground-truth object. Source pixels, target boxes, image/category IDs and source annotation file are unchanged. Five evaluation regression checks pass, including native category zero, duplicate prediction, below-threshold omission, crowd rejection and COCO positive annotation identity.

## Full local validation results

| Metric | Result |
|---|---:|
| COCO mAP50 | 0.3714 |
| COCO mAP50-95 | 0.2347 |
| COCO mAP75 | 0.2368 |
| Macro F1 at confidence 0.35 / IoU 0.50 | 0.3878 |
| Micro precision | 0.5689 |
| Micro recall | 0.2464 |
| Micro F1 | 0.3439 |
| Small-object AP50-95 | 0.0238 |

At the fixed threshold: **1486 true positives, 1126 false positives, 4544 missed targets**, out of 6,030 targets.

| Native label | Targets | AP50 | AP50-95 | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| `be_den` | 458 | 0.2690 | 0.1365 | 0.4897 | 0.2074 | 0.2914 |
| `mat_bo_phan` | 448 | 0.5491 | 0.3930 | 0.6556 | 0.4844 | 0.5571 |
| `mop_lom` | 971 | 0.1709 | 0.0669 | 0.4854 | 0.1030 | 0.1699 |
| `rach` | 963 | 0.2202 | 0.1258 | 0.5166 | 0.1620 | 0.2466 |
| `thung` | 416 | 0.4151 | 0.2266 | 0.5394 | 0.4111 | 0.4666 |
| `tray_son` | 2378 | 0.2647 | 0.1462 | 0.5411 | 0.2048 | 0.2971 |
| `vo_kinh` | 396 | 0.7110 | 0.5482 | 0.7182 | 0.6566 | 0.6860 |

Annotation SHA-256: `b152fc70573b914185c493889dcaa997efc4e04472bc78b2b4610c03e8dbe666`. Image-hash inventory SHA-256: `34460081366e2fb7ba5e1c00c7831f34e2d21140bfd8f0691d0ecaba1fd64b13`. Saved predictions SHA-256: `91fbbf2367c3bd04ad1eae554b495b4e3a10f9304cd499513ad60e0d09b9f673`.

Inference and original metric computation took 874.8 seconds; the annotation-ID correction recalculated COCO metrics from the identical saved predictions in 32.8 seconds, with no repeated inference. Median single-image prediction was 0.343 seconds; this is a local CPU engineering measurement, not a service SLA.

The independent local inference path gives lower AP than the trainer: 0.3714 versus 0.3843 mAP50. This check uses CPU FP32, the public prediction API and original decoded pixels; the trainer ran GPU validation. Exact parity between those paths has not been established, and the difference must not be hidden by quoting only the higher trainer value. The zero-annotation-ID correction alone is small (about 0.00013 mAP50); it does not explain the overall gap.

This trial misses 75.4% of labelled instances at confidence 0.35. `mop_lom` recall is only 10.3%, and small-object AP is weak. Two epochs establish a working training/evaluation path, not a dependable condition-assessment model. Further training and new permission-cleared independent product photos would be needed before considering it for release.

## App decision and cost

The new checkpoint loads and predicts with the native seven labels. A separate actual-checkpoint check confirms the six-class app adapter rejects it and leaves its detector unset, preventing silent class-name corruption. Do not copy these weights over the current CarDD app checkpoint.

Completed job timings, including scheduling and independently rounding each run upward, give a conservative project hardware estimate of $0.879978, including both failed attempts. The successful VehiDE run contributes $0.306659 at the checked L4 price of $0.013333/minute. This is a hardware estimate, not an account billing or storage charge statement. The authorized hardware budget is $2; no further training was launched during this evaluation.

Reproduce locally from the repository using the prepared D: environment, private checkpoint inventory and repaired dataset:

```powershell
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/evaluate_vehide.py
D:/hakathon_wiut/.venv/Scripts/python.exe -B -m unittest discover -s experiments/cardoctor-hf -p test_evaluation.py
```

Existing completed evaluation output is preserved rather than overwritten; use `--output-dir D:/path/to/new/private-runtime` for a new full run. Canonical published evidence is this Markdown report; full prediction/metric JSON and annotation hashes remain in the ignored `.runtime/vehide-validation-evaluation/` folder. Dataset attribution and research-use restrictions remain as documented in the Kaggle audit.
