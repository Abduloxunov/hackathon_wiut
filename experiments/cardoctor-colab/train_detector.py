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
