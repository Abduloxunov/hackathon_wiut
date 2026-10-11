import base64,io,sys,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pipeline import Pipeline,report
class FakeDetector:
    def __init__(self,classes=(1,6)):
        self.classes=classes
    def predict(self,image,threshold):
        return SimpleNamespace(xyxy=np.array([[10,10,100,100]]*len(self.classes)),confidence=np.array([.8]*len(self.classes)),class_id=np.array(self.classes))
def request(**updates):
    b=io.BytesIO();Image.new('RGB',(200,200),'gray').save(b,format='PNG')
    data={'image':base64.b64encode(b.getvalue()).decode(),'part':'body','query':'scratch paint door','retriever':'keyword','use_llm':False}
    data.update(updates);return data
class Tests(unittest.TestCase):
    def test_background_filtered_and_matching_label_routes(self):
        result=Pipeline(detector=FakeDetector()).analyze(request())
        self.assertEqual([d['class_id'] for d in result['detections']],[1])
        self.assertEqual(result['routed_cv_label'],'scratch')
        self.assertTrue(result['evidence']['evidence'])
    def test_component_not_inferred_from_damage_class(self):
        result=Pipeline(detector=FakeDetector()).analyze(request(part='tire',query=''))
        self.assertEqual(result['routed_cv_label'],'')
        self.assertFalse(result['evidence']['evidence'])
    def test_context_required_prevents_paid_call(self):
        with patch('openrouter_client.send') as send:
            result=Pipeline(detector=FakeDetector()).analyze(request(part='',use_llm=True))
        self.assertEqual(result['evidence']['status'],'needs_context');send.assert_not_called()
    def test_invalid_images_rejected_before_detector(self):
        with self.assertRaises(ValueError):Pipeline(detector=FakeDetector()).analyze(request(image='not base64!'))
    def test_invalid_threshold_and_context(self):
        for updates in [{'threshold':float('nan')},{'threshold':True},{'context':{'engine_running':'yes'}},{'use_llm':'yes'}]:
            with self.assertRaises(ValueError):Pipeline(detector=FakeDetector()).analyze(request(**updates))
    def test_vector_failure_uses_explicit_keyword_fallback(self):
        class Broken:
            def query(self,*args,**kwargs):raise RuntimeError('Index unavailable')
        result=Pipeline(detector=FakeDetector(),retriever=Broken()).analyze(request(retriever='hybrid'))
        self.assertEqual(result['retriever_used'],'keyword_fallback');self.assertTrue(result['warnings'])
    def test_no_detections_does_not_claim_undamaged(self):
        result=Pipeline(detector=FakeDetector(classes=())).analyze(request())
        self.assertTrue(any('does not establish' in x for x in result['warnings']))
    def test_concurrent_request_rejected(self):
        p=Pipeline(detector=FakeDetector());p.lock.acquire()
        with self.assertRaises(BlockingIOError):p.analyze(request())
        p.lock.release()
    def test_text_only_does_not_call_detector_or_claim_no_damage(self):
        detector=FakeDetector()
        with patch.object(detector,'predict') as predict:
            result=Pipeline(detector=detector).analyze(request(image=''))
        predict.assert_not_called()
        self.assertEqual(result['vision_status'],'no_photo')
        self.assertIsNone(result['image'])
        self.assertTrue(result['evidence']['evidence'])
        self.assertEqual(result['routed_cv_label'],'')
        self.assertFalse(any('No candidate damage' in x for x in result['warnings']))
    def test_dashboard_photo_is_not_classified_by_exterior_detector(self):
        detector=FakeDetector()
        with patch.object(detector,'predict') as predict:
            result=Pipeline(detector=detector).analyze(request(part='dashboard',query='red oil pressure warning'))
        predict.assert_not_called()
        self.assertEqual(result['vision_status'],'unsupported_component')
        self.assertTrue(result['image'])
        self.assertTrue(any('not been visually assessed' in x for x in result['warnings']))
    def test_invalid_context_rejected_before_inference(self):
        detector=FakeDetector()
        with patch.object(detector,'predict') as predict:
            for updates in [{'context':['bad']},{'propulsion':'diesel'},{'confirmed_manual':'unknown-id'},{'context':{'engine_running':1}},{'image':'','query':''}]:
                with self.assertRaises(ValueError):Pipeline(detector=detector).analyze(request(**updates))
        predict.assert_not_called()
    def test_export_preserves_context_warning_threshold_and_followups(self):
        result=Pipeline(detector=FakeDetector()).analyze(request(part='tire',query='flat tyre',vehicle='Example car',threshold=.4,context={'engine_running':False}))
        text=report(result)
        self.assertIn('Vehicle: example car',text)
        self.assertIn('detection threshold: 0.4',text)
        self.assertIn('do not match the selected component',text)
        self.assertIn('engine_running',text)
        self.assertIn('Explanation status: evidence_only',text)
        self.assertIn('## Warnings and limits',text)
        text=report(Pipeline(detector=FakeDetector()).analyze(request(image='')))
        self.assertIn('Visual detector not run for this assessment',text)
        self.assertNotIn('No candidate detected at the selected threshold',text)
if __name__=='__main__':unittest.main()
