"""Read verified smoke weights and render four private validation comparisons on D:."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'kb'))
from runtime import configure
configure()
os.environ['MPLCONFIGDIR']=str(ROOT/'experiments/cardoctor-colab/.runtime/matplotlib')
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',type=Path,default=Path('D:/hakathon_wiut/checkpoint_best_ema.pth'))
    parser.add_argument('--inventory',type=Path,default=Path('D:/hakathon_wiut/CHECKPOINTS.md'))
    parser.add_argument('--dataset',type=Path,default=Path('D:/hakathon_wiut/datasets/cardoctor-cardd-smoke'))
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'.runtime/smoke-review')
    args=parser.parse_args()
    if args.output.resolve().drive.upper()!='D:':parser.error('All outputs must stay on D:')
    if args.output.exists():parser.error('Use a fresh output directory; existing review files are preserved.')
    inventory=dict(re.findall(r'`([^`]+)`:\s*`([a-f0-9]{64})`',args.inventory.read_text(encoding='utf-8')))
    with args.checkpoint.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    if digest!=inventory.get(args.checkpoint.name):parser.error('Checkpoint hash differs from the Colab inventory.')
    import torch
    torch.set_num_threads(4)
    raw=torch.load(args.checkpoint,map_location='cpu',weights_only=True)
    data=json.loads((args.dataset/'valid/_annotations.coco.json').read_text(encoding='utf-8'))
    classes=[cat['name'] for cat in sorted(data['categories'],key=lambda c:c['id'])]
    if raw.get('model_config',{}).get('num_classes')!=len(classes):parser.error('Checkpoint class count differs from the dataset.')
    if raw.get('model_name') not in [None,'RFDETRNano']:parser.error('Unexpected detector architecture.')
    del raw
    from rfdetr import RFDETRNano
    from PIL import Image,ImageDraw
    start=time.perf_counter()
    model=RFDETRNano.from_checkpoint(str(args.checkpoint.resolve()),device='cpu',amp=False,compile=False)
    print('Verified EMA checkpoint loaded on CPU',flush=True)
    load_seconds=time.perf_counter()-start
    args.output.mkdir(parents=True)
    results=[]
    for im in data['images'][:4]:
        image=Image.open(args.dataset/'valid'/im['file_name']).convert('RGB')
        before=time.perf_counter();detections=model.predict(image,threshold=0.05);elapsed=time.perf_counter()-before
        background_count=sum(int(cid)==len(classes) for cid in detections.class_id)
        unknown=[int(cid) for cid in detections.class_id if not 0<=int(cid)<=len(classes)]
        if unknown:raise ValueError(f'Unexpected class IDs: {unknown}')
        rows=[{'class_id':int(cid),'label':classes[int(cid)],'score':float(score),'xyxy':[float(x) for x in box]}
              for cid,score,box in zip(detections.class_id,detections.confidence,detections.xyxy) if int(cid)<len(classes)]
        original=image.copy();ground_truth=image.copy();predicted=image.copy()
        gt_draw=ImageDraw.Draw(ground_truth);pred_draw=ImageDraw.Draw(predicted)
        gt=[ann for ann in data['annotations'] if ann['image_id']==im['id']]
        by_category={cat['id']:cat['name'] for cat in data['categories']}
        for ann in gt:
            x,y,w,h=ann['bbox'];gt_draw.rectangle((x,y,x+w,y+h),outline='lime',width=4)
            gt_draw.text((x,max(0,y-14)),by_category[ann['category_id']],fill='black',stroke_fill='white',stroke_width=2)
        high=[row for row in rows if row['score']>=0.35]
        for row in high:
            box=row['xyxy'];pred_draw.rectangle(box,outline='red',width=4)
            pred_draw.text((box[0],max(0,box[1]-14)),row['label']+' '+f"{row['score']:.2f}",fill='black',stroke_fill='white',stroke_width=2)
        ground_truth.thumbnail((700,500));predicted.thumbnail((700,500))
        combined=Image.new('RGB',(ground_truth.width+predicted.width,max(ground_truth.height,predicted.height)+30),'white')
        combined.paste(ground_truth,(0,30));combined.paste(predicted,(ground_truth.width,30))
        draw=ImageDraw.Draw(combined);draw.text((6,8),'Dataset annotation (green)',fill='black');draw.text((ground_truth.width+6,8),'Smoke predictions >= 0.35 (red)',fill='black')
        filename=Path(im['file_name']).stem+'-comparison.png';combined.save(args.output/filename)
        results.append({'file':im['file_name'],'ground_truth':[{ 'label':by_category[a['category_id']],'bbox':a['bbox']} for a in gt],
            'background_count_ge_005':background_count,'predictions_ge_005':rows,'count_ge_035':len(high),'best_score':max([r['score'] for r in rows],default=0),'cpu_seconds':round(elapsed,4),'comparison':filename})
        print(im['file_name']+': '+str(len(high))+' predictions >=0.35; '+str(len(rows))+' >=0.05',flush=True)
    metrics=[]
    with Path('D:/hakathon_wiut/metrics.csv').open(encoding='utf-8',newline='') as f:
        source=list(csv.DictReader(f))
    for epoch in ['0','1']:
        values={k:float(v) for row in source if row['epoch']==epoch for k,v in row.items() if v and k not in ['epoch','step']}
        metrics.append({'epoch':int(epoch)+1,'loss':values['train/loss'],'mAP_50':values['val/mAP_50'],'mAP_50_95':values['val/mAP_50_95']})
    audit={'checkpoint':str(args.checkpoint.resolve()),'sha256':digest,'hash_verified':True,'device':'cpu','load_seconds':round(load_seconds,4),'classes':classes,'training_metrics':metrics,'predictions':results}
    (args.output/'prediction-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    lines=['# Verified smoke checkpoint review','','Checked on 2026-10-11. The supplied checkpoint SHA-256 matches CHECKPOINTS.md. Original source logs, checkpoints and dataset images were not modified.','',
        'Checkpoint: `'+str(args.checkpoint.resolve())+'`. Device: CPU. Classes: '+', '.join(classes)+'.',
        '', 'The downloaded training log confirms a two-epoch CUDA run and reports saving the best EMA model. results.md records a 50.6-second training call; weights were downloaded before that timer. The held-out official test split was not used.',
        '', '| Epoch | Training loss | mAP@50 | mAP@50-95 |','|---|---:|---:|---:|']
    for m in metrics:lines.append(f"| {m['epoch']} | {m['loss']:.4f} | {m['mAP_50']:.4f} | {m['mAP_50_95']:.4f} |")
    lines+=['','## Private validation comparisons','','Four images from the smoke-validation split were inspected. Green boxes are dataset annotations; red boxes are predictions at score >=0.35. The no-object slot (class 6) is excluded from damage detections and its count is recorded. Raw foreground predictions at >=0.05 are retained only for debugging in prediction-audit.json. Scores are not calibrated diagnostic certainty. These examples and thresholds are not held-out accuracy measurements.','',
        '| Image | Labelled objects | Predictions >=0.35 | Best score among >=0.05 | CPU prediction seconds |','|---|---:|---:|---:|---:|']
    for r in results:lines.append(f"| {r['file']} | {len(r['ground_truth'])} | {r['count_ge_035']} | {r['best_score']:.3f} | {r['cpu_seconds']:.4f} |")
    for r in results:lines+=['','### '+r['file'],'','![Ground truth and smoke predictions]('+r['comparison']+')']
    lines+=['','## Interpretation and next step','','Training completed and the checkpoint can run inference locally. Falling loss and rising validation mAP are encouraging early signals, but the small, class-covered two-epoch subset does not establish useful damage accuracy. Review missed/mislabelled regions in the comparisons before a fresh full-data run. Keep the 374-image official test split untouched; use the full 2,816 train and 810 validation images for the next training/validation experiment.',
        '', 'The original log contains a scheduler-order warning to investigate before longer training, a CPU fallback for assignment while training used CUDA, and a skipped validation-loss computation. No traceback was present. This review does not measure per-class accuracy, generalization or GPU inference latency.',
        '', 'Images and this private output folder remain ignored/local, on D:. No dataset/photo upload, paid compute, API request, PDF, commit or push was performed during this review.','']
    (args.output/'REVIEW.md').write_text(chr(10).join(lines),encoding='utf-8')
    print('Saved review:',str(args.output/'REVIEW.md'),flush=True)
if __name__=='__main__':main()
