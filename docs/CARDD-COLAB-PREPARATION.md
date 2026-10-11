# Colab-ready CarDD preparation

Prepared locally on 2026-10-11. No GPU training or cloud upload occurred.

Original COCO root: `D:\hakathon_wiut\datasets\CarDD_release\CarDD_release\CarDD_COCO`.
Converted full dataset: `D:\hakathon_wiut\datasets\cardoctor-cardd-coco`.
Smoke upload ZIP: `D:\hakathon_wiut\datasets\cardoctor-cardd-smoke.zip`.

## Format and preservation

Original splits and annotations are preserved: train2017 -> train, val2017 -> valid, test2017 -> test. JSON files are renamed to `_annotations.coco.json` without changing IDs, categories, boxes, area, masks or split membership. Original source files were not overwritten.
Full converted images use same-volume hardlinks; never edit linked image bytes. Smoke images are separate copies. Do not overwrite hardlinked full-dataset image bytes.

## Actual subset

| Split | Full images | Full objects | Smoke images | Smoke objects |
|---|---:|---:|---:|---:|
| train | 2816 | 6211 | 64 | 141 |
| valid | 810 | 1744 | 16 | 41 |
| test | 374 | 785 | 0 | 0 |

The seed is 42. Selection ensures at least two training images and one validation image containing each of the six classes before filling the 64/16 limits. This deliberately covered subset is a pipeline test, not a representative accuracy evaluation. No test photos are packaged.

Smoke object counts:

| Class | Train objects | Validation objects |
|---|---:|---:|
| dent | 52 | 13 |
| scratch | 33 | 14 |
| crack | 16 | 4 |
| glass shatter | 16 | 2 |
| lamp broken | 11 | 4 |
| tire flat | 13 | 4 |

## Archive verification

Size: **61,212,543 bytes**. SHA-256: `7d5b6b628fe7af5e6da1458b727d49df080a26e4abc211cc677f9fe4e19dfa68`. ZIP CRC verification passed. Archive entries contain only train/valid images and annotations plus provenance/smoke-origin metadata.

## Authorization and evaluation limits

The user explicitly directed research use. `user_authorized_research_use` is true; `permission_confirmed` remains false, and PIC Lab author-consent/licensing-form status remains unverified. These fields distinguish user instruction from documented author consent. The source terms are linked from the training guide; no commercial or redistribution rights are asserted.
Not verified: exact-duplicate checks do not prove vehicle/incident independence.
All full/converted files passed the existing data audit. Smoke data passed the same image, box, schema and exact-leakage checks. No trained detector, mAP score, GPU allocation or reliability claim is reported.

## Next action

Upload `cardoctor_rfdetr_nano_smoke.ipynb` to Colab, select a GPU runtime and run its cells. At the upload prompt, select the smoke ZIP above. The notebook detects the already-prepared subset and uses it directly. It saves checkpoints/logs to your Drive after your interactive Google authorization, then offers an artifact ZIP for download. Keep downloaded files on D:.
