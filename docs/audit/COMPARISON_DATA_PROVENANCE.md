# Comparison Data Provenance

This note documents the provenance status for the comparison rows in
`data/processed/merged_kf_ziegel.csv`.

The pooled comparison file contains rows labelled:

- `FK`: Falk and Kosfeld.
- `PSZ1` through `PSZ5`: Ziegelmeyer, Schmelz, and Ploner.
- `SV`: Schnedler and Vadovic.
- `BHL1` and `BHL2`: Burdin, Halliday, and Landini control and third-party
  treatments.

The final comparison block in `code/stata/master_do_file.do` explicitly drops
`SV` before the reported comparison regressions.

## Falk and Kosfeld

Source article:

> Armin Falk and Michael Kosfeld, "The hidden costs of control," *American
> Economic Review*, 96(5), 1611-1630, 2006.
> https://doi.org/10.1257/aer.96.5.1611

Public data source:

> "The Hidden Costs of Control," openICPSR project 116246, version V1.
> https://doi.org/10.3886/E116246V1

The AEA article page links to the openICPSR replication package. The openICPSR
package includes an Excel data file, readme, article PDF, online appendix, and
figures. It is therefore reasonable to keep the FK-derived rows in the public
pooled comparison file, with citation to the openICPSR project.

## Ziegelmeyer, Schmelz, and Ploner

Source article:

> Anthony Ziegelmeyer, Katrin Schmelz, and Matteo Ploner, "Hidden costs of
> control: four repetitions and an extension," *Experimental Economics*, 15,
> 323-340, 2012. https://doi.org/10.1007/s10683-011-9302-8

Public data source:

> Springer electronic supplementary material for
> https://doi.org/10.1007/s10683-011-9302-8

The public Springer article page provides electronic supplementary material:

- `10683_2011_9302_MOESM1_ESM.pdf`:
  https://static-content.springer.com/esm/art%3A10.1007%2Fs10683-011-9302-8/MediaObjects/10683_2011_9302_MOESM1_ESM.pdf
- `10683_2011_9302_MOESM2_ESM.xls`:
  https://static-content.springer.com/esm/art%3A10.1007%2Fs10683-011-9302-8/MediaObjects/10683_2011_9302_MOESM2_ESM.xls

The local source archive contains those same supplementary filenames under
`Autonomy_Control/Stata/Ziegelmeyer - supplementary/`. It is therefore
reasonable to keep the PSZ-derived rows in the public pooled comparison file,
with citation to the article DOI and Springer supplementary materials.

## Schnedler and Vadovic

Source article:

> Wendelin Schnedler and Radovan Vadovic, "Legitimacy of Control," *Journal of
> Economics & Management Strategy*, 20(4), 985-1009, 2011.
> https://doi.org/10.1111/j.1530-9134.2011.00315.x

The pooled file includes rows labelled `SV`, but the final Stata comparison
block drops `SV` before the reported regressions. A comment in the legacy Stata
file says those data were not used because permission had not been obtained.

Release recommendation:

- Keep the current final-analysis behavior that drops `SV`.
- Do not describe `SV` rows as redistributable unless a public data source or
  explicit permission is verified.
- Consider removing `SV` rows from a future public comparison-data file, or
  retaining them only in a non-public provenance archive.

## Release recommendation

For the public GitHub draft:

- FK rows may remain, with the openICPSR citation.
- PSZ rows may remain, with the Springer supplementary-material citation.
- SV rows should remain documented as excluded from final comparison regressions
  and should not be treated as approved public comparison data without further
  verification.
