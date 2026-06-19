# Stata Code

`run_all.do` is the entry point. Run it from the repository root:

```stata
do code/stata/run_all.do
```

`master_do_file.do` is a curated copy of the legacy master script. The substantive commands are preserved, but local absolute paths and output locations have been updated to use this repository's `data/processed/` and `results/` folders.

The source archive contains additional legacy do-files. They are listed in `docs/audit/source_manifest.csv` but are not included in this public draft because several contain old local paths and exploratory commands unrelated to the final replication workflow.
