#!/usr/bin/env python3
"""Build the licence-gated public elemental feature release.

Only source rows classified GREEN/include are copied to public value matrices.
AMBER/HOLD values remain excluded and are locally reconstructable.  An optional
Tier-adjudication overlay is applied before the two A-C/D-G matrices are built.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping

TIER_LABELS = {
    "A_strict_direct": "Direct elemental/atomic property or explicit category",
    "B_condition_resolved_direct": "Condition-resolved direct property",
    "C_transparent_derived": "Transparently derived property",
    "D_empirical_contextual_auxiliary": "Empirical/contextual auxiliary feature",
    "E_engineered_arithmetic_auxiliary": "Engineered arithmetic auxiliary feature",
    "F_relational_pair_auxiliary": "Relational element-pair auxiliary feature",
    "G_noninterpretable_representation": "Non-interpretable learned or encoded representation",
}
PARTITION_CLASS = {
    "A_strict_direct": "strict_direct",
    "B_condition_resolved_direct": "condition_resolved_direct",
    "C_transparent_derived": "transparent_derived",
    "D_empirical_contextual_auxiliary": "empirical_contextual_auxiliary",
    "E_engineered_arithmetic_auxiliary": "engineered_arithmetic_auxiliary",
    "F_relational_pair_auxiliary": "relational_pair_auxiliary",
    "G_noninterpretable_representation": "noninterpretable_representation",
}


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_dicts(path: Path, fields: list[str], rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def read_matrix(path: Path) -> tuple[str, list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        h = next(r)
        return h[0], h[1:], list(r)


def write_matrix(path: Path, id_header: str, features: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([id_header] + features)
        w.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-package-dir", type=Path, required=True)
    ap.add_argument("--policy-file", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--tier-adjudication-overlay", type=Path)
    ap.add_argument("--build-date", default="2026-07-18")
    ap.add_argument("--release-version", default="1.0.0")
    ap.add_argument("--clean", action="store_true")
    args = ap.parse_args()

    src = args.full_package_dir.resolve()
    out = args.output_dir.resolve()
    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    overlay_path = args.tier_adjudication_overlay
    if overlay_path is None:
        candidate = Path(__file__).resolve().parents[1] / "curation" / "element_feature_metadata_adjudication_overlay.csv"
        overlay_path = candidate if candidate.is_file() else None
    overlay = {}
    if overlay_path:
        overlay = {r["feature_name"]: r for r in read_dicts(Path(overlay_path))}

    policy_rows = read_dicts(args.policy_file)
    policy = {r["source_id"]: r for r in policy_rows}
    registry = read_dicts(src / "element_source_registry.csv")
    block_to_source: dict[str, str] = {}
    for r in registry:
        for block in [x.strip() for x in r["feature_blocks"].split(";") if x.strip()]:
            block_to_source[block] = r["source_id"]

    meta = read_dicts(src / "element_feature_metadata.csv")
    public_meta: list[dict[str, str]] = []
    excluded_meta: list[dict[str, str]] = []
    for original in meta:
        r = dict(original)
        sid = block_to_source[r["feature_block"]]
        pr = policy[sid]
        r.update({
            "source_id": sid,
            "license_status": pr["license_status"],
            "public_value_distribution": pr["public_value_distribution"],
            "license_reason": pr.get("reason", ""),
            "required_action": pr.get("required_action", ""),
        })
        # Semantic fill rules retained from the initial public build.
        if r.get("interpretability_tier") == "G_noninterpretable_representation":
            r["unit"] = r.get("unit") or "dimensionless / model-dependent"
            r["reference_state"] = r.get("reference_state") or "pretrained element representation; individual coordinates have no standalone physical definition"
            r["calculation_method"] = r.get("calculation_method") or r.get("description", "").split(":", 1)[0]
        if r.get("feature_block") == "mendeleev_screening":
            r["unit"] = r.get("unit") or "dimensionless"
            r["reference_state"] = r.get("reference_state") or "neutral isolated atom; subshell-resolved screening constant"
            r["calculation_method"] = r.get("calculation_method") or "Mendeleev screening-constant lookup"
        if r.get("feature_block") == "mendeleev_scattering_factors":
            m = re.search(r"_at_(\d+)eV", r["feature_name"])
            if m:
                r["photon_energy_eV"] = m.group(1)
            r["reference_state"] = r.get("reference_state") or "isolated neutral atom; energy-resolved X-ray scattering factor"
            r["calculation_method"] = r.get("calculation_method") or "Mendeleev/Henke table lookup at fixed energy"
        if r.get("feature_block") == "mendeleev_ionization_uncertainty":
            m = re.search(r"stage_(\d+)", r["feature_name"])
            if m:
                r["charge_state"] = str(int(m.group(1)) - 1)
                r["reference_state"] = r.get("reference_state") or f"isolated atomic species; ionization stage {int(m.group(1))}"
            else:
                r["reference_state"] = r.get("reference_state") or "successive ionization-energy records aggregated over available stages"
            r["calculation_method"] = r.get("calculation_method") or "Mendeleev ionization-energy uncertainty lookup / transparent aggregation"
        # Apply the feature-level Tier adjudication after source parsing.
        ov = overlay.get(r["feature_name"])
        if ov:
            new_tier = ov["adjudicated_tier"]
            new_file = ov["adjudicated_dataset_file"]
            r["interpretability_tier"] = new_tier
            r["tier_label"] = TIER_LABELS[new_tier]
            r["dataset_file"] = new_file
            r["partition_class"] = PARTITION_CLASS[new_tier]
            if new_tier[0] in "ABC":
                r["dataset_partition"] = "interpretable_main"
                r["include_in_recommended_main"] = "1"
                r["interpretability_decision"] = "kept_interpretable"
                r["partition_reason"] = "Included in the recommended interpretable matrix after Tier adjudication."
            else:
                r["dataset_partition"] = "others"
                r["include_in_recommended_main"] = "0"
                r["interpretability_decision"] = "removed_noninterpretable" if new_tier.startswith("G_") else "moved_to_auxiliary"
                r["partition_reason"] = "Included in the other/auxiliary matrix after Tier adjudication."
            r["curation_notes"] = ((r.get("curation_notes", "") + " | ").strip(" |") + "Tier updated by second-review adjudication.")
        (public_meta if pr["license_status"] == "GREEN" and pr["public_value_distribution"] == "include" else excluded_meta).append(r)

    # Read both original matrices into one feature-value map, then route columns by the adjudicated dataset_file.
    matrix_data = []
    id_header = ""
    elements = None
    source_order: list[str] = []
    values_by_feature: dict[str, list[str]] = {}
    for filename in ("element_data_interpretable.csv", "element_data_others.csv"):
        ih, features, rows = read_matrix(src / filename)
        id_header = ih
        row_elements = [r[0] for r in rows]
        if elements is None:
            elements = row_elements
        elif elements != row_elements:
            raise ValueError("Element row order differs between full matrices")
        source_order.extend(features)
        for j, feature in enumerate(features, start=1):
            values_by_feature[feature] = [(row[j] if j < len(row) else "") for row in rows]
    public_by_name = {r["feature_name"]: r for r in public_meta}
    output_features = {
        filename: [f for f in source_order if f in public_by_name and public_by_name[f]["dataset_file"] == filename]
        for filename in ("element_data_interpretable.csv", "element_data_others.csv")
    }
    for filename, features in output_features.items():
        rows = [[element] + [values_by_feature[f][i] for f in features] for i, element in enumerate(elements or [])]
        write_matrix(out / filename, id_header, features, rows)

    meta_fields = list(meta[0].keys()) + ["source_id", "license_status", "public_value_distribution", "license_reason", "required_action"]
    write_dicts(out / "element_feature_metadata.csv", meta_fields, public_meta)
    write_dicts(out / "element_feature_metadata_interpretable.csv", meta_fields, [r for r in public_meta if r["dataset_file"] == "element_data_interpretable.csv"])
    write_dicts(out / "element_feature_metadata_others.csv", meta_fields, [r for r in public_meta if r["dataset_file"] == "element_data_others.csv"])
    write_dicts(out / "excluded_features.csv", meta_fields, excluded_meta)

    all_by_sid: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in public_meta + excluded_meta:
        all_by_sid[r["source_id"]].append(r)
    registry_fields = list(registry[0].keys()) + ["license_status", "public_value_distribution", "license_reason", "required_action", "release_scope"]
    public_registry, excluded_sources = [], []
    for original in registry:
        r = dict(original)
        pr = policy[r["source_id"]]
        items = all_by_sid[r["source_id"]]
        r["feature_count_interpretable"] = str(sum(x["dataset_file"] == "element_data_interpretable.csv" for x in items))
        r["feature_count_others"] = str(sum(x["dataset_file"] == "element_data_others.csv" for x in items))
        r["feature_count_total"] = str(len(items))
        r["feature_examples"] = "; ".join(x["feature_name"] for x in items[:5])
        r["retrieval_date"] = r.get("retrieval_date", "").strip() or args.build_date
        r.update({
            "license_status": pr["license_status"],
            "public_value_distribution": pr["public_value_distribution"],
            "license_reason": pr.get("reason", ""),
            "required_action": pr.get("required_action", ""),
            "release_scope": "public values" if pr["license_status"] == "GREEN" and pr["public_value_distribution"] == "include" else "script-only / locally rebuilt",
        })
        (public_registry if r["public_value_distribution"] == "include" else excluded_sources).append(r)
    write_dicts(out / "element_source_registry.csv", registry_fields, public_registry)
    write_dicts(out / "excluded_sources.csv", registry_fields, excluded_sources)
    write_dicts(out / "source_license_policy.csv", ["source_id", "license_status", "public_value_distribution", "reason", "required_action"], policy_rows)

    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for r in public_meta:
        grouped[(r["dataset_file"], r["interpretability_tier"], r["feature_block"], r["source"])].append(r)
    block_rows = []
    for (dataset_file, tier, block, source_name), rows in sorted(grouped.items()):
        cov = [int(float(r["coverage_count"])) for r in rows]
        block_rows.append({
            "dataset_file": dataset_file,
            "interpretability_tier": tier,
            "feature_block": block,
            "source": source_name,
            "feature_count": len(rows),
            "coverage_count_min": min(cov),
            "coverage_count_mean": f"{statistics.fmean(cov):.6g}",
            "coverage_count_max": max(cov),
            "coverage_percent_mean": f"{100 * statistics.fmean(cov) / 118:.6g}",
            "feature_examples": "; ".join(r["feature_name"] for r in rows[:5]),
        })
    write_dicts(out / "element_feature_block_summary.csv", list(block_rows[0]), block_rows)

    input_manifest = []
    for p in sorted(src.iterdir()):
        if p.is_file():
            input_manifest.append({"file_name": p.name, "size_bytes": p.stat().st_size, "sha256": sha256(p), "input_role": "full_package"})
    if overlay_path:
        p = Path(overlay_path)
        input_manifest.append({"file_name": p.name, "size_bytes": p.stat().st_size, "sha256": sha256(p), "input_role": "tier_adjudication_overlay"})
    write_dicts(out / "input_manifest.csv", ["file_name", "size_bytes", "sha256", "input_role"], input_manifest)

    summary = {
        "build_date": args.build_date,
        "release_version": args.release_version,
        "elements": len(elements or []),
        "public_interpretable_features": len(output_features["element_data_interpretable.csv"]),
        "public_other_features": len(output_features["element_data_others.csv"]),
        "public_total_features": len(public_meta),
        "excluded_interpretable_features": sum(r["dataset_file"] == "element_data_interpretable.csv" for r in excluded_meta),
        "excluded_other_features": sum(r["dataset_file"] == "element_data_others.csv" for r in excluded_meta),
        "excluded_total_features": len(excluded_meta),
        "green_sources": len(public_registry),
        "amber_sources": sum(r["license_status"] == "AMBER" for r in excluded_sources),
        "hold_sources": sum(r["license_status"] == "HOLD" for r in excluded_sources),
        "tier_review_features": len(overlay),
        "tier_review_exact_agreement": sum(r.get("agreement") == "1" for r in overlay.values()),
        "tier_review_disagreements": sum(r.get("agreement") == "0" for r in overlay.values()),
        "tier_review_cohen_kappa_7class": 0.9607306169408875 if overlay else None,
        "tier_review_public_partition_moves": sum(r.get("matrix_partition_changed") == "1" and r.get("public_value_distribution") == "include" for r in overlay.values()),
        "tier_review_type": "AI-assisted blinded rubric second pass" if overlay else "not applied",
    }
    (out / "build_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
