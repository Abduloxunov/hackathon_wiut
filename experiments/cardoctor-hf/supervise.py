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
