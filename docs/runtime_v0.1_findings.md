# ACA Runtime v0.1 Findings

**Extracted from docs/ and experiments/**

Version: v0.1.0  
Project: ACA Runtime  
Status: Findings draft for release preparation

---

## 1. Executive Summary

ACA Runtime has evolved from a simple origin-cost evaluator into a layered supervision architecture.

The main discovery is that criterion preservation requires more than measuring semantic field proximity. Runtime must control when an input is allowed to become semantic origin, preserve an accepted trajectory, condition generation, and review generated outputs.

The strongest current thesis is:

```text
ACA Runtime operationalizes ACA artifacts as a pre-reasoning and post-generation criterion supervision layer, preserving semantic origin, objective continuity, trajectory integrity, and admissible generation boundaries.
```

---

## 2. Architectural Finding: Signal Is Not Action

The documents define a central separation:

```text
The Atlas measures.
The Runtime interprets.
The Application decides.
The LLM generates.
```

This prevents a critical design error: treating a measurement as a decision.

An Atlas signal such as origin cost, field margin, drift, ambiguity, F-C-P orientation, or invariant preservation should not directly become a product action. The Runtime interprets signals into operational states, and the Application maps those states to behavior.

---

## 3. Main Runtime Finding: Invalid Inputs Must Not Become Origin

The Precondition Gate introduces the central invariant of Runtime v0.1:

```text
A rejected, unclear, restricted, or out-of-field input
must not become semantic origin
and must not update the accepted trajectory.
```

This is the operational answer to a common generative failure pattern:

```text
unvalidated premise
  ↓
probabilistic expansion
  ↓
apparent coherence
  ↓
semantic drift or hallucination
```

The Precondition Gate interrupts the sequence before the model expands from an invalid premise.

---

## 4. Distinction: Precondition Is Not Full Criterion

The Precondition Gate does not exercise full criterion.

Criterion requires:

```text
accepted origin
reference frame
trajectory history
objective or task context
sufficient evidence of preservation, drift, contradiction, inversion, or recovery
```

Precondition only determines whether the input may enter semantic state.

This distinction is essential because it prevents the runtime from overclaiming. It does not know the full truth of the input; it determines whether the input is admissible enough to become origin or continuation.

---

## 5. Finding from Reporter Mode

Reporter Mode tested whether semantic orientation can be observed without intervention.

Main finding:

```text
Semantic drift can occur without changing topics.
Declared frame transitions improve interpretability
without requiring psychological intention inference.
```

This is important because ACA Runtime does not need to infer hidden intention. It can detect whether a transition was declared or undeclared at the semantic level.

Examples:

```text
A hypothetical frame declared explicitly → interpretable transition.
An absurd factual-looking claim without declared frame → ambiguous drift.
A rhetorical frame declared explicitly → drift remains observable but becomes interpretable.
A return to evidential framing → recovery attempt, not necessarily immediate recovery.
```

---

## 6. Finding from Long-Horizon Criterion Preservation

The long-horizon experiment tested whether ACA-supervised interaction can preserve a research objective across multiple turns.

Main finding:

```text
ACA successfully preserved objective continuity.
The limitation was not criterion preservation.
The limitation was textual persistence cost.
```

In the experiment, ACA preserved the active evidence-based productivity investigation across subjective wellbeing, philosophical exploration, recovery, and supported-conclusion turns.

However, doing this through repeated textual reconstruction increased token cost.

Implication:

```text
Future Runtime should move from textual objective persistence
to persistent geometric objective representation.
```

---

## 7. Finding from Objective Vector Experiment

The objective-vector experiment clarified that ACA operates under two distinct regimes.

### Conversation Mode

Criterion is reconstructed dynamically from semantic trajectory.

Suitable for:

```text
moderation
short-horizon supervision
local drift detection
local criterion recovery
conversation stabilization
```

### Project Mode

Criterion must be declared explicitly and preserved as an external reference.

Required for:

```text
long-horizon projects
objective continuity
persistent task supervision
multi-turn research or writing workflows
```

Main finding:

```text
Conversation Mode ≠ Project Mode.
```

Trajectory continuity alone is not enough for project-level objective continuity.

---

## 8. Finding from Criterion Operating Layer Experiment

The Criterion Operating Layer experiment tested whether a persistent objective vector could guide long-horizon responses without repeatedly injecting full objective text.

Observed result:

```text
Pre-generation alignment over accumulated context is insufficient.
Accumulated context can mask local objective drift.
```

Generated responses drifted into generic answers even when goal alignment remained above threshold.

Implication:

```text
Runtime must evaluate generated outputs, not only user inputs.
```

A better loop is:

```text
User turn
  ↓
Generate candidates
  ↓
Evaluate candidates against objective vector, semantic field, origin cost, and orientation diagnostics
  ↓
Select, revise, clarify, or reanchor
```

---

## 9. Finding from Candidate Competition

Candidate competition tested whether the runtime could select the best response among generated candidates.

Main finding:

```text
Origin cost and field proximity alone are insufficient.
```

Candidate selection must separate several signals:

```text
origin cost
criterion confidence
objective alignment
foundation orientation
foundation delta
ambiguity
trajectory drift
policy state
```

A response may be close to a field but still fail the active objective or degrade foundational orientation.

---

## 10. Finding from Supervised Generation Prototype

Runtime v2 demonstrates a complete first loop:

```text
input measurement
precondition gate
state mutation only if admitted
application response
silent generation conditioning
LLM call only if allowed
post-generation review
release or reanchor
```

This shows that ACA Runtime can supervise generation without exposing internal runtime terminology to the user.

---

## 11. Finding on Output Drift

Generated output can shift orientation even when the user input was admissible.

Therefore, Runtime must compare the output orientation against the admitted input orientation.

Important drift flags include:

```text
foundation_shift
context_shift
principle_shift
research_to_manipulation_shift
investigate_to_exploit_shift
protect_to_exploit_shift
output_manipulation_exploit
```

This extends ACA Runtime beyond pre-generation supervision into post-generation release control.

---

## 12. Finding on Objective Persistence

Textual objective persistence works but is expensive.

Geometric objective persistence is the next necessary step.

The future architecture should preserve objective through:

```text
objective vector
criterion layer
trajectory supervision
post-generation candidate evaluation
```

rather than repeated full objective prompt reconstruction.

---

## 13. Finding on Runtime Scope

ACA Runtime should be presented as:

```text
a supervision layer
not a truth engine
not a product policy
not a standalone alignment solution
not a replacement for human judgment
```

Its defensible claim is operational:

```text
ACA Runtime interprets ACA geometric artifacts to preserve semantic origin, trajectory integrity, objective continuity, and generation admissibility.
```

---

## 14. Stable Claims for v0.1.0

Runtime v0.1 can defensibly claim:

1. It loads ACA artifacts and measures F-C-P orientation.
2. It applies a deterministic Precondition Gate before state mutation.
3. It prevents non-admitted inputs from altering accepted origin or trajectory.
4. It supports supervised generation by conditioning LLM calls only after admission.
5. It can review generated outputs for semantic orientation shifts.
6. It separates Atlas measurement, Runtime interpretation, Application decision, and LLM generation.

---

## 15. Open Problems

The next stage should investigate:

```text
geometric objective persistence
candidate evaluation loops
fairer baselines against constant system prompts
stress tests in overlapping high-capacity semantic spaces
detection window under noisy fields
multi-agent shared coordination layers
learned but human-governed invariant proposal
```

---

## 16. Recommended Release Framing

Recommended title:

```text
ACA Runtime v0.1.0 — Pre-Reasoning Criterion Gate and Supervised Generation Layer
```

Recommended release thesis:

```text
ACA Runtime v0.1 operationalizes ACA v0.3 artifacts as a model-independent supervision layer that measures semantic orientation, protects origin formation, preserves accepted trajectory state, conditions generation, and reviews outputs before release.
```
