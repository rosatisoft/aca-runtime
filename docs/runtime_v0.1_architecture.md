# ACA Runtime v0.1 Architecture

**Pre-Reasoning Criterion Gate and Supervised Generation Loop**

Version: v0.1.0  
Project: ACA Runtime  
Status: Architecture draft for release preparation

---

## 1. Purpose

ACA Runtime operationalizes ACA artifacts by interpreting persistent geometric measurements as runtime supervision signals.

The purpose of Runtime v0.1 is to demonstrate that ACA artifacts can be used before unrestricted generation to preserve semantic origin, trajectory integrity, objective continuity, and admissible generation boundaries.

The runtime is model-independent. It may supervise local models, cloud models, agent frameworks, chat interfaces, API gateways, moderation layers, or candidate selection systems.

---

## 2. Foundational Separation

```text
The Atlas measures.
The Runtime interprets.
The Application decides.
The LLM generates.
```

This separation is the architectural foundation of ACA Runtime.

The Atlas should not block, allow, answer, rank, moderate, or decide product behavior. It emits measurements.

The Runtime should not claim absolute truth or replace application policy. It interprets Atlas measurements into operational states.

The Application consumes Runtime states according to its use case.

---

## 3. Main Thesis

ACA Runtime v0.1 introduces a pre-reasoning criterion gate that determines whether a user input may become semantic origin or enter the accepted trajectory.

The core invariant is:

```text
A non-admitted input must never alter semantic origin
or accepted trajectory.
```

This is the operational bridge between ACA as persistent Atlas and ACA Runtime as a supervision layer.

---

## 4. Runtime Pipeline

```text
USER INPUT
  ↓
ACA ATLAS PRE-ORIENTATION MEASUREMENT
  ↓
PRECONDITION GATE
  ↓
RUNTIME STATE UPDATE OR REJECTION
  ↓
TRIAXIAL / TRAJECTORY / INVARIANT EVALUATION
  ↓
GENERATION CONDITIONING
  ↓
LLM OR GENERATIVE MODEL
  ↓
POST-GENERATION REVIEW
  ↓
APPLICATION ACTION
```

---

## 5. Functional Layers

### 5.1 Atlas Loading

Loads ACA artifacts from a local artifact root. Runtime v0.1 supports manifest-based loading and fallback loading from the known ACA artifact directory structure.

Expected artifact types include:

```text
foundation artifacts
context artifacts
principle artifacts
transversal artifacts
field metadata
basis vectors
singular values
invariant directions
criterion vectors
```

### 5.2 Atlas Measurements

Measures a text embedding against the ACA artifact axes:

```text
Foundation
Context
Principle
Transversal
```

For each axis, the runtime computes:

```text
top artifact
second artifact
top origin cost
second origin cost
margin
ambiguity status
raw costs
```

The measurement layer does not decide. It only reports geometric signal.

### 5.3 Precondition Gate

The Precondition Gate decides whether the input may enter semantic state.

It combines:

```text
predefined access-risk checks
safe/protective context detection
under-contextualization checks
absurd/out-of-field markers
manipulative pressure patterns
compact F-C-P signals
low-margin ambiguity interpretation
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

The Precondition Gate does not exercise full criterion. It protects the conditions required for criterion to become possible.

### 5.4 Runtime State

Runtime state stores:

```text
accepted origin
active objective
accepted trajectory
rejected inputs
runtime events
```

Rejected inputs may be recorded, but they must not mutate:

```text
origin
objective
accepted trajectory
```

This prevents invalid premise formation and trajectory contamination.

### 5.5 Application Response

The application response translates runtime state into deterministic application-level messages and flags:

```text
origin_accepted
continuation_accepted
clarification_required
predefined_risk_rejected
out_of_field
boundary_response
intent_confirmation_required
monitoring
```

It also determines whether the LLM should be called.

### 5.6 Generation Conditioning

When generation is allowed, Runtime builds a compact internal orientation prompt.

This internal orientation is used silently by the LLM and should not be exposed to the user.

It includes:

```text
precondition state
application action
accepted origin
active objective
Foundation / Context / Principle orientation
generation constraints
```

### 5.7 Post-Generation Review

Generated output is measured again and compared against the admitted input orientation.

The review checks for shifts in:

```text
Foundation
Context
Principle
```

Severe flags include:

```text
research_to_manipulation_shift
investigate_to_exploit_shift
protect_to_exploit_shift
output_manipulation_exploit
```

Possible output review states:

```text
ALLOW_OUTPUT
REVIEW_OUTPUT
REANCHOR_OUTPUT
FLAG_OUTPUT_DRIFT
RESTRICT_OUTPUT
```

---

## 6. Two Runtime Functions That Must Not Be Confused

### 6.1 Precondition Before Trajectory

Question:

```text
Can this input become semantic origin
or enter the accepted trajectory?
```

This function protects admissibility before the system reasons from a premise.

### 6.2 Criterion Preservation After Origin

Question:

```text
Does the accepted trajectory remain properly oriented?
```

This function evaluates preservation, drift, declared shifts, recovery, reanchoring, and restriction after a valid origin exists.

---

## 7. Runtime Modes

ACA Runtime may support several application modes:

```text
report
warning
interactive
moderator
candidate selection
supervised generation
gateway / middleware
```

Each mode consumes the same runtime signals but maps them to different product actions.

---

## 8. Design Rules

1. Do not treat every input as a valid semantic premise.
2. Do not confuse measurement with action.
3. Do not let rejected input mutate origin or accepted trajectory.
4. Do not expose internal runtime terminology in user-facing answers.
5. Do not rely only on accumulated context for objective preservation.
6. Evaluate generated outputs, not only user inputs.
7. Use origin cost as one signal, not as the entire criterion.
8. Keep application policy separate from runtime interpretation.

---

## 9. Release Scope for v0.1.0

Runtime v0.1.0 should include:

```text
working Atlas v2 loader
F-C-P measurement layer
Precondition Gate
Runtime State
Runtime V2 step interface
Application Response
Supervised Generation prototype
Post-Generation Review
FastAPI server
basic examples and validation tools
README updated to this architecture
runtime_v0.1_findings.md
```

Out of scope for v0.1.0:

```text
full objective-vector persistence
multi-agent shared coordination layer
production gateway hardening
complete benchmark suite
learned invariant promotion
```

---

## 10. Next Research Direction

The next phase should test whether ACA Runtime can detect criterion degradation early enough in high-capacity, overlapping semantic spaces, especially when:

```text
fields overlap,
calibration margins narrow,
internal model commitment is not observable,
outputs may drift after admitted input,
and multi-agent systems preserve local coherence but produce boundary conflicts.
```
