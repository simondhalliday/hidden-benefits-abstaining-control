# The Hidden Benefits of Abstaining from Control

Replication materials for:

> Gabriel Burdin, Simon D. Halliday, and Fabio Landini, "The hidden benefits of abstaining from control," *Journal of Economic Behavior & Organization*, 147, 1-12, 2018. https://doi.org/10.1016/j.jebo.2017.12.018

This repository is a working public draft of the replication package. It preserves the cleaned analysis data, Stata code, and experimental instruments currently identifiable from the project archive. It does **not** include the full legacy archive, literature PDFs, payment/reimbursement records, zTree executables, old paper drafts, or raw session output files that still require privacy and coauthor review.

## Current status

- Version: draft `v0.1`.
- Reproduction status: not yet independently verified.
- Main analysis language: Stata, originally written for Stata 13.
- External Stata packages used by the original scripts: `estout`, `esttab`, `estpost`, and `outreg2`.
- Data archive DOI: pending Zenodo deposit after coauthor review.

## Repository structure

```text
code/stata/                 Stata run script and curated master analysis file
code/r/                     R-based descriptive replication supplement
data/processed/             Consolidated analysis data included in this draft
instruments/ztree/          Final zTree treatment/questionnaire programs
instruments/instructions/   Final instructions, questionnaire, and appendix files
paper/                      Citation and article metadata
results/                    Empty output folders for generated logs, tables, figures
docs/audit/                 Source archive manifest and publication-readiness notes
```

## How to run

1. Clone the repository.
2. Open Stata.
3. Change Stata's working directory to the repository root.
4. Install the legacy table-output dependencies if needed:

```stata
ssc install estout
ssc install outreg2
```

5. Run:

```stata
do code/stata/run_all.do
```

The script writes logs to `results/logs/`, figures to `results/figures/`, and tables to `results/tables/`.

An R-based descriptive supplement is also available:

```r
rmarkdown::render("code/r/replicate_descriptives.Rmd")
```

The R document currently verifies the main descriptive cells for Tables 1-3,
renders the CDF figures, adds bootstrap and nonparametric checks, checks the
Result 6 control-choice tests, and reproduces the Table 4 point-estimate
convention. It also includes an Appendix A1 status table that pulls from the
aggregate demographics audit. It does not yet replace the canonical Stata
workflow for exact Stata bootstrap conventions, `mfx compute` standard errors,
or final publication table formatting.

The cleaned zTree analysis data can be rebuilt from the private source archive
extraction with:

```bash
python code/python/rebuild_clean_data.py --source /path/to/Autonomy_Control
```

This writes row-level rebuilt files to ignored `tmp/` outputs and aggregate audit
reports to `docs/audit/`.

Questionnaire demographics and free-text privacy risk can be audited in
aggregate with:

```bash
python code/python/audit_demographics.py --source /path/to/Autonomy_Control
```

This writes aggregate audit reports only. It does not export raw free-text
responses, majors, birthdates, or row-level demographics.

## Data included

The draft includes consolidated analysis data only:

- `data/processed/merged_control_treatment.csv`
- `data/processed/merged_treatment_control.dta`
- `data/processed/merged_kf_ziegel.csv`

The raw zTree session files and row-level questionnaire files remain excluded
pending privacy and coauthor review. See `DATA_PROVENANCE.md`,
`DEMOGRAPHICS_AUDIT.md`, and `docs/audit/source_manifest.csv`.

`COAUTHOR_REVIEW_PACKET.md` summarizes the proposed public data scope, remaining
provenance notes, and release decisions for Gabriel Burdin and Fabio Landini.

## Citation

Please cite the published article and, once available, the archived replication package DOI listed in `CITATION.cff`.

## License

Code is released under the MIT License. Shareable data and documentation are intended for CC-BY 4.0, subject to final coauthor and data-rights review. See `LICENSE` and `LICENSE-DATA.md`.
