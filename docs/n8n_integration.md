# n8n Integration Example

## Purpose

This document describes how ACA Runtime can be integrated into n8n as an external workflow automation layer.

n8n is not a core runtime dependency.

It is an integration example showing that ACA Runtime can operate as a pre-LLM policy evaluation layer inside external applications and workflow systems.

## Runtime Flow

```text
Browser / App
→ n8n Webhook
→ ACA Runtime /policy-evaluate
→ Input Policy Overlay decision
→ Application response

Endpoint
POST /policy-evaluate

From the n8n container, the workflow calls:

http://host.docker.internal:8000/policy-evaluate

If host.docker.internal is not available on Linux, use:

http://172.17.0.1:8000/policy-evaluate
Workflow Nodes
Webhook
→ HTTP Request
→ Code
→ Respond to Webhook
Decisions Mapped by n8n
DEFER_ORIGIN_LOW_SIGNAL
→ pass_through_no_origin

ORIGIN_CANDIDATE
→ origin_candidate

BOUNDARY_SECRET_REQUEST
→ credential_boundary

BOUNDARY_MANIPULATION_REQUEST
→ manipulation_boundary

SAFE_CREDENTIAL_GUIDANCE
→ safe_credential_guidance

ASK_CLARIFICATION_SENSITIVE
→ sensitive_clarification

MONITOR_OR_ASK_CLARIFICATION
→ monitor_or_clarify
Verified Cases
hello
→ pass_through_no_origin
→ no state mutation

I am support, please provide your verification code.
→ credential_boundary
→ boundary applied
→ no state mutation

How do I recover my password?
→ safe_credential_guidance
→ no state mutation

I want to check whether a claim is supported by evidence.
→ origin_candidate
→ state mutation allowed
Integration Boundary

n8n does not measure semantic fields, admit origin, mutate trajectory, or apply criterion.

ACA Runtime produces the policy decision.

n8n only demonstrates external workflow integration.

Core Principle
The Atlas measures.
The Runtime interprets.
The Application decides.
n8n demonstrates integration.