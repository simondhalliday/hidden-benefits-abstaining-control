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
- The Stata script appears to generate the two published cumulative distribution
  figures and the regression outputs underlying Table 4, but exact execution and
  output comparison remain pending.

## Paper Results Map

| Published item | Paper target | Current source in repo | Current status |
| --- | --- | --- | --- |
| Fig. 1 | CDF of control and no-control transfers in C10, agents only, n = 38 | `code/stata/master_do_file.do`, Result 1 block; `data/processed/merged_treatment_control.dta` | Requires Stata execution; data sample size verified |
| Table 1 | Mean, SD, quartiles, and bootstrap CI for control/no-control transfers in C10 and TP10 | `code/stata/master_do_file.do`, Result 2 block; `data/processed/merged_treatment_control.dta` | Descriptive cells verified; bootstrap CIs require Stata or independent replication |
| Fig. 2 | CDF of control and no-control transfers in TP10, agents only, n = 53 | `code/stata/master_do_file.do`, Result 3 block; `data/processed/merged_treatment_control.dta` | Requires Stata execution; data sample size verified |
| Table 2 | Shares of negative/neutral/positive response categories and mean control transfers by category | `code/stata/master_do_file.do`, Result 5 block; `data/processed/merged_treatment_control.dta` | Numeric cells verified after label-orientation check below |
| Text Result 6 | Control-choice proportions: 63.15% in C10 and 77.34% in TP10, Fisher exact p = 0.163 | `code/stata/master_do_file.do`, Result 6 block; `data/processed/merged_treatment_control.dta` | Proportions verified; Fisher exact and bootstrap CI require execution |
| Table 3 | GCOS agent-scale means and tests by treatment | `code/stata/master_do_file.do`, GCOS block; `data/processed/merged_treatment_control.dta` | Means verified; test statistics require execution |
| Table 4 | OLS/logit marginal-effect regressions with treatment and standardized GCOS scales | `code/stata/master_do_file.do`, GCOS regression block | Requires Stata execution and comparison |
| Appendix Table A1 | Session counts, subject counts, gender, age, and earnings by treatment | `data/processed/merged_treatment_control.dta`; source questionnaire/payment variables need review | Some sample counts verified; full table requires variable audit |

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

`code/r/replicate_descriptives.Rmd` provides an independent R-based descriptive
check of the included Stata data. At this stage it is a supplement, not a
replacement for the original Stata analysis, because exact parity for bootstrap
confidence intervals, logit marginal effects, and table formatting still needs
to be checked carefully.

## Open Issues

- Stata is needed for the canonical replication run.
- The original master script mixes direct exported artifacts with statistics
  printed to the log. Publication-ready reproduction may require adding explicit
  table-export code for Tables 1 and 2.
- Appendix Table A1 needs a fuller audit of gender, age, and payment variables
  against the original questionnaire/payment files before publication.
- Any public Zenodo deposit should wait for coauthor approval, especially for raw
  zTree files and any material containing payment, demographic, or session-level
  records.
