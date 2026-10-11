# KB engineering checks — 11 October 2026

## Observed results

| Check | Measured outcome | What it establishes |
|---|---|---|
| `test_retrieve.py` | 24 tests passed | Record validation, component isolation, model/manual guards, warning-state guards, EV variant guards, source binding, unknown handling and input/path validation |
| Source/record validator | 28 records, 20 sources, five contacts loaded | Markdown JSON fences parse and records have bound sources |
| Isolated prototype import | First run inserted 16 notes; second run inserted zero and updated 16 | Stable IDs prevent repeat-import duplication |
| Isolated database assertions | Exactly 16 notes; only body/windshield/tyre/lamp; no model-specific notes | Manual/high-voltage/context-dependent guidance is excluded from the old UI |
| Live prototype import | Before: three notes, zero references; after: 19 notes, zero references | 16 KB notes added; existing starter notes and photo count preserved |
| Local HTTP check | Health and library returned HTTP 200; library showed 19 notes, zero references | Running localhost app sees the imported library |
| Offline example queries | Six cases produced the outcomes below | Current deterministic examples behave as documented |

## Example outcomes

| Input | Result |
|---|---|
| `crack`, no component | `needs_context`; no evidence |
| `crack`, windscreen | K007 |
| `outward sidewall bulge`, tyre | K012 |
| Cobalt oil-pressure warning, confirmed S11, engine state missing | `needs_context`; no evidence |
| Same query with engine-running context true | K021 |
| `quantum banana spaceship`, body | `no_evidence` |

Full inputs and source-linked outputs are in [EXAMPLES.md](EXAMPLES.md). These are technical examples of retrieval, not completed diagnoses.

## Scope of the checks

The tests exercise specific failure modes rather than automotive diagnostic accuracy. A brake-warning query must not retrieve charging advice merely because both share the word “warning”. Different components cannot leak into one another. Manual-specific records cannot be used on another model, an unconfirmed manual or an incompatible engine state. Gentra is not silently treated as Lacetti; Cobalt MCM is not silently treated as the older Cobalt manual. General EV guidance requires a known electrified powertrain.

Engineering tests **do not establish** retrieval top-1/top-3 accuracy, repairability, severity calibration, diagnosis accuracy, mechanic approval, multilingual quality, price accuracy or workshop quality. No real labelled photo/question benchmark or paid LLM evaluation was run. The running prototype still reports that its damage detector is untrained and has no real reference images.

## Reproduce

From the repository root in PowerShell:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B -m unittest discover -s kb -p test_retrieve.py -v
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/retrieve.py --validate
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/import_local.py --runtime D:\hakathon_wiut\finals\mdb-vision-finals\experiments\cardoctor-local\.runtime\kb-import-check
```

The importer needs the existing local experiment's packages; the retriever and its tests use the standard library only. Tests and runtime storage stay on D:. No downloads, GPU training, cloud upload, paid requests, shop contacts or Git pushes were performed.

## Evaluation still needed

Have an automotive reviewer label applicable records, urgency conditions, supported actions and unknown outcomes for held-out real questions. Include component confusion, key-on dashboard lights, conflicting symptoms, incomplete model/year/variant information and cases absent from this KB. Keep these evaluation cases separate from search-term development. Then measure relevance, unsupported claims, citation support, unknown handling and latency, with dataset size and method recorded. Coordinate photo/retrieval measurements with the owner of T14 rather than presenting these engineering checks as T14 accuracy results.

## Vector extension — same day

The new vector extension has **47 passing engineering tests** in total: the original 24 plus 23 synthetic-vector tests against real Qdrant local storage. Synthetic vectors exercise scope filtering, stable IDs, stale/incompatible marker handling, unknown-neighbour rejection and LLM-context preparation. They do not measure embedding relevance.

Real CPU inference ingested 28 vectors at 384 dimensions with no truncation (maximum 269 passage tokens). A second real ingestion inserted zero new points and updated 28. The [development probe report](VECTOR-RESULTS.md) compares keyword, semantic and hybrid results on 20 hand-authored known-KB queries and includes multilingual/ranking failures. This is not a held-out accuracy result.

The vector extension downloaded the pinned public embedding model and installed inference packages on D:. It did not call an LLM, use GPU compute, train a model, upload data, contact shops or push Git changes. The earlier “no downloads” statement above refers to the first KB-content/import step, before this explicitly requested vector extension. The old local demo still uses keyword notes; product integration was not changed.
