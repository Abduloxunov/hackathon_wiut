# CarDoctor: audited Kaggle datasets and Hugging Face preparation

Status: preparation completed on 11 October 2026. The CarDD continuation was tested first. At the user's subsequent request, a separate VehiDE pilot was submitted; see the latest run status below. Preparation/upload code itself cannot launch a GPU job.

## Decision

Use **VehiDE as a separate seven-class damage-detection experiment**. Keep the current six-class CarDD detector for the submission until any replacement has been trained, evaluated and integrated. More images alone do not establish higher accuracy.

Keep **Humans in the Loop Car Parts and Car Damages** as the next candidate for a separate part detector. That could help associate visible damage with a door, bumper, lamp or window and improve knowledge-base routing. Its archive folder names are reversed relative to their annotation content; conversion must inspect classes, not infer the task from a folder name.

Do not spend time training on the tiny COCO dataset as the main accuracy upgrade. It is useful for checking a converter, not evidence of broad coverage.

## What was actually inspected

Public Kaggle metadata, the complete ZIP member lists, both VehiDE global annotation files, both Humans in the Loop class-definition files and one annotation from each subset, and all four small COCO annotation files were downloaded and parsed. These artifacts are on `D:/hakathon_wiut/datasets/kaggle-audit/`. Only the full VehiDE image archive was selected for download/conversion.

| Dataset | Audited content | Use in CarDoctor | Limitations |
|---|---|---|---|
| [VehiDE](https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection) | 13,945 JPEGs; 11,621 train / 2,324 validation; 36,081 polygon regions; 7 observed labels | Separate RF-DETR damage experiment | Different taxonomy from CarDD; no supplied test annotations, no damage-free images in the supplied annotation dictionaries |
| [Humans in the Loop](https://www.kaggle.com/datasets/humansintheloop/car-parts-and-car-damages) | 998 part-annotation files, 814 damage-annotation files; 21 part classes and 8 damage classes in metadata | Future part detector and damage expansion | Full annotation/image audit and conversion not performed; subsets are separate; masks/images are alternate representations, not additional independent examples |
| [Small COCO dataset](https://www.kaggle.com/datasets/lplenka/coco-car-damage-detection-dataset) | 59 annotated train images, 11 annotated validation images, 8 test JPEGs; generic damage or 5 part classes | Small format/conversion fixture | ZIP has 70 images in `img/`, copied images under train/val, and 8 test photos. Do not sum these as independent images; test annotations were absent |

The VehiDE source ZIP is 2,250,947,669 bytes; SHA-256:

```text
1e5fcf602cca8ccb532dee7b042c1c3c592076eb264b386918360e033d96a98a
```

## VehiDE native class counts before conversion

| Stable class ID | Native annotation label | Train regions | Validation regions |
|---|---|---:|---:|
| 0 | `be_den` | 2,324 | 458 |
| 1 | `mat_bo_phan` | 2,370 | 448 |
| 2 | `mop_lom` | 4,709 | 972 |
| 3 | `rach` | 4,546 | 963 |
| 4 | `thung` | 2,006 | 417 |
| 5 | `tray_son` | 12,267 | 2,380 |
| 6 | `vo_kinh` | 1,824 | 397 |
| Total | | 30,046 | 6,035 |

English glosses inferred from Vietnamese labels and the paper are broken lights, missing parts, dents, torn material, holes/punctures, scratched paint, and broken glass respectively. These glosses are for understanding; the training package preserves the native names and applies **no automatic CarDD class mapping**. A hole is not necessarily a tire puncture. Torn material is not an independently labelled crack class.

The [authors' paper](https://www.researchgate.net/profile/Hien-Nguyen-61/publication/375429192_VehiDE_Dataset_New_dataset_for_Automatic_vehicle_damage_detection_in_Car_insurance/links/65aa3ba7a59bf45fc9d940e2/VehiDE-Dataset-New-dataset-for-Automatic-vehicle-damage-detection-in-Car-insurance.pdf) describes eight categories, including non-damage. The actual downloaded dictionaries have seven labels, and every image has at least one region. The package follows those observed annotations rather than manufacturing an eighth class.

## Conversion and leakage controls

`experiments/cardoctor-hf/prepare_vehide.py` verifies the source archive hash and size, inspects ZIP paths before extraction, rejects symlinks/duplicate member names and limits extraction size. The original conversion checked JPEG structure and dimensions, but did not fully decode pixels. This missed corrupt files and caused the first GPU attempt to fail. The converter now strictly decodes full RGB pixels plus JPEG draft decoding at 384 and 1333, excluding invalid images.

The converter takes the bounding envelope of each polygon, clips it to image dimensions and discards empty/degenerate boxes. The raw annotation scan found 538 regions with negative coordinates and one zero-width/height envelope; the final audit also counts clipping at right/bottom borders. This package is for object detection. It preserves the original raw polygons in the source archive, but does not claim to provide segmentation masks in the COCO training package.

It retains the publisher's train/validation assignments, processes validation first, and excludes repeated byte-identical images rather than allowing duplicate photos across splits. It also excludes exact matches against the local CarDD validation and test files so future use does not contaminate those evaluation sets. All exclusions are recorded in `DATA-AUDIT.json`. It does not prove that visually similar photos or the same vehicle/incident are independent. No synthetic negatives or LLM-generated labels are introduced.

Prepared folder: `D:/hakathon_wiut/datasets/kaggle-audit/vehide-rfdetr-native7/`.

```text
vehide-rfdetr-native7/
  train/
    _annotations.coco.json
    *.jpg
  valid/
    _annotations.coco.json
    *.jpg
  provenance.json
  DATA-AUDIT.json
```

Prepared ZIP: `D:/hakathon_wiut/datasets/kaggle-audit/vehide-native7-train-valid.zip`.
Package receipt: `D:/hakathon_wiut/datasets/kaggle-audit/VEHIDE-PACKAGE.json`.
Local Hugging Face input stage: `experiments/cardoctor-hf/.runtime/vehide-input/`.
All caches, temporary files, data and weights remain on D:. Local image hard links reduce duplicate disk usage; they must not be edited in place.

## Hugging Face configuration

The prepared worker uses RF-DETR Nano 1.11.2 with official pretrained generic weights and a new seven-class head. It does not resume a six-class CarDD optimizer/checkpoint. The intended first experiment is 2 epochs, 384-pixel resolution, batch 2 with gradient accumulation 2, learning rate 1e-4, seed 42, and BF16 on an L4 GPU. Per-class validation metrics and checkpoints are enabled; the official test data is absent.

Dependencies use the previously working PyTorch 2.6.0 / CUDA 12.4 image and pinned remote requirements. Bootstrap installs GCC if needed, checks CUDA/BF16 and the actual CUDA assignment backend, verifies dataset/code hashes and writes durable logs/checkpoints. Job timeout must be 40 minutes; bootstrap limits the worker to at most 35 minutes within that envelope. Actual startup/training time on this larger dataset has not been measured.

Sources:

- `kaggle_prepare.py`: bounded HTTP-range archive inspection and resumable D: download.
- `prepare_vehide.py`: conversion, image checks, duplicate removal and package receipt.
- `hf_vehide.py`: idempotent local staging and private bucket upload verification. **It cannot launch a job.**
- `vehide-worker.py`: seven-class GPU training entry point, staged as `worker.py`.
- `vehide-bootstrap.py`: Linux dependency/bootstrap entry point, staged as `bootstrap.py`.
- `requirements-remote.txt`: pinned remote dependencies.

From `D:/hakathon_wiut/finals/mdb-vision-finals`:

```powershell
# Inspect metadata/annotations without downloading all image archives:
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/kaggle_prepare.py

# Source download can resume an interrupted .part file:
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/kaggle_prepare.py download vehide

# Conversion writes a fresh output and preserves any existing prepared dataset:
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/prepare_vehide.py

# Stage or upload into the existing private bucket; neither command starts GPU billing:
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/hf_vehide.py stage
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/hf_vehide.py upload
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/hf_vehide.py status
```

After a completed upload, `.runtime/VEHIDE-UPLOAD.json` records the private bucket and immutable input prefix. A future job must mount that prefix read-only at `/input`, a fresh output prefix read/write at `/output`, and execute `python -u /input/bootstrap.py` in `pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime`. Do not reuse the CarDD output directory.

The authorized budget is $2. Existing jobs have a conservative reserved hardware cap of $1.573294. Another 40-minute L4 reservation at the previously checked price would be $0.53332 and exceed that cap. No additional GPU job is started here. Before any new launch, reconcile completed-job usage, current prices and remaining account credit; otherwise request a changed budget. Upload/preparation does not establish that compute credit remains.

## What changes in the app after a successful experiment

A new model must first pass a real validation comparison and visual error review. Its class order must come from the saved manifest, and the background output must be filtered. The current app has a six-label CarDD adapter; loading this seven-label model without adapting that code would mislabel predictions.

Review native-to-product label mappings separately. Add missing parts, torn material and holes as explicit supported findings before exposing them to the knowledge-base retriever. Keep source-grounded guidance and user-confirmed part selection; the damage model alone does not tell us which component is affected. A part detector is a separate follow-up experiment.

Measure per-class mAP50, mAP50:95, precision/recall and F1 with the confidence/IoU definitions recorded. VehiDE validation scores cannot be directly compared with CarDD scores on different images and label definitions. A changed model is only an improvement for CarDoctor after evaluation on a fixed, uncontaminated product-relevant set. This preparation provides no new accuracy claim.

## Provenance and licences

Kaggle metadata lists VehiDE as Apache 2.0. The original authors state that image copyright belongs to the original providers and restrict their intended use to non-commercial research/education. The preparation records both statements and keeps the dataset private; it does not treat the listing as permission to redistribute or commercially use the source photos. See the linked authors' paper above.

Humans in the Loop and the small COCO listing declare CC0. The inspected metadata and annotation files are retained as evidence of the particular releases checked. The full Humans in the Loop archive was not downloaded or converted. Its `Car damages dataset` folder actually contains the 21 part classes, while `Car parts dataset` contains the 8 damage classes: Missing part, Broken part, Scratch, Cracked, Dent, Flaking, Paint chip and Corrosion.

The [official Kaggle CLI documentation](https://github.com/Kaggle/kaggle-cli/blob/main/docs/datasets.md) documents file listing and specific-file downloads. No Kaggle login, GPU session, or paid Kaggle resource was started. No data, weights, secrets or code were pushed to GitHub.

## Original preparation results (version 1; superseded by pixel repair)

Local conversion completed and independently checked:

| Split | Images retained | Regions retained | Boxes clipped | Duplicate photos removed | Degenerate regions removed |
|---|---:|---:|---:|---:|---:|
| Train | 11,603 | 30,009 | 1,292 | 18 | 2 |
| Validation | 2,324 | 6,035 | 296 | 0 | 0 |

No exact overlap was found against 1,184 distinct local CarDD validation/test image hashes. All prepared COCO image/annotation references, category IDs, category order and box bounds passed an independent check. Geometry checks covered clipping and degenerate polygons; ZIP path checks covered traversal and Windows absolute paths. These are preparation checks, not GPU-training or model-accuracy results.

The 2,310,391,381-byte prepared ZIP passed a full CRC scan (13,931 unique members, no test split). SHA-256: `9a7d1bfe1fbfa176c38db9c8a319dd2bf05c371d5787ab0eea8f76bf17754d97`.

Private Hugging Face upload **completed**: six input files, 2,310,414,494 remote bytes, inventory/sizes verified and the downloaded remote manifest hash matched the local manifest. Bucket: `abduloxunov/cardoctor-fullpilot-20261011t031655z`; input prefix: `vehide-native7-input-9a7d1bfe1fbf`. The worker rechecks the complete archive SHA before any future training. At this preparation checkpoint, no VehiDE GPU job had been launched.

The user subsequently requested testing the completed CarDD continuation before training another model. That comparison was completed before the subsequent dataset run below.


## Subsequent user-requested VehiDE run

After the completed CarDD comparison passed and the app was updated/verified, the user explicitly requested another dataset run. [VehiDE Hugging Face job](https://huggingface.co/jobs/abduloxunov/6acb23e3fee2c9007019213c) finished with **ERROR**. Bootstrap reached training after 42.44 seconds and the CUDA matcher check passed, but PIL raised `OSError: broken data stream when reading image file` during the first epoch. No completed epoch or validation score was obtained. This was an image-decoding failure, not a successful training result.

`launch_vehide.py` rechecked the three completed jobs' reported timestamps/durations and the current L4 price ($0.013333 per minute). Each completed job's total time, including scheduling, was rounded up independently: 3 + 9 + 28 = 40 minutes, a conservative hardware estimate of $0.53332. A new 40-minute cap is $0.53332; combined $1.06664 stays within the $2 project hardware budget. This replaces the earlier reserved-cap calculation after actual completion timestamps became available. It is not a billing statement or an account-credit/storage-cost audit.

The launcher verified completed same-test evaluations before submission, preserves immutable private input and separate output prefixes, records submission state to prevent duplicate paid jobs, and performs no automatic paid retry. The app stays on the tested six-class CarDD checkpoint. Seven-class metrics from this new dataset cannot be directly compared with six-class CarDD scores.

Commands: `launch_vehide.py status`, `monitor`, `download`, or `cancel`, using the prepared D: Python executable. Private state: `.runtime/VEHIDE-JOB.json`; budget evidence: `.runtime/VEHIDE-BUDGET.json`; preserved failure logs: `.runtime/downloaded-vehide-native7/`.


## Strict pixel repair and version 2

`repair_vehide.py` decoded all 13,927 version-1 photos at full RGB resolution and JPEG draft sizes 384 and 1333 with truncated-image tolerance disabled. It found 14 invalid training images and 2 invalid validation images. Their bytes and failure messages were recorded in the private `VEHIDE-PIXEL-AUDIT.json`; all targets belonging to those photos were excluded. Original files, split membership, valid image IDs and class labels are preserved.

| Repaired split | Images | Regions | Corrupt photos excluded |
|---|---:|---:|---:|
| Train | 11,589 | 29,982 | 14 |
| Validation | 2,322 | 6,030 | 2 |

Independent checks passed for exact retained split membership, unique IDs, seven native categories, image/target references, and finite in-bounds boxes. The fresh ZIP passed a complete CRC scan. It is 2,308,223,264 bytes; SHA-256 `34403a305826df583bda7b195f1e586179b36a8178e7c41a9fcb4754a650fcce`. No truncated-file tolerance or synthetic repair was used.

Version-2 private upload completed: all six remote files/sizes and downloaded manifest SHA verified (2,308,251,504 remote bytes). `hf_vehide_v2.py` stages/uploads the immutable repaired data and unchanged cloud training code. `launch_vehide_v2.py` includes the failed first VehiDE attempt in finished-job budget reconciliation, then permits one controlled two-epoch L4 retry with a 40-minute cap and prevents duplicate paid submission. The app continues to use the tested CarDD checkpoint.

```powershell
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/hf_vehide_v2.py upload
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/launch_vehide_v2.py preflight
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/launch_vehide_v2.py launch
D:/hakathon_wiut/.venv/Scripts/python.exe -B experiments/cardoctor-hf/launch_vehide_v2.py status
```

Private state is `.runtime/VEHIDE-JOB-V2.json`, with budget evidence in `.runtime/VEHIDE-BUDGET-V2.json`. Version-1 failure logs and immutable inputs remain available; neither launch tool automatically resubmits a paid failure.


The repaired [version-2 job](https://huggingface.co/jobs/abduloxunov/6acb26e6095c57808931b22c) was submitted once and is **RUNNING**. The launcher reconciled all four earlier jobs including the image-decoding failure: conservative completed hardware estimate $0.573319 plus new 40-minute cap $0.53332 = **$1.106639** within $2. This includes scheduling time and per-job upward rounding and is not a billing statement. There is no completed version-2 epoch or validation metric yet. A local monitor polls status and downloads final outputs, with checkpoint hashes verified against the cloud inventory.
