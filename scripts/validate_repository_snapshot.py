#!/usr/bin/env python3
"""Validate the committed GREEN-only repository snapshot using only the standard library."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

ELEMENTS = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_matrix(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    features = header[1:]
    data = rows[1:]
    elements = [r[0] for r in data]
    values = {r[0]: dict(zip(features, r[1:] + [""] * max(0, len(features) - len(r[1:])))) for r in data}
    return features, elements, values


def read_dicts(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def fail(message: str):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str):
    if not condition:
        fail(message)
    print(f"PASS: {message}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    args = ap.parse_args()
    root = args.repo_root.resolve()

    summary = json.loads((root / "build_summary.json").read_text(encoding="utf-8"))
    interp_features, interp_elements, interp = read_matrix(root / "element_data_interpretable.csv")
    other_features, other_elements, other = read_matrix(root / "element_data_others.csv")
    metadata = read_dicts(root / "element_feature_metadata.csv")
    registry = read_dicts(root / "element_source_registry.csv")
    policy = read_dicts(root / "source_license_policy.csv")

    check(interp_elements == ELEMENTS, "interpretable matrix uses canonical H–Og order")
    check(other_elements == ELEMENTS, "other matrix uses canonical H–Og order")
    check(len(interp_features) == int(summary["public_interpretable_features"]), "interpretable feature count matches build summary")
    check(len(other_features) == int(summary["public_other_features"]), "other feature count matches build summary")
    check(not (set(interp_features) & set(other_features)), "public matrices have no overlapping feature names")

    union = set(interp_features) | set(other_features)
    meta_names = [r["feature_name"] for r in metadata]
    check(len(meta_names) == len(set(meta_names)) == len(union), "metadata is one-to-one with public features")
    check(set(meta_names) == union, "metadata feature set equals matrix feature union")
    tier_by_feature = {r["feature_name"]: r["interpretability_tier"] for r in metadata}
    check(all(tier_by_feature[f].startswith(("A_", "B_", "C_")) for f in interp_features), "interpretable matrix contains only Tiers A-C")
    check(all(tier_by_feature[f].startswith(("D_", "E_", "F_", "G_")) for f in other_features), "other matrix contains only Tiers D-G")

    by_feature = {r["feature_name"]: r for r in metadata}
    invalid = []
    all_empty = []
    coverage_mismatch = []
    for feature in sorted(union):
        matrix = interp if feature in interp_features else other
        values = [matrix[e].get(feature, "") for e in ELEMENTS]
        populated = [v for v in values if v.strip()]
        if not populated:
            all_empty.append(feature)
        expected_coverage = int(float(by_feature[feature]["coverage_count"]))
        if len(populated) != expected_coverage:
            coverage_mismatch.append((feature, len(populated), expected_coverage))
        for element, value in zip(ELEMENTS, values):
            if not value.strip():
                continue
            try:
                number = float(value)
                if not math.isfinite(number):
                    invalid.append((element, feature, value))
            except ValueError:
                invalid.append((element, feature, value))
    check(not all_empty, "no public feature is empty for all elements")
    check(not invalid, "all populated public cells are finite numeric values")
    check(not coverage_mismatch, "metadata coverage counts match matrix values")

    check(all(r["license_status"] == "GREEN" and r["public_value_distribution"] == "include" for r in metadata), "all public feature metadata rows pass the GREEN/include gate")
    check(all(r["license_status"] == "GREEN" and r["public_value_distribution"] == "include" for r in registry), "all public source registry rows pass the GREEN/include gate")

    policy_map = {r["source_id"]: r for r in policy}
    check(len(policy_map) == 44, "licence policy contains 44 source decisions")
    check(sum(r["license_status"] == "GREEN" for r in policy) == int(summary["green_sources"]), "GREEN source count matches build summary")
    check(sum(r["license_status"] == "AMBER" for r in policy) == int(summary["amber_sources"]), "AMBER source count matches build summary")
    check(sum(r["license_status"] == "HOLD" for r in policy) == int(summary["hold_sources"]), "HOLD source count matches build summary")

    manifest = read_dicts(root / "release_core_manifest.csv")
    hash_mismatch = []
    for row in manifest:
        path = root / row["file_name"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            hash_mismatch.append(row["file_name"])
    check(not hash_mismatch, "core release files match release_core_manifest.csv")

    print(f"\nValidated {len(ELEMENTS)} elements and {len(union)} public features.")
    print("Repository snapshot validation completed successfully.")


if __name__ == "__main__":
    main()
