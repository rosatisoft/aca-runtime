# ACA Runtime v0.1 — Connecting Applications to the Criterion Engine

## 1. Purpose

ACA Runtime v0.1 provides a model-agnostic criterion supervision layer that can be connected to external applications, agents, APIs, dashboards, and LLM providers.

The goal is simple:

> Applications do not need to become criterion-aware.  
> They only need to call the ACA Runtime middleware or API.

ACA Runtime receives an input text and, optionally, an objective. It then evaluates whether the input can establish semantic origin, continue an accepted trajectory, require clarification, be rejected, or remain measurement-only.

This document explains how applications can connect to ACA Runtime as a reusable **criterion engine**.

---

## 2. Core idea

Most LLM applications place their criterion inside prompts. This makes criterion fragile, repeated, expensive, and difficult to audit.

ACA Runtime externalizes that responsibility.

Instead of asking every application to reconstruct criterion in prompt text, ACA Runtime exposes a reusable supervision layer:

```text
Application input
    ↓
ACA Runtime middleware or API
    ↓
Criterion supervision
    ↓
Operational decision
    ↓
Optional LLM generation
```

The application remains responsible for product behavior, user interface, and final action. ACA Runtime provides the criterion signal.

---

## 3. What is the criterion engine?

In ACA Runtime, the criterion engine is the operational layer that decides whether a semantic interaction is admissible before it is allowed to shape the accepted trajectory.

It is not a chatbot.

A chatbot answers.  
A criterion engine decides whether an answer should be allowed, delayed, clarified, bounded, rejected, or reviewed.

ACA Runtime v0.1 evaluates:

- whether an input can become semantic origin;
- whether an input can continue an accepted trajectory;
- whether an input is under-specified and requires clarification;
- whether an input is out-of-field or semantically unstable;
- whether an input triggers a predefined boundary;
- whether generation should be allowed;
- whether state should be mutated;
- whether the application should respond deterministically without calling an LLM.

---

## 4. Architecture

The v0.1 architecture separates measurement, runtime interpretation, application action, and optional LLM generation.

```text
External Application
        ↓
ACA Runtime API / Middleware
        ↓
Precondition Gate
        ↓
F-C-P / T Measurement
        ↓
Runtime State
        ↓
Application Decision
        ↓
Optional LLM Generation
        ↓
Optional Post-Generation Review
```

This separation follows the project principle:

```text
The Atlas measures.
The Runtime interprets.
The Application decides.
The LLM generates.
```

The Streamlit demo is a visual test surface. The FastAPI server and Python middleware are the primary integration paths.

---

## 5. Integration option A: Python middleware

Use this option when your application is written in Python or can directly import Python modules.

```python
from aca_runtime.middleware import ACAMiddleware

middleware = ACAMiddleware(
    artifacts_root="C:/path/to/ACA/artifacts",
    mode="supervise_only"
)

result = middleware.handle(
    text="Evaluate whether the evidence supports the claim.",
    objective="Analyze claims using only available evidence."
)

print(result.to_dict())
```

Recommended for:

- local Python applications;
- internal scripts;
- notebooks;
- agent experiments;
- Streamlit demos;
- research workflows;
- controlled middleware testing.

The middleware supports three modes:

```text
measure_only
supervise_only
generate
```

### measure_only

Measures the input against ACA artifacts without mutating runtime state.

Use this mode for diagnostics, dashboards, and silent inspection.

### supervise_only

Runs the precondition gate and runtime state logic. It decides whether the input is admitted, rejected, clarified, or bounded.

Use this mode when an application wants ACA Runtime to decide whether the input may enter the accepted semantic trajectory.

### generate

Runs supervision first. If the input is admitted and a provider is configured, it may call an LLM and optionally review the generated output.

Use this mode for supervised generation experiments.

---

## 6. Integration option B: FastAPI server

Use this option when your application is not Python-native or when you want ACA Runtime to run as a local service.

Start the server:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"
python -m uvicorn aca_runtime.server.app:app --reload
```

Health check:

```http
GET http://127.0.0.1:8000/health
```

Example evaluation request:

```http
POST http://127.0.0.1:8000/evaluate
```

Body:

```json
{
  "text": "Evaluate whether the evidence supports the claim."
}
```

Recommended for:

- n8n workflows;
- Node.js services;
- Odoo or ERP integrations;
- web frontends;
- dashboards;
- enterprise backends;
- agent orchestration layers;
- mobile applications;
- services that should not import Python directly.

The API path is the most important route for connecting ACA Runtime to real systems.

---

## 7. Integration option C: Streamlit visual demo

Use this option to show and test ACA Runtime visually.

```powershell
$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"
python -m streamlit run apps\streamlit_middleware_demo.py
```

The Streamlit demo displays:

- user input;
- middleware mode;
- accepted or rejected state;
- action;
- F-C-P / T orientation;
- application response;
- runtime state;
- accepted trajectory;
- rejected inputs;
- raw middleware response.

Streamlit is not the middleware. It is a public-facing demo and test surface.

---

## 8. Application decision contract

ACA Runtime returns a structured response that applications can use to decide what to do next.

```json
{
  "mode": "supervise_only",
  "input_text": "Evaluate whether the evidence supports the claim.",
  "objective": "Analyze claims using only available evidence.",
  "admitted": true,
  "action": "CREATE_ORIGIN",
  "final_response": "Input accepted as semantic origin. A new accepted trajectory has been established.",
  "llm_called": false,
  "should_call_llm": true,
  "boundary_applied": false,
  "runtime_result": {},
  "measurements": null,
  "application_response": {},
  "llm_response": null,
  "post_generation_review": null,
  "metadata": {}
}
```

Recommended interpretation:

```text
admitted = true
    The input may establish origin or continue the accepted trajectory.

admitted = false
    The input must not mutate accepted semantic state.

should_call_llm = true
    The application may call a model if generation is part of the workflow.

should_call_llm = false
    The application should not call a model for this input.

boundary_applied = true
    The application should return the deterministic boundary message.

action = ASK_CLARIFICATION
    The application should request clarification before continuing.

action = DO_NOT_EXPAND
    The application should avoid expanding the input.

action = BOUNDARY_OR_REJECT
    The application should reject or bound the request.

action = CREATE_ORIGIN
    The input becomes the accepted semantic origin.

action = UPDATE_TRAJECTORY
    The input becomes part of the accepted semantic trajectory.
```

---

## 9. Example integration flows

### Chat application

```text
User message
    ↓
ACA Runtime middleware
    ↓
If admitted and should_call_llm:
        call LLM
Else:
        return deterministic ACA Runtime response
```

### n8n workflow

```text
Webhook input
    ↓
HTTP POST to ACA Runtime /evaluate or /criterion-route
    ↓
Switch node on action
    ↓
Allow, clarify, reject, or route to LLM
```

### Enterprise dashboard

```text
Incoming text or ticket
    ↓
ACA Runtime API
    ↓
Store criterion signal
    ↓
Show status: accepted, rejected, ambiguous, drift-prone
```

### Local agent

```text
Agent proposed step
    ↓
ACA Runtime middleware
    ↓
If admitted:
        execute or generate
Else:
        replan or ask for clarification
```

### Supervised LLM generation

```text
Input
    ↓
ACA Runtime precondition gate
    ↓
If admitted:
        condition generation
        call LLM
        review output
Else:
        return deterministic boundary or clarification
```

---

## 10. Recommended use cases

ACA Runtime v0.1 is useful for:

- preventing invalid semantic origin formation;
- preserving declared objectives across interaction;
- preventing rejected or out-of-field inputs from contaminating state;
- routing ambiguous inputs to clarification;
- supervising long-running conversations;
- adding a criterion layer before LLM generation;
- giving applications a reusable decision contract;
- testing semantic drift and trajectory preservation;
- building explainable moderation and supervision prototypes.

---

## 11. What not to do

Do not treat Streamlit as the runtime architecture. Streamlit is only a visual interface for demonstration and testing.

Do not embed the entire criterion repeatedly inside application prompts. The purpose of ACA Runtime is to externalize criterion supervision into reusable runtime logic.

Do not allow rejected inputs to mutate accepted state. The v0.1 invariant is:

```text
A non-admitted input must never alter semantic origin
or accepted trajectory.
```

Do not treat ACA Runtime as a universal truth verifier. ACA Runtime provides geometric and operational signals. Applications still need policy, domain knowledge, and human judgment where appropriate.

---

## 12. Current limitations

ACA Runtime v0.1 is an early operational layer.

Current limitations include:

- local artifact path configuration is still manual;
- the embedding layer depends on configured embedding access unless replaced locally;
- generation mode depends on optional provider configuration;
- thresholds and policies are still experimental;
- long-horizon objective persistence requires further development;
- multi-agent shared criterion coordination remains future work;
- the Streamlit demo is for visualization, not deployment.

---

## 13. Roadmap

Near-term work:

```text
1. Stabilize middleware contract.
2. Add dedicated FastAPI middleware endpoints.
3. Improve installation documentation.
4. Add integration examples for n8n and external apps.
5. Add optional Ollama supervised generation demo.
6. Add trace logging for accepted, rejected, clarified, and reviewed events.
7. Prepare GitHub release v0.1.0.
8. Archive release on Zenodo.
```

Future work:

```text
1. Criterion trace learning.
2. Objective vector persistence.
3. Multi-agent shared coordination layer.
4. Overlapping semantic field stress tests.
5. Provider adapters for local and hosted LLMs.
6. Deployment recipes.
```

---

## 14. Summary

ACA Runtime v0.1 turns criterion supervision into an external service layer.

Applications can connect through Python middleware, HTTP API, or a visual Streamlit demo. The application sends an input and optional objective; ACA Runtime returns a structured decision about admissibility, state mutation, boundary behavior, and generation permission.

The result is a reusable criterion engine that can be connected to many applications without embedding the full criterion repeatedly into prompts.
