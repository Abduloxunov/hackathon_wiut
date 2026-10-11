"""Resume the verified full-data checkpoint for up to 12 total epochs."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import shutil
import time


def main():
    if os.name != 'posix':
        raise RuntimeError('Cloud GPU worker is not for local CPU training.')
    inputs, outputs = Path('/input'), Path('/output')
    continuation = json.loads(Path('/run-input/manifest.json').read_text(encoding='utf-8'))
    for name, expected in continuation['code_sha256'].items():
        if hashlib.sha256((Path('/run-input') / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Continuation source changed: ' + name)
    for name in ['checkpoint_best_ema.pth', 'checkpoint_best_total.pth']:
        shutil.copy2(Path('/resume') / name, outputs / name)
    resume = Path('/tmp/cardoctor-resume.ckpt')
    shutil.copyfile('/resume/checkpoint_1.ckpt', resume)
    with resume.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != continuation['resume_sha256']:
            raise ValueError('Resume checkpoint hash mismatch.')
    if resume.stat().st_size != continuation['resume_bytes']:
        raise ValueError('Resume checkpoint size mismatch.')
    (outputs / 'CONTINUATION.json').write_text(json.dumps(continuation, indent=2), encoding='utf-8')
    manifest = json.loads((inputs / 'manifest.json').read_text(encoding='utf-8'))
    archive = inputs / manifest['archive']
    print('Verifying full-data archive', flush=True)
    with archive.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != manifest['archive_sha256']:
            raise ValueError('Archive differs from the verified local package.')
    for name, expected in manifest['code_sha256'].items():
        if hashlib.sha256((inputs / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Code differs from the prepared manifest: {name}')
    import sys
    sys.path.insert(0, '/input')
    from data_tools import extract_dataset, audit_dataset
    # Extract to fast ephemeral local disk; outputs alone stay on the durable bucket mount.
    dataset = extract_dataset(archive, Path('/tmp/cardoctor-dataset'))
    if (dataset / 'test').exists():
        raise ValueError('The training job must not contain the official test split.')
    report, _ = audit_dataset(dataset)
    for split, expected in [('train', 2816), ('valid', 810)]:
        data = json.loads((dataset / split / '_annotations.coco.json').read_text(encoding='utf-8'))
        if len(data['images']) != expected:
            raise ValueError('This run requires the full train/validation splits.')
    for source in [inputs / 'manifest.json', dataset / 'provenance.json']:
        shutil.copy2(source, outputs / source.name)
    (outputs / 'DATA-AUDIT.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    import numpy as np
    import torch
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError('The selected L4 CUDA/BF16 GPU must be available.')
    if importlib.metadata.version('rfdetr') != '1.11.2':
        raise RuntimeError('Unexpected RF-DETR version.')
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)
    torch.set_float32_matmul_precision('high')
    gpu = {'name': torch.cuda.get_device_name(0), 'torch': torch.__version__,
           'cuda': torch.version.cuda, 'bf16_supported': torch.cuda.is_bf16_supported()}
    (outputs / 'GPU.json').write_text(json.dumps(gpu, indent=2), encoding='utf-8')
    print('GPU:', json.dumps(gpu), flush=True)
    # Compile and execute the exact assignment backend before the first training batch.
    from torch_linear_assignment import batch_linear_assignment
    cost = torch.tensor([[[0.0, 10.0], [10.0, 0.0]]], device='cuda')
    assignment = batch_linear_assignment(cost)
    torch.cuda.synchronize()
    if assignment.cpu().tolist() != [[0, 1]]:
        raise RuntimeError('CUDA matcher sanity check failed.')
    (outputs / 'MATCHER-CHECK.json').write_text(json.dumps({'passed': True, 'assignment': [[0, 1]]}), encoding='utf-8')
    print('CUDA matcher compiled and passed diagonal-assignment check', flush=True)
    from rfdetr import RFDETRNano
    model = RFDETRNano.from_checkpoint(str(resume), device='cuda')
    start = time.monotonic()
    classes = [report['categories'][cid] for cid in sorted(report['categories'])]
    model.train(dataset_dir=str(dataset), dataset_file='roboflow', class_names=classes,
                output_dir=str(outputs), epochs=12, resume=str(resume), batch_size=2, grad_accum_steps=2,
                resolution=384, lr=1e-4, device='cuda', amp_dtype='bf16', seed=42,
                num_workers=4, multi_scale=False, checkpoint_interval=2, log_per_class_metrics=True,
                run_test=False, tensorboard=False, wandb=False, early_stopping=True, early_stopping_patience=3, early_stopping_min_delta=0.002, early_stopping_use_ema=True,
                progress_bar='tqdm', notes={'purpose': 'Bounded full-state continuation to at most 12 total epochs; not final test accuracy',
                                         'starting_weights': continuation['resume_sha256']})
    elapsed = time.monotonic() - start
    checkpoints = []
    for p in sorted(outputs.iterdir()):
        if p.suffix in ['.pth', '.ckpt']:
            with p.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            checkpoints.append({'file': p.name, 'bytes': p.stat().st_size, 'sha256': digest})
    (outputs / 'CHECKPOINTS.json').write_text(json.dumps(checkpoints, indent=2), encoding='utf-8')
    (outputs / 'RESULT.md').write_text(
        '# Full-data pilot completed\n\n'
        'Resumed after epoch 2; at most 12 total epochs, on 2,816 train and 810 validation images. Official test data was absent.\n\n'
        f'Training call seconds: {elapsed:.1f}. GPU: {gpu["name"]}.\n\n'
        'See metrics.csv and training.log for actual validation measurements. '
        'Extra epochs do not guarantee improved accuracy. '
        'Review predictions and per-class failures before further training.\n', encoding='utf-8')
    print(f'Completed bounded continuation in {elapsed:.1f} seconds; {len(checkpoints)} checkpoint files persisted.', flush=True)


if __name__ == '__main__':
    main()
