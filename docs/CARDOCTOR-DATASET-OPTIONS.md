# Additional datasets for CarDoctor

Checked 11 October 2026. No additional dataset was downloaded or mixed into the active CarDD continuation. Options below come from primary dataset/project/paper pages and official Kaggle metadata. The initial VehiDE page was unreadable, but a follow-up API check recovered its publisher metadata.

## Practical recommendation for the deadline

Keep the running CarDD continuation and its validation split stable. Adding another dataset requires a label/provenance audit and independent split design; dataset size alone does not establish better performance. Use a small permission-cleared local photo set for realistic evaluation now. After the hackathon, the highest-value product extension is a separate vehicle-part model to complement damage detection; this helps route evidence to the actual door, glass, lamp or bumper.

## Verified options

| Dataset | Publisher-described contents | Intended use in our project | Important preparation |
|---|---|---|---|
| [CrashCar101 project](https://crashcar.compute.dtu.dk/) / [paper](https://openaccess.thecvf.com/content/WACV2024/papers/Parslov_CrashCar101_Procedural_Generation_for_Damage_Assessment_WACV_2024_paper.pdf) | 101,050 synthetic images with damage and part segmentation annotations | Later synthetic pretraining/augmentation experiment, followed by real-data fine-tuning and real-photo evaluation | Class mapping, masks-to-boxes conversion if used by our detector, synthetic-to-real validation. [Official HF release](https://huggingface.co/datasets/JensParslov/CrashCar) is gated, requires accepting access conditions, and lists total file size 17.7 GB; full terms not inspected. |
| [Carparts-Seg documentation](https://docs.ultralytics.com/datasets/segment/carparts-seg/) | 3,833 images; 23 part categories including a catch-all object class; masks; 3,156 train / 401 validation / 276 test | Train a separate part locator/segmenter. Combine its part regions with damage regions, retaining uncertainty and user confirmation | Part labels are not damage labels. The dataset page displays CC BY 4.0; the Ultralytics software/YAML notice separately uses AGPL-3.0. Check exact downloaded data/source terms; code/model and data licences are separate. The page has differing archive-size indicators, so size is not treated as audited. |
| [SYNDCAR, version 1](https://data.mendeley.com/datasets/hzpj48krdt/1) | Publisher describes a synthetic dataset of 245 high-resolution images, four damage classes (broken glass, broken lights, cracks, scratches) and 28 vehicle parts; damage boxes and part polygons; CC BY 4.0 | Small supplementary domain/part-and-damage evaluation or data-conversion experiment | Small sample and different class coverage; dents and flat tyres are absent from its stated damage taxonomy. Device identifiers are in filenames; preserve group information when defining evaluation. No local archive inspected. |
| Our own permission-cleared vehicle photos | Not collected/labelled by this chat; proposed data | Test the actual environment: local car models, parking lighting, phone cameras, reflections, small damage and undamaged examples | Label boxes/classes and component; record vehicle/incident IDs and permission. Split by vehicle/incident before augmentation. Remove sensitive identifying content before public display. Separate train and final evaluation photos. |

The CrashCar paper reports benefits from combining synthetic and real data for part segmentation and studies synthetic-to-real transfer for damage segmentation. Those results motivate an experiment; they do not predict CarDoctor's future score.

## Kaggle follow-up: official metadata verified

The official public `https://www.kaggle.com/api/v1/datasets/view/<owner>/<dataset>` endpoint returned these publisher descriptions and metadata on 11 October 2026. No archives, images or weights were downloaded. Counts below are publisher-reported, not locally audited file counts. `totalBytes` may differ from archive download size.

| Kaggle listing | Publisher-reported data | Listed licence | Role |
|---|---|---|---|
| [Humans in the Loop: Car Parts and Car Damages](https://www.kaggle.com/datasets/humansintheloop/car-parts-and-car-damages) | 1,812 images: 998 part-labelled, 814 damage-labelled; 24,851 polygons across both subsets; totalBytes 3,311,753,461 | CC0: Public Domain; description says CC0 1.0 | Strong candidate for adding separate part recognition and supplementary damage examples. The parts and damage subsets are not necessarily jointly annotated per photo. Inspect category definitions and convert polygons before training our current detector. |
| [VehiDE](https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection) | Description reports 13,945 high-resolution damage images and more than 32,000 annotated instances; totalBytes 2,347,389,916 | Listing says Apache 2.0 | Larger real-image damage candidate. Metadata alone does not establish that this upload is the full original release or that its taxonomy matches ours. Inspect original annotations, image provenance and all underlying terms before mixing it. |
| [LPLenka: COCO Car Damage Detection](https://www.kaggle.com/datasets/lplenka/coco-car-damage-detection-dataset) | Description reports 80 original images; train 59 / validation 11 / test 8; generic damage plus five damaged-part categories; totalBytes 15,630,103 | CC0: Public Domain | Small conversion/prototype check; not our main improvement dataset. Do not sum the img folder and split folders as unique photos without deduplication. |

A Kaggle listing's licence is publisher metadata, not a verified chain of rights for every source image. Dataset classes, split grouping and provenance are still archive-level checks. A CarDD mirror also does not provide new independent training data merely because it has a different repository name.

My candidate priority after the current CarDD continuation: Humans in the Loop for the part-plus-damage architecture; VehiDE for a separately validated damage-data expansion. Keep the current validation/test policy stable and measure actual benefit before adopting a mixed dataset.

Kaggle can also host training. [Its official GPU guide](https://www.kaggle.com/docs/efficient-gpu-usage) describes free GPU access subject to a weekly quota, ordinarily 30 hours or sometimes higher depending on resources. This chat has not checked the user's Kaggle account, available accelerators or remaining quota. The existing Hugging Face L4 continuation stays in place; no new Kaggle run has been started.

## How to combine data correctly

1. Define one damage taxonomy. A merged `scratch_crack` category cannot be automatically separated into our `scratch` and `crack` classes. Part labels such as `door` cannot be merged as though they were damage classes.
2. Audit every archive for class IDs, coordinate conventions, missing images, mask/box quality and access/reuse terms.
3. Deduplicate across sources and vehicle/incident groups before splitting. Keep the official CarDD test photos out of added training data, including copies from community mirrors.
4. Decide whether data trains a separate part model, augments the damage detector or provides external-domain evaluation. These are different experiments.
5. Compare against the preserved CarDD-only baseline on the same validation and independent local evaluation set; report per-class AP, misses and false positives. Choose the final model using validation, then reserve the final test for reporting.

More pictures can introduce incompatible labels, synthetic appearance or leakage. For the current deadline, measured continuation plus a realistic small evaluation set is a stronger plan than an unverified last-minute merge.


## Actual Kaggle archive audit and HF preparation, 11 October

See [the complete preparation guide](CARDOCTOR-KAGGLE-HF-PREPARATION.md) for parsed class definitions, corrected archive counts, cleaned data and scripts. VehiDE has seven observed native labels, 11,621 original training images and 2,324 validation images; conversion retained 11,603 train / 2,324 validation after exact duplicate removal. Its native labels remain separate from CarDD. No additional GPU job is started by preparation.

The Humans in the Loop archive folder names are reversed relative to their class definitions: `Car damages dataset` contains 998 part annotations (21 classes), and `Car parts dataset` contains 814 damage annotations (8 classes). The tiny COCO archive has 59 annotated train + 11 annotated validation + 8 unannotated test photos; `img/` contains 70 photos also represented in train/validation folders. These audited counts replace any earlier unverified size or class assumptions.
