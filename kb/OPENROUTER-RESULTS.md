# OpenRouter measured checks

Run locally on 2026-10-11 using the human-supplied key in the ignored `.env`. The key is not recorded here. These were three explicitly bounded text requests, not an LLM benchmark. No photos, CarDD files or complete manuals were uploaded.

## Actual API usage

| Call | Result | Input tokens | Output tokens | Reported cost (USD) |
|---|---|---:|---:|---:|
| Connection test | connection_ok | 8 | 4 | 0.0000024 |
| Initial grounded example | generated_unreviewed | 1651 | 371 | 0.0003135 |
| Corrected grounded example | generated_unreviewed | 1659 | 316 | 0.0002923 |

Total OpenRouter-reported cost: **$0.0006082 USD**. This is the actual usage returned for these calls, not a forecast or an independently reconciled account bill. The model was `google/gemini-2.5-flash-lite`.

## Live finding and correction

The initial response had valid K/S citation IDs and null diagnosis/cost, but its generated observations field included an uncited interpretation of the tyre report. This exposed a boundary weakness that structural/citation checks alone could not detect. The schema was revised: the model generates cited claims and follow-up questions only; the application now displays the exact user/CV report separately and marks it unverified. A regression test rejects model-generated observations. The corrected request succeeded without a schema or citation fallback.

## Corrected example

User report: “There is a bubble on the side of my tyre”. Confirmed retrieval component: `tire`. No image or CV detection was supplied. The hybrid retrieval supplied K012 (outward bulge), K013 (inward indentation) and K014 (sidewall cracking), all bound to S01.

Generated claims (unreviewed):

- An outward bulge on the tyre sidewall can indicate internal structural damage and may require immediate replacement. Do not continue normal driving with a confirmed bulging tyre. [K012 / S01]
- An inward indentation on the tyre sidewall might be a normal manufacturing feature related to cord overlap. If uncertain, have a tyre professional assess it. [K013 / S01]
- Cracking on the tyre sidewall can range from shallow, age-related surface cracks to deeper or more widespread cracking that necessitates replacement. Have the depth and distribution of any cracks assessed professionally. [K014 / S01]

Generated follow-up questions:

- Does the bubble protrude outward or is it an inward indentation?
- Are there any signs of cracking on the tyre sidewall?
- Have you noticed any pressure loss from the tyre?

The application retained exact original urgency conditions, manual/context scope and limitations alongside this output, and returned `repair_cost: null` and `diagnosis: null`. See [sources](sources.md) for the primary reference and [knowledge](knowledge.md) for the original conditional records.

## What this verifies and what remains unmeasured

These calls verify that the local configuration authenticates, the selected provider accepts the JSON Schema request, the existing vector pipeline can supply evidence, and the response passes local citation/type/null checks. They do not establish factual reliability, CV accuracy, medical/mechanic review, safety or production latency.

The corrected output also volunteered conditional cracking guidance although the user reported only a bubble. This illustrates a remaining candidate-selection/relevance issue: all supplied records should not automatically become advice. Human review, stronger relevance selection and held-out questions remain necessary. Similarity scores and valid citation IDs do not prove a claim is applicable to a particular vehicle/photo. No LLM query-rewriting or VLM observation experiment was run.

## Engineering checks

- 62 KB tests passed: 47 existing retrieval/vector tests plus 15 mocked OpenRouter boundary/regression tests. These run without real keys or API calls.
- 12 existing Colab dataset/training-preparation tests passed.
- CarDD read-only audit checked all 4,000 image files and 8,740 object annotations; zero detected structural/image.verify issues and zero SHA-256-identical files across official splits. See [full dataset audit](../docs/CARDD-DOWNLOAD-CHECK.md).
- `.env` was verified ignored by Git. Runtime logs stay in ignored `kb/.runtime/`.
.env.example contains an empty key only. No commit, push, GPU job or shared product integration was performed.

## Reproduce

Commands, configuration and request limits are in [OPENROUTER.md](OPENROUTER.md). Repeating `smoke` or `answer` with a real key makes another billable request. The saved runtime JSON files are local execution records, not test fixtures or production canned answers.
