---
id: nbs-2026-02-li-2026-female-equity-analysts
title: "Female Equity Analysts and Corporate Environmental and Social Performance"
authors:
  - "Li, K."
  - "Mai, F."
  - "Wong, G."
  - "Yang, C."
  - "Zhang, T."
year: 2026
journal: "Management Science"
doi: "https://doi.org/10.1287/mnsc.2024.06429"
volume: null
issue: null
pages: null

source: "NBS/2026-02"
pdf_path: "library/NBS/2026-02/pdfs/Li 2026 Female Equity Analysts and Corporate Environmental and Social Performance.pdf"
text_path: "library/NBS/2026-02/text/Li 2026 Female Equity Analysts and Corporate Environmental and Social Performance.txt"
ingested_at: "2026-04-17"
extraction_model: "claude-opus-4-6"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords:
  - "analyst coverage"
  - "analyst monitoring"
  - "analyst reports"
  - "cognition"
  - "corporate environmental and social performance"
  - "earnings conference calls"
  - "female equity analysts"
  - "FinBERT"
  - "readability"
  - "RepRisk"
theory:
  - "gender differences in values and preferences (psychology/economics)"
  - "analyst monitoring / governance role of analysts"
  - "information intermediary theory"
topics:
  - "gender-in-organizations"
  - "corporate-governance"
  - "esg-disclosure"
  - "csr-strategy"
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "mixed"
methods: "Archival empirical analysis combining hand-collected analyst gender data with E&S ratings; panel regressions with firm and year fixed effects; difference-in-differences around broker closures as a quasi-exogenous shock to female (male) analyst coverage; active-learning fine-tuning of FinBERT for E&S-topic classification on 2.4M analyst reports and 120K earnings call transcripts; Structural Topic Modeling (STM) and Linguistic Inquiry and Word Count (LIWC) for thematic, cognitive, and linguistic analysis; event-study tests of market reactions to analysts' E&S-related tone"
sample:
  industry: "Multi-industry publicly listed firms with analyst coverage (Fama-French 12 industries)"
  country: "United States"
  time_period: "2005-2021 (main E&S sample); 2004-2020 (report-level and recommendation samples)"
  units: "Firm-year observations; analyst reports; earnings conference calls"
  n: "20,423 firm-year observations covering 3,567 unique firms; more than 11,000 sell-side equity analysts; 2.4 million analyst reports; 120,000 earnings call transcripts"

evidence:
  sample_n: "The sample consists of 20,423 firm-year observations (representing 3,567 unique firms)"
  sample_country: "U.S. equities over the period 2004–2020"
  sample_industry: "Industry fixed effects are based on Fama-French 12-industry classifications"
  sample_time_period: "observations (representing 3,567 unique firms) with data on corporate E&S performance over the period 2005–2021"
  theories_overview: "because of gender differences in values and preferences"
  methods_overview: "machine-learning models to analyze more than 2.4 million analyst reports and 120,000 earnings"
  keywords_source: "Keywords: analyst coverage • analyst monitoring • analyst reports • cognition"
---

# Female Equity Analysts and Corporate Environmental and Social Performance

**Abstract**
stakeholders, and the environment, in both research reports and earnings conference calls. They also display distinct cognitive and linguistic patterns when discussing E&S issues. Fur­ thermore, female analysts are more likely to issue lower stock recommendations and target prices (lower stock recommendations) following negative E&S discussions in their reports (E&S incidents) than male analysts. Finally, investors respond more strongly to female analysts’ negative tones when discussing E&S issues. Overall, our findings suggest that gender diversity among analysts plays a significant role in shaping corporate E&S practices and provide new insights into the origins of gender differences in skills within the equity analyst profession.

**Research Question**
Does female equity analyst coverage causally influence firms' environmental and social (E&S) performance, and through what mechanisms—differences in research activities, thematic focus, cognitive and linguistic approaches, and post-report actions—do female analysts exert this influence compared with their male counterparts?

**Mechanism Process**
- IV(s): Number of female (and male) analysts covering a firm; exogenous shock to female (male) analyst coverage via broker closures
- DV(s): Firm E&S performance (LSEG/Refinitiv E&S scores, with robustness using ASSET4, KLD, Sustainalytics); probability that an analyst report or earnings-call question addresses E&S topics; readability and cognitive-processing indicators of E&S discussions; stock recommendations and target prices following negative E&S content; short-window market reactions to analysts' E&S tone
- Mediators: Female analysts' greater propensity to write and ask about E&S issues (especially regulatory compliance, stakeholders, environment); more sophisticated cognitive processing and more readable E&S communication; greater willingness to downgrade recommendations and target prices after negative E&S content
- Moderators: E&S incident occurrence (RepRisk events); brokerage size (top-10 vs. non-top-10); firm characteristics (size, Tobin's Q, governance controls)

Drawing on psychological and economic evidence that women place greater weight than men on the well-being of others, communities, and the environment, the authors argue that female equity analysts—who already constitute a selected, highly skilled group in a male-dominated profession—are more attentive to corporate E&S issues than male analysts. Through their research activities (writing reports, questioning managers on earnings calls), female analysts identify value-relevant E&S risks and communicate them with greater thematic breadth (regulatory compliance, stakeholder welfare, environment), more sophisticated cognitive processing, and greater clarity. These signals exert governance pressure on management because female analysts are also more willing to downgrade recommendations and target prices after negative E&S content, and investors react more strongly to their negative E&S tones. Together these information-production and monitoring channels lead firms with more female analyst coverage to improve their E&S performance.

**Theoretical Contribution**
The paper contributes to the gender-and-finance literature by showing that female equity analyst coverage causally improves corporate E&S performance, identifying gender diversity among sell-side analysts as an impetus for firms to adopt more environmentally and socially responsible policies. It extends the analyst-monitoring literature by taking a gender lens and uncovering the specific textual, cognitive, and action-based mechanisms through which female analysts influence firm outcomes, thereby explaining observed gender differences in analyst impact first documented by Kumar (2010). Methodologically, it advances the finance/accounting literature on computational linguistics by introducing a data-centric active-learning approach to fine-tune FinBERT on analyst reports and earnings-call transcripts for E&S-topic classification.

**Practical Implication**
The findings imply that firms, brokerages, and regulators interested in strengthening corporate E&S performance should promote gender diversity in the equity analyst profession, since female analysts act as effective external monitors of E&S issues. Investors and asset managers can use female analysts' reports and negative tones as informative signals of firms' E&S risks and are already shown to respond more strongly to them. For corporate management, the evidence suggests that expanding coverage by female analysts increases the likelihood that E&S concerns will be raised publicly and priced into stock recommendations.

**Limitations**
The analysis relies on hand-collected gender inferences and on E&S ratings (e.g., LSEG, ASSET4, KLD, Sustainalytics) that are known to contain measurement noise and inter-rater disagreement. The broker-closure design yields a small, clean treated-control sample, so the economic magnitude of the causal effect should be interpreted with care. The machine-learning pipeline, while extensively validated, still depends on the quality of human-labeled training data and on the coverage of the FinBERT backbone.

**Future Research**
Not reported in paper

**APA 7th Citation**
Li, K., Mai, F., Wong, G., Yang, C., & Zhang, T. (2026). Female equity analysts and corporate environmental and social performance. *Management Science*. https://doi.org/10.1287/mnsc.2024.06429
