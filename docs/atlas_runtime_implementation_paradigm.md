\# ACA Runtime Implementation Paradigm



\## Model-Independent Deterministic Conditioning and Criterion Preservation



Version: v0.1

Project: ACA Runtime v2

Status: Implementation architecture



\---



\# 1. Purpose



This document defines the implementation paradigm for using ACE Atlas with any large language model, generative model, agent, or semantic application.



The Runtime is model-independent.



Ollama, local models, cloud APIs, proprietary models, and open-weight models are implementation options.



The architecture does not depend on a specific model provider.



The central principle is:



```text

The Atlas measures.



The Runtime interprets.



The Application decides.



The LLM generates.

```



\---



\# 2. Implementation objective



The objective is to condition generative systems deterministically before, during, and after generation.



The Runtime should:



```text

prevent invalid origin formation

prevent rejected inputs from contaminating trajectory

preserve declared objective

measure semantic drift

activate triaxial discernment when needed

apply predefined risk policies

condition generation

review generated output

```



\---



\# 3. Two operational functions



ACA Runtime has two distinct functions.



\## 3.1 Precondition before trajectory



Question:



```text

Can this input become semantic origin

or enter the accepted trajectory?

```



Possible outcomes:



```text

ACCEPT\_AS\_ORIGIN

ACCEPT\_AS\_CONTINUATION

ASK\_CLARIFICATION

DECLARE\_INTENT

BOUNDARY\_RESPONSE

REJECT\_PREDEFINED\_RISK

FLAG\_OUT\_OF\_FIELD

CONTINUE\_MONITORING

```



\## 3.2 Criterion preservation after origin



Question:



```text

Does the accepted trajectory remain properly oriented?

```



Possible outcomes:



```text

ALLOW

CLARIFY

REANCHOR

DECLARED\_SHIFT

FLAG\_DRIFT

RECOVERING

VERIFY

RESTRICT

```



These functions must not be confused.



The Precondition Gate does not exercise full criterion.



It protects the conditions required for criterion to become possible.



\---



\# 4. Model-independent architecture



```text

USER INPUT

↓

ACE ATLAS PRE-ORIENTATION MEASUREMENT

↓

ACA RUNTIME PRECONDITION GATE

↓

ORIGIN / TRAJECTORY STATE UPDATE

↓

TRIAXIAL CRITERION PROJECTION

↓

TRAJECTORY AND INVARIANT EVALUATION

↓

GENERATION CONDITIONING

↓

LLM OR GENERATIVE MODEL

↓

POST-GENERATION REVIEW

↓

APPLICATION ACTION

```



\---



\# 5. ACE Atlas measurements



The Runtime should consume Atlas measurements such as:



```text

semantic field

origin cost

field margin

field coverage

projection energy

foundational stability

structural orientation

intent orientation

rhetorical movement

objective alignment

F–C–P profile

trajectory preservation

invariant preservation

```



The Atlas should not emit product actions.



It emits measurements.



\---



\# 6. Precondition Gate



The Precondition Gate determines whether an input may enter semantic state.



\## 6.1 Accept as origin



Use when:



```text

no origin exists

semantic orientation is sufficient

the input is understandable

no strict risk invariant applies

the input is not out-of-field

```



State:



```text

ACCEPT\_AS\_ORIGIN

```



Action:



```text

create origin

initialize objective if declared

initialize accepted trajectory

```



\## 6.2 Accept as continuation



Use when:



```text

an origin exists

the input is admissible

the input can be compared against the accepted trajectory

```



State:



```text

ACCEPT\_AS\_CONTINUATION

```



Action:



```text

update accepted trajectory

```



\## 6.3 Ask clarification



Use when:



```text

the objective is unclear

the request is under-contextualized

intent is insufficiently declared

field orientation is ambiguous

```



State:



```text

ASK\_CLARIFICATION

```



Action:



```text

do not create origin

do not update trajectory

```



\## 6.4 Declare intent



Use when the system can identify a likely intent but requires confirmation.



State:



```text

DECLARE\_INTENT

```



Action:



```text

state the apparent intent

request clarification

do not update trajectory

```



\## 6.5 Boundary response



Use when a request touches a restricted region but can be redirected safely.



State:



```text

BOUNDARY\_RESPONSE

```



Action:



```text

respond within safe boundaries

do not accept unsafe objective as origin

```



\## 6.6 Reject predefined risk



Use when a strict Runtime invariant applies.



Examples:



```text

credential extraction

private key request

unsafe access bypass

coercive compliance

```



State:



```text

REJECT\_PREDEFINED\_RISK

```



Action:



```text

do not create origin

do not update trajectory

do not perform unnecessary semantic expansion

```



\## 6.7 Flag out-of-field



Use when:



```text

origin cost is high

field coverage is poor

foundational stability is low

no known semantic field provides sufficient orientation

```



State:



```text

FLAG\_OUT\_OF\_FIELD

```



Action:



```text

do not invent meaning

do not update trajectory

```



\---



\# 7. State update rule



The most important Runtime invariant is:



```text

A non-admitted input must never alter the accepted origin or trajectory.

```



State mutation rules:



```text

ACCEPT\_AS\_ORIGIN

→ create origin

→ create trajectory



ACCEPT\_AS\_CONTINUATION

→ append to accepted trajectory



ASK\_CLARIFICATION

→ no state mutation



DECLARE\_INTENT

→ no state mutation



BOUNDARY\_RESPONSE

→ no unsafe state mutation



REJECT\_PREDEFINED\_RISK

→ no state mutation



FLAG\_OUT\_OF\_FIELD

→ no state mutation

```



Rejected inputs may be stored in an audit log, but not in the accepted semantic trajectory.



\---



\# 8. Origin state



The Runtime should preserve an explicit origin state.



Example:



```json

{

&#x20; "origin\_id": "origin\_001",

&#x20; "origin\_text": "Evaluate the evidence before drawing a conclusion.",

&#x20; "origin\_field": "factual",

&#x20; "origin\_cost": 0.18,

&#x20; "objective": "determine whether the evidence supports the claim",

&#x20; "triaxial\_profile": {

&#x20;   "F": "factual",

&#x20;   "C": "research",

&#x20;   "P": "investigate"

&#x20; }

}

```



The origin is not necessarily immutable.



It may be replaced only through a declared and accepted shift.



\---



\# 9. Objective vector



A declared project or task objective should be represented as a guide vector.



The Runtime should evaluate each accepted continuation against:



```text

origin

objective vector

previous accepted state

current field

F–C–P orientation

invariants

```



Possible objective states:



```text

ALIGNED

POSSIBLE\_SHIFT

DECLARED\_SHIFT

UNDECLARED\_SHIFT

CONFLICT

```



\---



\# 10. Triaxial activation



The Runtime should not force F–C–P onto every input.



The Triaxial Criterion Projection should activate when:



```text

an input is accepted

criterion resolution is needed

drift appears

context and principle disagree

a high-risk topic requires distinction

objective alignment becomes uncertain

```



Example:



```text

C = manipulation

P = protect

```



may represent defensive analysis.



But:



```text

C = manipulation

P = exploit

```



may represent exploitative manipulation.



\---



\# 11. Trajectory memory



The Runtime should preserve only accepted semantic states.



Each accepted turn may record:



```text

semantic field

origin cost

objective alignment

F

C

P

rhetorical movement

invariant preservation

risk signals

decision state

```



Example:



```json

{

&#x20; "step": 4,

&#x20; "field": "factual",

&#x20; "origin\_cost": 0.24,

&#x20; "objective\_alignment": 0.91,

&#x20; "F": "factual",

&#x20; "C": "research",

&#x20; "P": "investigate",

&#x20; "trajectory\_state": "stable"

}

```



\---



\# 12. Drift detection



Drift should be evaluated relative to accepted state.



Possible signals:



```text

field transition

origin cost increase

objective misalignment

context shift

principle shift

invariant inversion

contradiction

uncertainty collapse

rhetorical dominance

```



A single signal may not justify intervention.



The Runtime should combine signals unless a strict invariant applies.



\---



\# 13. Declared shift



Not every shift is drift.



A user may intentionally change objective.



The Runtime should distinguish:



```text

declared shift

undeclared shift

```



A declared shift may create a new origin.



```text

current origin

↓

user declares new objective

↓

Runtime confirms

↓

new accepted origin

```



\---



\# 14. Recovery



The Runtime should detect recovery after drift.



```text

drift

↓

reorientation

↓

return to origin-compatible trajectory

```



Recovery should be recorded separately from uninterrupted stability.



Possible states:



```text

STABLE

DRIFTING

REANCHORING

RECOVERING

RECOVERED

```



\---



\# 15. Generation conditioning



Once an input is admitted, the Runtime may provide compact conditioning to any LLM.



Example:



```text

Accepted origin:

Evaluate the evidence before drawing a conclusion.



Active objective:

Determine whether the evidence supports the claim.



Semantic field:

Factual



Triaxial orientation:

F = factual

C = research

P = investigate



Trajectory state:

Stable



Generation constraint:

Preserve uncertainty and evidence orientation.

```



The conditioning should be compact.



The purpose is to reduce prompt overhead and prevent criterion reconstruction from scratch.



\---



\# 16. Post-generation review



The generated output should be evaluated before final release.



```text

accepted user input

↓

generation conditioning

↓

LLM output

↓

Atlas measurement

↓

Runtime interpretation

↓

release / revise / reanchor / restrict

```



Possible post-generation states:



```text

ALLOW\_OUTPUT

REVISE\_OUTPUT

REANCHOR\_OUTPUT

FLAG\_DRIFT

RESTRICT\_OUTPUT

```



\---



\# 17. Deterministic operation



The Runtime can operate without asking an LLM to reason about every input.



Required components:



```text

fixed embedding model

versioned artifacts

fixed normalization

fixed thresholds

fixed scoring rules

fixed state transitions

fixed policy ordering

```



The same input and state should produce the same Runtime interpretation.



\---



\# 18. Any-LLM integration patterns



\## 18.1 External wrapper



```text

application

→ ACA Runtime

→ LLM API

```



The Runtime evaluates before and after generation.



\## 18.2 Middleware



```text

client

→ ACA middleware

→ model provider

```



The middleware conditions requests and reviews responses.



\## 18.3 Agent tool



```text

agent

→ consult Atlas tool

→ receive orientation

→ continue task

```



\## 18.4 Multi-agent supervisor



```text

worker agents

→ Atlas supervisor

→ trajectory coordination

```



\## 18.5 Local model deployment



```text

local application

→ ACA Runtime

→ local LLM

```



Ollama is one example, not a requirement.



\---



\# 19. Three implementation horizons



\## Horizon 1 — External deterministic supervision



```text

Atlas + Runtime + any LLM

```



The model is not modified.



\## Horizon 2 — ACA-aware model



A model is trained to use or imitate Runtime guidance.



```text

Atlas + Runtime + ACA decision dataset + fine-tuned model

```



\## Horizon 3 — Atlas-integrated inference



The Atlas becomes part of model inference.



```text

semantic field routing

criterion-aware decoding

trajectory-aware memory

invariant-conditioned generation

```



\---



\# 20. Efficiency hypothesis



The Runtime may reduce computational waste by preventing unnecessary generation.



Examples:



```text

ambiguous input

→ ask clarification

→ avoid long speculative response



out-of-field input

→ stop expansion

→ avoid hallucination



predefined risk

→ apply boundary

→ avoid unnecessary reasoning



long project

→ pass compact orientation

→ avoid repeated prompt reconstruction

```



The efficiency hypothesis should be tested through:



```text

token usage

generation count

latency

energy consumption

trajectory correction rate

prompt overhead

```



\---



\# 21. Validation plan



The Runtime should be validated against:



```text

valid origin cases

ambiguous origin cases

out-of-field cases

predefined risk cases

valid continuation cases

rejected continuation cases

origin preservation cases

declared shift cases

undeclared shift cases

recovery cases

```



Primary property:



```text

A non-admitted input must never alter the accepted origin or trajectory.

```



\---



\# 22. Baseline comparisons



The implementation should compare:



```text

LLM only

LLM + prompt instructions

LLM + F–C–P only

LLM + Atlas Precondition Gate

LLM + full ACA Runtime supervision

```



Metrics:



```text

drift rate

false origin creation

trajectory contamination

clarification accuracy

risk interception

objective preservation

token usage

latency

```



\---



\# 23. Separation of responsibilities



```text

ACE Atlas

→ measures geometry



ACA Runtime

→ interprets semantic state



Application

→ defines product action



LLM

→ generates language

```



Do not confuse these responsibilities.



A geometric signal is not an application action.



A Runtime state is not a final product decision.



\---



\# 24. Implementation thesis



ACA Runtime changes generative system behavior by placing semantic orientation before probabilistic expansion.



Instead of allowing the model to decide whether a premise is valid while already generating from it, the Runtime evaluates whether the premise may enter semantic state.



Once origin exists, the Runtime preserves criterion through objective vectors, trajectory memory, F–C–P orientation, and invariant evaluation.



```text

Do not expand an unvalidated semantic premise.



Do not update trajectory with a rejected input.



Do not reconstruct criterion from scratch in every prompt.



Condition generation with persistent geometric orientation.

```



\---



\# 25. Working conclusion



ACA Runtime provides a model-independent implementation path for ACE Atlas.



The Runtime enables deterministic conditioning before generation, trajectory supervision during interaction, and semantic review after generation.



The goal is not to replace the LLM.



The goal is to ensure that the LLM does not become the sole source, judge, and guardian of its own criterion.



```text

The Atlas measures.



The Runtime preserves orientation.



The Application acts.



The LLM expresses.

```



