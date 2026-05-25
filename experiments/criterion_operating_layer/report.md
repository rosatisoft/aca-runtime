\# Experiment 05 — Criterion Operating Layer v0.1



Status:

Exploratory / incomplete



\## Objective



Test whether a persistent objective vector can guide long-horizon responses without repeatedly injecting the full objective text.



\## Setup



The experiment used:



\- a fixed objective

\- a goal vector derived from the objective

\- conversational turns

\- pre-generation goal alignment

\- candidate generation

\- geometric ranking



\## Observed Result



The system did not successfully preserve the active objective.



Although goal alignment stayed above threshold, the generated responses drifted into generic answers.



Examples:



\- "Include employee wellbeing" produced a generic wellbeing answer instead of integrating wellbeing into the productivity investigation.

\- "Explore philosophical perspectives" produced a generic philosophy overview.

\- "Return to measurable outcomes" requested context again instead of returning to the active project objective.



\## Main Finding



Pre-generation alignment over accumulated context is insufficient.



The accumulated context can mask local objective drift.



Therefore, goal alignment should not be computed only over:



context + current\_turn



because prior context may keep the alignment score artificially high.



\## Architectural Implication



Criterion Operating Layer should evaluate generated outputs, not only user inputs.



A better loop is:



User turn

↓

Generate candidates

↓

Evaluate each candidate against:

\- objective vector

\- semantic field

\- origin cost

\- orientation diagnostics

↓

Select / revise / clarify



\## Conclusion



COL v0.1 did not yet operate as a true objective-preserving layer.



The experiment remains useful because it clarified that objective preservation requires post-generation candidate evaluation or iterative reorientation.

