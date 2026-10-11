"""Strict pixel-decode audit and versioned VehiDE repair; preserve original inputs."""
from pathlib import Path
import collections,concurrent.futures,hashlib,json,os,zipfile
from PIL import Image,ImageFile
ROOT=Path("D:/hakathon_wiut/datasets/kaggle-audit")
SOURCE=ROOT/"vehide-rfdetr-native7"
OUTPUT=ROOT/"vehide-rfdetr-native7-v2"
ImageFile.LOAD_TRUNCATED_IMAGES=False
def digest(p):
 with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def decode(item):
 split,im=item;path=SOURCE/split/im["file_name"]
 try:
  for draft in [None,384,1333]:
   with Image.open(path) as image:
    if image.size!=(im["width"],im["height"]):raise ValueError("Dimension mismatch")
    if draft:image.draft("RGB",(draft,draft))
    with image.convert("RGB") as rgb:rgb.load()
  return None
 except (OSError,ValueError,Image.DecompressionBombError) as e:return {"split":split,"file_name":im["file_name"],"error_type":type(e).__name__,"error":str(e),"sha256":digest(path)}
def main():
 if OUTPUT.exists():raise ValueError("Repair output exists; preserve it")
 datasets={s:json.loads((SOURCE/s/"_annotations.coco.json").read_text(encoding="utf-8")) for s in ["train","valid"]}
 items=[(s,im) for s,d in datasets.items() for im in d["images"]];failures=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for n,result in enumerate(pool.map(decode,items),1):
   if result:failures.append(result);print("Corrupt image",json.dumps(result),flush=True)
   if n%2000==0:print("Strict decode checked",n,"/",len(items),flush=True)
 audit={"images_checked":len(items),"decode_checks":["Full RGB pixel decode","JPEG draft RGB decode at 384","JPEG draft RGB decode at 1333"],"truncated_image_tolerance":False,"failures":failures,"source_package_sha256":json.loads((ROOT/"VEHIDE-PACKAGE.json").read_text(encoding="utf-8"))["archive_sha256"],"policy":"Exclude invalid photos and all their targets; do not tolerate truncated decoding, relabel targets or overwrite original files/splits"}
 (ROOT/"VEHIDE-PIXEL-AUDIT.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
 bad={(x["split"],x["file_name"]) for x in failures};report=json.loads((SOURCE/"DATA-AUDIT.json").read_text(encoding="utf-8"));report["pixel_decode_audit"]=audit
 for split,data in datasets.items():
  removed={im["id"] for im in data["images"] if (split,im["file_name"]) in bad}
  images=[im for im in data["images"] if im["id"] not in removed];annos=[a for a in data["annotations"] if a["image_id"] not in removed]
  data={**data,"images":images,"annotations":annos};folder=OUTPUT/split;folder.mkdir(parents=True)
  for im in images:os.link(SOURCE/split/im["file_name"],folder/im["file_name"])
  (folder/"_annotations.coco.json").write_text(json.dumps(data),encoding="utf-8")
  cats={c["id"]:c["name"] for c in data["categories"]};counts=collections.Counter(cats[a["category_id"]] for a in annos)
  report["splits"][split].update(images=len(images),annotations=len(annos),corrupt_images_excluded=len(removed),targets_per_class=dict(counts))
  print("Repaired split",split,len(images),len(annos),"excluded corrupt",len(removed),flush=True)
 provenance=json.loads((SOURCE/"provenance.json").read_text(encoding="utf-8"));provenance["pixel_decode_policy"]=audit["policy"]
 for n,d in [("provenance.json",provenance),("DATA-AUDIT.json",report)]: (OUTPUT/n).write_text(json.dumps(d,indent=2),encoding="utf-8")
 package=ROOT/"vehide-native7-v2-train-valid.zip"
 with zipfile.ZipFile(package,"w",compression=zipfile.ZIP_STORED,allowZip64=True) as z:
  for p in OUTPUT.rglob("*"):
   if p.is_file():z.write(p,p.relative_to(OUTPUT).as_posix())
 with zipfile.ZipFile(package) as z:
  if z.testzip() is not None:raise ValueError("Repaired package CRC mismatch")
 manifest=json.loads((ROOT/"VEHIDE-PACKAGE.json").read_text(encoding="utf-8"));manifest.update(archive=package.name,archive_bytes=package.stat().st_size,archive_sha256=digest(package),splits=report["splits"],pixel_audit=audit)
 (ROOT/"VEHIDE-PACKAGE-V2.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8");print("Repaired package ready",package,manifest["archive_bytes"],manifest["archive_sha256"],flush=True)
if __name__=="__main__":main()
