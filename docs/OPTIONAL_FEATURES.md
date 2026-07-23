# Optional AMBER/HOLD features

## Policy

The public matrices exclude 3,434 feature columns from 18 source records classified `AMBER` or `HOLD`. Their names, metadata, reasons, and required actions are preserved in `excluded_features.csv` and `excluded_sources.csv`.

The scripts enable **local reconstruction**, not redistribution.

## 1. Create a local environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-optional.txt
```

## 2. Acquire package assets

```bash
python scripts/acquire_optional_sources.py \
  --output-dir vendor/optional \
  --xenonpy-csv /absolute/path/to/original_xenonpy_element_data.csv
```

The script downloads pinned package distributions for ElementEmbeddings 0.8.0, matminer 0.10.1, and Mendeleev 1.1.0, and records SHA-256 values in an acquisition receipt.

Some model assets or checkpoints may require manual acquisition, access acceptance, or additional evidence. Follow `excluded_sources.csv` and do not assume that package availability grants value redistribution rights.

## 3. Rebuild optional matrices

```bash
python scripts/rebuild_optional_features.py \
  --excluded-features excluded_features.csv \
  --vendor-dir vendor/optional \
  --output-dir local_optional
```

Inspect the script help before execution:

```bash
python scripts/rebuild_optional_features.py --help
```

## 4. Merge for local analysis

```bash
python scripts/merge_optional_features.py \
  --public-dir . \
  --optional-dir local_optional \
  --output-dir local_merged
```

## 5. Do not commit local values

`vendor/`, `local_optional/`, and `local_merged/` are ignored by `.gitignore`. Keep them local unless every relevant asset-level licence has been independently cleared and the source policy has been updated.

The executed release validation reconstructed all 3,434 optional columns locally and compared 405,212 cells with zero mismatches at the specified tolerance.
