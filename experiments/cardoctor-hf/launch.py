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
