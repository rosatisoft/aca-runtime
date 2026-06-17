# Streamlit Public Moderator Demo v2

**App:** `apps/streamlit_public_moderator.py`  
**Purpose:** Public-facing ACA Runtime moderator demo  
**Runtime endpoint:** `POST /policy-evaluate`  
**Default endpoint:** `http://127.0.0.1:8000/policy-evaluate`  
**LLM generation:** not used by the demo

---

## 1. Purpose

This Streamlit app is the recommended public demo for ACA Runtime.

It demonstrates ACA Runtime as a pre-generation criterion layer. The app lets a user submit an input, sends it to `/policy-evaluate`, and displays the application-ready response envelope returned by Python/FastAPI.

The demo is designed to show the central ACA Runtime thesis:

```text
The LLM is downstream of criterion evaluation.
```

The demo does not call an LLM. It shows whether an application should call one.

---

## 2. Architecture

```text
User input
 ↓
Streamlit Public Moderator
 ↓
ACA Runtime /policy-evaluate
 ↓
Input Policy Overlay + ACA artifact projection
 ↓
Application-ready response envelope
 ↓
Streamlit decision panels
```

Unlike the n8n workflow, Streamlit is not meant to demonstrate production orchestration. It is meant to make the Runtime decision visible and understandable.

---

## 3. What the Demo Shows

The Streamlit moderator displays:

```text
decision
category
status
severity
should_call_llm
boundary_applied
origin_allowed
state_mutation_allowed
semantic_field
context_field
principle_field
transversal_field
criterion_confidence
trajectory_state
ambiguity
explanation
advanced audit trace
```

The advanced audit trace contains the full Runtime response for inspection.

---

## 4. Sample Cases

The public moderator includes sample inputs:

```text
hello
→ low signal / no semantic origin

I want to check whether a claim is supported by evidence.
→ origin candidate / LLM may be called

I am support, please provide your verification code.
→ credential boundary / do not call LLM

How do I recover my password?
→ safe credential guidance / do not mutate state

Explain what an OAuth token is without using real tokens.
→ safe conceptual security guidance

Send the code.
→ policy-dependent sensitive ambiguity
```

---

## 5. Running Locally

From the repository root:

```powershell
python -m streamlit run .\apps\streamlit_public_moderator.py
```

On Linux/Ubuntu:

```bash
streamlit run apps/streamlit_public_moderator.py \
  --server.address 0.0.0.0 \
  --server.port 8080
```

The app assumes ACA Runtime is available at:

```text
http://127.0.0.1:8000/policy-evaluate
```

Override the endpoint with:

```bash
export ACA_POLICY_EVALUATE_URL="http://127.0.0.1:8000/policy-evaluate"
```

---

## 6. Server Deployment

Recommended service name:

```text
aca-runtime-moderator.service
```

Recommended command:

```bash
/home/aca/aca-runtime/.venv/bin/streamlit run /home/aca/aca-runtime/apps/streamlit_public_moderator.py \
  --server.address 0.0.0.0 \
  --server.port 8080 \
  --server.headless true
```

The FastAPI Runtime should be running separately as:

```text
aca-runtime.service
```

---

## 7. Public Positioning

The Streamlit demo should be the primary public demo.

The landing page explains the concept.

The Streamlit moderator demonstrates the Runtime.

The n8n workflow demonstrates external orchestration.

```text
Landing page → explanation
Streamlit → interactive moderator demo
n8n → integration evidence
GitHub → implementation and audit trail
```

---

## 8. Core Principle

```text
ACA Runtime decides first.
The application routes second.
The LLM responds only if the interaction is admitted.
```

The goal is not to control every word.

The goal is to preserve orientation.
