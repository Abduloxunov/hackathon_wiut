"""Stage/upload private VehiDE inputs. This tool never launches a paid job."""
import argparse,hashlib,importlib,json,os,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=Path("D:/hakathon_wiut/datasets/kaggle-audit")
STAGE=HERE/".runtime/vehide-input-v2"
STATE=HERE/".runtime/VEHIDE-UPLOAD-V2.json"
def digest(p):
 with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def stage():
 if HERE.drive.upper()!="D:":raise ValueError("Local artifacts must stay on D:")
 manifest=json.loads((DATA/"VEHIDE-PACKAGE-V2.json").read_text(encoding="utf-8"))
 archive=DATA/manifest["archive"]
 if archive.stat().st_size!=manifest["archive_bytes"] or digest(archive)!=manifest["archive_sha256"]:raise ValueError("Data package integrity mismatch")
 STAGE.mkdir(parents=True,exist_ok=True)
 target=STAGE/archive.name
 if not target.exists():
  try:os.link(archive,target)
  except OSError:shutil.copy2(archive,target)
 if digest(target)!=manifest["archive_sha256"]:raise ValueError("Existing staged archive differs")
 sources={"worker.py":HERE/"vehide-worker.py","bootstrap.py":HERE/"vehide-bootstrap.py","requirements-remote.txt":HERE/"requirements-remote.txt","data_tools.py":HERE.parent/"cardoctor-colab/data_tools.py"}
 for name,source in sources.items():
  dest=STAGE/name
  if dest.exists() and dest.read_bytes()!=source.read_bytes():raise ValueError("Existing staged code differs; preserve upload and use a new stage")
  if not dest.exists():shutil.copy2(source,dest)
 manifest.update(code_sha256={n:digest(STAGE/n) for n in sources},starting_weights="Official RF-DETR Nano pretrained, new seven-class head, fresh optimizer; never resume CarDD checkpoint",epochs=2,resolution=384,batch_size=2,grad_accum_steps=2,lr=1e-4,amp_dtype="bf16",seed=42,flavor="l4x1",timeout_minutes=40,job_launched=False,user_budget_usd=2.0,budget_note="Preparation only. launch_vehide_v2.py reconciles all finished project jobs including the corrupt-image failure against the user USD 2 hardware budget before this bounded retry.")
 payload=json.dumps(manifest,indent=2)+"\n"
 mp=STAGE/"manifest.json"
 if mp.exists() and mp.read_text(encoding="utf-8")!=payload:raise ValueError("Existing manifest differs")
 mp.write_text(payload,encoding="utf-8")
 if set(p.name for p in STAGE.iterdir())!={manifest["archive"],"manifest.json",*sources}:raise ValueError("Unexpected upload file")
 print(json.dumps({"stage":str(STAGE),"archive_bytes":manifest["archive_bytes"],"classes":manifest["classes"],"job_launched":False}),flush=True)
 return manifest

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("action",choices=["stage","upload","status"]);action=parser.parse_args().action
 if action=="stage":stage();return
 os.environ["HF_HUB_DISABLE_PROGRESS_BARS"]="1"
 from huggingface_hub import HfApi,get_token
 token=get_token()
 sys.path.insert(0,str(ROOT/"kb"));from runtime import configure
 configure();import huggingface_hub.constants;importlib.reload(huggingface_hub.constants)
 api=HfApi(token=token)
 parent=json.loads((HERE/".runtime/job.json").read_text(encoding="utf-8"))
 if api.whoami()["name"]!=parent["namespace"]:raise ValueError("HF account changed")
 if not api.bucket_info(parent["bucket_id"]).private:raise ValueError("Dataset bucket must remain private")
 if action=="status":
  print(STATE.read_text(encoding="utf-8") if STATE.exists() else "Not uploaded");return
 manifest=stage();prefix="vehide-native7-v2-input-"+manifest["archive_sha256"][:12]
 state={"bucket_id":parent["bucket_id"],"input_prefix":prefix,"archive_sha256":manifest["archive_sha256"],"stage":"uploading","job_launched":False}
 STATE.write_text(json.dumps(state,indent=2),encoding="utf-8")
 api.sync_bucket(str(STAGE),f'hf://buckets/{parent["bucket_id"]}/{prefix}',delete=False,token=token)
 files=[f for f in api.list_bucket_tree(parent["bucket_id"],prefix=prefix,recursive=True,token=token) if f.type=="file"]
 names={Path(f.path).name:f for f in files}
 if set(names)!={p.name for p in STAGE.iterdir()}:raise ValueError("Remote file inventory differs")
 for name,record in names.items():
  if record.size!=(STAGE/name).stat().st_size:raise ValueError("Remote byte count differs")
 verify=HERE/".runtime/vehide-upload-v2-verify";verify.mkdir(exist_ok=True)
 api.download_bucket_files(parent["bucket_id"],[(names["manifest.json"].path,str(verify/"manifest.json"))],token=token)
 if digest(verify/"manifest.json")!=digest(STAGE/"manifest.json"):raise ValueError("Remote manifest differs")
 state.update(stage="uploaded",remote_files=len(files),remote_total_bytes=sum(f.size for f in files),manifest_sha256=digest(STAGE/"manifest.json"),verification="SDK upload completed; remote inventory/sizes and downloaded manifest verified. Full cloud archive SHA will be checked by worker before training.")
 STATE.write_text(json.dumps(state,indent=2),encoding="utf-8");print(json.dumps(state,indent=2),flush=True)
if __name__=="__main__":main()
