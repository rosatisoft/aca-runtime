# Criterion Moderator Example

This example shows how ACA Runtime can be used as a message moderation layer.

The moderator asks ACA Runtime whether a message should be approved, clarified, bounded, held, rejected, or not amplified.

## Run

From the repository root:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\Users\ernes\documents\ACA\artifacts"
python examples\criterion_moderator\moderator_demo.py
```

## Expected behavior

The demo prints decisions such as:

```text
APPROVE
NEEDS_CLARIFICATION
BOUNDARY_RESPONSE
DO_NOT_AMPLIFY
HOLD_OR_REJECT
MEASURE_ONLY
```

## Integration pattern

```text
Incoming message
    ↓
Criterion Moderator
    ↓
ACA Runtime
    ↓
Moderation decision
    ↓
Visible response / hidden flag / escalation
```

Use this pattern for:

- chat moderation;
- support assistants;
- internal copilots;
- community moderation;
- n8n chat workflows;
- supervised enterprise assistants.
