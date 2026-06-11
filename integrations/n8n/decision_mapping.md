# ACA Runtime + n8n Decision Mapping v0.1

This document defines the first n8n decision mapping for ACA Runtime Integration Lab.

This initial workflow uses the existing public FastAPI endpoint:

```text
POST /evaluate
```

The purpose is to connect n8n to the current public ACA Runtime server without changing the published API surface.

## Endpoint

Request:

```json
{
  "text": "Evaluate whether this conclusion follows from the available evidence."
}
```

Response shape:

```json
{
  "report": {
    "runtime_status": "stable",
    "decision": "ALLOW",
    "semantic_field": "factual",
    "secondary_field": "foundational",
    "origin_cost": 0.3919,
    "field_margin": 0.0633,
    "ambiguity": "CLEAR",
    "criterion_confidence": 0.608,
    "trajectory_state": "moderate_variation"
  },
  "raw_result": {}
}
```

## n8n switch field

Use the decision field:

```text
{{$json.report.decision}}
```

After normalization, use:

```text
{{$json.route}}
```

## Decision mapping

| ACA Runtime decision | n8n route | Application behavior |
|---|---|---|
| `ALLOW` | `ALLOW` | Continue workflow; call LLM, tool, or API if needed. |
| `CLARIFY` | `CLARIFY` | Ask the user for clarification before continuing. |
| `FLAG_DRIFT` | `REVIEW` | Do not forward directly; review, bound, or escalate. |
| `AMBIGUOUS_DRIFT` | `REVIEW` | Hold or route to human/application review. |
| `UNKNOWN` | `REVIEW` | Safe fallback; do not continue automatically. |

## Operational rule

A non-admitted, unclear, or drift-prone input should not be forwarded to generation or execution without review.

For this initial n8n integration, `/evaluate` provides a criterion signal. n8n performs the application routing.

## Initial n8n flow

```text
Webhook
    ↓
Prepare ACA Payload
    ↓
POST /evaluate
    ↓
Normalize ACA Decision
    ↓
Respond / Route by decision
        ├── ALLOW
        ├── CLARIFY
        └── REVIEW
```

## Local URL notes

If n8n runs directly on Windows:

```text
http://127.0.0.1:8000/evaluate
```

If n8n runs inside Docker and ACA Runtime runs on the host:

```text
http://host.docker.internal:8000/evaluate
```

## Future endpoint

A later branch may introduce a dedicated middleware endpoint:

```text
POST /middleware/supervise
```

That endpoint should return the full application contract:

```text
admitted
action
should_call_llm
boundary_applied
application_response
trace_id
```

For now, this workflow intentionally uses the already published `/evaluate` endpoint to avoid breaking the public release.
