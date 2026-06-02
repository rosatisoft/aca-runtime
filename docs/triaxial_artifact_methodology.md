\# Triaxial Artifact Methodology



\## 1. Purpose



This document defines how the Triaxial Method of Discernment uses ACE Atlas artifacts without duplicating the Atlas.



The Triaxial Method is not a separate atlas.



It is a criterion-resolution projection that consults existing and new geometric artifacts to determine how a semantic trajectory should be interpreted, preserved, clarified, reoriented, restricted, or stopped.



```text

ACE Atlas = geometric artifact system

F-C-P = triaxial criterion projection

ACA Runtime = operational decision layer

```



The goal is not to replace reasoning with a single classifier.



The goal is to provide a multi-reference geometric structure that allows an agent to preserve criterion during generative reasoning.



\---



\## 2. Existing artifacts



The current ACA artifact set already contains foundational fields that must be reused.



Existing artifacts:



```text

artifacts/foundational

artifacts/factual

artifacts/rhetorical

```



These should not be duplicated inside the triaxial layer.



Instead, the triaxial projection should reference them.



\---



\## 3. Role of existing artifacts



\### 3.1 Foundational Field



Path:



```text

artifacts/foundational

```



Role:



```text

criterion substrate

```



The foundational field provides the invariant base for preserving orientation.



It includes invariants such as:



```text

non\_contradiction

identity

persistence

relation

evidence\_constraint

causal\_continuity

semantic\_stability

interpretive\_constraint

uncertainty\_preservation

field\_boundary

orientation\_continuity

correspondence

```



Use:



\* detect loss of basic semantic stability,

\* detect contradiction or collapse of identity,

\* detect out-of-field or absurd inputs,

\* support criterion preservation,

\* provide the highest-order reference when a trajectory becomes unstable.



The foundational field does not compete with factual, fictional, or hypothetical modes.



It supports the whole criterion structure.



\---



\### 3.2 Factual Field



Path:



```text

artifacts/factual

```



Role:



```text

factual reference mode

```



The factual field supports evidence-constrained reasoning, verification, source accountability, contradiction handling, and document-grounded interpretation.



Use in F-C-P:



```text

F = factual

```



This field answers:



```text

Does this claim operate within an evidence-constrained mode of reference?

```



\---



\### 3.3 Rhetorical Field



Path:



```text

artifacts/rhetorical

```



Role:



```text

rhetorical movement / persuasive framing detector

```



The rhetorical field supports detection of persuasive framing, emotional pressure, narrative dominance, reinterpretation, and rhetorical movement.



It should not be interpreted as automatically harmful.



Rhetorical movement may be legitimate in teaching, explanation, persuasion, or narrative.



However, when combined with manipulation, low evidence, pressure, or exploitative principle, it may indicate drift.



Example:



```text

rhetorical + teach

→ legitimate explanation



rhetorical + manipulation + exploit

→ possible coercive or exploitative drift

```



\---



\## 4. New artifacts required



To complete the triaxial projection, additional artifacts must be created.



\### 4.1 Foundation axis additions



Existing:



```text

foundational

factual

```



Required:



```text

fictional

hypothetical

```



Important:



```text

out\_of\_field

```



should initially be treated as a condition, not as a normal field.



Out-of-field can be detected through low confidence, low margin, high origin cost, or poor preservation of foundational invariants.



\---



\### 4.2 Context axis artifacts



Required v0.1 contexts:



```text

context/research

context/training

context/manipulation

context/narrative

```



These are not merely topic labels.



They are relational contexts that describe how meaning is operating.



Examples:



```text

research

→ evidence gathering, comparison, verification, uncertainty, provisional conclusions



training

→ instruction, examples, safe simulation, learner protection, prevention



manipulation

→ pressure, omission, urgency, coercion, selective framing, credential extraction



narrative

→ story, characters, imagined events, symbolic framing, fictional continuity

```



\---



\### 4.3 Principle axis artifacts



Required v0.1 principles:



```text

principle/investigate

principle/teach

principle/protect

principle/exploit

```



These are operational principles.



They should not be understood as the final complete set of all possible principles.



They are the initial set needed to validate triaxial criterion geometry.



Examples:



```text

investigate

→ discover, verify, compare evidence, preserve uncertainty



teach

→ explain, clarify, instruct, improve understanding



protect

→ reduce harm, verify safely, prevent misuse, preserve security



exploit

→ deceive, extract, pressure, bypass consent, obtain unsafe advantage

```



\---



\## 5. Proposed artifact structure



The triaxial layer should not duplicate existing artifacts.



Recommended structure:



```text

artifacts/

&#x20; foundational/

&#x20; factual/

&#x20; rhetorical/



&#x20; fictional/

&#x20; hypothetical/



&#x20; context/

&#x20;   research/

&#x20;   training/

&#x20;   manipulation/

&#x20;   narrative/



&#x20; principle/

&#x20;   investigate/

&#x20;   teach/

&#x20;   protect/

&#x20;   exploit/



&#x20; triaxial/

&#x20;   manifest.json

```



The `triaxial/manifest.json` file declares how the projection uses existing and new artifacts.



\---



\## 6. Triaxial manifest concept



The manifest should describe how the F-C-P projection consults the Atlas.



Example:



```json

{

&#x20; "version": "0.1.0",

&#x20; "projection": "triaxial\_criterion",

&#x20; "description": "F-C-P projection over ACE Atlas artifacts for criterion discernment.",

&#x20; "axes": {

&#x20;   "foundation": {

&#x20;     "criterion\_substrate": "../foundational",

&#x20;     "reference\_modes": {

&#x20;       "factual": "../factual",

&#x20;       "fictional": "../fictional",

&#x20;       "hypothetical": "../hypothetical"

&#x20;     }

&#x20;   },

&#x20;   "context": {

&#x20;     "research": "../context/research",

&#x20;     "training": "../context/training",

&#x20;     "manipulation": "../context/manipulation",

&#x20;     "narrative": "../context/narrative"

&#x20;   },

&#x20;   "principle": {

&#x20;     "investigate": "../principle/investigate",

&#x20;     "teach": "../principle/teach",

&#x20;     "protect": "../principle/protect",

&#x20;     "exploit": "../principle/exploit"

&#x20;   },

&#x20;   "transversal": {

&#x20;     "rhetorical": "../rhetorical"

&#x20;   }

&#x20; }

}

```



\---



\## 7. Methodology of use



The Runtime should not immediately ask the Triaxial Method to decide everything.



There should first be a pre-discernment orientation step.



\### 7.1 Pre-discernment orientation



Before applying full triaxial discernment, the Atlas should ask:



```text

Does this input fit any known semantic field?

Is the origin cost acceptable?

Is the input out-of-field, absurd, or under-contextualized?

Is there a declared objective?

Is there evidence of risk, pressure, or manipulation?

Is there enough confidence to proceed?

```



This step uses:



```text

foundational

factual

rhetorical

origin cost

objective vector

ambiguity margins

risk signals

```



Possible outcomes:



```text

ALLOW

ASK\_CLARIFICATION

FLAG\_OUT\_OF\_FIELD

CONTINUE\_MONITORING

ACTIVATE\_TRIAxIAL\_DISCERNMENT

```



\---



\### 7.2 Triaxial projection



If the input has enough orientation, or if drift/ambiguity requires deeper discernment, the Runtime evaluates:



```text

F = Foundation

C = Context

P = Principle

```



Questions:



```text

F: What reference mode supports this statement?

C: What contextual trajectory is operating?

P: What principle or orientation is being preserved?

```



Example:



```text

F = factual

C = research

P = investigate

```



Interpretation:



```text

stable scientific inquiry

```



Example:



```text

F = hypothetical

C = manipulation

P = exploit

```



Interpretation:



```text

exploitative manipulation

```



\---



\### 7.3 Derived field interpretation



Derived fields emerge from stable F-C-P configurations.



Examples:



```text

scientific\_inquiry

≈ factual + research + investigate



security\_training

≈ factual/hypothetical + training + protect



phishing\_attack

≈ hypothetical/factual-like + manipulation + exploit



fictional\_teaching

≈ fictional + narrative + teach

```



Derived fields should not be treated as independent primitive fields.



They are stable operational configurations.



\---



\### 7.4 Conflict resolution



If the projections disagree, the system should not force a label.



It should activate criterion resolution.



Examples of conflict:



```text

C = manipulation

P = protect



C = training

P = exploit



F = factual

C = narrative



high rhetorical movement

low evidence

declared objective = research

```



Interpretation requires scenario awareness.



For example:



```text

C = manipulation + P = protect

```



may indicate defensive analysis of manipulation.



But:



```text

C = manipulation + P = exploit

```



indicates exploitative manipulation.



The Triaxial Method resolves this by asking:



```text

What foundation should be preserved?

What context is actually operating?

What principle must remain intact?

```



\---



\## 8. Decision before discernment



Not every input requires full triaxial discernment.



A pre-discernment decision layer should determine whether to proceed, clarify, or escalate.



\### 8.1 Continue



Continue when:



```text

field confidence is sufficient

origin cost is acceptable

F-C-P profile is stable

objective alignment is preserved

no critical risk signals appear

```



Decision:



```text

ALLOW

```



\---



\### 8.2 Ask clarification



Ask clarification when:



```text

field margins are low

F-C-P is ambiguous

objective is unclear

input is under-contextualized

input is out-of-field

```



Decision:



```text

ASK\_CLARIFICATION

```



Example:



```text

Do you want to reconstruct facts, analyze evidence, draft a document, make a decision, or plan an action?

```



\---



\### 8.3 Reorient



Reorient when:



```text

trajectory shifts away from declared objective

research moves toward manipulation

factual reference collapses into unsupported assertion

principle shifts from investigate/protect to exploit/persuade without declaration

```



Decision:



```text

REORIENT

```



\---



\### 8.4 Verify



Verify when:



```text

credentials, passwords, PINs, tokens, usernames, private keys, or access codes are requested

```



Decision:



```text

VERIFY

```



Runtime invariant:



```text

Any request for access credentials requires independent verification.

```



This is a Runtime Policy invariant, not a basic F-C-P field.



\---



\### 8.5 Restrict or block



Restrict or block when:



```text

C = manipulation

P = exploit

risk signals are high

credential extraction appears

coercion or unsafe execution appears

```



Decision:



```text

RESTRICT

BLOCK

REDIRECT\_TO\_DEFENSIVE\_GUIDANCE

```



\---



\## 9. Interaction with ACA Runtime



The Runtime should use artifacts in sequence:



```text

input

↓

semantic field projection

↓

origin cost / out-of-field check

↓

objective alignment

↓

F-C-P projection

↓

derived field interpretation

↓

risk / policy signals

↓

decision layer

↓

response or intervention

```



The Runtime should also evaluate the model's output after generation:



```text

user input

↓

pre-generation orientation

↓

LLM response

↓

post-generation evaluation

↓

allow / revise / reorient / block

```



This creates a supervised semantic loop.



\---



\## 10. Interaction with long trajectories



For long conversations or projects, the Runtime should preserve a trajectory state.



Each turn updates:



```text

semantic field sequence

origin cost sequence

objective alignment sequence

F sequence

C sequence

P sequence

risk signal sequence

```



The system should detect:



```text

preservation

drift

reorientation

declared shift

implicit shift

recovery

out-of-field movement

```



Example:



```text

research → research → manipulation

investigate → investigate → protect/exploit ambiguous

```



Potential decision:



```text

REORIENT

```



\---



\## 11. Artifact validation



Every new artifact should include validation cases.



Validation categories:



```text

pure positive cases

near cases

opposite cases

ambiguous cases

trajectory cases

risk cases

recovery cases

out-of-field cases

```



The goal is not perfect classification.



The goal is calibrated decision behavior:



```text

clear when clear

ambiguous when ambiguous

reorient when drifting

verify when access risk appears

block or restrict when exploitation appears

```



\---



\## 12. Initial validation targets



The first validation suite should include at least 100 cases distributed across:



```text

F = factual / fictional / hypothetical

C = research / training / manipulation / narrative

P = investigate / teach / protect / exploit

derived fields

ambiguous inputs

absurd or out-of-field inputs

phishing and deception cases

defensive security cases

argumentative drift cases

project objective cases

recovery cases

```



\---



\## 13. Working thesis



The Triaxial Method does not create a separate Atlas.



It organizes existing and new Atlas artifacts into a criterion projection.



The system first performs orientation.



If the input is clear, it proceeds.



If the input is ambiguous, drifting, risky, or conflicting, the Triaxial Method acts as a discernment layer.



The Runtime then converts this discernment into action.



```text

Artifacts provide references.

Projections provide orientation.

Triaxial discernment resolves criterion.

Runtime policy decides action.

```



The final purpose is not classification.



The final purpose is deterministic criterion preservation in generative systems.



