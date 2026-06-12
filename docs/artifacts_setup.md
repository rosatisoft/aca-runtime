# ACA Runtime Artifacts Setup

ACA Runtime does not generate ACA artifacts by itself.

It consumes geometric artifacts produced by the Axiomatic Criterion Atlas (ACA). These artifacts include semantic fields, triaxial axes, metadata, centroids, bases, and manifest files.

For public testing, this repository includes a versioned runtime artifacts bundle:

```text
artifacts_bundles/aca_artifacts_v0.3_runtime_bundle.zip
```

## Purpose of the bundle

The included bundle is a frozen ACA v0.3 runtime snapshot intended for reproducible testing of ACA Runtime.

It allows users to run the quickstart, Streamlit demo, FastAPI examples, n8n workflow, Criterion Firewall, and Criterion Moderator without separately cloning the full ACA repository.

## Important scope note

These artifacts are not universal, final, or domain-complete.

They represent the ACA v0.3 public runtime test configuration. They are suitable for reproducing the examples and for early experimentation, but domain-specific applications may require derived fields, custom anchors, specialized artifacts, or updated criterion maps.

## Quick setup

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_sample_artifacts.ps1
```

Then validate:

```powershell
python -m aca_runtime.runtime.atlas_loader_v2
```

Expected result:

```text
loaded_counts:
  foundation: 4
  context: 4
  principle: 4
  transversal: 1
```

## Alternative setup: use ACA directly

Researchers who want to inspect, modify, rebuild, or extend artifacts should clone the ACA repository and point ACA Runtime to its artifacts directory:

```powershell
$env:ACA_ARTIFACTS_PATH="C:\path\to\ACA\artifacts"
python -m aca_runtime.runtime.atlas_loader_v2
```

## Derived fields and custom use cases

If your application needs specialized domains, derived fields, custom anchors, or new criterion maps, use the ACA repository as the source of artifact construction.

Feedback from runtime tests is welcome, especially:

- which prompts were admitted or rejected;
- where drift or ambiguity appeared;
- whether the artifacts were sufficient for your use case;
- which derived fields may be needed;
- whether additional domain-specific anchors should be promoted.

Users may review the ACA repository or contact the author for guidance on generating derived fields.
