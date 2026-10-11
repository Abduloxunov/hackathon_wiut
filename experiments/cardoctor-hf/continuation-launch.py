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
