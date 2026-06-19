# Coauthor Review Packet

This note is for coauthor review of the draft public replication package for:

> Gabriel Burdin, Simon D. Halliday, and Fabio Landini, "The hidden benefits of
> abstaining from control," *Journal of Economic Behavior & Organization*, 147,
> 1-12, 2018. https://doi.org/10.1016/j.jebo.2017.12.018

Repository:

`https://github.com/simondhalliday/hidden-benefits-abstaining-control`

## Purpose

The goal is to make a clean public replication package while keeping raw
human-subject materials, payment/admin files, and potentially identifying
questionnaire responses out of public GitHub.

## What is currently public

- Cleaned consolidated analysis data used by the legacy Stata workflow.
- Curated Stata analysis files with repository-relative paths.
- An R replication supplement that independently checks the main descriptive
  results, tests, figures, and regression point estimates.
- Final zTree programs and final experimental instructions/questionnaire
  materials.
- Aggregate audit reports for raw-session provenance, raw-to-clean data rebuild,
  derived variables, questionnaire demographics, and free-text privacy risk.

## What is not public

- Raw zTree session files.
- Row-level questionnaire files, open-ended responses, majors, birthdates, or
  row-level demographics.
- Payment, reimbursement, receipt, or administrative records.
- zTree executables.
- Old paper drafts, referee correspondence, literature PDFs, and unrelated
  project detritus.

## Current replication status

- The cleaned zTree analysis CSV can be rebuilt from raw zTree exports. The
  rebuild matches the committed cleaned CSV on row count, column count, ordered
  column names, and cell values within tiny floating-point differences.
- Main derived variables in the Stata analysis dataset are reproduced by script,
  including treatment indicators, transfer differences, response categories,
  final earnings, and GCOS indexes.
- The R supplement reproduces the published sample sizes and the main
  descriptive cells for Tables 1-3, renders Figures 1 and 2, computes Result 6,
  and reproduces the Table 4 point-estimate convention closely.
- The original Stata workflow still needs to be run once Stata is available, so
  Stata-specific bootstrap intervals, `mfx compute` standard errors, stars, and
  exported table formatting remain pending.

## Provenance notes

- One raw control session folder is labelled crash/unusable and is excluded from
  the cleaned analysis data.
- All non-crash raw zTree exports found in the archive appear to be represented
  in the cleaned analysis data.
- The paper reports seven TP10 sessions, while the cleaned data have eight TP10
  zTree run identifiers. Because subject counts and raw-session coverage match,
  this looks like a session-definition issue or a possible article typo rather
  than a substantive missing-data problem.
- Appendix A1 demographics appear to come from questionnaire respondents, not
  all zTree subjects.
- TP10 gender and age demographics match the paper after rounding.
- C10 demographics are close but not exact: female share is 19/44 = 43.18%
  versus the paper's 44%, and mean age is 21.0455 versus the paper's 21.02.
  This should be checked against any old table-building notes if they exist.
- The free-text privacy audit found no obvious email, phone, URL, or long-number
  patterns, but free text can still be identifying by context. The current
  recommendation is not to release raw free text publicly.

## Proposed licensing and release path

- Code: MIT License.
- Shareable cleaned data and documentation: CC-BY 4.0, pending coauthor
  approval.
- Raw source archive or restricted materials: do not put on GitHub. If preserved,
  use a restricted/private archival deposit or omit from public release.
- Tag `v1.0.0` and create a Zenodo release only after coauthors approve the
  public data scope and the Stata/R replication checks are reconciled.

## Requested coauthor decisions

1. May the cleaned consolidated analysis data be released publicly under CC-BY
   4.0?
2. Should raw zTree files be excluded entirely, archived privately, or deposited
   with restricted access?
3. Should questionnaire workbooks be excluded entirely, archived privately, or
   deposited only after redacting free text and row-level demographics?
4. Do either of you remember whether the TP10 "seven sessions" statement in the
   paper is a typo, a lab-session definition, or something else?
5. Do either of you have old table-building notes that explain the small C10
   Appendix A1 demographic discrepancies?
6. Are there any constraints from consent, IRB, lab policy, or journal policy
   that should limit public release beyond the exclusions above?

## Files worth reviewing first

- `README.md`
- `REPLICATION_REPORT.md`
- `DATA_PROVENANCE.md`
- `DEMOGRAPHICS_AUDIT.md`
- `ANALYSIS_AUDIT.md`
- `code/r/replicate_descriptives.Rmd`
