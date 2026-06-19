# Replication Report

## Status

This is an initial public draft of the replication package. The Stata code has been organized around a repo-relative runner, but the analysis has not yet been independently executed and compared against the published article.

## What has been done

- Curated consolidated analysis data from the legacy archive.
- Preserved and curated the legacy Stata master script.
- Updated the copied master script to use repository-relative data and output paths.
- Added final zTree program files and final instructions/questionnaire materials.
- Generated an audit manifest of the source archive.

## What remains

- Run `do code/stata/run_all.do` in Stata.
- Install and confirm required Stata packages: `estout`, `esttab`, `estpost`, and `outreg2`.
- Compare generated tables and figures to the published article.
- Document exact matches, rounding differences, and any unresolved discrepancies.
- Review data-release permissions with coauthors before Zenodo deposit.

## Known caveats

- Stata is not available in the current shell environment, so the reproduction was not run here.
- Additional legacy scripts in the private source archive contain old absolute paths and exploratory commands, so they are documented in the manifest but omitted from this public draft.
- Raw zTree session files are not included pending privacy review.
