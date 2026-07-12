---
id: amj-vol-67-no-6-oyedeji-2024
title: "Perceived Firm-Specific Human Capital: Mobility Constraint or Enhancer?"
authors:
  - "Oyedeji, B. A."
  - "Coff, R. W."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.0874"
volume: 67
issue: 6
pages: "1488-1524"

source: "AMJ/vol-67-no-6"
pdf_path: "library/AMJ/vol-67-no-6/pdfs/Oyedeji 2024 Perceived Firm-Specific Human Capital Mobility Constraint or Enhancer.pdf"
text_path: "library/AMJ/vol-67-no-6/text/Oyedeji 2024 Perceived Firm-Specific Human Capital Mobility Constraint or Enhancer.txt"
ingested_at: "2026-05-05"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords:
  - "perceived firm-specific human capital"
  - "worker mobility"
  - "turnover"
  - "job satisfaction"
  - "job embeddedness"
  - "job autonomy"
  - "resource-based theory"
  - "human capital theory"
theory:
  - "resource-based theory (Barney, 1991)"
  - "human capital theory (Becker, 1964)"
  - "supply-side mobility theory (Campbell, Coff & Kryscynski, 2012)"
  - "bounded rationality (March & Simon, 1958; Mullainathan & Thaler, 2000)"
  - "job embeddedness theory (Mitchell et al., 2001; Lee, Burch & Mitchell, 2014)"
  - "self-determination / autonomy (Deci & Ryan, 1985)"
topics:
  - "hr-practices"
  - "motivation-engagement"
  - "competitive-strategy"
  - "cross-national-comparative"
unit_of_analysis: "individual"
level_of_theory: "micro"
dependent_variable_family: "social"
methods: "Multi-sample empirical study using two archival panels (KLIPS 2002-2007 and NLSY79 1994-1996) and two newly collected primary surveys (US2023 and SK2023). Estimation via Stata's random-effects parametric survival time model (xtstreg) for the longitudinal KLIPS panel and logistic regression for cross-sectional samples; mediation tested via the khb decomposition for nonlinear probability models; ITCV used to address omitted variable bias."
sample:
  industry: "Cross-industry full-time employees (excluding self-employed, part-time, contract, and military workers); for-profit organizations in US2023 sample."
  country: "South Korea (KLIPS, SK2023) and United States (NLSY79, US2023)"
  time_period: "KLIPS 2002-2007 panel; NLSY79 1994-1996 cross-section; US2023 and SK2023 primary surveys collected in 2023"
  units: "Person-job-year observations (KLIPS panel); individuals (cross-sectional samples)"
  n: "KLIPS: 18,341 person-year observations from 5,403 individuals; NLSY79: 1,976; US2023: 1,208; SK2023: 1,428"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "sample consists of 5,403"
  sample_country: "two archival surveys and two primary surveys collected in very different contexts (South Korea and the United States)"
  sample_industry: "adult, full-time workers in for-profit"
  sample_time_period: "person-job-year, ranging from 2002 to 2007"
  theories_overview: "central to resource-based theory (Barney, 1991)"
  methods_overview: "survival time model (xtstreg)"
  keywords_source: "the relationship between workers’ perceptions of firm-specific human capital (FSHC) and turnover"
  hypotheses_source: "human-capital is positively associated with mobility."
  measures_overview: "Mobility is coded as 1 when a respondent changes"
  findings_overview: "the NLSY79 (OR 5 1.44, p , .001), but no effect in"
---

# Perceived Firm-Specific Human Capital: Mobility Constraint or Enhancer?

**Abstract**
We explore the relationship between workers' perceptions of firm-specific human capital (FSHC) and turnover. The belief that actual FSHC constrains mobility undergirds its critical role in resource-based theory. However, this rests on a strong assumption of information efficiency that market actors correctly assess how specific an individual's skills are, and price it appropriately. Emerging theoretical viewpoints dispute this, pointing out labor market imperfections and substantial difficulty in observing FSHC. We therefore develop theory about how perceived FSHC may relate positively to mobility by articulating a role for well-known supply-side mechanisms such as job satisfaction, embeddedness, and preference for job autonomy. Using two archival surveys and two primary surveys collected in very different contexts (South Korea and the United States), we found support for our theory. Perceptions of FSHC were associated with increased mobility and this effect was partially mediated by job satisfaction and job embeddedness. The effect was augmented for workers who value autonomy in their jobs (and who are more likely to exit if they perceived their skills as FSHC). Since the effect of perceived FSHC is quite different from that of extant theory which focused on actual FSHC, we explore implications for resource-based and human capital theories.

**Research Question**
Do workers' perceptions of firm-specific human capital (FSHC) constrain mobility as predicted by resource-based and human capital theories, or do such perceptions instead operate as a supply-side driver of turnover through psychological mechanisms of fit, satisfaction, and embeddedness?

**Hypotheses / Propositions**
H1. Workers' perception of firm-specific human capital is positively associated with mobility (turnover).
H2a. Job satisfaction negatively mediates the positive effect of perceived FSHC on mobility.
H2b. Job embeddedness negatively mediates the positive effect of perceived FSHC on mobility.
H3. Job autonomy importance positively moderates the positive effect of perceived FSHC on mobility (stronger for workers who value autonomy).

**Mechanism Process**
- IV(s): Perceived firm-specific human capital (perceived FSHC) — workers' views about the extent to which additional human capital gained at the focal firm would be less useful to other employers.
- DV(s): Worker mobility (turnover) — change to a new employer (binary).
- Mediators: Job satisfaction; job embeddedness (work-related fit, links, and sacrifice).
- Moderators: Importance of job autonomy to the worker.

The authors theorize that as workers' perceptions of FSHC increase, they engage in deeper assessment of their fit with the firm because they feel their career opportunities are tied closely to that employer. This triggers negative affect, regret, and counterfactual thinking, eroding job satisfaction and embeddedness, which in turn precipitate turnover. The relationship is amplified for workers who value autonomy because perceived FSHC violates a broader preference for career autonomy and induces uncertainty management behavior. The argument deliberately abandons the demand-side information-efficiency assumption underlying classical FSHC theory and rests on bounded rationality and supply-side mobility logic.

**Data & Measures**
The theory is tested on four datasets across two countries: two archival panels — KLIPS (South Korea; 18,341 person-year observations from 5,403 full-time individuals, 2002-2007) and NLSY79 (United States; 1,976 individuals, 1994-1996) — and two primary recall surveys collected in 2023, US2023 (n = 1,208) and SK2023 (n = 1,428). The dependent variable, mobility, is coded 1 when a respondent changes employer and 0 otherwise (a change in the prior three months in the 2023 surveys). Perceived FSHC (IV) uses single-item measures in the archival datasets and a newly developed, validated four-item scale in the primary samples (α = .93). Mediators are job satisfaction (a five-item scale modeled on the Brayfield & Rothe [1951] index; a single item in NLSY79) and job embeddedness (an adapted Felps et al. [2009] work-domain short-form scale, available only in US2023/SK2023). The moderator, job autonomy importance, is a dummy coded 1 when a worker ranks autonomy among their top two job attributes (primary samples only). Estimation uses Stata's random-effects parametric survival-time model (xtstreg) for the KLIPS panel and logistic regression for the three cross-sectional samples; mediation is decomposed with the khb method and omitted-variable bias is probed via an impact-threshold-of-a-confounding-variable (ITCV) analysis. The design is associational; no causal identification is claimed.

**Key Findings**
H1 was supported in three of the four samples: perceived FSHC raised the likelihood of mobility in the NLSY79 (OR = 1.44, p < .001; +44% odds), US2023 (OR = 1.72, p < .001), and SK2023 (OR = 1.24, p < .05), with the overall increase reported as 24%-72%. H1 was not supported in the longitudinal KLIPS sample, where the main effect was null (OR = 1.00) and turned significantly negative once job satisfaction or embeddedness was controlled (HR = 0.92, p < .05). H2a (job satisfaction as a negative mediator) held in all four samples — mediation of 6.51% (NLSY79), 20.85% (US2023), and 39.40% (SK2023); in KLIPS the null-but-positive total effect was suppressed to a negative direct effect. H2b (job embeddedness as a negative mediator) was supported only in the two primary samples that measured embeddedness (18.12% US2023; 63.61% SK2023); KLIPS and NLSY79 had no embeddedness measure. H3 (autonomy moderation) was supported in both primary samples: the FSHC × autonomy-importance interaction was OR = 1.88 (p < .05) in US2023 — raising mobility by 88% for autonomy-valuing workers, over a 60% main effect — and OR = 1.57 (p < .05) in SK2023, over a statistically null 7% main effect; H3 was not testable in the archival samples, which lacked an autonomy measure. The pattern was robust across probit, complementary log-log, restricted-sample, and organizational-commitment checks.

**Theoretical Contribution**
The study reverses the dominant demand-side prediction in resource-based and human capital theory by showing that perceived FSHC is positively, not negatively, associated with mobility, with effects partially mediated by job satisfaction and embeddedness and amplified by autonomy preference. By integrating bounded rationality and heterogeneous worker preferences with resource-based logic, the paper highlights a multilevel, supply-side pathway through which perceived firm specificity erodes rather than sustains employee retention. This creates a substantial dilemma for resource-based theory: if perceived firm specificity does not hinder mobility, alternative mechanisms must be identified to explain how human-capital-based competitive advantage is sustained.

**Practical Implication**
Firms cannot rely on the assumption that firm-specific knowledge mechanically locks employees in; workers who perceive their skills as firm-specific are more, not less, likely to leave, particularly when they value autonomy. To realize human-capital-based competitive advantage, firms need complementary practices that motivate, satisfy, and embed workers who possess (or perceive themselves to possess) firm-specific skills, rather than depending on mobility frictions alone.

**Limitations**
The four datasets use different measurement instruments and time periods, so results across samples are not precisely comparable, and no objective measure of actual FSHC is available against which perceived FSHC can be benchmarked. The newly collected US2023 and SK2023 samples are cross-sectional and smaller than KLIPS, and were captured during the post-COVID-19 mobility surge, raising potential concerns about inflated effect sizes (though replicated patterns in NLSY79 mitigate this). Endogeneity from omitted variables remains possible despite ITCV checks, and the data lack employer information needed for matching designs.

**Future Research**
Develop and validate reliable objective measures of actual FSHC (e.g., patent self-citations or controlled experimental designs) so that perceived and actual FSHC can be compared directly. Investigate how firm-level constructs such as organizational structure, culture, and HR practices (e.g., compensation) shape the underlying mechanisms of job satisfaction, embeddedness, and autonomy that link perceived FSHC to turnover. Pursue multilevel research linking psychological processes around perceived skill specificity to firm-level value creation and human-capital investment decisions.

**APA 7th Citation**
Oyedeji, B. A., & Coff, R. W. (2024). Perceived firm-specific human capital: Mobility constraint or enhancer? *Academy of Management Journal*, 67(6), 1488-1524. https://doi.org/10.5465/amj.2021.0874
