---
id: nbs-2026-01-wang-2026-invests-gets-funded
title: "Who Invests, Who Gets Funded: Gender and Racial Bias in LLM-Generated Investment Advice"
authors:
  - "Wang, Ye (Emma)"
  - "Gu, Kexin"
year: 2026
journal: "Journal of Business Ethics"
doi: "https://doi.org/10.1007/s10551-026-06251-6"
volume: null
issue: null
pages: null

source: "NBS/2026-01"
pdf_path: "library/NBS/2026-01/pdfs/Wang 2026 Who Invests, Who Gets Funded Gender and Racial Bias in LLM-Generated Investment Advice.pdf"
text_path: "library/NBS/2026-01/text/Wang 2026 Who Invests, Who Gets Funded Gender and Racial Bias in LLM-Generated Investment Advice.txt"
ingested_at: "2026-06-22"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["Investment preferences", "Large language models", "Behavioral biases", "Generative AI"]
theory: ["business ethics (legitimacy, fiduciary responsibility, distributive justice)", "algorithmic fairness", "implicit bias / stereotype content (Fiske et al., 2002)"]
topics: ["ai-ethics", "responsible-investing", "racial-inequality"]
unit_of_analysis: "individual"
level_of_theory: "macro"
dependent_variable_family: "social"
methods: "Two-sided algorithmic audit experiment on LLM-generated investment advice (GPT-4 Turbo baseline; replicated on GPT-4.1, GPT-4o, Claude 3.5 Sonnet, Llama 3.1 8B). Demographic cues manipulated implicitly (names) and explicitly (stated race/gender) in prompts; analysis via Pearson chi-square tests, two-sample t-tests, and OLS regressions with fund and year-quarter fixed effects, standard errors clustered by institution."
sample:
  industry: "Mutual funds / robo-advisory financial services (LLM-generated investment recommendations); fund characteristics classified via Fama-French 48 industries"
  country: "United States (CRSP Mutual Fund Database)"
  time_period: "Funds sampled 2002-2023; analysis focuses on Q1 2022 to Q4 2023 (eight quarters)"
  units: "Investor profiles and mutual fund managers (synthetic, demographically varied) querying LLMs"
  n: "800 fund-quarter observations (100 funds x 8 quarters); up to 102,309 investor-allocation observations and 12,800 implicit / 3,200 explicit fund-manager observations"

evidence:
  sample_n: "The dataset used in this study consists of 800 mutual fund"
  sample_country: "sampled from a broader dataset in the CRSP"
  sample_industry: "Industry classification is based on the Fama–French 48 industries"
  sample_time_period: "first quarter of 2022 to the fourth quarter of 2023"
  theories_overview: "three interrelated nor"
  methods_overview: "We use Pearson’s chi-square test to evaluate this hypoth"
  keywords_source: "Keywords Investment preferences · Large language models · Behavioral biases · Generative AI"
---

# Who Invests, Who Gets Funded: Gender and Racial Bias in LLM-Generated Investment Advice

**Abstract**
Do large language models (LLMs) generate unbiased financial advice across investor and fund manager demographics? We develop a two-sided audit framework to evaluate demographic bias in LLM-generated investment advice and apply it to multiple large language models, with GPT-4 Turbo as the primary baseline. On the investor side, fund selections are similar across demographic groups and rely on financial criteria, but recommended investment amounts vary when investor names signal race or gender, despite identical age and income. On the fund manager side, capital allocations favor nonBlack and male managers: racial disparities persist even under explicit disclosure, while gender-related differences are more pronounced under name-based cues. Bias patterns are qualitatively similar across models, with differences in magnitude between implicit and explicit demographic signaling. These results suggest that, even when LLMs incorporate core financial reasoning, demographic signals can affect allocation decisions, with effects that tend to be stronger under implicit signaling, potentially replicating existing market inequalities and raising concerns about impartiality in financial advising. The proposed audit framework provides a generalizable approach for identifying and evaluating demographic bias in AI-driven financial advisory systems.

**Research Question**
Do LLM-driven financial advisory systems generate systematically different fund selections and capital allocations when investor or fund-manager race and gender are signaled implicitly (through names) or explicitly (through direct statements), even when financial fundamentals are held constant?

**Mechanism Process**
- IV(s): Demographic signal of investor/fund-manager race and gender — operationalized as a binary indicator for whether a race/gender-evocative name is included (implicit condition) or race/gender is directly stated (explicit condition); manager-side `Black` and `Male` dummies.
- DV(s): Recommended fund selection (categorical fund ID) and recommended investment amount in US dollars (continuous, plus an above-median dummy) generated by the LLM.
- Mediators: Not reported in paper (the LLM's internal token-prediction associations between demographic cues and perceived competence/trustworthiness are posited but not measured).
- Moderators: Task structure (constrained fund selection vs. open-ended allocation); signaling mode (implicit vs. explicit); investor age and income brackets; model identity (GPT-4 Turbo, GPT-4.1, GPT-4o, Claude 3.5 Sonnet, Llama 3.1 8B).

LLMs are not trained to be neutral but to reproduce statistical patterns in historical financial data that embed demographic disparities; when a task is under-specified (open-ended allocation), demographic cues fill the gap and shift outputs, whereas constrained tasks anchored to numeric criteria (fund selection by Sharpe ratio, alpha, NAV) suppress bias. For GPT-4 Turbo, fund selection shows no significant bias (chi-square p = 0.228), but allocation rises by ~$1,157 when investor names are added; Black fund managers receive significantly lower allocations even under explicit disclosure, while gender effects emerge mainly under implicit name-based cues — consistent with the view that structured rules constrain bias while discretionary judgment reintroduces it.

**Theoretical Contribution**
The paper introduces a two-sided audit framework that separates investor-side and fund-manager-side bias, showing that the same LLM expresses role-specific bias that varies in magnitude and in sensitivity to explicit versus implicit cues. It connects algorithmic-fairness diagnostics to core business-ethics constructs — legitimacy, fiduciary responsibility (duties of care and loyalty), and distributive justice — arguing that procedural fixes such as disclosure or richer prompts are insufficient to satisfy ethical impartiality requirements.

**Practical Implication**
Financial institutions deploying LLM advisory tools should run pre-deployment audits testing both investor- and manager-side outcomes under explicit and implicit demographic conditions, use standardized prompts tied to financial criteria, compare outputs across models before version changes, monitor allocation gaps by protected attributes, and add human review for sensitive cases to keep recommendations anchored in financial fundamentals.

**Limitations**
The experimental tasks are abstractions of professional due diligence and omit a direct human-advisor baseline, so the authors caution against concluding flatly that "LLMs are biased" — the models reproduce the direction of known market disparities but at smaller magnitudes, and an overstated conclusion could discourage adoption that might reduce real-world bias. Cross-model heterogeneity also indicates sensitivity to training data and alignment techniques.

**Future Research**
Future work could examine update drift across model versions, intersectional demographic effects, and longer-run feedback effects in capital flows, as well as bias-mitigation strategies such as fairness-aware prompts, algorithmic adjustments to decision criteria, and counterfactual explanations.

**APA 7th Citation**
Wang, Y. (E.), & Gu, K. (2026). Who invests, who gets funded: Gender and racial bias in LLM-generated investment advice. *Journal of Business Ethics*. https://doi.org/10.1007/s10551-026-06251-6
