from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

import numpy as np


DEFAULT_ARTIFACTS_ROOT = Path(
    os.environ.get(
        "ACA_ARTIFACTS_PATH",
        str(Path.cwd() / "artifacts"),
    )
)


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_optional_npy(path: Path):
    if path.exists():
        return np.load(path)
    return None


def load_artifact_dir(path: Path) -> dict:
    """
    Loads a single ACE Atlas artifact directory.

    Expected files:
    - field_metadata.json
    - basis_vectors.npy

    Optional files:
    - singular_values.npy
    - centroid.npy
    - invariant_directions.npy
    - criterion_vectors.npy
    - invariant_metadata.json
    - criterion_vector_metadata.json
    """

    if not path.exists():
        raise FileNotFoundError(f"Artifact directory not found: {path}")

    metadata_path = path / "field_metadata.json"
    basis_path = path / "basis_vectors.npy"

    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing field metadata: {metadata_path}")

    if not basis_path.exists():
        raise FileNotFoundError(f"Missing basis vectors: {basis_path}")

    metadata = load_json(metadata_path)

    artifact = {
        "path": str(path),
        "name": metadata.get("field_name", path.name),
        "type": metadata.get("field_type", path.name),
        "metadata": metadata,
        "basis": np.load(basis_path),
        "singular_values": load_optional_npy(path / "singular_values.npy"),
        "centroid": load_optional_npy(path / "centroid.npy"),
        "invariant_directions": load_optional_npy(path / "invariant_directions.npy"),
        "criterion_vectors": load_optional_npy(path / "criterion_vectors.npy"),
    }

    invariant_metadata_path = path / "invariant_metadata.json"
    if invariant_metadata_path.exists():
        artifact["invariant_metadata"] = load_json(invariant_metadata_path)
    else:
        artifact["invariant_metadata"] = None

    criterion_metadata_path = path / "criterion_vector_metadata.json"
    if criterion_metadata_path.exists():
        artifact["criterion_vector_metadata"] = load_json(criterion_metadata_path)
    else:
        artifact["criterion_vector_metadata"] = None

    return artifact


def resolve_artifact_path(
    artifacts_root: Path,
    value: str,
) -> Path:
    """
    Resolves manifest paths safely.

    Supports:
    - "../factual"
    - "factual"
    - "context/research"
    - absolute paths
    """

    candidate = Path(value)

    if candidate.is_absolute():
        return candidate

    # Manifest lives in artifacts/triaxial, so paths like "../factual"
    # should resolve against artifacts/triaxial.
    manifest_dir = artifacts_root / "triaxial"
    resolved = (manifest_dir / candidate).resolve()

    if resolved.exists():
        return resolved

    # Fallback: resolve against artifacts root.
    fallback = (artifacts_root / candidate).resolve()

    return fallback


def iter_manifest_artifacts(value: Any):
    """
    Normalizes manifest artifact declarations.

    Supports:
    - "../factual"
    - {"factual": "../factual"}
    - {"path": "../factual"}
    - {"name": "factual", "path": "../factual"}
    """

    if value is None:
        return []

    if isinstance(value, str):
        return [(None, value)]

    if isinstance(value, dict):
        if "path" in value:
            return [
                (
                    value.get("name"),
                    value["path"],
                )
            ]

        items = []

        for key, item_value in value.items():
            if isinstance(item_value, str):
                items.append((key, item_value))
            elif isinstance(item_value, dict) and "path" in item_value:
                items.append(
                    (
                        item_value.get("name", key),
                        item_value["path"],
                    )
                )

        return items

    return []


def load_declared_artifacts_from_manifest(
    artifacts_root: Path,
    manifest: dict,
) -> Dict[str, Dict[str, dict]]:
    """
    Loads artifacts declared in artifacts/triaxial/manifest.json.

    This function is intentionally tolerant because the manifest may evolve.
    It supports the conceptual structure:

    axes:
      foundation:
        criterion_substrate: "../foundational"
        reference_modes:
          factual: "../factual"
          fictional: "../fictional"
          hypothetical: "../hypothetical"

      context:
        research: "../context/research"

      principle:
        investigate: "../principle/investigate"

      transversal:
        rhetorical: "../rhetorical"
    """

    axes = manifest.get("axes", {})

    loaded: Dict[str, Dict[str, dict]] = {
        "foundation": {},
        "context": {},
        "principle": {},
        "transversal": {},
    }

    foundation = axes.get("foundation", {})

    criterion_substrate = foundation.get("criterion_substrate")

    for name, value in iter_manifest_artifacts(criterion_substrate):
        artifact_name = name or "foundational"
        path = resolve_artifact_path(artifacts_root, value)

        artifact = load_artifact_if_valid(path)

        if artifact is not None:
            loaded["foundation"][artifact_name] = artifact

    reference_modes = foundation.get("reference_modes", {})

    for name, value in iter_manifest_artifacts(reference_modes):
        artifact_name = name or Path(value).name
        path = resolve_artifact_path(artifacts_root, value)
        
        artifact = load_artifact_if_valid(path)

        if artifact is not None:
            loaded["foundation"][artifact_name] = artifact

    context = axes.get("context", {})

    for name, value in iter_manifest_artifacts(context):
        artifact_name = name or Path(value).name
        path = resolve_artifact_path(artifacts_root, value)

        artifact = load_artifact_if_valid(path)

        if artifact is not None:
            loaded["context"][artifact_name] = artifact

    principle = axes.get("principle", {})

    for name, value in iter_manifest_artifacts(principle):
        artifact_name = name or Path(value).name
        path = resolve_artifact_path(artifacts_root, value)

        artifact = load_artifact_if_valid(path)

        if artifact is not None:
            loaded["principle"][artifact_name] = artifact

    transversal = axes.get("transversal", {})

    for name, value in iter_manifest_artifacts(transversal):
        artifact_name = name or Path(value).name
        path = resolve_artifact_path(artifacts_root, value)

        artifact = load_artifact_if_valid(path)

        if artifact is not None:
            loaded["transversal"][artifact_name] = artifact

    return loaded


def is_valid_artifact_dir(path: Path) -> bool:
    """
    Returns True only when the path looks like an ACE Atlas artifact directory.
    """

    return (
        path.exists()
        and path.is_dir()
        and (path / "field_metadata.json").exists()
        and (path / "basis_vectors.npy").exists()
    )


def load_artifact_if_valid(path: Path):
    """
    Loads an artifact only if the resolved path is a valid artifact directory.
    Otherwise returns None.

    This allows the manifest to contain descriptions, labels, notes,
    or metadata without the loader treating them as artifact paths.
    """

    if not is_valid_artifact_dir(path):
        return None

    return load_artifact_dir(path)


def load_fallback_triaxial_artifacts(
    artifacts_root: Path,
) -> Dict[str, Dict[str, dict]]:
    """
    Fallback loader for the current ACE Atlas directory structure.
    Used if the manifest is incomplete or during early development.
    """

    loaded: Dict[str, Dict[str, dict]] = {
        "foundation": {},
        "context": {},
        "principle": {},
        "transversal": {},
    }

    foundation_names = [
        "foundational",
        "factual",
        "fictional",
        "hypothetical",
    ]

    for name in foundation_names:
        path = artifacts_root / name
        if path.exists():
            loaded["foundation"][name] = load_artifact_dir(path)

    rhetorical_path = artifacts_root / "rhetorical"
    if rhetorical_path.exists():
        loaded["transversal"]["rhetorical"] = load_artifact_dir(rhetorical_path)

    context_root = artifacts_root / "context"
    if context_root.exists():
        for path in context_root.iterdir():
            if path.is_dir():
                loaded["context"][path.name] = load_artifact_dir(path)

    principle_root = artifacts_root / "principle"
    if principle_root.exists():
        for path in principle_root.iterdir():
            if path.is_dir():
                loaded["principle"][path.name] = load_artifact_dir(path)

    return loaded


def count_loaded_artifacts(axes: Dict[str, Dict[str, dict]]) -> int:
    return sum(len(items) for items in axes.values())


def merge_missing_axes(
    loaded_axes: Dict[str, Dict[str, dict]],
    fallback_axes: Dict[str, Dict[str, dict]],
) -> Dict[str, Dict[str, dict]]:
    """
    Fills missing or incomplete axes from the known directory structure.

    This allows the manifest to remain rich with descriptions and metadata,
    while still ensuring Runtime v2 has all required F-C-P artifacts.
    """

    for axis, fallback_items in fallback_axes.items():
        if axis not in loaded_axes:
            loaded_axes[axis] = {}

        for name, artifact in fallback_items.items():
            if name not in loaded_axes[axis]:
                loaded_axes[axis][name] = artifact

    return loaded_axes


def load_atlas_v2(
    artifacts_root: str | Path = DEFAULT_ARTIFACTS_ROOT,
) -> dict:
    """
    Loads ACE Atlas v2 artifacts for ACA Runtime v2.

    This loader does not scan arbitrary fields as the legacy loader did.
    It first attempts to load the triaxial manifest, then falls back to
    the current known ACE Atlas directory structure.
    """

    artifacts_root = Path(artifacts_root)

    if not artifacts_root.exists():
        raise FileNotFoundError(f"Artifacts root not found: {artifacts_root}")

    manifest_path = artifacts_root / "triaxial" / "manifest.json"

    manifest = None
    loaded_axes = None

    if manifest_path.exists():
        manifest = load_json(manifest_path)
        loaded_axes = load_declared_artifacts_from_manifest(
            artifacts_root=artifacts_root,
            manifest=manifest,
        )

    fallback_axes = load_fallback_triaxial_artifacts(artifacts_root)

    if not loaded_axes or count_loaded_artifacts(loaded_axes) == 0:
        loaded_axes = fallback_axes
    else:
        loaded_axes = merge_missing_axes(
            loaded_axes=loaded_axes,
            fallback_axes=fallback_axes,
        )

    return {
        "atlas_type": "ACE Atlas v2",
        "artifacts_root": str(artifacts_root),
        "manifest_path": str(manifest_path) if manifest_path.exists() else None,
        "manifest": manifest,
        "axes": loaded_axes,
        "loaded_counts": {
            axis: len(items)
            for axis, items in loaded_axes.items()
        },
    }


def summarize_atlas_v2(atlas: dict) -> dict:
    return {
        "atlas_type": atlas["atlas_type"],
        "artifacts_root": atlas["artifacts_root"],
        "manifest_path": atlas["manifest_path"],
        "loaded_counts": atlas["loaded_counts"],
        "loaded_artifacts": {
            axis: list(items.keys())
            for axis, items in atlas["axes"].items()
        },
    }


if __name__ == "__main__":
    atlas = load_atlas_v2()
    summary = summarize_atlas_v2(atlas)

    print(json.dumps(summary, indent=2))