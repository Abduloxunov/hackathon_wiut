# CarDoctor: verified Colab smoke results

Reviewed on 11 October 2026. The user completed the two-epoch Colab run and supplied its results, training log, metrics and two checkpoints. This is an engineering smoke test, not a product-quality or held-out accuracy result.

## Files verified

Both downloaded files match the SHA-256 hashes in `D:/hakathon_wiut/CHECKPOINTS.md`:

| File | Bytes | SHA-256 | Purpose |
|---|---:|---|---|
| checkpoint_best_ema.pth | 120,974,041 | d5d1d78b8cc4ef1f27497c1fb1e267de0c41e96c8ccdc7c7db1376cbf5e1c93c | Best EMA weights; verified by loading and running CPU inference |
| checkpoint_1.ckpt | 483,441,344 | 972aa2c09fe373dbfb2d2fdddc027396eaad42250740595ff8f14c15f996be3f | Full training checkpoint; hash verified, optimizer-state resumption not tested |

The EMA checkpoint identifies RF-DETR Nano with six foreground classes, 384-pixel input and epoch index 1. Its classification head has seven slots: six damage classes plus the no-object slot. Training labels follow the sorted CarDD categories: dent, scratch, crack, glass shatter, lamp broken, tire flat.

Original inputs are preserved: `D:/hakathon_wiut/results.md`, `metrics.csv`, `training.log` and both weights. No checkpoint or image was overwritten.

## Actual training measurements

The supplied log confirms CUDA training, two completed epochs and normal completion at `max_epochs=2`. The submitted result records 50.6 seconds for the training call; initial pretrained-weight download is outside that timer. The GPU model is not established by the supplied log.

| Epoch | Training loss | Validation mAP@50 | Validation mAP@50–95 |
|---|---:|---:|---:|
| 1 | 8.4556 | 0.0298 | 0.0161 |
| 2 | 7.2541 | 0.1155 | 0.0667 |

These metrics belong to the deliberately class-covered 64-training / 16-validation-image smoke subset. mAP is a detection metric, not the percentage of photos diagnosed correctly. Neither these values nor four example predictions establish generalization, per-class accuracy or useful diagnostic reliability. The official test split remains unused.

## Local prediction review

The verified EMA weights loaded successfully on CPU, without another model download. Four smoke-validation images were processed at a display threshold of 0.35. Foreground predictions down to 0.05 are retained privately for debugging. Scores are uncalibrated.

| Image | Ground-truth objects | Predictions at score ≥0.35 | Review |
|---|---:|---:|---|
| 001494.jpg | 5 | 0 | All annotated damage absent at this threshold |
| 000187.jpg | 1 | 0 | Annotated glass shatter absent at this threshold |
| 002625.jpg | 2 | 1 | Incorrect large tire-flat box over a panel annotated with dent and scratch |
| 000825.jpg | 1 | 0 | Annotated flat tire absent at this threshold |

This inspection shows the pipeline works but the smoke weights are not ready for product use. Lowering the threshold would expose many low-scoring candidates; that does not fix the demonstrated classification/localization errors.

The first local rendering attempt exposed an indexing bug: RF-DETR can return its no-object slot, class ID 6. The review script and notebook preview now exclude that slot before displaying damage labels. This fixes the preview logic without changing checkpoint weights or the recorded training metrics.

Private comparison images, prediction scores, timings and the complete visual review are in `experiments/cardoctor-colab/.runtime/smoke-review-v2/`. This ignored local folder and the images must stay out of the public repository. See its `REVIEW.md` and `prediction-audit.json` on D:.

## Next training experiment

Use Colab for a fresh full-data experiment: 2,816 training images and 810 validation images, preserving the 374-image official test split. Keep these smoke checkpoints as reproducibility artifacts. Do not silently resume the smoke optimizer/scheduler against a different dataset and schedule. Record explicitly whether a future run starts from the standard pretrained detector or warm-starts the smoke weights.

Before the longer run, inspect the scheduler-order warning in the supplied log. A CPU fallback for assignment occurred while model training used CUDA; it did not mean the whole training ran on CPU. The log also notes skipped validation-loss computation, while validation mAP was recorded. No traceback was present.

Dataset author-consent status remains unverified; explicit user-directed research use is recorded separately in the existing provenance. See [data preparation](CARDD-COLAB-PREPARATION.md) and [training notebook documentation](../experiments/cardoctor-colab/README.md).

No full-data training was started during this review. Browser control remains unavailable for launching Colab here. All new local packages, caches and review files are on D:. No paid job, API call, PDF, commit, push or message to another team member was performed.
