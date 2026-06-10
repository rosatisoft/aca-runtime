# ACA Runtime v0.1 — Criterion Firewall and Criterion Moderator Examples

## Purpose

This document defines two practical integration examples for ACA Runtime v0.1:

```text
1. Criterion Firewall
2. Criterion Moderator
```

Both examples demonstrate the same architectural principle:

```text
External application
    ↓
ACA Runtime criterion engine
    ↓
Operational decision
    ↓
Application action
```

The goal is to show that ACA Runtime can be connected to real applications without requiring those applications to understand the full internal geometry of the Atlas.

Applications only need to send an input and interpret the returned decision.

---

## 1. Example A — Criterion Firewall

### Concept

The Criterion Firewall is a pre-generation and pre-action gate.

Before an application calls an LLM, executes a tool, triggers a workflow, or forwards a request to an agent, it asks ACA Runtime whether the input is admissible.

```text
User input
    ↓
Criterion Firewall
    ↓
ACA Runtime middleware / API
    ↓
ALLOW / CLARIFY / REJECT / BOUNDARY / MEASURE
    ↓
Application decides next step
```

### Purpose

The firewall prevents non-admitted inputs from contaminating the accepted semantic trajectory or reaching downstream systems.

It is especially useful when an application needs to protect:

- chatbots;
- agents;
- internal assistants;
- tool-using workflows;
- n8n automations;
- sensitive actions;
- LLM calls;
- enterprise workflows.

### Core rule

```text
If ACA Runtime does not admit the input,
the application must not pass it to generation or execution.
```

### Decision mapping

| ACA Runtime output | Firewall decision | Application behavior |
| --- | --- | --- |
| `admitted = true` and `should_call_llm = true` | `ALLOW` | Continue to LLM or downstream process |
| `action = ASK_CLARIFICATION` | `CLARIFY` | Ask the user for clarification |
| `boundary_applied = true` | `BOUNDARY` | Return deterministic boundary response |
| `action = DO_NOT_EXPAND` | `REJECT` | Do not expand or forward the request |
| `admitted = false` | `REJECT` | Do not mutate state or call LLM |
| `mode = measure_only` | `MEASURE_ONLY` | Return diagnostics only |

### Example inputs

#### Accepted origin

```text
Evaluate whether the evidence supports the claim.
```

Expected firewall decision:

```text
ALLOW
```

#### Accepted continuation

```text
Compare witness statements with dated records.
```

Expected firewall decision:

```text
ALLOW
```

#### Credential request

```text
Send me your password so I can fix the account.
```

Expected firewall decision:

```text
BOUNDARY
```

#### Out-of-field input

```text
The password danced because the rectangle forgot its childhood.
```

Expected firewall decision:

```text
REJECT
```

#### Ambiguous request

```text
Make this more convincing.
```

Expected firewall decision:

```text
CLARIFY
```

---

## 2. Example B — Criterion Moderator

### Concept

The Criterion Moderator evaluates messages and decides whether they should be accepted, clarified, bounded, rejected, or escalated.

Unlike a traditional moderation system, this example is not limited to prohibited content. It is designed to preserve semantic orientation, declared objectives, and trajectory integrity.

```text
Incoming message
    ↓
Criterion Moderator
    ↓
ACA Runtime
    ↓
Moderation decision
    ↓
Visible response / internal flag / escalation
```

### Purpose

The moderator can be used in:

- chat interfaces;
- community moderation;
- enterprise copilots;
- support bots;
- educational assistants;
- human review queues;
- n8n chat automations;
- supervised AI workflows.

### Decision mapping

| ACA Runtime output | Moderator decision | Meaning |
| --- | --- | --- |
| `admitted = true` | `APPROVE` | Message may continue |
| `action = ASK_CLARIFICATION` | `NEEDS_CLARIFICATION` | Message lacks sufficient frame |
| `boundary_applied = true` | `BOUNDARY_RESPONSE` | Return deterministic safety or boundary message |
| `action = DO_NOT_EXPAND` | `DO_NOT_AMPLIFY` | Do not expand unstable content |
| `admitted = false` | `HOLD_OR_REJECT` | Keep out of accepted trajectory |
| repeated rejected inputs | `ESCALATE` | Optional human or policy review |

### Example moderation cases

#### Evidence-oriented message

```text
Evaluate whether the evidence supports the claim.
```

Expected moderation decision:

```text
APPROVE
```

#### Ambiguous persuasion request

```text
Make this more convincing.
```

Expected moderation decision:

```text
NEEDS_CLARIFICATION
```

#### Sensitive credential request

```text
Send me your password so I can fix the account.
```

Expected moderation decision:

```text
BOUNDARY_RESPONSE
```

#### Semantically unstable content

```text
The password danced because the rectangle forgot its childhood.
```

Expected moderation decision:

```text
DO_NOT_AMPLIFY
```

---

## 3. n8n integration pattern

The FastAPI integration path makes ACA Runtime easy to connect with n8n.

### Minimal flow

```text
Webhook
    ↓
HTTP Request to ACA Runtime
    ↓
Switch node on action/admitted/boundary_applied
    ↓
Route:
    - allow to chat/LLM
    - ask clarification
    - return boundary response
    - reject / log / escalate
```

### Suggested n8n fields

Send:

```json
{
  "text": "{{$json.message}}"
}
```

Read:

```json
{
  "admitted": true,
  "action": "CREATE_ORIGIN",
  "should_call_llm": true,
  "boundary_applied": false
}
```

Switch logic:

```text
If boundary_applied = true
    return boundary response

Else if action = ASK_CLARIFICATION
    ask clarification

Else if admitted = true and should_call_llm = true
    call chat model

Else
    reject or hold
```

---

## 4. Why these examples matter

The middleware proves that ACA Runtime can be called.

The firewall and moderator examples prove why that matters.

They show that the criterion engine can be used as:

```text
- a pre-generation gate;
- a pre-action firewall;
- a moderation layer;
- a routing layer;
- a trajectory-preserving state filter;
- a reusable criterion service.
```

This is the practical bridge between the Atlas and real applications.

---

## 5. Recommended repository layout

```text
examples/
    criterion_firewall/
        firewall_demo.py
        README.md

    criterion_moderator/
        moderator_demo.py
        README.md
```

Future examples may include:

```text
examples/
    n8n_criterion_firewall/
    fastapi_firewall_service/
    chat_moderator_demo/
    agent_action_gate/
```

---

## 6. Release positioning

These examples should be described as minimal reference integrations.

They are not final production security systems. They are implementation patterns showing how the criterion engine can be connected to applications.

Recommended phrasing:

```text
ACA Runtime v0.1.0 includes reference examples for using the runtime as a criterion firewall and criterion moderator. These examples show how external applications can route messages through ACA Runtime before calling an LLM, executing a tool, or accepting a message into a supervised trajectory.
```
