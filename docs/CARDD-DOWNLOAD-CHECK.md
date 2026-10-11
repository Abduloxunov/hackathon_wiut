# Downloaded CarDD audit

Checked locally on 2026-10-11. Original files were read without modification.

COCO root: `D:\hakathon_wiut\datasets\CarDD_release\CarDD_release\CarDD_COCO`.

| Original split | Images | Objects | Image bytes |
|---|---:|---:|---:|
| train2017 | 2816 | 6211 | 2125093417 |
| val2017 | 810 | 1744 | 618275743 |
| test2017 | 374 | 785 | 283634610 |

## Objects by class

| Class | Train | Validation | Test |
|---|---:|---:|---:|
| scratch | 2560 | 728 | 307 |
| tire flat | 225 | 62 | 32 |
| crack | 651 | 177 | 70 |
| dent | 1806 | 501 | 236 |
| lamp broken | 494 | 141 | 69 |
| glass shatter | 475 | 135 | 71 |

## Integrity checks

Structural/image issues found: **0**. Identical image files across splits: **0**.

Checked matching category schemas, image/annotation IDs, file presence, relative-path containment, Pillow image.verify integrity and annotation dimensions, finite positive bounding boxes within image bounds, and SHA-256 byte duplicates across the official splits.

No structural or image-file issues found by these checks.

## Training readiness and limits

The release uses `train2017`, `val2017`, `test2017` with `annotations/instances_*.json`. Our prepared training notebook currently expects `train`, `valid`, `test` and `_annotations.coco.json` inside each split: conversion was still required at the time of this initial audit. It has now been completed; see [the Colab preparation report](CARDD-COLAB-PREPARATION.md). The release also contains CarDD_SOD; use CarDD_COCO for the six-class detector experiment.

Preserve the official test split for final evaluation. These checks do not identify visually similar photos, multiple images of the same vehicle/scene, or group leakage. No vehicle-group metadata was supplied. No segmentation-mask evaluation, detector training or accuracy measurement was performed.

Training permission and any cloud-upload rights must be recorded from the actual access agreement. No permission confirmation was inferred from having downloaded the files. No data was uploaded, copied to C:, or included in Git.

Run the audit again with:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B experiments/cardoctor-colab/audit_original_cardd.py "D:\hakathon_wiut\datasets\CarDD_release\CarDD_release\CarDD_COCO" --output "D:\hakathon_wiut\finals\mdb-vision-finals\docs\CARDD-DOWNLOAD-CHECK.md"
```
