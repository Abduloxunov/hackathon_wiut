"""Read-only audit of original CarDD COCO files. Writes only a Markdown report."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from PIL import Image

def audit(root):
    errors=[];counts={}; seen={}; hashes={}; duplicate=[]; categories=None
    for split in ["train2017","val2017","test2017"]:
        path=root/"annotations"/("instances_"+split+".json")
        data=json.loads(path.read_text(encoding="utf-8"))
        current={c["id"]:c["name"] for c in data["categories"]}
        if categories is not None and current!=categories: errors.append("Category schema differs: "+split)
        categories=current
        images={i["id"]:i for i in data["images"]}
        if len(images)!=len(data["images"]): errors.append("Duplicate image IDs within "+split)
        objects=Counter();boxes=0;byte_count=0
        for i in data["images"]:
            p=(root/split/i["file_name"]).resolve()
            if not p.is_relative_to((root/split).resolve()): errors.append("Unsafe image path: "+split);continue
            if not p.is_file(): errors.append("Missing image: "+str(p));continue
            byte_count+=p.stat().st_size
            if i["id"] in seen: errors.append("Image ID appears in two splits: "+str(i["id"]))
            seen[i["id"]]=split
            try:
                with Image.open(p) as image:
                    if image.size!=(i["width"],i["height"]): errors.append("Dimensions differ: "+str(p))
                    image.verify()
                with p.open("rb") as stream:
                    digest=hashlib.file_digest(stream,"sha256").hexdigest()
                if digest in hashes and hashes[digest][0]!=split: duplicate.append((str(p),hashes[digest][1]))
                hashes[digest]=(split,str(p))
            except Exception as exc: errors.append("Unreadable image: "+p.name+" "+type(exc).__name__)
        annotation_ids=set()
        for a in data["annotations"]:
            if a["id"] in annotation_ids: errors.append("Duplicate annotation ID: "+split)
            annotation_ids.add(a["id"])
            if a["image_id"] not in images or a["category_id"] not in current: errors.append("Invalid annotation reference: "+split);continue
            i=images[a["image_id"]];bbox=a.get("bbox",[])
            if len(bbox)!=4 or any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in bbox): errors.append("Invalid bbox: "+split);continue
            x,y,w,h=bbox
            if min(x,y)<0 or min(w,h)<=0 or x+w>i["width"]+1e-4 or y+h>i["height"]+1e-4: errors.append("Out-of-bounds bbox: "+split+" / "+str(a["id"]))
            objects[current[a["category_id"]]]+=1;boxes+=1
        counts[split]={"images":len(images),"annotations":len(data["annotations"]),"checked_boxes":boxes,"image_bytes":byte_count,"by_class":dict(objects)}
        print(split+": checked "+str(len(images))+" images",flush=True)
    return counts,errors,duplicate

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root",type=Path);parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.resolve().drive.upper()!="D:": parser.error("Write reports only on D:")
    counts,errors,duplicate=audit(args.root)
    lines=["# Downloaded CarDD audit", "", "Checked locally on 2026-10-11. Original files were read without modification.","", "COCO root: `"+str(args.root.resolve())+"`.","", "| Original split | Images | Objects | Image bytes |","|---|---:|---:|---:|"]
    for split,c in counts.items(): lines.append(f"| {split} | {c['images']} | {c['annotations']} | {c['image_bytes']} |")
    lines += ["", "## Objects by class", "", "| Class | Train | Validation | Test |", "|---|---:|---:|---:|"]
    for name in counts["train2017"]["by_class"]: lines.append("| "+name+" | "+" | ".join(str(counts[s]["by_class"].get(name,0)) for s in counts)+" |")
    lines += ["", "## Integrity checks", "", f"Structural/image issues found: **{len(errors)}**. Identical image files across splits: **{len(duplicate)}**.","", "Checked matching category schemas, image/annotation IDs, file presence, relative-path containment, Pillow image.verify integrity and annotation dimensions, finite positive bounding boxes within image bounds, and SHA-256 byte duplicates across the official splits."]
    lines += ["", "Issues:"]+["- "+e for e in errors] if errors else ["", "No structural or image-file issues found by these checks."]
    if duplicate: lines += ["", "Cross-split exact duplicates:"]+["- "+a+" / "+b for a,b in duplicate]
    lines += ["", "## Training readiness and limits", "", "The release uses `train2017`, `val2017`, `test2017` with `annotations/instances_*.json`. Our prepared training notebook currently expects `train`, `valid`, `test` and `_annotations.coco.json` inside each split: conversion is still required. The release also contains CarDD_SOD; use CarDD_COCO for the six-class detector experiment.","", "Preserve the official test split for final evaluation. These checks do not identify visually similar photos, multiple images of the same vehicle/scene, or group leakage. No vehicle-group metadata was supplied. No segmentation-mask evaluation, detector training or accuracy measurement was performed.","", "Training permission and any cloud-upload rights must be recorded from the actual access agreement. No permission confirmation was inferred from having downloaded the files. No data was uploaded, copied to C:, or included in Git.","", "Run the audit again with:","", "```powershell", 'D:\\hakathon_wiut\\.venv\\Scripts\\python.exe -B experiments/cardoctor-colab/audit_original_cardd.py "'+str(args.root.resolve())+'" --output "'+str(args.output.resolve())+'"', "```", ""]
    args.output.write_text(chr(10).join(lines),encoding="utf-8")
    print(json.dumps({"images":sum(c["images"] for c in counts.values()),"annotations":sum(c["annotations"] for c in counts.values()),"issues":len(errors),"cross_split_exact_duplicates":len(duplicate)}))
if __name__=="__main__": main()
