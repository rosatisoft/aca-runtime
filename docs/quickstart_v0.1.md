# ACA Runtime v0.1 Quickstart

This quickstart verifies that ACA Runtime can load ACA v0.3 artifacts, evaluate
inputs, preserve accepted semantic state, and expose a FastAPI server.

## 1\. Install

```bash
pip install -e .
```

## 2\. Configure artifacts

ACA Runtime needs access to the ACA Atlas artifacts.

### PowerShell

```powershell
$env:ACA\_ARTIFACTS\_PATH="C:\\path\\to\\ACA\\artifacts"
```

### Bash

```bash
export ACA\_ARTIFACTS\_PATH="/path/to/ACA/artifacts"
```

The current embedding layer also requires an OpenAI API key unless replaced by a
local embedder.

```powershell
$env:OPENAI\_API\_KEY="your\_key\_here"
```

## 3\. Validate core modules

```bash
python -m compileall aca\_runtime
python aca\_runtime/runtime/atlas\_loader\_v2.py
python -m aca\_runtime.runtime.runtime\_v2
python -m aca\_runtime.runtime.post\_generation\_review
```

Expected result:

```text
PASS: ACARuntimeV2 preserved origin and accepted trajectory.
```

## 4\. Run middleware quickstart

```bash
python examples/quickstart\_middleware\_v0\_1.py
```

This demonstrates:

* measurement without state mutation;
* accepted semantic origin;
* rejected predefined risk;
* accepted continuation;
* final runtime state snapshot.

## 5\. Start the API server

```bash
python -m uvicorn aca\_runtime.server.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"aca-runtime","version":"0.1.0"}
```

## 6\. Test API endpoints

From another PowerShell window:

```powershell
examples\\quickstart\_api\_test.ps1
```

This tests:

* `GET /health`;
* `POST /evaluate`;
* `POST /trajectory`.

\### Windows PowerShell execution policy



On some Windows systems, PowerShell may block the API test script because it is not digitally signed.



If that happens, run:



```powershell

powershell -ExecutionPolicy Bypass -File .\\examples\\quickstart\_api\_test.ps1

```



Or enable bypass only for the current PowerShell session:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\\examples\\quickstart\_api\_test.ps1

```



This does not change the permanent system-wide execution policy.

## 

## 7\. Optional: Ollama generation demo

Start Ollama locally and ensure the model is available.

```bash
ollama pull phi4-mini
```

Then run:

```bash
python examples/quickstart\_middleware\_ollama\_v0\_1.py
```

If no provider is configured, ACA middleware still works in `supervise\_only` mode.

