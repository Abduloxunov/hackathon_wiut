"""Format/selection/authorization checks; synthetic fixtures are never training results."""
import copy
import json
import random
import tempfile
import unittest
import zipfile
from pathlib import Path
from PIL import Image
from data_tools import audit_dataset, select_smoke_images
from prepare_cardd import convert_cardd, archive_smoke, SPLITS

class PreparationChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="cardd-convert-");self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/"original";self.target=self.root/"converted"
        (self.source/"annotations").mkdir(parents=True)
        for split_index,split in enumerate(SPLITS):
            folder=self.source/split;folder.mkdir()
            Image.new("RGB",(24,20),(30*split_index,60,110)).save(folder/"a.png")
            data={"categories":[{"id":1,"name":"dent"}],"images":[{"id":1,"file_name":"a.png","width":24,"height":20}],
                "annotations":[{"id":1,"image_id":1,"category_id":1,"bbox":[1,1,10,10],"area":100,"iscrowd":0}]}
            (self.source/"annotations"/("instances_"+split+".json")).write_text(json.dumps(data),encoding="utf-8")
    def test_conversion_preserves_bytes_and_ids(self):
        before=(self.source/"annotations/instances_train2017.json").read_bytes()
        provenance=convert_cardd(self.source,self.target,user_authorized=True)
        self.assertEqual((self.target/"train/_annotations.coco.json").read_bytes(),before)
        self.assertEqual((self.source/"annotations/instances_train2017.json").read_bytes(),before)
        self.assertEqual((self.target/"train/a.png").stat().st_ino,(self.source/"train2017/a.png").stat().st_ino)
        self.assertFalse(provenance["permission_confirmed"])
        self.assertEqual(audit_dataset(self.target)[0]["authorization_status"],"user_directed_research_owner_consent_unverified")
        self.assertTrue((self.target/"test/_annotations.coco.json").is_file())
    def test_user_directive_not_inferred_by_default(self):
        convert_cardd(self.source,self.target)
        with self.assertRaisesRegex(ValueError,"authorized"):audit_dataset(self.target)
    def test_string_authorization_not_accepted(self):
        convert_cardd(self.source,self.target)
        path=self.target/"provenance.json";data=json.loads(path.read_text());data["user_authorized_research_use"]="true";path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,"authorized"):audit_dataset(self.target)
    def test_existing_files_not_overwritten(self):
        self.target.mkdir();(self.target/"keep").write_text("keep")
        with self.assertRaisesRegex(ValueError,"exists"):convert_cardd(self.source,self.target)
        self.assertEqual((self.target/"keep").read_text(),"keep")
    def test_unsafe_names_rejected_before_mutation(self):
        p=self.source/"annotations/instances_train2017.json";data=json.loads(p.read_text());data["images"][0]["file_name"]="../escape.png";p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,"escapes"):convert_cardd(self.source,self.target)
        self.assertFalse(self.target.exists())
    def test_category_mismatch_rejected(self):
        p=self.source/"annotations/instances_val2017.json";data=json.loads(p.read_text());data["categories"][0]["name"]="scratch";p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,"schemas"):convert_cardd(self.source,self.target)
    def test_class_coverage_and_determinism(self):
        data={"categories":[{"id":1},{"id":2}],"images":[{"id":i} for i in range(10)],
            "annotations":[{"image_id":i,"category_id":1 if i<8 else 2} for i in range(10)]}
        first=select_smoke_images(data,4,random.Random(42),2)
        self.assertEqual(first,select_smoke_images(data,4,random.Random(42),2))
        self.assertEqual(len({i["id"] for i in first if i["id"]>=8}),2)
        with self.assertRaisesRegex(ValueError,"too small"):select_smoke_images(data,2,random.Random(42),2)
    def test_archive_excludes_test_and_checks_crc(self):
        subset=self.root/"subset";(subset/"train").mkdir(parents=True);(subset/"valid").mkdir()
        (subset/"train/a.txt").write_text("real fixture content")
        archive=self.root/"smoke.zip";meta=archive_smoke(subset,archive)
        self.assertEqual(len(meta["sha256"]),64)
        with zipfile.ZipFile(archive) as z:self.assertIsNone(z.testzip())
        with self.assertRaisesRegex(ValueError,"exists"):archive_smoke(subset,archive)

if __name__=="__main__":unittest.main()
