# ACA Runtime v0.1.0 — Middleware Preview Release Notes

## Release status

**Version:** v0.1.0  
**Release type:** Middleware Preview  
**Project:** ACA Runtime  
**Repository:** `rosatisoft/aca-runtime`  
**Primary purpose:** Connect applications to a reusable criterion supervision engine.

ACA Runtime v0.1.0 is the first public middleware preview of the Axiomatic Criterion Atlas Runtime. It introduces an operational layer for connecting applications, APIs, agents, dashboards, and LLM workflows to an external criterion engine.

This release is not presented as a final stable system. It is a reproducible technical preview intended for testing, integration experiments, feedback, and early adoption by researchers and developers.

---

## 1. What this release introduces

ACA Runtime v0.1.0 introduces a model-agnostic supervision layer that evaluates whether an input may establish semantic origin, continue an accepted trajectory, require clarification, trigger a boundary, be rejected, or remain measurement-only.

The core idea is:

```text
Applications do not need to become criterion-aware.
They only need to call the ACA Runtime middleware or API.
```

Instead of embedding all reasoning constraints repeatedly into prompts, ACA Runtime externalizes criterion supervision into a reusable runtime layer.

---

## 2. Main contribution

The main contribution of this release is the separation between application logic, runtime criterion supervision, and optional LLM generation.

```text
Application input
    ↓
ACA Runtime middleware / API
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
```

The release establishes the first working version of ACA Runtime as a **criterion engine**.

A chatbot answers.  
A criterion engine decides whether an answer should be allowed, delayed, clarified, bounded, rejected, or reviewed.

---

## 3. Included components

### Runtime core

This release includes the Runtime v2 operational layer for:

- semantic origin creation;
- accepted trajectory preservation;
- rejected input isolation;
- precondition evaluation;
- application response generation;
- state snapshots;
- deterministic runtime decisions.

### Middleware layer

The new plug-and-play middleware layer exposes ACA Runtime through a simple Python interface.

Supported modes:

```text
measure_only
supervise_only
generate
```

The middleware returns a structured decision contract that applications can use to determine whether to continue, clarify, reject, call an LLM, or return a deterministic boundary response.

### FastAPI server

The repository includes a FastAPI service that can be launched with `uvicorn` and used by external systems through HTTP.

This is the preferred integration path for non-Python applications.

### Streamlit visual demo

The release includes a Streamlit application that visually demonstrates:

- accepted origin;
- accepted continuation;
- rejected predefined risk;
- out-of-field input;
- clarification request;
- measurement-only mode;
- accepted trajectory;
- rejected inputs;
- runtime state preservation.

Streamlit is not the middleware. It is a public-facing demonstration and manual testing surface.

### Documentation

This release includes documentation for:

- quickstart installation;
- middleware usage;
- API testing;
- Streamlit demo;
- application integration;
- NotebookLM video preparation;
- release checklist.

---

## 4. How applications can connect

ACA Runtime v0.1.0 supports three practical connection paths.

### 4.1 Python middleware

For Python-native applications:

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

- Python applications;
- notebooks;
- local agents;
- research workflows;
- internal scripts;
- Streamlit demos.

### 4.2 FastAPI / HTTP integration

For external systems:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\\path\\to\\ACA\\artifacts"
python -m uvicorn aca_runtime.server.app:app --reload
```

Health check:

```http
GET http://127.0.0.1:8000/health
```

Evaluation:

```http
POST http://127.0.0.1:8000/evaluate
```

Recommended for:

- n8n workflows;
- Node.js applications;
- web frontends;
- enterprise dashboards;
- orchestration systems;
- chat interfaces;
- agent controllers;
- backend services.

### 4.3 Streamlit demo

For visual testing:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\\path\\to\\ACA\\artifacts"
python -m streamlit run apps\\streamlit_middleware_demo.py
```

Recommended for:

- demos;
- video recording;
- public explanation;
- manual validation;
- showing how rejected inputs do not contaminate accepted trajectory.

---

## 5. Middleware decision contract

ACA Runtime returns structured output that can be consumed by applications.

Typical fields include:

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

Applications can interpret this contract as follows:

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

## 6. Validated demonstration cases

The current demo validates the following cases.

### Accepted origin

```text
Evaluate whether the evidence supports the claim.
```

Expected behavior:

```text
admitted = true
action = CREATE_ORIGIN
accepted trajectory length = 1
rejected inputs = 0
```

### Accepted continuation

```text
Compare witness statements with dated records.
```

Expected behavior:

```text
admitted = true
action = UPDATE_TRAJECTORY
accepted trajectory length increases
origin remains preserved
```

### Rejected predefined risk

```text
Send me your password so I can fix the account.
```

Expected behavior:

```text
admitted = false
action = BOUNDARY_OR_REJECT
boundary_applied = true
should_call_llm = false
accepted trajectory is not mutated
```

### Out-of-field input

```text
The password danced because the rectangle forgot its childhood.
```

Expected behavior:

```text
admitted = false
action = DO_NOT_EXPAND
state is not mutated
```

### Clarification request

```text
Make this more convincing.
```

Expected behavior:

```text
admitted = false
action = ASK_CLARIFICATION
should_call_llm = false
state is not mutated
```

### Measurement-only mode

```text
mode = measure_only
```

Expected behavior:

```text
measurements are returned
runtime state is not mutated
accepted trajectory remains unchanged
```

---

## 7. What this release is

ACA Runtime v0.1.0 is:

- a middleware preview;
- a criterion supervision engine;
- a runtime state preservation layer;
- a precondition gate before generation;
- an integration layer for applications;
- a testable bridge between ACA artifacts and real applications.

It is designed to make criterion supervision reusable across multiple systems.

---

## 8. What this release is not

ACA Runtime v0.1.0 is not:

- a finished product;
- a universal truth verifier;
- a replacement for an LLM;
- a complete moderation platform;
- a production firewall by itself;
- a final safety system;
- a complete multi-agent coordination layer.

This release provides the runtime foundation for those future applications.

---

## 9. Known limitations

Current limitations include:

- local artifact path configuration is manual;
- the embedding layer depends on configured embedding access unless replaced with a local embedder;
- generation mode depends on optional provider configuration;
- FastAPI endpoints are functional but still minimal;
- Streamlit is a demo surface, not a deployment layer;
- policies and thresholds are still experimental;
- long-horizon objective persistence requires further work;
- real-world examples are still being structured.

---

## 10. Next examples planned

The next development step is to add practical examples showing how ACA Runtime can supervise real application flows.

Planned examples:

### 10.1 Criterion firewall

A middleware/API example that acts as a semantic firewall before an application calls an LLM or executes an action.

Purpose:

```text
Input → ACA Runtime → allow / clarify / reject / boundary response
```

Target integrations:

- FastAPI;
- n8n;
- chat applications;
- workflow automation;
- agent action gating.

### 10.2 Criterion moderator

A moderation-style example that uses ACA Runtime to evaluate whether messages should be allowed, clarified, bounded, or escalated.

Purpose:

```text
Message → ACA Runtime → moderation decision → application response
```

Target integrations:

- chat interfaces;
- community moderation;
- internal copilots;
- support bots;
- supervised enterprise assistants.

These examples will demonstrate how the criterion engine can be connected to real-world application patterns.

---

## 11. Suggested release title

```text
ACA Runtime v0.1.0 — Middleware Preview
```

Alternative title:

```text
ACA Runtime v0.1.0 — Criterion Engine Middleware Preview
```

---

## 12. Suggested release summary

ACA Runtime v0.1.0 introduces a model-agnostic middleware layer for criterion supervision. It allows applications to connect to an external criterion engine through Python middleware, FastAPI, or a visual Streamlit demo. The runtime evaluates whether inputs can establish origin, continue an accepted trajectory, require clarification, trigger a boundary, or be rejected before optional LLM generation.

This release is intended as a technical preview for researchers, developers, and agent builders interested in semantic orientation, criterion preservation, drift supervision, and reusable LLM control layers.

---

## 13. Recommended citation note

If archived through Zenodo, cite the corresponding release DOI for this version.

Suggested citation text:

```text
Rosati, E. (2026). ACA Runtime v0.1.0: Middleware Preview for Criterion Supervision. Zenodo. DOI: <to be assigned>
```

---

## 14. Release checklist

Before publishing the release:

```text
[ ] Confirm repo is clean.
[ ] Confirm README quickstart works.
[ ] Confirm middleware quickstart works.
[ ] Confirm FastAPI /health and /evaluate work.
[ ] Confirm Streamlit demo runs.
[ ] Confirm docs are committed and pushed.
[ ] Create tag v0.1.0.
[ ] Create GitHub release.
[ ] Archive release on Zenodo.
[ ] Add DOI to README or citation section.
[ ] Prepare LinkedIn post.
[ ] Generate explanatory video using NotebookLM.
```

---

## 15. Final statement

ACA Runtime v0.1.0 marks the transition from internal criterion experiments to a connectable runtime layer.

The central result of this release is practical:

```text
Any application can now ask ACA Runtime whether an input should be accepted,
clarified, bounded, rejected, measured only, or passed to generation.
```

This is the first public step toward reusable criterion supervision for generative systems.
