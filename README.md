# ACA Runtime

## Citation

ACA Runtime v0.2.1 — Criterion Engine Middleware Preview is archived on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20621666.svg)](https://doi.org/10.5281/zenodo.20621666)

Version-specific DOI:

```text
10.5281/zenodo.20621666

**Pre-Reasoning and Post-Generation Criterion Supervision for ACA v0.3 Artifacts**

ACA Runtime operationalizes the Axiomatic Criterion Atlas (ACA) by loading persistent geometric artifacts and applying them as a runtime supervision layer for generative systems.

Instead of relying on repeated prompt reconstruction to preserve criterion, ACA Runtime uses Atlas measurements, precondition gating, trajectory state, generation conditioning, and post-generation review to supervise whether a semantic interaction remains admissible, oriented, and coherent with its accepted origin and objective.

---

## Core Principle

```text
The Atlas measures.
The Runtime interprets.
The Application decides.
The LLM generates.
```

This separation prevents a common architectural mistake: confusing a geometric signal with a product action.

- **ACA Atlas** builds and publishes persistent geometric artifacts.
- **ACA Runtime** loads those artifacts and interprets their signals.
- **Application layers** decide what to do with the interpreted state.
- **LLMs or generative models** generate only when the runtime/application state permits it.

---

## What ACA Runtime Does

ACA Runtime provides a model-independent supervision layer that can operate before, during, and after generation.

It is designed to:

- prevent invalid semantic origin formation;
- prevent rejected, unclear, restricted, or out-of-field inputs from contaminating the accepted trajectory;
- preserve declared objectives across interaction;
- measure F-C-P orientation using ACA artifacts;
- detect ambiguity, drift, declared shifts, and recovery attempts;
- condition generation silently without exposing internal runtime terminology;
- review generated outputs before release;
- support application modes such as reporting, warning, moderation, interactive clarification, and candidate selection.

---

## What ACA Runtime Is Not

ACA Runtime is not:

- a universal truth verifier;
- a moral reasoning engine;
- a consciousness model;
- a replacement for human judgment;
- a standalone guarantee of alignment;
- a product policy layer by itself.

It provides auditable geometric and operational signals that applications may use to preserve semantic orientation and runtime admissibility.

---

## Runtime v0.1 Focus

**ACA Runtime v0.1** focuses on the **Pre-Reasoning Criterion Gate** and the first supervised generation loop.

The central invariant is:

```text
A non-admitted input must never alter semantic origin
or accepted trajectory.
```

This means that unclear, restricted, adversarial, absurd, or out-of-field inputs may be recorded and reported, but they do not become the operational foundation of the conversation or project.

---

## Operational Functions

ACA Runtime separates two functions that should not be conflated.

### 1. Precondition Before Trajectory

Question:

```text
Can this input become semantic origin
or enter the accepted trajectory?
```

Possible states:

```text
ACCEPT_AS_ORIGIN
ACCEPT_AS_CONTINUATION
ASK_CLARIFICATION
DECLARE_INTENT
BOUNDARY_RESPONSE
REJECT_PREDEFINED_RISK
FLAG_OUT_OF_FIELD
CONTINUE_MONITORING
```

### 2. Criterion Preservation After Origin

Question:

```text
Does the accepted trajectory remain properly oriented?
```

Possible states:

```text
ALLOW
CLARIFY
REANCHOR
DECLARED_SHIFT
FLAG_DRIFT
RECOVERING
VERIFY
RESTRICT
```

The Precondition Gate does not exercise full criterion. It protects the conditions required for criterion to become possible.

---

## Runtime Architecture

```text
User input
  ↓
ACA Atlas pre-orientation measurement
  ↓
Precondition Gate
  ↓
Runtime State
  ↓
F-C-P / trajectory / invariant evaluation
  ↓
Generation conditioning
  ↓
LLM or generative model
  ↓
Post-generation review
  ↓
Application action
```

---

## Key Components

```text
aca_runtime/runtime/atlas_loader_v2.py
aca_runtime/runtime/atlas_measurements.py
aca_runtime/runtime/precondition_gate.py
aca_runtime/runtime/runtime_state.py
aca_runtime/runtime/runtime_v2.py
aca_runtime/runtime/generation_conditioning.py
aca_runtime/runtime/supervised_generation.py
aca_runtime/runtime/post_generation_review.py
aca_runtime/server/app.py
```

---

## Installation

```bash
pip install -e .
```

ACA Runtime expects ACA artifacts to be available locally. The artifact path may be passed explicitly to the runtime or server.

---

## Plug-and-Play Middleware Quickstart

```powershell
git clone https://github.com/rosatisoft/aca-runtime.git
cd aca-runtime

python -m pip install -e .

$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"

python examples\quickstart_middleware_v0_1.py

python -m uvicorn aca_runtime.server.app:app --reload
```

In another PowerShell window, test the API:

```powershell
powershell -ExecutionPolicy Bypass -File .\examples\quickstart_api_test.ps1
```

Expected result:

```text
GET /health       -> ok
POST /evaluate    -> ALLOW / CLARIFY / FLAG_DRIFT depending on input
POST /trajectory  -> trajectory report with drift diagnostics
```

---

## Minimal Runtime Example

```python
from aca_runtime.runtime.runtime_v2 import ACARuntimeV2

runtime = ACARuntimeV2(
    artifacts_root="path/to/ACA/artifacts"
)

result = runtime.step(
    text="Evaluate whether the evidence supports the claim.",
    objective="Analyze claims using only available evidence."
)

print(result.to_dict())
```

---

## Supervised Generation Example

```python
from aca_runtime.runtime.supervised_generation import ACASupervisedGenerator
from aca_runtime.runtime.runtime_v2 import ACARuntimeV2

runtime = ACARuntimeV2(
    artifacts_root="path/to/ACA/artifacts"
)

generator = ACASupervisedGenerator(runtime=runtime)

result = generator.step(
    "Compare the witness statements with dated records.",
    objective="Evaluate evidence without unsupported certainty."
)

print(result.final_response)
```

---

## API Server

```bash
python -m uvicorn aca_runtime.server.app:app --reload
```

Endpoints:

```text
GET  /health
POST /evaluate
POST /trajectory
POST /criterion-route
```

---

## Experimental Findings

The current experiments suggest:

1. Semantic drift can occur without changing topics.
2. Declared frame transitions improve interpretability without requiring psychological intention inference.
3. Conversation-mode supervision can preserve local criterion through trajectory monitoring.
4. Project-mode supervision requires persistent objective conditioning.
5. Textual objective persistence improves continuity but increases token cost.
6. Persistent geometric objective representation is a necessary next step.
7. Pre-generation alignment over accumulated context is insufficient because prior context can mask local objective drift.
8. Candidate selection requires multiple signals, not origin cost alone.

See:

```text
docs/runtime_v0.1_findings.md
docs/runtime_v0.1_architecture.md
```

---

## Relationship to ACA

```text
ACA v0.3
  ↓
Persistent geometric artifacts
  ↓
ACA Runtime v0.1
  ↓
Pre-reasoning and post-generation criterion supervision
```

ACA builds the Atlas. ACA Runtime applies the Atlas.

---

## Status

Current focus:

- Runtime v2 precondition gate
- F-C-P Atlas measurements
- semantic origin preservation
- accepted trajectory protection
- supervised generation conditioning
- post-generation review
- basic API server

Next work:

- remove local hard-coded artifact paths;
- stabilize v0.1 demos;
- improve objective vector persistence;
- expand post-generation candidate evaluation;
- test overlapping fields and shorter intervention windows;
- add multi-agent shared coordination layer experiments.

---

## License

Apache License 2.0.
