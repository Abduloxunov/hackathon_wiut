"""Evaluate trusted CarDD checkpoints on the fixed official test split locally.
No training, model downloads, LLM calls or cloud GPU usage.
"""
import argparse,collections,hashlib,json,math,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/"kb"))
from runtime import configure
configure()
os.environ.update(HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1",MPLCONFIGDIR=str(ROOT/"kb/.runtime/cache/matplotlib"))
LABELS=["dent","scratch","crack","glass shatter","lamp broken","tire flat"]
DATA=Path("D:/hakathon_wiut/datasets/cardoctor-cardd-coco/test")
def sha(path):
 with path.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def iou(a,b):
 x1,y1,w1,h1=a;x2,y2,w2,h2=b
 inter=max(0,min(x1+w1,x2+w2)-max(x1,x2))*max(0,min(y1+h1,y2+h2)-max(y1,y2))
 union=w1*h1+w2*h2-inter
 return inter/union if union else 0.0
def fixed_threshold_metrics(data,preds,threshold=.35):
 truth=collections.defaultdict(list);guesses=collections.defaultdict(list)
 for a in data["annotations"]:
  if a.get("iscrowd",0):raise ValueError("This fixed-threshold evaluator does not implement crowd matching")
  truth[(a["image_id"],a["category_id"])].append(a["bbox"])
 for p in preds:
  if p["score"]>=threshold:guesses[(p["image_id"],p["category_id"])].append(p)
 counts={c["id"]:{"tp":0,"fp":0,"fn":0} for c in data["categories"]}
 for key in truth.keys()|guesses.keys():
  gt=truth[key];used=set();c=counts[key[1]]
  for pred in sorted(guesses[key],key=lambda p:-p["score"]):
   candidates=[(iou(pred["bbox"],box),i) for i,box in enumerate(gt) if i not in used]
   best=max(candidates,default=(0,None))
   if best[0]>=.5:used.add(best[1]);c["tp"]+=1
   else:c["fp"]+=1
  c["fn"]+=len(gt)-len(used)
 def finish(c):
  tp,fp,fn=c["tp"],c["fp"],c["fn"]
  return {**c,"precision":tp/(tp+fp) if tp+fp else 0.0,"recall":tp/(tp+fn) if tp+fn else 0.0,"f1":2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0}
 per={c["name"]:finish(counts[c["id"]]) for c in data["categories"]}
 totals={k:sum(c[k] for c in counts.values()) for k in ["tp","fp","fn"]}
 return {"confidence_threshold":threshold,"iou_threshold":.5,"matching":"Per-image per-class greedy in descending score, one GT match per prediction, no crowds","micro":finish(totals),"macro_f1":sum(v["f1"] for v in per.values())/len(per),"per_class":per}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--checkpoint",required=True);parser.add_argument("--tag",required=True,choices=["pilot","continuation"]);args=parser.parse_args()
 checkpoint=Path(args.checkpoint).resolve();output=HERE/".runtime/test-comparison";output.mkdir(exist_ok=True)
 inventory=json.loads((checkpoint.parent/"CHECKPOINTS.json").read_text(encoding="utf-8"));record=next(r for r in inventory if r["file"]==checkpoint.name)
 cksha=sha(checkpoint)
 if record["sha256"]!=cksha or record["bytes"]!=checkpoint.stat().st_size:raise ValueError("Checkpoint verification failed")
 annotation=DATA/"_annotations.coco.json";data=json.loads(annotation.read_text(encoding="utf-8"))
 if [(c["id"],c["name"]) for c in data["categories"]]!=list(enumerate(LABELS,1)) or len(data["images"])!=374 or len(data["annotations"])!=785:raise ValueError("Official test split/schema changed")
 images=sorted(data["images"],key=lambda im:im["id"])
 import torch
 torch.set_num_threads(4)
 from rfdetr import RFDETRNano
 from PIL import Image
 start=time.monotonic();model=RFDETRNano.from_checkpoint(str(checkpoint),device="cpu",amp=False,compile=False)
 if model.class_names!=LABELS:raise ValueError("Saved checkpoint label order differs")
 predictions=[];timings=[];image_hashes=[]
 with torch.inference_mode():
  for n,im in enumerate(images,1):
   path=DATA/im["file_name"];image_hashes.append([im["id"],sha(path)])
   with Image.open(path) as opened:
    image=opened.convert("RGB")
   if image.size!=(im["width"],im["height"]):raise ValueError("Image dimensions changed")
   t=time.monotonic();p=model.predict(image,threshold=0.0);timings.append(time.monotonic()-t)
   for box,score,cid in zip(p.xyxy,p.confidence,p.class_id):
    cid=int(cid);score=float(score)
    if not 0<=cid<6:continue
    x1,y1,x2,y2=[float(v) for v in box]
    if not all(math.isfinite(v) for v in [x1,y1,x2,y2,score]):raise ValueError("Nonfinite prediction")
    x1,x2=max(0,min(im["width"],x1)),max(0,min(im["width"],x2));y1,y2=max(0,min(im["height"],y1)),max(0,min(im["height"],y2))
    if x2<=x1 or y2<=y1:continue
    predictions.append({"image_id":im["id"],"category_id":cid+1,"bbox":[x1,y1,x2-x1,y2-y1],"score":score})
   if n%25==0:print(args.tag,"test images",n,"/",len(images),flush=True)
 (output/(args.tag+"-predictions.json")).write_text(json.dumps(predictions),encoding="utf-8")
 from pycocotools.coco import COCO
 from pycocotools.cocoeval import COCOeval
 import numpy as np,importlib.metadata
 gt=COCO(str(annotation));dt=gt.loadRes(predictions);evaluator=COCOeval(gt,dt,"bbox");evaluator.params.imgIds=[im["id"] for im in images];evaluator.evaluate();evaluator.accumulate();evaluator.summarize()
 precision=evaluator.eval["precision"];per_ap={}
 for k,c in enumerate(data["categories"]):
  values=precision[:,:,k,0,-1];p50=precision[0,:,k,0,-1]
  per_ap[c["name"]]={"mAP50_95":float(values[values>-1].mean()),"AP50":float(p50[p50>-1].mean())}
 summary={"tag":args.tag,"split":"Official CarDD test, not validation","checkpoint":str(checkpoint),"checkpoint_sha256":cksha,"annotation_sha256":sha(annotation),"image_hash_inventory_sha256":hashlib.sha256(json.dumps(image_hashes).encode()).hexdigest(),"images":374,"ground_truth_instances":785,"labels":LABELS,"coco_bbox":{"mAP50_95":float(evaluator.stats[0]),"mAP50":float(evaluator.stats[1]),"mAP75":float(evaluator.stats[2]),"mAR100":float(evaluator.stats[8]),"AP_small":float(evaluator.stats[3]),"AP_medium":float(evaluator.stats[4]),"AP_large":float(evaluator.stats[5]),"per_class":per_ap},"fixed_threshold":fixed_threshold_metrics(data,predictions),"evaluation":{"backend":"pycocotools "+importlib.metadata.version("pycocotools"),"iou_thresholds":evaluator.params.iouThrs.tolist(),"max_detections_per_category":evaluator.params.maxDets,"prediction_threshold_for_AP":0.0,"device":"CPU FP32, no compile","image_policy":"Original decoded pixels and sizes; no EXIF reorientation/thumbnail for benchmark","torch_threads":4,"training_performed":False,"llm_calls":0,"elapsed_seconds":time.monotonic()-start,"median_predict_seconds":float(np.median(timings)),"torch":torch.__version__,"rfdetr":importlib.metadata.version("rfdetr"),"scope":"Dataset test detection scores; not mechanical diagnosis accuracy or vehicle/incident-independent real-world validation"}}
 (output/(args.tag+"-metrics.json")).write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps({"tag":args.tag,"coco_bbox":summary["coco_bbox"],"fixed_threshold":summary["fixed_threshold"]},indent=2),flush=True)
if __name__=="__main__":main()
