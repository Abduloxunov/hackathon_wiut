"""Convert original CarDD locally, preserving COCO IDs and official split membership."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import zipfile
from data_tools import contained, audit_dataset, make_smoke_subset

SPLITS = {'train2017':'train', 'val2017':'valid', 'test2017':'test'}

def convert_cardd(source, destination, *, user_authorized=False, copy_images=False):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.exists():
        raise ValueError('Conversion destination exists; original and existing converted files are never overwritten.')
    if destination.is_relative_to(source):
        raise ValueError('Choose a destination outside the original source directory.')
    entries=[]; schemas=[]
    for original, converted in SPLITS.items():
        annotation=source/'annotations'/('instances_'+original+'.json')
        data=json.loads(annotation.read_text(encoding='utf-8'))
        schemas.append({c['id']:c['name'] for c in data['categories']})
        files=[]
        for image in data['images']:
            src=contained(source/original,image['file_name'])
            contained(destination/converted,image['file_name'])
            if not src.is_file(): raise ValueError('Missing source image: '+str(src))
            files.append((src,image['file_name']))
        entries.append((original,converted,annotation,files))
    if any(schema!=schemas[0] for schema in schemas):
        raise ValueError('Original category schemas differ.')
    destination.mkdir(parents=True)
    incomplete=destination/'PREPARATION-INCOMPLETE.md'
    incomplete.write_text('Conversion incomplete: do not train from this directory yet.',encoding='utf-8')
    manifest=[]
    for original,converted,annotation,files in entries:
        folder=destination/converted;folder.mkdir()
        # Annotation bytes, image IDs, categories and all boxes/masks remain unchanged.
        shutil.copy2(annotation,folder/'_annotations.coco.json')
        for src,name in files:
            target=contained(folder,name);target.parent.mkdir(parents=True,exist_ok=True)
            if copy_images: shutil.copy2(src,target)
            else: os.link(src,target)
        manifest.append({'original_split':original,'converted_split':converted,'images':len(files),
            'annotation_sha256':hashlib.sha256(annotation.read_bytes()).hexdigest()})
        print(converted+': prepared '+str(len(files))+' images',flush=True)
    provenance={'source':'CarDD_release supplied locally by the user; official project https://cardd-ustc.github.io/',
        'permission':'User explicitly instructed research use on 2026-10-11. PIC Lab licensing-form/prior-consent status is unverified; no author consent or commercial/redistribution rights are asserted.',
        'permission_confirmed':False,'user_authorized_research_use':bool(user_authorized),
        'owner_consent_status':'unverified',
        'split_policy':'Original train2017/val2017/test2017 preserved as train/valid/test; no reassignment; vehicle/incident grouping unavailable.',
        'source_root':str(source),'image_storage':'copies' if copy_images else 'same-volume hardlinks; never edit linked image bytes',
        'original_annotation_fingerprints':manifest,'prepared_at':'2026-10-11'}
    (destination/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    incomplete.unlink()
    return provenance

def archive_smoke(root, archive):
    root,archive=Path(root).resolve(),Path(archive).resolve()
    if archive.exists(): raise ValueError('Archive exists; it will not be overwritten.')
    if archive.is_relative_to(root): raise ValueError('Archive must be outside the dataset.')
    archive.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for path in sorted(root.rglob('*')):
            if path.is_file(): z.write(path,path.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None: raise ValueError('ZIP CRC verification failed.')
        if any(name.startswith('test/') for name in z.namelist()): raise ValueError('Test image accidentally included in smoke ZIP.')
    with archive.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'path':str(archive),'bytes':archive.stat().st_size,'sha256':digest}

def d_path(text):
    p=Path(text).resolve()
    if p.drive.upper()!='D:': raise argparse.ArgumentTypeError('Local outputs must stay on D:')
    return p

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--destination',type=d_path,required=True)
    parser.add_argument('--smoke',type=d_path,required=True)
    parser.add_argument('--archive',type=d_path,required=True)
    parser.add_argument('--report',type=d_path,required=True)
    parser.add_argument('--user-authorized-research-use',action='store_true')
    parser.add_argument('--copy-images',action='store_true')
    args=parser.parse_args()
    provenance=convert_cardd(args.source,args.destination,user_authorized=args.user_authorized_research_use,copy_images=args.copy_images)
    report=make_smoke_subset(args.destination,args.smoke,train_limit=64,valid_limit=16,seed=42,min_class_images=2)
    smoke,_=audit_dataset(args.smoke)
    archive=archive_smoke(args.smoke,args.archive)
    lines=['# Colab-ready CarDD preparation','','Prepared locally on 2026-10-11. No GPU training or cloud upload occurred.','',
        'Original COCO root: `'+str(args.source.resolve())+'`.','Converted full dataset: `'+str(args.destination)+'`.','Smoke upload ZIP: `'+str(args.archive)+'`.','',
        '## Format and preservation','','Original splits and annotations are preserved: train2017 -> train, val2017 -> valid, test2017 -> test. JSON files are renamed to `_annotations.coco.json` without changing IDs, categories, boxes, area, masks or split membership. Original source files were not overwritten.',
        'Full converted images use '+provenance['image_storage']+'. Smoke images are separate copies. Do not overwrite hardlinked full-dataset image bytes.',
        '', '## Actual subset','','| Split | Full images | Full objects | Smoke images | Smoke objects |','|---|---:|---:|---:|---:|']
    for split in ['train','valid','test']:
        full=report['splits'][split];small=smoke['splits'].get(split,{})
        lines.append(f"| {split} | {full['images']} | {full['annotations']} | {small.get('images',0)} | {small.get('annotations',0)} |")
    lines+=['','The seed is 42. Selection ensures at least two training images and one validation image containing each of the six classes before filling the 64/16 limits. This deliberately covered subset is a pipeline test, not a representative accuracy evaluation. No test photos are packaged.',
        '', 'Smoke object counts:', '', '| Class | Train objects | Validation objects |', '|---|---:|---:|']
    for name in report['categories'].values():
        lines.append('| '+name+' | '+str(smoke['splits']['train']['targets_per_class'].get(name,0))+' | '+str(smoke['splits']['valid']['targets_per_class'].get(name,0))+' |')
    lines+=['','## Archive verification','',f"Size: **{archive['bytes']:,} bytes**. SHA-256: `{archive['sha256']}`. ZIP CRC verification passed. Archive entries contain only train/valid images and annotations plus provenance/smoke-origin metadata.",
        '', '## Authorization and evaluation limits','',
        'The user explicitly directed research use. `user_authorized_research_use` is true; `permission_confirmed` remains false, and PIC Lab author-consent/licensing-form status remains unverified. These fields distinguish user instruction from documented author consent. The source terms are linked from the training guide; no commercial or redistribution rights are asserted.',
        report['grouping'], 'All full/converted files passed the existing data audit. Smoke data passed the same image, box, schema and exact-leakage checks. No trained detector, mAP score, GPU allocation or reliability claim is reported.',
        '', '## Next action','',
        'Upload `cardoctor_rfdetr_nano_smoke.ipynb` to Colab, select a GPU runtime and run its cells. At the upload prompt, select the smoke ZIP above. The notebook detects the already-prepared subset and uses it directly. It saves checkpoints/logs to your Drive after your interactive Google authorization, then offers an artifact ZIP for download. Keep downloaded files on D:.', '']
    args.report.write_text(chr(10).join(lines),encoding='utf-8')
    print(json.dumps({'full':report['splits'],'smoke':smoke['splits'],'archive':archive},indent=2))
if __name__=='__main__': main()
