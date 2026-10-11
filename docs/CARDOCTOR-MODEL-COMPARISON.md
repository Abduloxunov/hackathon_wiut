# CarDoctor: pilot versus completed continuation

The user requested testing the completed CarDD model before training a new dataset. VehiDE inputs are uploaded privately, but no VehiDE training job is running.

## Checkpoints and fixed evaluation

The two-epoch pilot and the validation-selected continuation EMA checkpoints are evaluated on the same complete official CarDD test split: 374 images and 785 labelled damage instances. Cloud jobs did not contain this split. Six classes and their saved checkpoint order are verified before inference; model IDs 0-5 map to original COCO IDs 1-6. The background output is discarded.

Checkpoint selection used validation mAP50-95, before looking at the official test scores. The continuation ran to 12 total epochs; the best EMA checkpoint was selected at epoch 10. Final-epoch weights are not automatically the best weights.

The local evaluation uses CPU FP32, four Torch threads, RF-DETR 1.11.2, original decoded image sizes, and no LLM calls or model downloads. The [COCO evaluator](https://github.com/ppwwyyxx/cocoapi) is pinned as pycocotools 2.0.11. Detection AP uses all model predictions with threshold 0, the standard IoU thresholds 0.50-0.95 and max 100 detections per category. It reports no classification-style image accuracy.

Precision, recall and F1 are also computed at the fixed confidence threshold 0.35 and IoU 0.50 using score-ordered one-to-one matching within each image/class. Micro scores aggregate instances; macro F1 gives each class equal weight. These fixed-threshold results differ from the trainer's confidence-optimized macro F1. They evaluate detections, not the LLM, repair diagnosis or the full app's photo-resizing/output-cap policy.

## Actual result

Both complete evaluations passed. **Keep the improved CarDD checkpoint for the current app/submission; no new dataset training is needed before the demo.**

| Metric | Two-epoch pilot | Best continuation | Change in percentage points |
|---|---:|---:|---:|
| mAP50 | 66.30% | 73.54% | +7.24 |
| mAP50-95 | 53.42% | 59.16% | +5.74 |
| Macro F1 | 63.06% | 71.35% | +8.29 |
| Micro F1 | 57.80% | 64.19% | +6.40 |
| Micro precision | 63.37% | 64.44% | +1.07 |
| Micro recall | 53.12% | 63.95% | +10.83 |

F1/precision/recall rows use confidence 0.35 and IoU 0.50. mAP uses all confidences and standard COCO matching.

| Class | Pilot AP50 | Improved AP50 | Pilot fixed-threshold F1 | Improved fixed-threshold F1 | Test instances |
|---|---:|---:|---:|---:|---:|
| dent | 49.06% | 59.48% | 51.33% | 58.46% | 236 |
| scratch | 55.68% | 62.73% | 53.53% | 60.06% | 307 |
| crack | 30.08% | 38.94% | 30.77% | 39.06% | 70 |
| glass shatter | 97.52% | 98.85% | 89.80% | 93.71% | 71 |
| lamp broken | 75.39% | 85.82% | 65.85% | 81.75% | 69 |
| tire flat | 90.04% | 95.42% | 87.10% | 95.08% | 32 |

All six class AP50 and F1 scores increased. The improved model found 502 of 785 targets at the fixed threshold, versus 417 previously. It also produced more false positives overall: 277 versus 241. Aggregate precision improved slightly, but dent/scratch/crack precision decreased while their recall increased. Do not claim every metric improved.

Cracks remain weak: precision 43.10%, recall 35.71%, F1 39.06%. Small-object COCO AP50-95 decreased from 19.20% to 11.57%; medium-object AP increased from 26.98% to 28.67% and large-object AP from 52.88% to 59.98%. Overall gains do not establish reliable detection of tiny defects. Area figures are stored in the raw metrics JSON after evaluator-only recomputation from the saved predictions; inference was not repeated.

No threshold tuning was performed against the test set. These are point estimates on one dataset, not statistical significance or real-world diagnostic accuracy. Glass shatter and flat tires are strongest; fine cracks and detailed surface defects need further data/error review. The test set was used for this comparison, so future model development needs a new untouched evaluation set.

Pilot checkpoint SHA-256: `fbae8f302223f484e8b6148492e7a251f0ae6f75ec487f48f498b1c2083d0397`.

Improved checkpoint SHA-256: `3b2addfe24b78c764d9f5758c74f0d3f8e0ecb646c21294fa39c968d811938b4`.

Test annotation SHA-256: `130cde81a32820cd83091e78bdbce236753c7675306da004b88bf54bad130a71`.

Both runs used identical image hash inventory: `1315d3ad81f0b13630135ed271b378647111118f70d0ffec6d5cca3561621a1d`.


## Reproduction and private evidence

```powershell
# Run from D:/hakathon_wiut/finals/mdb-vision-finals:
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/evaluate_cardd.py --tag pilot --checkpoint experiments/cardoctor-hf/.runtime/downloaded-output-attempt-2/checkpoint_best_ema.pth
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/evaluate_cardd.py --tag continuation --checkpoint experiments/cardoctor-hf/.runtime/downloaded-continuation-12/checkpoint_best_ema.pth
```

Additional evaluator dependency: `experiments/cardoctor-hf/requirements-evaluation-local.txt`. Install/download caches and temporary files must stay on D:. The existing local inference dependencies remain in place.

Raw evidence is ignored/private: `experiments/cardoctor-hf/.runtime/test-comparison/{pilot,continuation}-metrics.json` and corresponding prediction JSON. Results record checkpoint SHA, annotation SHA and a hash inventory for every test image, evaluator versions and thresholds. Do not publish private test photos or treat dataset test scores as proven field reliability. Byte-duplicate checks do not establish vehicle/incident independence; no near-duplicate grouping claim is made.

Future training after repeatedly reviewing this test set requires a fresh untouched evaluation set. Do not tune confidence thresholds against these test outcomes and then call them an independent final result.


## App verification after replacement

The local app at http://127.0.0.1:8766 now defaults to the improved validation-selected checkpoint. All 8 integration tests and 7 real browser workflow checks passed after replacement. The browser-exported Markdown report contains the improved checkpoint SHA, confirming that the live server loaded the new file. The workflow exercised a real photo, retrieval/source links, export and 390-pixel mobile layout with no paid LLM call. The six-label adapter now rejects checkpoints with a different saved class order. VehiDE seven-class weights cannot silently enter this adapter.
