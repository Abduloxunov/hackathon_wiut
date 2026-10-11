# CarDoctor: Google Colab training smoke test

Updated on 11 October 2026. **The user completed the two-epoch Colab smoke run; downloaded checkpoints are hash-verified and the EMA weights run locally.** The four-image review demonstrates poor predictions, so these smoke weights are not ready for product use. See the [actual results and checkpoint review](../../docs/CARDOCTOR-SMOKE-REVIEW.md). Original data, checkpoints and local outputs remain on D:. Browser control is unavailable here; future Colab uploads, GPU selection and Google Drive authorization require the user's interaction.

## Start the prepared run

1. Open [Google Colab](https://colab.research.google.com/) and choose **File -> Upload notebook**. Select `D:\hakathon_wiut\finals\mdb-vision-finals\experiments\cardoctor-colab\cardoctor_rfdetr_nano_smoke.ipynb`.
2. Choose **Runtime -> Change runtime type -> GPU**. Use T4 if it is offered; the first code cell confirms the actual GPU. Free availability varies.
3. Choose **Runtime -> Run all**. When the file picker appears, select `D:\hakathon_wiut\datasets\cardoctor-cardd-smoke.zip`.
4. Complete Google's authorization to save checkpoints privately in your Drive. The notebook runs two epochs with RF-DETR Nano. Training has a 30-minute subprocess timeout; upload and installation are separate.
5. Inspect the run status, checkpoint hashes and four validation prediction previews. Keep the saved run folder for review. Download optional artifacts only to D:, with the browser configured to ask where to save; no automatic local download is triggered.

No OpenRouter or Hugging Face token is required. No paid GPU job or external monitoring service is started. Dependencies and pretrained weights are downloaded to the remote Colab `/content` disk. Default persistent outputs are in `MyDrive/CarDoctor/runs/<run-id>` after user authorization.

## Prepared data and actual checks

- Original COCO data: `D:\hakathon_wiut\datasets\CarDD_release\CarDD_release\CarDD_COCO`.
- Converted full layout: `D:\hakathon_wiut\datasets\cardoctor-cardd-coco`.
- Prepared smoke data: `D:\hakathon_wiut\datasets\cardoctor-cardd-smoke`.
- Upload ZIP: `D:\hakathon_wiut\datasets\cardoctor-cardd-smoke.zip` (**61,212,543 bytes**, approximately 61 MB).
- Archive SHA-256: `7d5b6b628fe7af5e6da1458b727d49df080a26e4abc211cc677f9fe4e19dfa68`.

The converted full dataset retains the original 2,816 training / 810 validation / 374 test images and 8,740 object annotations. Annotation bytes, category IDs, image IDs, boxes, masks and split membership were preserved. Converted images are hardlinks on D:, so they share bytes with the originals: do not overwrite linked image contents. The 80 smoke images are separate copies.

The seed-42 smoke selection includes 64 train images / 141 objects and 16 validation images / 41 objects, with all six classes present in each split. It first covers at least two training images and one validation image containing each class, then fills the remaining slots. Test images are excluded. This deliberate class coverage is a pipeline test, not a representative validation sample or accuracy benchmark.

Full data and smoke data passed image dimensions, finite/positive/in-bounds boxes, class-schema consistency and exact cross-split duplicate checks. The ZIP passed CRC verification. Vehicle/incident grouping remains unverified; byte hashes do not establish independence or detect every near duplicate. See the [original download audit](../../docs/CARDD-DOWNLOAD-CHECK.md) and [complete preparation results](../../docs/CARDD-COLAB-PREPARATION.md).

## Source and authorization metadata

The user explicitly directed research use of the downloaded data. The prepared provenance records `user_authorized_research_use: true` while retaining `permission_confirmed: false` and `owner_consent_status: unverified`. The audit accepts this explicitly recorded user instruction and reports it separately from confirmed owner consent; it never changes the author-consent field to true. Without either confirmed permission or explicit user-directed research use, the notebook stops.

The [CarDD authors' terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf) require prior PIC Lab consent for research and authorization for third-party transfer; commercial use needs separate authorization. Completion of that licensing form has not been verified here. No author consent or commercial/redistribution rights are asserted by local conversion or the user's instruction. The images, private ZIP and future preview images must stay out of the public Git repository. The local datasets folder has an ignore file.

## Implementation and reproduction

- [Notebook](cardoctor_rfdetr_nano_smoke.ipynb): self-contained; embedded Python helpers match the local files and code outputs are empty until a real Colab run.
- [Checkpoint review script](inspect_checkpoint.py): verifies the EMA hash, loads weights offline on CPU and saves four private ground-truth/prediction comparisons on D:. Local inference dependencies are pinned in [inference-requirements.txt](inference-requirements.txt).
- [Data tools](data_tools.py): scoped extraction, authorization metadata, COCO/image/box checks, exact/group leakage checks and reproducible class-covered smoke selection.
- [Original CarDD converter](prepare_cardd.py): fresh output directories only, source/annotation preservation, same-volume image links, subset and checked ZIP.
- [Training script](train_detector.py): `rfdetr[train]==1.11.2`, RF-DETR Nano, two epochs, 384-pixel input, physical batch 2, accumulation 2, learning rate `1e-4`, explicit six-class names, no test evaluation, no W&B/TensorBoard upload.
- [Data checks](test_data_tools.py) and [conversion checks](test_prepare_cardd.py): synthetic engineering fixtures, never claimed as car-damage results.

To reproduce conversion into **new** output directories on D: (existing files are preserved):

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B experiments/cardoctor-colab/prepare_cardd.py --source D:\hakathon_wiut\datasets\CarDD_release\CarDD_release\CarDD_COCO --destination D:\hakathon_wiut\datasets\cardoctor-cardd-coco-v2 --smoke D:\hakathon_wiut\datasets\cardoctor-cardd-smoke-v2 --archive D:\hakathon_wiut\datasets\cardoctor-cardd-smoke-v2.zip --report D:\hakathon_wiut\finals\mdb-vision-finals\docs\CARDD-COLAB-PREPARATION-V2.md --user-authorized-research-use
```

The last flag records an actual explicit user research instruction; do not use it to claim author consent. `--copy-images` is available when hardlinks are unsuitable but duplicates about 3 GB of images on D:. Dataset copies, archives and weights are local ignored files; no Git push was performed.

## Outputs and failure handling

Each training run saves source and smoke audits, exact provenance/selection metadata, installed package versions, logs, process status, checkpoints and hashes. Four smoke-validation images are rendered with the trained model at threshold 0.35, with predictions identified as uncalibrated and unreviewed. Zero predictions or poor boxes after two epochs are useful debug outcomes, not useful damage accuracy.

A failed/timed-out process is not success even when partial checkpoints exist. For CUDA out-of-memory, change the embedded training script to physical batch 1 / accumulation 4 and start a fresh run. Checkpoint previews happen only after successful training and checkpoint inventory. Keep full `.ckpt` for later optimizer-state resumption; `.pth` is normally a weights export.

The pinned RF-DETR wheel was inspected in memory. Its Roboflow COCO builder supports train/valid/test with `_annotations.coco.json`, maps sorted category IDs to training labels, and aligns the class count. Original CarDD IDs 1–6 can therefore be preserved. The preparation step does not run training; a subsequent local CPU review loaded the user-supplied EMA weights.

20 local data/conversion engineering checks passed. Notebook Python cells compile, embedded helpers match local source files, and no executed GPU outputs or model accuracy numbers are fabricated. The user subsequently completed Colab training and supplied real logs, metrics and weights; the linked smoke review records those results separately from the unexecuted notebook template.

Primary references checked: [CarDD project](https://cardd-ustc.github.io/), [CarDD terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf), [RF-DETR training](https://rfdetr.roboflow.com/latest/learn/train/), [pinned package](https://pypi.org/project/rfdetr/1.11.2/), [Colab limits](https://research.google.com/colaboratory/faq.html).

## Complete notebook cells

All cells are reproduced below for Markdown review. `%%writefile` is a Colab/IPython directive. Run the notebook rather than this Markdown rendering.

### Cell 1

# CarDoctor: RF-DETR Nano training smoke test

CarDD is now downloaded and converted locally. This notebook runs a two-epoch pipeline check on a prepared, six-class subset: 64 training images and 16 validation images. The official test split is excluded. These are not product accuracy measurements.

Select **Runtime -> Change runtime type -> GPU** (T4 if offered), then run cells in order. Upload `D:\hakathon_wiut\datasets\cardoctor-cardd-smoke.zip` when prompted. GPU allocation, Google Drive authorization and file selection require your browser interaction.

The user directed research use; provenance records this separately from the unverified PIC Lab licensing-form status. No author consent is invented. No Hugging Face/OpenRouter key is needed. All package/model downloads occur on the remote Colab disk. The training subprocess has a 30-minute timeout. Outputs are saved privately in your Google Drive by default; no automatic local download is triggered.

References: [RF-DETR training](https://rfdetr.roboflow.com/latest/learn/train/), [pinned release](https://pypi.org/project/rfdetr/1.11.2/), [CarDD](https://cardd-ustc.github.io/), [CarDD terms](https://cardd-ustc.github.io/docs/CarDD_license.pdf), [Colab FAQ](https://research.google.com/colaboratory/faq.html).

### Cell 2

```python
import os, sys
from pathlib import Path
WORK = Path('/content/cardoctor')
WORK.mkdir(parents=True, exist_ok=True)
for key, folder in {'HF_HOME':'hf', 'TORCH_HOME':'torch', 'PIP_CACHE_DIR':'pip', 'XDG_CACHE_HOME':'xdg'}.items():
    os.environ[key] = str(WORK / 'cache' / folder)
os.chdir(WORK)
import torch
print('Python:', sys.version.split()[0], '| PyTorch:', torch.__version__)
assert torch.cuda.is_available(), 'No GPU allocated. Select a GPU runtime, then reconnect and rerun.'
print('GPU:', torch.cuda.get_device_name(0))
print('GPU memory GiB:', round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 1))
print('GPU check passed. No detector weights have been downloaded.')
```

### Cell 3

## Upload the prepared smoke ZIP

The local upload file is **`D:\hakathon_wiut\datasets\cardoctor-cardd-smoke.zip`**. Select that file in the next cell's picker. It contains only the 64/16 subset, COCO annotations, truthful provenance, and its selection metadata; no test photos or API secrets.

You can instead upload a full converted COCO archive using `train/`, `valid/`, `test/`, root `provenance.json`, and `_annotations.coco.json` inside each split. The notebook will make a covered 64/16 subset automatically. It does not silently infer author permissions: the prepared metadata records the user's explicit research instruction and leaves author consent unverified.

Vehicle/incident group independence is not verified. Class-covered smoke selection deliberately changes the class mix; validation outputs are for debugging the training pipeline only.

### Cell 4

```python
from google.colab import files
uploaded = files.upload()
assert len(uploaded) == 1, 'Select exactly one prepared COCO ZIP.'
ARCHIVE_PATH = WORK / next(iter(uploaded))
assert ARCHIVE_PATH.is_file() and ARCHIVE_PATH.suffix.lower() == '.zip', 'Upload a dataset ZIP.'
print('Uploaded:', ARCHIVE_PATH.name, '| bytes:', ARCHIVE_PATH.stat().st_size)
del uploaded
```

### Cell 5

```python
%%writefile /content/cardoctor/data_tools.py
"""COCO damage-data checks and smoke-subset preparation. No model downloads."""
from pathlib import Path, PureWindowsPath
from collections import Counter
import csv
import hashlib
import json
import math
import random
import shutil
import stat
import zipfile
from PIL import Image

DAMAGE_CLASSES = {'dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat', 'glassshatter', 'lampbroken', 'tireflat'}

def contained(root, name):
    root = Path(root).resolve()
    if not isinstance(name, str) or not name or PureWindowsPath(name).drive or '\\' in name:
        raise ValueError(f'Unsafe dataset path: {name!r}')
    target = (root / name).resolve()
    if not target.is_relative_to(root) or target == root:
        raise ValueError(f'Path escapes dataset: {name!r}')
    return target

def extract_dataset(archive, destination, max_bytes=8 * 1024**3):
    """Inspect the complete archive before extracting into a new directory."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Choose a fresh extraction directory; existing files are not overwritten.')
    with zipfile.ZipFile(archive) as z:
        if sum(info.file_size for info in z.infolist()) > max_bytes:
            raise ValueError('Archive exceeds the 8 GiB uncompressed limit.')
        seen = set()
        for info in z.infolist():
            contained(destination, info.filename.rstrip('/'))
            if info.filename in seen:
                raise ValueError(f'Duplicate ZIP entry: {info.filename}')
            seen.add(info.filename)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Dataset ZIP must not contain symbolic links.')
        destination.mkdir(parents=True)
        z.extractall(destination)
    roots = [p.parent.parent for p in destination.rglob('_annotations.coco.json')
             if p.parent.name == 'train' and (p.parent.parent / 'valid/_annotations.coco.json').exists()]
    if len(roots) != 1:
        raise ValueError('Expected exactly one dataset root with train/ and valid/ COCO annotations.')
    return roots[0]

def audit_dataset(root):
    root = Path(root).resolve()
    provenance_path = root / 'provenance.json'
    if not provenance_path.exists():
        raise ValueError('Add provenance.json beside train/ and valid/; see the guide.')
    provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
    owner_confirmed = provenance.get('permission_confirmed') is True
    user_directed = provenance.get('user_authorized_research_use') is True
    if not owner_confirmed and not user_directed:
        raise ValueError('Dataset use has not been authorized; record permission or explicit user-directed research use.')
    for field in ('source', 'permission', 'split_policy'):
        if not isinstance(provenance.get(field), str) or not provenance[field].strip():
            raise ValueError(f'provenance.json needs a nonempty {field}.')
    reports, records, digest_splits, schemas = {}, {}, {}, []
    image_keys = set()
    for split in ('train', 'valid', 'test'):
        annotation_file = root / split / '_annotations.coco.json'
        if not annotation_file.exists():
            if split != 'test':
                raise ValueError(f'Missing {annotation_file}')
            continue
        data = json.loads(annotation_file.read_text(encoding='utf-8'))
        cats = data.get('categories', [])
        categories = {}
        for cat in cats:
            cid, name = cat.get('id'), cat.get('name')
            if type(cid) is not int or cid < 0 or cid in categories or not isinstance(name, str):
                raise ValueError(f'{split}: invalid or duplicate category.')
            normalized = name.lower().replace('_', ' ').replace('-', ' ').strip()
            if normalized not in DAMAGE_CLASSES:
                raise ValueError(f'{split}: unsupported damage category {name!r}; review the taxonomy.')
            categories[cid] = name
        if not categories:
            raise ValueError(f'{split}: empty categories.')
        schemas.append(categories)
        images, names = {}, set()
        for im in data.get('images', []):
            iid, name = im.get('id'), im.get('file_name')
            if type(iid) is not int or iid in images or name in names:
                raise ValueError(f'{split}: invalid or duplicate image ID/name.')
            path = contained(root / split, name)
            with Image.open(path) as opened:
                actual_size = opened.size
                opened.verify()
            if actual_size != (im.get('width'), im.get('height')):
                raise ValueError(f'{split}/{name}: annotation dimensions differ from the image.')
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            prior = digest_splits.get(digest)
            if prior is not None and prior != split:
                raise ValueError(f'Exact image leakage across {prior} and {split}: {name}')
            digest_splits[digest] = split
            images[iid], names = im, names | {name}
            image_keys.add((split, name))
        if not images:
            raise ValueError(f'{split}: empty images.')
        anns, counts, positive_ids = set(), Counter(), set()
        for ann in data.get('annotations', []):
            aid, iid, cid = ann.get('id'), ann.get('image_id'), ann.get('category_id')
            if type(aid) is not int or aid in anns or iid not in images or cid not in categories:
                raise ValueError(f'{split}: invalid annotation ID, image reference or category reference.')
            anns.add(aid)
            box = ann.get('bbox')
            if not isinstance(box, list) or len(box) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) for v in box):
                raise ValueError(f'{split}: nonfinite or malformed bounding box.')
            x, y, w, h = box
            im = images[iid]
            if min(x, y) < 0 or min(w, h) <= 0 or x + w > im['width'] + 0.001 or y + h > im['height'] + 0.001:
                raise ValueError(f'{split}: bounding box outside its image or empty.')
            if ann.get('iscrowd', 0) not in (0, 1):
                raise ValueError(f'{split}: invalid iscrowd.')
            if not ann.get('iscrowd', 0):
                positive_ids.add(iid)
                counts[categories[cid]] += 1
        if not positive_ids:
            raise ValueError(f'{split}: no non-crowd labelled damage examples.')
        reports[split] = {'images': len(images), 'annotations': len(anns),
                          'images_without_targets': len(images) - len(positive_ids),
                          'targets_per_class': dict(counts)}
        records[split] = data
    if any(schema != schemas[0] for schema in schemas[1:]):
        raise ValueError('Category IDs/names must match across all splits.')
    grouping = 'Not verified: exact-duplicate checks do not prove vehicle/incident independence.'
    group_file = root / 'groups.csv'
    if group_file.exists():
        groups, keys = {}, set()
        with group_file.open(newline='') as handle:
            for row in csv.DictReader(handle):
                key = (row.get('split'), row.get('file_name'))
                group = row.get('group_id', '').strip()
                if key not in image_keys or key in keys or not group:
                    raise ValueError('Invalid, duplicate or missing groups.csv record.')
                keys.add(key)
                prior = groups.get(group)
                if prior and prior != key[0]:
                    raise ValueError(f'Vehicle/incident group {group!r} leaks across splits.')
                groups[group] = key[0]
        if keys != image_keys:
            raise ValueError('groups.csv must cover every image in every supplied split.')
        grouping = 'Supplied group IDs checked for overlap; source grouping accuracy requires human review.'
    return {'source': provenance['source'], 'permission': provenance['permission'],
            'authorization_status': 'owner_consent_confirmed' if owner_confirmed else 'user_directed_research_owner_consent_unverified',
            'split_policy': provenance['split_policy'], 'grouping': grouping,
            'categories': schemas[0], 'splits': reports}, records

def select_smoke_images(data, limit, rng, min_class_images=0):
    """Seeded class-coverage selection for a pipeline check, not evaluation."""
    items = list(data['images'])
    rng.shuffle(items)
    if min_class_images < 0:
        raise ValueError('Minimum class coverage must be nonnegative.')
    labels = {im['id']: set() for im in items}
    for ann in data['annotations']:
        if not ann.get('iscrowd', 0):
            labels[ann['image_id']].add(ann['category_id'])
    counts = Counter()
    categories = {cat['id'] for cat in data['categories']}
    selected = []
    while min_class_images and any(counts[c] < min_class_images for c in categories):
        if not items or len(selected) >= limit:
            raise ValueError('Subset too small or source lacks requested class coverage.')
        best = max(items, key=lambda im: sum(counts[c] < min_class_images for c in labels[im['id']]))
        if not any(counts[c] < min_class_images for c in labels[best['id']]):
            raise ValueError('Source lacks requested class coverage.')
        selected.append(best)
        counts.update(labels[best['id']])
        items.remove(best)
    return selected + items[:max(0, limit - len(selected))]


def make_smoke_subset(root, destination, train_limit=64, valid_limit=16, seed=42, min_class_images=0):
    report, records = audit_dataset(root)
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Smoke subset already exists; use a new output directory.')
    if train_limit < 2 or valid_limit < 1:
        raise ValueError('Smoke subset needs at least two training and one validation image.')
    rng = random.Random(seed)
    for split, limit in [('train', train_limit), ('valid', valid_limit)]:
        data = records[split]
        minimum = min_class_images if split == 'train' else min(1, min_class_images)
        items = select_smoke_images(data, limit, rng, minimum)
        selected = {im['id'] for im in items}
        output = {**data, 'images': items,
                  'annotations': [a for a in data['annotations'] if a['image_id'] in selected]}
        if not any(not a.get('iscrowd', 0) for a in output['annotations']):
            raise ValueError(f'{split}: random smoke subset has no targets; review data or increase its size.')
        folder = destination / split
        folder.mkdir(parents=True)
        for im in items:
            target = contained(folder, im['file_name'])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(contained(Path(root) / split, im['file_name']), target)
        (folder / '_annotations.coco.json').write_text(json.dumps(output), encoding='utf-8')
    shutil.copy2(Path(root) / 'provenance.json', destination / 'provenance.json')
    (destination / 'smoke-origin.json').write_text(json.dumps({'seed': seed, 'train_limit': train_limit,
          'valid_limit': valid_limit, 'min_class_images': min_class_images, 'purpose': 'pipeline-only; not a representative accuracy benchmark'}, indent=2), encoding='utf-8')
    return report
```

### Cell 6

```python
import json
from data_tools import extract_dataset, audit_dataset, make_smoke_subset
from datetime import datetime, timezone
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
DATASET_DIR = extract_dataset(ARCHIVE_PATH, WORK / ('data-' + RUN_ID))
AUDIT, _ = audit_dataset(DATASET_DIR)
print(json.dumps(AUDIT, indent=2))
if (DATASET_DIR / 'smoke-origin.json').exists():
    assert AUDIT['splits']['train']['images'] <= 64 and AUDIT['splits']['valid']['images'] <= 16, 'Prepared smoke ZIP exceeds the intended limits.'
    assert 'test' not in AUDIT['splits'], 'Prepared smoke ZIP must not contain test images.'
    SMOKE_DIR = DATASET_DIR
    print('Using the already-prepared subset; no reselection.')
else:
    SMOKE_DIR = WORK / ('smoke-' + RUN_ID)
    make_smoke_subset(DATASET_DIR, SMOKE_DIR, train_limit=64, valid_limit=16, seed=42, min_class_images=2)
SMOKE_AUDIT, _ = audit_dataset(SMOKE_DIR)
assert len(SMOKE_AUDIT['categories']) == 6, 'This experiment expects the six CarDD damage classes.'
for split in ['train', 'valid']:
    missing = set(SMOKE_AUDIT['categories'].values()) - set(SMOKE_AUDIT['splits'][split]['targets_per_class'])
    assert not missing, f'{split} lacks damage examples for {missing}'
print('Smoke subset:', json.dumps(SMOKE_AUDIT['splits'], indent=2))
```

### Cell 7

## Save checkpoints outside the temporary runtime

The next cell mounts your Google Drive when `SAVE_TO_DRIVE=True`; complete Google's authorization yourself. Outputs are private files in your Drive, not a public upload. Ensure dataset/checkpoint terms permit this storage.

If you choose `False`, outputs remain on the temporary Colab disk and may disappear on disconnect. Save them manually before ending the session. For a local download, choose a destination on **D:**; do not use a browser default that writes to C:.

### Cell 8

```python
SAVE_TO_DRIVE = True
if SAVE_TO_DRIVE:
    from google.colab import drive
    drive.mount('/content/drive')
    OUTPUT_DIR = Path('/content/drive/MyDrive/CarDoctor/runs') / RUN_ID
else:
    OUTPUT_DIR = WORK / 'runs' / RUN_ID
    print('Temporary output only: save artifacts before the runtime disconnects.')
OUTPUT_DIR.mkdir(parents=True, exist_ok=False)
(OUTPUT_DIR / 'SOURCE-DATA-AUDIT.md').write_text('# Original dataset audit\n\n```json\n' + json.dumps(AUDIT, indent=2) + '\n```\n')
print('Checkpoint destination:', OUTPUT_DIR)
```

### Cell 9

```python
import subprocess
subprocess.run([sys.executable, '-m', 'pip', 'install', 'rfdetr[train]==1.11.2'], check=True)
from importlib.metadata import version
print('Installed RF-DETR:', version('rfdetr'))
# If Colab requests a runtime restart, restart, then rerun configuration/data cells.
# The timestamp creates fresh folders; existing data and outputs are not overwritten.
```

### Cell 10

```python
%%writefile /content/cardoctor/train_detector.py
"""Runs only inside the Colab GPU runtime after a successful dataset audit."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    from data_tools import audit_dataset
    report, _ = audit_dataset(args.dataset)
    import numpy as np
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError('Select a GPU runtime in Colab; CPU training is not enabled here.')
    if importlib.metadata.version('rfdetr') != '1.11.2':
        raise RuntimeError('This experiment is pinned to rfdetr 1.11.2.')
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    for name in ['provenance.json', 'smoke-origin.json']:
        source = Path(args.dataset) / name
        if source.exists():
            shutil.copy2(source, output / name)
    (output / 'DATA-AUDIT.md').write_text('# Data audit\n\n```json\n' + json.dumps(report, indent=2) + '\n```\n')
    freeze = subprocess.run([os.sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True, check=True)
    (output / 'ENVIRONMENT.md').write_text('# Colab environment\n\nGPU: ' + torch.cuda.get_device_name(0) + '\n\n```text\n' + freeze.stdout + '\n```\n')
    from rfdetr import RFDETRNano
    model = RFDETRNano()
    start = time.monotonic()
    class_names = [report['categories'][cid] for cid in sorted(report['categories'])]
    model.train(dataset_dir=args.dataset, dataset_file='roboflow', class_names=class_names, output_dir=str(output), epochs=2,
                batch_size=2, grad_accum_steps=2, resolution=384, lr=1e-4,
                device='cuda', seed=42, num_workers=2, multi_scale=False,
                checkpoint_interval=1, run_test=False, tensorboard=False,
                wandb=False, early_stopping=False,
                notes={'purpose': 'CarDoctor pipeline smoke test; not an accuracy benchmark',
                       'rfdetr': '1.11.2', 'source': report['source']})
    elapsed = time.monotonic() - start
    (output / 'SMOKE-RESULT.md').write_text(
        '# Smoke run completed\n\nTwo epochs completed on a small labelled subset.\n\n'
        f'Training call elapsed seconds: {elapsed:.1f}\n\n'
        'Any logged validation metrics are diagnostic only. The subset does not establish product accuracy.\n'
        'The held-out test set was not used.\n')

if __name__ == '__main__':
    main()
```

### Cell 11

```python
import signal, time
command = [sys.executable, str(WORK / 'train_detector.py'), '--dataset', str(SMOKE_DIR), '--output', str(OUTPUT_DIR)]
LOG_PATH = OUTPUT_DIR / 'training.log'
started = time.monotonic()
status = 'failed before completion'
child_env = {**os.environ, 'PYTHONUNBUFFERED': '1'}
with LOG_PATH.open('w', buffering=1) as log:
    proc = subprocess.Popen(command, cwd=WORK, env=child_env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    print('Training started. Logs:', LOG_PATH, flush=True)
    try:
        while proc.poll() is None:
            if time.monotonic() - started >= 30 * 60:
                raise subprocess.TimeoutExpired(command, 1800)
            time.sleep(5)
            if int(time.monotonic() - started) % 30 < 5:
                print(LOG_PATH.read_text(errors='replace')[-1800:], flush=True)
        status = 'completed' if proc.returncode == 0 else f'failed (exit {proc.returncode})'
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
        status = 'timed out' if isinstance(exc, subprocess.TimeoutExpired) else 'interrupted'
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    finally:
        elapsed = time.monotonic() - started
        (OUTPUT_DIR / 'RUN-STATUS.md').write_text(
            f'# Training status\n\nStatus: {status}\n\nProcess elapsed seconds: {elapsed:.1f}\n\n'
            'This is a pipeline smoke test, not a product accuracy result.\n')
print('Status:', status)
print(LOG_PATH.read_text(errors='replace')[-6000:])
if status != 'completed':
    raise RuntimeError(f'Smoke run {status}; inspect training.log. Existing checkpoints are preserved.')
```

### Cell 12

## Inspect checkpoints and predictions

Completion plus a saved checkpoint establishes that the training pipeline works. It does not establish useful damage accuracy. The following cells inventory/hash checkpoints and render predictions on four smoke-validation photos. They do not use the official test split.

A zero-detection or poor prediction result is still useful feedback after only two epochs. Keep thresholds, missed defects and false detections visible. Do not treat detection scores as diagnostic certainty. A timeout/failure is a failed run even if partial checkpoints were saved.

For CUDA out-of-memory, change the embedded training script to `batch_size=1, grad_accum_steps=4` and start a new run. Do not launch a paid alternative automatically if Colab cannot allocate a GPU. For later resumption retain a full `.ckpt` and matching configuration; `.pth` exports are usually weights for inference.

### Cell 13

```python
import hashlib
inventory = []
for file in sorted(OUTPUT_DIR.rglob('*')):
    if file.is_file():
        inventory.append(f'- `{file.relative_to(OUTPUT_DIR)}`: {file.stat().st_size:,} bytes')
print('\n'.join(inventory))
checkpoints = list(OUTPUT_DIR.rglob('*.pth')) + list(OUTPUT_DIR.rglob('*.ckpt'))
assert checkpoints, 'No saved checkpoint found: inspect logs before calling this test successful.'
lines = ['# Saved checkpoint hashes', '']
for file in checkpoints:
    digest = hashlib.sha256()
    with file.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    lines.append(f'- `{file.relative_to(OUTPUT_DIR)}`: `{digest.hexdigest()}`')
(OUTPUT_DIR / 'CHECKPOINTS.md').write_text('\n'.join(lines) + '\n')
print('Saved checkpoint inventory:', OUTPUT_DIR / 'CHECKPOINTS.md')
```

### Cell 14

```python
from rfdetr import RFDETRNano
import supervision as sv
from PIL import Image
from IPython.display import display
candidates = sorted(OUTPUT_DIR.rglob('*.pth')) or sorted(OUTPUT_DIR.rglob('*.ckpt'))
assert candidates, 'No trained checkpoint available for preview.'
CHECKPOINT = next((p for p in candidates if 'best' in p.name.lower() and 'ema' in p.name.lower()),
                  next((p for p in candidates if 'best' in p.name.lower()), candidates[-1]))
print('Preview checkpoint:', CHECKPOINT.name)
preview_model = RFDETRNano.from_checkpoint(str(CHECKPOINT))
PREVIEW_DIR = OUTPUT_DIR / 'validation-previews'
PREVIEW_DIR.mkdir(exist_ok=True)
names = [SMOKE_AUDIT['categories'][i] for i in sorted(SMOKE_AUDIT['categories'])]
validation = json.loads((SMOKE_DIR / 'valid/_annotations.coco.json').read_text())
preview_records = []
for item in validation['images'][:4]:
    image = Image.open(SMOKE_DIR / 'valid' / item['file_name']).convert('RGB')
    detections = preview_model.predict(image, threshold=0.35)
    # RF-DETR can return its no-object slot (index len(names)); exclude it.
    detections = detections[(detections.class_id >= 0) & (detections.class_id < len(names))]
    labels = [f'{names[int(cid)]} {float(conf):.2f}' for cid, conf in zip(detections.class_id, detections.confidence)]
    annotated = sv.BoxAnnotator().annotate(image.copy(), detections)
    annotated = sv.LabelAnnotator().annotate(annotated, detections, labels)
    output = PREVIEW_DIR / (Path(item['file_name']).stem + '-predictions.png')
    annotated.save(output)
    preview_records.append({'file':item['file_name'], 'detections':len(detections), 'threshold':0.35,
                            'labels':labels, 'artifact':output.name})
    print(item['file_name'], '| detections:', len(detections), '| uncalibrated scores; two-epoch smoke only')
    display(annotated)
(OUTPUT_DIR / 'PREVIEWS.md').write_text('# Smoke validation predictions\n\nNot an accuracy benchmark. Four validation examples at threshold 0.35.\n\n```json\n' + json.dumps(preview_records, indent=2) + '\n```\n')
```

### Cell 15

## Keep the result

The next cell packages the checkpoints, run status, environment, training log, provenance and preview images. Outputs already saved to Google Drive remain there after disconnect. No file is automatically downloaded to your computer.

For a local copy, select the generated ZIP in Colab's Files panel and download it only with a browser setting/location that saves to **D:**. Keep the archive and `RUN-STATUS.md` for the next review. Do not publish CarDD photos or this private archive to GitHub.

### Cell 16

```python
import shutil
ARCHIVE_OUTPUT = WORK / ('cardoctor-smoke-artifacts-' + RUN_ID)
ARTIFACT_ZIP = Path(shutil.make_archive(str(ARCHIVE_OUTPUT), 'zip', root_dir=OUTPUT_DIR))
print('Persistent run folder:', OUTPUT_DIR)
print('Optional download ZIP:', ARTIFACT_ZIP, '| bytes:', ARTIFACT_ZIP.stat().st_size)
print('No automatic local download. Choose D: when saving the result.')
```
