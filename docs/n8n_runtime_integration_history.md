# n8n Runtime Integration History

## Purpose

This document records the practical history of the ACA Runtime + n8n integration.

The history matters because n8n did not merely serve as a demo layer. It exposed where ACA Runtime still needed stronger pre-input criterion, low-signal handling, and access-boundary interpretation.

## Timeline

### 1. Initial web + n8n integration

A web page was first connected to n8n so that user input could be sent through an automation workflow before returning an application response.

At this stage, n8n acted mainly as a bridge between the web interface and ACA Runtime.

### 2. Low-signal issue discovered

During testing, simple inputs such as:

```text
hola
hello
```

did not behave as expected.

This revealed that the system needed to distinguish between:

```text
application pass-through
semantic origin admission
runtime state mutation
LLM generation
```

A greeting may be accepted by the application without becoming semantic origin.

### 3. Temporary n8n disconnection

To remove integration noise, the web page was temporarily connected directly to Python/FastAPI on the Ubuntu server.

This allowed testing ACA Runtime behavior without n8n as an intermediate layer.

### 4. n8n reconnection

After the direct Python path was stabilized, n8n was reconnected.

The integration worked, but additional boundary and criterion issues appeared. This led back to experimentation rather than further UI tuning.

### 5. Security Access Boundary experiments

The next phase focused on credential/access-boundary behavior.

This produced:

```text
datasets/security_access_boundary/out_of_sample_v1.jsonl
datasets/security_access_boundary/holdout_v1.jsonl
tools/probe_security_access_boundary_dataset.py
tools/probe_security_access_boundary_contextual_experiment_v2.py
docs/security_access_boundary_holdout_v1_analysis.md
```

The frozen holdout established a baseline of:

```text
74/96 strict decisions
```

The contextual experiment improved this to:

```text
95/96 strict decisions
0 regressions
```

without modifying the atlas, anchors, artifacts, embedding model, or holdout dataset.

### 6. Architectural conclusion

The important discovery was not only the improved score.

The main architectural discovery was:

```text
Criterion should be evaluated as a ranked-field relation,
not as a single-field assignment.
```

This means ACA Runtime should preserve:

```text
top field
second field
third field
margins
deterministic signals
application policy profile
trajectory state
```

### 7. Return to n8n

After the experiments, n8n becomes useful again as an external orchestrator.

The new integration goal is:

```text
Browser / Web App
→ n8n Webhook
→ ACA Runtime /policy-evaluate
→ application-ready response envelope
→ n8n response
```

n8n should not duplicate criterion logic.

## Current Integration Decision

The recommended current design is:

```text
Webhook
→ HTTP Request /policy-evaluate
→ Respond to Webhook
```

The JavaScript Code node is no longer needed because ACA Runtime should return the application-ready envelope directly.

## Why This Matters

n8n showed the architectural problem.

Python/FastAPI isolated the Runtime problem.

The security access-boundary experiments improved the criterion layer.

Now n8n can return as the orchestration layer without duplicating Runtime logic.

## Final Principle

```text
n8n is not the criterion layer.
n8n is the integration layer.

ACA Runtime is the criterion interpreter.
The application decides how to act.
The LLM is called only when allowed.
```
