#!/usr/bin/env python3
"""Regenerate release_core_manifest.csv from the Git-normalized working tree."""
from __future__ import annotations
import csv
import hashlib
from pathlib import Path

CORE_FILES = [
    "build_summary.json",
    "element_data_interpretable.csv",
    "element_data_others.csv",
    "element_feature_block_summary.csv",
    "element_feature_metadata.csv",
    "element_feature_metadata_interpretable.csv",
    "element_feature_metadata_others.csv",
    "element_source_registry.csv",
    "excluded_features.csv",
    "excluded_sources.csv",
    "input_manifest.csv",
    "source_license_policy.csv",
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

root = Path(__file__).resolve().parents[1]
with (root / "release_core_manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["file_name", "size_bytes", "sha256"])
    for rel in CORE_FILES:
        p = root / rel
        w.writerow([rel, p.stat().st_size, sha256(p)])
print("Updated release_core_manifest.csv for the current Git-normalized checkout.")
