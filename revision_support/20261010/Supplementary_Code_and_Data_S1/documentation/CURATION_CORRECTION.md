# Correction to the interpretation of the historical Tier audit

The v1.0.1 files, labels and numerical data are preserved. The historical phrases
“blinded second pass” and “independent reviewer” are not supported by the rule-
development record: initial Tier labels were visible when the rules were devised.
Excluding those fields at classifier execution does not establish blind rule design.

The revised paper reports a **rule-based consistency audit**. The stored initial
and audit labels still yield 5,080/5,200 agreement and unweighted kappa 0.9607306.
These are descriptive statistics, not independent-rater reliability or accuracy.
The 120 decisions are rule-based resolutions, not an independent human consensus.

The script `tier_rules.py` is an executable reconstruction of the recorded branch
logic. It reproduces every archived audit label. It does not replay a ChatGPT
conversation; historical model/decoding settings were not retained and are not
invented. No second human rater is claimed.

TV-036 remains unresolved against its original independent-assessment criterion.
The separate reporting addendum makes this correction explicit and preserves the
historical result file. The public GitHub tagged CI summary now supports TV-039;
TV-040 remains unverified for a fresh Zenodo-versus-GitHub binary comparison.
