---
id: amj-vol-67-no-1-cao-2024
title: "Performance Shortfalls, Response Directions, and Belief in the Effectiveness of Responses"
authors:
  - "Cao, Zhi"
  - "Jiang, Feifei"
  - "Wang, Donghan"
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.0241"
volume: 67
issue: 1
pages: "178-207"

source: "AMJ/vol-67-no-1"
pdf_path: "library/AMJ/vol-67-no-1/pdfs/Cao 2024 Performance Shortfalls, Response Directions, and Belief in the Effectiveness of Responses.pdf"
text_path: "library/AMJ/vol-67-no-1/text/Cao 2024 Performance Shortfalls, Response Directions, and Belief in the Effectiveness of Responses.txt"
ingested_at: "2026-05-12"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-14"

paper_type: "empirical-quantitative"
keywords:
  - "problemistic search"
  - "performance shortfalls"
  - "shared belief"
  - "R&D intensity"
  - "donation intensity"
  - "corporate social responsibility"
  - "behavioral theory of the firm"
theory:
  - "behavioral theory of the firm (Cyert & March, 1963)"
  - "problemistic search / decision rules (Greve, 2003a; Posen et al., 2018)"
  - "managerial and social cognition (March & Simon, 1958; Fiske & Taylor, 2021)"
topics:
  - "strategy-innovation"
  - "corporate-social-responsibility"
  - "behavioral-theory-of-the-firm"
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Firm-level fixed-effects panel regressions on an unbalanced firm-year panel of publicly listed Chinese firms (2009–2018); independent, moderating, and control variables lagged one year; standard errors clustered at the firm level; shared-belief variables constructed from MD&A documents via a causal-mapping NLP approach (sentence-count of R&D–performance and CSR–performance causal statements); evidence-of-belief measured as three-year rolling correlations between R&D/CSR and ROA based on the firm's own history and on a five-firm matched peer group; Granger causality and AR(1) (xtregar) robustness checks."
sample:
  industry: "Publicly listed firms in China, excluding financial firms and specially treated (ST) firms; further excluding industries (e.g., real estate, residential services) where most firms do not invest substantially in R&D"
  country: "China"
  time_period: "2009–2018"
  units: "firm-year"
  n: "Unbalanced panel; analytic samples of 12,837 firm-years for R&D-intensity models and 11,495 firm-years for donation-intensity models"

evidence:
  sample_n: "n                                               12837                  12837                  12837               11818               12697"
  sample_country: "2009–2018 data collected from publicly listed Chinese"
  sample_industry: "financial and CSR data from publicly listed"
  sample_time_period: "Our sample consists of data pertaining to publicly"
  theories_overview: "behavioral theory of the firm (BTOF) (Cyert & March,"
  methods_overview: "fixed-effects panel estimation"
  keywords_source: "Problemistic search literature has long"
  hypotheses_source: "effectiveness of R&D negatively moderates the relationship between performance shortfalls and philanthropic donation intensity"
  measures_overview: "we measured R&D intensity as the ratio of"
  findings_overview: "relationship between performance shortfalls and R&D intensity strengthens"
---

# Performance Shortfalls, Response Directions, and Belief in the Effectiveness of Responses

**Abstract**
Problemistic search literature has long sought to understand which responses firms adopt when addressing performance shortfalls. Studies have typically considered certain responses and focused on established decision rules to examine search directions, thereby, implicitly assuming that all responses considered are workable solutions to performance shortfalls. Conversely, we argue that variations in decision-makers' beliefs about the effectiveness of particular responses in improving firm performance play an important role. These beliefs, alongside evidence supporting them, determine which specific responses firms adopt. To test this argument, we focus on two types of search solutions represented by research and development (R&D) intensity and philanthropic donation intensity. Based on 2009–2018 data collected from publicly listed Chinese firms, we find that, when decision-makers agree on the effectiveness of R&D, the positive relationship between performance shortfalls and R&D intensity strengthens; whereas when they agree on the effectiveness of corporate social responsibility (CSR), the negative relationship between performance shortfalls and donation intensity weakens. The effects of shared beliefs on the effectiveness of R&D and CSR are stronger when they are supported by relevant evidence—that is, when there is a stronger correlation between R&D or CSR on the one hand and firm performance on the other.

**Research Question**
Which specific responses do firms adopt when addressing performance shortfalls, once we relax the implicit assumption that all considered responses are equally workable, and how do decision-makers' shared beliefs in the effectiveness of those responses—and the evidence supporting those beliefs—shape the direction of problemistic search?

**Hypotheses / Propositions**
The paper develops three propositions and derives six testable hypotheses (an R&D and a CSR variant of each), reporting the predicted sign for each.
Proposition 1. Shared belief in the effectiveness of a particular response positively moderates the relationship between performance shortfalls and the intensity of that response.
Proposition 2. Shared belief in the effectiveness of a particular response negatively moderates the relationship between performance shortfalls and the intensity of other responses.
Proposition 3. Shared belief and the evidence supporting it jointly shape the shortfall–response-intensity relationship, which is strongest when the shared belief is supported by strong evidence.
H1a. Decision-makers' shared belief in the effectiveness of R&D positively moderates the relationship between performance shortfalls and R&D intensity.
H1b. Decision-makers' shared belief in the effectiveness of CSR positively moderates the relationship between performance shortfalls and philanthropic donation intensity.
H2a. Decision-makers' shared belief in the effectiveness of R&D negatively moderates the relationship between performance shortfalls and philanthropic donation intensity.
H2b. Decision-makers' shared belief in the effectiveness of CSR negatively moderates the relationship between performance shortfalls and R&D intensity.
H3a. In the presence of strong R&D–performance correlations, the relationship between performance shortfalls and R&D intensity is stronger in firms with a stronger shared belief in the effectiveness of R&D.
H3b. In the presence of strong CSR–performance correlations, the relationship between performance shortfalls and philanthropic donation intensity is stronger in firms with a stronger shared belief in the effectiveness of CSR.

**Mechanism Process**
- IV(s): Performance shortfalls, operationalized as the absolute value of (ROA – Aspiration Level) when ROA is at or below aspirations (weighted blend of historical and social aspirations following Kuusela et al., 2017)
- DV(s): R&D intensity (R&D expenditures / sales) and philanthropic donation intensity (philanthropic expenses / sales, rescaled ×100)
- Mediators: None modeled
- Moderators: Shared belief in the effectiveness of R&D and shared belief in the effectiveness of CSR (sentence-count of causal statements linking R&D/CSR to performance in firm MD&A documents, identified via a causal-mapping plus NLP procedure); evidence of those beliefs, measured as three-year rolling R&D–performance and CSR–performance correlations based on the firm's own history ("hist.") and on a matched five-firm industry peer group ("soc."); two- and three-way interactions of shortfalls with shared beliefs and evidence

When a firm falls below its aspiration level, decision-makers do not simply apply a single decision rule (proximity, time-horizon, risk-taking) to a set of equally workable responses; rather, they assess whether a particular response is believed to improve performance. A dominant shared belief in R&D effectiveness steepens the positive performance-shortfall–R&D-intensity slope, while a dominant shared belief in CSR effectiveness flattens the otherwise negative performance-shortfall–donation-intensity slope. These shared-belief effects are strongest when accompanied by supportive correlational evidence linking the response to firm performance, because such evidence persuades non-supporters and consolidates the dominant belief. The process thus combines behavioral search with a social-cognitive mechanism in which action–outcome linkages, not just abstract response characteristics, direct search.

**Data & Measures**
- Data: unbalanced firm-year panel of publicly listed Chinese firms, 2009–2018 (financial firms and specially treated firms excluded), assembled from the China Stock Market and Accounting Research (CSMAR) database (firm and board data), Rankins CSR Ratings (RKS, CSR–performance data), management discussion and analysis (MD&A) filings from cninfo.com.cn (shared-belief text), and the China Statistical Yearbook (province variables).
- IV — Performance shortfalls: absolute value of (ROA − aspiration level) when ROA is at or below aspirations, else zero; aspiration level is a weighted blend of historical and social aspirations (weights a1 = 0.70, a2 = 0.75 from a grid search; social aspiration = average ROA of a five-firm, Mahalanobis-matched industry peer group).
- DVs — R&D intensity = R&D expenditures / sales; philanthropic donation intensity = philanthropic expenses / sales, rescaled ×100.
- Firm performance — return on assets (ROA) = net income / total assets.
- Moderators (shared belief) — logged sentence-count of causal statements linking R&D (CSR) to performance in each MD&A document, identified via a causal-mapping procedure plus an NLP/heuristic classifier.
- Moderators (evidence of belief) — three-year rolling correlations between R&D (CSR) and next-year ROA, computed from the firm's own history ("hist.") and from the matched peer group ("soc.").
- Controls: board-level (CEO duality, board size, independent/returnee/female director proportions, average age, R&D and CSR experience), firm-level (performance above aspirations, absorbed and unabsorbed slack, firm size, state ownership, debt ratio), province GDP per capita, and year dummies.
- Estimation: firm-level fixed-effects panel regressions with standard errors clustered by firm; independent, moderating, and control variables lagged one year to reduce reverse causality. The design is associational (two- and three-way moderation/interaction tests), supported by Granger-causality, Heckman-selection, confounding-impact-threshold, and AR(1) xtregar robustness checks rather than a causal-identification strategy.

**Key Findings**
- H1a supported: shared belief in R&D positively and significantly moderates the performance-shortfall–R&D-intensity relationship (interaction b = 0.033, p = .046); the marginal effect of shortfalls on R&D intensity is larger under strong belief (0.060, p < .001) than weak belief (0.018, p = .269), so the positive relationship strengthens.
- H1b partial support: the shortfall × shared-belief-in-CSR interaction on donation intensity is positive but only marginally significant (b = 0.296, p = .077); the negative shortfall–donation relationship weakens (effectively disappears) when belief in CSR is strong. The authors flag this as partial support (significant only when controlling for the direct effect of shared belief in R&D), and the word-count robustness measure did not support H1b.
- H2a supported: shared belief in R&D negatively and significantly moderates the shortfall–donation-intensity relationship (b = −0.214, p = .004).
- H2b not supported: shared belief in CSR does not significantly moderate the shortfall–R&D-intensity relationship (b = 0.002, p = .957).
- H3a supported: the three-way interaction (shortfalls × shared belief in R&D × R&D–performance correlation) is positive and significant for both historical (b = 0.061, p = .017) and peer-based/social (b = 0.130, p = .004) correlations; the positive shortfall–R&D relationship is strongest when strong belief is backed by strong evidence.
- H3b partially supported: the three-way interaction is positive and significant for historical CSR–performance correlations (b = 0.850, p = .036) but nonsignificant for social correlations (b = 0.233, p = .669) — supported for historical evidence only.
- Baseline direction: on average, performance shortfalls relate positively to R&D intensity but negatively to donation intensity; Granger tests indicate performance shortfalls Granger-cause R&D and donation intensity, but not the reverse.

**Theoretical Contribution**
The paper extends the behavioral theory of the firm by introducing decision-makers' shared beliefs in the effectiveness of specific responses as a determinant of problemistic search directions, complementing the established decision-rule approach that focuses on abstract response characteristics. It enriches managerial-cognition research in strategy by showing that supportive evidence (here, response–performance correlations) can substitute for political maneuvering or power-based coalition-building in producing a dominant shared belief among decision-maker subgroups. It also contributes a behavioral perspective to the CSR literature by explaining when firms expand or contract philanthropic donation intensity in response to performance shortfalls.

**Practical Implication**
Top management teams that wish to redirect search toward a particular response after a performance shortfall (for example, increasing R&D or sustaining CSR investments such as philanthropic donations) should invest in building and documenting a shared belief in that response's effectiveness, ideally supported by concrete correlational evidence linking the response to firm performance. Presenting strong evidence can persuade dissenting subgroups without resorting to power plays or ally-building, and is reflected in the firm's communicative artifacts such as MD&A narratives.

**Limitations**
The study examines only two responses (R&D and philanthropic donations), so generalization to other market and non-market responses requires further work. Data constraints prevented direct observation of the micro-level process by which shared beliefs are formed and how evidence persuades doubters. Reliance on publicly listed Chinese firms means the findings reflect a distinct institutional environment whose national culture and formal institutions may bound generalizability to other contexts.

**Future Research**
Future work should extend the shared-belief framework to additional response types beyond R&D and philanthropic donations, including other market and non-market actions. It should also open up the micro-process by which subgroups of decision-makers with diverging beliefs interact, marshal evidence, and converge on a dominant shared belief. Comparative studies in non-Chinese institutional environments would clarify how the effects of shared beliefs and supporting evidence on problemistic search vary across contexts.

**APA 7th Citation**
Cao, Z., Jiang, F., & Wang, D. (2024). Performance shortfalls, response directions, and belief in the effectiveness of responses. *Academy of Management Journal*, 67(1), 178–207. https://doi.org/10.5465/amj.2021.0241
