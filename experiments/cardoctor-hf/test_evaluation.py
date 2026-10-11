"""Regression checks for instance matching, including VehiDE category ID zero."""
import unittest,contextlib,io
from evaluate_cardd import fixed_threshold_metrics

class MatchingTests(unittest.TestCase):
 def data(self):
  return {"categories":[{"id":0,"name":"native_zero"}],"annotations":[{"image_id":0,"category_id":0,"bbox":[0,0,10,10],"iscrowd":0}]}
 def pred(self,score=.8):
  return {"image_id":0,"category_id":0,"bbox":[0,0,10,10],"score":score}
 def test_native_category_zero_matches(self):
  metrics=fixed_threshold_metrics(self.data(),[self.pred()])
  self.assertEqual(metrics['micro'],{'tp':1,'fp':0,'fn':0,'precision':1,'recall':1,'f1':1})
 def test_duplicate_prediction_is_false_positive(self):
  metrics=fixed_threshold_metrics(self.data(),[self.pred(),self.pred(.7)])
  self.assertEqual((metrics['micro']['tp'],metrics['micro']['fp'],metrics['micro']['fn']),(1,1,0))
  self.assertAlmostEqual(metrics['macro_f1'],2/3)
 def test_below_threshold_is_not_a_detection(self):
  metrics=fixed_threshold_metrics(self.data(),[self.pred(.2)])
  self.assertEqual((metrics['micro']['tp'],metrics['micro']['fp'],metrics['micro']['fn']),(0,0,1))
 def test_crowd_targets_are_explicitly_unsupported(self):
  data=self.data();data['annotations'][0]['iscrowd']=1
  with self.assertRaises(ValueError):fixed_threshold_metrics(data,[self.pred()])

 def test_coco_category_zero_works_with_positive_annotation_id(self):
  from evaluate_vehide import coco_bbox_metrics
  data={"info":{},"images":[{"id":0,"width":100,"height":100}],**self.data()}
  data['annotations']=[{**a,'id':0,'area':100} for a in data['annotations']]
  with contextlib.redirect_stdout(io.StringIO()):bbox,_=coco_bbox_metrics(data,[self.pred()])
  self.assertAlmostEqual(bbox['mAP50_95'],1.0)
  self.assertEqual(data['annotations'][0]['id'],0)  # Source IDs stay intact.

if __name__=='__main__':unittest.main()
