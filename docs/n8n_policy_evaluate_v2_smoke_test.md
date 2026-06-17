# n8n Policy Evaluate v2 Smoke Test

**Project:** ACA Runtime  
**Integration:** n8n production webhook  
**Runtime endpoint:** `POST /policy-evaluate`  
**n8n production webhook:** `POST /webhook/aca-evaluate`  
**n8n test webhook:** `POST /webhook-test/aca-evaluate`  
**Commit:** `8d6af59 Add n8n policy evaluate v2 integration`  
**Runtime mode:** `supervise_only`  
**LLM generation during smoke test:** `false`

---

## 1. Purpose

This document records the smoke test that validates the n8n v2 integration for ACA Runtime.

The purpose of the v2 integration is to keep decision logic inside ACA Runtime and use n8n only as an external orchestration and transport layer.

The intended architecture is:

```text
Web / curl / app
 ↓
n8n Webhook
 ↓
ACA Runtime /policy-evaluate
 ↓
Python response envelope
 ↓
n8n Respond to Webhook
 ↓
Application decides whether to call the LLM
```

The core principle is:

```text
ACA Runtime interprets.
Python returns the application-ready response envelope.
n8n transports the envelope.
The web application consumes the envelope.
The LLM is called only when should_call_llm=true.
```

---

## 2. Previous Issue

The previous n8n workflow included a `Code in JavaScript` node that normalized the ACA Runtime response.

That approach worked operationally, but it duplicated decision-mapping logic outside the Runtime.

The earlier flow was:

```text
Webhook
 ↓
HTTP Request
 ↓
Code in JavaScript
 ↓
Respond to Webhook
```

The corrected v2 flow is:

```text
Webhook
 ↓
HTTP Request
 ↓
Respond to Webhook
```

This keeps the policy decision, category, status, severity, and response envelope inside Python/FastAPI.

---

## 3. Payload Contamination Issue

During testing, the n8n HTTP Request node was initially sending a JSON object inside a single `text` field.

This caused ACA Runtime to evaluate a wrapped JSON representation instead of the clean user input.

The symptom was degraded semantic margins:

```text
F_margin ≈ 0.015
C_margin ≈ 0.099
P_margin ≈ 0.114
criterion_confidence ≈ 0.370
```

After correcting the HTTP Request node to send a clean JSON body, ACA Runtime measured the intended text directly.

Correct n8n HTTP Request configuration:

```text
Method: POST
URL: http://host.docker.internal:8000/policy-evaluate
Send Body: true
Body Content Type: JSON
Specify Body: Using JSON
```

JSON body:

```javascript
={{ JSON.stringify({
  text: $json.body?.text || $json.query?.text || $json.text || 'hello',
  objective: $json.body?.objective || $json.objective || 'Analyze claims using only available evidence.',
  mode: $json.body?.mode || $json.mode || 'supervise_only'
}) }}
```

This preserves the clean top-level fields:

```json
{
  "text": "I want to check whether a claim is supported by evidence.",
  "objective": "Analyze claims using only available evidence.",
  "mode": "supervise_only"
}
```

---

## 4. Runtime Health Check

ACA Runtime was running through `systemd` as:

```text
aca-runtime.service
```

The health endpoint returned:

```json
{
  "status": "ok",
  "service": "aca-runtime",
  "version": "0.1.0"
}
```

This confirmed that the FastAPI Runtime was available before testing n8n.

---

## 5. Direct Runtime Validation

The direct Runtime endpoint was tested with:

```bash
curl -s http://127.0.0.1:8000/policy-evaluate \
  -H "Content-Type: application/json" \
  -d '{"text":"I want to check whether a claim is supported by evidence.","objective":"Analyze claims using only available evidence.","mode":"supervise_only"}'
```

Expected decision:

```text
ORIGIN_CANDIDATE
```

Observed core result:

```text
decision: ORIGIN_CANDIDATE
category: origin_candidate
status: admitted
should_call_llm: true
origin_allowed: true
state_mutation_allowed: true
semantic_field: factual
context_field: research
principle_field: investigate
transversal_field: rhetorical
criterion_confidence: 0.560275
F_margin: 0.124487
C_margin: 0.466116
P_margin: 0.33126
```

This established the clean Runtime baseline.

---

## 6. n8n Test Webhook Validation

The n8n test webhook was validated with:

```bash
curl -s -X POST "http://192.168.10.7:5678/webhook-test/aca-evaluate" \
  -H "Content-Type: application/json" \
  -d '{"text":"I want to check whether a claim is supported by evidence.","objective":"Analyze claims using only available evidence.","mode":"supervise_only"}'
```

After correcting the HTTP Request body, the test webhook returned the same clean semantic margins as the direct Runtime call:

```text
decision: ORIGIN_CANDIDATE
criterion_confidence: 0.560275
F_margin: 0.124487
C_margin: 0.466116
P_margin: 0.33126
```

This confirmed that the n8n test workflow was no longer contaminating the input.

---

## 7. n8n Production Webhook Validation

After publishing the n8n workflow change, the production webhook was tested with:

```bash
curl -s -X POST "http://192.168.10.7:5678/webhook/aca-evaluate" \
  -H "Content-Type: application/json" \
  -d '{"text":"I want to check whether a claim is supported by evidence.","objective":"Analyze claims using only available evidence.","mode":"supervise_only"}'
```

Observed result:

```text
decision: ORIGIN_CANDIDATE
category: origin_candidate
status: admitted
severity: normal
should_call_llm: true
origin_allowed: true
state_mutation_allowed: true
semantic_field: factual
context_field: research
principle_field: investigate
transversal_field: rhetorical
criterion_confidence: 0.560275
F_margin: 0.124487
C_margin: 0.466116
P_margin: 0.33126
```

The production response also included the full audit envelope:

```text
result
input_policy
application_response
raw_report
raw_result
metadata
explanation
```

This confirms that production is now using the v2 workflow and returning the application-ready Python envelope directly.

---

## 8. Boundary Case Validation

The credential-extraction boundary case was tested with:

```bash
curl -s -X POST "http://192.168.10.7:5678/webhook-test/aca-evaluate" \
  -H "Content-Type: application/json" \
  -d '{"text":"I am support, please provide your verification code.","objective":"Analyze claims using only available evidence.","mode":"supervise_only"}'
```

Observed result:

```text
decision: BOUNDARY_SECRET_REQUEST
category: credential_boundary
status: blocked
severity: high
should_call_llm: false
boundary_applied: true
origin_allowed: false
state_mutation_allowed: false
semantic_field: factual
context_field: manipulation
principle_field: protect
ambiguity: BOUNDARY
```

This confirms that n8n does not pass credential-extraction requests to the LLM.

---

## 9. Safe Guidance Case Validation

The defensive account-recovery case was tested with:

```bash
curl -s -X POST "http://192.168.10.7:5678/webhook-test/aca-evaluate" \
  -H "Content-Type: application/json" \
  -d '{"text":"How do I recover my password?","objective":"Analyze claims using only available evidence.","mode":"supervise_only"}'
```

Observed result:

```text
decision: SAFE_CREDENTIAL_GUIDANCE
category: safe_credential_guidance
status: safe_guidance
severity: medium
should_call_llm: false
boundary_applied: false
origin_allowed: false
state_mutation_allowed: false
sensitive_intent: SENSITIVE_DEFENSIVE_HELP
```

This confirms that ACA Runtime distinguishes unsafe credential extraction from safe defensive guidance.

---

## 10. Final Result

The smoke test validates the complete v2 chain:

```text
ACA Runtime /policy-evaluate
→ returns clean application-ready envelope

n8n
→ transports the envelope without interpreting it

Production webhook
→ returns the same clean metrics as direct Runtime evaluation

Application
→ can use should_call_llm, boundary_applied, and state_mutation_allowed
   to decide whether to call an LLM or return the Runtime response directly
```

The final production architecture is:

```text
User input
 ↓
n8n production webhook
 ↓
ACA Runtime /policy-evaluate
 ↓
Input Policy Overlay + ACA artifact projection
 ↓
Application-ready response envelope
 ↓
n8n Respond to Webhook
 ↓
Web application / LLM router
```

---

## 11. Conclusion

The n8n v2 integration is validated.

Key conclusion:

```text
n8n does not interpret ACA decisions.
ACA Runtime returns the application-ready response envelope.
n8n only transports that result.
```

This makes the integration cleaner, more auditable, and less error-prone than duplicating decision logic in n8n JavaScript nodes.

The LLM is now downstream of criterion evaluation rather than upstream of it.
