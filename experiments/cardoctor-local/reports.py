"""Case reports are Markdown and are written only by the local server on D:."""
def clean(text):return str(text).replace('\n',' ').replace('\r',' ').replace('|','\\|')
def markdown_report(r):
    out=['# CarDoctor local visual-reference assessment','',f"**Case:** {r['case_id']}",f"**Date:** {r['created']}",f"**Vehicle:** {clean(r['vehicle']) or 'Unknown'}",f"**Component:** {clean(r.get('part','')) or 'Unspecified'}",f"**Driver symptoms:** {clean(r['symptoms']) or 'Not supplied'}",'','## Status','',r['assessment'],'','This is an assisted reference-retrieval baseline using ImageNet-pretrained visual features. It is not a trained automotive damage detector or an automated diagnosis. Similarity scores are not probabilities.','',f"Selected region in original image pixels: {r['region_pixels'] or 'whole image'}",f"User-confirmed visible label: {clean(r['confirmed_label']) or 'none'}",'','## Capture checks','',f"Region dimensions: {r['quality']['width']} x {r['quality']['height']}",f"Edge variance: {r['quality']['edge_variance']}",f"Dark fraction: {r['quality']['dark_fraction']}; bright fraction: {r['quality']['bright_fraction']}",'',r['quality']['threshold_status']]
    out+=['- '+clean(s) for s in r['quality']['issues']] or ['No heuristic capture flags. This does not guarantee useful damage detail.']
    out+=['','## Retrieved reference examples','','| Label of reference | Cosine similarity | Vehicle/incident group | Source / rights |','| --- | --- | --- | --- |']
    out += [f"| {clean(m['label'])} | {m['similarity']} | {clean(m['group_id'])} | {clean(m['source'])} / {clean(m['rights'])} |" for m in r['matches']]
    if not r['matches']:out+=['','No eligible references found.']
    out+=['','## Retrieved source notes','']
    if not r['knowledge']:out+=['No relevant reviewed note was retrieved. No repair cause, urgency or price was inferred.']
    for n in r['knowledge']:out += ['### '+clean(n['title']),'',n['excerpt'],'',f"Source: {n['source_url']}",f"Vehicle applicability: {clean(n['vehicle']) or 'generic'}",'']
    if r.get('experimental_classifier'):
        head=r['experimental_classifier'];out+=['','## Experimental classifier','',head['status'],'']
        out += [f"- {clean(p['label'])}: {p['uncalibrated_score']} (uncalibrated model score)" for p in head['predictions']]
    out += ['','## Reproducibility','',f"Feature pipeline: {r['feature_version']}",f"Analysis time: {r['elapsed_ms']} ms (this request only)",f"Exact-image exclusions: {r['excluded_exact_images']}",f"Same-group exclusions: {r['excluded_same_group']}",'','No vehicle-damage accuracy or repair-cost metric has been measured.']
    return '\n'.join(out)+'\n'
