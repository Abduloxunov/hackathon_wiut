"""Engineering checks only; fixtures are coloured rectangles, not car-damage data."""
from pathlib import Path
import copy
import csv
import json
import tempfile
import unittest
import zipfile
from PIL import Image
from data_tools import audit_dataset, extract_dataset, make_smoke_subset

class DataChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cardoctor-audit-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'dataset'
        for index, split in enumerate(('train', 'valid', 'test')):
            folder = self.root / split
            folder.mkdir(parents=True)
            Image.new('RGB', (24, 20), (index * 70, 20, 100)).save(folder / 'a.png')
            Image.new('RGB', (24, 20), (index * 70, 40, 100)).save(folder / 'b.png')
            data = {'categories':[{'id':1,'name':'dent'}],
                    'images':[{'id':i,'file_name':n,'width':24,'height':20} for i,n in [(1,'a.png'),(2,'b.png')]],
                    'annotations':[{'id':1,'image_id':1,'category_id':1,'bbox':[2,2,8,6], 'area':48,'iscrowd':0}]}
            (folder / '_annotations.coco.json').write_text(json.dumps(data))
        (self.root / 'provenance.json').write_text(json.dumps({'source':'Synthetic engineering fixture',
            'permission':'Locally generated fixture; never used for damage training', 'permission_confirmed':True,
            'split_policy':'Distinct fixtures'}))
    def edit(self, split, change):
        p=self.root / split / '_annotations.coco.json'
        data=json.loads(p.read_text()); change(data); p.write_text(json.dumps(data))
    def test_valid_audit_and_no_test_in_smoke(self):
        report,_=audit_dataset(self.root)
        self.assertEqual(report['splits']['train']['images'],2)
        target=Path(self.temp.name)/'smoke'
        make_smoke_subset(self.root,target,2,2)
        self.assertFalse((target/'test').exists())
        self.assertEqual(audit_dataset(target)[0]['splits']['valid']['annotations'],1)
    def test_permission_missing(self):
        (self.root/'provenance.json').unlink()
        with self.assertRaisesRegex(ValueError,'provenance'): audit_dataset(self.root)
    def test_permission_unconfirmed(self):
        p=self.root/'provenance.json'; d=json.loads(p.read_text()); d['permission_confirmed']=False;p.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'permission'): audit_dataset(self.root)
    def test_duplicate_leakage(self):
        (self.root/'valid/a.png').write_bytes((self.root/'train/a.png').read_bytes())
        with self.assertRaisesRegex(ValueError,'leakage'): audit_dataset(self.root)
    def test_dimensions(self):
        self.edit('train',lambda d:d['images'][0].update(width=999))
        with self.assertRaisesRegex(ValueError,'dimensions'): audit_dataset(self.root)
    def test_invalid_box(self):
        self.edit('train',lambda d:d['annotations'][0].update(bbox=[2,2,999,6]))
        with self.assertRaisesRegex(ValueError,'bounding box'): audit_dataset(self.root)
    def test_nan_box(self):
        self.edit('train',lambda d:d['annotations'][0].update(bbox=[2,2,float('nan'),6]))
        with self.assertRaisesRegex(ValueError,'nonfinite'): audit_dataset(self.root)
    def test_mismatched_categories(self):
        self.edit('valid',lambda d:d['categories'][0].update(name='scratch'))
        with self.assertRaisesRegex(ValueError,'match'): audit_dataset(self.root)
    def test_annotation_bad_reference(self):
        self.edit('train',lambda d:d['annotations'][0].update(image_id=999))
        with self.assertRaisesRegex(ValueError,'reference'): audit_dataset(self.root)
    def test_group_leakage(self):
        with (self.root/'groups.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['split','file_name','group_id']);writer.writeheader()
            for split in ('train','valid','test'):
                for name in ('a.png','b.png'):
                    writer.writerow({'split':split,'file_name':name,'group_id':'same-car'})
        with self.assertRaisesRegex(ValueError,'group.*leaks'): audit_dataset(self.root)
    def test_archive_traversal_before_extract(self):
        archive=Path(self.temp.name)/'bad.zip';dest=Path(self.temp.name)/'unpacked'
        with zipfile.ZipFile(archive,'w') as z:z.writestr('../escaped.txt','bad')
        with self.assertRaisesRegex(ValueError,'escapes'): extract_dataset(archive,dest)
        self.assertFalse(dest.exists())
        self.assertFalse((dest.parent/'escaped.txt').exists())
    def test_existing_directory_preserved(self):
        dest=Path(self.temp.name)/'existing';dest.mkdir();(dest/'marker').write_text('preserve')
        with self.assertRaisesRegex(ValueError,'fresh'):extract_dataset(Path(self.temp.name)/'missing.zip',dest)
        self.assertEqual((dest/'marker').read_text(),'preserve')

if __name__=='__main__': unittest.main()
