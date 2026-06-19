# Data Provenance

## Source archive

The package was curated from the old project archive:

`/Users/shalliday/Dropbox/My Mac (MacBook-Pro)/Downloads/Autonomy_Control-20260619T102557Z-3-001.zip`

The archive contains 622 files, including zTree programs, experiment outputs, consolidated data, Stata scripts, paper drafts, literature PDFs, reimbursement files, and presentation material. The full archive is not committed to GitHub.

## Included data

The following files are included because they are consolidated analysis data rather than raw session output:

| Repository path | Source path | Notes |
| --- | --- | --- |
| `data/processed/merged_treatment_control.dta` | `Autonomy_Control/Stata/merged_treatment_control.dta` | Stata dataset loaded by the legacy master analysis script. |
| `data/processed/merged_control_treatment.csv` | `Autonomy_Control/data-autonomy/Consolidated/merged_control_treatment.csv` | CSV version of the consolidated Burdin-Halliday-Landini experiment data. |
| `data/processed/merged_kf_ziegel.csv` | `Autonomy_Control/data-autonomy/merged_kf_ziegel.csv` | Pooled comparison data used in robustness/comparison analyses. |

The visible identifiers in the included CSV files are session, subject, pair, group, role, and experiment codes. I did not observe names, email addresses, phone numbers, addresses, or direct personal identifiers in the headers inspected. This still needs formal coauthor review before an archival release.

## Excluded data

The following categories are excluded from this public draft:

- Raw zTree session outputs: `.gsf`, `.sbj`, `.pay`, `.adr`, and session-level `.xls` files.
- Questionnaire spreadsheets from individual sessions.
- Pilot and crash/unusable sessions.
- Legacy exploratory do-files with old absolute paths or unrelated commands.
- Reimbursement, receipt, payment, and administrative records.
- zTree executables.
- Literature PDFs and bibliography scraps.
- Old paper drafts and referee-response files.

## Raw-session audit

The legacy archive contains raw zTree `.xls` exports under
`Autonomy_Control/data-autonomy/`. These files are tab-delimited zTree exports,
not binary Excel workbooks. The folder
`data-autonomy/2014.04.25 - C1 - CRASH - Unusable/` appears to be the crashed
control session Simon remembered and is excluded from the cleaned analysis data.

Use `code/python/audit_raw_sessions.py` to compare a local extraction of the raw
zTree exports against `data/processed/merged_control_treatment.csv` without
copying raw data into the public repository:

```bash
python code/python/audit_raw_sessions.py --source /path/to/Autonomy_Control
```

The current audit indicates that all non-crash candidate exports appear in the
cleaned data and that the crash/unusable export does not. The cleaned TP10 data
contain eight zTree run identifiers totaling 159 subjects. The paper reports
seven TP10 sessions, so the remaining provenance question is probably
definitional rather than a missing-data issue: two zTree runs may have been
counted as one session in the paper. This should be confirmed against lab
records or coauthor memory before marking Appendix Table A1 fully verified.

## Open questions before Zenodo

- Confirm with Gabriel Burdin and Fabio Landini that the consolidated data can be released under CC-BY 4.0.
- Confirm whether the raw zTree outputs should be archived privately, deposited with restricted access, or excluded from the public replication package.
- Confirm whether comparison data from Falk-Kosfeld, Ploner-Schmelz-Ziegelmeyer, and Schnedler-Vadovic are redistributable or should be replaced by access instructions.
