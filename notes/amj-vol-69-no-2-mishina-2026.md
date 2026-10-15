---
id: amj-vol-69-no-2-mishina-2026
title: "Woulda, Shoulda, Coulda? The Impact of Predictive, Prescriptive, and Prospective Expectations on Stakeholder Reactions"
authors:
  - "Mishina, Y."
  - "Yu, M."
  - "Gomulya, D."
year: 2026
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2024.0135"
volume: 69
issue: 2
pages: "275-298"
source: "AMJ/vol-69-no-2"
pdf_path: "library/AMJ/vol-69-no-2/pdfs/Mishina 2025 Woulda, Shoulda, Coulda The Impact of Predictive, Prescriptive, and Prospective Expectations on Stakeholder Reactions.pdf"
text_path: "library/AMJ/vol-69-no-2/text/Mishina 2025 Woulda, Shoulda, Coulda The Impact of Predictive, Prescriptive, and Prospective Expectations on Stakeholder Reactions.txt"
ingested_at: "2026-10-14"
extraction_model: "gpt-6-astra"
extraction_version: "v3"
paper_type: "empirical-quantitative"
keywords: ["predictive expectations", "prescriptive expectations", "prospective expectations", "heuristics", "earnings surprises"]
theory: ["expectancy violation theory"]
topics: ["asset-pricing", "behavioral-economics"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Archival firm-quarter panel; earnings-announcement event study and random-effects regressions with robust standard errors; robustness and post hoc analyses."
sample:
  industry: "Multiple industries, classified by two-digit SIC codes"
  country: "United States"
  time_period: "2013–2019"
  units: "Firm-quarters of S&P 500 firms with December 31 fiscal year ends"
  n: "4,752 firm-quarters"
evidence:
  sample_n: "our final sample comprises 4,752"
  sample_country: "U.S. equities"
  sample_industry: "using the first two digits of the Standard Industrial"
  sample_time_period: "firms from 2013 to 2019."
  theories_overview: "expectancy violation theory (EVT)"
  methods_overview: "random effects models in our analyses"
  keywords_source: "predictive and prescriptive expectations"
  hypotheses_source: "Hypothesis 1. When the current earnings surprise"
  measures_overview: "divided by the Q value at the beginning."
  findings_overview: "The results similarly supported Hypothesis 2."
---

# Woulda, Shoulda, Coulda? The Impact of Predictive, Prescriptive, and Prospective Expectations on Stakeholder Reactions

**Abstract**
When and why might stakeholders react to firm activities in ways that might be different than, or even contradictory to, what we might expect based on the extant research? We draw on expectancy violation theory (EVT) and bring in the notion of heuristics and future-oriented expectations to examine this question, using a sample of investor reactions to earnings surprises from 2013 to 2019. We find that, in addition to comparing earnings to consensus earnings estimates, investors appear to compare the earnings surprises to the firm’s past performance and to its peers. Importantly, their expectations regarding future interactions with the firm appear to shape their decisions and generate anticipatory reactions despite a lack of full certainty about the future—a point notably absent from the EVT literature so far, which has tended to be reactive. Numerous robustness checks and post hoc analyses indicate that this behavior is driven not necessarily by unsophisticated investors, as initially predicted, but seemingly by institutional investors who rely on these multiple expectations, even though that may not be entirely rational. Our theorizing and findings make several contributions to the EVT literature, and offer practical insights for managers and investors.

**Research Question**
When and why do stakeholders react to firm activities differently from what existing expectancy violation theory predicts? How do predictive, prescriptive, and prospective expectations jointly inform investor reactions to earnings announcements?

**Hypotheses / Propositions**
- Baseline: Investors use consensus earnings estimates as predictive expectations, reacting more positively (negatively) when earnings exceed (fall below) them than when earnings meet them.
- H1: Investors react more negatively when the current earnings surprise falls short of the prescriptive expectation based on past performance than when it meets or exceeds that expectation.
- H2: Investors react more negatively when the current earnings surprise falls short of the prescriptive expectation based on peer comparison than when it meets or exceeds that expectation.
- H3: Investors react more negatively to a negative prospective expectancy violation—believing future earnings will be lower—than to unchanged or positively revised prospective expectations.

**Mechanism Process**
- IVs: Predictive expectancy violations; prescriptive expectancy violations based on past performance and peer comparison; prospective expectancy violations.
- DV: Investor reactions to earnings announcements.
- Mediators: Not reported in paper.
- Moderators: Post hoc tests examine estimate dispersion, institutional investor ownership, and institutional investors’ average portfolio size.

Predictive expectations concern what a firm would do; prescriptive expectations concern what it should do. Investors may use earnings surprises as a common metric and compare them with prior surprises and industry peers through simplifying heuristics. Prospective expectations concern the current expected value of future interactions: updating them can prompt anticipatory reactions, whereas a violation attributed to one-time factors need not change them. These are proposed cognitive mechanisms, not directly observed individual cognitions.

**Data & Measures**
The archival sample contains 4,752 firm-quarters of S&P 500 firms during 2013–2019, restricted to December 31 fiscal year ends. I/B/E/S analyst EPS forecasts made within five days of the announcement were excluded; the closest remaining forecast per analyst was retained, firm-quarters needed at least five estimates, and estimates were winsorized at the 1st and 99th percentiles before firm-level aggregation. Data were combined with EVENTUS, CRSP, Compustat, Audit Analytics, and Thomson Reuters Institutional (13F) Holdings; observations with missing values were excluded.

Investor reactions are three-day CARs over days [-1, +1], calculated using the Fama–French plus momentum model with an estimation window from 255 to 46 days before the announcement. Actual EPS and mean forecasts are rounded to two decimals before calculating earnings surprise = (actual earnings − average earnings estimate) / average earnings estimate. Separate predictive-violation splines retain the magnitude of material positive or negative surprises, defined by the top quartiles of each within industry-year-quarter; nonmaterial surprises are zero. Industries use two-digit SIC codes. The past-performance prescriptive indicator equals one when the current surprise is below the previous quarter’s surprise; the peer indicator equals one when it is below the current industry average surprise excluding the focal firm, and zero otherwise.

Prospective violation is proxied by the percentage change in Tobin’s Q over days [-7, -1]: subtract beginning Q from ending Q and divide by beginning Q. Q equals the sum of common stock, preferred stock, long-term debt, and short-term debt maturing within a year, divided by total assets. Controls include prior-quarter ROA, high reputation, institutional ownership, managerial guidance, analyst coverage, estimate dispersion, and financial restatements. Random-effects regressions with robust standard errors assess associations; individual expectations are not directly measured. For the post hoc portfolio-size test, the authors count firms held by each institutional investor each quarter, average those counts across the focal firm’s institutional investors, then log-transform the average before forming interactions.

**Key Findings**
- Baseline: Material positive surprises are positively associated with CAR in Model 2 (p < .01) and Model 6 (p < .05). The negative-surprise association is significant in Model 2 (p < .05), but not in the full Model 6 (p = .16). Thus, the authors’ summary that all hypotheses receive support requires this qualification for the negative baseline component.
- H1 and H2 are supported: Both negative prescriptive-violation indicators have b = −0.02, p < .001 in their separate and full models. The full-model CAR differences are −1.77 percentage points for falling below the previous quarter’s surprise and −1.64 percentage points for falling below industry peers. Coefficients are reported rounded to two decimals; the authors calculate effect sizes from unrounded values.
- H3 is supported: Positive changes in Q are associated with more positive CAR (Model 5: b = 0.21; Model 6: b = 0.20; both p < .001); a one-standard-deviation increase corresponds to 0.51 percentage points higher CAR in Model 6. Robustness checks are largely consistent, but the P–E percentage-change alternative (4,266 observations) is only marginal in the stepwise model (b = 0.05, p < .10; full model p < .05), and absolute P–E change is nonsignificant.
- Post hoc estimate-dispersion and institutional-ownership interactions with the prescriptive indicators are nonsignificant. Negative prescriptive associations appear in both the early [-1, 0] and later [+1, +3] reaction windows used as proxies for sophisticated and unsophisticated investors. Larger average institutional-investor portfolios strengthen the negative peer-comparison association (interaction b = −0.02, p < .01), consistent with an attention-constraint interpretation.
- Replacing surprise comparisons with actual-earnings comparisons preserves the past-performance association (b = −0.01, p < .001), while the peer association is marginal in the stepwise model and nonsignificant in the full model. Neither prescriptive indicator significantly predicts subsequent earnings; only the past-performance indicator predicts subsequent earnings surprises (b = 0.08, p < .05), in a direction inconsistent with the negative contemporaneous reaction. The authors interpret these patterns as suggesting semi-rational or irrational heuristic use.

**Theoretical Contribution**
The paper extends expectancy violation theory by introducing prospective expectations and anticipatory reactions alongside reactive responses to predictive and prescriptive violations. It distinguishes multiple expectations that can impose separate evaluative hurdles, and suggests that earnings-surprise heuristics permit comparison and economize on attention even among sophisticated institutional investors.

**Practical Implication**
For managers, meeting analyst estimates may still leave past-performance, peer-comparison, and prospective expectations unsatisfied; satisfying multiple expectations can also raise subsequent hurdles. For investors, the authors suggest that anticipating heuristic-driven reactions may offer trading opportunities, while warning that these opportunities may disappear as market behavior adjusts.

**Limitations**
The earnings-announcement setting and large, well-known S&P 500 firms limit generalization to very different activities and less familiar firms. The study examines only selected expectations and a general form of prospective expectations; other expectations may combine differently. Archival data do not reveal individual investor cognitions directly or separate cognitions and emotions from reactions.

**Future Research**
The authors propose studying other activities, stakeholders, and less well-known firms, as well as when multiple expectations align, conflict, are nested, or receive different weights. They call for examining how expected interaction frequency, future behavior, and evaluative criteria change prospective expectations, and when heuristics are useful or damaging and how they are updated. Policy-capturing studies and qualitative evidence could investigate expectations, violations, and subsequent behavior more directly.

**APA 7th Citation**
Mishina, Y., Yu, M., & Gomulya, D. (2026). Woulda, shoulda, coulda? The impact of predictive, prescriptive, and prospective expectations on stakeholder reactions. *Academy of Management Journal, 69*(2), 275–298. https://doi.org/10.5465/amj.2024.0135
