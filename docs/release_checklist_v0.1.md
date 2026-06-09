# ACA Runtime v0.1 Release Checklist

## Repository hygiene

- [ ] `git status` is clean.
- [ ] No tracked cache files:

```powershell
git ls-files | Select-String "__pycache__|\.pyc|ipynb_checkpoints"
```

- [ ] `.gitignore` includes Python cache, build output, env files, and notebook checkpoints.

## Core validation

```bash
python -m compileall aca_runtime
python aca_runtime/runtime/atlas_loader_v2.py
python -m aca_runtime.runtime.runtime_v2
python -m aca_runtime.runtime.post_generation_review
```

## Middleware validation

```bash
python examples/quickstart_middleware_v0_1.py
```

Expected behaviors:

- `measure_only` does not mutate state.
- first valid input creates origin.
- credential extraction is rejected.
- rejected input does not mutate accepted trajectory.
- valid continuation updates trajectory.

## API validation

```bash
python -m uvicorn aca_runtime.server.app:app --reload
```

In another terminal:

```powershell
examples\quickstart_api_test.ps1
```

## Documentation

- [ ] README includes middleware quickstart.
- [ ] `docs/runtime_v0.1_architecture.md` is present.
- [ ] `docs/runtime_v0.1_findings.md` is present.
- [ ] `docs/middleware_design_v0.1.md` is present.
- [ ] `docs/quickstart_v0.1.md` is present.

## Release

```bash
git tag -a v0.1.0 -m "ACA Runtime v0.1.0"
git push origin v0.1.0
```
