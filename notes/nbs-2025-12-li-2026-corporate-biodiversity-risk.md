---
id: nbs-2025-12-li-2026-corporate-biodiversity-risk
title: "Corporate biodiversity risk exposure in China: A system-based perspective from natural capital theory using machine and deep learning algorithms"
authors:
  - "Li, Peigong"
  - "Shahzad, Umeair"
year: 2026
journal: "Ecological Economics"
doi: "https://doi.org/10.1016/j.ecolecon.2025.108906"
volume: 242
issue: null
pages: "108906"

source: "NBS/2025-12"
pdf_path: "library/NBS/2025-12/pdfs/Li 2025 Corporate biodiversity risk exposure in China A system-based perspective from natural capital theory using machine and deep learning algorithms.pdf"
text_path: "library/NBS/2025-12/text/Li 2025 Corporate biodiversity risk exposure in China A system-based perspective from natural capital theory using machine and deep learning algorithms.txt"
ingested_at: "2026-06-10"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["Biodiversity risk", "Natural capital theory", "Machine learning", "China"]
theory: ["natural capital theory (system-based perspective; Pelenc and Ballet, 2015)", "stakeholder theory (Ren et al., 2023)", "agency theory", "resource-based view (M.-J. Chen et al., 2021)"]
topics: ["biodiversity", "esg-disclosure", "stakeholder-theory", "china"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "environmental"
methods: "Quantitative panel study of Chinese listed firms. Baseline mixed-effects (multilevel) logistic regression with time and industry effects on a binary biodiversity-risk-exposure outcome; subsequently modeled with three machine learning algorithms (support vector regression, random forest, K-nearest neighbor) and two deep learning models (LSTM, deep multilayer perceptron), validated via normal training, k-fold cross-validation, and bootstrap bagging."
sample:
  industry: "Publicly listed firms across SIC-classified industries (e.g., agriculture/forestry/fisheries, water conservancy, utilities, real estate, manufacturing); high- vs low-biodiversity-sensitivity industries"
  country: "China"
  time_period: "2011 to 2022 (environmental data from 2010-2022)"
  units: "Firm-year observations of publicly listed Chinese firms"
  n: "1960 listed firms; initial 32,180 firm-year observations reduced to 24,477 after filtering; regression N = 20,535"

evidence:
  sample_n: "sample initially comprises 32,180 firm-year observations"
  sample_country: "The study focuses on Chinese enterprises due to their growing"
  sample_industry: "(agriculture, forestry, and fisheries) exhibits the highest risk, followed"
  sample_time_period: "firms in China, covering the period from 2011 to 2022. China is selected"
  theories_overview: "builds on the system-based perspective of natural capital theory"
  methods_overview: "machine learning algorithms such as support vector regression, random forest, and K-nearest neighbor"
  keywords_source: "Natural capital theory"
---

# Corporate biodiversity risk exposure in China: A system-based perspective from natural capital theory using machine and deep learning algorithms

**Abstract**
The results show that firms with high resource use, carbon emissions, supply chain concentration, and financial leverage face greater biodiversity risk. In contrast, firms that invest in green innovation, attract institutional investors, and establish environmental governance committees report lower biodiversity exposure.

**Research Question**
Which firm-level operational, financial, and governance attributes are associated with heightened or reduced corporate biodiversity risk exposure, and can machine-learning and deep-learning algorithms predict this exposure more effectively than conventional methods? The study addresses the gap that "current literature lacks a systematic framework connecting firm-level choices to biodiversity risk disclosure."

**Mechanism Process**
- IV(s): Operational activities (resource/water consumption, carbon emissions/environmental footprints, supply chain concentration); financial activities (green innovation, firm size, financial leverage, profitability); governance activities (institutional investors, environmental governance board committee)
- DV(s): Corporate biodiversity risk exposure — a binary indicator derived from the frequency of biodiversity-related terms in annual reports (He et al.'s 2024 Biodiversity Concerns Index; risk score = 1 if terms appear more than twice, 0 otherwise)
- Mediators: Not reported in paper
- Moderators: Industry biodiversity sensitivity (high- vs low-sensitivity industries) tested via split-sample analysis

Grounded in the system-based perspective of natural capital theory, the paper argues that firms are embedded within interdependent ecological systems (interconnectedness), depend on ecosystem services (dependency), and feed back into natural-capital degradation through pollution and resource extraction (feedback loops). Resource-intensive operations and concentrated supply chains raise ecological vulnerability and the salience of biodiversity risk, while green innovation, scale/profitability slack, institutional ownership, and dedicated environmental committees reduce information asymmetry and agency costs, buffering exposure. High financial leverage constrains mitigation investment and amplifies exposure.

**Theoretical Contribution**
The paper extends the system-based perspective of natural capital theory into the corporate domain, reframing firms from passive recipients of ecological risk into active agents that drive biodiversity risk, yielding a bidirectional framework linking corporate decisions to biodiversity outcomes. It also delivers a validated empirical model of the core operational, financial, and governance predictors of biodiversity risk exposure and demonstrates a methodological roadmap for applying deep learning to test corporate environmental-finance models beyond the assumptions of traditional regression.

**Practical Implication**
Biodiversity risk is a predictable outcome of internal decisions (resource use, footprints, supply chain configuration, leverage) rather than an external shock, so firms can manage it through operational and financial strategy. For investors, governance structures such as institutional ownership and board-level environmental committees serve as credible signals of ecological risk-management capacity, informing investment screening, portfolio construction, and engagement. For policymakers, the findings support mandatory biodiversity-related disclosures and governance reforms that treat biodiversity loss as financially material.

**Limitations**
Measuring corporate biodiversity risk exposure is challenging due to the absence of standardized metrics; the text-analysis approach to corporate reports, while widely accepted, has limitations, and the authors recommend validating results with alternative biodiversity-risk measures. Conclusions on model performance should be interpreted with caution because the biodiversity-concern intensity is estimated via textual analysis — a setting that favors deep learning models that learn contextual patterns; in settings relying solely on accounting ratios and structured financial data, the relative effectiveness of machine and deep learning may differ.

**Future Research**
The proposed empirical approach can be extended to other socio-economic contexts beyond China. Future work should explore the mechanisms and boundary conditions that modulate the impact of these operational, financial, and governance predictors, and should test the relative effectiveness of machine-learning versus deep-learning approaches in contexts using structured financial data rather than textual disclosure, requiring careful model selection.

**APA 7th Citation**
Li, P., & Shahzad, U. (2026). Corporate biodiversity risk exposure in China: A system-based perspective from natural capital theory using machine and deep learning algorithms. *Ecological Economics*, 242, 108906. https://doi.org/10.1016/j.ecolecon.2025.108906
