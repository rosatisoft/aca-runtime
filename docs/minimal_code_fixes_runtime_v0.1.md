# ACA Runtime v0.1 Minimal Code Fixes

These are the minimum code changes recommended before preparing the v0.1.0 release.

---

## 1. Remove tracked Python cache file

A `.pyc` file was already tracked before `.gitignore` rules were in place.

```powershell
git rm --cached aca_runtime/__pycache__/__init__.cpython-314.pyc
git commit -m "Remove tracked Python cache file"
git push
```

Verify:

```powershell
git ls-files | Select-String "__pycache__|\.pyc|ipynb_checkpoints"
```

Expected: no output.

---

## 2. Fix duplicate dataclass decorator

File:

```text
aca_runtime/runtime/supervised_generation.py
```

Current:

```python
@dataclass
@dataclass
class SupervisedGenerationResult:
```

Replace with:

```python
@dataclass
class SupervisedGenerationResult:
```

---

## 3. Remove unreachable return

File:

```text
aca_runtime/runtime/generation_conditioning.py
```

The function `build_minimal_prompt()` contains a second `return f"""..."""` after the first return. Remove the unreachable second return block.

---

## 4. Unify artifact path handling

Current code contains local Windows paths such as:

```text
C:\Users\ernes\documents\ACA\artifacts
C:\Users\ernes\documents\aca\artifacts
```

Recommended approach:

1. Accept `artifacts_root` explicitly whenever possible.
2. Support environment variable:

```text
ACA_ARTIFACTS_PATH
```

3. If neither is provided, fail clearly with a helpful error instead of silently assuming a local developer path.

Suggested helper:

```python
import os
from pathlib import Path


def resolve_artifacts_root(artifacts_root: str | None = None) -> Path:
    value = artifacts_root or os.getenv("ACA_ARTIFACTS_PATH")

    if not value:
        raise ValueError(
            "Missing artifacts root. Pass artifacts_root or set ACA_ARTIFACTS_PATH."
        )

    path = Path(value)

    if not path.exists():
        raise FileNotFoundError(f"Artifacts root not found: {path}")

    return path
```

---

## 5. Keep Runtime v0.1 versioning

Keep package/runtime version as:

```text
0.1.0
```

ACA is v0.3, but ACA Runtime is entering its first formal release stage.

Recommended label:

```text
ACA Runtime v0.1.0 — Pre-Reasoning Criterion Gate and Supervised Generation Layer
```

---

## 6. Recommended validation commands

After edits:

```powershell
python -m compileall aca_runtime
python examples/test_artifacts_loader.py
python examples/test_runtime_report.py
python examples/test_trajectory_runtime.py
python tools/validate_runtime_v2_precondition_cases.py
python tools/validate_supervised_generation_flow.py
python tools/validate_post_generation_review.py
```

Then:

```powershell
git status
git add README.md docs/runtime_v0.1_architecture.md docs/runtime_v0.1_findings.md aca_runtime/runtime/supervised_generation.py aca_runtime/runtime/generation_conditioning.py aca_runtime/runtime/atlas_loader_v2.py aca_runtime/server/app.py
git commit -m "Prepare ACA Runtime v0.1 architecture and minimal fixes"
git push
```
