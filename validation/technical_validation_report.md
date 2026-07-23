# Technical Validation report — v1.0.0

The GREEN-only public release contains **118 elements**, **822 interpretable features**, and **944 other features**. The public values are unchanged from v0.1.0; three Mendeleev Miedema-model parameters were moved from the A–C matrix to the D–G matrix after Tier adjudication.

## Results

| Status | Count |
|---|---:|
| PASS | 33 |
| PASS WITH NOTE | 5 |
| DEFERRED | 2 |
| FAIL | 0 |

All numerical, structural, provenance, licence-gate, source-fidelity, and local optional-reconstruction checks remain valid. The two deferred tests require a tagged GitHub CI run and a DOI archive.

## Tier classification review (TV-036)

An AI-assisted blinded second-pass review reclassified all 5,200 catalogue features without access to the first-review Tier or matrix partition. Exact agreement was 5,080/5,200 (97.69%), and the seven-class Cohen's κ was 0.9607. The 120 disagreements were adjudicated. TV-036 is therefore reported **PASS WITH NOTE**. This was not a second independent human reviewer; human domain-expert confirmation is recommended before claiming human inter-rater reliability in the manuscript.

## Value preservation

The 1,766 public columns were compared with the complete pre-filter catalogue after combining its two original matrices. All 208,388 feature–element cells matched exactly, including the three moved columns. Prior direct source/API evidence comprised 107,950 comparisons with zero failures. Local reconstruction of the 3,434 licence-excluded columns comprised 405,212 cells with zero mismatches at the specified tolerance.

## Release decision

**TECHNICALLY VALIDATED FOR GREEN-ONLY PUBLIC RELEASE.**
