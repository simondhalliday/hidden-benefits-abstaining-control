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

## Public experimental materials

Final zTree program/questionnaire/payoff files are included under
`instruments/ztree/` and are intended to remain public as part of the
replication package. The excluded zTree category above refers to zTree
executables and raw session outputs, not the public experiment program files.

## Comparison data

`data/processed/merged_kf_ziegel.csv` includes BHL rows and comparison rows from
Falk-Kosfeld and Ziegelmeyer-Schmelz-Ploner. Those comparison sources have
public provenance:

- Falk-Kosfeld data are available through openICPSR:
  https://doi.org/10.3886/E116246V1
- Ziegelmeyer-Schmelz-Ploner data are available as Springer electronic
  supplementary material for https://doi.org/10.1007/s10683-011-9302-8

The pooled file also contains Schnedler-Vadovic rows, but the final Stata
comparison block drops them before the reported regressions because permission
had not been obtained. See `docs/audit/COMPARISON_DATA_PROVENANCE.md`.

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
seven TP10 sessions. Because the subject counts and raw-session coverage match,
this is probably a session-definition convention or article typo rather than a
substantive missing-data issue. This can be checked against lab records or
coauthor memory, but it should not block the core replication audit.

## Raw-to-clean rebuild

Use `code/python/rebuild_clean_data.py` to rebuild the cleaned zTree analysis
CSV from the raw zTree exports and derive the main variables that appear in the
Stata analysis dataset:

```bash
python code/python/rebuild_clean_data.py --source /path/to/Autonomy_Control
```

The script writes rebuilt row-level files to `tmp/rebuilt_clean_data/`, which is
git-ignored, and writes aggregate audit outputs to `docs/audit/`:

- `raw_to_clean_rebuild_audit.csv`
- `derived_variable_audit.csv`
- `questionnaire_demographics_audit.csv`

Current status:

- The rebuilt zTree data match `data/processed/merged_control_treatment.csv` on
  row count, column count, ordered column names, and all cell values within a
  maximum numeric difference of `4.991552934e-07`. The tiny difference is due to
  rounding of random-number fields in the committed CSV.
- The derived variables used in `data/processed/merged_treatment_control.dta`
  match the scripted derivation within floating-point tolerance, including
  `finalearnings`, the GCOS indexes, treatment indicators, transfer differences,
  response categories, and standardized scale variables.
- The GCOS control-preference index in the committed Stata data is reproduced by
  summing `Q1b`, `Q2c`, `Q3a`, `Q4b`, `Q5c`, `Q6c`, `Q7a`, `Q8a`, `Q9c`, `Q10c`,
  `Q11a`, and `Q12b`.

## Questionnaire demographics and free text

Use `code/python/audit_demographics.py` to audit the consolidated questionnaire
demographics and screen open-ended responses without exporting raw questionnaire
rows:

```bash
python code/python/audit_demographics.py --source /path/to/Autonomy_Control
```

The script writes aggregate outputs to `docs/audit/`:

- `appendix_a1_demographics_audit.csv`
- `questionnaire_privacy_audit.csv`

Current status:

- Appendix Table A1 demographics appear to come from questionnaire respondents,
  not all zTree subjects.
- TP10 gender and age cells match the paper after rounding.
- C10 age SD matches after rounding. C10 female share is 19/44 = 43.18% versus
  the paper's 44%, and C10 mean age is 21.0455 versus the paper's 21.02. These
  are close but not exact, so the C10 demographic cells remain a table-note
  audit item.
- The free-text screen found no email, phone, URL, or long-number patterns, but
  raw open-ended responses, row-level majors, birthdates, and row-level
  demographics should remain out of public GitHub.

See `DEMOGRAPHICS_AUDIT.md` for the release recommendation and remaining checks.

## Open questions before Zenodo

- Confirm with Gabriel Burdin and Fabio Landini that the consolidated data can be released under CC-BY 4.0.
- Confirm whether the raw zTree outputs should be archived privately, deposited with restricted access, or excluded from the public replication package.
- Decide whether to remove Schnedler-Vadovic rows from a future public
  comparison-data file, since they are not used in the final comparison
  regressions and public redistribution has not been verified.
- Confirm whether questionnaire workbooks should be excluded entirely from
  Zenodo or included only in a restricted/private archive.
- See `COAUTHOR_REVIEW_PACKET.md` for the compact review questions to send to
  coauthors.
