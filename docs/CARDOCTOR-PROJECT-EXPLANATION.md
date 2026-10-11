# CarDoctor: project explanation and technical stack

CarDoctor is a car-assessment assistant that combines computer vision, a sourced automotive knowledge base and a language model. A user uploads car photos, describes symptoms and provides relevant vehicle details. The product is designed to identify supported visible damage and explain what the available evidence suggests, what remains uncertain and which follow-up information or inspection is needed.

## The problem we are solving

Seeing damage and understanding it are different tasks. A person may notice a scratch, crack, broken lamp or flat tyre but still need answers to practical questions: What is visible? Which component is involved? What information helps assess the situation? What guidance applies to this vehicle? What should be inspected next?

A label such as “crack” does not answer all of those questions. CarDoctor connects visual findings and user-reported symptoms to traceable automotive guidance, then turns that evidence into an understandable report. The intended use cases are used-car checks, fleet triage and initial assistance after a breakdown or accident.

The initial vision scope is six exterior-damage categories: dent, scratch, crack, shattered glass, broken lamp and flat tyre. Symptom and dashboard guidance relies on applicable knowledge and explicit vehicle/context information; those conditions are not automatically established by an exterior-damage detector. The assessment should clearly express uncertainty and avoid asserting hidden mechanical faults, exact prices or overall roadworthiness from a photo.

## How the system works

1. **Collect inputs.** The user supplies an overview/close-up, symptoms, vehicle details and relevant context. Missing or unclear information becomes a follow-up question.
2. **Analyse visible damage.** A specialist CV model produces candidate damage classes, bounding boxes and model scores. These are visual observations for further assessment, not a complete mechanical diagnosis.
3. **Retrieve applicable knowledge.** Symptoms and confirmed visual findings are used to search source-linked records. Filters narrow results by component, vehicle/manual applicability and required context, such as engine state. The system can withhold guidance when its conditions are not established.
4. **Generate an explanation.** The LLM receives the user reports and retrieved evidence. It explains supported possibilities, conditional urgency, inspection/repair assessment types and useful questions, citing the supplied records and sources.
5. **Validate and display the report.** The application checks structured fields and citation bindings, preserves original conditions and limitations, and displays the findings and sources. If generation fails, it can display the evidence directly. Citation validation alone does not establish that every statement is supported; reviewed evaluation remains part of the design.

The core flow is:

**Photos + symptoms + vehicle context -> CV observations -> scoped knowledge retrieval -> grounded LLM explanation -> source-linked assessment.**

## Technical stack

| Layer | Technology / approach | Purpose |
|---|---|---|
| ML implementation | Python and PyTorch | Model training and inference |
| Specialist vision model | RF-DETR Nano | Fine-tuning target for locating and classifying supported visible damage |
| Vision training data | CarDD, COCO image/box annotations | Supervised examples for six car-damage classes |
| Training environment | Google Colab GPU | First small training run, followed by larger experiments after review |
| Text embeddings | `intfloat/multilingual-e5-small` | Represent symptoms and knowledge records as searchable vectors |
| Vector storage/search | Local Qdrant | Store record vectors and retrieve nearby candidates |
| Retrieval strategy | BM25 + vector search, fused with reciprocal-rank fusion; structured applicability filters | Combine direct term matching with semantic retrieval and preserve vehicle/component constraints |
| Language model | `google/gemini-2.5-flash-lite` through OpenRouter | Produce structured explanations from retrieved evidence |
| Knowledge storage | Source-linked Markdown records with structured fields | Keep guidance, conditions, limits and citations reviewable |
| Collaboration | Git and GitHub | Share code and documentation and review integration changes |

The shared application presents these components through a web interface. A specific frontend/backend framework is not assumed in this explanation. Visual reference retrieval can complement the detector with relevant example images; CLIP/DINOv2 are candidate image-embedding approaches, separate from the selected text-embedding model.

## What the user receives

The intended report contains visible findings and their locations, reported symptoms, relevant evidence and source links, qualified explanations, conditional urgency, supported inspection/repair assessment types, follow-up questions and limitations. Prices or workshop suggestions require separately verified and applicable provider/quote data.

For example, a user uploads a damaged-bumper photo and describes what happened. The visual stage identifies a candidate damaged region and label. Retrieval selects relevant bumper guidance. The explanation connects that evidence to the report, asks useful missing-context questions and links the sources. It does not turn the visual label into a confirmed hidden-system diagnosis.

## Why combine CV, retrieval and an LLM?

Each component serves a distinct purpose: the vision model locates supported visible damage, retrieval selects traceable domain evidence, and the LLM explains that evidence in plain language. This design lets us evaluate detection, retrieval and explanation separately and keep a factual source behind the report. We intend to fine-tune the vision model; LLM fine-tuning is not required for the initial RAG architecture.

CarDoctor's value is helping a user move from a visible finding and symptoms to an evidence-backed understanding and a sensible next assessment step.
