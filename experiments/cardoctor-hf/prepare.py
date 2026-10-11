"""Package exactly train/valid for private HF training. All local writes stay on D:."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = Path('D:/hakathon_wiut/datasets/cardoctor-cardd-coco')
STAGE = HERE / '.runtime/input'
sys.path.insert(0, str(HERE.parent / 'cardoctor-colab'))
from data_tools import audit_dataset, contained


def main():
    if HERE.drive.upper() != 'D:':
        raise ValueError('Local preparation must remain on D:')
    if STAGE.exists():
        raise ValueError('Existing prepared input is preserved; use the existing manifest or a fresh folder.')
    report, _ = audit_dataset(SOURCE)
    datasets = {}
    for split, expected in [('train', 2816), ('valid', 810)]:
        datasets[split] = json.loads((SOURCE / split / '_annotations.coco.json').read_text(encoding='utf-8'))
        if len(datasets[split]['images']) != expected:
            raise ValueError(f'{split}: expected {expected} images, refusing a smoke subset.')
    STAGE.mkdir(parents=True)
    archive = STAGE / 'cardd-train-valid.zip'
    # JPEG images are already compressed; ZIP_STORED avoids needless compression work.
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED, allowZip64=True) as z:
        z.write(SOURCE / 'provenance.json', 'cardd/provenance.json')
        for split, data in datasets.items():
            z.write(SOURCE / split / '_annotations.coco.json', f'cardd/{split}/_annotations.coco.json')
            for item in data['images']:
                image = contained(SOURCE / split, item['file_name'])
                z.write(image, f'cardd/{split}/{item["file_name"]}')
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('Archive CRC verification failed.')
        if any('/test/' in name for name in z.namelist()):
            raise ValueError('Official test data must not be sent to the training job.')
    with archive.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    manifest = {
        'archive': archive.name, 'archive_sha256': digest, 'archive_bytes': archive.stat().st_size,
        'train_images': 2816, 'valid_images': 810, 'official_test_included': False,
        'starting_weights': 'official RF-DETR Nano pretrained; fresh optimizer/scheduler',
        'epochs': 2, 'resolution': 384, 'batch_size': 2, 'grad_accum_steps': 2,
        'amp_dtype': 'bf16', 'lr': 0.0001, 'seed': 42, 'flavor': 'l4x1',
        'timeout_minutes': 75, 'hardware_max_usd_at_checked_price': 1.0,
        'budget_usd': 2.0, 'author_consent_status': 'unverified',
        'user_authorized_research_use': True,
    }
    files = ['worker.py', 'bootstrap.py', 'requirements-remote.txt']
    for name in files:
        shutil.copy2(HERE / name, STAGE / name)
    shutil.copy2(HERE.parent / 'cardoctor-colab/data_tools.py', STAGE / 'data_tools.py')
    manifest['code_sha256'] = {
        name: hashlib.sha256((STAGE / name).read_bytes()).hexdigest()
        for name in files + ['data_tools.py']
    }
    (STAGE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (HERE / '.runtime/DATA-AUDIT.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == '__main__':
    main()
