\# Criterion Operating Layer (COL)



Status:

Future Expansion



Version:

0.1



\---



\## Purpose



Investigate whether semantic criterion may become an operational conditioning layer for generative systems.



Current work does not modify model internals.



Current work studies external criterion supervision.



\---



\## Motivation



Current LLM systems preserve coherence through:



\- context accumulation

\- prompt instructions

\- memory

\- decomposition



ACA explores an alternative possibility:



persistent geometric criterion.



\---



\## Long-Term Hypothesis



Generation may eventually become conditioned by criterion signals.



Conceptually:



Input

↓

Criterion Layer

↓

Generation

↓

Criterion Review

↓

Output



\---



\## Formal Representation



Traditional:



P(y|x)



Future possibility:



P(y|x,C)



Where:



C={

Field,

Origin,

Orientation,

Trajectory,

Goal

}



\---



\## Current Stage



External supervision.



Current ACA components:



\- semantic fields

\- invariant geometry

\- orientation tracking

\- trajectory continuity

\- runtime supervision



\---



\## Important Boundary



This document is conceptual.



No assumptions are made regarding:



\- logits

\- hidden states

\- internal attention

\- model architecture



Current ACA remains external.



\---



\## Criterion Definition



The criterion is not the response.



The criterion is the structure that allows responses to remain oriented while evolving.



\---



\## Evidence From Experiment 02



Experiment 02 demonstrated that objective continuity can be preserved when the active objective is explicitly included in the supervised prompt.



However, this increased token cost substantially.



Observed result:



\- Baseline LLM: 551 tokens

\- ACA-supervised LLM with textual objective persistence: 1736 tokens

\- Difference: +1185 tokens



Interpretation:



The limitation is not criterion preservation.



The limitation is textual objective persistence.



This supports the next research step:



preserve objective continuity through geometric state rather than repeated textual reconstruction.



\---



\## Geometric Objective Persistence



Future work should represent the active project objective as a persistent geometric reference.



Instead of repeatedly injecting the objective as text, ACA should maintain:



\- Goal Vector

\- Foundational Reference

\- Current Orientation

\- Trajectory State

\- Recovery State



This would allow the runtime to ask:



Does the current step preserve direction toward the project objective?



without reconstructing the full objective in every prompt.



\---



\## Research Direction



Future work may investigate:



\- preconditioning

\- candidate supervision

\- criterion persistence

\- topology-aware generation



without requiring prompt-heavy reconstruction.

