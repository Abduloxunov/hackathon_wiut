# Local vector retrieval for CarDoctor

We now have a working local vector-database experiment: the existing 28 canonical knowledge records are embedded and stored in Qdrant on D:. Retrieval supports semantic search and BM25/vector hybrid search. This implements ingestion and retrieval, not a trained damage detector, an LLM conversation or a deployed product integration.

## Selected components

| Component | Choice | Why and limits |
|---|---|---|
| Vector database | Qdrant local mode, Python client 1.19.1 | Persistent D: files, explicit payload/ID filters, no server or cloud account needed for this small experiment |
| Text embeddings | `intfloat/multilingual-e5-small` | 384 dimensions; supports multilingual retrieval, but Uzbek/Russian automotive quality needs testing |
| Model revision | `614241f622f53c4eeff9890bdc4f31cfecc418b3` | Pinned public snapshot; loaded from local files with remote code disabled |
| Inference | CPU, Sentence Transformers 6.1.0 | No GPU rental, HF Job or paid inference |
| Keyword channel | BM25 over titles, search terms and source summaries | Helps exact terms; generic component words are removed from matching terms |
| Fusion | Reciprocal Rank Fusion | Combines ranks rather than adding incompatible BM25/cosine scores |
| Scope checks | Shared deterministic KB policy | Component, exact model, manual confirmation, powertrain, engine state and parking-brake context |
| LLM preparation | `--llm-context` output | Produces evidence JSON; no LLM request is sent |

Primary references: [Qdrant local mode and licence](https://github.com/qdrant/qdrant-client), [Qdrant filtering](https://qdrant.tech/documentation/search/filtering/), [E5 model card at the pinned revision](https://huggingface.co/intfloat/multilingual-e5-small/blob/614241f622f53c4eeff9890bdc4f31cfecc418b3/README.md), [hybrid search and rank fusion](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview).

Qdrant's client uses Apache-2.0; this E5 model is published with an MIT licence. The model card specifies `query: ` and `passage: ` prefixes, normalised embeddings and a 512-token input limit. It also cautions that low-resource language quality can be weaker. Those are model capabilities, not measured CarDoctor accuracy.

## What is ingested

Each K-record is one coherent passage containing its title, component, search terms, source summary, possible causes, conditions, repair assessment, actions, questions and limits. A source URL is retained in the evidence metadata rather than used as semantic content. Complete webpages, full manuals, photos and provider images are not ingested.

The vector point carries its canonical record ID, component, scope, source references, full structured record, content fingerprint and embedding-model identity. Point IDs are stable UUIDs derived from K-IDs. Source facts returned to the caller come from the checked canonical Markdown loaded by the store; the database cannot silently substitute arbitrary payload prose.

The initial real ingestion stored **28 points**, each with **384 dimensions**. The longest passage used **269 tokens**, so no passage was silently truncated. The pinned model files downloaded to D: total **493,292,828 bytes**, about **470.4 MiB**; this excludes installed Python libraries and other cache/runtime files. This is pretrained embedding inference, not training.

## Storage and download boundary

All mutable state is under `D:\hakathon_wiut\finals\mdb-vision-finals\kb\.runtime`, which is Git-ignored. This includes Qdrant storage, the model snapshot, model/index markers, test artifacts and query audit data. Package installation used the existing D: virtual environment and D: pip/temp caches.

`setup_vector.py` is the explicit model-download step. Querying and ingestion load the cached model with `local_files_only=True`, offline flags and `trust_remote_code=False`. They fail if setup is missing instead of downloading at query time. A runtime outside D: or a model path outside its selected runtime is rejected.

## Run the already prepared index

From the repository root in PowerShell:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py status
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py query 'There is a bubble on the side of my tyre' --part tire
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py query 'The headlight looks misty inside' --part lamp --mode semantic
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py query 'oil pressure warning' --part dashboard --vehicle Cobalt --manual S11 --engine-running yes
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py query 'crack' --part windshield --llm-context
```

`--manual S11` requires actual confirmation that the S11 edition applies to the vehicle's year and variant. It is not an instruction to infer this match from a model name. Do not set an engine state from a dashboard photo alone.

Default mode is `hybrid`. `--mode semantic` isolates the embedding channel for comparison. `--format json` shows scores and structured evidence. `--output D:\path\result.md` saves a Markdown report on D:; the parent directory must exist. `--llm-context` prints JSON intended for a future LLM adapter; no model is called.

For another environment, first install the pinned inference dependencies with package/cache/temp locations explicitly on D:, then run:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/setup_vector.py
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/vector_store.py ingest
```

The model is public and setup does not use the user's HF token. Downloading pretrained weights does not consume HF inference credits. A paid hosted LLM, if chosen later, has a separate budget and configuration.

## Editing and re-ingestion

Keep editing the Markdown records and source register. Then run `vector_store.py ingest`. Stable point IDs update existing records, and removed records are removed from this dedicated collection. A content/model fingerprint binds the collection to the current canonical KB. Missing, incomplete or stale markers cause retrieval to fail with a re-ingestion instruction.

An interrupted ingestion invalidates its marker before database mutation, preventing the partially updated index from being treated as ready. Qdrant local mode also locks its store: use one process/owner at a time. This CLI experiment is not a multi-worker production database. A product server can keep one `VectorKB` object open to reuse the loaded embedding model, then later move to Qdrant server mode as needed. Standalone CLI queries load the model each time; the development report separates cold startup from reused-model timing.

## How retrieval works

1. Validate typed query/context using the existing KB request contract.
2. Require a component and an actual symptom/observed label.
3. Exclude records with known incompatible vehicle or powertrain context.
4. Separate applicable records from records needing missing-context questions.
5. Search each permitted set with component/point-ID filters in Qdrant. Withheld records may inform a context question, but their factual guidance is not returned as evidence.
6. Run BM25; in hybrid mode, combine eligible dense/lexical candidates with rank fusion.
7. If the strongest candidate lacks required context, ask that question rather than substitute another warning's guidance.
8. Return source-linked candidates, or `needs_context` / `no_evidence`.

The status `candidates_found` means relevant-looking guidance was found; it is not a diagnosis, proof of applicability or a roadworthiness decision. The source record's conditions still determine how it can be used.

## Unknowns and score limits

A vector search always has nearest neighbours. This experiment uses an initial cosine gate of **0.80** for semantic results. Hybrid search can retain a lower-scoring candidate with keyword/observed-label support. This is a development heuristic, not a calibrated probability or automotive relevance threshold; it can miss paraphrases or retain irrelevant matches. `--min-cosine` is exposed for experiments, and any change should be evaluated on separate data.

Negation, subtle conflicts, unsupported symptoms, language variation and similar warning records need further testing. Candidate selection does not prove a cause or urgency. An LLM must preserve uncertainty and may need another question. Do not use a nearest match as an automatic replacement or safety verdict.

## Product integration proposal

The existing local visual demo still uses its earlier keyword-note retrieval. This vector collection is available through the CLI/Python API, but shared `src/` / `web/` code was not changed. Product integration belongs to T10.

A product adapter can call `VectorKB.query()` with confirmed facts and pass `llm_context(bundle)` to the chosen LLM using [LLM-GROUNDING.md](LLM-GROUNDING.md). The LLM can also assist before retrieval with faithful symptom extraction or query rewriting, and after retrieval with follow-ups. These roles are considered in [LLM-ROLES.md](LLM-ROLES.md); none has been silently deployed here.

Image embeddings belong in a separate reference collection with a separately selected model and data rights. Text and image vectors must not be mixed simply because dimensions match. Workshop metadata/location/quotes also need a separate verified search path.

## Validation

The 24 existing KB engineering tests and 23 new synthetic-vector tests pass against Qdrant local mode. Synthetic vectors verify database behaviour and isolation, not semantic relevance. Real-model development outcomes, including failures, are in [VECTOR-RESULTS.md](VECTOR-RESULTS.md). One Russian tyre query was missed at the default threshold. Initial hybrid rank ties preferred arbitrary record IDs; ties now preserve semantic ordering. This is a development rule, not a validated reranker. Multilingual preprocessing and ranking remain development work.

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B -m unittest discover -s kb -p 'test_*.py' -v
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/probe_vector.py
```

The probe report compares keyword, semantic and hybrid results on 20 hand-authored known-KB queries. It is not a held-out accuracy measurement, CV metric or LLM evaluation. Mechanic review, native-language review and real grouped test cases remain necessary.

## Optional text explanation after retrieval

The separately invoked [OpenRouter adapter](OPENROUTER.md) can now explain the scoped vector evidence using Gemini 2.5 Flash Lite. Vector ingestion/query commands themselves remain offline. [Live checks](OPENROUTER-RESULTS.md) record the bounded calls and limitations; this is not shared product integration.
