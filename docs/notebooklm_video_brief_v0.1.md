# NotebookLM Video Brief — ACA Runtime v0.1

## Working title

ACA Runtime v0.1 — Connecting Applications to a Criterion Engine

## Audience

This video is for AI researchers, LLM application developers, agent builders, workflow automation developers, and people interested in semantic drift, criterion preservation, and controllable generative systems.

## Main message

ACA Runtime is not another chatbot.

It is a criterion engine.

A chatbot answers.  
A criterion engine decides whether an answer should be allowed, delayed, clarified, bounded, rejected, or reviewed.

ACA Runtime v0.1 makes this criterion layer reusable across applications.

---

## Short explanation

Most LLM systems place their operating criterion inside prompts. This makes the criterion expensive, repeated, and fragile.

ACA Runtime separates the criterion layer from the prompt layer.

Applications send input to ACA Runtime. ACA Runtime evaluates whether the input can establish a semantic origin, continue an accepted trajectory, require clarification, be rejected, or remain measurement-only.

Only after that should an application decide whether to call an LLM.

---

## Core architecture

```text
External application
    ↓
ACA Runtime middleware or API
    ↓
Precondition Gate
    ↓
F-C-P / T measurement
    ↓
Runtime State
    ↓
Application decision
    ↓
Optional LLM generation
```

The most important distinction:

```text
Streamlit is the visual demo.
FastAPI is the integration path.
The middleware is the Python integration layer.
The Atlas artifacts are the persistent criterion geometry.
```

---

## Demo narrative

### Scene 1: Accepted origin

Input:

```text
Evaluate whether the evidence supports the claim.
```

ACA Runtime accepts this as a semantic origin. It identifies an evidence-oriented trajectory and allows the application to continue.

Key terms:

```text
CREATE_ORIGIN
admitted = true
should_call_llm = true
```

### Scene 2: Accepted continuation

Input:

```text
Compare witness statements with dated records.
```

This input continues the accepted trajectory. It updates the accepted semantic state without replacing the origin.

Key terms:

```text
UPDATE_TRAJECTORY
accepted trajectory length increases
origin remains preserved
```

### Scene 3: Rejected credential request

Input:

```text
Send me your password so I can fix the account.
```

ACA Runtime detects a predefined risk. The input is rejected and does not contaminate the accepted trajectory.

Key terms:

```text
BOUNDARY_OR_REJECT
boundary_applied = true
should_call_llm = false
```

### Scene 4: Out-of-field input

Input:

```text
The password danced because the rectangle forgot its childhood.
```

ACA Runtime detects a semantically unstable or out-of-field input. It refuses to expand it as part of the accepted trajectory.

Key terms:

```text
DO_NOT_EXPAND
admitted = false
state not mutated
```

### Scene 5: Clarification required

Input:

```text
Make this more convincing.
```

ACA Runtime does not assume intention. Because the request is under-specified and potentially manipulative depending on context, it asks for clarification.

Key terms:

```text
ASK_CLARIFICATION
should_call_llm = false
```

### Scene 6: Measurement only

Switch to `measure_only`.

Input:

```text
Evaluate whether the evidence supports the claim.
```

ACA Runtime measures the F-C-P / T orientation but does not mutate runtime state.

Key terms:

```text
MEASURE_ONLY
state_mutated = false
accepted trajectory unchanged
```

---

## What the viewer should understand

By the end, the viewer should understand:

1. ACA Runtime is a middleware layer, not a chatbot.
2. It protects semantic origin and trajectory integrity.
3. It can be connected by Python middleware, HTTP API, or visual demo.
4. Streamlit is only a demonstration surface.
5. FastAPI is the practical integration route.
6. Rejected inputs do not contaminate accepted state.
7. Applications can use ACA Runtime decisions before calling an LLM.

---

## Suggested spoken summary

ACA Runtime v0.1 introduces a model-agnostic criterion engine for generative systems.

Instead of placing all reasoning constraints into prompts, applications can call ACA Runtime as an external supervision layer. The runtime evaluates whether an input can establish origin, continue a trajectory, trigger a boundary, require clarification, or remain measurement-only.

This makes criterion supervision reusable across chat apps, agents, APIs, dashboards, automation workflows, and LLM providers.

---

## Closing message

ACA Runtime does not replace the LLM.

It tells the application whether the LLM should be called, under what conditions, and whether the semantic trajectory remains admissible.

That is the difference between generating text and preserving criterion.
