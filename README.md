# Elemental Feature Bank

[日本語版 README](README_ja.md)

## October 2026 revision: audit correction and executable examples

The core dataset remains v1.0.1 (118 elements; 822 interpretable and 944 other
features), DOI https://doi.org/10.5281/zenodo.21509504. The additive revision
materials are in [revision_support/20261010/](revision_support/20261010/).
The proposed new package tag is v1.0.2; the numerical data have not been reversioned.

**Correction:** historical "blinded second-pass review"/"independent reviewer"
wording is withdrawn. Initial labels were available during rule development.
The study reports an AI-assisted rule-based consistency audit, not independent
human inter-rater validation. Descriptive agreement remains 97.69% and kappa
0.9607306. See the correction notice and executable rules in the supplement.

The revision reporting addendum is 34 PASS, 4 PASS WITH NOTE, 2 DEFERRED, 0 FAIL.
TV-036 (independent assessment) and TV-040 (fresh cross-host archive equivalence)
remain unresolved; TV-039 has public tagged-run success evidence. The original
40-test records and old review documents below are preserved historical records,
not current claims of independent/blinded validation. This notice supersedes
conflicting historical descriptions.

The supplement includes a small composition-descriptor example with eight tests,
complete labels for all elements in Fig. 2, and an event-driven maintenance policy.
No new property-prediction benchmark or additional element data are introduced.

After depositing a new Zenodo version, append its version-specific DOI here as
"Revision supplement DOI"; retain the original DOI as "Core dataset DOI".


A provenance-aware elemental feature dataset for materials informatics. The public release contains **118 chemical elements**, **822 interpretable features**, and **944 auxiliary, learned, or encoded features**. Features from sources whose redistribution status is `AMBER` or `HOLD` are excluded from the public value matrices and can only be reconstructed locally with the provided scripts.

## Public data

| File | Elements | Feature columns | Scope |
|---|---:|---:|---|
| `element_data_interpretable.csv` | 118 | 822 | Direct, condition-resolved, and transparently derived elemental features from `GREEN` sources |
| `element_data_others.csv` | 118 | 944 | Auxiliary, empirical, learned, or encoded elemental features from `GREEN` sources |
| **Total** | **118** | **1,766** | No duplicate feature names across the two matrices |

Rows follow the canonical H–Og order. Missing values are stored as blank cells. No imputation, scaling, or dimensionality reduction has been applied.

## Quick start

```python
import pandas as pd

interpretable = pd.read_csv("element_data_interpretable.csv", index_col=0)
others = pd.read_csv("element_data_others.csv", index_col=0)
metadata = pd.read_csv("element_feature_metadata.csv")

print(interpretable.shape)  # (118, 822)
print(others.shape)         # (118, 944)
```

For model development, select feature blocks deliberately rather than concatenating all columns by default. Perform imputation, scaling, feature selection, and dimensionality reduction inside each training fold.

## Metadata and provenance

- `element_feature_metadata.csv` — one row per public feature, including source, version, unit, interpretation tier, conditions, coverage, citation, and licence gate.
- `element_feature_block_summary.csv` — feature counts and elemental coverage by block.
- `element_source_registry.csv` — source-level provenance for the 26 public `GREEN` sources.
- `source_license_policy.csv` — release decision for all 44 source records.
- `excluded_sources.csv` and `excluded_features.csv` — 18 excluded sources and 3,434 optional columns.

See [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) and [`docs/LICENSING.md`](docs/LICENSING.md).

## Optional AMBER/HOLD features

The repository does **not** redistribute the 3,434 optional feature values. Users with lawful access to the upstream assets can reconstruct them locally:

```bash
python scripts/acquire_optional_sources.py \
  --output-dir vendor/optional \
  --xenonpy-csv /path/to/original_xenonpy_element_data.csv

python scripts/rebuild_optional_features.py \
  --excluded-features excluded_features.csv \
  --vendor-dir vendor/optional \
  --output-dir local_optional

python scripts/merge_optional_features.py \
  --public-dir . \
  --optional-dir local_optional \
  --output-dir local_merged
```

Exact arguments and prerequisites are documented in [`docs/OPTIONAL_FEATURES.md`](docs/OPTIONAL_FEATURES.md). Locally reconstructed values must not be recommitted unless their asset-level redistribution rights have been independently cleared.

## Technical Validation

The release was evaluated with 40 prespecified tests:

| Result | Count |
|---|---:|
| PASS | 33 |
| PASS WITH NOTE | 5 |
| DEFERRED | 2 |
| FAIL | 0 |

Validation included **107,950 direct source/API comparisons** with zero failures and **405,212 locally reconstructed optional cells** with zero mismatches at the specified tolerance. The two deferred tests require a tagged GitHub Actions run and a DOI archive.

- Human-readable report: [`validation/technical_validation_report.md`](validation/technical_validation_report.md)
- Results table: [`validation/technical_validation_results.csv`](validation/technical_validation_results.csv)
- Execution workbook: [`validation/technical_validation_execution_results.xlsx`](validation/technical_validation_execution_results.xlsx)
- Lightweight repository snapshot check:

```bash
python scripts/validate_repository_snapshot.py --repo-root .
```

The GitHub Actions workflow runs the same snapshot check on pushes and pull requests. The full 40-test workflow requires local source assets that are intentionally not committed; see [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Tier classification review

All 5,200 catalogue features underwent an AI-assisted blinded second-pass review. The input omitted the first-review Tier and matrix partition. Exact agreement was **97.69%** and the seven-class Cohen's κ was **0.9607**. After adjudication, three Mendeleev Miedema-model parameters moved from the interpretable matrix to the other matrix; no values changed.

This review is not a second independent human rater. Human domain-expert confirmation is recommended before the associated manuscript claims human inter-rater reliability. Machine-readable evidence is in [`validation/tier_review/`](validation/tier_review/).

## Repository structure

```text
.
├── element_data_interpretable.csv
├── element_data_others.csv
├── element_feature_metadata*.csv
├── element_source_registry.csv
├── excluded_*.csv
├── source_license_policy.csv
├── scripts/
├── validation/
├── docs/
└── .github/workflows/validate.yml
```

## Author and funding

- **Author:** Hiromasa Kaneko, Department of Applied Chemistry, School of Science and Technology, Meiji University
- **Repository:** https://github.com/hkaneko1985/elemental-feature-bank
- **Funding:** This work was supported by Grants-in-Aid for Scientific Research (KAKENHI) (Grant Numbers 24K08152 and 24K01234) from the Japan Society for the Promotion of Science.

See [`AUTHORS.md`](AUTHORS.md) and [`FUNDING.md`](FUNDING.md).

## Citation

The repository includes a completed [`CITATION.cff`](CITATION.cff) for release v1.0.1. Cite the versioned dataset release and the associated Data Descriptor when available. Add the archival DOI to `CITATION.cff` and `.zenodo.json` after deposit.

## Licence and attribution

This repository does not apply a single blanket licence to all third-party values. Public values are limited to sources classified `GREEN`, but source-specific attribution and reuse conditions still apply.

- Project-authored code licence template, with the copyright holder completed but not activated as `LICENSE`: `LICENSE_CODE.template`
- Dataset-rights notice: `DATA_LICENSE.md`
- Source-level notices: `THIRD_PARTY_LICENSES.md`
- Scientific attribution: `ATTRIBUTION.md`

The licence classification is research-data due diligence, not legal advice. Obtain institutional review before assigning the final repository and data licences.

## Development and contributions

Data corrections and new source proposals are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md). A proposed change must include a primary source, units and reference state, redistribution evidence, updated metadata, and validation results.
