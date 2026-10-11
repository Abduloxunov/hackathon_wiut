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
