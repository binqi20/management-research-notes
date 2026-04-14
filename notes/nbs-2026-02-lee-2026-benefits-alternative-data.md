---
id: nbs-2026-02-lee-2026-benefits-alternative-data
title: "Who Benefits from Alternative Data for Credit Scoring? Evidence from Peru"
authors:
  - "Lee, J. Y."
  - "Yang, J."
  - "Anderson, E. T."
year: 2026
journal: "Journal of Marketing Research"
doi: "https://doi.org/10.1177/00222437251360996"
volume: 63
issue: 1
pages: "105-126"

source: "NBS/2026-02"
pdf_path: "library/NBS/2026-02/pdfs/Lee 2026 Who Benefits from Alternative Data for Credit Scoring Evidence from Peru.pdf"
text_path: "library/NBS/2026-02/text/Lee 2026 Who Benefits from Alternative Data for Credit Scoring Evidence from Peru.txt"
ingested_at: "2026-04-14"
extraction_model: "claude-opus-4-6"
extraction_version: "v1"

paper_type: "empirical-quantitative"
keywords:
  - "alternative data"
  - "financial inclusion"
  - "consumer finance"
  - "credit cards market"
theory:
  - "information asymmetry in credit markets"
  - "algorithmic decision-making and fairness"
  - "distributional consequences of data"
topics:
  - "financial-accounting"
  - "sustainable-finance"
  - "ai-automation"
  - "developing-economies"
unit_of_analysis: "individual"
level_of_theory: "micro"
dependent_variable_family: "financial"
methods: "Observational study using merged administrative and proprietary data (credit card applications, loyalty card transaction data, Peruvian administrative credit registry RCC, and Equifax utility payment score RP2). Machine-learning credit scoring algorithms trained separately for applicants with and without credit history; simulation of credit card approval decisions under alternative business objectives; counterfactual comparisons of approval rates with and without retail data."
sample:
  industry: "Consumer credit / retail (credit card issuer owned by a Peruvian multi-sector company)"
  country: "Peru"
  time_period: "January 2021-September 2023 (loyalty and credit registry); credit card applications from June 2022"
  units: "Individual credit card applicants (with and without formal credit history)"
  n: "Applicants grouped into six cohorts (e.g., Group A: 24,899 approved applicants with credit history; Group C: 1,719; Group D: 1,016; Group F: 10,132 no-history rejected applicants also denied elsewhere)"
---

# Who Benefits from Alternative Data for Credit Scoring? Evidence from Peru

**Abstract**
The World Bank estimates that 1.4 billion individuals worldwide are unbanked, lacking access to credit due to the absence of traditional credit scores. In this article, the authors demonstrate how retail transaction data can be used to construct an alternative credit score, potentially expanding credit access for these individuals. The study utilizes a unique dataset obtained through a partnership with a Peruvian company. The authors merge customer loyalty data and credit card repayment data with administrative records from the Peruvian ﬁnancial system that provide individuals’ detailed ﬁnancial histories. This comprehensive dataset allows the authors to construct credit scores for people both with and without a credit history. Through simulations of credit card approval decisions, they ﬁnd that incorporating retail data increases approval rates for individuals without a credit history, from 16% to between 31% and 48%. In contrast, for those with an established credit history, approval rates remain largely unchanged, at around 88%. The authors investigate why retail data particularly beneﬁts people without a credit history and discuss the broader implications of this credit scoring methodology for consumers, ﬁrms, and policy makers. The ﬁndings highlight the methodology’s potential to transform credit access for millions of previously unbanked individuals.

**Research Question**
Can retail transaction data be used as alternative data to construct credit scores that expand credit access for individuals lacking formal credit histories, and who benefits most from incorporating this alternative data into credit scoring decisions?

**Mechanism Process**
- IV(s): Inclusion of retail loyalty card transaction data (shopping behavior features) in credit scoring algorithms, alongside self-reported socioeconomic characteristics, utility payment-based scores, and administrative credit registry (RCC) data.
- DV(s): Simulated credit card approval rates and portfolio default risk, separately for applicants with and without a formal credit history.
- Mediators: Improved risk differentiation via the predictive signal embedded in retail shopping behavior (product mix, consistency of shopping routines).
- Moderators: Applicant's credit-history status (no-history vs. with-history); lender's business objective (market share expansion vs. portfolio risk minimization); baseline stringency of the lender's credit policy.

For applicants without a formal credit history, lenders face severe information asymmetry because conventional socioeconomic and utility-based predictors produce highly overlapping risk score distributions for defaulters and non-defaulters. Retail transaction data adds orthogonal behavioral signals (what and how consumers buy) that sharpen the ability to separate low- and high-risk individuals, which expands the set of applicants whose predicted risk falls below approval thresholds. For applicants already in the credit registry, registry data already captures most repayment-relevant information, so retail data produces only marginal reclassification and may even tighten approval when used to identify higher-risk borrowers inside the existing pool.

**Theoretical Contribution**
The paper contributes to four literatures: the distributional consequences of data and algorithmic decision-making in marketing, the use of alternative data for credit scoring (extending Lee, Yang, and Anderson 2025 beyond grocery to multi-domain retail), the emerging literature on nonfinancial firms entering consumer lending, and information-frictions research in credit markets. It reframes marketing data as a nonmarketing asset whose predictive power is concentrated precisely where traditional financial data is missing, and shows that the welfare effect of alternative data depends on which segment of the applicant pool currently suffers from information asymmetry rather than on data volume per se.

**Practical Implication**
For lenders, retail transaction data is most valuable as a "second look" tool for evaluating applicants who would otherwise be rejected due to missing credit histories, and can nearly triple approval rates for no-history applicants (from 15.6% to as high as 47.8%) depending on risk appetite. For policy makers, the results suggest alternative data can advance financial inclusion goals for unbanked populations, but realizing these gains requires attention to long-term consumer welfare, procedural and distributive fairness, strategic manipulation risks, and privacy safeguards around cross-sector data sharing.

**Limitations**
Selection bias remains because the algorithms cannot account for approved applicants who never activated their cards or for rejected applicants who do not appear in the credit registry. The sample is restricted to individuals who voluntarily enrolled in a single firm's loyalty program, limiting generalizability to the broader applicant pool and excluding people entirely invisible to traditional financial data. The analysis relies on simulated rather than randomized field-experimental approval decisions.

**Future Research**
The authors suggest extending analyses to broader pools of potential borrowers beyond loyalty-program members, conducting field experiments that deploy alternative-data scoring algorithms in production to validate downstream behavioral effects, and investigating how alternative data reshapes organizational practices beyond credit scoring, including marketing targeting, customer acquisition strategies, and post-approval customer service and operations for newly included borrowers.

**APA 7th Citation**
Lee, J. Y., Yang, J., & Anderson, E. T. (2026). Who benefits from alternative data for credit scoring? Evidence from Peru. *Journal of Marketing Research*, 63(1), 105-126. https://doi.org/10.1177/00222437251360996
