# Supplementary Code and Data S1 — CDC revision

This supplement contains executable, target-independent demonstrations and audit
reconstruction for the revised Elemental Feature Bank Data Article. No new
property-prediction analysis has been performed. Public data and metadata copied
here are byte-identical to the v1.0.1 archive. Excluded numerical feature values
are not redistributed.

## Offline reproduction (Python 3.10 or later, standard library only)

Run from this extracted directory:

```bash
python scripts/reproduce_tier_audit.py
python scripts/composition_example.py
python -m unittest discover -s tests -v
```

Expected outcomes: 5,200 archived audit labels reproduced without mismatch;
5,080 initial/audit agreements; unweighted kappa 0.9607306169408875; nine
composition-feature rows; eight passing unit tests. Outputs are written to
`outputs/`. `--out` can be supplied to keep the supplied output files unchanged.

The statistical interpretation is **rule-based consistency**, not an independent
or blinded classification experiment. Initial classifications were available
while the rules were drafted. Historical AI model/decoding settings are not
claimed or required. See `documentation/CURATION_CORRECTION.md`.

## Optional figure reproduction

```bash
python -m pip install -r requirements_figures.txt
python scripts/plot_coverage.py
```

Every one of the 118 element symbols is shown across Fig. 2(a-c). The 34 group
identifiers are defined in `outputs/coverage_group_key.csv` / Table S1.

## Optional external archive check

```bash
python scripts/verify_archive_downloads.py
```

This requires internet access. It reports success only after separately downloading
both named assets and verifying their ZIP signatures and pinned SHA-256. Failure
of a network request is inconclusive and does not establish a Zenodo outage.
This network-dependent check is not required for the offline examples.

## Contents

- `data/`: two unchanged public matrices, metadata and inherited rights notices.
- `classification/`: label-free descriptive inputs and separately saved label pairs.
- `scripts/`: full ordered rules, metric reproduction, worked example, plotter,
  and optional fresh archive verification.
- `tests/`: eight worked-example unit tests.
- `outputs/`: executed outputs, rule IDs, confusion counts, differences, hashes,
  coverage and the revision reporting addendum.
- `access_evidence/`: exact scope of public-web observations and failed network attempts.
- `documentation/`: correction and maintenance statements.

The full historical 40-item pipeline was not rerun. Its old result file is not
silently changed. The reporting addendum retains TV-036 as unresolved against its
original independent-rater criterion, verifies the public tagged-CI summary for
TV-039, and leaves TV-040 unresolved. Current reporting counts are 34 PASS,
4 PASS WITH NOTE, 2 DEFERRED, 0 FAIL; this is not 40 completed passes.

New supplementary files are provided with the revised submission. They have not
been uploaded to GitHub or Zenodo by this preparation step. Supplementary Data S2
is the unchanged original v1.0.1 ZIP and remains the reference dataset.
