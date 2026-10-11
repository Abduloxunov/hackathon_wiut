"""Convert the audited VehiDE Kaggle release to RF-DETR COCO on D:.
Keeps all seven native labels. Never merges or remaps into CarDD.
"""
import argparse,collections,hashlib,json,math,os,stat,zipfile
from pathlib import Path,PureWindowsPath
from PIL import Image
ROOT=Path("D:/hakathon_wiut/datasets/kaggle-audit")
LABELS=["be_den","mat_bo_phan","mop_lom","rach","thung","tray_son","vo_kinh"]
def digest(path):
 with Path(path).open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def box_from_region(region,width,height):
 xs,ys=region.get("all_x",[]),region.get("all_y",[])
 if len(xs)!=len(ys) or len(xs)<3 or any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in xs+ys):return None,False
 raw=[min(xs),min(ys),max(xs),max(ys)]
 clipped=[max(0,min(width,raw[0])),max(0,min(height,raw[1])),max(0,min(width,raw[2])),max(0,min(height,raw[3]))]
 x,y,right,bottom=clipped
 if right<=x or bottom<=y:return None,clipped!=raw
 return [x,y,right-x,bottom-y],clipped!=raw
def safe_member(root,name):
 if PureWindowsPath(name).drive or "\\" in name:raise ValueError("Unsafe ZIP name")
 p=(root/name).resolve()
 if not p.is_relative_to(root.resolve()) or p==root.resolve():raise ValueError("Unsafe ZIP member")
 return p
def extract(archive,out):
 if out.exists():return
 with zipfile.ZipFile(archive) as z:
  infos=z.infolist()
  if sum(i.file_size for i in infos)>5*1024**3:raise ValueError("Archive exceeds 5 GiB extraction limit")
  if len({i.filename for i in infos})!=len(infos):raise ValueError("Duplicate ZIP names")
  for i in infos:
   safe_member(out,i.filename.rstrip("/"))
   if stat.S_ISLNK(i.external_attr>>16):raise ValueError("Symlink in ZIP")
  out.mkdir(parents=True)
  z.extractall(out)
 (out/".complete").write_text(digest(archive),encoding="utf-8")
def prepare():
 archive=ROOT/"vehide.zip";receipt=json.loads((ROOT/"vehide-download.json").read_text(encoding="utf-8"))
 if archive.stat().st_size!=receipt["bytes"] or digest(archive)!=receipt["sha256"]:raise ValueError("Source archive integrity mismatch")
 source=ROOT/"vehide-extracted";extract(archive,source)
 if not (source/".complete").exists() or (source/".complete").read_text(encoding="utf-8")!=receipt["sha256"]:raise ValueError("Incomplete extraction")
 destination=ROOT/"vehide-rfdetr-native7"
 if destination.exists():raise ValueError("Prepared output exists; preserve it or choose a new output")
 image_lookup={p.name:p for p in source.rglob("*.jpg")}
 if len(image_lookup)!=len(list(source.rglob("*.jpg"))):raise ValueError("Ambiguous source filenames")
 datasets={"train":json.loads((source/"0Train_via_annos.json").read_text(encoding="utf-8")),"valid":json.loads((source/"0Val_via_annos.json").read_text(encoding="utf-8"))}
 if len(datasets["train"])!=11621 or len(datasets["valid"])!=2324:raise ValueError("Release split counts changed")
 if set(datasets["train"])&set(datasets["valid"]):raise ValueError("Source filename leakage")
 protected=set();cardd=Path("D:/hakathon_wiut/datasets/cardoctor-cardd-coco")
 for split in ["valid","test"]:
  ann=cardd/split/"_annotations.coco.json"
  if ann.exists():
   for im in json.loads(ann.read_text(encoding="utf-8"))["images"]:protected.add(digest(cardd/split/im["file_name"]))
 print("Protected CarDD validation/test hashes",len(protected),flush=True)
 seen={};report={"source_archive":receipt,"native_labels":LABELS,"source_images":{s:len(d) for s,d in datasets.items()},"splits":{},"changes":[],"scope":"Separate seven-class VehiDE experiment; not CarDD training resume","group_independence":"Unverified: byte hashes do not detect all near duplicates or repeated vehicle/incident photos."}
 for split in ["valid","train"]:
  folder=destination/split;folder.mkdir(parents=True)
  records={"images":[],"annotations":[],"categories":[{"id":i,"name":c,"supercategory":"damage"} for i,c in enumerate(LABELS)]};stats=collections.Counter();counts=collections.Counter()
  for name,v in datasets[split].items():
   if name!=v["name"] or name not in image_lookup or Path(name).name!=name:raise ValueError("Missing or unsafe source image")
   path=image_lookup[name];sha=digest(path)
   reason="duplicate_image" if sha in seen else "overlaps_cardd_evaluation" if sha in protected else None
   if reason:
    stats[reason]+=1;report["changes"].append({"split":split,"file":name,"reason":reason,"sha256":sha});continue
   try:
    with Image.open(path) as image:w,h=image.size;image.verify()
    for draft in [None,384,1333]:
     with Image.open(path) as image:
      if draft:image.draft("RGB",(draft,draft))
      with image.convert("RGB") as rgb:rgb.load()
   except (OSError,ValueError,Image.DecompressionBombError) as exc:
    stats["corrupt_images_excluded"]+=1;report["changes"].append({"split":split,"file":name,"reason":"pixel_decode_failure","error":str(exc)});continue
   boxes=[]
   for region in v["regions"]:
    label=region["class"]
    if label not in LABELS:raise ValueError("Unknown native label")
    box,clipped=box_from_region(region,w,h)
    if box is None:
     stats["discarded_degenerate_regions"]+=1;report["changes"].append({"split":split,"file":name,"reason":"degenerate_region","class":label});continue
    if clipped:stats["clipped_boxes"]+=1
    boxes.append((LABELS.index(label),box))
   if not boxes:stats["images_with_no_valid_targets_excluded"]+=1;continue
   seen[sha]=split;iid=len(records["images"])
   records["images"].append({"id":iid,"file_name":name,"width":w,"height":h})
   try:os.link(path,folder/name)
   except OSError:
    import shutil;shutil.copy2(path,folder/name)
   for cid,box in boxes:
    records["annotations"].append({"id":len(records["annotations"]),"image_id":iid,"category_id":cid,"bbox":box,"area":box[2]*box[3],"iscrowd":0,"segmentation":[]});counts[LABELS[cid]]+=1
   if iid%2000==0:print(split,"verified",iid+1,flush=True)
  stats.update(images=len(records["images"]),annotations=len(records["annotations"]))
  report["splits"][split]={**stats,"targets_per_class":dict(counts)}
  (folder/"_annotations.coco.json").write_text(json.dumps(records),encoding="utf-8")
 provenance={"source":"https://www.kaggle.com/datasets/"+receipt["slug"],"archive_sha256":receipt["sha256"],"permission_confirmed":False,"user_authorized_research_use":True,"permission":"Kaggle listing says Apache 2.0; original authors restrict image usage to non-commercial research/education and do not own image copyrights. No commercial or public image redistribution permission established.","split_policy":"Retain publisher train/validation assignments; remove exact duplicate images, keep validation before train; exclude overlap with local CarDD validation/test. No official test in package.","taxonomy_policy":"Keep all seven Vietnamese native labels. Do not equate torn/punctured with crack/tireflat. English aliases are explanatory and require domain review.","conversion":"Polygon envelope boxes clipped to decoded image dimensions. Degenerate targets discarded; images with no valid targets excluded. Original polygons retained in source archive; package is detection only."}
 (destination/"provenance.json").write_text(json.dumps(provenance,indent=2),encoding="utf-8")
 (destination/"DATA-AUDIT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
 print(json.dumps(report["splits"],indent=2),flush=True)
 package=ROOT/"vehide-native7-train-valid.zip"
 with zipfile.ZipFile(package,"w",compression=zipfile.ZIP_STORED,allowZip64=True) as z:
  for p in destination.rglob("*"):
   if p.is_file():z.write(p,p.relative_to(destination).as_posix())
 manifest={"archive":package.name,"archive_bytes":package.stat().st_size,"archive_sha256":digest(package),"classes":LABELS,"dataset":"VehiDE native seven classes","splits":report["splits"],"contains_test":False,"permission":provenance["permission"]}
 (ROOT/"VEHIDE-PACKAGE.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
 print("Hugging Face data package ready",package,manifest["archive_bytes"],manifest["archive_sha256"],flush=True)
if __name__=="__main__":prepare()
