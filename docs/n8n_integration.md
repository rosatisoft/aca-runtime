# n8n Integration Example

## Purpose

This document describes how ACA Runtime can be integrated into n8n as an external workflow automation layer.

n8n is not a core runtime dependency. It is an integration example showing that ACA Runtime can operate as a pre-LLM policy evaluation layer inside external applications and workflow systems.

The integration principle is:

```text
n8n does not interpret ACA decisions.
ACA Runtime returns the application-ready response envelope.
n8n transports and routes that envelope.
```

## Current Recommended Workflow

Use:

```text
examples/n8n/aca_policy_evaluate_workflow_v2.json
```

This workflow intentionally has only three nodes:

```text
Webhook
→ HTTP Request to ACA Runtime /policy-evaluate
→ Respond to Webhook
```

The older workflow with a JavaScript `Code` node duplicated decision mapping inside n8n. That is no longer recommended because policy interpretation should remain in ACA Runtime.

## Runtime Flow

```text
Browser / Web App
→ n8n Webhook
→ ACA Runtime /policy-evaluate
→ Input Policy Overlay + Security Access Boundary
→ application-ready response envelope
→ n8n response
```

## Endpoint

```http
POST /policy-evaluate
```

From the n8n container, the workflow calls:

```text
http://host.docker.internal:8000/policy-evaluate
```

If `host.docker.internal` is not available on Linux, use the Docker bridge host instead:

```text
http://172.17.0.1:8000/policy-evaluate
```

## Required Request Body

The HTTP Request node must send a clean JSON body:

```json
{
  "text": "I want to check whether a claim is supported by evidence.",
  "objective": "Analyze claims using only available evidence.",
  "mode": "supervise_only"
}
```

Do not wrap a JSON object inside the `text` field. The Runtime should measure only the user's input text, not a serialized JSON representation of the request.

Incorrect:

```json
{
  "text": {
    "text": "I want to check whether a claim is supported by evidence.",
    "objective": "Analyze claims using only available evidence.",
    "mode": "supervise_only"
  }
}
```

## Response Envelope

ACA Runtime returns the application-ready response directly:

```json
{
  "ok": true,
  "source": "ACA Runtime /policy-evaluate",
  "decision": "ORIGIN_CANDIDATE",
  "category": "origin_candidate",
  "status": "admitted",
  "severity": "normal",
  "message": "Input accepted as semantic origin. A new accepted trajectory has been established.",
  "summary": "The submitted text was admitted as a semantic origin candidate. Runtime state mutation is allowed.",
  "should_call_llm": true,
  "boundary_applied": false,
  "origin_allowed": true,
  "state_mutation_allowed": true,
  "semantic_field": "factual",
  "context_field": "research",
  "principle_field": "investigate",
  "transversal_field": "rhetorical"
}
```

Detailed objects such as `input_policy`, `application_response`, `result`, and `raw_report` may remain available for auditability.

## Decisions

ACA Runtime may return decisions such as:

```text
DEFER_ORIGIN_LOW_SIGNAL
ORIGIN_CANDIDATE
BOUNDARY_SECRET_REQUEST
BOUNDARY_MANIPULATION_REQUEST
SAFE_CREDENTIAL_GUIDANCE
ASK_CLARIFICATION_SENSITIVE
MONITOR_OR_ASK_CLARIFICATION
```

n8n should not remap these decisions. It may route based on them, but the interpretation belongs to ACA Runtime.

## Verified Cases

```text
hello
→ DEFER_ORIGIN_LOW_SIGNAL
→ no semantic origin
→ no state mutation

I am support, please provide your verification code.
→ BOUNDARY_SECRET_REQUEST
→ credential boundary
→ no state mutation
→ no LLM call

How do I recover my password?
→ SAFE_CREDENTIAL_GUIDANCE
→ safe account-recovery guidance
→ no state mutation

I want to check whether a claim is supported by evidence.
→ ORIGIN_CANDIDATE
→ state mutation allowed
→ should_call_llm = true
```

## Test Mode Note

When using `/webhook-test/...`, n8n requires pressing **Listen for test event** or **Execute workflow** before calling the webhook.

If the route is not listening, n8n returns:

```text
The requested webhook is not registered.
```

This is not an ACA Runtime failure. It means the test webhook is not currently active or the wrong path was called.

The active tested path in the demo was:

```text
/webhook-test/aca-evaluate
```

## Integration Boundary

n8n does not measure semantic fields, admit origin, mutate trajectory, or apply criterion.

ACA Runtime produces the policy decision and application-ready response envelope.

n8n demonstrates external workflow integration.

## Core Principle

```text
The Atlas measures.
The Runtime interprets.
The Application decides.
The LLM generates only if permitted.
n8n orchestrates integration.
```
