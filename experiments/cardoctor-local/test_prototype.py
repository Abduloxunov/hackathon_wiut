"""Engineering tests use synthetic fixtures, never vehicle accuracy claims."""
from pathlib import Path
import os,uuid
BASE=Path(__file__).resolve().parent
PRODUCTION=BASE/'.runtime'
os.environ['CARDOCTOR_RUNTIME']=str(PRODUCTION/'tests'/uuid.uuid4().hex)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import core
core.MODEL_FILE=PRODUCTION/'cache/torch/checkpoints/resnet18-f37072fd.pth'
import base64,io,json,threading,time,unittest,urllib.request,urllib.error
import numpy as np
from PIL import Image,ImageDraw
import train,server
from reports import markdown_report

def fixture(kind,offset=0):
    image=Image.new('RGB',(320,240),(225-offset,229,232));draw=ImageDraw.Draw(image)
    if kind=='circle':draw.ellipse((40+offset,25,220+offset,205),fill=(20,105,170),outline=(0,0,0),width=5)
    else:draw.rectangle((40+offset,35,225+offset,205),fill=(180,45,30),outline=(0,0,0),width=5)
    raw=io.BytesIO();image.save(raw,format='PNG');return 'data:image/png;base64,'+base64.b64encode(raw.getvalue()).decode()

class PrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.start=time.perf_counter();cls.a=fixture('circle');cls.b=fixture('square');cls.query=fixture('circle',7)
        cls.one=core.add_reference({'image':cls.a,'label':'synthetic circle','group_id':'vehicle-A','source':'Generated engineering fixture, not car damage','rights':'Original synthetic fixture'})
        cls.two=core.add_reference({'image':cls.b,'label':'synthetic square','group_id':'vehicle-B','source':'Generated engineering fixture, not car damage','rights':'Original synthetic fixture'})
        for model in ['', 'Cobalt','Other model']:
            core.add_note({'title':'Synthetic crack source fixture','excerpt':'Crack test guidance only. This is a synthetic API fixture, not automotive advice.','source_url':'https://example.org/test-fixture','vehicle':model,'tags':'crack','reviewed':True})
    def test_embedding(self):
        image,_=core.decode_image(self.a);v=core.feature(image);self.assertEqual(v.shape,(512,));self.assertAlmostEqual(float(np.linalg.norm(v)),1,places=5);np.testing.assert_allclose(v,core.feature(image),atol=1e-6)
    def test_region_validation(self):
        im,_=core.decode_image(self.a);region,bounds=core.crop_image(im,[.1,.1,.8,.8]);self.assertEqual(bounds,[32,24,256,192]);self.assertEqual(region.size,(224,168))
        for crop in [[0,0,.01,.01],[-1,0,1,1],[0,0,float('nan'),1],[0,0,True,1],[1,1,0,0]]:
            with self.subTest(crop=crop),self.assertRaises(ValueError):core.crop_image(im,crop)
    def test_encoding_rejection(self):
        for value in ['not an image','data:image/svg+xml;base64,AAAA',None,'data:image/png']:
            with self.subTest(value=value),self.assertRaises(ValueError):core.decode_image(value)
    def test_duplicate_reference(self):
        with self.assertRaises(ValueError):core.add_reference({'image':self.a,'label':'circle','group_id':'vehicle-C','source':'own','rights':'own'})
    def test_exact_and_group_exclusion(self):
        exact=core.analyze({'image':self.a});self.assertNotIn(self.one['id'],[m['id'] for m in exact['matches']]);self.assertEqual(exact['excluded_exact_images'],1)
        grouped=core.analyze({'image':self.query,'group_id':'vehicle-A'});self.assertNotIn(self.one['id'],[m['id'] for m in grouped['matches']]);self.assertEqual(grouped['excluded_same_group'],1)
    def test_vehicle_and_review_filter(self):
        notes=core.retrieve_notes('crack','Cobalt');self.assertEqual({r['vehicle'] for r in notes},{'','Cobalt'})
        self.assertEqual({r['vehicle'] for r in core.retrieve_notes('crack','')},{''})
        with self.assertRaises(ValueError):core.add_note({'title':'bad','excerpt':'bad','source_url':'javascript:alert(1)','reviewed':True})
        with self.assertRaises(ValueError):core.add_note({'title':'unreviewed','excerpt':'crack','source_url':'https://example.org','reviewed':False})
    def test_component_filter(self):
        core.add_note({'title':'Windshield fixture','excerpt':'Glass chip crack test only.','source_url':'https://example.org/glass-fixture','part':'windshield','tags':'glass crack','reviewed':True})
        self.assertNotIn('windshield',[n['part'] for n in core.retrieve_notes('glass crack','','tire')])
        self.assertNotIn('windshield',[n['part'] for n in core.retrieve_notes('glass crack','','')])
        self.assertIn('windshield',[n['part'] for n in core.retrieve_notes('glass crack','','windshield')])
    def test_no_automatic_label_to_knowledge(self):
        result=core.analyze({'image':self.query});self.assertFalse(result['damage_detector_trained']);self.assertEqual(result['knowledge'],[]);self.assertNotIn('experimental_classifier',result)
        text=markdown_report(result);self.assertIn('not',text.lower());self.assertIn('#',text);self.assertIn('cosine',text.lower())
    def test_quality_feedback(self):
        q=core.quality(Image.new('RGB',(80,80),(0,0,0)));self.assertEqual(q['dark_fraction'],1);self.assertGreaterEqual(len(q['issues']),3)
    def test_grouped_training_and_reload(self):
        # Orthogonal toy vectors exercise optimizer/serialization, not vehicle performance.
        rows=[]
        for label in range(2):
            for group in range(4):
                vector=np.zeros(512,dtype=np.float32);vector[label]=1
                rows.append({'label':'toy-'+str(label),'group_id':f'toy-{label}-{group}','image_hash':f'hash-{label}-{group}','embedding':vector.tobytes()})
        head,metrics=train.fit(rows,epochs=40);self.assertFalse(set(metrics['train_groups'])&set(metrics['validation_groups']));self.assertGreater(metrics['validation_accuracy'],.9)
        out=core.RUNTIME/'synthetic-training-smoke';train.save(head,metrics,out)
        with np.load(out/'linear_classifier.npz',allow_pickle=False) as saved:self.assertEqual(saved['weight'].shape,(512,2))
        (out/'FIXTURE-NOTICE.md').write_text('# Engineering fixture only\n\nAll vectors and labels here are synthetic. These metrics do not measure car damage accuracy.\n',encoding='utf-8')
        rows[-1]['image_hash']=rows[0]['image_hash']
        with self.assertRaises(ValueError):train.grouped_split(rows)
    def test_multiclass_grouped_split(self):
        rows=[{'label':f'class-{label}','group_id':f'vehicle-{label}-{group}','image_hash':f'image-{label}-{group}'} for label in range(3) for group in range(3)]
        training,validation,labels=train.grouped_split(rows)
        self.assertEqual({rows[i]['label'] for i in validation},set(labels))
        self.assertEqual({rows[i]['label'] for i in training},set(labels))
        self.assertFalse({rows[i]['group_id'] for i in training}&{rows[i]['group_id'] for i in validation})
    def test_http_flow(self):
        service=server.ThreadingHTTPServer(('127.0.0.1',8765),server.Handler);thread=threading.Thread(target=service.serve_forever,daemon=True);thread.start()
        base='http://127.0.0.1:8765'
        def request(path,data=None,token=None):
            headers={};body=None
            if data is not None:body=json.dumps(data).encode();headers={'Content-Type':'application/json','X-CarDoctor-Token':token or ''}
            with urllib.request.urlopen(urllib.request.Request(base+path,data=body,headers=headers),timeout=20) as response:return response.status,response.read()
        try:
            status,raw=request('/api/health');health=json.loads(raw);self.assertEqual(status,200);self.assertTrue(health['model_available']);self.assertTrue(health['storage'].startswith('D:'))
            for path in ['/','/app.js','/style.css']:self.assertEqual(request(path)[0],200)
            with self.assertRaises(urllib.error.HTTPError) as rejected:request('/api/analyze',{'image':self.query})
            self.assertEqual(rejected.exception.code,403)
            status,raw=request('/api/analyze',{'image':self.query,'symptoms':'crack','vehicle':'Cobalt'},health['token']);result=json.loads(raw);self.assertEqual(status,200);self.assertEqual({n['vehicle'] for n in result['knowledge']},{'','Cobalt'});self.assertNotIn('windshield',[n['part'] for n in result['knowledge']])
            status,raw=request('/api/export',{'image':self.query},health['token']);report=json.loads(raw);self.assertTrue(Path(report['path']).is_file());self.assertTrue(report['path'].startswith('D:'));self.assertTrue(report['path'].endswith('.md'))
        finally:service.shutdown();service.server_close();thread.join()
    @classmethod
    def tearDownClass(cls):
        elapsed=round(time.perf_counter()-cls.start,2);print('Fixture runtime on D:',core.RUNTIME);print('Engineering suite seconds:',elapsed)

if __name__=='__main__':unittest.main(verbosity=2)
