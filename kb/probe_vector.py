"""Development probes on real embeddings; not a held-out automotive benchmark."""
import json
import time
from pathlib import Path
import retrieve
from vector_store import VectorKB

CASES = [
 ('Tyre outward bubble', 'There is a bubble sticking out of the rubber near the wheel.', {'part':'tire'}, ['K012'], 'candidates_found'),
 ('Tyre inward dip', 'There is a hollow inward dip in the side of the tyre.', {'part':'tire'}, ['K013'], 'candidates_found'),
 ('Front glass chip', 'A stone left a small chip in the front glass.', {'part':'windshield'}, ['K006'], 'candidates_found'),
 ('Nail in tread', 'A nail is stuck in the tread.', {'part':'tire'}, ['K010'], 'candidates_found'),
 ('Misty headlight', 'The headlight looks misty inside after rain.', {'part':'lamp'}, ['K028'], 'candidates_found'),
 ('Paint scratch with unknown depth', 'Paint has a thin scratch on the door.', {'part':'body'}, ['K001','K002'], 'candidates_found'),
 ('Split bumper', 'The plastic bumper is split.', {'part':'body'}, ['K004'], 'candidates_found'),
 ('Green puddle', 'A green puddle is under my car.', {'part':'fluid'}, ['K017'], 'candidates_found'),
 ('Flooded EV', 'The electric car was partly underwater.', {'part':'ev','propulsion':'ev'}, ['K020'], 'candidates_found'),
 ('Confirmed Cobalt running-engine warning', 'The oil pressure light stays on after the motor starts.', {'part':'dashboard','vehicle':'Cobalt','confirmed_manual':'S11','context':{'engine_running':True}}, ['K021'], 'candidates_found'),
 ('Russian tyre protrusion', 'На боковине шины появилась выпуклая шишка.', {'part':'tire'}, ['K012'], 'candidates_found'),
 ('Uzbek tyre protrusion', 'Shinaning yon tomonida tashqariga shish chiqdi.', {'part':'tire'}, ['K012'], 'candidates_found'),
 ('Russian lamp mist', 'Фара запотевает изнутри после дождя.', {'part':'lamp'}, ['K028'], 'candidates_found'),
 ('Unrelated licensing question', 'How do I renew my driving licence?', {'part':'body'}, [], 'no_evidence'),
 ('Unrelated nonsense', 'quantum banana spaceship', {'part':'body'}, [], 'no_evidence'),
 ('Crack with no component', 'crack', {}, [], 'needs_context'),
 ('Cobalt key-on photo only', 'oil pressure warning', {'part':'dashboard','vehicle':'Cobalt','confirmed_manual':'S11','context':{'engine_running':False}}, [], 'needs_context'),
 ('Lacetti parking-brake context missing', 'brake warning', {'part':'dashboard','vehicle':'Lacetti','confirmed_manual':'S14','context':{'engine_running':True}}, [], 'needs_context'),
 ('Gentra is not Lacetti', 'brake warning', {'part':'dashboard','vehicle':'Gentra','confirmed_manual':'S14','context':{'engine_running':True,'parking_brake_released':True}}, [], 'no_evidence'),
 ('Unknown BYD propulsion', 'battery crash', {'part':'ev','vehicle':'BYD Song'}, [], 'needs_context')]

def main():
    results=[]
    with VectorKB() as kb:
        manifest=kb.check_index()
        for title,query,args,expected,status in CASES:
            keyword=retrieve.retrieve(query,**args)
            modes={}
            for mode in ['semantic','hybrid']:
                result=kb.query(query,mode=mode,**args)
                ids=[r['id'] for r in result['evidence']]
                matched=(result['status']==status and (bool(set(expected)&set(ids)) if expected else not ids))
                modes[mode]={'status':result['status'],'ids':ids,'expected_candidate_in_top3':matched,
                             'seconds':result.get('query_seconds'),'scores':result['candidate_scores'],
                             'questions':result['questions']}
            item={'title':title,'query':query,'context':args,'expected':expected,'expected_status':status,
                  'keyword_ids':[r['id'] for r in keyword['evidence']],'keyword_status':keyword['status'],**modes}
            results.append(item)
            print(json.dumps({'case':title,'semantic':modes['semantic']['ids'],'hybrid':modes['hybrid']['ids'],
                              'status':modes['hybrid']['status'],'development_check':modes['hybrid']['expected_candidate_in_top3']},ensure_ascii=True))
        repeat=kb.ingest()
        packages={}
        from importlib.metadata import version
        for name in ['qdrant-client','sentence-transformers','transformers','huggingface-hub','numpy','torch','scipy','scikit-learn','tokenizers']:
            packages[name]=version(name)
        data={'manifest':manifest,'repeat_ingest':repeat,'cases':results,'packages':packages}
        (kb.root/'development-probes.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Vector retrieval development results — 11 October 2026','',
           'These are 20 hand-authored development queries against the same 28 known KB records. They are not held-out cases, mechanic-reviewed diagnoses or an estimate of real-world accuracy. Expected IDs express a candidate we intended to retrieve; an ID appearing in the first three does not establish diagnosis or top-1 correctness. Uzbek/Russian wording needs native review.','',
           'The actual pinned multilingual E5 model and persistent local Qdrant store were used, on CPU. Synthetic-vector engineering tests are documented separately.','',
           '## Actual index','', '```json',json.dumps(manifest,indent=2),'```','',
           '## Development query comparison','',
           '| Case | Keyword candidates | Semantic candidates | Hybrid candidates | Hybrid status | Expected candidate/status check |',
           '|---|---|---|---|---|---|']
    for item in results:
        lines.append('| '+ ' | '.join([item['title'],', '.join(item['keyword_ids']) or 'None',
                     ', '.join(item['semantic']['ids']) or 'None',', '.join(item['hybrid']['ids']) or 'None',
                     item['hybrid']['status'],'Matched' if item['hybrid']['expected_candidate_in_top3'] else 'Needs review'])+' |')
    lines += ['', '## Repeat ingestion','', '```json',json.dumps(repeat,indent=2),'```','',
              '## Installed versions','', '```json',json.dumps(packages,indent=2),'```','',
              '## Full probe inputs and scores','',
              'Cosine and BM25/RRF scores are retrieval signals, not diagnostic probabilities. The default cosine gate is an initial heuristic, not a validated threshold. Hybrid retrieval may retain a candidate with lexical support even below that gate.','']
    for item in results:
        lines += ['### '+item['title'],'','```json',json.dumps(item,ensure_ascii=False,indent=2),'```','']
    lines += ['## Findings and limits', '',
              'The English misty-headlight paraphrase retrieved K028 through embeddings when the original title/search-term keyword baseline found no record. Different outward-bubble and inward-dip descriptions retrieved different leading semantic candidates. This demonstrates behaviour on these known records, not diagnostic accuracy.', '',
              'The Russian tyre-protrusion query was missed at the default threshold. The Uzbek tyre query and Russian lamp-mist query needed lexical support to include the expected candidate; semantic-only searches returned no candidate at that threshold. Lowering the threshold without separate evaluation can also accept unrelated queries.', '',
              'An initial rank-fusion probe produced exact ties whose record-ID fallback put cosmetic bumper damage above split/crack damage. Equal fused ranks now preserve semantic ordering before lexical ordering and stable IDs. This engineering rule fixes the arbitrary ID preference; it is not a trained or validated reranker.', '',
              'The depth-unknown paint query retains both scratch-depth records. Other candidate lists also include alternatives requiring follow-up rather than a single inferred repair recommendation. Native-language review, query rewriting and reranking should be tested on separate cases.', '',
              'No LLM rewriting, LLM answer generation, automotive training, mechanic review or held-out accuracy evaluation was run.', '']
    lines += ['## Reproduce','', '```powershell',
              r'D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/probe_vector.py','```','',
              'This overwrites this development report and its ignored runtime audit file. No LLM, cloud database, paid compute or automotive training is used.','']
    (retrieve.BASE/'VECTOR-RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':main()
