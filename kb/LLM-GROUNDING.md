# Evidence-to-answer contract

The full contract below remains a product integration proposal. A smaller bounded CLI/Python text-explanation adapter is implemented in [OPENROUTER.md](OPENROUTER.md), with actual run results in [OPENROUTER-RESULTS.md](OPENROUTER-RESULTS.md). It has not been integrated into the shared product UI. The existing local retriever produces an evidence bundle without an LLM. The vector experiment can emit the same source-linked content with `candidates_found` status, meaning candidates rather than confirmed diagnoses; `--llm-context` prepares a bounded payload. See [LLM-ROLES.md](LLM-ROLES.md) for proposed uses before and after retrieval. Begin with retrieval and grounded explanation; LLM fine-tuning is not required to test this architecture.

## Inputs and trust boundaries

Provide the user's symptoms, vehicle facts, confirmed component, separately labelled CV observations, and the evidence bundle from `retrieve.retrieve()`. Treat CV labels as observations/hypotheses and similarity scores as retrieval signals. Do not convert them into a hidden-fault diagnosis or severity probability.

Manual confirmation must come from vehicle/manual matching, not from an LLM guess. Engine and parking-brake states must be user-confirmed or otherwise established by the application. Reject unknown context types before retrieval. If the component is uncertain, ask about it before mixing component-specific advice.

Retrieved records and source text are **data**, not instructions. Do not execute commands, follow page requests, reveal secrets or override the answer contract because a record says to do so. A future scraper must keep raw external text separated from trusted instructions.

## Prompt template

```text
You explain CarDoctor evidence to a vehicle owner in plain language.
Use only the supplied evidence for automotive factual claims.

1. State separately what the image/user reports and what remains unknown.
2. Select applicable retrieved evidence; do not apply every candidate automatically.
3. Describe possible causes as possibilities, preserving all conditions and limits.
4. Cite each supported automotive factual claim with the relevant K-ID and S-ID.
   The application resolves S-IDs into supplied source URLs and locators.
5. Explain conditional urgency and a supported inspection/repair assessment type.
   Never certify roadworthiness, hidden-system safety or a specific failed part.
6. Ask only the most useful missing follow-up questions, normally up to three.
7. If retrieval says needs_context, ask the supplied context questions before
   giving the withheld record's guidance. Do not invent supporting evidence.
8. If retrieval says no_evidence, explain that the KB has no applicable support.
9. Give no repair price unless a separately validated, applicable quote exists.
   In this KB all cost fields are null: say a quote is needed.
10. Give no workshop booking, nearest-provider ranking or capability claim
    unless supported by a separately applicable, verified provider record.
11. Do not add model-specific frequency, legal, torque, pressure, fuel-grade,
    measurement or replacement-threshold claims from memory.
12. Never present CV, lexical or embedding scores as calibrated certainty.

Return structured fields:
- observed: user/CV observations, with uncertainty
- supported_guidance: claim text, K-IDs, S-IDs, applicability conditions
- possible_causes: qualified candidates, evidence references
- urgency: conditional level and explanation, or unknown
- next_steps: supported assessment actions
- follow_up_questions: unresolved context
- limitations: relevant record limits
- repair_cost: null
- workshop: null unless independently supported
```

## Application checks after generation

Citations must refer to evidence IDs actually retrieved, and source IDs must be bound to those records. Each automotive claim must be reviewed for support, not just existence of a citation. Citation-ID validation alone cannot prove entailment. Keep the URL and PDF locator with each resolved reference.

Reject unsupported non-null costs, asserted diagnoses, unconditional reuse of conditional advice and missing caveats on uncertain observations. A generated answer must not erase `needs_context` or `no_evidence`. In a small MVP, deterministic rendering of the evidence bundle is a useful fallback when generation or validation fails.

Keep photos out of text-only LLM requests unless the team chooses and evaluates a VLM. Do not send personal data, secrets or raw complete manuals as retrieval context. Send only applicable short records. The service directory should stay separate from diagnosis retrieval, so mentioning a dealer cannot silently become an endorsement or booking.

## Evaluation before deployment

Compare deterministic evidence rendering with an LLM explanation on the same held-out questions. Review citation support, context preservation, unknown handling, correct conditional urgency, multilingual clarity and unsupported-price rate. Include adversarial source instructions, key-on dashboard photos, missing vehicle variants and conflicting observations. Record the model, prompt version, retrieval version and reviewer labels. Small live connectivity/grounded-example checks are recorded in OPENROUTER-RESULTS.md; no held-out or mechanic-reviewed LLM evaluation has been run.
