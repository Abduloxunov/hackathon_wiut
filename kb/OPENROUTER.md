# OpenRouter text-RAG experiment

The local KB now has an explicit OpenRouter adapter using `google/gemini-2.5-flash-lite`. It follows the HTTP chat-completions endpoint from the user's cURL example. Python's standard library performs the request, so the OpenRouter SDK is not required. This is a CLI/Python experiment in `kb/`; the shared product UI has not been changed.

## Local configuration

The repository root `.env` is ignored by Git. The `.env.example` contains an empty key and may be shared. Put the actual key only in `.env`, or set `OPENROUTER_API_KEY` in the process environment. Process environment values take precedence over file values.

```dotenv
OPENROUTER_API_KEY=
OPENROUTER_MODEL=google/gemini-2.5-flash-lite
OPENROUTER_MAX_TOKENS=900
OPENROUTER_TIMEOUT_SECONDS=45
CARDOCTOR_DATASET_DIR=D:/hakathon_wiut/datasets/CarDD_release
```

The dataset setting records the download location only. The API adapter reads only the four `OPENROUTER_*` settings and does not open or upload CarDD. Its simple environment parser supports `KEY=value` and matching outer quotes. It does not execute expressions, interpolate variables, or export file contents.

Check configuration without printing the key:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/openrouter_client.py config
```

Run from `D:\hakathon_wiut\finals\mdb-vision-finals`. The adapter locates this folder's `.env` independently of the working directory. Use `--env D:\path\.env` to select another file.

## Explicit live tests

The following commands make billable requests only when a real key is configured. Importing the module, running offline unit tests, checking configuration, or retrieving records does not call OpenRouter. No automatic retries are performed.

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/openrouter_client.py smoke
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/openrouter_client.py answer 'There is a bubble on the side of my tyre' --part tire --output D:\hakathon_wiut\finals\mdb-vision-finals\kb\.runtime\answer.json
```

The connection smoke test allows 32 output tokens. Grounded answers default to 900 and reject settings outside 32-1500. Each call has a configurable 5-90 second HTTP timeout, default 45. There is no streaming, web search, paid tool invocation, model fallback, GPU job, audio/video input, photo upload, or dataset upload in this experiment. Normal compatible-provider routing remains enabled; `require_parameters: true` requires support for the requested schema parameters.

`--retriever keyword` selects the older lexical baseline. The default is the existing E5/Qdrant hybrid implementation. The first hybrid call loads the local embedding model; this startup is separate from the HTTP timeout. The adapter does not download models. Set up the vector runtime as described in [VECTOR-RAG.md](VECTOR-RAG.md) first.

Vehicle/manual/context arguments are identical to retrieval:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/openrouter_client.py answer 'oil pressure warning' --part dashboard --vehicle Cobalt --manual S11 --engine-running yes
```

Supply manual and running-state confirmations only when established by the application/user. An LLM guess is not confirmation. Missing context and absent applicable evidence return deterministic evidence/context reports without invoking the LLM.

## Data flow and answer contract

1. Retrieve up to three scoped KB candidates using component, vehicle, propulsion, confirmed manual, and engine/parking-brake context.
2. Build a bounded text context containing user reports, CV labels if supplied, complete applicable records, source references, conditions, and limits. Treat scores as retrieval signals rather than diagnostic confidence.
3. Send trusted system instructions separately from user/evidence data. No complete manuals, API keys, photos, contact records, or CarDD images are included.
4. Request JSON Schema output: up to four cited explanation/possible-cause/next-step claims, up to three follow-up questions, and null cost/diagnosis.
5. Validate response field types, lengths, null fields, retrieved K-IDs, retrieved S-IDs and each record's source binding. Resolve source URLs from the supplied catalog instead of accepting model-generated links.
6. Display reported observations directly from user/CV input, marked unverified; the model cannot generate an observations field. Return the exact retrieved conditions, scope and limitations alongside generated prose. Responses are marked `generated_unreviewed`; a citation check does not establish factual entailment or mechanic approval.
7. On API errors, truncation, invalid JSON or invalid citations, return `deterministic_fallback` and the original evidence report. Never silently rerun a charged request.

`OPENROUTER_MAX_TOKENS` bounds output, while serialized request bodies are limited to 48 KB. Response bodies are limited to 2 MB. The fixed HTTPS endpoint cannot be overridden through environment values. HTTP redirects are refused to prevent forwarding authentication to a different destination. Error output includes safe status/type information rather than request headers, credentials or remote response bodies. Runtime answer files contain automotive examples and source evidence, and are ignored by Git.

## Scope and unresolved evaluation

The API explains retrieved text. CV fine-tuning, image embeddings and text explanations remain separate modules. A VLM observation layer, symptom extraction and query rewriting remain future experiments described in [LLM-ROLES.md](LLM-ROLES.md). They are not automatically called by this adapter, and no LLM fine-tuning is required for this experiment.

Validation does not prove that every cited statement follows from a record, and cannot guarantee that a model preserves every condition inside its prose. The application therefore retains original conditions next to the generated answer. The system still needs reviewed held-out examples, contradictory observations, adversarial evidence, multilingual questions, missing-context cases and human judgments of citation support before a production reliability claim.

Offline verification:

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B -m unittest discover -s kb -p 'test_*.py'
```

The new tests mock the network. They check request limits, placeholder rejection, credential redaction, no redirects/retries, truncation handling, schema requests, citation binding, deterministic fallback, missing-context behavior, and preservation of original evidence conditions. They do not measure LLM factual reliability.

## Primary references checked on 2026-10-11

- [OpenRouter chat-completions API](https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion): endpoint and request format.
- [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs): JSON Schema and compatible-provider requirements.
- [Gemini 2.5 Flash Lite model page](https://openrouter.ai/google/gemini-2.5-flash-lite): exact model identifier. The public `/api/v1/models` metadata was also checked: `response_format` and `structured_outputs` were present among supported parameters. Provider support may change.

See [OPENROUTER-RESULTS.md](OPENROUTER-RESULTS.md) for the actual measured calls and [download audit](../docs/CARDD-DOWNLOAD-CHECK.md) for the separate dataset check.
