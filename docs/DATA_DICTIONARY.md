# Data dictionary

## Matrix format

Both matrices are CSV files with one row per element and one column per feature. The first column is the element symbol; rows are ordered by atomic number from H to Og.

| File | Feature columns | Meaning |
|---|---:|---|
| `element_data_interpretable.csv` | 822 | Tiers A–C: direct, condition-resolved direct, and transparently derived features |
| `element_data_others.csv` | 944 | Tiers D–G: contextual/empirical, engineered, relational, and learned/encoded features |

A populated cell is numeric. Missing values are blank. No imputation or scaling has been applied.

## Core metadata columns

| Column | Meaning |
|---|---|
| `dataset_file` | Matrix containing the feature |
| `feature_name` | Exact CSV column name |
| `feature_block` | Source/semantic block |
| `source`, `source_version`, `source_url` | Provenance |
| `description`, `unit` | Meaning and unit |
| `recommended_citation` | Primary citation guidance |
| `coverage_count`, `coverage_percent`, `missing_count` | Elemental coverage |
| `interpretability_tier`, `tier_label` | A–G classification |
| `direct_or_derived`, `formula`, `input_features` | Derivation information |
| `reference_state` | Physical or computational reference state |
| `charge_state`, `isotope_mass_number`, `spin_multiplicity` | Condition variables |
| `temperature_K`, `pressure_Pa`, `photon_energy_eV`, `wavelength_nm` | Experimental/computational conditions |
| `crystal_structure`, `space_group`, `polymorph`, `miller_index` | Structure-dependent context |
| `experimental_or_calculated`, `calculation_method` | Origin of the value |
| `source_id`, `license_status`, `public_value_distribution` | Licence gate |

The complete metadata schema is represented directly by the header of `element_feature_metadata.csv`.

## Interpretability tiers

| Tier | Meaning | Public matrix |
|---|---|---|
| A | Strict direct elemental or atomic quantity | Interpretable |
| B | Direct quantity with explicit charge, isotope, energy, structure, or other condition | Interpretable |
| C | Transparent derived quantity with documented formula/aggregation | Interpretable |
| D | Empirical, contextual, historical, or socioeconomic scale | Others |
| E | Engineered arithmetic descriptor | Others |
| F | Relational or element-pair aggregate | Others |
| G | Learned or encoded representation whose coordinates lack standalone physical definitions | Others |

Only licence-cleared (`GREEN`) features are present in the two public matrices.


## Tier adjudication in v1.0.0

The AI-assisted blinded second pass reassigned 120 catalogue features. Three public Mendeleev Miedema-model parameters crossed the A-C/D-G boundary and are now in `element_data_others.csv`. See `validation/tier_review/` and `curation/public_matrix_partition_patch.csv`.
