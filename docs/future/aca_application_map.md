# ACA Application Map

Status:
Conceptual Architecture

Version:
0.1

---

## Purpose

ACA Atlas is a geometric criterion infrastructure.

Its purpose is not to answer questions, block actions, or optimize outputs.

Its purpose is to measure semantic criterion through reusable geometric structures.

ACA produces criterion signals.

Applications interpret and use those signals.

---

## Core Signals

ACA evaluates:

- semantic field
- origin cost
- orientation
- trajectory continuity
- preservation
- contextual transitions
- drift
- reorientation
- inversion

Abstract representation:

S(z)={
Field,
Origin,
Orientation,
Trajectory,
Preservation
}

---

## Architectural Separation

ACA Atlas
→ Measures

ACA Runtime
→ Interprets

Applications
→ Decide

Principle:

The Atlas measures.
The application decides.

---

## Operational Applications

### Project Criterion Runtime

Goal:

Preserve long-horizon objective continuity.

Possible actions:

- allow
- clarify
- reanchor
- recovering
- declared_shift

---

### Semantic Firewall

Goal:

Evaluate whether content remains inside acceptable criterion boundaries.

Possible actions:

- allow
- flag
- block
- audit

---

### Moderation Runtime

Goal:

Detect ambiguity, contradiction, instability, or criterion loss.

Possible actions:

- warn
- clarify
- monitor

---

### Candidate Competition

Goal:

Compare candidate trajectories.

Possible actions:

- rank
- observe
- report

---

### Domain Runtime

Goal:

Apply specialized criterion.

Examples:

- legal
- scientific
- operational
- medical
- business

---

### Autonomous Runtime

Goal:

Maintain criterion continuity across long execution.

Possible actions:

- preserve
- recover
- redirect

---

## Current Focus

Current development studies:

external geometric supervision.

No modification of LLM internals is assumed.

---

## Design Principle

Do not replace context with more context.

Replace repeated context with persistent orientation.

---

## Conclusion

ACA is not a decision system.

ACA is criterion infrastructure.