# Bounded training continuation

Started 11 October 2026 after the user asked whether scores could improve and whether the short run was wrong. This is a follow-on experiment, not a claim of improved results.

## Why the pilot completed quickly

The actual cloud audit counted 2,816 train images / 6,211 labelled objects and 810 validation images / 1,744 labelled objects, covering all six CarDD categories. Training logs show 1,408 microbatches per epoch (batch size 2) and 405 validation batches, with both epochs completed. Gradient accumulation 2 gives 704 optimizer updates per epoch; the full checkpoint records epoch index 1 and global optimizer step 1,408. The trainer explicitly stopped at `max_epochs=2`.

RF-DETR Nano started from official pretrained weights, used 384-pixel inputs and BF16 on an NVIDIA L4. Training-call elapsed time was 313.9 seconds. The evidence does not indicate a tiny subset, CPU execution, skipped epochs or evaluation on the training split. It does not establish absence of all modelling/evaluation problems: near-duplicate/vehicle grouping, domain shift, class imbalance, field reliability and final test performance remain unresolved.

Validation mAP@50-95 improved from .480928 to .538297; macro F1 rose from .564962 to .631578. This motivates trying additional epochs; improvement is not guaranteed.

## New run

Job: https://huggingface.co/jobs/abduloxunov/6acb1a9cfee2c90070191e18

Resume source: the full trainer `checkpoint_1.ckpt`, SHA-256 `6a66d21e64935767947bb1cedd662de8bd58d8da38ff9942b0febaa8bc99e25e`, 483,445,491 bytes. Local inspection verified epoch 1, step 1408, optimizer state, LR scheduler and EMA callback state. We use full-state resume, rather than loading only inference weights. See [official RF-DETR training documentation](https://rfdetr.roboflow.com/learn/train/) and [advanced resume documentation](https://github.com/roboflow/rf-detr/blob/develop/docs/learn/train/advanced.md).

- Maximum total epochs: 12, meaning at most 10 additional epochs.
- Same original training/validation split, Nano architecture, 384 resolution, batch 2, accumulation 2, LR settings and seed.
- Per-class metric logging enabled to expose weak classes.
- Early stopping: patience 3, minimum mAP improvement .002, monitoring EMA.
- Cloud job limit: 40 minutes; worker time bounded within that limit.
- Expected training duration, extrapolated from pilot: roughly 25-35 minutes including ordinary setup; scheduling and transfer can vary.
- Live price checked through the HF hardware API: new hardware allocation cap $0.533320. Conservative prior reserved upper bound $1.039974; combined $1.573294, below the user's $2 hardware budget. This is not audited account billing or remaining credit.
- Private bucket reused; only four small source/manifest files were uploaded. Existing dataset and resume outputs are mounted read-only. All new outputs use a separate prefix.
- No HF credential is passed into the job; bucket mount authentication is handled by the service. Local saved login is read before D: cache redirection.
- Working app and pilot weights remain unchanged. No automatic replacement without score comparison and a real inference check.
- No official test data in the cloud training archive; no new held-out test claim.

## Commands

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B experiments/cardoctor-hf/continuation-launch.py status
D:\hakathon_wiut\.venv\Scripts\python.exe -B experiments/cardoctor-hf/continuation-launch.py cancel
D:\hakathon_wiut\.venv\Scripts\python.exe -B experiments/cardoctor-hf/continuation-launch.py download
```

The local monitor polls every minute and downloads logs, metadata and selected weights to `experiments/cardoctor-hf/.runtime/downloaded-continuation-12` when the job reaches a terminal state. It verifies hashes against the completed output manifest. It does not start another paid job or retry a failed submission. Do not start a second monitor unnecessarily.

## Selection after training

Compare best validation mAP@50-95 with the pilot .538297, inspect per-class metrics and diverse predictions. Keep the old checkpoint if the new result is worse or shows regression. F1 is a macro average selected through a validation confidence sweep; it is not automatically the app's .35-threshold F1. Choose the model/threshold using validation, then evaluate the separate test set for final reporting. Report validation and test results separately.

## Complete continuation source

The original input worker/data-tools/requirements and bootstrap are preserved in the main HF README. The files below are the full added implementation.


### continuation-worker.py

```python
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
```

### continuation-bootstrap.py

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
    if os.name != 'posix' or not Path('/run-input/manifest.json').exists():
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
                '-r', '/run-input/requirements-remote.txt'], out / 'installation.log', timeout=900)
    if code:
        state.update(stage='installation_failed', exit_code=code)
        save()
        return code
    with (out / 'ENVIRONMENT.txt').open('w', encoding='utf-8') as f:
        subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=f, check=True)
    # Installed dependencies remain in the cloud; no desktop C: download occurs.
    state['stage'] = 'training'
    save()
    code = run([sys.executable, '-u', '/run-input/continuation-worker.py'], out / 'training.log', timeout=max(1, min(2100, int(2280 - (time.monotonic() - start)))))
    state.update(stage='completed' if code == 0 else 'training_failed_or_timed_out',
                 completed_training=code == 0, exit_code=code)
    save()
    return code


if __name__ == '__main__':
    raise SystemExit(main())
```

### continuation-launch.py

```python
"""One budget-bounded HF continuation; preserves pilot/app; no paid retries."""
import argparse,hashlib,json,math,os,sys,time
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STATE=HERE/'.runtime/CONTINUATION-JOB.json'
STAGE=HERE/'.runtime/continuation-input'
def save(state):
    temp=STATE.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2),encoding='utf-8');temp.replace(STATE)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['preflight','launch','status','monitor','download','cancel'])
    action=parser.parse_args().action
    from huggingface_hub import HfApi,get_token,Volume
    token=get_token()
    sys.path.insert(0,str(ROOT/'kb'))
    from runtime import configure
    configure()
    import importlib,huggingface_hub.constants
    importlib.reload(huggingface_hub.constants)
    api=HfApi(token=token)
    manifest=json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
    parent=json.loads((HERE/'.runtime/job.json').read_text(encoding='utf-8'))
    state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else None
    namespace=api.whoami()['name']
    if namespace!=parent['namespace']:raise ValueError('Account changed; stopping.')
    if action in ['preflight','launch']:
        if set(p.name for p in STAGE.iterdir())!={'manifest.json',*manifest['code_sha256']}:raise ValueError('Unexpected upload files.')
        for name,expected in manifest['code_sha256'].items():
            if hashlib.sha256((STAGE/name).read_bytes()).hexdigest()!=expected:raise ValueError('Source mismatch.')
        if api.inspect_job(job_id=parent['job_id'],namespace=namespace).status.stage!='COMPLETED':raise ValueError('Parent job is not completed.')
        if not api.bucket_info(parent['bucket_id']).private:raise ValueError('Bucket must be private.')
        flavor=next(h for h in api.list_jobs_hardware() if h.name=='l4x1')
        cap=math.ceil(manifest['timeout_minutes'])*flavor.unit_cost_usd
        combined=manifest['prior_reserved_hardware_upper_usd']+cap
        if flavor.unit_label!='minute' or cap>0.54 or combined>manifest['user_budget_usd']:raise ValueError('Combined hardware cap exceeds budget.')
        print(json.dumps({'new_hardware_cap_usd':round(cap,6),'combined_reserved_upper_usd':round(combined,6),'additional_epochs_max':10,'timeout_minutes':40}),flush=True)
        if action=='preflight':return
        if state:
            if state.get('job_id'):print('Existing continuation preserved:',state['job_url'],flush=True);return
            if state.get('submission_attempted'):raise ValueError('Submission outcome uncertain; inspect Jobs before retrying.')
        else:
            run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ').lower()
            state={'namespace':namespace,'bucket_id':parent['bucket_id'],'run_id':run,'input_prefix':'continuation-input-'+run,'output_prefix':'output-continuation-'+run,'job_id':None,'timeout_minutes':40,'hardware_cap_usd':cap,'combined_hardware_upper_usd':combined,'parent_job_id':parent['job_id']}
            save(state)
        api.sync_bucket(str(STAGE),f'hf://buckets/{state["bucket_id"]}/{state["input_prefix"]}',delete=False,token=token)
        api.batch_bucket_files(state['bucket_id'],add=[(b'Private continuation output',state['output_prefix']+'/.keep')])
        state['submission_attempted']=True;save(state)
        job=api.run_job(namespace=namespace,image='pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime',flavor='l4x1',timeout='40m',name='cardoctor-continuation-'+state['run_id'],command=['python','-u','/run-input/continuation-bootstrap.py'],
            volumes=[Volume(type='bucket',source=state['bucket_id'],path='input',mount_path='/input',read_only=True),Volume(type='bucket',source=state['bucket_id'],path=state['input_prefix'],mount_path='/run-input',read_only=True),Volume(type='bucket',source=state['bucket_id'],path=parent['output_prefix'],mount_path='/resume',read_only=True),Volume(type='bucket',source=state['bucket_id'],path=state['output_prefix'],mount_path='/output',read_only=False)],
            env={'HF_HOME':'/tmp/cardoctor-cache/hf','TORCH_HOME':'/tmp/cardoctor-cache/torch','PIP_CACHE_DIR':'/tmp/cardoctor-cache/pip','MPLCONFIGDIR':'/tmp/cardoctor-cache/matplotlib','PYTHONUNBUFFERED':'1','PYTHONIOENCODING':'utf-8','HF_HUB_DISABLE_TELEMETRY':'1','TOKENIZERS_PARALLELISM':'false','OMP_NUM_THREADS':'4'})
        state.update(job_id=job.id,job_url=f'https://huggingface.co/jobs/{namespace}/{job.id}',stage=job.status.stage);save(state);print(json.dumps({'job_url':state['job_url'],'stage':state['stage']}),flush=True);return
    if not state or not state.get('job_id'):raise ValueError('No continuation recorded.')
    if action=='cancel':api.cancel_job(job_id=state['job_id'],namespace=namespace);print('Cancellation requested.');return
    def download():
        target=HERE/'.runtime/downloaded-continuation-12';target.mkdir(exist_ok=True)
        files=list(api.list_bucket_tree(state['bucket_id'],prefix=state['output_prefix'],recursive=True,token=token))
        allowed={'CHECKPOINTS.json','CONTINUATION.json','DATA-AUDIT.json','ENVIRONMENT.txt','GPU.json','MATCHER-CHECK.json','metrics.csv','RESULT.md','RUN-STATUS.json','training_config.json','training.log','provenance.json','checkpoint_best_ema.pth','checkpoint_best_total.pth'}
        plan=[(f.path,str(target/Path(f.path).name)) for f in files if f.type=='file' and Path(f.path).name in allowed]
        api.download_bucket_files(state['bucket_id'],plan,token=token)
        if (target/'CHECKPOINTS.json').exists():
            for record in json.loads((target/'CHECKPOINTS.json').read_text(encoding='utf-8')):
                path=target/record['file']
                if path.exists():
                    with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
                    if digest!=record['sha256'] or path.stat().st_size!=record['bytes']:raise ValueError('Downloaded checkpoint differs.')
        state['downloaded_to']=str(target);save(state);print('Outputs saved on D:',target,flush=True)
    if action=='download':download();return
    terminal={'COMPLETED','ERROR','FAILED','CANCELED','CANCELLED','DELETED'}
    deadline=time.monotonic()+50*60
    while True:
        job=api.inspect_job(job_id=state['job_id'],namespace=namespace)
        state.update(stage=job.status.stage,checked_utc=datetime.now(timezone.utc).isoformat());save(state)
        print(json.dumps({'stage':state['stage'],'job_url':state['job_url']}),flush=True)
        if state['stage'] in terminal:
            if action=='monitor':download()
            return
        if action=='status':
            for line in api.fetch_job_logs(job_id=job.id,namespace=namespace,follow=False,tail=15):print(line,end='')
            return
        if time.monotonic()>deadline:
            api.cancel_job(job_id=state['job_id'],namespace=namespace);print('Monitor deadline cancellation requested.',flush=True);return
        time.sleep(60)
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Stopped:',type(exc).__name__,'HTTP',getattr(getattr(exc,'response',None),'status_code',None),flush=True)
        if isinstance(exc,(ValueError,RuntimeError)):print(str(exc),flush=True)
        raise SystemExit(1)
```


## Completion verified on 11 October 2026

Job completed successfully: all ten additional epochs ran, for 12 total. Bootstrap elapsed 1593.65 seconds; training call 1505.7 seconds. The best EMA checkpoint by validation mAP50-95 was selected at human epoch 10 (CSV epoch 9), with validation mAP50 0.7396975, mAP50-95 0.5930983 and macro F1 0.7266563 at the trainer-selected threshold. The final human epoch 12 had mAP50 0.7423880 but lower mAP50-95 0.5910695. The last epoch and the selected checkpoint are different.

Verified best EMA SHA-256: `3b2addfe24b78c764d9f5758c74f0d3f8e0ecb646c21294fa39c968d811938b4`. Downloaded logs, metrics and best EMA/total checkpoints are in `.runtime/downloaded-continuation-12/`. Official test evaluation was then requested locally; see `docs/CARDOCTOR-MODEL-COMPARISON.md` after it is complete. No VehiDE job was started.
