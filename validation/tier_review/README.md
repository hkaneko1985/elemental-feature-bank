# Tier classification second-review package

Prepared: 2026-07-18

This package contains an **AI-assisted blinded second-pass review** of the A–G interpretability classification for all 5,200 elemental features.

## Scope

- Public features reviewed: 1,766
- Licence-excluded optional features reviewed: 3,434
- Total: 5,200
- Feature blocks: 47

The second-pass input excluded the first-review Tier, dataset partition, interpretability decision/class, curation rule/notes, and `include_in_recommended_main`. Classification used names, blocks, sources, descriptions, units, formulas, input dependencies, and condition fields.

## Agreement results

- Exact agreement: 5,080 / 5,200 = 97.69%
- Cohen's kappa, seven nominal classes: 0.9607
- Cohen's kappa excluding Tier G: 0.9189
- Binary A–C versus D–G kappa: 0.9973
- Blocks with complete agreement: 40 / 47
- Feature-level disagreements adjudicated: 120

The pre-specified kappa target of 0.80 was exceeded.

## Main reclassification groups

- B → C: 44
- A → B: 41
- A → C: 28
- A → D: 6
- C → A: 1

## Public matrix impact

Three GREEN-source features cross the A–C / D–G boundary:

- `mend_elem__en_miedema`
- `mend_elem__miedema_molar_volume`
- `mend_elem__miedema_electron_density`

The adjudicated preview therefore contains:

- 822 interpretable features
- 944 other features
- 1,766 total public features

The current public release is **not overwritten** by this package.

## Key files

- `Tier分類_第二評価者レビュー報告書.docx` / `.pdf`
- `tier_classification_second_reviewer.xlsx`
- `reviewer2_blinded_input.csv`
- `reviewer2_assignments.csv`
- `interpretability_adjudication.csv`
- `element_feature_metadata_adjudication_overlay.csv`
- `tier_review_block_summary.csv`
- `tier_confusion_matrix.csv`
- `tier_agreement_metrics.csv`
- `public_matrix_partition_patch.csv`
- `adjudicated_preview/`
- `apply_tier_adjudication.py`
- `technical_validation_results_TV036_updated.csv`
- `manuscript_Tier_review_text_ja.md`

## Technical Validation status

The proposed TV-036 status is `PASS WITH NOTE`.

Updated overall status counts:

- PASS: 33
- PASS WITH NOTE: 5
- DEFERRED: 2
- FAIL: 0

## Important limitation

This is not a second independent **human** reviewer. It is an AI-assisted blinded rubric pass. Before stating in a manuscript that two independent human raters performed the classification, obtain a separate human domain-expert review and retain the signed adjudication record.
