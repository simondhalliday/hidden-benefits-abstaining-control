*--------------------------------------------------
* Program Setup
* --------------------------------------------------
version 13              // Set Version number for backward compatibility, feel free to replace 13 with 14
set maxvar 10000        // Increase the maximum number of variables used in a dataset
set more off            // Disable partitioned output
clear all               // Start with a clean slate
set linesize 80         // Line size limit to make output more readable
macro drop _all         // clear all macros
capture log close       // Close existing log files
capture mkdir "results"
capture mkdir "results/logs"
capture mkdir "results/figures"
capture mkdir "results/tables"
log using "results/logs/halliday.txt", text replace       // Open log file
* --------------------------------------------------




**Master do file
**Please replace the file paths with the relevant file paths on your computer
**CHANGE Working Directory PATH HERE
* Run this script from the repository root.
cd "."
use "data/processed/merged_treatment_control.dta", clear
*I use the following fairly commonly used additoinal commands with corresponding packages: 
*estout, esttab, estpost, outreg2
*You can install them as follows:
*ssc install estout
*ssc instal outreg2

/*For much of the analysis, we restrict our statistics to looking 
at the agents, those subjects who played role A, therefore you will 
regularly see us dropping if the role is not A i.e. using the command: 
drop if playedrolea!=1
In later analysis, for result 6 specifically, we look at the behavior 
of subjects who played the role of principals in C10 (playedroleb==1) 
and the third party TP10 (playedrolec==1)*/

*Some variable re-labeling after editor comments
replace treatmentstring = "C10" if treatmentstring == "Experiment 1"
replace treatmentstring = "TP10" if treatmentstring == "Experiment 2"

/*--------------------------------------*/
*Result 1:: There exist statistically significant hidden costs of control
/*--------------------------------------*/
*Preserve the data and then drop for subjects who aren't player A and check the CDF
preserve
drop if playedrolea!=1
*Signrank tests of the transfers with the modified distribution for C10
signrank transferbounded = transferubx if treatment==1
*Shows a result that is consistent with result 1 from Z et al
*Also need the cumulative distributions to be consistent with F&K. 
gen exp1transferb = transferbounded if treatment==1
gen exp1transferub = transferunbounded if treatment==1
cumul exp1transferb, gen(cumulexp1b) equal
cumul exp1transferub, gen(cumulexp1ub) equal
stack cumulexp1b exp1transferb cumulexp1ub exp1transferub, into(c transfer) wide clear
twoway line cumulexp1ub cumulexp1b transfer, ///
	sort ylab(, grid) ytitle("") xlab(, grid) xtitle("Transfer (x)") ///
	title("Cumulative Distributions:" "Control and No-Control Transfers in C10") ///
	connect(J J) legend(label(1 "No-Control") label(2 "Control")) ///
	lpattern(l -) 
graph export "results/figures/cumul_exp1.pdf", replace
restore

/*--------------------------------------*/
*Result 2: The hidden costs of control are not sufficient to outweigh the benefits of control
/*--------------------------------------*/

*Generate Table 2
*First generate the means and their details
preserve
drop if playedrolea!=1
*The contol/bounded transfers means
by treatment: sum transferbounded, detail
*The no-contol/unbounded transfers means
by treatment: sum transferunbounded, detail
*Mean with 10^5 reps and a seed for replicability
*Baseline experiment 1
*Note: random seed obtained from https://www.random.org on 2015.05.20 
bootstrap meantransdif=r(mean), reps(100000) nodots seed(17884): sum transdif if treatment==1
*TP10 experiment 2
bootstrap meantransdif=r(mean), reps(100000) nodots seed(17884): sum transdif if treatment==2
*Also check the 90% confidence intervals: 
*C10/experiment 1
bootstrap meantransdif=r(mean), reps(100000) nodots seed(17884) level(90): sum transdif if treatment==1 
*TP10 experiment 2
bootstrap meantransdif=r(mean), reps(100000) nodots seed(17884) level(90): sum transdif if treatment==2

*Signrank tests of the transfers with the baseline distributions
by treatment: signrank transferbounded = transferunbounded

gen bindingcontrol = 0 
replace bindingcontrol = 1 if transferbounded == 10 & transferunbounded <=10
tab controlpos bindingcontrol if treatment == 2, sum(transferbounded)
restore


*Only keep one instance of each behavior
preserve
drop if playedrolea!=1
ranksum transferunbounded, by(treatment)
local rz1 = r(z)
local probz1 = 2 * normprob(-abs(r(z)))
ranksum transferbounded, by(treatment)
local rz2 = r(z)
local probz2 = 2 * normprob(-abs(r(z)))
restore

*Result 3
preserve
*Only keep one instance of each behavior
drop if playedrolea!=1
*Signrank tests of the transfers with the modified distributions for TP10
signrank transferbounded = transferubx if treatment==2
restore
*Also need the cumulative distributions to be consistent with F&K. 
*Preserve the data and then drop for subjects who aren't player A and check the CDFs
preserve
drop if playedrolea!=1
gen exp2transferb = transferbounded if treatment==2
gen exp2transferub = transferunbounded if treatment==2
cumul exp2transferb, gen(cumulexp2b) equal
cumul exp2transferub, gen(cumulexp2ub) equal
stack cumulexp2b exp2transferb cumulexp2ub exp2transferub, into(c transfer) wide clear
twoway line cumulexp2ub cumulexp2b  transfer, sort ylab(, grid) ///
	ytitle("") xlab(, grid) xtitle("Transfer (x)") ///
	title("Cumulative Distributions:" "Control and No-Control Transfers in TP10") ///
	connect(J J) legend(label(1 "No-Control") label(2 "Control")) ///
	lpattern(l -) 
graph export "results/figures/cumul_exp2.pdf", replace
restore

*Result 4: refer to the generation of Table 2 earlier with result 2
**The following is to for the Kruskal-Wallis tests across the treatments. 
preserve
*Drop if the role is not 'Agent'
drop if playedrolea!=1
*Compare the bounded transfers by treatment
kwallis transferbounded, by(treatment)
*Compare the unbounded transfers by treatment
kwallis transferunbounded, by(treatment)

**The Wilcoxon Signed Rank test was already done for Result 2, but is repeated here for clarity: 
by treatment: signrank transferbounded = transferunbounded 
restore

*Result 5: 
*Preserve the data
preserve
*Drop if the role is not 'Agent'
drop if playedrolea!=1
*We need tables with the prooportions of agents falling into each category followed by statistical tests of the 
*prportions across the conditions
*Proportions of agents falling into each category in C10 Replication (Exp 1)
tab controlcat if treatment == 1
*Proportions of agents falling into each category in TP10 (Exp 2)
tab controlcat if  treatment == 2 
*Fisher's exact tests of the proportions of subjects responding negatively, neutrally or positively to control
*Negative
tab controlneg treatment, exact
*Neutral
tab controlneutral treatment, exact
*Positive
tab controlpos treatment, exact
*For each of the treatments, summarize their transfers in the control and no-control conditions
*Control condition
by treatment: tab controlcat, sum(transferbounded)
*No control condition
by treatment: tab controlcat, sum(transferunbounded)
restore


*Filter sample further for pairwise comparisons
preserve
drop if playedrolea != 1
drop if controlneg == 1
ranksum controlpos, by(treatment)


preserve
clear
**CHANGE FILE PATH HERE
**You'll need to insheet the csv for the Pooled data and change the next line to work for your drive path
insheet using "data/processed/merged_kf_ziegel.csv", names clear
*First generate transferbounded and transferunbounded -- I prefer these names
*transferbounded as a real version of x_c
gen transferbounded = real(x_c)
replace transferbounded = . if role=="Principal"
replace transferbounded = . if role=="Third Party"
*transferunbounded as a real version of x_nc
gen transferunbounded = real(x_nc)
replace transferunbounded = . if role=="Principal"
replace transferunbounded = . if role=="Third Party"
*Now the modified transfer distribution
gen transferubx = transferunbounded
replace transferubx = 10 if transferunbounded < 10
lab var transferubx "Transfers with UB < 10 set = 10"
*Now generate the dummy variables for each treatment, leaving out our baseline as the omitted dummy. 
gen tp10dum = 0
*Burdin, Halliday and Landini
replace tp10dum = 1 if experiment=="BHL2"
lab var tp10dum "D: = 1 for our Exp 2"
*Falk & Kosfeld C10
gen fk10dum = 0
replace fk10dum = 1 if experiment=="FK"
lab var fk10dum "D: = 1 for FK Exp"
*Ploner, Schmelz and Ziegelmeyer Exp 1 C10
gen psz1dum = 0
replace psz1dum = 1 if experiment=="PSZ1"
lab var psz1dum "D: = 1 for PSZ Exp 1"
*Ploner, Schmelz and Ziegelmeyer Exp 2 C10
gen psz2dum = 0
replace psz2dum = 1 if experiment=="PSZ2"
lab var psz2dum "D: = 1 for PSZ Exp 2"
*Ploner, Schmelz and Ziegelmeyer Exp 3 C10
gen psz3dum = 0
replace psz3dum = 1 if experiment=="PSZ3"
lab var psz3dum "D: = 1 for PSZ Exp 3"
*Ploner, Schmelz and Ziegelmeyer Exp 4 C10
gen psz4dum = 0
replace psz4dum = 1 if experiment=="PSZ4"
lab var psz4dum "D: = 1 for PSZ Exp 4"
*Ploner, Schmelz and Ziegelmeyer Exp 5 C10
gen psz5dum = 0
replace psz5dum = 1 if experiment=="PSZ5"
lab var psz5dum "D: = 1 for PSZ Exp 5"
*Schnedler and Vadovic C10 equivalent
gen svdum = 0
replace svdum = 1 if experiment=="SV"
lab var svdum "D: = 1 for SV Exp"
*Now generate the dependent variables for the regressions
*Transfer differences, i.e. x^NC - x^C
gen transdif = transferunbounded - transferbounded
lab var transdif "Difference between the unbounded and bounded transfers"
*Control averse dummy
gen controlneg=0
replace controlneg = 1 if transferbounded<transferunbounded & role=="Agent"
lab var controlneg "D: =1 if Control Averse"
*Control loving dummy
gen controlpos=0
replace controlpos = 1 if transferbounded>transferunbounded & role=="Agent"
lab var controlpos "D: =1 if Control Positive"
*Control neutral dummy
gen controlneutral = 0
replace controlneutral = 1 if transferbounded == transferunbounded & role=="Agent"
lab var controlneutral "D: =1 if Control Neutral"

**Now run regressions for each of those that appear in Ziegelmeyer et al barring the last 
**because our TP10 has too small a sample of negative responders
**Also, as Z et al do not contrast with SV and I have not gotten their permission, I won't use the Schnedler and Vadovic data
**(That said, when I tested it anyway, the results remained robust to their inclusion)
drop if experiment=="SV"

*OLS of x^NC 
quietly regress transferunbounded tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", vce(hc3)
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
outreg2 using "results/tables/agent_regressions_tests.doc", replace ctitle(xNC) label adds(TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, r(p))


*OLS of x^NC - x^C
quietly regress transdif tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", vce(hc3)
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
outreg2 using "results/tables/agent_regressions_tests.doc", append ctitle(xNC - xC) label adds(TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, r(p))

*Logit for positive*
quietly logit controlpos tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", robust
mfx compute
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
local p6=r(p)
outreg2 using "results/tables/agent_regressions_tests.doc", append mfx ctitle(Positive) addstat(Log Likelihood, e(ll), TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label


*Logit for neutral*
quietly logit controlneutral tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", robust
mfx compute
test tp10dum = fk10dum
local p1 = r(p)
test tp10dum = psz1dum
local p2 = r(p)
test tp10dum = psz2dum
local p3 = r(p)
test tp10dum = psz3dum
local p4 = r(p)
test tp10dum = psz4dum
local p5 = r(p)
test tp10dum = psz5dum
local p6 = r(p)
outreg2 using "results/tables/agent_regressions_tests.doc", append mfx ctitle(Neutral) addstat(Log Likelihood, e(ll), TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label


*Logit for negative*
quietly logit controlneg tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", robust
mfx compute
test tp10dum = fk10dum
local p1 = r(p)
test tp10dum = psz1dum
local p2 = r(p)
test tp10dum = psz2dum
local p3 = r(p)
test tp10dum = psz3dum
local p4 = r(p)
test tp10dum = psz4dum
local p5 = r(p)
test tp10dum = psz5dum
local p6 = r(p)
outreg2 using "results/tables/agent_regressions_tests.doc", append mfx ctitle(Negative) addstat(Log Likelihood, e(ll), TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label

*Now, we run a multinomial logit model with these data
*First, we need the categories as numbers
gen controlcats = .
replace controlcats = 1 if controlpos==1
replace controlcats = 2 if controlneutral==1
replace controlcats = 3 if controlneg==1
replace controlcats = . if role!="Agent"
lab var controlcats "Control Categories: 1 = Positive, 2 = Neutral, 3 = Negative"
quietly mlogit controlcats tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", robust baseoutcome(1)
mfx compute, predict(outcome(1))
outreg2 using "results/tables/mlogits_pooled.doc", mfx ctitle(Positive) label replace
mfx compute, predict(outcome(2))
outreg2 using "results/tables/mlogits_pooled.doc", mfx ctitle(Neutral) label append
mfx compute, predict(outcome(3))
outreg2 using "results/tables/mlogits_pooled.doc", mfx ctitle(Negative) label append

*In the CEBERG sessions of the CEA meetings, Glenn Harrison asked about whether we had checked for (multiplicative) heteroskedasticity. 
*At that point, we had not. But,  heteroskedasticity is difficult to test or correct for in logit models in Stata. 
*Below we run LPMs and Probit models with tests for heteroskedasticity.  
*LPM for positive*
quietly reg controlpos tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", vce(hc3)
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
local p6=r(p)
outreg2 using "results/tables/agent_regressions_tests_lpm.doc", replace ctitle(Positive) addstat(TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label
estat hettest 
estat imtest, white


*LPM for neutral*
quietly reg controlneutral tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", vce(hc3)
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
local p6=r(p)
outreg2 using "results/tables/agent_regressions_tests_lpm.doc", append ctitle(Neutral) addstat(TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label
estat hettest 
estat imtest, white

*LPM for negative*
quietly reg controlneg tp10dum fk10dum psz1dum psz2dum psz3dum psz4dum psz5dum if role=="Agent", vce(hc3)
test tp10dum = fk10dum
local p1=r(p)
test tp10dum = psz1dum
local p2=r(p)
test tp10dum = psz2dum
local p3=r(p)
test tp10dum = psz3dum
local p4=r(p)
test tp10dum = psz4dum
local p5=r(p)
test tp10dum = psz5dum
local p6=r(p)
outreg2 using "results/tables/agent_regressions_tests_lpm.doc", append ctitle(Negative) addstat(TP10 Dummy = FK Dummy, `p1', TP10 Dummy = PSZ E1 Dummy, `p2', TP10 Dummy = PSZ E2 Dummy, `p3', TP10 Dummy = PSZ E3 Dummy, `p4', TP10 Dummy = PSZ E4 Dummy, `p5', TP10 Dummy = PSZ E5 Dummy, `p6') label
estat hettest 
estat imtest, white

**We are now done with the pooled data & return to looking at our data only

*First we need to generate the table of the summaries of the GCOS variables,
** a density function of their distributions, and ttests and Mann-Whitney tests of their means & medians
*First a kernel density function (Note: I didn't think histograms would depict this well & couldn't be overlaid nicely)
graph twoway (kdensity autonomy, kernel(gaussian) lpattern()) ///
		(kdensity impersonal,  kernel(gaussian) lpattern(_)) ///
		(kdensity controlpref,  kernel(gaussian) lpattern(-)), ///
		legend(ring(0) cols(1) pos(11) label(1 "GCOS: Autonomy") ///
		label(2 "GCOS: Impersonal") label(3 "GCOS: Control")) ///
		xtitle("Scale Value") ytitle("Density")
graph export "results/figures/kdensity_gcos.pdf", replace

*Generate the table (Table 3) for agents only; for all subjects see online appendix summarizing the means, sds, etc of the scales
preserve
drop if playedrolea != 1
sort treatmentstring
by treatmentstring: eststo: quietly estpost summarize autonomy impersonal controlpref
esttab using "results/tables/gcos_agents.rtf", main(mean) aux(sd) nostar unstack label mtitle nonum replace
eststo clear

*Now generate a table with the ttests
eststo: quietly estpost ttest autonomy impersonal controlpref, by(treatment)
esttab using "results/tables/gcos2_agents.rtf", cell("b t p") nonumber label replace
eststo clear
*It was more expendient to copy/paste than to add this to the other file

*Now we also need to do Mann-Whitney Ranksums to check difference too
ranksum autonomy, by(treatment)
ranksum impersonal, by(treatment)
ranksum controlpref, by(treatment)

restore
*Now compare full sample with the GCOS variables
*First summarize means, etc
sort treatmentstring
by treatmentstring: eststo: quietly estpost summarize autonomy impersonal controlpref
esttab using "results/tables/gcos.rtf", main(mean) aux(sd) nostar unstack label mtitle nonum replace
eststo clear

*Now generate a table with the ttests
eststo: quietly estpost ttest autonomy impersonal controlpref, by(treatment)
esttab using "results/tables/gcos2.rtf", cell("b t p") nonumber label replace
eststo clear
*It was more expendient to copy/paste than to add this to the other file

*Now we also need to do Mann-Whitney Ranksums to check medians too
ranksum autonomy, by(treatment)
ranksum impersonal, by(treatment)
ranksum controlpref, by(treatment)
restore

ranksum impersonal, by(treatment)
ranksum controlpref, by(treatment)
*Repeat the regressions only on our sample with the GCOS variables included

*OLS Regression* With standard errors corrected using the MacKinnon & White (1985) residual-variance estimator HC3 
**i.e. consistent with Ziegelmayer et al
*We first do just x^NC as requested by the reviewer
quietly regress transferunbounded treatdum stauto stimp stcont if playedrolea==1, vce(hc3)
outreg2 using "results/tables/agent_regressions_gcos.doc", replace ctitle(xNC) label
*Now the difference, consistent with Ziegelmeyer et al
quietly regress transdif treatdum stauto stimp stcont if playedrolea==1, vce(hc3)
outreg2 using "results/tables/agent_regressions_gcos.doc", append ctitle(xNC - xC) label
estat hettest 
estat imtest, white
*Note: these tests suggest that there exists heteroskedasticity even with the MacKinnon & White corrections. 
*This is not the worst outcome, but things could be better. 
*For your interest, you can check the residual plots if you uncomment the following commands: 
*rvpplot treatdum, yline(0)
*rvpplot stauto, yline(0)
*rvpplot stimp, yline(0)
*rvpplot stcont, yline(0)
*You can see in these figures that the residuals and the explanatory variables correlate,
*which is cause for worry w.r.t. the consistency of our estimates
*Nevertheless, we proceed.

*Logit for positive response*
quietly logit controlpos treatdum stauto stimp stcont if playedrolea==1, robust
mfx compute
outreg2 using "results/tables/agent_regressions_gcos.doc", append mfx ctitle(Positive) addstat(Log Likelihood, e(ll)) label
*Logit for neutral response*
quietly logit controlneutral treatdum stauto stimp stcont if playedrolea==1, robust
mfx compute
outreg2 using "results/tables/agent_regressions_gcos.doc", append mfx ctitle(Neutral) addstat(Log Likelihood, e(ll))  label
*Logit for negative response*
quietly logit controlneg treatdum stauto stimp stcont if playedrolea==1, robust
mfx compute
outreg2 using "results/tables/agent_regressions_gcos.doc", append mfx ctitle(Negative) addstat(Log Likelihood, e(ll))  label

*For footnote, check that Linear Probability Model results are consistent with the Logit results
*LPM for positive response*
quietly reg controlpos treatdum stauto stimp stcont if playedrolea==1, vce(hc3)
outreg2 using "results/tables/agent_regressions_gcos_lpm.doc", replace  ctitle(Positive) label
estat hettest
estat imtest, white
*We do not reject the null of homoskedasticity
*LPM for neutral response*
quietly reg controlneutral treatdum stauto stimp stcont if playedrolea==1, vce(hc3)
outreg2 using "results/tables/agent_regressions_gcos_lpm.doc", append  ctitle(Neutral)  label
estat hettest
estat imtest, white
*We do not reject the null of homoskedasticity
*LPM for negative response*
quietly reg controlneg treatdum stauto stimp stcont if playedrolea==1, vce(hc3)
outreg2 using "results/tables/agent_regressions_gcos_lpm.doc", append  ctitle(Negative)  label
estat hettest
estat imtest, white
*We must REJECT the null of homoskedasticity for controlneg



*Quietly run the multinomial logit with the GCOS variables
quietly mlogit controlcats treatdum  stauto stimp stcont if playedrolea==1, robust baseoutcome(1)
*Need to compute the marginal effects for each predicted outcome: Negative, Neutral and Positive
*Positive is outcome 1
mfx compute, predict(outcome(1))
outreg2 using "results/tables/mlogits.doc", mfx ctitle(Positive) addstat(Log Likelihood, e(ll)) label replace
*Neutral is outcome 2
mfx compute, predict(outcome(2))
outreg2 using "results/tables/mlogits.doc", mfx ctitle(Neutral) addstat(Log Likelihood, e(ll)) label append
*Negative is outcome 3
mfx compute, predict(outcome(3))
outreg2 using "results/tables/mlogits.doc", mfx ctitle(Negative) addstat(Log Likelihood, e(ll)) label append

**Need to also check the consistency of the GCOS variables using the Cronbach's Alpha: 
*First use the entire sample from our experiment
*autonomy
alpha q1c q2a q3c q4a q5a q6b q7b q8c q9c q10b q11b q12a, item
*Impersonal
alpha q1a q2b q3b q4c q5b q6a q7c q8b q9a q10a q11c q12c, item
*Control
alpha q1b q2c q3a q4b q5c q6c q7a q8a q9b q10c q11a q12b, item 

*Now restrict the sample to the agents
*autonomy
alpha q1c q2a q3c q4a q5a q6b q7b q8c q9c q10b q11b q12a if playedrolea==1, item
*Impersonal
alpha q1a q2b q3b q4c q5b q6a q7c q8b q9a q10a q11c q12c if playedrolea==1, item
*Control
alpha q1b q2c q3a q4b q5c q6c q7a q8a q9b q10c q11a q12b if playedrolea==1, item 


**Result 6
*We need the proportions of principals or third parties who choose to control ("bound") the transfer
*For the proportion of principals in C10, Experiment 1, restricted to those who played role B (principals)
tab transferisbounded if playedroleb==1 & treatment==1
*For the proportion of third parties in TP10, Experiment 2, restricted to those who played role C (third parties)
tab transferisbounded if playedrolec==1 & treatment==2
**Analyzing the behavior of principals
*Summary of Choice to bound transfers in experiment 1
preserve
drop if playedrolea==1
drop if treatment==2
sum(transferisbounded)
restore

*Summary of Choice to bound transfers in experiment 2
preserve
drop if playedrolea==1
drop if playedroleb==1
drop if treatment==1
sum(transferisbounded)
restore

*Now we need to check if these are the same across treatments
*Making some assumptions about the distributions, we can do a binomial test of equivalence of the proportions
preserve
sum transferisbounded  if playedroleb==1 & treatment==1, meanonly
scalar m1 = r(mean)
sum transferisbounded  if playedrolec==1 & treatment==2, meanonly
scalar m2 =  r(mean)
*Test that the proportion of those who chose to control in C10 is equal to the proportion who chose to control in TP10
bitest transferisbounded = m2 if playedroleb==1 & treatment==1
*Test that the proportion of those who chose to control in TP10 is equal to the proportion who chose to control in C10
bitest transferisbounded = m1 if playedrolec==1 & treatment==2
restore

*Next, we can check the proportions using the ranksum command
*To do so we generate a new variable, 'controller', that indicates whether a subject chose to control or not
gen controller = 0
replace controller = 1 if transferisbounded == 1 & playedroleb==1 & treatment==1
replace controller = . if treatment==1 & playedroleb!=1
replace controller = 1 if transferisbounded == 1 & playedrolec==1 & treatment==2
replace controller = . if treatment==2 & playedrolec!=1
lab var controller "D: = 1 if subject chose to control A"
*We can check the equivalence of these proportions using a Mann-Whitney or Wilcoxon Ranksum test
sort treatment 
ranksum controller, by(treatment)
tab controller treatment, exact
*The results suggest that the proportions are not different

*Lastly, we can construct a bootstrap confidence interval on the difference
preserve
drop if playedrolea==1
drop if playedroleb==1 & treatment == 2
bootstrap, reps(100000) nodots seed(80023): regress transferisbounded treatdum
restore










