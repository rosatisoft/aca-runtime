# ACA Runtime Artifacts Bundles

This folder contains versioned ACA artifact bundles for reproducible ACA Runtime testing.

## Included bundle

```text
aca_artifacts_v0.3_runtime_bundle.zip
```

This bundle is a frozen ACA v0.3 runtime snapshot.

It is intended for:

- quickstart testing;
- Streamlit demo testing;
- FastAPI /evaluate testing;
- n8n integration tests;
- Criterion Firewall and Criterion Moderator examples;
- reproducible public experiments.

## Scope

The bundle is not a universal criterion map.

It is a public test artifact set. For domain-specific use, derived artifacts should be generated from the ACA repository.

## Install

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_sample_artifacts.ps1
```

Then validate:

```powershell
python -m aca_runtime.runtime.atlas_loader_v2
```
