* Replication runner for Burdin, Halliday, and Landini (2018)
*
* Usage:
*   1. Open Stata.
*   2. cd to the repository root.
*   3. do code/stata/run_all.do

version 13
set more off
clear all

capture mkdir "results"
capture mkdir "results/figures"
capture mkdir "results/logs"
capture mkdir "results/tables"

do "code/stata/master_do_file.do"
