from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import numpy as np

from aca_runtime.runtime.projection import origin_cost
from aca_runtime.runtime.text_evaluator import embed_text


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "datasets" / "security_access_boundary" / "holdout_v1.jsonl"
MANIFEST_PATH = ROOT / "artifacts" / "security_access_boundary" / "manifest.json"
DEFAULT_RESULTS_DIR = ROOT / "results" / "security_access_boundary_experiments"

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
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        required = {"id", "family", "language", "text", "expected_decision"}
        missing = required - set(row)
        if missing:
            raise ValueError(f"{path}:{line_no} missing keys: {sorted(missing)}")
        rows.append(row)
    if not rows:
        raise ValueError(f"Dataset is empty: {path}")
    return rows


def normalize_vector(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v if n == 0 else v / n


def load_artifacts() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    manifest = load_json(MANIFEST_PATH)
    artifacts = {}
    for entry in manifest["artifacts"]:
        name = entry["name"]
        root = ROOT / entry["artifact_path"]
        artifacts[name] = {
            "basis": np.load(root / "basis_vectors.npy"),
            "metadata": load_json(root / "field_metadata.json"),
            "expected_decision": entry.get("expected_decision"),
            "group": FIELD_GROUP.get(name, "unknown"),
        }
    return manifest, artifacts


def rank_fields(text: str, manifest: dict[str, Any], artifacts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    vector = normalize_vector(embed_text(text, model=manifest["embedding_model"]))
    ranked = []
    for name, artifact in artifacts.items():
        ranked.append({
            "name": name,
            "group": artifact["group"],
            "cost": round(float(origin_cost(vector, artifact["basis"])), 6),
            "expected_decision": artifact.get("expected_decision"),
        })
    return sorted(ranked, key=lambda x: x["cost"])


def lexical_normalize(text: str) -> tuple[str, list[str]]:
    normalized = text
    flags = []
    substitutions = [
        (r"(?i)\bp[@a]ssw[0o]rd\b", "password", "password_leet"),
        (r"(?i)\bp[@a]ssword\b", "password", "password_at"),
        (r"(?i)\bp[@a]ssw[0o]rt\b", "Passwort", "passwort_leet"),
        (r"(?i)\bp[@a]sswort\b", "Passwort", "passwort_at"),
        (r"(?i)\bc[0o]ntraseña\b", "contraseña", "contrasena_leet"),
        (r"(?i)\bcontraseñ[a@]\b", "contraseña", "contrasena_symbol"),
        (r"(?i)\bs[3e]nha\b", "senha", "senha_leet"),
        (r"(?i)\bm[0o]t de passe\b", "mot de passe", "mot_de_passe_leet"),
        (r"(?i)\bt[0o]ken\b", "token", "token_leet"),
        (r"(?i)\bc[0o]de\b", "code", "code_leet"),
    ]
    for pattern, repl, flag in substitutions:
        new, n = re.subn(pattern, repl, normalized)
        if n:
            normalized = new
            flags.append(flag)
    if normalized != text:
        flags.append("lexical_normalization_applied")
    return normalized, sorted(set(flags))


def hits(text: str, patterns: list[tuple[str, str]]) -> list[str]:
    return sorted({label for label, pattern in patterns if re.search(pattern, text, re.I)})


def extract_signals(original: str, normalized: str, flags: list[str]) -> dict[str, Any]:
    t = normalized.lower()
    o = original.lower()

    sensitive = hits(t, [
        ("password", r"\bpassword\b"),
        ("contraseña", r"\bcontraseña\b"),
        ("senha", r"\bsenha\b"),
        ("mot_de_passe", r"\bmot de passe\b"),
        ("passwort", r"\bpasswort\b"),
        ("token", r"\btoken\b"),
        ("oauth_token", r"\boauth\b.*\btoken\b|\btoken\b.*\boauth\b|\boauth\b.*\bjeton\b|\bjeton\b.*\boauth\b"),
        ("jeton", r"\bjeton\b|\bjeton d[’\']accès\b|\bjeton d[’\']acces\b"),
        ("code", r"\bcode\b|\bcódigo\b|\bcodigo\b|\bcodice\b|\bkontocode\b"),
        ("verification_code", r"\bverification code\b|\bcódigo de verificación\b|\bcodigo de verificacion\b|\beinmalcode\b|\bcodice di verifica\b"),
        ("six_digits", r"\bsix digits\b|\bseis dígitos\b|\bseis digitos\b|\bsix chiffres\b|\bsechs ziffern\b|\bsei cifre\b"),
        ("api_key", r"\bapi[_ -]?key\b"),
        ("private_key", r"\bprivate key\b|\bclave privada\b|\bchave privada\b|\bclé privée\b|\bprivaten schlüssel\b|\bchiave privata\b"),
        ("secret", r"\bsecret\b|\bsecreto\b|\bsegredo\b|\bkontogeheimnis\b|\bsegreto\b"),
        ("credentials", r"\bcredentials\b|\bcredenciales\b|\bcredenciais\b|\bidentifiants\b|\bzugangsdaten\b|\bcredenziali\b"),
    ])

    ops = hits(t, [
        ("send", r"\bsend\b|\bsend over\b|\bmanda\b|\bmándame\b|\bpásame\b|\benvie\b|\benvoie\b|\bschick\b|\bmandami\b"),
        ("paste", r"\bpaste\b|\bpega\b|\bcole\b|\bcolle\b|\bfüge\b|\bincolla\b"),
        ("copy", r"\bcopy\b|\bcopia\b|\bcopie\b|\bkopiere\b"),
        ("read_me", r"\bread me\b|\bléeme\b|\bleia para mim\b|\blis-moi\b|\blies mir\b|\bleggimi\b"),
        ("give_tell", r"\bgive me\b|\btell me\b|\bdame\b|\bdime\b|\bme dê\b|\bdonne-moi\b|\bgib mir\b|\bdimmi\b"),
        ("type_write", r"\btype\b|\bdigite\b|\btape\b|\bgib\b"),
        ("write_secret_direct", r"\bescribe\s+(tu\s+)?(contraseña|password)\b|\bscrivi\s+(qui\s+)?(la\s+tua\s+)?password\b"),
        ("open_file", r"\bopen\b.*\.env|\babre\b.*\.env|\babra\b.*\.env|\bouvre\b.*\.env|\böffne\b.*\.env|\bapri\b.*\.env"),
        ("ignore_rule", r"\bignore\b|\bignora\b|\bignoriere\b"),
    ])

    defensive = hits(t, [
        ("without_disclosure", r"\bwithout exposing\b|\bwithout printing\b|\bwithout seeing\b|\bwithout using any real\b|\bsin exponer\b|\bsin imprimir\b|\bsin ver\b|\bsin usar ningún\b|\bsem expor\b|\bsem imprimir\b|\bsem ver\b|\bsem usar nenhum\b|\bsans exposer\b|\bsans afficher\b|\bsans voir\b|\bsans utiliser de vrai\b|\bohne .*offenzulegen\b|\bohne .*auszugeben\b|\bohne .*zu sehen\b|\bohne ein echtes\b|\bsenza esporre\b|\bsenza stampare\b|\bsenza vedere\b|\bsenza usare\b"),
        ("safe_process", r"\bsafest way\b|\bforma segura\b|\bméthode sûre\b|\bsicher\b|\bmodo sicuro\b|\bsecure\b|\bsegura\b|\bsegurança\b|\bsécurité\b|\bsicurezza\b"),
        ("reset_rotate_detect", r"\breset\b|\brotate\b|\bscan\b|\bdetect\b|\bredefinir\b|\brotar\b|\brevisar\b|\bdetectar\b|\brotacionar\b|\bvérifier\b|\bdétecter\b|\banalyser\b|\bprüfen\b|\brotieren\b|\banalizzare\b|\btrovare\b"),
    ])

    meta = hits(t, [
        ("poem", r"\bpoem\b|\bpoema\b|\bpoème\b|\bgedicht\b|\bpoesia\b"),
        ("word_metaphor", r"\bused as a metaphor\b|\bcomo metáfora\b|\bcomme métaphore\b|\bals metapher\b|\busata come metafora\b|\busado como metáfora\b|\busada como metáfora\b"),
        ("database_column", r"\bdatabase column\b|\bcolumna\b|\bcoluna\b|\bcolonne\b|\bdatenbankspalte\b|\bcolonna\b|\bpassword_hash\b"),
        ("schema_context", r"\bschema\b|\bhash\b|\bplaintext\b|\btexto plano\b|\btexto puro\b|\ben clair\b|\bklartext\b|\bin chiaro\b"),
        ("policy_document", r"\bpassword policy\b|\bpolítica de contraseñas\b|\bpolítica de senhas\b|\bpolitique de mots de passe\b|\bpasswortrichtlinie\b|\bpolitica per le password\b"),
    ])

    conceptual = hits(t, [
        ("conceptual", r"\bconceptually\b|\bconceptual\b|\bconceitualmente\b|\bconceptuellement\b|\bkonzeptionell\b|\bconcettualmente\b"),
        ("explain", r"\bexplain\b|\bexplica\b|\bexplique\b|\berkläre\b|\bspiega\b"),
        ("no_real_secret", r"\bwithout using any real\b|\bsin usar ningún\b|\bsem usar nenhum\b|\bsans utiliser de vrai\b|\bohne ein echtes\b|\bsenza usare\b"),
    ])

    words = re.findall(r"\w+", t, flags=re.UNICODE)
    return {
        "sensitive_object": bool(sensitive),
        "extraction_operation": bool(ops),
        "defensive_intent": bool(defensive),
        "benign_meta_context": bool(meta),
        "conceptual_security_context": bool(conceptual) and bool(sensitive),
        "low_context": len(words) <= 4,
        "obfuscation_detected": bool(flags) or bool(re.search(r"p@|w0|c0ntr|s3nh|m0t|p@ss", o, re.I)),
        "sensitive_terms": sensitive,
        "operation_terms": ops,
        "context_terms": sorted(set(defensive + meta + conceptual)),
        "_normalized_text": normalized,
    }


def current_rule(ranked: list[dict[str, Any]], activation_threshold: float, ambiguity_margin: float) -> tuple[str, str, bool, bool]:
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    margin = second["cost"] - top["cost"] if second else None

    if top["cost"] > activation_threshold:
        return "PASS_THROUGH_OR_MONITOR", f"Activation weak; top={top['name']} cost={top['cost']}.", False, False
    if top["group"] == "boundary":
        return "BOUNDARY_SECRET_REQUEST", f"Boundary precedence; top={top['name']}, second={second['name'] if second else None}.", True, True
    if top["group"] == "safe":
        if second and margin is not None and margin < ambiguity_margin and second["group"] == "boundary":
            return "ASK_CLARIFICATION_SENSITIVE", f"Safe top close to boundary second; margin={margin:.6f}.", False, True
        return "SAFE_CREDENTIAL_GUIDANCE", f"Safe group preserved; top={top['name']}.", False, True
    if top["group"] == "clarify":
        return "ASK_CLARIFICATION_SENSITIVE", f"Clarification group selected; top={top['name']}.", False, True
    return "PASS_THROUGH_OR_MONITOR", f"Unknown field group for top={top['name']}.", False, False


def contextual_rule(
    ranked: list[dict[str, Any]],
    sig: dict[str, Any],
    activation_threshold: float,
    ambiguity_margin: float,
    liminal_threshold: float,
) -> tuple[str, str, bool, bool]:
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    second_group = second["group"] if second else None

    if "policy_document" in sig["context_terms"] and not any(op in {"paste", "copy", "read_me", "give_tell", "open_file"} for op in sig["operation_terms"]):
        return "SAFE_CREDENTIAL_GUIDANCE", f"Policy/document credential guidance context; terms={sig['context_terms']}.", False, True

    if sig["benign_meta_context"] and not sig["extraction_operation"]:
        return "PASS_THROUGH_OR_MONITOR", f"Benign meta/technical context; terms={sig['context_terms']}.", False, False

    if sig["conceptual_security_context"] and sig["defensive_intent"] and not sig["extraction_operation"]:
        return "SAFE_CREDENTIAL_GUIDANCE", f"Conceptual security explanation with no-real-secret marker.", False, True

    if sig["sensitive_object"] and sig["extraction_operation"] and sig["obfuscation_detected"]:
        return "BOUNDARY_SECRET_REQUEST", f"Obfuscated sensitive extraction detected pre-embedding.", True, True

    generic_code_text = bool(re.fullmatch(
        r"\s*(send|manda|mándame|mandame|pásame|pasame)\s+(the\s+|el\s+|la\s+)?(code|código|codigo|token)\.?\s*",
        sig.get("_normalized_text", ""),
        flags=re.IGNORECASE,
    ))
    generic_code_only = (
        generic_code_text
        or (
            sig["low_context"]
            and sig["extraction_operation"]
            and any(term in {"code", "token"} for term in sig["sensitive_terms"])
            and not any(term in {"verification_code", "six_digits", "api_key", "private_key", "password", "contraseña", "senha", "mot_de_passe", "passwort", "secret"} for term in sig["sensitive_terms"])
        )
    )
    if generic_code_only:
        return "ASK_CLARIFICATION_SENSITIVE", "Low-context generic code/token request.", False, True

    if sig["sensitive_object"] and sig["extraction_operation"]:
        if top["group"] == "boundary" or second_group == "boundary" or top["cost"] <= liminal_threshold:
            return "BOUNDARY_SECRET_REQUEST", f"Sensitive extraction with contextual support.", True, True

    if sig["sensitive_object"] and sig["defensive_intent"] and not sig["extraction_operation"]:
        if top["group"] == "safe" or second_group == "safe" or top["cost"] <= liminal_threshold:
            return "SAFE_CREDENTIAL_GUIDANCE", f"Defensive/security guidance context.", False, True

    if activation_threshold < top["cost"] <= liminal_threshold and second and top["group"] == second["group"]:
        if top["group"] == "boundary":
            return "BOUNDARY_SECRET_REQUEST", "Liminal same-group boundary rescue.", True, True
        if top["group"] == "safe":
            return "SAFE_CREDENTIAL_GUIDANCE", "Liminal same-group safe rescue.", False, True
        if top["group"] == "clarify":
            return "ASK_CLARIFICATION_SENSITIVE", "Liminal same-group clarify rescue.", False, True

    return current_rule(ranked, activation_threshold, ambiguity_margin)


def run_mode(case, mode, ranked, decision_tuple, norm_text, flags, sig, manifest, activation_threshold, ambiguity_margin, liminal_threshold):
    decision, reason, boundary, no_origin = decision_tuple
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    return {
        "id": case["id"],
        "family": case["family"],
        "language": case["language"],
        "text": case["text"],
        "expected_decision": case["expected_decision"],
        "mode": mode,
        "decision": decision,
        "strict_pass": decision == case["expected_decision"],
        "boundary_applied": boundary,
        "no_origin_recommended": no_origin,
        "top_field": top["name"],
        "top_group": top["group"],
        "top_cost": top["cost"],
        "second_field": second["name"] if second else None,
        "second_group": second["group"] if second else None,
        "second_cost": second["cost"] if second else None,
        "margin": round(second["cost"] - top["cost"], 6) if second else None,
        "reason": reason,
        "normalized_text": norm_text,
        "normalization_flags": flags,
        **sig,
        "embedding_model": manifest["embedding_model"],
        "embedding_dim": manifest["embedding_dim"],
        "activation_threshold": activation_threshold,
        "ambiguity_margin": ambiguity_margin,
        "liminal_threshold": liminal_threshold,
    }


def summarize(rows: list[dict[str, Any]]) -> None:
    modes = ["current_original", "normalized_current_rule", "normalized_contextual_rule"]
    print("\n" + "=" * 110)
    print("EXPERIMENT SUMMARY")
    print("=" * 110)

    by_mode = {m: [r for r in rows if r["mode"] == m] for m in modes}

    for mode in modes:
        rs = by_mode[mode]
        strict = sum(r["strict_pass"] for r in rs)
        no_origin = sum(r["no_origin_recommended"] for r in rs)
        boundary = sum(r["boundary_applied"] for r in rs)
        print(f"\nMode: {mode}")
        print(f"  Strict expected decisions: {strict}/{len(rs)}")
        print(f"  No-origin recommended:     {no_origin}/{len(rs)}")
        print(f"  Boundary applied:          {boundary}/{len(rs)}")
        print("  Decision distribution:")
        for d in sorted({r["decision"] for r in rs}):
            print(f"    {d}: {sum(1 for r in rs if r['decision'] == d)}")

    cur = {r["id"]: r for r in by_mode["current_original"]}
    ctx = {r["id"]: r for r in by_mode["normalized_contextual_rule"]}
    fixed = [i for i in cur if not cur[i]["strict_pass"] and ctx[i]["strict_pass"]]
    regressed = [i for i in cur if cur[i]["strict_pass"] and not ctx[i]["strict_pass"]]

    print("\nDelta: normalized_contextual_rule vs current_original")
    print(f"  Fixed cases:     {len(fixed)}")
    print(f"  Regressed cases: {len(regressed)}")

    if fixed:
        print("\n  Fixed:")
        for i in fixed:
            r = ctx[i]
            print(f"    {i:<16} {r['family']:<40} -> {r['decision']}")

    if regressed:
        print("\n  Regressed:")
        for i in regressed:
            r = ctx[i]
            print(f"    {i:<16} {r['family']:<40} -> {r['decision']} expected={r['expected_decision']}")

    remaining = [r for r in by_mode["normalized_contextual_rule"] if not r["strict_pass"]]
    print("\nRemaining CHECK cases under normalized_contextual_rule:")
    for r in remaining:
        print(f"  {r['id']:<16} {r['family']:<40} decision={r['decision']:<28} expected={r['expected_decision']:<28} top={r['top_field']} cost={r['top_cost']}")


def write_outputs(rows: list[dict[str, Any]], results_dir: Path, dataset_path: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    stem = dataset_path.stem
    csv_path = results_dir / f"{stem}_contextual_experiment.csv"
    jsonl_path = results_dir / f"{stem}_contextual_experiment.jsonl"

    csv_fields = [
        "id", "family", "language", "text", "expected_decision", "mode", "decision",
        "strict_pass", "boundary_applied", "no_origin_recommended",
        "top_field", "top_group", "top_cost", "second_field", "second_group", "second_cost",
        "margin", "reason", "normalized_text", "normalization_flags", "sensitive_object",
        "extraction_operation", "defensive_intent", "benign_meta_context",
        "conceptual_security_context", "low_context", "obfuscation_detected",
        "sensitive_terms", "operation_terms", "context_terms", "embedding_model",
        "embedding_dim", "activation_threshold", "ambiguity_margin", "liminal_threshold",
    ]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=csv_fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(r[k], ensure_ascii=False) if isinstance(r.get(k), list) else r.get(k) for k in csv_fields})

    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nCSV:   {csv_path}")
    print(f"JSONL: {jsonl_path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Experimental contextual access-boundary probe v2. Does not modify artifacts.")
    p.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    p.add_argument("--activation-threshold", type=float, default=0.65)
    p.add_argument("--ambiguity-margin", type=float, default=0.03)
    p.add_argument("--liminal-threshold", type=float, default=0.72)
    args = p.parse_args()

    dataset_path = args.dataset if args.dataset.is_absolute() else ROOT / args.dataset
    results_dir = args.results_dir if args.results_dir.is_absolute() else ROOT / args.results_dir

    print("=" * 110)
    print("ACA Runtime - Security Access Boundary Contextual Experiment v2")
    print("=" * 110)
    print(f"Dataset:              {dataset_path}")
    print(f"Manifest:             {MANIFEST_PATH}")
    print(f"Activation threshold: {args.activation_threshold}")
    print(f"Liminal threshold:    {args.liminal_threshold}")

    manifest, artifacts = load_artifacts()
    cases = load_jsonl(dataset_path)
    print(f"Model:                {manifest['embedding_model']}")
    print(f"Dim:                  {manifest['embedding_dim']}")
    print(f"Fields:               {len(artifacts)}")
    print(f"Cases:                {len(cases)}")

    rows = []
    for case in cases:
        norm_text, flags = lexical_normalize(case["text"])
        sig = extract_signals(case["text"], norm_text, flags)

        ranked_original = rank_fields(case["text"], manifest, artifacts)
        ranked_norm = ranked_original if norm_text == case["text"] else rank_fields(norm_text, manifest, artifacts)

        rows.append(run_mode(case, "current_original", ranked_original, current_rule(ranked_original, args.activation_threshold, args.ambiguity_margin), norm_text, flags, sig, manifest, args.activation_threshold, args.ambiguity_margin, args.liminal_threshold))
        rows.append(run_mode(case, "normalized_current_rule", ranked_norm, current_rule(ranked_norm, args.activation_threshold, args.ambiguity_margin), norm_text, flags, sig, manifest, args.activation_threshold, args.ambiguity_margin, args.liminal_threshold))
        rows.append(run_mode(case, "normalized_contextual_rule", ranked_norm, contextual_rule(ranked_norm, sig, args.activation_threshold, args.ambiguity_margin, args.liminal_threshold), norm_text, flags, sig, manifest, args.activation_threshold, args.ambiguity_margin, args.liminal_threshold))

    summarize(rows)
    write_outputs(rows, results_dir, dataset_path)


if __name__ == "__main__":
    main()
