# Analysis Audit

This audit maps the published article to the current replication package and
separates what can be checked from the included data from what still requires a
Stata execution audit.

Published article:

> Gabriel Burdin, Simon D. Halliday, and Fabio Landini, "The hidden benefits of
> abstaining from control," *Journal of Economic Behavior & Organization*, 147,
> 1-12, 2018. https://doi.org/10.1016/j.jebo.2017.12.018

## Current Audit Status

- The public draft contains the consolidated Stata analysis data, pooled
  comparison data, the curated master Stata script, and final experimental
  materials.
- Stata is not currently available in the local shell environment, so the full
  Stata replication has not yet been executed.
- The included Stata data reproduce the published sample sizes and the headline
  descriptive statistics for Tables 1-3 and Appendix Table A1.
- The cleaned zTree analysis data can now be rebuilt from the raw zTree exports
  with `code/python/rebuild_clean_data.py`; the rebuild matches the committed
  cleaned CSV and derived Stata variables within floating-point tolerance.
- The Stata script appears to generate the two published cumulative distribution
  figures and the regression outputs underlying Table 4, but exact execution and
  output comparison remain pending.

## Paper Results Map

| Published item | Paper target | Current source in repo | Current status |
| --- | --- | --- | --- |
| Fig. 1 | CDF of control and no-control transfers in C10, agents only, n = 38 | `code/stata/master_do_file.do`, Result 1 block; `data/processed/merged_treatment_control.dta`; `code/r/replicate_descriptives.Rmd` | R figure renders; Stata figure still pending |
| Table 1 | Mean, SD, quartiles, and bootstrap CI for control/no-control transfers in C10 and TP10 | `code/stata/master_do_file.do`, Result 2 block; `data/processed/merged_treatment_control.dta`; `code/r/replicate_descriptives.Rmd` | Descriptive cells verified; R bootstrap normal CIs added; Stata bootstrap still pending |
| Fig. 2 | CDF of control and no-control transfers in TP10, agents only, n = 53 | `code/stata/master_do_file.do`, Result 3 block; `data/processed/merged_treatment_control.dta`; `code/r/replicate_descriptives.Rmd` | R figure renders; Stata figure still pending |
| Table 2 | Shares of negative/neutral/positive response categories and mean control transfers by category | `code/stata/master_do_file.do`, Result 5 block; `data/processed/merged_treatment_control.dta` | Numeric cells verified after label-orientation check below |
| Text Result 6 | Control-choice proportions: 63.15% in C10 and 77.34% in TP10, Fisher exact p = 0.163 | `code/stata/master_do_file.do`, Result 6 block; `data/processed/merged_treatment_control.dta`; `code/r/replicate_descriptives.Rmd` | Proportions, Fisher exact test, Mann-Whitney test, and R bootstrap CI added; Stata still pending |
| Table 3 | GCOS agent-scale means and tests by treatment | `code/stata/master_do_file.do`, GCOS block; `data/processed/merged_treatment_control.dta`; `code/r/replicate_descriptives.Rmd` | Means and R test statistics added; Stata still pending |
| Table 4 | OLS/logit marginal-effect regressions with treatment and standardized GCOS scales | `code/stata/master_do_file.do`, GCOS regression block; `code/r/replicate_descriptives.Rmd` | R point estimates added and match published convention closely; Stata standard errors/stars still pending |
| Appendix Table A1 | Session counts, subject counts, gender, age, and earnings by treatment | `data/processed/merged_treatment_control.dta`; `code/python/audit_raw_sessions.py`; `code/python/rebuild_clean_data.py`; source questionnaire/payment variables need review | Subject and earnings cells mostly verified; crash export excluded; questionnaire demographics partially audited; TP10 has eight zTree run IDs but paper reports seven sessions |

## Verified Descriptive Checks

These checks were computed from `data/processed/merged_treatment_control.dta`
without running Stata.

### Agent Sample Sizes

| Treatment | Agents |
| --- | ---: |
| C10 | 38 |
| TP10 | 53 |

These match the paper's reported `n = 38` for C10 and `n = 53` for TP10.

### Table 1 Descriptive Cells

| Treatment | Variable | Mean | SD | Q1 | Median | Q3 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| C10 | Control transfer | 17.47 | 11.76 | 10 | 10 | 20 |
| C10 | No-control transfer | 21.24 | 19.03 | 0 | 18.5 | 40 |
| TP10 | Control transfer | 18.00 | 11.62 | 10 | 10 | 25 |
| TP10 | No-control transfer | 12.87 | 15.50 | 0 | 5 | 30 |

The mean differences are:

| Treatment | Mean of xNC - xC |
| --- | ---: |
| C10 | 3.76 |
| TP10 | -5.13 |

These match Table 1. The published confidence intervals require the bootstrap
routine in the Stata script or an independently matched bootstrap implementation.

### Table 2 Category Orientation

The dataset contains `controlneg`, `controlneutral`, and `controlpos` labels from
the perspective of response to control. Published Table 2 labels the columns as
responses to control abstinence. This reverses the verbal interpretation of the
non-neutral categories:

- Published "Negative" response to control abstinence corresponds to cases where
  control transfer exceeds no-control transfer, i.e. `controlpos == 1` in the
  current data.
- Published "Positive" response to control abstinence corresponds to cases where
  no-control transfer exceeds control transfer, i.e. `controlneg == 1` in the
  current data.
- Neutral maps directly to `controlneutral == 1`.

With that orientation, the published Table 2 cells are reproduced:

| Treatment | Published category | Share | Mean control transfer | SD |
| --- | --- | ---: | ---: | ---: |
| C10 | Negative | 36.84% | 11.64 | 4.40 |
| C10 | Neutral | 21.05% | 25.13 | 19.16 |
| C10 | Positive | 42.11% | 18.75 | 9.40 |
| TP10 | Negative | 54.72% | 10.76 | 2.21 |
| TP10 | Neutral | 41.51% | 27.36 | 12.67 |
| TP10 | Positive | 3.77% | 20.00 | 7.07 |

### Table 3 GCOS Means

| Scale | C10 mean | TP10 mean |
| --- | ---: | ---: |
| Autonomy | 73.53 | 71.30 |
| Impersonal | 43.32 | 44.19 |
| Control | 59.66 | 58.45 |

These match Table 3. The t-statistics and Mann-Whitney statistics still require
Stata execution or an explicitly matched independent implementation.

### Result 6 Control Choice Proportions

| Treatment and role | Observations | Share choosing control |
| --- | ---: | ---: |
| C10 principals | 38 | 63.16% |
| TP10 third parties | 53 | 77.36% |

These match the paper's rounded proportions of 63.15% and 77.34%, allowing for
rounding conventions. Fisher's exact test and the bootstrap confidence interval
remain pending.

## Stata Execution Checklist

Run from the repository root:

```stata
ssc install estout
ssc install outreg2
do code/stata/run_all.do
```

Then check that the following files are created:

- `results/logs/halliday.txt`
- `results/figures/cumul_exp1.pdf`
- `results/figures/cumul_exp2.pdf`
- `results/figures/kdensity_gcos.pdf`
- `results/tables/agent_regressions_tests.doc`
- `results/tables/agent_regressions_tests_lpm.doc`
- `results/tables/gcos_agents.rtf`
- `results/tables/gcos2_agents.rtf`
- `results/tables/gcos.rtf`
- `results/tables/gcos2.rtf`
- `results/tables/agent_regressions_gcos.doc`
- `results/tables/agent_regressions_gcos_lpm.doc`
- `results/tables/mlogits.doc`
- `results/tables/mlogits_pooled.doc`

The next audit pass should compare:

1. Graph shapes and sample sizes against Figs. 1 and 2.
2. Bootstrap confidence intervals against Table 1.
3. Wilcoxon/ranksum/Fisher exact p-values against the reported text.
4. Table 4 coefficients, significance stars, and marginal effects.
5. Appendix Table A1 demographic and earnings summaries.

## R Replication Supplement

`code/r/replicate_descriptives.Rmd` provides an independent R-based replication
supplement. It now covers the main descriptive cells, CDF figures, bootstrap
checks, nonparametric tests, Result 6 control-choice tests, and a Table 4
point-estimate check. At this stage it is still a supplement, not a replacement
for the original Stata analysis, because exact Stata parity for bootstrap
conventions, `mfx compute` standard errors, stars, and table formatting still
needs to be checked carefully.

## Raw-To-Clean Rebuild

`code/python/rebuild_clean_data.py` rebuilds the subject-level zTree analysis
CSV from raw zTree exports in the private archive extraction. The current rebuild
passes all raw-to-clean checks:

- 235 rebuilt rows versus 235 committed cleaned rows.
- 98 rebuilt columns versus 98 committed cleaned columns.
- Ordered column names match.
- Cell values match within tolerance, with maximum numeric difference
  `4.991552934e-07`.

The same script derives the main analysis variables in
`data/processed/merged_treatment_control.dta`. All audited derived variables pass
against the committed Stata data within tolerance.

## Open Issues

- Stata is needed for the canonical replication run.
- The original master script mixes direct exported artifacts with statistics
  printed to the log. Publication-ready reproduction may require adding explicit
  table-export code for Tables 1 and 2.
- Appendix Table A1 needs a fuller audit of gender, age, and payment variables
  against the original questionnaire/payment files before publication. The raw
  zTree audit suggests the TP10 session-count discrepancy is likely a difference
  between zTree run identifiers and the session definition used in the paper.
- Any public Zenodo deposit should wait for coauthor approval, especially for raw
  zTree files and any material containing payment, demographic, or session-level
  records.
