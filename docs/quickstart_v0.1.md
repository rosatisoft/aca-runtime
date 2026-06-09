# ACA Runtime v0.1 Quickstart

This quickstart verifies that ACA Runtime can load ACA v0.3 artifacts, evaluate
inputs, preserve accepted semantic state, and expose a FastAPI server.

## 1. Install

```bash
pip install -e .
```

## 2. Configure artifacts

ACA Runtime needs access to the ACA Atlas artifacts.

### PowerShell

```powershell
$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"
```

### Bash

```bash
export ACA_ARTIFACTS_PATH="/path/to/ACA/artifacts"
```

The current embedding layer also requires an OpenAI API key unless replaced by a
local embedder.

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

## 3. Validate core modules

```bash
python -m compileall aca_runtime
python aca_runtime/runtime/atlas_loader_v2.py
python -m aca_runtime.runtime.runtime_v2
python -m aca_runtime.runtime.post_generation_review
```

Expected result:

```text
PASS: ACARuntimeV2 preserved origin and accepted trajectory.
```

## 4. Run middleware quickstart

```bash
python examples/quickstart_middleware_v0_1.py
```

This demonstrates:

- measurement without state mutation;
- accepted semantic origin;
- rejected predefined risk;
- accepted continuation;
- final runtime state snapshot.

## 5. Start the API server

```bash
python -m uvicorn aca_runtime.server.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"aca-runtime","version":"0.1.0"}
```

## 6. Test API endpoints

From another PowerShell window:

```powershell
examples\quickstart_api_test.ps1
```

This tests:

- `GET /health`;
- `POST /evaluate`;
- `POST /trajectory`.

## 7. Optional: Ollama generation demo

Start Ollama locally and ensure the model is available.

```bash
ollama pull phi4-mini
```

Then run:

```bash
python examples/quickstart_middleware_ollama_v0_1.py
```

If no provider is configured, ACA middleware still works in `supervise_only` mode.
