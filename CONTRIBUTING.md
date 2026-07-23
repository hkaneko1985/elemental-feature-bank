# Contributing

Contributions are welcome when they improve correctness, provenance, interpretability, or reproducibility.

## Report a data issue

Open a **Data error** issue and include:

- element and feature name;
- current and proposed value;
- unit and reference state;
- primary source and exact page/table/record;
- source version or retrieval date;
- whether the change affects other elements or derived columns.

## Propose a new data source

A proposed source must include:

1. a stable source URL or DOI;
2. version/tag/commit and retrieval date;
3. asset-level redistribution evidence;
4. scientific citation;
5. unit, reference state, and condition variables;
6. elemental coverage and missingness policy;
7. a proposed A–G interpretability tier;
8. a deterministic extraction or transformation script.

Sources without clear redistribution rights must remain script-only and may not add numerical values to the public matrices.

## Pull-request requirements

A pull request that changes data must update, as applicable:

- the two public matrices;
- feature metadata and source registry;
- feature-block summary;
- licence policy and attribution;
- validation evidence;
- `release_core_manifest.csv` and `DATA_SHA256SUMS.txt`;
- `CHANGELOG.md`.

Run before submitting:

```bash
python scripts/validate_repository_snapshot.py --repo-root .
```

Do not commit downloaded model weights, private files, or locally reconstructed AMBER/HOLD values.
