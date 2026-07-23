# Elemental Feature Bank v1.0.0

## Summary

Version 1.0.0 is the first stable, citation-ready release of the Elemental Feature Bank.
It preserves the Tier-adjudicated public matrices and the complete provenance,
licence, reconstruction, and Technical Validation records.

## Public data

- `element_data_interpretable.csv`: 118 elements × **822** features
- `element_data_others.csv`: 118 elements × **944** features
- Total public features: **1,766**
- Licence-excluded optional features: **3,434**

## Tier review

An AI-assisted blinded second pass reviewed all 5,200 catalogue features without
access to the first-review Tier or matrix partition.

- Exact agreement: 5,080 / 5,200 (**97.69%**)
- Seven-class Cohen's κ: **0.9607**
- Non-G Cohen's κ: **0.9189**
- A–C versus D–G κ: **0.9973**
- Adjudicated disagreements: **120**

Three GREEN-source Mendeleev Miedema-model parameters are assigned to the
other/auxiliary matrix rather than the interpretable matrix:

- `mend_elem__en_miedema`
- `mend_elem__miedema_molar_volume`
- `mend_elem__miedema_electron_density`

The review is AI-assisted and is not a second independent human rater.

## Technical Validation

- PASS: 33
- PASS WITH NOTE: 5
- DEFERRED: 2
- FAIL: 0

TV-039 and TV-040 are intentionally deferred until the tagged GitHub Actions run
and GitHub–Zenodo archive hash comparison have been completed.

## Author and repository

- Author: Hiromasa Kaneko
- Repository: https://github.com/hkaneko1985/elemental-feature-bank
- Version: 1.0.0
- Funding: This work was supported by Grants-in-Aid for Scientific Research
  (KAKENHI) (Grant Numbers 24K08152 and 24K01234) from the Japan Society for
  the Promotion of Science.
