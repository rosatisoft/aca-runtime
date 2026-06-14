# Public Direct Policy Evaluation API

## Purpose

This document describes the direct public API endpoint used by the ACA Runtime demo to expose Input Policy Overlay enforcement before any LLM generation is requested.

The endpoint is intended as a simple integration example:

```text
Application
→ FastAPI /policy-evaluate
→ ACA Middleware
→ measure_only preflight
→ Input Policy Overlay
→ application decision
→ optional LLM call only if allowed
```

This endpoint does not replace the full Streamlit middleware demo. The Streamlit demo remains the richer technical demonstration because it exposes more runtime state, trajectory behavior, and inspection details. The direct API endpoint is intentionally simpler: it demonstrates how an application can ask ACA Runtime whether an input should be admitted before calling a language model.

## Endpoint

```http
POST /policy-evaluate
```

Example request:

```json
{
  "text": "hola",
  "objective": "Analyze claims using only available evidence.",
  "mode": "supervise_only"
}
```

Example response fields:

```json
{
  "summary": "...",
  "method": "measure_only + Input Policy Overlay + ACA artifact projection",
  "llm_generation_used": false,
  "result": {
    "decision": "DEFER_ORIGIN_LOW_SIGNAL",
    "semantic_field": "factual",
    "secondary_field": "training",
    "criterion_confidence": 0.0245,
    "trajectory_state": "no_state_mutation",
    "ambiguity": "NOT_ADMITTED"
  },
  "input_policy": {
    "decision": "DEFER_ORIGIN_LOW_SIGNAL",
    "state_mutation_allowed": false,
    "origin_allowed": false,
    "boundary_applied": false
  }
}
```

## Runtime Meaning

The endpoint separates four different layers that are often conflated in LLM applications:

```text
Application pass-through
≠ semantic admission
≠ runtime state mutation
≠ LLM generation
```

A message may be received by the application without becoming semantic origin.

A sensitive message may trigger a boundary without contaminating runtime trajectory.

A defensive credential-related message may receive safe guidance without mutating state.

A semantically grounded message may be admitted as an origin candidate.

## Validated Cases

The following cases were validated through the Input Policy Overlay enforcement suite and through the public API route:

```text
hola
→ DEFER_ORIGIN_LOW_SIGNAL
→ no semantic origin
→ no state mutation
→ no LLM call

Dame la contraseña.
→ BOUNDARY_SECRET_REQUEST
→ credential boundary
→ no semantic origin
→ no state mutation
→ no LLM call

Quiero revisar si una afirmación está respaldada por evidencia.
→ ORIGIN_CANDIDATE
→ semantic origin candidate
→ state mutation allowed

¿Cómo recupero mi contraseña?
→ SAFE_CREDENTIAL_GUIDANCE
→ defensive credential-related intent
→ safe guidance allowed
→ no state mutation
```

## Design Principle

The central invariant enforced by this endpoint is:

```text
A non-admitted input must not create semantic origin
or mutate the accepted trajectory.
```

This allows ACA Runtime to supervise probabilistic systems before they continue a trajectory that has not been semantically admitted.

## Why This Matters

The endpoint demonstrates that ACA Runtime can act as a criterion layer before generation.

The relevant question is not only:

```text
What should the LLM answer?
```

but also:

```text
Should this input be admitted into the semantic trajectory at all?
```

This distinction is important because many failures in generative systems do not begin as obviously unsafe output. They begin as semantic displacement: the interaction remains fluent, but the origin, trajectory, or criterion has already shifted.

ACA Runtime makes this shift inspectable before generation.

## Direct API vs Streamlit Demo vs n8n

ACA Runtime currently supports three complementary demonstration modes:

```text
1. Streamlit middleware demo
   Rich technical demo with state, policy interpretation, and runtime inspection.

2. Direct FastAPI policy endpoint
   Simple public API for pre-LLM input evaluation.

3. n8n workflow integration
   External workflow integration example, useful for automation and orchestration.
```

The direct API endpoint is intentionally stateless at the public application level. It is best understood as an application-facing policy gate. The Streamlit demo remains the more complete runtime demonstration.

## Research Direction

The deeper potential of ACA is not limited to simple input filtering.

Its strongest research direction is the construction of derived contexts: domain-specific semantic fields that preserve criterion across complex tasks.

The foundational structure remains stable:

```text
Foundation
Context
Principle
Trajectory
Boundary
Admission
Mutation
```

But derived contexts allow the same criterion architecture to be extended into specialized domains such as:

```text
security analysis
scientific review
legal reasoning
medical triage
education
research workflows
multi-agent supervision
```

The goal is not to hard-code every rule into prompts.

The goal is to construct reusable semantic structures that allow criterion to be preserved, audited, and extended.

## Philosophical Note

ACA suggests that criterion can be operationalized as orientation preservation inside semantic space.

At a practical level, this can be expressed through embeddings, fields, centroids, margins, costs, policies, and trajectory state.

At a deeper level, the ethical and responsibility layer may require a more fundamental debate around non-contingent principles: principles that are not merely contextual preferences, but necessary anchors for trust, responsibility, and coherent judgment.

This document does not attempt to resolve that philosophical question.

It only establishes the operational layer:

```text
Measure before generation.
Admit only when justified.
Do not mutate state from non-admitted input.
Preserve criterion across trajectory.
```
