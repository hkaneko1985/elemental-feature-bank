# October 2026 revision support

This is an additive, frozen supplement to the Elemental Feature Bank core data
v1.0.1. Proposed package release: v1.0.2. It does not alter root CSVs, metadata,
core manifests or archived validation records.

Read **REVISION_NOTES_20261010.md** first: it supersedes the historical descriptions
of a "blinded" or "independent" Tier review. The audit is related rule-based
consistency, not independent human validation. Current reporting also corrects
TV-036/039 without rewriting the historical checklist.

Files: Supplementary_Methods_S1.docx; figures/; Supplementary_Code_and_Data_S1/.

## Offline reproduction

Use Python 3.10 or later. Open a terminal in Supplementary_Code_and_Data_S1.
To keep the archived outputs unchanged, use a temporary output directory:

```powershell
python scripts/reproduce_tier_audit.py --out "$env:TEMP/efb_revision_check/audit"
python scripts/composition_example.py --out "$env:TEMP/efb_revision_check/example"
python -m unittest discover -s tests -v
```

Expected: 5,200 reproduced labels, no label-replay mismatch; 5,080 agreements;
unweighted kappa about 0.9607306; nine example rows; eight tests pass. No model
training is performed. The inherited root GitHub Actions workflow checks the
core snapshot, not automatically these new supplementary commands.

The local .gitattributes fixes this supplement's bytes against line-ending
conversion. Keep it when copying. Existing root manifests describe the historical
core/repository snapshot and are NOT a current inventory of this additive folder.
REVISION_SHA256SUMS.txt inventories the frozen files here (excluding itself).

Do not upload reviewer responses or blue-marked manuscripts to this folder.
