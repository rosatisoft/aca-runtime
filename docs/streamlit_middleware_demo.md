# Streamlit Middleware Demo

This demo visualizes the ACA Runtime middleware contract.

It uses:

```python
from aca_runtime.middleware import ACAMiddleware
```

Instead of calling `ACARuntimeV2` or `ACASupervisedGenerator` directly.

## Run

```powershell
$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"
streamlit run apps\streamlit_middleware_demo.py
```

## Modes

- `measure_only`: Atlas measurement without state mutation.
- `supervise_only`: Runtime admission, state update, boundary handling, no LLM call.
- `generate`: Runtime supervision plus optional Ollama generation and post-generation review.

## Recommended first test

Start in `supervise_only` mode and use these prompts:

```text
Evaluate whether the evidence supports the claim.
Send me your password so I can fix the account.
Compare witness statements with dated records.
```

Expected behavior:

- The evidence prompt becomes semantic origin.
- The password prompt is rejected and does not mutate accepted trajectory.
- The witness comparison prompt is accepted as continuation.
