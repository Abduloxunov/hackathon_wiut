# CarDoctor: Hugging Face full-data pilot

Prepared on 11 October 2026 following the user's choice to use Hugging Face. This is a supervised RF-DETR Nano experiment supporting the current CarDoctor CV/RAG project. Shared product code and team assignments are unchanged. No GitHub commit or push was made.

## Current execution status

Hugging Face account `abduloxunov` reports PRO. Initial Jobs access returned HTTP 403; after the user updated token permissions, Jobs access succeeded. A new bucket was created and verified private. The complete train/validation upload finished. The first L4 job failed before completing its first batch because the runtime image lacked GCC. A corrected second job has been submitted using the same dataset and a fresh output prefix. A local supervisor is running: once the upload completes, it submits exactly one bounded L4 job, records its URL, checks its status and downloads outputs to D: after the job ends.

**Recovery update: attempt 1 failed; attempt 2 was submitted at 09:41 Tashkent on 11 October 2026.** No training completion or model accuracy is established by submission. Consult `.runtime/PIPELINE-STATUS.json` and `.runtime/job.json` for current actual state. Successful preparation/upload is not successful training. `remote_completed` and downloaded `RESULT.md`, logs and metrics must be checked before claiming completion or accuracy. If submission fails for unavailable credits or permissions, the supervisor records that failure and does not create automatic paid retries.

The user previously set a $2 budget. Remaining credit balance has not been established by the accessible SDK; the service validates eligibility on submission. The L4 price was verified using the authenticated hardware API as $0.013333 per billed minute, approximately $0.80/hour. A 75-minute job allocation is approximately $1 in GPU charges, leaving budget headroom. Installation and cloud data preparation use the allocated hardware and are included in its billed time. Bucket storage has a free allowance; charges beyond an account's allowance are separate from GPU usage. We do not assert an audited final bill or verified account credit balance.

Keep this laptop awake with network access during upload and automatic submission. Once the job is confirmed submitted to Hugging Face, GPU work continues there independently of this laptop. The local supervisor needs the laptop awake to monitor/download results; if it closes afterward, saved cloud checkpoints remain in the private bucket and can be downloaded later.

## Experiment scope

| Setting | Value |
|---|---|
| Hardware | One Nvidia L4 (`l4x1`), 24 GB GPU memory |
| Model | RF-DETR Nano, `rfdetr[train]==1.11.2` |
| Starting weights | Official general pretrained model; fresh optimizer/scheduler |
| Training images | All 2,816 original training images |
| Validation images | All 810 original validation images |
| Official test split | All 374 images excluded from the upload and job |
| Classes | dent, scratch, crack, glass shatter, lamp broken, tire flat |
| Epochs | 2, a full-data speed/quality pilot |
| Input resolution | 384 |
| Physical batch / accumulation | 2 / 2, effective batch 4 |
| Learning rate / seed | 0.0001 / 42 |
| Precision | BF16, checked for GPU support |
| Data loader workers | 4 |
| Multiscale | Disabled |
| Checkpoint interval | Every epoch; best EMA retained by RF-DETR |
| GPU job timeout | 75 minutes |
| Dependency installation timeout | 15 minutes |
| Worker timeout | 55 minutes including cloud data verification/extraction |
| External monitoring | W&B and TensorBoard disabled |

These are intended settings, not measured GPU throughput. CUDA/GPU identity, actual installed versions and training metrics are recorded by the worker. The model does not resume the small-subset Colab optimizer/checkpoint. The older smoke weights are preserved separately.

The Colab smoke log's scheduler-order warning was reviewed against the pinned library: the optimizer and scheduler are configured through Lightning with a step-interval schedule. That static inspection does not establish the warning's cause. This run uses L4 BF16, which avoids FP16 gradient scaling, and retains logs so recurrence or non-finite losses can be investigated. No library scheduler implementation was patched or causal fix claimed.

## Verified local data package

Archive: `.runtime/input/cardd-train-valid.zip`.

- Bytes: **2,770,337,856** (2.77 GB decimal).
- SHA-256: `af1d7c23552168128d8e242249de5f06d07deedd351c71bb0a20082cd43170ff`.
- Original train/valid image bytes and COCO annotation bytes are preserved.
- Six categories are present; all 2,816/810 image entries are included.
- ZIP CRC, split image counts, absence of test photos, staging/source parity and Python syntax were verified.
- Dataset audit includes schema, image dimensions, finite in-bounds boxes and exact cross-split duplicate checks. Vehicle/incident independence and near-duplicate leakage are still unverified.
- The input upload allowlist contains only the archive, manifest, worker, bootstrap, requirements and data helper. It excludes `.env`, local API keys, unrelated project files and smoke checkpoint artifacts.

The user explicitly directed research use of CarDD. Metadata retains `user_authorized_research_use: true` separately from `permission_confirmed: false` / author consent unverified. Private storage does not assert commercial, redistribution or author-consent rights. See [dataset preparation](../../docs/CARDD-COLAB-PREPARATION.md) and [verified smoke results](../../docs/CARDOCTOR-SMOKE-REVIEW.md).

## Private storage and persistence

Private bucket: `abduloxunov/cardoctor-fullpilot-20261011t031655z`.

The input prefix is mounted read-only at `/input`; the output prefix is mounted read-write at `/output`. Both mounts are authorized by Hugging Face at job creation. No desktop token, OpenRouter key or `.env` is passed to the worker. The worker downloads only public pretrained model resources on the remote Linux runtime.

The archive is verified and extracted to ephemeral `/tmp` for local GPU data loading. Logs, metrics, status, provenance and checkpoints are written directly to durable `/output`. This avoids relying on a final upload before the ephemeral job disk is discarded. If a job is interrupted mid-epoch, the prior completed checkpoint can survive; checkpoint writes interrupted in progress must be hash/structure checked before use.

The Docker image tag is `pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime`. Package pins are in `requirements-remote.txt`; the image digest and all transitive package hashes are not locked, so this is not a completely frozen environment. `ENVIRONMENT.txt` records actual remote package versions. No training packages or CUDA wheels are installed on the laptop during cloud setup.

The supervisor waits up to three hours for this upload, submits one job, and polls that job while active. It has an additional local time guard for Starting/Running and records failures. The HF timeout remains effective when the laptop closes. Submission is recorded before the request; an uncertain submission outcome blocks automatic duplicate creation. A second supervisor is prevented by a local lock.

## Commands and recovery

Run from `D:/hakathon_wiut/finals/mdb-vision-finals`:

```powershell
# Current local pipeline status, including upload/submission state:
Get-Content experiments/cardoctor-hf/.runtime/PIPELINE-STATUS.json
Get-Content experiments/cardoctor-hf/.runtime/job.json

# After a job ID is recorded: inspect status and recent HF console logs.
& 'D:/hakathon_wiut/.venv/Scripts/python.exe' -B experiments/cardoctor-hf/launch.py status

# Cancel the recorded remote job explicitly.
& 'D:/hakathon_wiut/.venv/Scripts/python.exe' -B experiments/cardoctor-hf/launch.py cancel

# Download cloud outputs later if the laptop closed before automatic retrieval.
& 'D:/hakathon_wiut/.venv/Scripts/python.exe' -B experiments/cardoctor-hf/launch.py download
```

The current local download target is `.runtime/downloaded-output-attempt-2/` on D:. Attempt 1 failure logs are preserved separately in `.runtime/failed-attempt-1/`. `.runtime/` is ignored by Git. `training.log` is written to the private output bucket; HF console logs primarily show bootstrap stages. Download `RUN-STATUS.json`, `RESULT.md`, `metrics.csv`, `GPU.json`, `CHECKPOINTS.json` and actual checkpoint files before interpreting the run.

Preparation (`prepare.py`) requires a fresh input directory and preserves existing data. The corrected job and its supervisor are active; do not start parallel copies. `launch.py` refuses a second job when an ID is recorded, and refuses automatic resubmission after an ambiguous response. If that happens, inspect the account Jobs page first, then recover the known job ID rather than spending again.

## What to decide after the pilot

Measure the actual two-epoch training time and per-epoch metrics on L4. Inspect correctly matched boxes, missed thin defects, misclassifications and false positives on validation photos. Estimate a longer schedule from the measured speed and remaining credits; further paid runs are not automatically created by this supervisor. Preserve the official test split until model/threshold selection is complete. Two full-data epochs still do not establish product-ready quality.

## Primary provider references

- [Jobs pricing and included credits](https://huggingface.co/docs/hub/jobs-pricing).
- [Job configuration and private volumes](https://huggingface.co/docs/hub/jobs-configuration).
- [Training and durable checkpoint storage](https://huggingface.co/docs/hub/jobs-training).
- [Storage Buckets and free allowance](https://huggingface.co/docs/hub/storage-buckets).
- [Access tokens](https://huggingface.co/docs/hub/security-tokens).


## Diagnosed first-attempt failure and correction

First job: `6acb05affee2c9007019128b`. GPU was confirmed as NVIDIA L4, torch 2.6.0+cu124, CUDA 12.4, BF16 supported. Dataset extraction and checks passed. The first training batch failed inside Triton CUDA driver initialization with `RuntimeError: Failed to find C compiler`. No completed epoch, trained checkpoint or accuracy result was produced. Provider-reported durations were 59 scheduling seconds, 79 running seconds and 139 total seconds. Counting all 139 seconds conservatively at the hardware rate and rounding up to three minutes gives an estimated upper hardware charge of about $0.04; this is not an audited bill.

The corrected bootstrap installs GCC, G++ and C headers in the cloud if GCC is missing, sets CC explicitly and logs compiler installation. The worker compiles/runs a tiny CUDA assignment sanity check before starting training, proving that the formerly failing backend works rather than only checking the compiler binary. Code/manifest hashes were refreshed. The 2.77 GB data archive was reused; only small corrected source files were uploaded. Original code and failure logs are preserved locally and privately in the bucket.

Second job: [current HF job](https://huggingface.co/jobs/abduloxunov/6acb137b095c57808931ad0d). It mounts `output-attempt-2` at `/output`, preserving first-attempt outputs. Cumulative budget checking includes the prior conservative $0.04 and this job's approximately $1 allocation, together approximately $1.04 against the user's $2 budget. There are no automatic repeated paid attempts.

The first automatic result download also failed because a local child process lost access to the saved token after cache relocation. Explicit token forwarding to local SDK sync calls and local supervisor children fixes that; no token is passed to the GPU worker. A real authenticated recovery sync with caches on D: succeeded. The supervisor uses a separate lock for each recorded run.

Live verification of attempt 2: the CUDA matcher check passed (`MATCHER-CHECK.json`), the job remains RUNNING, and `metrics.csv` records epoch 0 through step 299. This demonstrates progress past the first-batch failure. No completed epoch, validation accuracy or final training success is claimed at this check. Compiler dependency installation has a bounded timeout; the worker timeout is reduced when necessary to retain a five-minute margin before the 75-minute job limit.

## Complete experiment source


### requirements-remote.txt

```text
torch==2.6.0
torchvision==0.21.0
rfdetr[train]==1.11.2
supervision==0.29.0
transformers==5.19.0
numpy==2.2.6
opencv-python-headless==4.11.0.86

```

### prepare.py

```python
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

```

### bootstrap.py

```python
"""HF-only bootstrap. Durable output volume is mounted before installation/training."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import time


def run(command, log_path, timeout):
    # Child processes write directly to durable logs: a blocked line read cannot bypass the timeout.
    with log_path.open('w', encoding='utf-8') as log:
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        try:
            return child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            child.terminate()
            try:
                child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=10)
            return 124


def main():
    if os.name != 'posix' or not Path('/input/manifest.json').exists():
        raise RuntimeError('This bootstrap runs only in the configured HF Linux job.')
    out = Path('/output')
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'RUN-STATUS.json').exists():
        raise RuntimeError('Use a new run output directory, preserving previous runs.')
    start = time.monotonic()
    state = {'stage': 'installing', 'completed_training': False}
    def save():
        state['elapsed_seconds'] = round(time.monotonic() - start, 2)
        (out / 'RUN-STATUS.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
        print(json.dumps(state), flush=True)
    save()
    # Runtime image lacks GCC, required by Triton's CUDA driver extension.
    if shutil.which('gcc') is None:
        state['stage'] = 'installing_compiler'
        save()
        code = run(['apt-get', 'update'], out / 'compiler-update.log', timeout=300)
        if not code:
            code = run(['apt-get', 'install', '-y', '--no-install-recommends', 'gcc', 'g++', 'libc6-dev'],
                       out / 'compiler-install.log', timeout=300)
        if code or shutil.which('gcc') is None:
            state.update(stage='compiler_install_failed', exit_code=code or 1)
            save()
            return code or 1
    os.environ['CC'] = shutil.which('gcc')
    code = run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check',
                '-r', '/input/requirements-remote.txt'], out / 'installation.log', timeout=900)
    if code:
        state.update(stage='installation_failed', exit_code=code)
        save()
        return code
    with (out / 'ENVIRONMENT.txt').open('w', encoding='utf-8') as f:
        subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=f, check=True)
    # Installed dependencies remain in the cloud; no desktop C: download occurs.
    state['stage'] = 'training'
    save()
    code = run([sys.executable, '-u', '/input/worker.py'], out / 'training.log', timeout=max(1, min(3300, int(4200 - (time.monotonic() - start)))))
    state.update(stage='completed' if code == 0 else 'training_failed_or_timed_out',
                 completed_training=code == 0, exit_code=code)
    save()
    return code


if __name__ == '__main__':
    raise SystemExit(main())

```

### worker.py

```python
"""Two full-data epochs on HF L4; independent official test data is absent."""
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
    manifest = json.loads((inputs / 'manifest.json').read_text(encoding='utf-8'))
    archive = inputs / manifest['archive']
    print('Verifying full-data archive', flush=True)
    with archive.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != manifest['archive_sha256']:
            raise ValueError('Archive differs from the verified local package.')
    for name, expected in manifest['code_sha256'].items():
        if hashlib.sha256((inputs / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Code differs from the prepared manifest: {name}')
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
    model = RFDETRNano(device='cuda')
    start = time.monotonic()
    classes = [report['categories'][cid] for cid in sorted(report['categories'])]
    model.train(dataset_dir=str(dataset), dataset_file='roboflow', class_names=classes,
                output_dir=str(outputs), epochs=2, batch_size=2, grad_accum_steps=2,
                resolution=384, lr=1e-4, device='cuda', amp_dtype='bf16', seed=42,
                num_workers=4, multi_scale=False, checkpoint_interval=1,
                run_test=False, tensorboard=False, wandb=False, early_stopping=False,
                progress_bar='tqdm', notes={'purpose': 'Full-data two-epoch pilot; not final accuracy',
                                         'starting_weights': manifest['starting_weights']})
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
        'Two epochs on 2,816 train and 810 validation images. Official test data was absent.\n\n'
        f'Training call seconds: {elapsed:.1f}. GPU: {gpu["name"]}.\n\n'
        'See metrics.csv and training.log for actual validation measurements. '
        'Two epochs are a pilot, not a claim of useful damage accuracy. '
        'Review predictions and per-class failures before further training.\n', encoding='utf-8')
    print(f'Completed two full epochs in {elapsed:.1f} seconds; {len(checkpoints)} checkpoint files persisted.', flush=True)


if __name__ == '__main__':
    main()

```

### launch.py

```python
"""Prepare/upload/launch one bounded private Hugging Face L4 pilot; never push GitHub."""
import argparse
from datetime import datetime,timezone
import hashlib,json,math,os
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGE=HERE/'.runtime/input'
STATE=HERE/'.runtime/job.json'
ALLOWED={'cardd-train-valid.zip','manifest.json','worker.py','bootstrap.py','requirements-remote.txt','data_tools.py'}

def save(state):
    STATE.parent.mkdir(parents=True,exist_ok=True)
    temp=STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(state,indent=2)+chr(10),encoding='utf-8')
    temp.replace(STATE)

def check_bundle():
    if {p.name for p in STAGE.iterdir()}!=ALLOWED:raise ValueError('Input contains unexpected files; refusing upload.')
    m=json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
    if m['epochs']!=2 or m['train_images']!=2816 or m['valid_images']!=810 or m['official_test_included']:raise ValueError('Unexpected training scope.')
    for name,expected in m['code_sha256'].items():
        if hashlib.sha256((STAGE/name).read_bytes()).hexdigest()!=expected:raise ValueError('Prepared code changed: '+name)
    with (STAGE/m['archive']).open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=m['archive_sha256']:raise ValueError('Prepared archive changed.')
    return m

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['preflight','upload','launch','status','cancel','download'])
    args=parser.parse_args()
    if HERE.drive.upper()!='D:':raise ValueError('Local caches and files must remain on D:')
    from huggingface_hub import HfApi,get_token,Volume
    # Read the existing login before redirecting all mutable cache/runtime paths to D:.
    token=get_token()
    sys.path.insert(0,str(ROOT/'kb'))
    from runtime import configure
    configure()
    # Hub constants may have been initialized while reading the existing login.
    import importlib
    import huggingface_hub.constants
    importlib.reload(huggingface_hub.constants)
    api=HfApi(token=token)
    user=api.whoami();namespace=user['name']
    print('HF account:',namespace,'PRO:',user.get('isPro'),flush=True)
    state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else None
    if state and state['namespace']!=namespace:raise ValueError('Login account changed; preserving the existing run.')
    if args.action in ['preflight','upload','launch']:
        list(api.list_jobs(namespace=namespace))
        flavor=next(h for h in api.list_jobs_hardware() if h.name=='l4x1')
        # Current hardware price is checked again, not assumed from a stale documentation table.
        maximum=math.ceil(75)*flavor.unit_cost_usd
        if flavor.unit_label!='minute' or maximum>1.01:raise ValueError('L4 price exceeds the prepared $1 hardware cap.')
        print('L4 hourly USD:',round(flavor.unit_cost_usd*60,4),'75-minute hardware cap USD:',round(maximum,4),flush=True)
        if args.action=='preflight':return
    if args.action in ['status','cancel','download']:
        if not state or not state.get('job_id'):raise ValueError('No submitted job is recorded.')
        if args.action=='cancel':api.cancel_job(job_id=state['job_id'],namespace=namespace);print('Cancellation requested.');return
        if args.action=='download':
            target=HERE/'.runtime'/('downloaded-'+state.get('output_prefix','output'))
            api.sync_bucket(f'hf://buckets/{state["bucket_id"]}/{state.get("output_prefix","output")}',str(target),delete=False,token=token)
            print('Outputs downloaded to D:',target);return
        job=api.inspect_job(job_id=state['job_id'],namespace=namespace)
        print('Job:',job.id,'status:',job.status.stage,'message:',job.status.message,flush=True)
        print('URL:',state['job_url'],flush=True)
        for line in api.fetch_job_logs(job_id=job.id,namespace=namespace,follow=False,tail=30):print(line,end='')
        return
    manifest=check_bundle()
    if not state:
        run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ').lower()
        state={'namespace':namespace,'run_id':run,'bucket_id':namespace+'/cardoctor-fullpilot-'+run,
            'uploaded':False,'job_id':None,'flavor':'l4x1','timeout_minutes':75,'epochs':2,
            'budget_usd':2.0,'hardware_max_usd':round(maximum,6),'archive_sha256':manifest['archive_sha256']}
        save(state)
    if state.get('job_id'):
        print('Existing job preserved; refusing to create a duplicate:',state['job_url']);return
    if state['archive_sha256']!=manifest['archive_sha256']:raise ValueError('Prepared data differs from the recorded run.')
    api.create_bucket(state['bucket_id'],private=True,exist_ok=True)
    if not api.bucket_info(state['bucket_id']).private:raise ValueError('Training storage must be private.')
    if not state['uploaded']:
        print('Uploading checked input to private storage; no GPU billing during this local upload.',flush=True)
        api.sync_bucket(str(STAGE),f'hf://buckets/{state["bucket_id"]}/input',delete=False,token=token)
        api.batch_bucket_files(state['bucket_id'],add=[(b'Private CarDoctor run output', 'output/.keep')])
        state['uploaded']=True;save(state)
    if args.action=='upload':print('Private upload complete; no GPU job submitted.');return
    if state.get('submission_attempted'):
        raise RuntimeError('A prior submission has uncertain outcome. Inspect account Jobs before retrying; no automatic duplicate.')
    if maximum + state.get('prior_compute_upper_usd', 0) > state.get('budget_usd', 2):
        raise ValueError('Combined run hardware limits exceed the user budget.')
    state['submission_attempted']=True;save(state)
    job=api.run_job(namespace=namespace,image='pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime',
        command=['python','-u','/input/bootstrap.py'],flavor='l4x1',timeout='75m',
        name='cardoctor-fullpilot-'+state['run_id'],
        volumes=[Volume(type='bucket',source=state['bucket_id'],path='input',mount_path='/input',read_only=True),
                 Volume(type='bucket',source=state['bucket_id'],path=state.get('output_prefix','output'),mount_path='/output',read_only=False)],
        env={'HF_HOME':'/tmp/cardoctor-cache/hf','TORCH_HOME':'/tmp/cardoctor-cache/torch',
             'PIP_CACHE_DIR':'/tmp/cardoctor-cache/pip','MPLCONFIGDIR':'/tmp/cardoctor-cache/matplotlib',
             'PYTHONUNBUFFERED':'1','PYTHONIOENCODING':'utf-8','HF_HUB_DISABLE_TELEMETRY':'1',
             'TOKENIZERS_PARALLELISM':'false','OMP_NUM_THREADS':'4'})
    state.update(job_id=job.id,job_url=f'https://huggingface.co/jobs/{namespace}/{job.id}',stage=job.status.stage)
    save(state)
    print('Submitted:',state['job_url'],'status:',job.status.stage,flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        # Do not echo request headers, environment variables or token-bearing exception text.
        print('Stopped:',type(exc).__name__,'HTTP',getattr(getattr(exc,'response',None),'status_code',None),flush=True)
        if isinstance(exc,(ValueError,RuntimeError)):print(str(exc),flush=True)
        raise SystemExit(1)

```

### supervise.py

```python
"""Finish the current upload, submit one bounded job, monitor it and download private results to D:."""
import json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
STATE=HERE/'.runtime/job.json'
STATUS=HERE/'.runtime/PIPELINE-STATUS.json'

def write(stage,**extra):
    STATUS.parent.mkdir(parents=True,exist_ok=True)
    data={'stage':stage,'updated_utc':datetime.now(timezone.utc).isoformat(),**extra}
    STATUS.write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps(data),flush=True)

def action(name):
    return subprocess.run([sys.executable,'-B',str(HERE/'launch.py'),name],check=False).returncode

def main():
    # Single supervisor; an existing lock prevents a second accidental launch loop.
    lock=HERE/('.runtime/supervisor-'+json.loads(STATE.read_text(encoding='utf-8'))['run_id']+'.lock')
    with lock.open('x',encoding='utf-8') as f:f.write(str(os.getpid()))
    write('waiting_for_private_upload')
    limit=time.monotonic()+3*3600
    while time.monotonic()<limit:
        state=json.loads(STATE.read_text(encoding='utf-8'))
        if state.get('uploaded'):break
        time.sleep(15)
    else:write('upload_wait_expired',training_started=False);return 1
    write('submitting_bounded_job')
    if action('launch'):
        write('submission_failed',training_started=False);return 1
    state=json.loads(STATE.read_text(encoding='utf-8'))
    if not state.get('job_id'):write('submission_not_confirmed');return 1
    write('job_submitted',job_url=state['job_url'])
    from huggingface_hub import get_token,HfApi
    token=get_token();sys.path.insert(0,str(HERE.parents[1]/'kb'))
    from runtime import configure
    configure()
    # Forward credentials only to local child processes; the remote job gets no token.
    os.environ['HF_TOKEN'] = token
    import importlib,huggingface_hub.constants
    importlib.reload(huggingface_hub.constants)
    api=HfApi(token=token)
    first_billed=None
    terminal={'COMPLETED','ERROR','FAILED','CANCELED','CANCELLED','DELETED'}
    deadline=time.monotonic()+2*3600
    while time.monotonic()<deadline:
        job=api.inspect_job(job_id=state['job_id'],namespace=state['namespace'])
        stage=job.status.stage
        write('remote_'+stage.lower(),job_url=state['job_url'])
        if stage in ['STARTING','RUNNING']:
            if first_billed is None:first_billed=time.monotonic()
            if time.monotonic()-first_billed>=75*60:
                api.cancel_job(job_id=job.id,namespace=state['namespace'])
                write('local_time_guard_cancel_requested',job_url=state['job_url'])
        if stage in terminal:
            result=action('download')
            write('finished',remote_stage=stage,download_ok=result==0,job_url=state['job_url'])
            return 0 if stage=='COMPLETED' and result==0 else 1
        time.sleep(60)
    api.cancel_job(job_id=state['job_id'],namespace=state['namespace'])
    write('monitor_deadline_cancel_requested',job_url=state['job_url'])
    return 1

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        write('supervisor_failed',exception_type=type(exc).__name__,http_status=getattr(getattr(exc,'response',None),'status_code',None))
        raise SystemExit(1)

```
