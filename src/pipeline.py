"""CarDoctor photo detection, scoped evidence retrieval and bounded explanation."""
from pathlib import Path
import base64, hashlib, io, json, math, os, sys, threading, time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'kb'))
from runtime import configure
configure()
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['MPLCONFIGDIR'] = str(ROOT / 'kb/.runtime/cache/matplotlib')
import retrieve
import openrouter_client
LABELS = ('dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat')
COMPATIBLE = {'body': {0,1,2}, 'windshield': {2,3}, 'side_window': {2,3}, 'lamp': {2,4}, 'tire': {5}}
DEFAULT = ROOT / 'experiments/cardoctor-hf/.runtime/downloaded-continuation-12/checkpoint_best_ema.pth'

class Pipeline:
    def __init__(self, checkpoint=None, detector=None, retriever=None):
        self.checkpoint = Path(checkpoint or os.environ.get('CARDOCTOR_CHECKPOINT', DEFAULT)).resolve()
        self.detector, self.retriever = detector, retriever
        self.lock = threading.Lock()
        self.identity = None

    def close(self):
        if self.retriever is not None and hasattr(self.retriever, "close"):
            self.retriever.close()

    def model(self):
        if self.detector is None:
            if not self.checkpoint.is_file() or self.checkpoint.stat().st_size < 1000000:
                raise ValueError('Trained checkpoint is still downloading or missing. Check server setup.')
            # Only a server-configured, trusted checkpoint is loaded; uploads are images only.
            with self.checkpoint.open('rb') as stream:
                self.identity = hashlib.file_digest(stream, 'sha256').hexdigest()
            manifest = self.checkpoint.parent / 'CHECKPOINTS.json'
            if manifest.exists():
                inventory = json.loads(manifest.read_text(encoding='utf-8'))
                entry = next((r for r in inventory if r['file'] == self.checkpoint.name), None)
                if entry is None or entry['sha256'] != self.identity or entry['bytes'] != self.checkpoint.stat().st_size:
                    raise ValueError('Checkpoint differs from the recorded training output.')
            import torch
            torch.set_num_threads(min(4, torch.get_num_threads()))
            from rfdetr import RFDETRNano
            candidate = RFDETRNano.from_checkpoint(str(self.checkpoint), device='cpu', amp=False, compile=False)
            if candidate.class_names != list(LABELS):
                raise ValueError('Checkpoint damage labels differ from the app adapter.')
            self.detector = candidate
        return self.detector

    def analyze(self, data):
        if not self.lock.acquire(blocking=False):
            raise BlockingIOError('Another analysis is running. Please try again shortly.')
        try:
            return self._analyze(data)
        finally:
            self.lock.release()

    def _analyze(self, data):
        from PIL import Image, ImageOps, UnidentifiedImageError
        start = time.perf_counter()
        if not isinstance(data, dict): raise ValueError('Expected an object.')
        query = data.get('query', '')
        if not isinstance(query, str) or len(query)>2000: raise ValueError('Describe symptoms in at most 2,000 characters.')
        part = data.get('part', '')
        if part not in retrieve.PARTS | {''}: raise ValueError('Choose a valid component.')
        for key in ('vehicle','propulsion','confirmed_manual'):
            if not isinstance(data.get(key,''),str) or len(data.get(key,''))>100: raise ValueError('Invalid vehicle context.')
        if data.get('retriever','hybrid') not in {'hybrid','keyword'}: raise ValueError('Invalid retrieval mode.')
        if not isinstance(data.get('use_llm',False),bool): raise ValueError('Invalid explanation choice.')
        threshold=data.get('threshold',0.35)
        if isinstance(threshold,bool) or not isinstance(threshold,(float,int)) or not math.isfinite(threshold) or not 0.1<=threshold<=0.9:
            raise ValueError('Detection threshold must be between 0.1 and 0.9.')
        context=data.get('context',{})
        if not isinstance(context,dict) or set(context)-{'engine_running','parking_brake_released'} or any(not isinstance(v,bool) for v in context.values()):
            raise ValueError('Use boolean engine and parking-brake context.')
        if data.get('propulsion','') not in retrieve.PROPULSIONS | {''}: raise ValueError('Choose a valid propulsion.')
        manual=data.get('confirmed_manual','')
        if manual and manual not in retrieve.load()[1]: raise ValueError('Unknown manual source ID.')
        encoded=data.get('image','')
        if not isinstance(encoded,str) or len(encoded)>12*1024*1024: raise ValueError('Image is too large.')
        if ',' in encoded: encoded=encoded.split(',',1)[1]
        image=None
        if encoded:
            try:
                raw=base64.b64decode(encoded,validate=True)
                if len(raw)>8*1024*1024: raise ValueError('Use an image under 8 MB.')
                with Image.open(io.BytesIO(raw)) as source:
                    if source.format not in {'JPEG','PNG','WEBP'}: raise ValueError('Use JPEG, PNG or WebP.')
                    if source.width*source.height>24000000: raise ValueError('Image has too many pixels; resize first.')
                    image=ImageOps.exif_transpose(source).convert('RGB')
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
                raise ValueError('The image could not be decoded.') from None
            if min(image.size)<96: raise ValueError('Use a larger, clearer photo (at least 96 pixels per side).')
            image.thumbnail((2000,2000))
        elif not query.strip():
            raise ValueError('Add a photo or describe a symptom.')
        cv_start=time.perf_counter()
        detections=[]
        vision_status='no_photo' if image is None else 'unsupported_component' if part and part not in COMPATIBLE else 'completed'
        if vision_status=='completed':
            predictions=self.model().predict(image,threshold=threshold)
            for box,score,cid in zip(predictions.xyxy,predictions.confidence,predictions.class_id):
                cid=int(cid); score=float(score)
                if not 0<=cid<len(LABELS) or not math.isfinite(score): continue
                x1,y1,x2,y2=[float(x) for x in box]
                if not all(math.isfinite(x) for x in (x1,y1,x2,y2)): continue
                x1=max(0,min(image.width,x1));x2=max(0,min(image.width,x2))
                y1=max(0,min(image.height,y1));y2=max(0,min(image.height,y2))
                if x2<=x1 or y2<=y1:continue
                detections.append({'class_id':cid,'label':LABELS[cid],'score':round(score,4),'box':[round(v,1) for v in [x1,y1,x2,y2]]})
        detections=sorted(detections,key=lambda d:-d['score'])[:30]
        cv_seconds=time.perf_counter()-cv_start
        matching=[d for d in detections if d['class_id'] in COMPATIBLE.get(part,set())]
        # Component is supplied by the user, never guessed from a damage category.
        label=matching[0]['label'] if matching else ''
        params={key:data.get(key,'') for key in ('part','vehicle','propulsion','confirmed_manual')}
        params.update(context=context,vision_label=label)
        warnings=[]
        if detections and not matching and part:
            warnings.append('The detected damage categories do not match the selected component. Confirm the affected component; retrieval uses your description only.')
        method=data.get('retriever','hybrid')
        rag_start=time.perf_counter()
        if method=='hybrid':
            try:
                if self.retriever is None:
                    from vector_store import VectorKB
                    self.retriever=VectorKB()
                bundle=self.retriever.query(query,**params)
            except (RuntimeError,OSError,ImportError):
                bundle=retrieve.retrieve(query,**params)
                warnings.append('Vector retrieval is unavailable; using sourced keyword retrieval.')
                method='keyword_fallback'
        else:bundle=retrieve.retrieve(query,**params)
        # The generic retriever is also used alone; remove its standalone-only limitation here.
        bundle['limitations']=[x for x in bundle['limitations'] if not x.startswith('No trained CV inference')]
        rag_seconds=time.perf_counter()-rag_start
        explanation={'status':'evidence_only','api_called':False,'evidence_report':retrieve.as_markdown(bundle)}
        llm_start=time.perf_counter()
        if data.get('use_llm',False):explanation=openrouter_client.explain(bundle)
        llm_seconds=time.perf_counter()-llm_start
        if vision_status=='completed' and not detections:warnings.append('No candidate damage was detected at this threshold. This does not establish that the vehicle is undamaged.')
        if vision_status=='unsupported_component':warnings.append('The damage detector covers body panels, glass, lamps and tyres. This component uses your symptom description for retrieval; the photo has not been visually assessed.')
        if vision_status=='no_photo':warnings.append('Text-only assessment: no visual damage detection was performed.')
        preview=None
        if image is not None:
            buffer=io.BytesIO();image.save(buffer,format='JPEG',quality=85)
            preview='data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()
        return {'detections':detections,'image':preview,
            'image_size':list(image.size) if image is not None else None,'threshold':threshold,'routed_cv_label':label,
            'vision_status':vision_status,'confirmed_manual':manual,
            'evidence':bundle,'explanation':explanation,'warnings':warnings,'retriever_used':method,
            'model':{'name':'RF-DETR Nano','checkpoint':self.checkpoint.name,'sha256':self.identity,
                     'purpose':'Trained damage detector; predictions are unverified candidates.'},
            'timing':{'cv_seconds':round(cv_seconds,3),'retrieval_seconds':round(rag_seconds,3),'explanation_seconds':round(llm_seconds,3),'total_seconds':round(time.perf_counter()-start,3)},
            'limits':['Detection scores are not calibrated probabilities.','Photos cannot establish hidden faults, damage depth, repair cost or roadworthiness.','User-confirmed component context is required for repair retrieval.']}


def report(result):
    bundle=result['evidence']
    lines=['# CarDoctor assessment','', 'Experimental assessment with sourced guidance. Mechanic review is required.','',
           '## Reported context','',
           f"Component: {bundle['part'] or 'not confirmed'}",
           f"Vehicle: {bundle['vehicle'] or 'not supplied'}",
           f"Propulsion: {bundle['propulsion'] or 'unknown'}",'',
           'User description (unverified):','']
    # Quote user text so it cannot become report headings or source annotations.
    lines += ['> '+line for line in bundle['query'].splitlines()] or ['> No description supplied.']
    lines += ['',f"Confirmed manual source: {result['confirmed_manual'] or 'not supplied'}",f"Confirmed context: {json.dumps(bundle['context'],sort_keys=True)}",'', '## Visual candidates','',
              f"Visual analysis: {result['vision_status']}; detection threshold: {result['threshold']}.",'']
    for d in result['detections']:lines.append(f"- {d['label']}: model score {d['score']:.3f}; box {d['box']}")
    if result['vision_status']=='completed' and not result['detections']:lines.append('No candidate detected at the selected threshold; damage may still be present.')
    lines+=['','## Warnings and limits','']+['- '+x for x in result['warnings']+result['limits']]
    lines+=['','## Retrieved guidance','',retrieve.as_markdown(bundle)]
    answer=result['explanation'].get('answer')
    if answer:
        sources={s['id']:s for s in bundle['sources']}
        lines+=['','## Generated explanation - unreviewed','']
        for c in answer['claims']:
            source=sources[c['source_id']]
            lines.append(f"- {c['text']} [{c['record_id']} / {c['source_id']}]({source['url']})")
        lines+=['','Generated follow-up questions:','']+['- '+q for q in answer['follow_up_questions']]
    lines+=['','## Run details','',f"Model SHA-256: {result['model']['sha256'] if result['vision_status']=='completed' else 'Visual detector not run for this assessment'}",
            f"Retrieval: {result['retriever_used']}",f"Explanation status: {result['explanation']['status']}",
            f"Seconds: {result['timing']}",'']
    return '\n'.join(lines)
