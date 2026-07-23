#!/usr/bin/env python3
"""Apply the provisional Tier adjudication overlay to an Elemental Feature Bank repository.

The script does not download any optional source values. It updates Tier metadata,
moves public columns whose final A-C/D-G partition changed, rebuilds split metadata
and the block summary, and writes a change summary.

Usage:
    python apply_tier_adjudication.py \
        --repo-root /path/to/elemental-feature-bank \
        --overlay element_feature_metadata_adjudication_overlay.csv \
        --output-dir /path/to/elemental-feature-bank-adjudicated
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path

TIER_LABELS = {
    "A_strict_direct": "直接的な元素・原子物性または明示的カテゴリ",
    "B_condition_resolved_direct": "条件を明示した直接量",
    "C_transparent_derived": "透明な派生量",
    "D_empirical_contextual_auxiliary": "経験的・文脈依存補助量",
    "E_engineered_arithmetic_auxiliary": "人工的演算補助量",
    "F_relational_pair_auxiliary": "元素対関係補助量",
    "G_noninterpretable_representation": "非解釈可能な学習済み・符号化表現",
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
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_dicts(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def read_matrix(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError(f"Empty CSV: {path}")
    return rows[0], rows[1:]

def write_matrix(path: Path, header: list[str], data: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--overlay", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    src = args.repo_root.resolve()
    out = args.output_dir.resolve()
    if out.exists():
        raise FileExistsError(f"Output directory already exists: {out}")
    shutil.copytree(src, out)

    overlay_rows = read_dicts(args.overlay)
    overlay = {r["feature_name"]: r for r in overlay_rows}
    if len(overlay) != len(overlay_rows):
        raise ValueError("Duplicate feature_name in overlay")

    public_meta = read_dicts(out / "element_feature_metadata.csv")
    excluded_meta = read_dicts(out / "excluded_features.csv")
    all_meta = public_meta + excluded_meta
    if set(overlay) != {r["feature_name"] for r in all_meta}:
        raise ValueError("Overlay feature set does not match metadata + excluded_features")

    changed = []
    for row in all_meta:
        ov = overlay[row["feature_name"]]
        old_tier = row["interpretability_tier"]
        new_tier = ov["adjudicated_tier"]
        new_file = ov["adjudicated_dataset_file"]
        if old_tier != new_tier or row["dataset_file"] != new_file:
            changed.append((row["feature_name"], old_tier, new_tier, row["dataset_file"], new_file))
        row["interpretability_tier"] = new_tier
        row["tier_label"] = TIER_LABELS[new_tier]
        row["dataset_file"] = new_file
        if new_tier[0] in "ABC":
            row["dataset_partition"] = "interpretable_main"
            row["include_in_recommended_main"] = "1"
            row["interpretability_decision"] = "kept_interpretable"
            row["partition_reason"] = (
                "Included in the recommended interpretable matrix after Tier adjudication."
            )
        else:
            row["dataset_partition"] = "others"
            row["include_in_recommended_main"] = "0"
            row["interpretability_decision"] = (
                "removed_noninterpretable"
                if new_tier.startswith("G_")
                else "moved_to_auxiliary"
            )
            row["partition_reason"] = (
                "Included in the other/auxiliary matrix after Tier adjudication."
            )
        row["partition_class"] = PARTITION_CLASS[new_tier]
        row["curation_notes"] = (
            (row.get("curation_notes", "") + " | ").strip(" |")
            + "Tier updated by second-review adjudication."
        )

    # Move public columns across the A-C/D-G boundary.
    final_public = [r for r in all_meta if r.get("public_value_distribution") == "include"]
    final_file = {r["feature_name"]: r["dataset_file"] for r in final_public}
    ih, idata = read_matrix(out / "element_data_interpretable.csv")
    oh, odata = read_matrix(out / "element_data_others.csv")
    if [r[0] for r in idata] != [r[0] for r in odata]:
        raise ValueError("Element row order differs between public matrices")

    source_headers = ih[1:] + oh[1:]
    if len(source_headers) != len(set(source_headers)):
        raise ValueError("Duplicate public feature names")
    values_by_feature = {}
    for j, name in enumerate(ih[1:], start=1):
        values_by_feature[name] = [r[j] for r in idata]
    for j, name in enumerate(oh[1:], start=1):
        values_by_feature[name] = [r[j] for r in odata]

    new_interpretable = [name for name in source_headers if final_file[name] == "element_data_interpretable.csv"]
    new_others = [name for name in source_headers if final_file[name] == "element_data_others.csv"]
    elements = [r[0] for r in idata]
    write_matrix(
        out / "element_data_interpretable.csv",
        [""] + new_interpretable,
        [[el] + [values_by_feature[name][i] for name in new_interpretable] for i, el in enumerate(elements)],
    )
    write_matrix(
        out / "element_data_others.csv",
        [""] + new_others,
        [[el] + [values_by_feature[name][i] for name in new_others] for i, el in enumerate(elements)],
    )

    # Write updated metadata files.
    fields = list(public_meta[0].keys())
    public_updated = [r for r in all_meta if r.get("public_value_distribution") == "include"]
    excluded_updated = [r for r in all_meta if r.get("public_value_distribution") == "exclude"]
    write_dicts(out / "element_feature_metadata.csv", public_updated, fields)
    write_dicts(
        out / "element_feature_metadata_interpretable.csv",
        [r for r in public_updated if r["dataset_file"] == "element_data_interpretable.csv"],
        fields,
    )
    write_dicts(
        out / "element_feature_metadata_others.csv",
        [r for r in public_updated if r["dataset_file"] == "element_data_others.csv"],
        fields,
    )
    write_dicts(out / "excluded_features.csv", excluded_updated, fields)

    # Rebuild block summary for public features.
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for r in public_updated:
        key = (r["dataset_file"], r["interpretability_tier"], r["feature_block"], r["source"])
        groups[key].append(r)
    summary_fields = [
        "dataset_file", "interpretability_tier", "feature_block", "source",
        "feature_count", "coverage_count_min", "coverage_count_mean",
        "coverage_count_max", "coverage_percent_mean", "feature_examples",
    ]
    summary_rows = []
    for key, items in sorted(groups.items()):
        counts = [int(float(r["coverage_count"])) for r in items]
        pcts = [float(r["coverage_percent"]) for r in items]
        summary_rows.append({
            "dataset_file": key[0],
            "interpretability_tier": key[1],
            "feature_block": key[2],
            "source": key[3],
            "feature_count": str(len(items)),
            "coverage_count_min": str(min(counts)),
            "coverage_count_mean": f"{sum(counts)/len(counts):.6g}",
            "coverage_count_max": str(max(counts)),
            "coverage_percent_mean": f"{sum(pcts)/len(pcts):.6g}",
            "feature_examples": "; ".join(r["feature_name"] for r in items[:5]),
        })
    write_dicts(out / "element_feature_block_summary.csv", summary_rows, summary_fields)

    result = {
        "changed_feature_count": len(changed),
        "public_interpretable_feature_count": len(new_interpretable),
        "public_other_feature_count": len(new_others),
        "public_total_feature_count": len(new_interpretable) + len(new_others),
        "public_partition_moves": [
            {
                "feature_name": name,
                "old_file": old_file,
                "new_file": new_file,
            }
            for name, old_tier, new_tier, old_file, new_file in changed
            if old_file != new_file and name in final_file
        ],
    }
    (out / "tier_adjudication_applied_summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
