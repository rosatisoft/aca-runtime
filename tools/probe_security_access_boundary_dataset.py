from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from aca_runtime.runtime.projection import origin_cost
from aca_runtime.runtime.text_evaluator import embed_text


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "datasets" / "security_access_boundary" / "out_of_sample_v1.jsonl"
MANIFEST_PATH = ROOT / "artifacts" / "security_access_boundary" / "manifest.json"
DEFAULT_RESULTS_DIR = ROOT / "results" / "security_access_boundary"

FIELD_GROUP = {
    "unsafe_secret_extraction": "boundary",
    "manipulative_credential_pressure": "boundary",

    "defensive_account_recovery": "safe",
    "safe_security_guidance": "safe",
    "credential_hygiene_guidance": "safe",

    "ambiguous_sensitive_access": "clarify",
    "sensitive_access_object": "clarify",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc

            required = {"id", "family", "language", "text", "expected_decision"}
            missing = required - set(case)
            if missing:
                raise ValueError(f"Case at {path}:{line_no} is missing keys: {sorted(missing)}")

            cases.append(case)

    if not cases:
        raise ValueError(f"Dataset is empty: {path}")

    return cases


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def load_artifacts() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Security access boundary manifest not found: {MANIFEST_PATH}")

    manifest = load_json(MANIFEST_PATH)
    artifacts: dict[str, dict[str, Any]] = {}

    for entry in manifest["artifacts"]:
        name = entry["name"]
        artifact_path = ROOT / entry["artifact_path"]
        basis_path = artifact_path / "basis_vectors.npy"
        metadata_path = artifact_path / "field_metadata.json"

        if not basis_path.exists():
            raise FileNotFoundError(f"Missing basis vectors for {name}: {basis_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Missing metadata for {name}: {metadata_path}")

        artifacts[name] = {
            "basis": np.load(basis_path),
            "metadata": load_json(metadata_path),
            "expected_decision": entry.get("expected_decision"),
            "group": FIELD_GROUP.get(name, "unknown"),
        }

    return manifest, artifacts


def rank_fields(vector: np.ndarray, artifacts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []

    for name, artifact in artifacts.items():
        ranked.append({
            "name": name,
            "group": artifact["group"],
            "cost": round(float(origin_cost(vector, artifact["basis"])), 6),
            "expected_decision": artifact.get("expected_decision"),
        })

    ranked.sort(key=lambda item: item["cost"])
    return ranked


def decide(
    ranked: list[dict[str, Any]],
    *,
    activation_threshold: float,
    ambiguity_margin: float,
) -> tuple[str, str, bool, bool]:
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    margin = second["cost"] - top["cost"] if second else None

    if top["cost"] > activation_threshold:
        return (
            "PASS_THROUGH_OR_MONITOR",
            f"Activation weak; top={top['name']} group={top['group']} cost={top['cost']:.6f}.",
            False,
            False,
        )

    if top["group"] == "boundary":
        return (
            "BOUNDARY_SECRET_REQUEST",
            f"Boundary precedence; top={top['name']}, second={second['name'] if second else None}, margin={margin}.",
            True,
            True,
        )

    if top["group"] == "safe":
        if second and margin is not None and margin < ambiguity_margin and second["group"] == "boundary":
            return (
                "ASK_CLARIFICATION_SENSITIVE",
                f"Safe top close to boundary second; top={top['name']}, second={second['name']}, margin={margin:.6f}.",
                False,
                True,
            )
        return (
            "SAFE_CREDENTIAL_GUIDANCE",
            f"Safe group preserved; top={top['name']}, second={second['name'] if second else None}, margin={margin}.",
            False,
            True,
        )

    if top["group"] == "clarify":
        return (
            "ASK_CLARIFICATION_SENSITIVE",
            f"Clarification group selected; top={top['name']}, second={second['name'] if second else None}, margin={margin}.",
            False,
            True,
        )

    return (
        "PASS_THROUGH_OR_MONITOR",
        f"Unknown field group for top={top['name']}.",
        False,
        False,
    )


def run_case(
    case: dict[str, Any],
    manifest: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    *,
    activation_threshold: float,
    ambiguity_margin: float,
) -> dict[str, Any]:
    vector = normalize_vector(embed_text(case["text"], model=manifest["embedding_model"]))
    ranked = rank_fields(vector, artifacts)
    decision, reason, boundary_applied, no_origin = decide(
        ranked,
        activation_threshold=activation_threshold,
        ambiguity_margin=ambiguity_margin,
    )

    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    margin = round(second["cost"] - top["cost"], 6) if second else None

    return {
        "id": case["id"],
        "family": case["family"],
        "language": case["language"],
        "text": case["text"],
        "expected_decision": case["expected_decision"],
        "decision": decision,
        "strict_pass": decision == case["expected_decision"],
        "boundary_applied": boundary_applied,
        "no_origin_recommended": no_origin,
        "top_field": top["name"],
        "top_group": top["group"],
        "top_cost": top["cost"],
        "second_field": second["name"] if second else None,
        "second_group": second["group"] if second else None,
        "second_cost": second["cost"] if second else None,
        "margin": margin,
        "reason": reason,
        "embedding_model": manifest["embedding_model"],
        "embedding_dim": manifest["embedding_dim"],
        "activation_threshold": activation_threshold,
        "ambiguity_margin": ambiguity_margin,
        "ranked_fields": ranked,
    }


def print_case(row: dict[str, Any]) -> None:
    status = "PASS" if row["strict_pass"] else "CHECK"
    print("-" * 110)
    print(f"ID:       {row['id']}")
    print(f"Family:   {row['family']}")
    print(f"Language: {row['language']}")
    print(f"Input:    {row['text']}")
    print(f"Decision: {row['decision']} | expected={row['expected_decision']} | {status}")
    print(
        f"Top:      {row['top_field']} [{row['top_group']}] ({row['top_cost']}) | "
        f"Second: {row['second_field']} [{row['second_group']}] ({row['second_cost']}) | "
        f"Margin: {row['margin']}"
    )
    print(f"Boundary: {row['boundary_applied']} | No-origin recommended: {row['no_origin_recommended']}")
    print(f"Reason:   {row['reason']}")


def summarize(rows: list[dict[str, Any]]) -> None:
    total = len(rows)
    strict = sum(1 for row in rows if row["strict_pass"])
    no_origin = sum(1 for row in rows if row["no_origin_recommended"])
    boundary = sum(1 for row in rows if row["boundary_applied"])

    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)
    print(f"Strict expected decisions: {strict}/{total}")
    print(f"No-origin recommended:     {no_origin}/{total}")
    print(f"Boundary applied:          {boundary}/{total}")

    print("\nDecision distribution:")
    for decision in sorted({row["decision"] for row in rows}):
        print(f"  {decision}: {sum(1 for row in rows if row['decision'] == decision)}")

    print("\nTop-field distribution:")
    for field in sorted({row["top_field"] for row in rows}):
        print(f"  {field}: {sum(1 for row in rows if row['top_field'] == field)}")

    print("\nLanguage / decision:")
    for row in rows:
        status = "OK" if row["strict_pass"] else "CHECK"
        print(
            f"  {status:<5} | {row['id']:<14} | {row['family']:<28} | "
            f"{row['language']:<17} | {row['top_field']:<34} | {row['decision']}"
        )


def write_outputs(rows: list[dict[str, Any]], results_dir: Path, dataset_path: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)

    stem = dataset_path.stem
    csv_path = results_dir / f"{stem}_results.csv"
    jsonl_path = results_dir / f"{stem}_results.jsonl"

    fields = [
        "id", "family", "language", "text", "expected_decision", "decision",
        "strict_pass", "boundary_applied", "no_origin_recommended",
        "top_field", "top_group", "top_cost",
        "second_field", "second_group", "second_cost",
        "margin", "reason", "embedding_model", "embedding_dim",
        "activation_threshold", "ambiguity_margin",
    ]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})

    with jsonl_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\nCSV:   {csv_path}")
    print(f"JSONL: {jsonl_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dataset-driven probe for ACA security access boundary artifacts."
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--activation-threshold", type=float, default=0.65)
    parser.add_argument("--ambiguity-margin", type=float, default=0.03)
    args = parser.parse_args()

    print("=" * 110)
    print("ACA Runtime - Security Access Boundary Dataset Probe")
    print("=" * 110)

    dataset_path = args.dataset if args.dataset.is_absolute() else ROOT / args.dataset
    results_dir = args.results_dir if args.results_dir.is_absolute() else ROOT / args.results_dir

    manifest, artifacts = load_artifacts()
    cases = load_jsonl(dataset_path)

    print(f"Manifest:             {MANIFEST_PATH}")
    print(f"Dataset:              {dataset_path}")
    print(f"Model:                {manifest['embedding_model']}")
    print(f"Dim:                  {manifest['embedding_dim']}")
    print(f"Fields:               {len(artifacts)}")
    print(f"Cases:                {len(cases)}")
    print(f"Activation threshold: {args.activation_threshold}")
    print(f"Ambiguity margin:     {args.ambiguity_margin}")

    rows = [
        run_case(
            case,
            manifest,
            artifacts,
            activation_threshold=args.activation_threshold,
            ambiguity_margin=args.ambiguity_margin,
        )
        for case in cases
    ]

    for row in rows:
        print_case(row)

    summarize(rows)
    write_outputs(rows, results_dir, dataset_path)


if __name__ == "__main__":
    main()
