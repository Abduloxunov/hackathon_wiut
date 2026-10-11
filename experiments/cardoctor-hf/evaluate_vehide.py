"""Offline CPU evaluation of a trusted VehiDE checkpoint on publisher validation.
This is not an independent test set: validation also selected the checkpoint.
No training, cloud GPU or model/API downloads are performed.
"""
import argparse,hashlib,importlib.metadata,json,math,os,statistics,time
from pathlib import Path
from evaluate_cardd import fixed_threshold_metrics,sha
os.environ.update(HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1")
HERE=Path(__file__).resolve().parent
DATA=Path("D:/hakathon_wiut/datasets/kaggle-audit/vehide-rfdetr-native7-v2/valid")
LABELS=["be_den","mat_bo_phan","mop_lom","rach","thung","tray_son","vo_kinh"]
def coco_bbox_metrics(data,predictions):
 from pycocotools.coco import COCO
 from pycocotools.cocoeval import COCOeval
 # COCOeval uses zero as an unmatched sentinel, so annotation ID 0 breaks matching.
 # Only evaluator-local annotation identities change; pixels, boxes, image/category IDs stay identical.
 gt=COCO();gt.dataset={**data,"annotations":[{**a,"id":i} for i,a in enumerate(data["annotations"],1)]};gt.createIndex()
 dt=gt.loadRes(predictions);ev=COCOeval(gt,dt,"bbox");ev.params.imgIds=[im["id"] for im in data["images"]]
 ev.evaluate();ev.accumulate();ev.summarize();pr=ev.eval["precision"];per={}
 for k,c in enumerate(data["categories"]):
  a=pr[:,:,k,0,-1];b=pr[0,:,k,0,-1]
  per[c["name"]]={"mAP50_95":float(a[a>-1].mean()),"AP50":float(b[b>-1].mean())}
 return {"mAP50_95":float(ev.stats[0]),"mAP50":float(ev.stats[1]),"mAP75":float(ev.stats[2]),"AP_small":float(ev.stats[3]),"AP_medium":float(ev.stats[4]),"AP_large":float(ev.stats[5]),"mAR100":float(ev.stats[8]),"per_class":per},{"iou_thresholds":ev.params.iouThrs.tolist(),"max_detections_per_category":ev.params.maxDets}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--checkpoint",type=Path,default=HERE/".runtime/downloaded-vehide-native7-v2/checkpoint_best_ema.pth")
 parser.add_argument("--output-dir",type=Path,default=HERE/".runtime/vehide-validation-evaluation")
 args=parser.parse_args();checkpoint=args.checkpoint.resolve()
 out=args.output_dir.resolve()
 if out.drive.upper()!="D:":raise ValueError("Evaluation artifacts must stay on D:")
 out.mkdir(parents=True,exist_ok=True)
 if (out/"metrics.json").exists():raise ValueError("Completed evaluation exists; preserve it")
 inventory=json.loads((checkpoint.parent/"CHECKPOINTS.json").read_text(encoding="utf-8"));entry=next(x for x in inventory if x["file"]==checkpoint.name)
 cksha=sha(checkpoint)
 if cksha!=entry["sha256"] or checkpoint.stat().st_size!=entry["bytes"]:raise ValueError("Checkpoint integrity differs")
 annotation=DATA/"_annotations.coco.json";data=json.loads(annotation.read_text(encoding="utf-8"))
 if [(c["id"],c["name"]) for c in data["categories"]]!=list(enumerate(LABELS)) or len(data["images"])!=2322 or len(data["annotations"])!=6030:raise ValueError("Full native7 validation schema changed")
 import torch
 torch.set_num_threads(4)
 from rfdetr import RFDETRNano
 from PIL import Image,ImageFile
 ImageFile.LOAD_TRUNCATED_IMAGES=False
 start=time.monotonic();model=RFDETRNano.from_checkpoint(str(checkpoint),device="cpu",amp=False,compile=False)
 if model.class_names!=LABELS:raise ValueError("Saved label order differs")
 print("Trusted native7 checkpoint loaded",cksha,flush=True)
 predictions=[];timings=[];hashes=[];background=0
 images=sorted(data["images"],key=lambda im:im["id"])
 with torch.inference_mode():
  for n,im in enumerate(images,1):
   pth=DATA/im["file_name"];hashes.append([im["id"],sha(pth)])
   with Image.open(pth) as opened:image=opened.convert("RGB")
   if image.size!=(im["width"],im["height"]):raise ValueError("Image dimensions differ")
   t=time.monotonic();p=model.predict(image,threshold=0.0);timings.append(time.monotonic()-t)
   for box,score,cid in zip(p.xyxy,p.confidence,p.class_id):
    cid=int(cid);score=float(score)
    if cid==len(LABELS):background+=1;continue
    if not 0<=cid<len(LABELS):raise ValueError("Unexpected predicted class ID")
    x1,y1,x2,y2=[float(v) for v in box]
    if not all(math.isfinite(v) for v in [x1,y1,x2,y2,score]):raise ValueError("Nonfinite prediction")
    x1,x2=max(0,min(im["width"],x1)),max(0,min(im["width"],x2));y1,y2=max(0,min(im["height"],y1)),max(0,min(im["height"],y2))
    if x2<=x1 or y2<=y1:continue
    predictions.append({"image_id":im["id"],"category_id":cid,"bbox":[x1,y1,x2-x1,y2-y1],"score":score})
   image.close()
   if n==1 or n%100==0 or n==len(images):
    state={"images_completed":n,"images_total":len(images),"elapsed_seconds":round(time.monotonic()-start,2),"checkpoint_sha256":cksha}
    temp=out/"progress.tmp";temp.write_text(json.dumps(state),encoding="utf-8");temp.replace(out/"progress.json")
    print("Validation images",n,"/",len(images),"elapsed",state["elapsed_seconds"],flush=True)
 (out/"predictions.json").write_text(json.dumps(predictions),encoding="utf-8")
 bbox,protocol=coco_bbox_metrics(data,predictions)
 metrics={"split":"Publisher VehiDE validation, used for model selection; not independent test", "checkpoint":str(checkpoint),"checkpoint_sha256":cksha,"annotation_sha256":sha(annotation),"image_hash_inventory_sha256":hashlib.sha256(json.dumps(hashes).encode()).hexdigest(),"images":len(images),"ground_truth_instances":len(data["annotations"]),"labels":LABELS,"coco_bbox":bbox,"fixed_threshold":fixed_threshold_metrics(data,predictions),"evaluation":{"backend":"pycocotools "+importlib.metadata.version("pycocotools"),"prediction_threshold_for_AP":0.0,**protocol,"device":"CPU FP32, no compile","torch_threads":4,"background_predictions_excluded":background,"annotation_id_policy":"Evaluator-local positive IDs 1..N; source annotation ID 0 conflicts with COCOeval unmatched sentinel; all boxes and image/category IDs unchanged","image_policy":"Original decoded sizes/pixels; no EXIF orientation or thumbnail","elapsed_seconds":time.monotonic()-start,"median_predict_seconds":statistics.median(timings),"torch":torch.__version__,"rfdetr":importlib.metadata.version("rfdetr"),"training_performed":False,"llm_calls":0,"limits":"Not independent test, not field/diagnosis accuracy, and not directly comparable to CarDD's different labels/images"}}
 (out/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
 print(json.dumps({"coco_bbox":metrics["coco_bbox"],"fixed_threshold":metrics["fixed_threshold"]},indent=2),flush=True)
if __name__=="__main__":main()
