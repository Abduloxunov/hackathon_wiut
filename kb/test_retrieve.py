"""Engineering checks for evidence isolation, binding and unknown handling.
These are not clinical, CV accuracy or retrieval relevance measurements.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import retrieve

class KnowledgeTests(unittest.TestCase):
    def test_catalog(self):
        records, sources, providers = retrieve.load()
        self.assertEqual((len(records),len(sources),len(providers)),(28,20,5))
        self.assertEqual(len({r['id'] for r in records}),len(records))
        self.assertEqual(set().union(*(set(r['vision_labels']) for r in records)),retrieve.LABELS)

    def test_price_unavailable(self):
        records, _, providers = retrieve.load()
        self.assertTrue(all(r['cost_estimate'] is None for r in records))
        self.assertTrue(all(p['price_ranges'] is None and p['coordinates'] is None for p in providers))
        self.assertTrue(all(not p['contact_verified_by_call'] for p in providers))

    def test_unknown(self):
        result = retrieve.retrieve('quantum banana spaceship',part='body')
        self.assertEqual(result['status'],'no_evidence')
        self.assertEqual(result['sources'],[])

    def test_empty(self):
        self.assertEqual(retrieve.retrieve('')['status'],'no_evidence')

    def test_missing_part(self):
        result = retrieve.retrieve('crack')
        self.assertEqual(result['status'],'needs_context')
        self.assertEqual(result['evidence'],[])

    def test_component_isolation(self):
        for part in ['body','windshield','tire']:
            result = retrieve.retrieve('crack',part=part)
            self.assertTrue(result['evidence'])
            self.assertTrue(all(r['part'] == part for r in result['evidence']))

    def test_bulge_and_dent_isolation(self):
        result = retrieve.retrieve('bulge sidewall',part='tire')
        self.assertEqual(result['evidence'][0]['id'],'K012')
        self.assertNotIn('K005',[r['id'] for r in result['evidence']])

    def test_model_scope(self):
        result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Spark',confirmed_manual='S11',context={'engine_running':True})
        self.assertEqual(result['evidence'],[])

    def test_manual_required(self):
        result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Cobalt',context={'engine_running':True})
        self.assertEqual(result['status'],'needs_context')
        self.assertEqual(result['evidence'],[])

    def test_wrong_manual(self):
        result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Cobalt',confirmed_manual='S12',context={'engine_running':True})
        self.assertEqual(result['evidence'],[])

    def test_engine_state_required(self):
        for context in [{},{'engine_running':False}]:
            result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Cobalt',confirmed_manual='S11',context=context)
            self.assertEqual(result['evidence'],[])
            self.assertEqual(result['status'],'needs_context')

    def test_confirmed_engine_warning(self):
        result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Cobalt',confirmed_manual='S11',context={'engine_running':True})
        self.assertEqual(result['evidence'][0]['id'],'K021')
        self.assertEqual(result['evidence'][0]['urgency']['level'],'stop_engine')

    def test_parking_brake_guard(self):
        result = retrieve.retrieve('brake warning',part='dashboard',vehicle='Lacetti',confirmed_manual='S14',context={'engine_running':True})
        self.assertEqual(result['evidence'],[])
        self.assertEqual(result['status'],'needs_context')
        result = retrieve.retrieve('brake warning',part='dashboard',vehicle='Lacetti',confirmed_manual='S14',context={'engine_running':True,'parking_brake_released':True})
        self.assertEqual(result['evidence'][0]['id'],'K023')

    def test_gentra_is_not_alias(self):
        result = retrieve.retrieve('brake warning',part='dashboard',vehicle='Gentra',confirmed_manual='S14',context={'engine_running':True,'parking_brake_released':True})
        self.assertEqual(result['evidence'],[])

    def test_cobalt_mcm_is_not_alias(self):
        result = retrieve.retrieve('oil pressure',part='dashboard',vehicle='Cobalt MCM',confirmed_manual='S11',context={'engine_running':True})
        self.assertEqual(result['evidence'],[])

    def test_powertrain_required(self):
        result = retrieve.retrieve('battery crash',part='ev',vehicle='BYD Song')
        self.assertEqual(result['status'],'needs_context')
        self.assertEqual(result['evidence'],[])
        result = retrieve.retrieve('battery crash',part='ev',propulsion='ice')
        self.assertEqual(result['evidence'],[])
        result = retrieve.retrieve('battery crash',part='ev',propulsion='phev')
        self.assertEqual(result['evidence'][0]['id'],'K019')

    def test_source_subset(self):
        result = retrieve.retrieve('crack',part='windshield')
        used = {ref['source_id'] for r in result['evidence'] for ref in r['source_refs']}
        self.assertEqual(used,{s['id'] for s in result['sources']})
        self.assertIn('https://www3.safelite.com',retrieve.as_markdown(result))

    def test_uzbek_and_russian_terms(self):
        self.assertTrue(retrieve.retrieve('yoriq',part='tire')['evidence'])
        self.assertTrue(retrieve.retrieve('царапина',part='body')['evidence'])

    def test_label_aliases(self):
        for part, alias, target in [('side_window','glassshatter','K008'),('lamp','lampbroken','K027'),('tire','tireflat','K009')]:
            result = retrieve.retrieve('',part=part,vision_label=alias)
            self.assertEqual(result['evidence'][0]['id'],target)

    def test_context_types(self):
        with self.assertRaises(ValueError):
            retrieve.retrieve('oil pressure',part='dashboard',context={'engine_running':'false'})
        with self.assertRaises(ValueError):
            retrieve.retrieve('x',context={'untrusted_flag':True})

    def test_invalid_input(self):
        for kw in [{'part':'banana'},{'propulsion':'hydrogen'},{'vision_label':'engine broken'},{'limit':0}]:
            with self.assertRaises(ValueError): retrieve.retrieve('x',**kw)

    def test_c_disk_output_blocked(self):
        with self.assertRaises(ValueError): retrieve.d_output('C:/should-not-write.md')

    def test_unbound_source_rejected(self):
        records, sources, providers = retrieve.load()
        records = copy.deepcopy(records)
        records[0]['source_refs'][0]['source_id'] = 'MISSING'
        with patch('retrieve.blocks',side_effect=[records,list(sources.values()),providers]):
            with self.assertRaises(ValueError): retrieve.load()

    def test_duplicate_id_rejected(self):
        records, sources, providers = retrieve.load()
        with patch('retrieve.blocks',side_effect=[records+[records[0]],list(sources.values()),providers]):
            with self.assertRaises(ValueError): retrieve.load()

if __name__ == '__main__':
    unittest.main()
