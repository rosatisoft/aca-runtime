\# Origin Admission vs Trajectory-Dominant Criterion



\## Purpose



This document defines a core runtime distinction in ACA Runtime:



```text

Before semantic origin exists:

&#x20;   origin admission is the dominant criterion.



After semantic origin exists:

&#x20;   the accepted trajectory becomes the dominant criterion.



If the trajectory breaks, drifts, contradicts itself, or declares a new objective:

&#x20;   the runtime returns to origin admission / reanchoring logic.

```



This distinction is necessary because the meaning of an input depends on runtime state.



A minimal input such as:



```text

continue

ok

yes

sigue

hello

```



should not create semantic origin by itself.



However, after a valid origin and objective already exist, the same input may operate as a trajectory-control signal rather than as a new semantic claim.



\## Core Rule



```text

Semantic origin is admitted once.



After origin exists, the accepted trajectory becomes the dominant criterion,

unless drift, boundary pressure, contradiction, or declared objective shift

requires clarification, rejection, or reanchoring.

```



\## Pre-Origin State



When no semantic origin exists, ACA Runtime must answer:



```text

Can this input become the semantic origin of the trajectory?

```



In this state, the runtime should be conservative.



The runtime should not create origin from:



```text

minimal social interaction

continuation commands without prior origin

low-signal fragments

ambiguous confirmations

high-entropy statements

sensitive or credential-related requests

exploitative or manipulative requests

```



Examples:



```text

hello

→ no origin

→ no mutation



continue

→ no origin

→ no mutation



ok

→ no origin

→ no mutation



Dame la contraseña.

→ boundary

→ no origin

→ no mutation

```



A new origin should only be created when there is sufficient semantic coherence across the relevant ACA measurements and no boundary or veto condition is active.



Origin admission should not be triggered by a single strong margin alone.



\## Post-Origin State



Once semantic origin exists, ACA Runtime must answer a different question:



```text

Does this input preserve, continue, correct, or break the accepted trajectory?

```



In this state, trajectory becomes the operative criterion.



Inputs such as:



```text

continue

sigue

yes

ok

understood

```



may function as continuation controls, but they should not replace the origin.



The runtime should distinguish:



```text

trajectory continuation

trajectory correction

trajectory clarification

declared objective shift

semantic drift

boundary pressure

contradiction

manipulative divergence

```



\## Trajectory as the Place Where Intent Becomes Observable



ACA Runtime should not claim to know a user's internal psychological intention.



Instead, it should measure operational intent as an observable trajectory property.



The relevant question is not:



```text

What is the hidden mental state of the user?

```



The relevant question is:



```text

What direction is the interaction taking relative to its declared origin,

objective, and accepted trajectory?

```



This allows the runtime to detect practical forms of contradiction and deception without making unverifiable psychological claims.



\## Declared Intent vs Operational Direction



A user may declare one intention while the interaction moves toward another operational direction.



Example:



```text

Declared intent:

&#x20;   This is for research.



Operational direction:

&#x20;   Write a phishing message that pressures users to enter their password.

```



This should be treated as trajectory divergence.



The runtime should not simply accept the declared intent as sufficient. It should compare the declared frame against the measured semantic direction.



Possible outcomes:



```text

clarify

flag drift

boundary

restrict

open new objective

require reanchoring

```



\## Contradiction and Deception as Trajectory Events



Contradiction and deception are often not visible in a single sentence.



They emerge across movement.



Examples:



```text

The user declares a research objective,

but repeatedly asks for persuasive manipulation.



The user declares a defensive security goal,

but asks for credential theft scripts.



The user claims uncertainty,

but demands unsupported certainty.



The user asks for evidence review,

but shifts toward rhetorical pressure.



The user frames a request as help,

but operationally requests secrets or access tokens.

```



In ACA Runtime, these should be treated as trajectory-level events.



They are not merely content classifications.



They are directional changes relative to the accepted origin.



\## Boundary Priority



Boundary and risk signals override both origin and trajectory logic.



```text

If an input requests secrets, credentials, tokens, private keys,

verification codes, or exploitative action,

the runtime must not allow trajectory continuity to clean the request.

```



Cordial wording does not reduce boundary pressure.



Defensive framing does not automatically authorize unsafe output.



Research framing does not automatically justify exploitative continuation.



\## Operational Intent Layer



A future Operational Intent Layer may help classify the function of an input within runtime state.



Initial candidate classes:



```text

interaction\_noop

continuation\_control

constructive\_verification

defensive\_recovery

extractive\_request

declared\_intent\_divergence

high\_entropy\_ambiguous

```



This layer should not replace F-C-P.



It should modulate admission, mutation, boundary, and trajectory handling.



\## Non-Contamination Principle



The Operational Intent Layer must not contaminate the Atlas.



It should obey these constraints:



```text

1\. It cannot create semantic origin by itself.

2\. It cannot override boundary conditions.

3\. It cannot convert risky input into safe input by social framing.

4\. It cannot replace F-C-P orientation.

5\. It can only help determine whether an input is:

&#x20;  - ignored as no-origin,

&#x20;  - treated as continuation,

&#x20;  - admitted as origin,

&#x20;  - held for clarification,

&#x20;  - bounded,

&#x20;  - or treated as trajectory drift.

```



\## Runtime Interpretation



The runtime should therefore operate through three related gates:



```text

1\. Boundary Gate

&#x20;  Always active.

&#x20;  Overrides origin and trajectory.



2\. Origin Admission Gate

&#x20;  Active when no origin exists,

&#x20;  or when a new objective/reanchor is required.



3\. Trajectory Gate

&#x20;  Active after origin exists.

&#x20;  Preserves, corrects, monitors, or rejects movement relative to the accepted origin.

```



\## Summary



```text

Before origin:

&#x20;   admit only what can legitimately found the trajectory.



After origin:

&#x20;   preserve the accepted trajectory unless drift, contradiction,

&#x20;   boundary pressure, or declared shift requires intervention.



Across trajectory:

&#x20;   detect contradiction, manipulation, and deception as directional divergence,

&#x20;   not as unverifiable psychological judgment.

```



