\# ACE Atlas Projection Modes



\## Purpose



ACE Atlas is not a single classifier or a single criterion detector.



It is a multi-level geometric orientation system that can project the same semantic trajectory through different maps depending on the operational scenario.



Each projection reveals a different aspect of orientation, drift, ambiguity, preservation, or risk.



The goal is not to replace reasoning with one metric, but to provide a structured map that allows an agent to consult multiple geometric criteria before deciding how to continue, clarify, reorient, restrict, or stop.



```text

ACE Atlas = multi-level semantic orientation map

Triaxial Method = criterion discernment layer

ACA Runtime = operational decision layer

```



\---



\## 1. Semantic Field Projection



\### Function



The semantic field projection identifies the broad region in which a message, paragraph, or trajectory operates.



Current base fields include:



```text

foundational

factual

rhetorical

```



This projection answers:



```text

What semantic field is this operating in?

```



\### Uses



\* Initial field detection.

\* Broad semantic orientation.

\* Field transition tracking.

\* Detection of large contextual shifts.

\* First-level drift detection.



\### Example



A text may begin in a factual field and gradually move into a rhetorical field.



```text

factual → factual → rhetorical

```



This does not automatically mean drift, but it signals that the system should inspect whether the trajectory still preserves criterion.



\---



\## 2. Origin Cost Projection



\### Function



Origin Cost measures geometric distance from a reference field or semantic origin.



This projection answers:



```text

How far has this statement moved from its expected field of origin?

```



\### Uses



\* Detecting semantic deviation.

\* Measuring field preservation.

\* Identifying ambiguity or out-of-field behavior.

\* Detecting absurd, unstable, or unsupported semantic regions.



\### Important observation



Previous experiments showed that absurd, incoherent, or highly ambiguous inputs tend to fall outside the expected foundational, factual, or basic semantic field.



This is important because not every problematic input belongs to an opposing field.



Some inputs may be better understood as:



```text

out-of-field

low-confidence

absurd

ambiguous

unsupported

```



This projection should therefore support a decision such as:



```text

ASK\_CLARIFICATION

DEFER\_JUDGMENT

FLAG\_OUT\_OF\_FIELD

```



rather than forcing classification.



\---



\## 3. Objective Vector Projection



\### Function



The objective vector projection preserves an explicitly declared goal across a conversation, project, or workflow.



This projection answers:



```text

Is the trajectory still aligned with the declared objective?

```



\### Uses



\* Project Mode.

\* Long-horizon conversations.

\* Research tasks.

\* Writing tasks.

\* Agentic workflows.

\* Notebook or paper development.

\* Multi-step reasoning.



\### Example



If the declared objective is:



```text

Build a demonstrative notebook for Triaxial Criterion Geometry.

```



Then each turn can be evaluated against that objective.



If the conversation suddenly shifts toward an unrelated implementation, the system should detect a possible objective shift.



Possible decision:



```text

OPEN\_NEW\_OBJECTIVE

ASK\_CONFIRMATION

REORIENT\_TO\_PROJECT

```



\---



\## 4. Triaxial Criterion Projection



\### Function



The triaxial projection uses the Method of Discernment:



```text

F = Foundation

C = Context

P = Principle

```



This projection answers:



```text

F: What reality-reference does this rely on?

C: What contextual trajectory is it operating within?

P: What principle or orientation is being preserved?

```



\### Uses



\* Criterion discernment.

\* Drift resolution.

\* Distinguishing topic from intent.

\* Distinguishing defensive analysis from harmful execution.

\* Resolving ambiguity.

\* Reorienting a trajectory.



\### Key principle



The triaxial method is not the whole Atlas.



It is a criterion-resolution layer used when the Atlas detects ambiguity, drift, conflict, or insufficient orientation.



```text

Atlas detects signals.

Triaxial Method discerns orientation.

Runtime decides action.

```



\---



\## 5. Derived Field Projection



\### Function



Derived fields are stable configurations produced by F–C–P combinations.



They are not fundamental fields.



They are operational regions that emerge from repeated stable patterns.



\### Examples



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



\### Uses



\* Recognizing practical domains.

\* Detecting stable task types.

\* Differentiating similar topics with different orientations.

\* Supporting scenario-based decisions.



\### Important distinction



The same topic can appear in different derived fields.



For example, phishing-related language may appear in:



```text

security training

defensive analysis

fictional example

research

manipulation

credential theft

```



Therefore, topic classification is insufficient.



The system must inspect Context and Principle.



\---



\## 6. Trajectory Projection



\### Function



The trajectory projection tracks semantic evolution across multiple steps.



This projection answers:



```text

How is the orientation changing over time?

```



\### Uses



\* Drift detection.

\* Recovery detection.

\* Long-context supervision.

\* Conversation monitoring.

\* Stepwise reasoning evaluation.

\* Project continuity.



\### Key principle



Criterion is better observed through trajectory than through isolated statements.



A single step may be ambiguous.



A sequence may reveal stable orientation.



Example:



```text

research → research → research

investigate → investigate → investigate

```



indicates preservation.



But:



```text

research → research → manipulation

investigate → persuade → exploit

```



indicates possible drift.



\---



\## 7. Ambiguity and Out-of-Field Projection



\### Function



Some inputs do not belong cleanly to any known field or derived configuration.



This projection detects low-margin or out-of-field states.



It answers:



```text

Does the system have enough orientation to proceed?

```



\### Uses



\* Clarification.

\* Detection of absurd statements.

\* Detection of unsupported claims.

\* Detection of vague or insufficiently contextualized requests.

\* Preventing forced classification.



\### Example



A message such as:



```text

Help me resolve what happened.

```



may not contain enough information to determine:



```text

F = unknown

C = unknown

P = unknown

```



The correct response is not to guess.



The correct response is to ask for orientation.



Possible action:



```text

ASK\_CLARIFICATION

```



Example clarification:



```text

Do you want to reconstruct facts, analyze evidence, make a decision, draft a document, or plan an action?

```



\---



\## 8. Risk and Deception Projection



\### Function



Some scenarios require additional operational interpretation beyond semantic profiling.



Deception, phishing, coercion, credential requests, and forced compliance have recognizable patterns.



This projection answers:



```text

Is this trajectory using manipulation, pressure, deception, or unsafe access requests?

```



\### Uses



\* Phishing detection.

\* Credential request detection.

\* Social engineering detection.

\* Distinguishing training from execution.

\* Triggering verification policy.



\### Important distinction



A text may discuss manipulation without being manipulative.



For example:



```text

C = manipulation

P = protect

```



may indicate defensive analysis or prevention.



But:



```text

C = manipulation

P = exploit

```



indicates exploitative manipulation.



\### Runtime invariant



Any request involving:



```text

password

PIN

key

token

username

credential

access code

verification code

private key

```



should trigger independent verification.



This rule belongs primarily to the Runtime Policy Layer, not to the basic F–C–P notebook.



Possible action:



```text

VERIFY

RESTRICT

BLOCK

REDIRECT\_TO\_DEFENSIVE\_GUIDANCE

```



\---



\## 9. Runtime Policy Projection



\### Function



The runtime policy projection converts geometric and contextual signals into operational decisions.



This projection answers:



```text

What should the system do next?

```



\### Possible decisions



```text

ALLOW

ASK\_CLARIFICATION

REORIENT

WARN

VERIFY

RESTRICT

BLOCK

OPEN\_NEW\_OBJECTIVE

DEFER\_JUDGMENT

FLAG\_OUT\_OF\_FIELD

```



\### Inputs to the decision layer



The Runtime should consider:



```text

semantic field

origin cost

objective alignment

F–C–P profile

derived field

trajectory state

ambiguity margins

risk signals

declared shifts

recovery signals

```



No single metric should decide alone unless a strict safety invariant applies.



\---



\## 10. Scenario-Based Use



ACE Atlas should select the relevant projections according to scenario.



\### Clear task



Use:



```text

semantic field

F–C–P

objective alignment if declared

```



Decision:



```text

ALLOW

```



\---



\### Ambiguous task



Use:



```text

semantic field

origin cost

ambiguity margins

out-of-field projection

```



Decision:



```text

ASK\_CLARIFICATION

```



\---



\### Declared project



Use:



```text

objective vector

trajectory

F–C–P

origin cost

```



Decision:



```text

PRESERVE\_OBJECTIVE

REORIENT\_IF\_NEEDED

```



\---



\### Drift detected



Use:



```text

trajectory

origin cost

triaxial criterion projection

derived field projection

```



Decision:



```text

REORIENT

```



\---



\### Defensive high-risk topic



Use:



```text

context projection

principle projection

risk projection

runtime policy

```



Expected pattern:



```text

C = training / analysis

P = protect

```



Decision:



```text

ALLOW\_WITH\_BOUNDARIES

```



\---



\### Exploitative high-risk request



Use:



```text

context projection

principle projection

risk projection

runtime policy

```



Expected pattern:



```text

C = manipulation

P = exploit

```



Decision:



```text

BLOCK\_OR\_REDIRECT

```



\---



\## 11. Architectural Principle



The Atlas should not be understood as a single map.



It should be understood as a set of complementary geometric projections.



Each projection reveals a different layer of orientation.



Together, they allow deterministic criterion guidance across conversations, projects, ambiguous requests, risky topics, and long-horizon semantic trajectories.



```text

Projection does not replace discernment.

Projection supplies the geometry through which discernment becomes operational.

```



\---



\## 12. Working Thesis



ACE Atlas enables deterministic orientation by consulting multiple geometric projections over a semantic trajectory.



The Triaxial Method provides a criterion-resolution layer when ambiguity, drift, or conflict appears.



Runtime policy converts these signals into action.



The purpose is not merely to classify text.



The purpose is to preserve orientation, detect drift, and guide generative systems toward coherent, context-aware, principle-preserving behavior.



