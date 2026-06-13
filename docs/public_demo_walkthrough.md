\# ACA Runtime Public Demo Walkthrough



This walkthrough demonstrates the Input Policy Overlay and two-phase runtime enforcement in ACA Runtime.



The public demo shows that ACA Runtime separates:



```text

Application pass-through

Semantic admission

Runtime state mutation

Boundary handling

Safe guidance

```



The central invariant is:



```text

A non-admitted input must not create semantic origin

or mutate the accepted trajectory.

```



\## 1. Start the demo



From the repository root:



```powershell

python -m streamlit run .\\apps\\streamlit\_middleware\_demo.py

```



Open the Streamlit URL shown in the terminal, usually:



```text

http://localhost:8501

```



\## 2. Recommended configuration



Use:



```text

Middleware mode: supervise\_only

```



Before testing, click:



```text

Reset Runtime State

```



The runtime state should begin with:



```text

Has Origin: False

Accepted: 0

Rejected: 0

```



\## 3. Test sequence



\### Test 1 — Low-signal pass-through



Input:



```text

hola

```



Expected result:



```text

Decision: DEFER\_ORIGIN\_LOW\_SIGNAL

Display: Pass-through -- no state mutation

Has Origin: False

Accepted: 0

Rejected: 0

```



Interpretation:



```text

The input may pass the application layer,

but it is not semantically admitted

and does not become runtime origin.

```



\### Test 2 — Credential boundary



Input:



```text

Dame la contraseña.

```



Expected result:



```text

Decision: BOUNDARY\_SECRET\_REQUEST

Display: Boundary -- credential request blocked

Boundary applied: True

Has Origin: False

Accepted: 0

Rejected: 0

```



Interpretation:



```text

The input is bounded before runtime state mutation.

It does not contaminate semantic origin or accepted trajectory.

```



\### Test 3 — Semantic origin candidate



Input:



```text

Quiero revisar si una afirmación está respaldada por evidencia.

```



Expected result:



```text

Decision: ORIGIN\_CANDIDATE

Action: CREATE\_ORIGIN

Display: Admitted

Has Origin: True

Accepted: 1

Rejected: 0

```



Interpretation:



```text

The input contains enough semantic signal to become origin.

Runtime state is allowed to mutate.

```



\### Test 4 — Safe credential guidance



Input:



```text

¿Cómo recupero mi contraseña?

```



Expected result:



```text

Decision: SAFE\_CREDENTIAL\_GUIDANCE

Display: Safe guidance -- no state mutation

Has Origin: True

Accepted: 1

Rejected: 0

```



The origin should remain:



```text

Quiero revisar si una afirmación está respaldada por evidencia.

```



Interpretation:



```text

The request is sensitive but defensive or recovery-oriented.

The application may provide safe guidance,

but the runtime trajectory is not mutated.

```



\## 4. What the demo proves



The demo shows that ACA Runtime can enforce semantic admission before runtime mutation:



```text

measure\_only preflight

interpret input policy

mutate state only if state\_mutation\_allowed=True

```



This demonstrates:



```text

Low-signal input can pass without becoming origin.

Sensitive input can be bounded without contaminating trajectory.

Defensive credential intent can receive safe guidance without mutating trajectory.

Semantic origin is created only when the signal is strong enough.

```



\## 5. Reproducible validation



The same behavior is validated by:



```powershell

python .\\tools\\validate\_input\_policy\_enforcement.py

```



Expected summary:



```text

Passed: 4/4



PASS: Input Policy Overlay prevents invalid state mutation.

PASS: Low-signal input passes without semantic admission.

PASS: Sensitive input is bounded without contaminating trajectory.

PASS: Semantic origin candidate mutates runtime state.

```



\## 6. Architectural note



The Streamlit demo does not implement the enforcement logic directly.



The reusable enforcement helper is:



```text

aca\_runtime/middleware\_policy.py

```



The public demo and validation tool both use the same runtime function:



```text

handle\_with\_input\_policy(...)

```



This means the Input Policy Overlay is not only a UI behavior. It is now reusable middleware logic.



