---
id: amj-vol-65-no-6-um-2022
title: "The Downside of CFO Function-Based Language Incongruity"
authors:
  - "Um, Cyril Taewoong"
  - "Guo, Shiau-Ling"
  - "Lumineau, Fabrice"
  - "Shi, Wei"
  - "Song, Ruixiang"
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2019.0943"
volume: 65
issue: 6
pages: "1984-2013"

source: "AMJ/vol-65-no-6"
pdf_path: "library/AMJ/vol-65-no-6/pdfs/Um 2022 The Downside of CFO Function-Based Language Incongruity.pdf"
text_path: "library/AMJ/vol-65-no-6/text/Um 2022 The Downside of CFO Function-Based Language Incongruity.txt"
ingested_at: "2026-06-24"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-29"

paper_type: "empirical-quantitative"
keywords: ["role congruity theory", "function-based language incongruity", "within-role incongruity", "CFO", "debt contract covenants", "perceived exchange hazards", "contract design"]
theory: ["role congruity theory", "expectancy violations theory", "transaction cost / exchange hazards perspective"]
topics: ["corporate-governance", "role-theory"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Archival quantitative study. Negative binomial regression (count DV, overdispersion) of the number of debt-contract covenants on CFO function-based language incongruity, with interaction terms for two moderators, 4-digit SIC industry, year, loan-purpose, and lead-bank fixed effects, and standard errors clustered by firm. CFO/CEO language attributes (optimism, risk-taking, promotion focus, future focus) measured from conference-call transcripts via LIWC and combined into a PCA index. Robustness via heteroskedasticity-based instrumental variables, curvilinearity tests, and supplementary moderator analyses."
sample:
  industry: "U.S. public firms (non-financial) that signed bank debt contracts; lenders are commercial banks (lead arrangers)"
  country: "United States"
  time_period: "2003-2018"
  units: "Loan deals (debt contracts) nested within borrowing firms"
  n: "7,649 deals across 1,915 firms"

evidence:
  sample_n: "a sample of 7,649 deals with"
  sample_country: "Our sample construction started with all U.S. firms"
  sample_industry: "merged our sample with the DealScan database to"
  sample_time_period: "deals between 2003 and 2018."
  theories_overview: "by drawing on role congruity theory, we"
  methods_overview: "4-digit SIC industry fixed effects"
  keywords_source: "leads banks to employ more debt contract covenants"
  hypotheses_source: "Hypothesis 1. The level of CFO function-based language incongruity is positively related to the number"
  measures_overview: "employed Linguistic Inquiry and Word Count (LIWC)"
  findings_overview: "we show that the incongruity of function-based expectations manifested through the language of the CFO leads banks to employ more debt contract covenants."
---

# The Downside of CFO Function-Based Language Incongruity

**Abstract**
The prior literature on role congruity theory has revolved around demographic-based expectations, emphasizing role incongruity derived from a mismatch between prescriptive expectations of distinct roles. In this study, we depart from this traditional focus on between-role incongruity and explore an alternative source of role incongruity by examining how language can trigger the within-role incongruity of function-based expectations. Through an analysis of conference call transcripts and contracts for 7,649 deals during 2003–2018, we show that the incongruity of function-based expectations manifested through the language of the CFO leads banks to employ more debt contract covenants. This takes place because such incongruity increases banks’ perceived hazards. In addition, by investigating the moderating effects of corresponding CEO language and media sentiment, we show how the social context and sentiment toward the firm weaken this incongruity effect. We discuss the theoretical implications of our study for future research on the sources of role incongruity and the antecedents of contract design.

**Research Question**
(a) How does role-incongruent language influence the observer's perceived hazard, and (b) how is that relationship moderated by factors that influence the interpretation of incongruity? Specifically, how does a borrowing firm's CFO exhibiting language incongruent with function-based role expectations shape the perceived exchange hazards of the lending bank and thereby the design (number of covenants) of debt contracts?

**Hypotheses / Propositions**
- Hypothesis 1. The level of CFO function-based language incongruity is positively related to the number of covenants in debt contracts.
- Hypothesis 2. Corresponding CEO language weakens the relationship between CFO function-based language incongruity and the number of covenants in debt contracts.
- Hypothesis 3. Media sentiment positivity weakens the relationship between CFO function-based language incongruity and the number of covenants in debt contracts.

**Mechanism Process**
- IV(s): CFO function-based language incongruity (PCA index of CFO-exhibited optimism, risk-taking, promotion focus, and future focus measured from conference-call transcripts).
- DV(s): Number of covenants in the debt contract.
- Mediators: Banks' perceived exchange hazards (theorized, not directly measured — the mechanism through which incongruity increases covenants).
- Moderators: Corresponding CEO language (social-context consistency); media sentiment positivity (sentiment toward the firm).

CFOs are culturally expected to be conservative "watchdogs"/"naysayers"; when a CFO's public language exhibits optimism, risk-taking, promotion focus, or future focus, observers (banks) perceive incongruity with the function-based role. Drawing on role congruity and expectancy-violations logic, this within-role incongruity raises banks' perceived exchange hazards, leading them to add more covenants to control risk. Because the violation is interpreted, the effect is weakened when the CEO speaks similarly (the incongruity is read as the organization's broader social norm) and when positive media sentiment makes observers attribute the incongruity less negatively.

**Data & Measures**
Single archival study. Debt-contract data come from DealScan; CFO and CEO conference-call transcripts from Thomson Reuters' StreetEvents (quarterly earnings calls, corporate conference calls, conference presentations, and analyst calls); accounting and market data from Compustat and the Center for Research in Security Prices (CRSP); executive compensation and identification data from Capital IQ and Execucomp; media data from the Dow Jones edition of RavenPack; board data from BoardEx; and auditor-change data from Audit Analytics. Sample construction started with all U.S. firms covered by StreetEvents that are not financial instruments, then merged them with DealScan to identify firms that had signed at least one debt contract, giving 6,105 firms with 13,171 deals between 2003 and 2018; after merging the financial, executive, and media data and removing firms not covered by Compustat or CRSP and CFOs whose identification did not match Capital IQ and Execucomp, the final sample is 7,649 deals across 1,915 firms (all four models in Table 3 report 7,649 observations).

DV: number of covenants, constructed by counting the covenants used in a debt contract, unweighted because prior contract research found the relative importance of individual clauses unclear (mean 1.05, SD 1.16; the exhaustive covenant list is in Appendix A). IV: CFO function-based language incongruity. CFO speeches were extracted from conference-call transcripts by title and name and taken from the managerial discussion section rather than the Q&A section, which is driven by analyst interrogation. Speeches were processed with Linguistic Inquiry and Word Count (LIWC): a positive-emotion dictionary for CFO-exhibited optimism, a risk-focus dictionary for CFO-exhibited risk-taking, a future-focus dictionary for CFO-exhibited future focus, and the Gamache et al. (2015) regulatory-focus dictionary for CFO-exhibited promotion focus, each computed as a percentage of the total words spoken and then averaged (weighted) across all of a CFO's speeches in a year. Principal component analysis with varimax rotation was run on the four attributes (Stata "pca," "rotate," and "predict"), and the data were recast along the first two principal component axes to form the index (Table 1, Panel A). Moderator 1: corresponding CEO language, built with the same four dimensions and the same PCA procedure from all speeches by the firm's CEO during the year in which the firm signed the debt contract (Table 1, Panel B). Moderator 2: media sentiment positivity, the annual average RavenPack composite sentiment score (CSS) across business-topic news articles with a relevance score of 100; the CSS ranges from 0 to 100, with values above 50 indicating positive sentiment and below 50 negative sentiment.

Controls cover loan characteristics (deal size as the log loan amount, average maturity in months, loan price as the log interest spread in basis points over LIBOR per dollar drawn down, and the number of prior transactions between the borrower and the lead bank), borrower characteristics (current ratio, ROA, cash holding ratio, log total assets, leverage, financially constrained set to 1 if Altman's Z-score is below 1.8, and prior covenant violations in the previous five years), lead-bank characteristics including the log distance between borrower and bank computed with the Google Maps Directions API, CFO demographics and individual governance controls (gender, race, age, tenure, log salary, log bonus), board independence, auditor turnover, and orthogonal CFO and CEO linguistic controls (pessimism, past focus, present focus, prevention focus). Year, 4-digit SIC industry, loan purpose, and lead bank fixed effects are included. Before estimation the authors winsorized all continuous independent, moderating, and control variables at 1% and 99%, expressed monetary values in constant 2018 dollars, and standardized all continuous predictors and control variables. Because the DV is an overdispersed count (mean 1.05, SD 1.16), the models are negative binomial rather than Poisson regressions, with standard errors clustered by firm; the maximum VIF is 4.27 and the mean 1.90. The design is observational and archival, so the estimates are associational; endogeneity is addressed not with a natural experiment or randomized design but with instrumental variable regressions using heteroskedasticity-based instruments (IVHI, Stata "ivreg2h").

**Key Findings**
All three hypotheses were supported in this single archival study. Hypothesis 1 was supported: in Model 1 of Table 3 the coefficient of CFO function-based language incongruity is positive and statistically significant (β = 0.05, p < .01). In economic terms, the number of debt covenants increases by 10.51% when CFO function-based language incongruity rises from its mean −1 SD to its mean +1 SD. Hypothesis 2 was supported: in Model 2 the interaction of CFO function-based language incongruity with corresponding CEO language is negative and significant (β = −0.02, p < .05), and the marginal effect of incongruity on the number of covenants is weaker when corresponding CEO language is high (β = 0.02, z = 1.23) than when it is low (β = 0.07, z = 3.86) (Table 4, Panel A). Hypothesis 3 was supported: in Model 3 the interaction of incongruity with media sentiment positivity is negative and significant (β = −0.03, p < .01), and the marginal effect of incongruity is stronger when media sentiment positivity is low (β = 0.08, z = 4.24) than when it is high (β = 0.01, z = 0.70) (Table 4, Panel B). Model 4, the fully saturated model, produces interaction coefficient estimates consistent with Models 2 and 3.

Robustness and supplementary analyses. Curvilinearity tests found the quadratic and cubic terms of CFO function-based language incongruity not significant (Table 5, Panel A); threshold specifications at the 50% and 75% thresholds and the mean level remained robust, but the results did not hold at the 25% threshold. In the IVHI estimation the coefficient of CFO function-based language incongruity remains positive and significant (β = 0.06, p < .001, Model 1 of Table 6), with statistical and economic significance equivalent to the main models, and support for Hypothesis 1 continued in Model 2 with bank fixed effects. Testing the information-asymmetry alternative explanation, the moderating effect of geographical distance between borrower and bank was not significant (Table 7, Panel A), so the authors fail to find evidence that information asymmetry drives the number of covenants. Hiring an industry-specialist auditor weakens the incongruity effect (β = −0.06, p < .05, Model 1 of Table 7, Panel B), and prior covenant violations significantly and positively moderate — that is, strengthen — the positive incongruity-covenants relationship (β = 0.03, p < .05, Table 7, Panel C). Examining the four linguistic attributes separately (Table 8), CFO-exhibited optimism and CFO-exhibited future focus are positively related to the number of covenants, CFO-exhibited risk-taking is not significant (β = −0.01, n.s.), and CFO-exhibited promotion focus is unexpectedly negatively related to the number of covenants (β = −0.03, p < .05), which the authors attribute to their empirical setting, in which all sampled CFOs were using bank financing to initiate a project and so may themselves be perceived as strongly promotion-focused.

**Theoretical Contribution**
The study extends role congruity theory by introducing within-role, function-based language incongruity as a previously overlooked source of the role incongruity effect, moving beyond the demography-based, between-role focus of prior work and showing language as an underexplored trigger. It contributes to the interorganizational contracting literature by foregrounding individuals (specifically the CFO's linguistic attributes) as antecedents of contract design, and advances understanding of the perceptual, microfoundational dimension linking perceived exchange hazards to governance choices.

**Practical Implication**
Boards selecting executives should weigh not only candidates' characteristics but also stakeholders' expectations of the role and how the candidate is perceived; firms can reduce partner-perceived exchange hazards by choosing executives who speak congruently with role expectations and by managing strategic communication when executives address external audiences. Executives should understand their role expectations and use congruent language to avoid triggering perceived hazards; bankers are an important, often-overlooked stakeholder audience.

**Limitations**
The authors do not directly measure whether banks hold different expectation levels or tolerance for CFO role incongruity, so surveys or field studies could capture that variation. Findings are drawn from U.S. bank debt contracting and may not generalize to other contract types or contexts where no ideal characteristic is associated with a given role. The study links incongruent language to more covenants but cannot establish performance implications—whether projects financed under more-covenant contracts ultimately perform better or worse is unclear.

**Future Research**
Future work could investigate why the influence of banks' executive expectations varies across firms and how that variation shapes strategic decisions, and whether role congruity theory of the executive applies in other settings and contract types. Researchers could examine how the individual linguistic attributes differ across industries or contexts, the interplay between perceived counterparty behaviors and the contract drafter's own attributes, and the conditions under which covenant levels translate into better or worse loan-project performance.

**APA 7th Citation**
Um, C. T., Guo, S.-L., Lumineau, F., Shi, W., & Song, R. (2022). The downside of CFO function-based language incongruity. *Academy of Management Journal*, 65(6), 1984-2013. https://doi.org/10.5465/amj.2019.0943
