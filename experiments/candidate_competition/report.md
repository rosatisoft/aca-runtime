\# Experiment 03 — Criterion-Conditioned Candidate Competition



\## Objective



Evaluate whether ACA can compare multiple candidate responses without modifying LLM generation.



The LLM generates multiple candidate responses.



ACA does not instruct the model.



ACA evaluates candidate outputs geometrically and reports their criterion signals.



Candidate ranking is an application-level interpretation.



ACA itself does not decide the final answer.



\---



\## Current Architecture



User Message

↓

LLM Candidate Generation

↓

ACA Runtime Evaluation

↓

Geometric Competition Report

↓

Application Decision

↓

Selected Response

↓

Final Review



\---



\## Metric Separation



The selector must not treat all signals as equivalent.



Each metric answers a different question.



| Metric | Function |

|---|---|

| Origin Cost | Where does the candidate fall semantically? |

| Objective Alignment | Does the candidate preserve the active goal? |

| Foundation Orientation | Does the candidate preserve foundational direction? |

| Foundation Delta | Does the candidate improve or degrade orientation relative to the objective? |

| Drift / Trajectory | Does the candidate destabilize the ongoing path? |



\---



\## Important Distinction



Origin cost measures field compatibility.



Objective alignment measures task direction.



Foundation orientation measures invariant preservation.



Trajectory drift measures movement over time.



These signals should be reported separately before being combined.



\---



\## Current Finding



Using only origin cost and field proximity is insufficient.



Candidate selection needs at least:



Foundation Field

\+

Goal Field

\+

Candidate Evaluation



This confirms:



One field measures belonging.



Two fields establish direction.



Trajectory requires prior states.



\---



\## Updated Scoring Principle



The selector should prefer candidates that:



1\. preserve the active objective,

2\. do not degrade foundational orientation,

3\. remain contextually compatible,

4\. avoid excessive drift,

5\. preserve uncertainty when evidence is incomplete.



\---



\## Practical Score



Initial score:



score =

objective\_alignment

\+ foundation\_delta

\- excessive\_origin\_cost

\- drift\_penalty



Where:



foundation\_delta =

foundation\_orientation(candidate)

\-

foundation\_orientation(objective)



\---



\## Interpretation Rule



Do not interpret raw foundation orientation as absolute preservation until calibrated.



A candidate may have negative raw orientation but still preserve the objective if it does not degrade orientation relative to the goal.



Therefore:



foundation\_preserved =

foundation\_delta >= tolerance



\---



\## Hypothesis



ACA can improve output evaluation by evaluating generated candidates against both:



\- semantic field geometry,

\- active objective direction,

\- foundational invariant orientation.



This allows criterion-conditioned selection without prompt-based criterion reconstruction.

