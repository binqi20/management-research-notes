---
id: nbs-2025-12-maiolini-2026
title: "The Persuasive Power of Signals: How Narratives, Fundraising Model, and Number of Borrowers Drive Success in Lending-Based Prosocial Crowdfunding"
authors:
  - "Maiolini, Riccardo"
  - "Cappa, Francesco"
  - "Kalanoski, Dimitrija"
  - "Quaratino, Giovanni Raimondo"
year: 2026
journal: "Business & Society"
doi: "https://doi.org/10.1177/00076503251390311"
volume: 65
issue: 6
pages: "1605-1642"

source: "NBS/2025-12"
pdf_path: "library/NBS/2025-12/pdfs/Maiolini 2025 The Persuasive Power of Signals How Narratives, Fundraising Model, and Number of Borrowers Drive Success in Lending-Based Prosocial Crowdfunding.pdf"
text_path: "library/NBS/2025-12/text/Maiolini 2025 The Persuasive Power of Signals How Narratives, Fundraising Model, and Number of Borrowers Drive Success in Lending-Based Prosocial Crowdfunding.txt"
ingested_at: "2026-06-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["crowdfunding", "extrinsic", "intrinsic", "Kiva", "lending-based", "narrative", "prosocial", "signaling theory"]
theory: ["signaling theory (Spence, 2002; Bergh et al., 2014; Connelly et al., 2011; Steigenberger et al., 2024)"]
topics: ["impact-investing", "social-innovation", "signaling-theory", "sustainable-finance"]
unit_of_analysis: "organization"
level_of_theory: "macro"
dependent_variable_family: "social"
methods: "Quantitative observational study of 773,916 Kiva loan campaigns (2019-2022); computer-aided textual analysis in Python classifying how/why narrative words (Falchetti et al. 2022 framework, >95% intercoder agreement); Poisson regression on funding time with regional and project controls."
sample:
  industry: "Lending-based prosocial crowdfunding (microfinance loans to micro and small enterprises) on the Kiva platform"
  country: "Global (backers from over 60 countries)"
  time_period: "2019-2022"
  units: "Crowdfunding loan campaigns/projects"
  n: "773,916 campaigns"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
# Each value is a <=25-word verbatim quote from the PDF text, or the literal
# string "Not reported in paper" (case-sensitive). See the Evidence anchors
# section above for the full schema.
evidence:
  sample_n: "Our analysis examines 773,916 campaigns launched on the Kiva platform"
  sample_country: "total of 773,916 projects globally, supported by backers from over 60 countries."
  sample_industry: "LBPSC, a model particularly utilized by"
  sample_time_period: "data from campaigns initiated between 2019, when the platform introduced"
  theories_overview: "Drawing on signaling theory, we examine how the interplay of multiple signals,"
  methods_overview: "success, we applied Poisson regression analysis. This methodological choice"
  keywords_source: "crowdfunding, extrinsic, intrinsic, Kiva, lending-based, narrative, prosocial,"
---

# The Persuasive Power of Signals: How Narratives, Fundraising Model, and Number of Borrowers Drive Success in Lending-Based Prosocial Crowdfunding

**Abstract**
Crowdfunding has emerged as a significant alternative financing source, drawing the attention of scholars, practitioners, and policymakers. This study examines the success factors in lending-based prosocial crowdfunding (LBPSC), a model that integrates economic objectives with social impact. Drawing on signaling theory, we examine how the interplay of multiple signals, narrative framing, fundraising models, and borrower counts influences the success of campaigns. Our analysis of the Kiva platform provides empirical support for our theoretical claims and deepens understanding of the LBPSC phenomenon. Our findings also provide practical guidance for entrepreneurs and policymakers to design more effective crowdfunding campaigns.

**Research Question**
Under what conditions does the interaction of multiple signals positively influence the success of LBPSC campaigns? Specifically, how do project narrative framing (how vs. why), the fundraising model, and the number of borrowers jointly shape funding success.

**Mechanism Process**
- IV(s): How_Narrative_weighted (operational/feasibility narrative cues); Why_Narrative_weighted (mission/purpose narrative cues), both derived via computer-aided textual analysis and normalized by description length.
- DV(s): Funding time (days from listing to full funding), an inverse proxy for LBPSC campaign success.
- Moderators: Flexible fundraising enabled (keep-it-all funding model dummy); Borrower count (number of borrowers per campaign).
- Controls: Funded amount, backers total count, teams total count, and regional dummies (North America, Africa, South America, Asia, Middle East, Oceania, Eastern Europe).

Drawing on signaling theory, the paper argues that backers facing information asymmetry read narrative, funding-model, and borrower-count cues to gauge a project's feasibility and prosocial purpose, which activate extrinsic versus intrinsic motivations respectively. How narratives lengthen funding time (reduce success) by diluting emotional/prosocial resonance, while why narratives shorten it (raise success) by aligning with backers' altruistic values. Flexible financing buffers the negative effect of how narratives but undercuts the positive effect of why narratives by introducing feasibility doubt, and a higher borrower count signals broader collective impact that accelerates funding across both narrative types.

**Theoretical Contribution**
The study extends signaling theory to the LBPSC context by demonstrating how multiple signals (narratives, fundraising model, borrower count) operate jointly rather than as isolated cues, and how their alignment or misalignment activates backers' intrinsic and extrinsic motivations. It empirically validates and extends Falchetti et al.'s (2022) how/why narrative framework in prosocial microlending, showing the two narrative types are non-exclusive and that contextual moderators can reverse or amplify their effects on campaign success.

**Practical Implication**
Entrepreneurs and borrowers should foreground why (purpose-driven) narratives to accelerate funding and treat the choice of flexible financing cautiously because it weakens purpose-driven appeals while compensating for operational ones. Platform designers and policymakers can use these findings to build templates, prompts, and feedback tools that guide narrative framing, funding-structure, and borrower-configuration choices, advancing financial inclusion for underserved micro and small enterprises.

**Limitations**
The analysis focuses on a single platform (Kiva), which may limit generalizability to other crowdfunding platforms with different operating models and user demographics. It also centers exclusively on LBPSC, leaving open whether the effects of storytelling, funding methods, and group size extend to traditional lending or to equity- and reward-based crowdfunding.

**Future Research**
Future studies should examine multiple and diverse crowdfunding platforms and broaden the scope across crowdfunding types (equity, reward) to test the robustness of the narrative, financing, and borrower-count effects. Longitudinal designs tracking projects from inception through post-funding could reveal how narrative techniques evolve, and additional contextual factors (cultural differences, business-model innovations, regional regulatory environments) warrant investigation.

**APA 7th Citation**
Maiolini, R., Cappa, F., Kalanoski, D., & Quaratino, G. R. (2026). The persuasive power of signals: How narratives, fundraising model, and number of borrowers drive success in lending-based prosocial crowdfunding. *Business & Society*, 65(6), 1605–1642. https://doi.org/10.1177/00076503251390311
