"""A CPU visual-reference baseline. All mutable storage and caches stay on D:."""
from pathlib import Path
import os
BASE=Path(__file__).resolve().parent
RUNTIME=Path(os.environ.get('CARDOCTOR_RUNTIME',BASE/'.runtime')).resolve()
if RUNTIME.drive.upper()!='D:':
    raise RuntimeError('CarDoctor runtime storage must be on D:')
RUNTIME.mkdir(parents=True,exist_ok=True)
for name in ['cache','tmp','images','reports']:(RUNTIME/name).mkdir(exist_ok=True)
for key,sub in {'TORCH_HOME':'cache/torch','HF_HOME':'cache/huggingface','HUGGINGFACE_HUB_CACHE':'cache/huggingface/hub','XDG_CACHE_HOME':'cache','PIP_CACHE_DIR':'cache/pip','TMP':'tmp','TEMP':'tmp','TMPDIR':'tmp'}.items():
    target=RUNTIME/sub;target.mkdir(parents=True,exist_ok=True);os.environ[key]=str(target)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import base64,hashlib,io,json,math,re,sqlite3,threading,time,uuid
from collections import Counter
from urllib.parse import urlparse
import cv2
import numpy as np
from PIL import Image,ImageOps,UnidentifiedImageError
import torch
from torchvision.models import resnet18,ResNet18_Weights

MAX_BYTES=8*1024*1024
MAX_PIXELS=16_000_000
Image.MAX_IMAGE_PIXELS=MAX_PIXELS
MODEL_URL=ResNet18_Weights.IMAGENET1K_V1.url
MODEL_FILE=RUNTIME/'cache/torch/checkpoints/resnet18-f37072fd.pth'
FEATURE_VERSION='resnet18-imagenet1k-v1-letterbox224-l2-v1'
_db_lock=threading.RLock()
_inference_lock=threading.RLock()
_model=None

def connection():
    conn=sqlite3.connect(RUNTIME/'library.sqlite3');conn.row_factory=sqlite3.Row
    return conn

def initialize():
    with connection() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS refs(id TEXT PRIMARY KEY,label TEXT NOT NULL,group_id TEXT NOT NULL,source TEXT NOT NULL,rights TEXT NOT NULL,image_hash TEXT NOT NULL,image_file TEXT NOT NULL,embedding BLOB NOT NULL,crop TEXT,created TEXT NOT NULL,feature_version TEXT NOT NULL);
        CREATE UNIQUE INDEX IF NOT EXISTS unique_ref ON refs(image_hash,ifnull(crop,''));
        CREATE TABLE IF NOT EXISTS notes(id TEXT PRIMARY KEY,title TEXT NOT NULL,excerpt TEXT NOT NULL,source_url TEXT NOT NULL,vehicle TEXT NOT NULL,tags TEXT NOT NULL,reviewed INTEGER NOT NULL,created TEXT NOT NULL);
        ''')
        if 'part' not in [row['name'] for row in db.execute('PRAGMA table_info(notes)')]:db.execute("ALTER TABLE notes ADD COLUMN part TEXT NOT NULL DEFAULT ''" )

def model():
    global _model
    with _inference_lock:
        if _model is None:
            if not MODEL_FILE.exists():raise ValueError('Vision weights are not available. Run setup_model.py first; it saves them to D:.')
            torch.set_num_threads(min(4,os.cpu_count() or 1))
            m=resnet18(weights=None)
            m.load_state_dict(torch.load(MODEL_FILE,map_location='cpu',weights_only=True))
            m.fc=torch.nn.Identity();m.eval();_model=m
        return _model

def decode_image(encoded):
    if not isinstance(encoded,str) or len(encoded)>MAX_BYTES*1.38:raise ValueError('Upload an image smaller than 8 MB.')
    if encoded.startswith('data:'):
        header,encoded=encoded.split(',',1)
        if not header.startswith(('data:image/jpeg;','data:image/png;','data:image/webp;')):raise ValueError('Use JPEG, PNG or WebP.')
    try:
        raw=base64.b64decode(encoded,validate=True)
        if len(raw)>MAX_BYTES:raise ValueError('Image is larger than 8 MB.')
        with Image.open(io.BytesIO(raw)) as source:
            if source.format not in ['JPEG','PNG','WEBP']:raise ValueError('Use JPEG, PNG or WebP.')
            if source.width*source.height>MAX_PIXELS:raise ValueError('Image exceeds 16 megapixels. Resize it first.')
            im=ImageOps.exif_transpose(source).convert('RGB');im.load()
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError,Image.DecompressionBombWarning) as e:
        raise ValueError('The image could not be read safely.') from e
    except (TypeError,base64.binascii.Error) as e:raise ValueError('Invalid image encoding.') from e
    image_hash=hashlib.sha256(np.asarray(im).tobytes()+str(im.size).encode()).hexdigest()
    return im,image_hash

def crop_image(image,crop):
    if crop is None:return image,None
    if not isinstance(crop,list) or len(crop)!=4:raise ValueError('Region requires four normalized coordinates.')
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in crop):raise ValueError('Invalid region coordinates.')
    x0,y0,x1,y1=crop
    if not (0<=x0<x1<=1 and 0<=y0<y1<=1):raise ValueError('Region must be within the image.')
    bounds=[round(x0*image.width),round(y0*image.height),round(x1*image.width),round(y1*image.height)]
    if bounds[2]-bounds[0]<16 or bounds[3]-bounds[1]<16:raise ValueError('Select a region at least 16 pixels wide and high.')
    return image.crop(tuple(bounds)),bounds

def feature(image):
    # Letterbox retains the whole selected region; a center crop can discard thin defects.
    im=ImageOps.pad(image,(224,224),method=Image.Resampling.BILINEAR,color=(124,116,104))
    array=np.asarray(im,dtype=np.float32)/255
    array=(array-np.array([.485,.456,.406],dtype=np.float32))/np.array([.229,.224,.225],dtype=np.float32)
    tensor=torch.from_numpy(array.transpose(2,0,1).copy()).unsqueeze(0)
    with _inference_lock,torch.inference_mode():v=model()(tensor).squeeze(0).numpy().astype(np.float32)
    return v/max(float(np.linalg.norm(v)),1e-12)

def quality(image):
    sample=np.asarray(ImageOps.contain(image,(1024,1024)))
    gray=cv2.cvtColor(sample,cv2.COLOR_RGB2GRAY)
    lap=float(cv2.Laplacian(gray,cv2.CV_64F).var())
    dark=float(np.mean(gray<12));bright=float(np.mean(gray>245))
    issues=[]
    if min(image.size)<160:issues.append('The selected area is small; a closer photo may preserve more detail.')
    if lap<35:issues.append('Low edge detail: check focus and take a closer photo if necessary.')
    if dark>.45:issues.append('Much of the image is very dark; try more even lighting.')
    if bright>.45:issues.append('Much of the image is very bright; try reducing glare or exposure.')
    return {'width':image.width,'height':image.height,'edge_variance':round(lap,2),'dark_fraction':round(dark,3),'bright_fraction':round(bright,3),'issues':issues,'threshold_status':'Heuristic capture feedback; not a calibrated damage-quality test.'}

def string(data,key,limit,required=False):
    value=data.get(key,'')
    if not isinstance(value,str):raise ValueError(f'{key} must be text.')
    value=value.strip()
    if len(value)>limit:raise ValueError(f'{key} is too long.')
    if required and not value:raise ValueError(f'{key} is required.')
    return value

def add_reference(data):
    label=string(data,'label',60,True);group=string(data,'group_id',100,True)
    source=string(data,'source',500,True);rights=string(data,'rights',500,True)
    image,image_hash=decode_image(data.get('image'));region,bounds=crop_image(image,data.get('crop'))
    crop_key=json.dumps(bounds) if bounds else ''
    with _db_lock,connection() as db:
        duplicate=db.execute('SELECT id FROM refs WHERE image_hash=? AND crop=?',(image_hash,crop_key)).fetchone()
        if duplicate:raise ValueError('This exact image and region are already in the reference library.')
    embedding=feature(region);rid=uuid.uuid4().hex;name=rid+'.png'
    image.save(RUNTIME/'images'/name)
    with _db_lock,connection() as db:
        try:db.execute('INSERT INTO refs VALUES(?,?,?,?,?,?,?,?,?,?,?)',(rid,label,group,source,rights,image_hash,name,embedding.tobytes(),crop_key,time.strftime('%Y-%m-%dT%H:%M:%S'),FEATURE_VERSION))
        except sqlite3.IntegrityError:
            (RUNTIME/'images'/name).unlink(missing_ok=True)
            raise ValueError('This reference has already been added.')
    return {'id':rid,'label':label,'group_id':group,'image_url':'/media/'+name,'quality':quality(region)}

def add_note(data):
    title=string(data,'title',160,True);excerpt=string(data,'excerpt',4000,True)
    url=string(data,'source_url',1000,True);vehicle=string(data,'vehicle',100);tags=string(data,'tags',400)
    parsed=urlparse(url)
    if parsed.scheme not in ['http','https'] or not parsed.netloc:raise ValueError('Provide the source as an HTTP or HTTPS URL.')
    part=string(data,'part',60)
    reviewed=data.get('reviewed') is True
    if not reviewed:raise ValueError('Review the source excerpt before adding it to the knowledge library.')
    nid=uuid.uuid4().hex
    with _db_lock,connection() as db:db.execute('INSERT INTO notes(id,title,excerpt,source_url,vehicle,tags,reviewed,created,part) VALUES(?,?,?,?,?,?,?,?,?)',(nid,title,excerpt,url,vehicle,tags,1,time.strftime('%Y-%m-%dT%H:%M:%S'),part))
    return {'id':nid,'title':title}

def tokens(text):return re.findall(r'[^\W_]+',text.casefold(),re.UNICODE)

def retrieve_notes(query,vehicle,part='' ):
    with connection() as db:rows=[dict(r) for r in db.execute('SELECT * FROM notes WHERE reviewed=1')]
    # Exact model filter: generic records are allowed; incompatible model-specific records are excluded.
    rows=[r for r in rows if not r['vehicle'] or (vehicle and r['vehicle'].casefold()==vehicle.casefold())]
    rows=[r for r in rows if not r['part'] or (part and r['part'].casefold()==part.casefold())]
    if not rows or not tokens(query):return []
    docs=[Counter(tokens(r['title']+' '+r['tags']+' '+r['excerpt'])) for r in rows]
    length=[sum(d.values()) for d in docs];avg=sum(length)/len(length);terms=set(tokens(query));scored=[]
    for row,doc,n in zip(rows,docs,length):
        score=0.
        for t in terms:
            freq=doc[t]
            if not freq:continue
            df=sum(t in d for d in docs);idf=math.log(1+(len(docs)-df+.5)/(df+.5))
            score+=idf*freq*2.5/(freq+1.5*(.25+.75*n/max(avg,1)))
        if score>0:scored.append({**row,'retrieval_score':round(score,4)})
    return sorted(scored,key=lambda r:r['retrieval_score'],reverse=True)[:3]

def library():
    with connection() as db:
        refs=[{k:r[k] for k in ['id','label','group_id','source','rights','image_file','created']} for r in db.execute('SELECT * FROM refs ORDER BY created DESC')]
        notes=[dict(r) for r in db.execute('SELECT * FROM notes ORDER BY created DESC')]
    for r in refs:r['image_url']='/media/'+r.pop('image_file')
    return {'references':refs,'notes':notes}

def analyze(data):
    start=time.perf_counter();image,image_hash=decode_image(data.get('image'))
    region,bounds=crop_image(image,data.get('crop'));symptoms=string(data,'symptoms',2000);vehicle=string(data,'vehicle',100);group=string(data,'group_id',100)
    vector=feature(region)
    with connection() as db:rows=[dict(r) for r in db.execute('SELECT * FROM refs WHERE feature_version=?',(FEATURE_VERSION,))]
    candidates=[r for r in rows if r['image_hash']!=image_hash and (not group or r['group_id']!=group)]
    matches=[]
    for r in candidates:
        score=float(vector@np.frombuffer(r['embedding'],dtype=np.float32))
        matches.append({'id':r['id'],'label':r['label'],'group_id':r['group_id'],'source':r['source'],'rights':r['rights'],'image_url':'/media/'+r['image_file'],'crop_pixels':json.loads(r['crop']) if r['crop'] else None,'similarity':round(score,4),'score_type':'cosine_similarity_not_probability'})
    matches=sorted(matches,key=lambda m:m['similarity'],reverse=True)[:3]
    # Do not automatically promote a retrieved label into a confirmed finding or a KB query.
    confirmed_label=string(data,'confirmed_label',60)
    part=string(data,'part',60)
    notes=retrieve_notes(symptoms+' '+confirmed_label,vehicle,part)
    assessment='Compare the retrieved examples with the selected region. Reference labels are annotations of those examples, not a diagnosis of this photo.' if matches else 'No eligible reference examples are available. Add reviewed photos from different vehicle or incident groups.'
    result={'case_id':uuid.uuid4().hex,'mode':'assisted_visual_reference_baseline','region_pixels':bounds,'quality':quality(region),'matches':matches,'knowledge':notes,'vehicle':vehicle,'part':part,'symptoms':symptoms,'confirmed_label':confirmed_label,'assessment':assessment,'feature_version':FEATURE_VERSION,'damage_detector_trained':False,'elapsed_ms':round((time.perf_counter()-start)*1000,1),'excluded_exact_images':sum(r['image_hash']==image_hash for r in rows),'excluded_same_group':sum(bool(group) and r['group_id']==group for r in rows),'created':time.strftime('%Y-%m-%dT%H:%M:%S')}
    active=RUNTIME/'linear_classifier.npz'
    if active.exists():
        with np.load(active,allow_pickle=False) as head:
            if str(head['feature_version'])==FEATURE_VERSION:
                logits=vector@head['weight']+head['bias'];prob=np.exp(logits-logits.max());prob/=prob.sum()
                order=np.argsort(prob)[::-1]
                result['experimental_classifier']={'predictions':[{'label':str(head['labels'][i]),'uncalibrated_score':round(float(prob[i]),4)} for i in order[:3]],'status':'User-reference-trained classifier; scores are uncalibrated. Consult the training report.'}
    return result

initialize()
