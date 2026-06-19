# Verification Guide

This guide describes what can be checked now in R and what still needs a Stata
run.

## R-only verification

From the repository root:

```bash
Rscript -e 'rmarkdown::render("code/r/replicate_descriptives.Rmd", quiet = TRUE)'
```

This renders `code/r/replicate_descriptives.html` locally and writes review
outputs to:

- `results/tables/r/`
- `results/figures/r/`

The R supplement currently checks:

- Figures 1 and 2 CDFs.
- Table 1 descriptive statistics, mean differences, and independent bootstrap
  intervals.
- Table 2 response-category shares and control-transfer means.
- Table 3 GCOS means and R test statistics.
- Result 6 control-choice proportions, Fisher exact test, Mann-Whitney test, and
  independent bootstrap interval.
- Table 4 point-estimate convention.
- Appendix A1 subject/earnings cells and aggregate questionnaire demographics.

The R outputs are intended as an independent replication supplement. They do not
yet replace the canonical Stata workflow because the published paper was built
from Stata and some details depend on Stata conventions.

## Raw-data provenance verification

The raw source archive is not included in the public repository. If you have a
local extraction of the old archive, run:

```bash
python code/python/audit_raw_sessions.py --source /path/to/Autonomy_Control
python code/python/rebuild_clean_data.py --source /path/to/Autonomy_Control
python code/python/audit_demographics.py --source /path/to/Autonomy_Control
```

These scripts write aggregate audit outputs to `docs/audit/` and ignored
row-level rebuild scratch files to `tmp/`. They do not add raw zTree exports,
free-text responses, majors, birthdates, or row-level demographics to GitHub.

## Stata verification

Once Stata is available, run from the repository root:

```stata
ssc install estout
ssc install outreg2
do code/stata/run_all.do
```

The Stata run should be compared against:

- The published article.
- `code/r/replicate_descriptives.html`.
- CSV outputs in `results/tables/r/`.

Priority checks:

1. Table 1 bootstrap confidence intervals.
2. Text-reported signed-rank, rank-sum, Kruskal-Wallis, and Fisher exact tests.
3. Table 4 marginal effects, standard errors, and stars from `mfx compute`.
4. Figures 1 and 2.
5. Appendix A1 earnings and demographic cells.

## Current known notes

- All usable raw zTree exports found in the archive appear to be represented in
  the cleaned data.
- The crash/unusable control session remains excluded.
- The paper reports seven TP10 sessions, while the cleaned data have eight TP10
  zTree run identifiers. Because subject counts and raw-session coverage match,
  this is probably a session-counting convention or article typo rather than a
  substantive missing-data issue.
- C10 Appendix A1 demographics are close but not exact: female share is
  19/44 = 43.18% versus 44%, and mean age is 21.0455 versus 21.02.
