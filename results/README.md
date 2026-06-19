# Results

This folder contains review outputs generated from the public replication
materials.

## Tracked R outputs

Run:

```bash
Rscript -e 'rmarkdown::render("code/r/replicate_descriptives.Rmd", quiet = TRUE)'
```

The R supplement writes:

- CSV review tables to `results/tables/r/`
- CDF figures to `results/figures/r/`

These files are tracked because they are small, public, and useful for reviewing
the R-focused replication before Stata is available.

For a single review page containing all CSV tables, run:

```bash
Rscript -e 'rmarkdown::render("code/r/r_output_review.Rmd", output_file = "../../results/r_output_review.html", quiet = TRUE)'
```

The rendered page is `results/r_output_review.html`.
It is tracked because it is a convenient review artifact for human readers.

## Ignored Stata outputs

The original Stata workflow writes logs, tables, and figures to `results/`.
Those generated files remain ignored until the Stata run is complete and the
outputs have been reviewed against the published article.
