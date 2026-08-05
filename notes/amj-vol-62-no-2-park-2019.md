---
id: amj-vol-62-no-2-park-2019
title: "Capability Reputation, Character Reputation, and Exchange Partners’ Reactions to Adverse Events"
authors:
  - "Park, B."
  - "Rogan, M."
year: 2019
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2016.0445"
volume: 62
issue: 2
pages: "553-578"

source: "AMJ/vol-62-no-2"
pdf_path: "library/AMJ/vol-62-no-2/pdfs/Park 2019 Capability Reputation, Character Reputation, and Exchange Partners’ Reactions to Adverse Events.pdf"
text_path: "library/AMJ/vol-62-no-2/text/Park 2019 Capability Reputation, Character Reputation, and Exchange Partners’ Reactions to Adverse Events.txt"
ingested_at: "2026-06-29"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-08-05"

paper_type: "empirical-quantitative"
keywords: ["capability reputation", "character reputation", "adverse events", "exchange partners", "relationship formation", "relationship dissolution", "controllability"]
theory: ["theory regarding uncertainty in exchange", "attribution theory", "multidimensional organizational reputation"]
topics: ["risk-management", "supply-chain-management", "stakeholder-engagement", "unethical-behavior"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Empirical quantitative study using PHMSA, FERC, and Mastio survey data on U.S. interstate natural gas transmission pipeline operators; the authors estimate fixed-effects unconditional negative binomial regressions with firm and year fixed effects and robust standard errors clustered by operator."
sample:
  industry: "Interstate natural gas transmission pipeline operators and gas shippers."
  country: "United States."
  time_period: "2004 to 2013."
  units: "Pipeline operator-year observations and counts of shipper ties formed and dissolved."
  n: "57 major interstate gas transmission pipeline operators; 423 operator-year observations."

# Mandatory evidence anchors (v2 - Layer 1 faithfulness audit).
# Each value is a <=25-word verbatim quote from the PDF text, or the literal
# string "Not reported in paper" (case-sensitive). See the Evidence anchors
# section above for the full schema.
evidence:
  sample_n: "423 operator-year observations"
  sample_country: "in the United States from 2004 to 2013"
  sample_industry: "interstate gas transmission pipeline accidents"
  sample_time_period: "from 2004 to 2013"
  theories_overview: "theory regarding uncertainty in exchange"
  methods_overview: "We used negative binomial regression analysis"
  keywords_source: "capability reputation and character reputation"
  hypotheses_source: "Hypothesis 1. Capability reputation will have a greater buffering effect on relationship formation than will character reputation following adverse events."
  measures_overview: "Count of controllable accidents. PHMSA categorizes the major causes of gas pipeline accidents."
  findings_overview: "provides clear support for Hypothesis 3b."
---

# Capability Reputation, Character Reputation, and Exchange Partners’ Reactions to Adverse Events

**Abstract**
To investigate when a firm’s reputation affects its exchange partners’ responses to adverse events, we distinguish between two types of reputation identified in prior work, capability reputation and character reputation, and present arguments for differences in their effects on exchange with potential and current exchange partners. Building on theory regarding uncertainty in exchange, we propose that potential exchange partners pay more attention to a firm’s capability reputation than its character reputation in the wake of adverse events. Thus, capability reputation has a buffering effect on relationship formation. In contrast, current exchange partners attend more to the firm’s character reputation than its capability reputation following adverse events. Hence, they are less likely to dissolve their relationships with organizations with high character reputations. Furthermore, we propose that the buffering effects of capability reputation and character reputation will be significantly reduced when the adverse events are caused by factors within the firm’s control. We find support for our arguments in an analysis of interstate gas transmission pipeline accidents in the United States from 2004 to 2013.

**Research Question**
The paper asks when different types of firm reputation affect exchange partners' responses to adverse events. It specifically examines whether capability reputation and character reputation buffer relationship formation and dissolution differently for potential versus current exchange partners, and whether controllability limits those buffering effects.

**Hypotheses / Propositions**
Hypothesis 1. Capability reputation will have a greater buffering effect on relationship formation than will character reputation following adverse events.
Hypothesis 2. Character reputation will have a greater buffering effect on relationship dissolution than will capability reputation following adverse events.
Hypothesis 3a. The buffering effect of capability reputation on relationship formation following adverse events is lower for controllable events than for uncontrollable events.
Hypothesis 3b. The buffering effect of character reputation on relationship dissolution following adverse events is lower for controllable events than for uncontrollable events.

**Mechanism Process**
- IV(s): Severe pipeline accidents; severe-controllable and severe-uncontrollable accidents in the controllability tests.
- DV(s): Count of shipper ties formed and count of shipper ties dissolved in the subsequent period.
- Mediators: Not directly measured; the theorized mechanisms are exchange partners' uncertainty reduction, blame-shifting concerns, and stigma anxiety.
- Moderators: Capability reputation, character reputation, and the controllability of the adverse event.

The mechanism is that potential exchange partners lack direct experience with the firm and therefore rely more on capability reputation to reduce ex ante quality uncertainty after an adverse event. Current exchange partners already have direct experience with quality, so character reputation becomes more relevant because it reduces concerns that the firm will shift blame or become stigmatized. When an accident is controllable, reputation becomes a less reliable cue because exchange partners may treat the event as discrepant evidence about the firm's competence or trustworthiness.

**Data & Measures**
Data sources: PHMSA annual reports for pipeline mileage, commodities transported, and annual accident data on impacts and causes; FERC Form 549B Customers Index, which every interstate gas transmission pipeline operator must file quarterly, for the exchange relationships with shippers; FERC Form 2/2A via the SNL Financial database for operator financials; and Mastio and Company's annual Natural Gas Pipeline Customer Value and Loyalty Study for reputation. Mastio scores are based on responses of approximately 1,100 North American gas shippers, including large LDCs, industrial users, independent power producers, gas producers, and gas marketers in the United States, who rate each operator on a 1-10-point scale. The final sample is 57 major interstate gas transmission pipeline operators in the United States from 2004 to 2013, or 423 operator-year observations.
- DVs: count of shipper ties formed = the number of new shippers each pipeline operator gains each year; count of shipper ties dissolved = the number of current shippers each pipeline operator loses each year. Both are measured at t + 1 and taken from the FERC customer index.
- IVs: count of severe accidents (natural logarithm). Following PHMSA's definition, a severe accident is any that involved (1) any human loss or injury, (2) the evacuation of 25 or more people, or (3) gas loss (in dollars) one standard deviation above the mean. For the controllability tests the authors classified each accident using PHMSA's cause categories - accidents induced by "natural forces" or "outside forces" were treated as uncontrollable, other causes such as corrosion as controllable - and created logged counts for four categories: severe-controllable, severe-uncontrollable, nonsevere-controllable, and nonsevere-uncontrollable.
- Moderators: capability reputation = shippers' 1-10-point rating of "[How well does the operator provide] direct access to ample and diverse gas supply?" Character reputation = a single annual Mastio item whose wording was updated three times: 2004, "[Please rate the] integrity of transportation provider"; 2005 to 2007, "[Does the operator] honor contracts and agreements?"; from 2008, "[Does the operator] communicate in an honest and forthright manner?" Across the three versions Cronbach's alpha was 0.62 and the average interitem correlation 0.35; the three items are used independently across the three time periods rather than aggregated, and year fixed effects absorb the wording change. Interaction terms were built from the count of severe accidents with capability reputation and character reputation, respectively (Hypotheses 1 and 2), and from the counts of severe-controllable and severe-uncontrollable accidents with capability reputation and character reputation (Hypotheses 3a and 3b).
- Controls: counts of shipper ties formed and dissolved in the prior year; operating revenue (log); slack resources = current assets divided by current liabilities; operator's share of available pipeline; pipeline lengths (log miles); percentage change in pipeline lengths; average relationship duration, built by tracking each operator-shipper dyad from its first contract year (from 1954) to 2013 and coding a relationship as ended when no contract is observed for two years in a row; general reputation, from the Mastio item "How likely would you be to recommend this pipeline company to your peers?" on a 1-10-point scale; media attention = logged count of mentions in the Financial Times, New York Times, USA Today, Washington Post, Wall Street Journal, Bloomberg BusinessWeek, Forbes, and Fortune; time under repair, a binary set to 1 if the operator's average "elapsed time until the area was made safe" (pre-2010) or "shutdown time" (2010 onward) exceeded all other operators' average times that year, with missing values for 4.9% of the sample multiply imputed; and the count of nonsevere accidents (log).

Estimation: fixed-effects unconditional negative binomial regression, chosen because the count dependent variables are overdispersed, implemented by including a dummy variable for each pipeline operator and year with robust standard errors clustered by operator, following Allison and Waterman (2002); the conditional fixed-effect negative binomial model was rejected for not controlling stable covariates. All control variables are lagged one year, and every model in Tables 3 and 4 reports 423 observations across 57 operators. The design is an associational fixed-effects panel; the authors do not claim a causal identification strategy beyond firm and year fixed effects and lagged predictors.

**Key Findings**
Hypothesis 1 is supported. In Model 2 of Table 3 the interaction of the count of severe accidents and capability reputation is positive and significant for shipper ties formed (b = 0.41, p < .05), indicating that operators with high capability reputation have a lower reduction in new shipper ties following severe accidents in the prior year, and model fit improves significantly. The interaction of character reputation and severe accidents in Model 3 is not significantly related to ties formed. Comparing the two interaction coefficients in Model 4, they differ significantly (p < .05), supporting Hypothesis 1.
Hypothesis 2 receives weaker support. In Model 7 of Table 3 the interaction between the count of severe accidents and character reputation is significant and negative for shipper ties dissolved (b = -0.31, p < .05), with model fit also improving, whereas the interaction of severe accidents and capability reputation on tie dissolutions (Model 6) is not significant. However, in Model 8 the two interaction coefficients are not significantly different from each other by conventional thresholds (p = .12), and in Figure 3 the marginal-effect confidence intervals overlap at the 95% level, so the authors interpret the result as weakly supporting Hypothesis 2 while reading the overall pattern as support for their argument that potential and current exchange partners selectively attend to different types of reputation after severe accidents.
Hypothesis 3a is not supported. In Model 2 of Table 4 the interaction of capability reputation and the count of severe-uncontrollable accidents is weakly significant and positive (b = 0.69, p < .1), consistent with the prediction, but the interaction of capability reputation and severe-controllable accidents in Model 3 is not significant, and when both interaction terms are entered together in Model 4 the severe-uncontrollable interaction becomes insignificant. A comparison of the two interaction coefficients in Model 4 finds no significant difference, so Hypothesis 3a is not supported.
Hypothesis 3b is supported. In Model 6 of Table 4 the interaction of character reputation and the count of severe-uncontrollable accidents is significant (b = -0.68, p < .01), whereas the interaction of character reputation and severe-controllable accidents in Model 7 is not significant; in Model 8 the two interaction coefficients are significantly different (p < .05). In Figure 4 the confidence intervals do not overlap, which the authors read as indicating that the marginal effect of severe and uncontrollable accidents on tie dissolution is significantly stronger when an operator has high character reputation. The pattern of results provides clear support for Hypothesis 3b.
Magnitudes and descriptives: the total number of severe accidents is 63, and 37 operators experienced at least one severe accident. Marginal effects from Model 2 of Table 3 show no significant difference in the number of new shippers before and after a severe accident for an operator one standard deviation above the mean on capability reputation, while for an operator one standard deviation below the mean one severe accident leads to a loss of about 1.48 new shippers in the subsequent period - a 32% drop against the sample average of 4.6 new shipper ties per year, and a change the authors value at $2 million to $10 million in revenue for the majority of shipper ties in their data.
Robustness and exploratory results: results hold when the sample is restricted to the 37 operators that experienced accidents, when the lagged dependent variables are dropped, and when accident counts are used unlogged; with a two-year rather than one-year lag (n = 311) capability reputation still shows a significant buffering effect on relationship formation, while the buffering effect of character reputation on relationship dissolution persists but with reduced significance. In exploratory analyses of the "being known" dimension of reputation (Online Appendix A, Table A2), firms with high media attention gain fewer potential exchange partners (b = -0.45, p < .01) and lose more current exchange partners (b = 0.48, p < .1) after adverse events. For the "generalized favorability" dimension the authors did not find a significant effect of severe accidents and general reputation on exchange networks, and in contrast to prior work they did not find evidence of a liability of good reputation for capability reputation and character reputation.

**Theoretical Contribution**
The paper extends organizational reputation research by showing that reputation's effect after adverse events depends on the specific reputation dimension and the stakeholder audience. It contributes to exchange-network research by treating relationship formation and dissolution as asymmetric processes shaped by different uncertainty problems. It also refines organizational-accident research by showing that stakeholder reactions depend not only on event severity but also on reputation and perceived controllability.

**Practical Implication**
Managers should not assume that a single general reputation protects all exchange relationships after an adverse event. The findings suggest that capability reputation matters more for preserving opportunities with potential partners, while character reputation matters more for retaining current partners. Managers should also minimize controllable adverse events because reputation may not buffer partner reactions when the event appears preventable.

**Limitations**
The authors note that capability reputation and character reputation are measured with single survey items, so each measure captures only one dimension of broader constructs. They also do not directly observe the theorized mechanisms behind character reputation's buffering effect, such as reduced blame shifting or stigma anxiety. The study is limited to exchange partners in one regulated industry, so other stakeholder groups may interpret the same reputation attributes differently.

**Future Research**
Future research could use multiple and aggregated measures of capability and character reputation. Scholars could examine how negative and positive events change different types of reputation over time. Further work could test the proposed mechanisms in field or experimental settings and compare how regulators, consumers, social movement activists, and the general public respond to adverse events.

**APA 7th Citation**
Park, B., & Rogan, M. (2019). Capability reputation, character reputation, and exchange partners' reactions to adverse events. *Academy of Management Journal*, 62(2), 553-578. https://doi.org/10.5465/amj.2016.0445
