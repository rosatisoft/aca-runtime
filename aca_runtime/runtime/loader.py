import json
from pathlib import Path

import numpy as np


DEFAULT_THRESHOLDS = {
    "foundational": 0.35,
    "factual": 0.45,
    "rhetorical": 0.55,
}


def load_field(field_dir: str | Path) -> dict:
    field_dir = Path(field_dir)

    metadata_path = field_dir / "field_metadata.json"
    basis_path = field_dir / "basis_vectors.npy"
    singular_values_path = field_dir / "singular_values.npy"

    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing field metadata: {metadata_path}")

    if not basis_path.exists():
        raise FileNotFoundError(f"Missing basis vectors: {basis_path}")

    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    basis = np.load(basis_path)

    singular_values = None
    if singular_values_path.exists():
        singular_values = np.load(singular_values_path)

    field_type = metadata.get("field_type", field_dir.name)

    return {
        "name": metadata.get("field_name", field_type),
        "type": field_type,
        "basis": basis,
        "singular_values": singular_values,
        "threshold": DEFAULT_THRESHOLDS.get(field_type, 0.45),
        "metadata": metadata,
    }


def load_artifacts_atlas(artifacts_dir: str | Path) -> dict:
    artifacts_dir = Path(artifacts_dir)

    if not artifacts_dir.exists():
        raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")

    fields = {}

    for field_dir in artifacts_dir.iterdir():
        if not field_dir.is_dir():
            continue

        metadata_path = field_dir / "field_metadata.json"
        basis_path = field_dir / "basis_vectors.npy"

        if metadata_path.exists() and basis_path.exists():
            field = load_field(field_dir)
            fields[field["type"]] = field

    if not fields:
        raise ValueError(f"No valid ACA fields found in: {artifacts_dir}")

    return {
        "atlas_type": "ACA artifacts atlas",
        "fields": fields,
    }