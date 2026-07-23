# Licensing and release gate

## Public-value rule

A source contributes numerical values to the public matrices only when:

```text
license_status == GREEN
and
public_value_distribution == include
```

The policy is machine-readable in `source_license_policy.csv`.

## Current scope

| Status | Source records | Public treatment |
|---|---:|---|
| GREEN | 26 | Values included |
| AMBER | 13 | Values excluded; local reconstruction only |
| HOLD | 5 | Values excluded; local reconstruction only |
| RED | 0 | None identified |

This release gate removed 3,434 optional features from the public matrices.

## Files

- `element_source_registry.csv` — included public sources;
- `excluded_sources.csv` — excluded AMBER/HOLD sources;
- `excluded_features.csv` — excluded feature-level records;
- `source_license_policy.csv` — source-level decision;
- `THIRD_PARTY_LICENSES.md` — human-readable notice index;
- `docs/licensing/license_audit_elemental_feature_dataset.xlsx` — detailed due-diligence workbook.

## Important limitation

`GREEN` is a project release classification, not a universal legal conclusion. Source-specific attribution, notices, database rights, model terms, and jurisdictional rules may still apply. The final public release should be reviewed by the relevant institutional office.
