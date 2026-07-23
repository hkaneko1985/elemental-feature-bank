# Elemental Feature Bank v1.0.1

## Patch summary

Version 1.0.1 is a packaging and continuous-integration correction. Scientific
data values, feature names, Tier assignments, and public matrix dimensions are
unchanged from v1.0.0.

The v1.0.0 GitHub Actions run failed because:

1. CSV files were hashed before Git normalized CRLF line endings to LF according
   to `.gitattributes`; and
2. an ignored `*.log` file was included in the old manifest.

Version 1.0.1 fixes this by:

- normalizing tracked text files to LF before manifest creation;
- restricting `release_core_manifest.csv` to twelve stable core-release files;
- excluding ignored log files;
- providing a manifest-regeneration utility; and
- printing exact hash mismatches in the validator.

## Public data

- `element_data_interpretable.csv`: 118 elements × 822 features
- `element_data_others.csv`: 118 elements × 944 features
- Total public features: 1,766
- Licence-excluded optional features: 3,434

No scientific data value was changed.
