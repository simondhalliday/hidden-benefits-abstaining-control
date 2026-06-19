# Replication Report

## Status

This is an initial public draft of the replication package. The Stata code has been organized around a repo-relative runner, but the analysis has not yet been independently executed and compared against the published article.

## What has been done

- Curated consolidated analysis data from the legacy archive.
- Preserved and curated the legacy Stata master script.
- Updated the copied master script to use repository-relative data and output paths.
- Added final zTree program files and final instructions/questionnaire materials.
- Generated an audit manifest of the source archive.
- Added `ANALYSIS_AUDIT.md` mapping published results to the current code/data.
- Added `code/r/replicate_descriptives.Rmd`, an R-based replication supplement
  that currently reproduces the main published descriptive cells for Tables
  1-3, renders the CDF figures, adds bootstrap and nonparametric checks, checks
  Result 6, and reproduces the Table 4 point-estimate convention.
- Added `code/python/rebuild_clean_data.py`, which rebuilds the cleaned zTree
  analysis data from raw zTree exports and derives the main Stata analysis
  variables. The current rebuild passes all committed raw-to-clean and
  derived-variable audit checks.
- Added `code/python/audit_demographics.py` and `DEMOGRAPHICS_AUDIT.md`, which
  audit Appendix A1 questionnaire demographics and screen free-text fields
  without exporting raw questionnaire rows.
- Expanded `code/r/replicate_descriptives.Rmd` with a third-party status table,
  published-target checks, and Appendix A1 demographic audit output.
- Added `COAUTHOR_REVIEW_PACKET.md` to summarize the public data scope and
  coauthor approval questions.

## What remains

- Run `do code/stata/run_all.do` in Stata.
- Install and confirm required Stata packages: `estout`, `esttab`, `estpost`, and `outreg2`.
- Compare generated tables and figures to the published article.
- Document exact matches, rounding differences, and any unresolved discrepancies.
- Review data-release permissions with coauthors before Zenodo deposit.
- Compare the R supplement against Stata once Stata is available, especially
  bootstrap conventions, `mfx compute` standard errors, and publication table
  formatting.
- Resolve the remaining Appendix A1 provenance notes: C10 demographic cells are
  close but not exact, and TP10 has eight zTree run IDs versus seven sessions in
  the paper. The TP10 count does not appear to affect subject counts or main
  results and may be a session-definition convention or article typo.

## Known caveats

- Stata is not available in the current shell environment, so the reproduction was not run here.
- Additional legacy scripts in the private source archive contain old absolute paths and exploratory commands, so they are documented in the manifest but omitted from this public draft.
- Raw zTree session files are not included pending privacy review.
- Raw questionnaire rows, free-text responses, majors, birthdates, and row-level
  demographics are not included. The current free-text screen found no obvious
  direct-identifier patterns, but contextual disclosure risk remains.
