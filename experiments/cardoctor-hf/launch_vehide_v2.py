"""One controlled VehiDE retry after strict image repair; no automatic paid resubmission."""
import argparse,hashlib,importlib,json,math,os,sys,time
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
STATE=HERE/".runtime/VEHIDE-JOB-V2.json"
PARENT_JOBS=["6acb05affee2c9007019128b","6acb137b095c57808931ad0d","6acb1a9cfee2c90070191e18","6acb23e3fee2c9007019213c"]
TERMINAL={"COMPLETED","ERROR","FAILED","CANCELED","CANCELLED","DELETED"}
def save(s):
 temp=STATE.with_suffix(".tmp");temp.write_text(json.dumps(s,indent=2),encoding="utf-8");temp.replace(STATE)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("action",choices=["preflight","launch","status","monitor","download","cancel"]);action=parser.parse_args().action
 os.environ["HF_HUB_DISABLE_PROGRESS_BARS"]="1"
 from huggingface_hub import HfApi,get_token,Volume
 token=get_token();sys.path.insert(0,str(ROOT/"kb"));from runtime import configure
 configure();import huggingface_hub.constants;importlib.reload(huggingface_hub.constants)
 api=HfApi(token=token);upload=json.loads((HERE/".runtime/VEHIDE-UPLOAD-V2.json").read_text(encoding="utf-8"))
 namespace=upload["bucket_id"].split("/")[0]
 if api.whoami()["name"]!=namespace:raise ValueError("HF account changed")
 if not api.bucket_info(upload["bucket_id"]).private:raise ValueError("Input/output bucket must be private")
 state=json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else None
 if action in ["preflight","launch"]:
  if upload["stage"]!="uploaded":raise ValueError("Verified data upload required")
  stage=HERE/".runtime/vehide-input-v2";manifest=json.loads((stage/"manifest.json").read_text(encoding="utf-8"))
  if hashlib.sha256((stage/"manifest.json").read_bytes()).hexdigest()!=upload["manifest_sha256"]:raise ValueError("Staged manifest changed")
  for name,digest in manifest["code_sha256"].items():
   if hashlib.sha256((stage/name).read_bytes()).hexdigest()!=digest:raise ValueError("Staged code changed")
  # Require the completed same-test comparison the user explicitly requested before another run.
  tests=[json.loads((HERE/f".runtime/test-comparison/{tag}-metrics.json").read_text(encoding="utf-8")) for tag in ["pilot","continuation"]]
  if tests[0]["image_hash_inventory_sha256"]!=tests[1]["image_hash_inventory_sha256"] or any(t["images"]!=374 for t in tests):raise ValueError("Incomplete or different test comparison")
  hardware=next(h for h in api.list_jobs_hardware() if h.name=="l4x1")
  if hardware.unit_label!="minute" or hardware.unit_cost_usd>0.013334:raise ValueError("Unexpected L4 pricing")
  prior=[]
  for jid in PARENT_JOBS:
   job=api.inspect_job(job_id=jid,namespace=namespace)
   if job.status.stage not in TERMINAL or job.finished_at is None or job.started_at is None:raise ValueError("Earlier job still active or timing unavailable")
   if getattr(job.flavor,"name",job.flavor)!="l4x1":raise ValueError("Prior hardware differs")
   # Include queue/scheduling time conservatively, and round EACH job up to a full minute.
   seconds=max((job.finished_at-job.created_at).total_seconds(),job.durations.total_secs)
   minutes=math.ceil(seconds/60)
   prior.append({"job_id":jid,"stage":job.status.stage,"created_utc":job.created_at.isoformat(),"finished_utc":job.finished_at.isoformat(),"rounded_total_minutes":minutes,"hardware_upper_usd":minutes*hardware.unit_cost_usd})
  previous=sum(r["hardware_upper_usd"] for r in prior);new_cap=40*hardware.unit_cost_usd;combined=previous+new_cap
  if combined>2.0:raise ValueError("Combined project hardware estimate/cap exceeds user $2 budget")
  audit={"checked_utc":datetime.now(timezone.utc).isoformat(),"user_hardware_budget_usd":2.0,"unit_cost_usd":hardware.unit_cost_usd,"unit":"minute","completed_jobs":prior,"completed_hardware_upper_usd":previous,"new_timeout_minutes":40,"new_hardware_cap_usd":new_cap,"combined_hardware_upper_usd":combined,"billing_scope":"Conservative hardware estimate using finished job durations, including scheduling; not an account billing statement or storage charge estimate. Credit availability is enforced by HF scheduler."}
  (HERE/".runtime/VEHIDE-BUDGET-V2.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
  print(json.dumps({"completed_hardware_upper_usd":previous,"new_hardware_cap_usd":new_cap,"combined_hardware_upper_usd":combined,"epochs":2,"train_images":manifest["splits"]["train"]["images"],"valid_images":manifest["splits"]["valid"]["images"]}),flush=True)
  if action=="preflight":return
  if state:
   if state.get("job_id"):print("Existing job preserved",state["job_url"],flush=True);return
   if state.get("submission_attempted"):raise ValueError("Submission outcome uncertain; inspect Jobs before retry")
  else:
   run=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ").lower()
   state={"namespace":namespace,"bucket_id":upload["bucket_id"],"input_prefix":upload["input_prefix"],"output_prefix":"output-vehide-native7-v2-"+run,"job_id":None,"run_id":run,"dataset":"VehiDE native7","timeout_minutes":40,"budget_audit":audit};save(state)
  api.batch_bucket_files(state["bucket_id"],add=[(json.dumps(audit,indent=2).encode(),state["output_prefix"]+"/BUDGET.json")],token=token)
  state["submission_attempted"]=True;save(state)
  job=api.run_job(namespace=namespace,image="pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime",flavor="l4x1",timeout="40m",name="cardoctor-vehide-native7-v2-"+state["run_id"],command=["python","-u","/input/bootstrap.py"],volumes=[Volume(type="bucket",source=state["bucket_id"],path=state["input_prefix"],mount_path="/input",read_only=True),Volume(type="bucket",source=state["bucket_id"],path=state["output_prefix"],mount_path="/output",read_only=False)],env={"HF_HOME":"/tmp/cardoctor-cache/hf","TORCH_HOME":"/tmp/cardoctor-cache/torch","PIP_CACHE_DIR":"/tmp/cardoctor-cache/pip","MPLCONFIGDIR":"/tmp/cardoctor-cache/matplotlib","PYTHONUNBUFFERED":"1","PYTHONIOENCODING":"utf-8","HF_HUB_DISABLE_TELEMETRY":"1","TOKENIZERS_PARALLELISM":"false","OMP_NUM_THREADS":"4"})
  state.update(job_id=job.id,stage=job.status.stage,job_url=f"https://huggingface.co/jobs/{namespace}/{job.id}");save(state);print(json.dumps({"job_url":state["job_url"],"stage":state["stage"]}),flush=True);return
 if not state or not state.get("job_id"):raise ValueError("No VehiDE job recorded")
 if action=="cancel":api.cancel_job(job_id=state["job_id"],namespace=namespace);print("Cancellation requested");return
 def download():
  target=HERE/".runtime/downloaded-vehide-native7-v2";target.mkdir(exist_ok=True)
  allowed={"BUDGET.json","CHECKPOINTS.json","DATA-AUDIT.json","ENVIRONMENT.txt","GPU.json","MATCHER-CHECK.json","metrics.csv","RESULT.md","RUN-STATUS.json","training_config.json","training.log","provenance.json","checkpoint_best_ema.pth","checkpoint_best_total.pth","installation.log","compiler-install.log"}
  fs=list(api.list_bucket_tree(state["bucket_id"],prefix=state["output_prefix"],recursive=True,token=token))
  plan=[(f.path,str(target/Path(f.path).name)) for f in fs if f.type=="file" and Path(f.path).name in allowed];api.download_bucket_files(state["bucket_id"],plan,token=token)
  verified=[]
  if (target/"CHECKPOINTS.json").exists():
   for r in json.loads((target/"CHECKPOINTS.json").read_text(encoding="utf-8")):
    p=target/r["file"]
    if p.exists():
     with p.open("rb") as f:digest=hashlib.file_digest(f,"sha256").hexdigest()
     if digest!=r["sha256"] or p.stat().st_size!=r["bytes"]:raise ValueError("Downloaded checkpoint mismatch")
     verified.append(r["file"])
  state.update(downloaded_to=str(target),verified_checkpoints=verified);save(state);print("Outputs saved on D:",target,flush=True)
 if action=="download":download();return
 deadline=time.monotonic()+45*60
 while True:
  job=api.inspect_job(job_id=state["job_id"],namespace=namespace);state.update(stage=job.status.stage,checked_utc=datetime.now(timezone.utc).isoformat());save(state);print(json.dumps({"stage":state["stage"],"job_url":state["job_url"]}),flush=True)
  if state["stage"] in TERMINAL:
   if action=="monitor":download()
   return
  if action=="status":return
  if time.monotonic()>deadline:api.cancel_job(job_id=state["job_id"],namespace=namespace);print("Monitor deadline: cancellation requested",flush=True);return
  time.sleep(60)
if __name__=="__main__":
 try:main()
 except Exception as exc:
  print("Stopped",type(exc).__name__,"HTTP",getattr(getattr(exc,"response",None),"status_code",None),flush=True)
  if isinstance(exc,(ValueError,RuntimeError)):print(str(exc),flush=True)
  raise SystemExit(1)
