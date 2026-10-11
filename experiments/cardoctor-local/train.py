"""Train a small linear head on local reviewed image features; no downloads."""
import core
import argparse,json,time
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import torch

def grouped_split(rows,seed=42):
    labels=sorted({r['label'] for r in rows})
    if len(labels)<2:raise ValueError('At least two reviewed labels are required.')
    per_label=defaultdict(set)
    hashes=defaultdict(set)
    for r in rows:
        per_label[r['label']].add(r['group_id']);hashes[r['image_hash']].add(r['group_id'])
    if any(len(groups)>1 for groups in hashes.values()):raise ValueError('The same image appears under different groups. Correct the grouping before training.')
    for label in labels:
        if len(per_label[label])<3:raise ValueError(f'{label}: provide at least three independent vehicle/incident groups.')
    groups=sorted({r['group_id'] for r in rows});rng=np.random.default_rng(seed)
    for attempt in range(2000):
        shuffled=list(rng.permutation(groups));cut=max(1,round(len(groups)*.25)) if attempt<500 else int(rng.integers(1,len(groups)));valid_groups=set(shuffled[:cut])
        train=[i for i,r in enumerate(rows) if r['group_id'] not in valid_groups]
        valid=[i for i,r in enumerate(rows) if r['group_id'] in valid_groups]
        if {rows[i]['label'] for i in train}==set(labels) and {rows[i]['label'] for i in valid}==set(labels):
            return train,valid,labels
    raise ValueError('Could not create a grouped validation split covering all labels. Add independent groups.')

def fit(rows,epochs=150,seed=42):
    train,valid,labels=grouped_split(rows,seed)
    torch.manual_seed(seed);torch.set_num_threads(min(4,core.os.cpu_count() or 1))
    x=torch.from_numpy(np.stack([np.frombuffer(r['embedding'],dtype=np.float32).copy() for r in rows]))
    y=torch.tensor([labels.index(r['label']) for r in rows]);head=torch.nn.Linear(512,len(labels))
    counts=torch.bincount(y[train],minlength=len(labels)).float();weights=counts.sum()/(len(labels)*counts)
    loss_fn=torch.nn.CrossEntropyLoss(weight=weights);optimizer=torch.optim.AdamW(head.parameters(),lr=.03,weight_decay=.01)
    for epoch in range(epochs):
        head.train();optimizer.zero_grad();loss=loss_fn(head(x[train]),y[train]);loss.backward();optimizer.step()
    with torch.inference_mode():pred=head(x[valid]).argmax(1).numpy()
    truth=y[valid].numpy();matrix=np.zeros((len(labels),len(labels)),dtype=int)
    for expected,actual in zip(truth,pred):matrix[expected,actual]+=1
    f1=[]
    for i in range(len(labels)):
        tp=matrix[i,i];fp=matrix[:,i].sum()-tp;fn=matrix[i,:].sum()-tp;f1.append(float(2*tp/max(2*tp+fp+fn,1)))
    metrics={'validation_accuracy':float((pred==truth).mean()),'validation_macro_f1':float(np.mean(f1)),'confusion_matrix':matrix.tolist(),'labels':labels,'train_count':len(train),'validation_count':len(valid),'train_groups':sorted({rows[i]['group_id'] for i in train}),'validation_groups':sorted({rows[i]['group_id'] for i in valid}),'epochs':epochs,'seed':seed,'feature_version':core.FEATURE_VERSION,'evaluation_status':'Development validation only. No independent held-out test or probability calibration.'}
    return head,metrics

def save(head,metrics,destination):
    destination.mkdir(parents=True,exist_ok=True)
    np.savez(destination/'linear_classifier.npz',weight=head.weight.detach().numpy().T,bias=head.bias.detach().numpy(),labels=np.asarray(metrics['labels']),feature_version=np.asarray(core.FEATURE_VERSION))
    (destination/'training_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    lines=['# Local classifier training run','','This is a frozen ResNet18 feature extractor with a newly trained linear classification head. It does not localize defects.','','## Data split','',f"- Training images: {metrics['train_count']}",f"- Validation images: {metrics['validation_count']}",f"- Training groups: {', '.join(metrics['train_groups'])}",f"- Validation groups: {', '.join(metrics['validation_groups'])}",'','Whole vehicle/incident groups are separated. Duplicate images assigned to different groups are rejected.','','## Development validation','',f"- Accuracy: {metrics['validation_accuracy']:.4f}",f"- Macro F1: {metrics['validation_macro_f1']:.4f}",'','These numbers apply only to the provided local validation examples. They are not a claim of real-world automotive accuracy. Reserve independent vehicle groups for final testing before selecting the model. Scores in the app are uncalibrated.','','Rows below are true labels; columns are predicted labels.','','| True / predicted | '+' | '.join(metrics['labels'])+' |','| --- | '+' | '.join(['---']*len(metrics['labels']))+' |']
    for label,row in zip(metrics['labels'],metrics['confusion_matrix']):lines.append('| '+label+' | '+' | '.join(map(str,row))+' |')
    lines+=['','## Reproduction','',f"- Feature version: `{core.FEATURE_VERSION}`",f"- Seed: {metrics['seed']}; epochs: {metrics['epochs']}",'','Source and permission records remain attached to references in the local SQLite library. Annotation quality and rights require human review.','']
    (destination/'TRAINING-REPORT.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--epochs',type=int,default=150);parser.add_argument('--seed',type=int,default=42);parser.add_argument('--activate',action='store_true',help='Activate this experimental head in the local app.');args=parser.parse_args()
    if not 1<=args.epochs<=1000:parser.error('epochs must be between 1 and 1000')
    with core.connection() as db:rows=[dict(r) for r in db.execute('SELECT * FROM refs WHERE feature_version=?',(core.FEATURE_VERSION,))]
    try:head,metrics=fit(rows,args.epochs,args.seed)
    except ValueError as error:parser.exit(2,str(error)+'\n')
    destination=core.RUNTIME/'training'/time.strftime('%Y%m%d-%H%M%S');save(head,metrics,destination)
    if args.activate:
        import shutil
        shutil.copyfile(destination/'linear_classifier.npz',core.RUNTIME/'linear_classifier.npz')
        shutil.copyfile(destination/'TRAINING-REPORT.md',core.RUNTIME/'ACTIVE-TRAINING-REPORT.md')
    print('Saved:',destination);print(json.dumps(metrics,indent=2))
