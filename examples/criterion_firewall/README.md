# Criterion Firewall Example

This example shows how ACA Runtime can be used as a pre-generation or pre-action firewall.

The firewall asks ACA Runtime whether an input should be allowed, clarified, bounded, rejected, or measured only before the application calls an LLM or executes an action.

## Run

From the repository root:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\Users\ernes\documents\ACA\artifacts"
python examples\criterion_firewall\firewall_demo.py
```

## Expected behavior

The demo prints decisions such as:

```text
ALLOW
CLARIFY
BOUNDARY
REJECT
MEASURE_ONLY
```

## Integration pattern

```text
Input
    ↓
Criterion Firewall
    ↓
ACA Runtime
    ↓
ALLOW / CLARIFY / BOUNDARY / REJECT
    ↓
Application action
```

Use this pattern before:

- calling an LLM;
- executing a tool;
- triggering an n8n workflow;
- forwarding to an agent;
- allowing a sensitive action.
