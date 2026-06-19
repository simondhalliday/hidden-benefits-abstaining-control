# Demographics and Free-Text Audit

This audit covers questionnaire demographics and open-ended responses in the
legacy source archive. It does not add raw questionnaire rows, free-text
responses, majors, birthdates, or row-level demographics to the public
repository.

## Summary

- The paper's Appendix Table A1 gender and age cells appear to come from two
  consolidated questionnaire workbooks rather than from every zTree participant.
- The C10 demographic workbook has 44 individual demographic rows. Its age SD
  matches Appendix Table A1 after rounding, but the female share and age mean
  are close rather than exact matches.
- The TP10 demographic workbook has 102 individual demographic rows. Its summary
  rows reproduce the paper's TP10 gender and age values after rounding.
- This implies the Appendix A1 demographic values are best described as
  questionnaire-respondent summaries, while the subject counts are zTree subject
  counts.
- Raw free-text responses and row-level demographics should not be released on
  public GitHub.

## Files Audited

The main demographic source files are:

- `Autonomy_Control/data-autonomy/Consolidated/Workbook3.xlsx` for C10
  questionnaire demographics.
- `Autonomy_Control/data-autonomy/Consolidated/questionnaires_treatment.xlsx`
  for TP10 questionnaire demographics.

Session-level questionnaire workbooks also exist, but several are incomplete or
contain only subject IDs/free text with missing demographic fields. They are
useful for provenance, but the consolidated workbooks are the cleanest sources
for matching Appendix Table A1.

## Appendix A1 Match

See `docs/audit/appendix_a1_demographics_audit.csv`.

Current result:

- C10 female share: 19/44 = 0.4318, while the paper reports 44%.
- C10 age: 21.0455 with SD 2.3423, while the paper reports 21.02 (2.34).
- TP10 female share: 0.5392, which rounds to the paper's 54%.
- TP10 age: 20.7451 with SD 4.1997, matching the paper's 20.75 (4.20).

The C10 values are close enough to suggest the same source, but they should be
checked against any older paper table-building notes before marking the Appendix
cell exact. The likely possibilities are a manual table edit, a slightly
different questionnaire consolidation, or a reporting/rounding idiosyncrasy.

## Free-Text Risk

See `docs/audit/questionnaire_privacy_audit.csv`.

The audit counts open-ended responses and checks for common direct-identifier
patterns such as emails, phone numbers, URLs, and long number strings. This is a
screening pass only. It is not a guarantee that responses are non-identifying:
open text can contain names, rare circumstances, or sensitive details that simple
pattern checks miss.

The current pattern screen found no email, phone, URL, or long-number hits in
the audited free-text fields. The longest consolidated free-text response is 550
characters, so contextual disclosure risk remains plausible even without direct
identifier patterns.

Recommendation:

- Do not put raw free-text responses on public GitHub.
- Do not include row-level majors, birthdates, or row-level demographics in the
  public repository.
- If these materials are archived, use a restricted or private archival deposit,
  or deposit only aggregate summaries.
- The public replication package can reproduce the main analysis without raw
  free text.

## Remaining Checks

- Confirm with coauthors whether Appendix A1 demographics should be described as
  questionnaire-respondent demographics.
- Confirm the C10 age mean discrepancy: 21.0455 in the consolidated workbook
  versus 21.02 in the paper.
- Decide whether to exclude questionnaire workbooks entirely from public Zenodo
  or include them only in a restricted/private archive.
