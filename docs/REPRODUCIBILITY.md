# Reproducibility

## Public snapshot validation

The committed public release can be checked without third-party Python packages:

```bash
python scripts/validate_repository_snapshot.py --repo-root .
```

The script verifies:

- 118-element H–Og row order;
- 822 and 944 feature-column counts;
- no cross-file feature-name overlap;
- exact metadata membership and coverage counts;
- finite numeric cells and blank-only missing values;
- licence gate consistency;
- core-file SHA-256 values.

This check is run by `.github/workflows/validate.yml`.

## Full 40-test validation

`scripts/validate_public_release.py` implements the full validation used to create the committed evidence. It requires local paths that are intentionally not stored in the public repository:

- the complete pre-filter dataset;
- pinned package/model assets;
- the earlier interpretable-v2 build inputs;
- locally rebuilt optional features.

Example structure:

```bash
python scripts/validate_public_release.py \
  --public-dir . \
  --full-dir /path/to/full_pre_filter_package \
  --vendor-dir /path/to/pinned_vendor_assets \
  --v2-dir /path/to/interpretable_v2_inputs \
  --optional-rebuild-dir /path/to/local_optional \
  --output-dir validation_rerun
```

The archived execution evidence is stored in `validation/`. After the Tier adjudication update, the workflow status is **33 PASS, 5 PASS WITH NOTE, 2 DEFERRED, and 0 FAIL**.

## Tier review and remaining deferred tests

- **TV-036 — PASS WITH NOTE.** An AI-assisted blinded second pass reviewed all 5,200 features. Exact agreement was 97.69% and seven-class Cohen's κ was 0.9607; 120 disagreements were adjudicated. This was not a second independent human rater, so human domain-expert confirmation remains recommended before claiming human inter-rater reliability.
- **TV-039 — DEFERRED.** Tagged GitHub Actions regression run.
- **TV-040 — DEFERRED.** Hash equivalence between the GitHub release and DOI archive.

The two deferred items require repository/archival infrastructure and are not identified data failures.


## Reproducing the adjudicated partition

`build_public_release.py` applies `curation/element_feature_metadata_adjudication_overlay.csv` by default. Use `--tier-adjudication-overlay` to specify an alternative reviewed overlay. TV-036 is supported by the records in `validation/tier_review/`; it is an AI-assisted blind second pass and not a second human reviewer.
