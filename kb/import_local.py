"""Explicitly import generic supported-component records into the local prototype.
Manual-, powertrain- and runtime-dependent guidance stays in the scoped retriever.
Existing notes and photos are preserved. Re-running updates stable KB IDs.
"""
import argparse
import hashlib
import sys
import time
from pathlib import Path
import retrieve

def import_records(runtime=None):
    if runtime:
        import os
        path = Path(runtime).resolve()
        if path.drive.upper() != 'D:':
            raise ValueError('Runtime must be on D:.')
        os.environ['CARDOCTOR_RUNTIME'] = str(path)
    sys.path.insert(0, str(retrieve.BASE.parent / 'experiments' / 'cardoctor-local'))
    import core
    records, sources, _ = retrieve.load()
    eligible = [r for r in records if r['part'] in {'body','windshield','tire','lamp'}
                and not r['scope']['vehicle_models'] and not r['scope']['propulsion'] and not r['required_context']]
    core.initialize()
    inserted = updated = 0
    with core.connection() as db:
        for r in eligible:
            sid = r['source_refs'][0]['source_id']
            excerpt = ('Source-checked research summary, not mechanic-reviewed. ' + r['source_summary'] +
                       '\nApplicability: ' + r['urgency']['condition'] +
                       '\nPossible causes, unconfirmed: ' + '; '.join(r['possible_causes']) +
                       '\nSuggested assessment: ' + r['repair_type'] +
                       '\nNext steps: ' + '; '.join(r['actions']) +
                       '\nAsk: ' + '; '.join(r['follow_up_questions']) +
                       '\nLimits: ' + '; '.join(r['limits']) +
                       '\nNo verified price. Checked: ' + r['checked_at'])
            data = dict(title=r['id'] + ': ' + r['title'], excerpt=excerpt, source_url=sources[sid]['url'],
                        vehicle='', tags=' '.join(r['search_terms'] + r['vision_labels']), part=r['part'], reviewed=True)
            for key, limit in {'title':160,'excerpt':4000,'source_url':1000,'tags':400,'part':60}.items():
                if len(data[key]) > limit:
                    raise ValueError(f'{r["id"]} exceeds prototype {key} limit.')
            nid = hashlib.sha256(('cardoctor-kb-v1:' + r['id']).encode()).hexdigest()[:32]
            existing = db.execute('SELECT id FROM notes WHERE id=?', (nid,)).fetchone()
            values = (data['title'],data['excerpt'],data['source_url'],'',data['tags'],1,time.strftime('%Y-%m-%dT%H:%M:%S'),data['part'])
            if existing:
                db.execute('UPDATE notes SET title=?,excerpt=?,source_url=?,vehicle=?,tags=?,reviewed=?,created=?,part=? WHERE id=?', (*values,nid))
                updated += 1
            else:
                db.execute('INSERT INTO notes(id,title,excerpt,source_url,vehicle,tags,reviewed,created,part) VALUES(?,?,?,?,?,?,?,?,?)', (nid,*values))
                inserted += 1
    return {'eligible':len(eligible),'inserted':inserted,'updated':updated,'runtime':str(core.RUNTIME)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', help='Optional isolated D: runtime; default is the local prototype runtime.')
    args = parser.parse_args()
    print(import_records(args.runtime))
