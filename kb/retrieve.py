"""Offline, component-scoped retrieval from canonical Markdown records.
No dependencies, network requests, LLM calls, downloads or GPU usage.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent
PARTS = {'body', 'windshield', 'side_window', 'tire', 'lamp', 'fluid', 'dashboard', 'engine', 'wiper', 'fuel', 'ev'}
PROPULSIONS = {'ev', 'phev', 'hev', 'ice'}
LABELS = {'dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat'}
STOP = {'a','an','the','is','it','my','car','vehicle','has','have','and','or','of','on','in','to','with','what','do','i','there','this','that','can','please','help'}

def blocks(path):
    """Only explicit JSON fences are data; surrounding prose is documentation."""
    content = Path(path).read_text(encoding='utf-8')
    return [json.loads(s) for s in re.findall(r'^```json\s*\n(.*?)\n```\s*$', content, re.M | re.S)]

def load(base=BASE):
    records = blocks(base / 'knowledge.md')
    sources_list = blocks(base / 'sources.md')
    sources = {s['id']: s for s in sources_list}
    if len(sources) != len(sources_list):
        raise ValueError('Duplicate source ID.')
    ids = set()
    for source in sources.values():
        url = urlparse(source['url'])
        if url.scheme not in {'http','https'} or not url.netloc:
            raise ValueError('Invalid source URL.')
    for r in records:
        if r['id'] in ids:
            raise ValueError('Duplicate knowledge ID.')
        ids.add(r['id'])
        if r['part'] not in PARTS or not set(r['vision_labels']) <= LABELS:
            raise ValueError('Unknown component or vision label.')
        if not r['source_refs'] or any(ref['source_id'] not in sources for ref in r['source_refs']):
            raise ValueError('Unbound source reference.')
        if r['review_status'] != 'source_checked' or not r['limits']:
            raise ValueError('Unchecked record or missing limits.')
        if r['cost_estimate'] is not None:
            raise ValueError('Quotes are not supported in this version.')
        scope = r['scope']
        if not set(scope['propulsion']) <= PROPULSIONS:
            raise ValueError('Unknown propulsion scope.')
        manual = scope['confirmed_manual_source']
        if scope['vehicle_models'] and (manual not in sources or not any(ref['source_id'] == manual for ref in r['source_refs'])):
            raise ValueError('Model-specific records require a bound manual.')
        if any(not isinstance(v, bool) for v in r['required_context'].values()):
            raise ValueError('Required context must be boolean.')
    providers = blocks(base / 'workshops.md')
    if len({p['id'] for p in providers}) != len(providers):
        raise ValueError('Duplicate provider ID.')
    for p in providers:
        if p['source_id'] not in sources or p['price_ranges'] is not None:
            raise ValueError('Provider has an unbound source or unsupported prices.')
    return records, sources, providers

def tokens(text):
    return [t for t in re.findall(r'[^\W_]+', text.casefold(), re.UNICODE) if t not in STOP]

def normalize_label(label):
    label = label.casefold().strip().replace('_', ' ').replace('-', ' ')
    return {'glassshatter':'glass shatter','lampbroken':'lamp broken','tireflat':'tire flat'}.get(label,label)

def score_records(records, query, vision_label):
    terms = set(tokens(query))
    scored = []
    for r in records:
        doc = Counter(tokens(r['title'] + ' ' + ' '.join(r['search_terms'])))
        overlap = terms & set(doc)
        score = sum((1 + math.log(doc[t])) for t in overlap)
        if vision_label and vision_label in r['vision_labels']:
            score += 2
        if score:
            scored.append((score, r))
    ranked = sorted(scored, key=lambda item: (-item[0], item[1]['id']))
    # Avoid answering a specific brake-warning query using only the shared word 'warning'.
    # This is a retrieval heuristic, not a validated relevance or confidence threshold.
    return [item for item in ranked if item[0] >= ranked[0][0] * 0.6] if ranked else []

def check_scope(record, *, vehicle='', propulsion='', confirmed_manual='', context=None):
    """Shared deterministic applicability gate for keyword and vector retrieval.
    Unknown facts produce questions; known incompatible scope produces no evidence.
    """
    context = context or {}
    scope = record['scope']
    models = [m.casefold() for m in scope['vehicle_models']]
    if models and vehicle.casefold().strip() not in models:
        return False, ['Which exact vehicle model, year and variant is this?'] if not vehicle else []
    if scope['propulsion'] and propulsion.casefold().strip() not in scope['propulsion']:
        return False, ['Is the vehicle EV, PHEV, HEV or combustion-only? Confirm the exact variant.'] if not propulsion else []
    if scope['confirmed_manual_source'] and confirmed_manual != scope['confirmed_manual_source']:
        return False, [f'Confirm that manual {scope["confirmed_manual_source"]} applies to this exact model/year/variant; matching the model name alone is insufficient.']
    unmet = [key for key, value in record['required_context'].items() if context.get(key) is not value]
    if unmet:
        messages = {'engine_running':'Is the warning still present with the engine running? A key-on lamp check alone does not establish a fault.',
                    'parking_brake_released':'Is the parking brake fully released and the warning still present?'}
        return False, [messages[key] for key in unmet]
    return True, []

def retrieve(query, *, part='', vehicle='', propulsion='', confirmed_manual='', context=None, vision_label='', limit=3, base=BASE):
    records, sources, _ = load(base)
    if not isinstance(query, str):
        raise ValueError('Query must be text.')
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 10:
        raise ValueError('Limit must be 1-10.')
    context = dict(context or {})
    if set(context) - {'engine_running','parking_brake_released'} or any(not isinstance(v, bool) for v in context.values()):
        raise ValueError('Use boolean engine_running / parking_brake_released context only.')
    part = part.casefold().strip()
    vehicle = vehicle.casefold().strip()
    propulsion = propulsion.casefold().strip()
    vision_label = normalize_label(vision_label)
    if part and part not in PARTS:
        raise ValueError('Unknown component.')
    if propulsion and propulsion not in PROPULSIONS:
        raise ValueError('Unknown propulsion.')
    if vision_label and vision_label not in LABELS:
        raise ValueError('Unknown vision label.')
    if confirmed_manual and confirmed_manual not in sources:
        raise ValueError('Unknown manual source ID.')
    result = {'status':'no_evidence','query':query,'part':part,'vehicle':vehicle,'propulsion':propulsion,
              'context':context,'vision_label':vision_label,'questions':[], 'evidence':[], 'sources':[],
              'cost_estimate':None, 'method':'Offline lexical candidate retrieval; scores are not probabilities.',
              'limitations':['Source summaries are not mechanic-reviewed diagnoses.',
                             'No trained CV inference or paid LLM request is performed by this tool.']}
    if not tokens(query) and not vision_label:
        return result
    if not part:
        result.update(status='needs_context', questions=['Which component is affected: body, windshield, side window, tyre, lamp, fluid, dashboard, engine, wiper, fuel or EV system?'])
        return result
    candidates = score_records([r for r in records if r['part'] == part], query, vision_label)
    evidence = []
    questions = []
    for score, r in candidates:
        allowed, needed = check_scope(r, vehicle=vehicle, propulsion=propulsion,
                                      confirmed_manual=confirmed_manual, context=context)
        if not allowed:
            questions.extend(needed)
            continue
        evidence.append({**r, 'retrieval_score':round(score,4)})
    result['evidence'] = evidence[:limit]
    result['questions'] = list(dict.fromkeys(questions))
    used = {ref['source_id'] for r in result['evidence'] for ref in r['source_refs']}
    result['sources'] = [sources[sid] for sid in sorted(used)]
    if result['evidence']:
        result['status'] = 'evidence_found'
    elif result['questions']:
        result['status'] = 'needs_context'
    return result

def as_markdown(bundle):
    lines = ['# CarDoctor retrieved evidence', '', f'Status: **{bundle["status"]}**', '',
             bundle['method'], '', 'This is an evidence bundle, not a generated diagnosis or a roadworthiness decision.', '']
    if bundle['questions']:
        lines += ['## Context needed', ''] + ['- ' + q for q in bundle['questions']] + ['']
    sources = {s['id']:s for s in bundle['sources']}
    for r in bundle['evidence']:
        ref = r['source_refs'][0]
        source = sources[ref['source_id']]
        lines += [f'## {r["id"]}: {r["title"]}', '', r['source_summary'] + f' [{source["title"]}]({source["url"]})', '',
                  'Applicability: ' + r['urgency']['condition'], '', 'Possible causes (unconfirmed): ' + '; '.join(r['possible_causes']), '',
                  'Repair assessment: ' + r['repair_type'], '', 'Next steps:', '']
        lines += ['- ' + a for a in r['actions']] + ['', 'Follow-up questions:', '']
        lines += ['- ' + q for q in r['follow_up_questions']] + ['', 'Limits:', '']
        lines += ['- ' + l for l in r['limits']] + ['', f'Source locator: {ref["locator"]}. Mechanic review: pending.', '']
    lines += ['Repair cost: unavailable; no verified quote in this knowledge base.', '']
    return '\n'.join(lines)

def d_output(value):
    path = Path(value).resolve()
    if path.drive.upper() != 'D:':
        raise ValueError('File output must be on D:.')
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--part', default='')
    parser.add_argument('--vehicle', default='')
    parser.add_argument('--propulsion', default='')
    parser.add_argument('--manual', default='')
    parser.add_argument('--vision-label', default='')
    parser.add_argument('--engine-running', choices=['yes','no'])
    parser.add_argument('--parking-brake-released', choices=['yes','no'])
    parser.add_argument('--format', choices=['json','md'], default='md')
    parser.add_argument('--output', type=d_output)
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--export', type=d_output, help='Optional JSON interoperability export on D:; Markdown remains canonical.')
    args = parser.parse_args()
    if args.validate or args.export:
        records, sources, providers = load()
        if args.export:
            args.export.write_text(json.dumps({'knowledge':records,'sources':list(sources.values()),'providers':providers}, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Validated {len(records)} records, {len(sources)} sources, {len(providers)} contacts.')
        return
    context = {}
    for key in ['engine_running','parking_brake_released']:
        value = getattr(args, key)
        if value is not None:
            context[key] = value == 'yes'
    bundle = retrieve(args.query, part=args.part, vehicle=args.vehicle, propulsion=args.propulsion,
                      confirmed_manual=args.manual, context=context, vision_label=args.vision_label)
    content = json.dumps(bundle, ensure_ascii=False, indent=2) if args.format == 'json' else as_markdown(bundle)
    if args.output:
        args.output.write_text(content, encoding='utf-8')
    else:
        print(content)

if __name__ == '__main__':
    main()
