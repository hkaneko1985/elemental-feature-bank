# Elemental Feature Bank: October 2026 revision supplement

## Version identities

Suggested NEW GitHub tag and Zenodo version: **v1.0.2 / 1.0.2**.
This identifies the additive documentation/code package, not changed numerical data.
The core numerical dataset remains **v1.0.1**, DOI **10.5281/zenodo.21509504**,
with 118 elements, 822 interpretable columns and 944 other columns.
The old v1.0.1 tag, DOI files and core byte hashes must be preserved.
Do not rename or rebuild the original elemental-feature-bank-v1.0.1-data.zip.

This file is a prepared publication notice. It does not assert that the new tag,
new Zenodo record or new DOI already exists. Enter the actual publication date
in the new Zenodo record; 10 October 2026 is the supplement preparation date.

## Correction that supersedes the historical audit interpretation

The historical phrases "blinded second-pass review" and "independent reviewer"
are withdrawn. Initial Tier labels were visible during rule development. The
correct description is an **AI-assisted rule-based consistency audit**.
The archived label comparison still gives 5,080/5,200 agreement (97.69%) and
unweighted kappa 0.9607306. These are descriptive consistency statistics, not
accuracy, an independent validation experiment, or human inter-rater reliability.
No separate human reviewer is claimed. The reproducible Python rules do not replay
an undocumented historical ChatGPT session or require a live model/API call.

The archived forty-test result file is retained as historical evidence. The
revision reporting addendum is **34 PASS, 4 PASS WITH NOTE, 2 DEFERRED, 0 FAIL**:
TV-036 is unresolved against the original independent-rater requirement; TV-039
has public tagged-run success evidence; TV-040 remains unverified for fresh
cross-host ZIP downloads. This notice does not retrospectively claim a rerun
of all forty historical tests or a repair of the reviewer's Zenodo timeout.

## Included assets

- elemental-feature-bank-v1.0.1-data.zip: unchanged original public data archive.
- Supplementary_Code_and_Data_S1.zip: deterministic rule replay, stored label
  pairs, agreement calculation, three composition examples, eight unit tests,
  full-element coverage data, maintenance and correction notices.
- Supplementary_Methods_S1.docx: supporting explanations and Tables S1-S5.
- Revision_Figures_20261010.zip: clean Fig. 2(a-c), Fig. 3 and graphical abstract.
- REVISION_NOTES_20261010.md: this precedence/versioning notice.
- SHA256SUMS.txt: expected hashes of the five assets above; not a hash of itself.

## Scope and rights

No new property-prediction benchmark or extra feature collection is introduced.
The 3,434 licence-excluded feature values are not redistributed. Their definitions
and labels remain available. All inherited data notices remain applicable; this
package does not grant a new blanket licence. See DATA_LICENSE.md,
THIRD_PARTY_LICENSES.md and ATTRIBUTION.md in the original archive and S1/data.

Blue-marked manuscripts, reviewer comments, the response letter and submission
administration files are intentionally not included in these public uploads.

## Where to publish

GitHub project: https://github.com/hkaneko1985/elemental-feature-bank
Add revision_support/20261010/ to main, add a prominent README correction notice,
then create a NEW tag (suggested v1.0.2). Attach these exact assets to that Release.
Use the existing Zenodo record's **New version** action, not an unrelated New
upload. Import the original data ZIP and add the new assets to the draft. If the
old record contains extra files, keep them unless there is an explicit reason
not to; this list is the minimum contents of the updated record.
New version DOI: not yet assigned; it must not be replaced by the old DOI above.

Once published, the preparation-state sentences within the frozen S1/Methods
record describe their creation history. This notice and the new hosting record
provide the later deployment context. Preserve the original evidence files.
