# CarDoctor CV training plan

Status: proposed experiment, not an accepted shared architecture change. Researched 11 October 2026. Prices and service limits below were checked against provider documentation on that date.

This expands [the project plan](CARDOCTOR-PROJECT-PLAN.md) and [the research dossier](CARDOCTOR-CV-RESEARCH.md). The current agreed product remains multimodal visual/text retrieval with a knowledge base and an LLM. A specialist damage detector would provide additional visual evidence to that pipeline. It would not replace the knowledge base or silently reassign implementation tasks.

## Recommended first decision

**Fine-tune RF-DETR Nano for damage detection, once suitable labelled data is available. The user selected Google Colab for the first test.** Begin with a short smoke run before deciding the full training time. Hugging Face Jobs with an L4 GPU remains a fallback if available credits or an approved budget cover it.

We are teaching an existing vision model to recognise our damage categories. We are not training a foundation model from scratch. A damage-trained checkpoint with compatible terms and satisfactory measurements could remove the need to train initially, but the checkpoints reviewed below do not yet justify that choice.

No paid run, dataset download, package installation, model download, cloud upload, email or Git push was performed for this plan. Account credit balance, dataset access and the training budget remain unconfirmed.

## 1. What the CV model will do

For the first experiment, use one object detector: photo in, damage labels and bounding boxes out. For example, a photo can contain a dent and a scratch; the model should locate each independently. Its score expresses model confidence, not mechanical severity.

Detection requires pictures with a class and a rectangle around each visible defect. Segmentation additionally requires a pixel mask for the defect shape. Segmentation can be valuable for highlighting irregular scratches, but first establish that we can reliably recognise and locate damage. Consider RF-DETR Seg Nano later if masks improve the actual user workflow.

One model can learn several classes. We do not need separate networks for dents, scratches and cracks. We also do not need to train an LLM now: retrieval can supply reviewed knowledge to an existing LLM.

A proposed evidence flow is:

```text
Photo -> quality check -> damage detector -> labelled regions / crops
                                                |
                                   visual reference retrieval
                                                |
                          user symptoms + reviewed knowledge sources
                                                |
                             LLM explanation with source links
```

Damage type alone cannot establish hidden mechanical problems, repair prices or whether a vehicle is safe to drive. Car part and symptom context should be requested or checked before retrieving advice. Part identification is a separate capability; a damage-only model does not automatically recognise every component.

## 2. What exists locally

The [local prototype](../experiments/cardoctor-local/README.md) has ImageNet ResNet18 features, manually selected regions and similarity-based reference retrieval. Its optional frozen-feature linear head is an image/crop classifier. It is not a full-photo damage detector, and no automotive training accuracy has been measured.

The checked local environment has CPU-only PyTorch, about 15 GB system memory and integrated AMD graphics, with no NVIDIA CUDA GPU. Use it for data preparation, labels, retrieval and inference measurements. Use a cloud GPU for the proposed detector training.

D: had about 54 GiB free at inspection; C: had very little free space. Keep any later local dataset, weights, package caches and temporary training files on D:. Configure `HF_HOME`, `TORCH_HOME`, package caches and temporary paths before any download; their defaults can otherwise use C:.

## 3. Model selection and checkpoint review

| Candidate | What is already learned | Decision for this experiment |
| --- | --- | --- |
| RF-DETR Nano, official pretrained weights | General object detection, not our damage labels | Preferred supervised fine-tuning candidate |
| RF-DETR Seg Nano | General instance segmentation | Later comparison if defect masks add value |
| `harpreetsahota/car-dd-segmentation-yolov11` | Six CarDD damage classes; uses YOLO11x segmentation | Research comparator only: large variant and AGPL-3.0 conflict with the team's preferred licence route |
| `vineetsarpal/yolov11n-car-damage` | Fourteen mostly part-specific dent/window/lamp labels | Does not directly cover our scratch/crack scope; its Apache tag does not by itself resolve the underlying Ultralytics terms |

RF-DETR's official documentation identifies Nano through Large and its code as Apache 2.0; larger Plus variants have different terms. Select the exact Nano artifact and record its version. This preference is about a feasible, compatible starting point, not a claim that it outperforms every alternative on CarDoctor photos. [Official RF-DETR documentation](https://rfdetr.roboflow.com/latest/), [repository licence](https://github.com/roboflow/rf-detr/blob/develop/LICENSE).

The damage checkpoints above were inspected through their model cards, not downloaded or tested. Their author-reported metrics are not our results. [CarDD YOLO segmentation card](https://huggingface.co/harpreetsahota/car-dd-segmentation-yolov11), [YOLO Nano damage card](https://huggingface.co/vineetsarpal/yolov11n-car-damage).

## 4. Dataset selection

**CarDD is the strongest first dataset candidate found for this scope.** It contains 4,000 high-resolution photos and more than 9,000 annotated damage instances across dent, scratch, crack, glass shatter, lamp broken and tire flat. Its official access process requires prior author consent; the licence also restricts redistribution and commercial use without authorization. We have not obtained that consent or the data. [Official dataset](https://cardd-ustc.github.io/), [owner licence and access form](https://cardd-ustc.github.io/docs/CarDD_license.pdf).

If authorized, preserve all six original labels when training and focus the first product evaluation on dent, scratch and crack. Expose each additional class only after its behaviour is tested. Having a label in training is not proof that we support it reliably.

Add permission-cleared local photos because public damage datasets may differ from our actual phone photos, vehicles and lighting. Include genuinely undamaged panels and confusing examples: reflections, seams, dirt, rain, shadows and stickers. Annotate all supported visible defects. A photograph is not a valid clean negative merely because one defect was left unlabelled.

If CarDD access is delayed, use team-owned, annotated photos for a limited feasibility experiment, and keep the current retrieval workflow available. Do not claim generalisation from a few example cars. Dashboard warnings, leaks, engine symptoms and road cracks require different data and evaluation; CarDD does not teach them.

A larger merged dataset is not automatically a better substitute. The [AutoDamageIQ dataset card](https://huggingface.co/datasets/tugberkkalay/autodamageiq-vehicle-damage-dataset) says it combines CarDD, VehiDE and additional annotations. Its displayed licence tag does not establish that CarDD's owner granted the permissions needed for our use. Provenance remains unresolved until checked.

For each image, record an image ID, source/permission, vehicle or incident group, labels and split. Keep originals and derivatives in the same split. Check exact and near duplicates. Use the official benchmark split where supplied, audit overlap, and reserve separate local vehicles as a transfer test. Split our own photos by vehicle/incident before cropping or augmentation; random image splitting can leak near-identical views into the test set.

Use COCO annotations for the first export. RF-DETR documents `train`, `valid` and `test` directories with their images and `_annotations.coco.json`. Verify image dimensions, boxes, class IDs and empty annotations before GPU use. [Dataset format documentation](https://rfdetr.roboflow.com/latest/learn/train/dataset-formats/).

## 5. Where to train and what PRO provides

Hugging Face PRO currently includes monthly compute credits that its documentation says can be used for Jobs, as well as other compute services. The subscription is not an unlimited dedicated training GPU. Check the account's actual remaining eligible balance before selecting hardware. [PRO benefits](https://huggingface.co/docs/hub/pro).

| Training option | Published price | Proposed use |
| --- | --- | --- |
| HF Jobs T4 small, 16 GB GPU memory | $0.40/hour | Cheapest listed GPU candidate; benchmark speed and memory fit |
| HF Jobs L4, 24 GB GPU memory | $0.80/hour | Preferred first paid/credit-covered experiment, subject to availability |
| HF Jobs A10G small, 24 GB GPU memory | $1.00/hour | Backup if L4 unavailable |
| Free Google Colab GPU | No paid plan required for free-tier use | First attempt when there is no approved extra spending; availability and session limits vary |

Jobs hardware is billed by the minute in Starting/Running states. Four billed hours would cost $1.60 on T4, $3.20 on L4 or $4.00 on A10G; these are cost scenarios, not predictions of training time. A 30-minute L4 allocation is about $0.40 in hardware charges. Check available hardware and set a hard job timeout. [Jobs pricing](https://huggingface.co/docs/hub/jobs-pricing).

Free Colab is useful but does not guarantee GPU availability or a particular GPU. Save checkpoints regularly so interruption does not erase progress. [Colab FAQ](https://research.google.com/colaboratory/faq.html).

PRO's ZeroGPU Spaces quota is for dynamically allocated GPU functions. It is a better fit for interactive inference than this sustained fine-tuning workflow; do not interpret its quota as a continuous dedicated training allocation. [ZeroGPU documentation](https://huggingface.co/docs/hub/spaces-zerogpu).

## 6. Proposed experiment protocol

1. **Data gate:** verify access/permissions, labels and grouped splits. Keep the independent test set untouched during model and threshold selection.
2. **Setup:** pin the RF-DETR package, pretrained checkpoint, CUDA container and experiment configuration. Training currently uses the `rfdetr[train]` extra. No installation has been performed. [Training guide](https://rfdetr.roboflow.com/latest/learn/train/).
3. **Smoke run:** use a reviewed training subset, two epochs and a 20-30 minute maximum allocation. Check loss, validation predictions, checkpoint persistence and GPU memory. A tiny smoke run proves that the pipeline runs, not that the detector is accurate.
4. **Pilot:** start with pretrained Nano, its default 384-pixel input, the documented optimizer defaults and GPU-tested batch size. A 20-30 epoch pilot is a proposed initial observation window, not a promised sufficient training length. Review validation results and failure examples.
5. **Refinement:** if thin defects disappear at low resolution, compare a compatible higher resolution such as 640 for the detection model, or suitable crops. Tune only on validation data. Do not copy detection resolution settings blindly to segmentation variants.
6. **Decision:** estimate full runtime from measured pilot throughput, then choose further epochs or stop. Persist the best checkpoint and a full resume checkpoint, with logs and data/model identifiers.
7. **Held-out evaluation:** select model and thresholds on validation, then evaluate the test set once for the reported result. Measure per-class precision/recall and AP, missed small cracks, false positives on normal/confusing photos, and actual app latency. Record test size and vehicle groups alongside metrics.

RF-DETR supports automatic batch-size probing on CUDA; resolution, accumulation and resume behaviour should follow the pinned version's documentation. [Training parameters](https://rfdetr.roboflow.com/latest/learn/train/training-parameters/).

HF Jobs' working disk is ephemeral. Arrange permitted durable checkpoint storage before the job, not after it ends. Closing a log stream does not cancel the running job; use explicit cancellation or its timeout. [Jobs training guide](https://huggingface.co/docs/hub/jobs-training).

## 7. Decision record and next step

| Item | Current state |
| --- | --- |
| Task | Proposed damage detection extension to the existing retrieval pipeline |
| Training type | Supervised fine-tuning of pretrained weights |
| Model | RF-DETR Nano candidate; no comparative CarDoctor result yet |
| Data | CarDD permission pending; local photo inventory/labels not established |
| Compute | User selected Google Colab first; HF Jobs remains a later credit/budget-dependent option |
| Spending | No extra budget assumed; no paid job started |
| Product claim | Detect visible supported damage and retrieve reviewed context; no measured accuracy yet |

The first practical step is to establish the labelled data we can actually use and check the Hugging Face credit balance. Then perform a small cloud smoke run. The repository's 13:00 local code freeze means dataset authorization or a full training run may not finish in time; keep an honestly described working retrieval baseline available and treat training as an experiment until it passes evaluation.

## Colab preparation update — 11 October 2026

The user authorized a Colab training experiment and confirmed there is no dataset yet. A [self-contained notebook and complete Markdown guide](../experiments/cardoctor-colab/README.md) are prepared locally. The first cell checks GPU availability without downloading detector weights. Later cells require a real permission-cleared COCO dataset, validate labels and split integrity, and cap the smoke subset at 64 training and 16 validation images. Two-epoch training has a 30-minute process timeout and saves checkpoints, logs and provenance. Twelve local data-integrity checks passed and notebook code cells compile; cloud GPU execution remains unverified. No training, dataset/model-weight download, cloud upload, spending or Git push occurred.

## Local preparation completed - 11 October

CarDD is downloaded and audited. The [Colab preparation report](CARDD-COLAB-PREPARATION.md) records the original 2,816/810/374 split, unchanged COCO annotation bytes, full converted layout on D:, and a seed-42 class-covered 64/16 smoke subset (141/41 objects) packaged into a 61,212,543-byte ZIP with verified CRC and SHA-256. The [full notebook guide](../experiments/cardoctor-colab/README.md) contains every notebook cell, upload instructions, GPU check, two-epoch RF-DETR Nano training, checkpoint persistence and four validation prediction previews.

20 local data/conversion checks pass. All 11 notebook Python cells compile and its embedded helpers match local source files. The user explicitly directed research use; metadata preserves the distinction between that instruction and unverified PIC Lab prior consent. No GPU training or cloud upload occurred: the browser-control helper failed before accessing Colab, including a fresh-session retry. The notebook, private local upload ZIP and manual launch steps are ready; no model accuracy is claimed.
