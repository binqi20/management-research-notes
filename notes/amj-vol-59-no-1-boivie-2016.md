---
id: amj-vol-59-no-1-boivie-2016
title: "Understanding the Direction, Magnitude, and Joint Effects of Reputation When Multiple Actors’ Reputations Collide"
authors:
  - "Boivie, Steven"
  - "Graffin, Scott D."
  - "Gentry, Richard J."
year: 2016
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2014.0521"
volume: 59
issue: 1
pages: "188-206"

source: "AMJ/vol-59-no-1"
pdf_path: "library/AMJ/vol-59-no-1/pdfs/Boivie 2016 Understanding the Direction, Magnitude, and Joint Effects of Reputation When Multiple Actors’ Reputations Collide.pdf"
text_path: "library/AMJ/vol-59-no-1/text/Boivie 2016 Understanding the Direction, Magnitude, and Joint Effects of Reputation When Multiple Actors’ Reputations Collide.txt"
ingested_at: "2026-07-03"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "gpt-6-astra"
augmented_at: "2026-09-06"

paper_type: "empirical-quantitative"
keywords: ["reputation", "analyst recommendations", "analyst reputation", "CEO reputation", "firm reputation", "cumulative abnormal returns"]
theory: ["reputation as collective social judgment", "attribute-specific and audience-specific reputation", "social evaluations"]
topics: ["governance-leadership", "ceo-leadership", "finance-accounting", "quantitative-methods"]
unit_of_analysis: "dyad"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Empirical quantitative event-study design using IBES analyst recommendation changes from 1996 to 2008. The study estimates OLS regressions of downgrade and upgrade cumulative abnormal returns, with robust standard errors clustered over firms and controls for analyst, firm, management, industry, year, and fiscal-quarter factors."
sample:
  industry: "U.S. publicly traded firms covered by IBES analyst recommendation data across global industry-classification-system sectors."
  country: "United States."
  time_period: "1996 to 2008."
  units: "Individual analyst recommendation-change events modeled as CEO-by-analyst dyads at covered firms."
  n: "36,878 recommendation-change observations: 19,512 downgrades and 17,358 upgrades."

evidence:
  sample_n: "Note: N 5 36,878."
  sample_country: "U.S.-specific sample"
  sample_industry: "global industry-classification-system sector"
  sample_time_period: "from 1996 to 2008"
  theories_overview: "both attribute specific and audience specific"
  methods_overview: "We used ordinary least squares (OLS) regression"
  keywords_source: "reputations of analysts, CEOs, and firms individually"
  hypotheses_source: "Hypothesis 1. Analyst reputation will amplify"
  measures_overview: "measure of CEO reputation (Star CEO) was a count"
  findings_overview: "5b is thus partially supported."
---

# Understanding the Direction, Magnitude, and Joint Effects of Reputation When Multiple Actors’ Reputations Collide

**Abstract**
Despite extensive research efforts into the effects of reputation, virtually all of it has examined the effect of one type of reputation on one or more specific outcomes. But, how, for example, might the reputations of analysts, CEOs, and firms individually and jointly affect firm outcomes? To answer this question, the present study focuses on a context in which reputations are particularly relevant: changes in analyst recommendations and the effect of those changes on stock market reactions. Our study contributes to the increasing reputation literature by being one of the first to recognize and measure how the market accounts for multiple reputations. Further, we argue and find that the reputations of different actors interact with each other when determining particular firm outcomes. We also find that different actor’s reputations influence the reactions of observers.

**Research Question**
The paper asks how the reputations of analysts, CEOs, and firms individually and jointly affect shareholder reactions to changes in analysts’ stock recommendations. It focuses on whether multiple actor reputations have distinct, relative, and interactive effects on the cumulative abnormal returns associated with recommendation upgrades and downgrades.

**Hypotheses / Propositions**
- H1: Analyst reputation will amplify the size of the CAR associated with a downgrade or an upgrade.
- H2: CEO reputation will diminish the size of the CAR associated with a downgrade or an upgrade.
- H3: Firm reputation will diminish the size of the CAR associated with a downgrade or an upgrade.
- H4: Analyst reputation will be more influential than CEO reputation, which will be more influential than firm reputation, on CARs associated with a downgrade or an upgrade.
- H5a: Following a downgrade, analyst reputation will moderate the effect of CEO reputation on the firm's CAR, reducing the positive impact of CEO reputation on the stock market reaction.
- H5b: Following an upgrade, analyst reputation will moderate the effect of CEO reputation on the firm's CAR, reducing the negative impact of CEO reputation on the stock market reaction.

**Mechanism Process**
- IV(s): Analyst reputation, CEO reputation, firm reputation, and the interaction between analyst reputation and CEO reputation.
- DV(s): Stock market reaction to analyst recommendation upgrades and downgrades, measured as cumulative abnormal returns around the recommendation-change event.
- Mediators: Not modeled as mediators.
- Moderators: Analyst reputation moderates the effect of CEO reputation on market reactions to both downgrades and upgrades.

The mechanism is that investors use reputation as social information under uncertainty, but they weight each reputation according to its attribute specificity and relevance to the audience’s expectations. Analyst reputation is built around forecast accuracy and is directly relevant to stock recommendations, so it amplifies market reactions to upgrades and downgrades. CEO reputation buffers recommendation changes when analysts are not stars, but star analyst reputation can dominate CEO reputation when the two reputations collide.

**Data & Measures**
The observational event study uses the IBES recommendation-detail file for 1996–2008 and restricts firms to December fiscal year ends. The unit is the individual CEO-by-analyst dyad at a recommendation-change event. Table 1 reports 36,878 observations for the descriptive dataset; Table 2 reports 19,512 downgrade observations and 17,358 upgrade observations for the separate regressions. Firm and industry data came from Compustat, stock prices and CARs from Eventus, CEO data from ExecuComp, and director information from RiskMetrics. Recommendations range from 1 (strong buy) to 5 (strong sell); the event is a change toward a less or more favorable recommendation.

The outcome is the market-model CAR over the event day and following day, a [0,1] window. Analyst reputation is an indicator for inclusion on any Institutional Investor analyst team that year. CEO reputation is the number of awards won from six business publications during the preceding five years; award collection begins in 1991. Firm reputation is an indicator for appearing on either of the paper's two corporate-reputation lists in the year before the recommendation change. The models include the analyst-reputation-by-CEO-reputation interaction and analyst, firm, management, industry, year, and fiscal-quarter controls. Separate downgrade and upgrade OLS regressions use robust standard errors clustered over firms; these observational estimates describe associations.

**Key Findings**
- H1 was supported: analyst reputation amplified both negative downgrade reactions and positive upgrade reactions. In Table 2, Models 2 and 5, the star-analyst coefficients were −1.08 and 1.08, respectively (both p < .01).
- H2 was supported: CEO reputation reduced the magnitude of both reactions. The CEO-award coefficient was positive for downgrade CARs (0.14, p < .01, Model 2) and negative for upgrade CARs (−0.07, p < .05, Model 5).
- H3 was not supported for either downgrades or upgrades. Firm reputation was not significant when analyst and CEO reputation were included; its negative upgrade coefficient was only marginally significant when considered without those reputations (−0.46, p < .10, Model 4).
- H4 was mostly supported. Standardized-coefficient comparisons showed analyst reputation was more influential than CEO reputation for downgrades (F = 27.28, p < .01) and upgrades (F = 37.51, p < .01). CEO reputation exceeded firm reputation for downgrades only at p < .10 (F = 3.43); their effect sizes did not differ significantly for upgrades.
- H5a was supported: the analyst-by-CEO interaction was negative for downgrades (−0.13, p < .05, Model 3). CEO reputation buffered downgrades by non-star analysts, but did not significantly offset downgrades by star analysts.
- H5b was partially supported: the upgrade interaction was positive but only marginally significant (0.09, p < .10, Model 6), consistent with analyst reputation reducing CEO reputation's dampening of the positive upgrade reaction.

**Theoretical Contribution**
The paper extends reputation research by shifting from single-actor reputation effects to simultaneous and joint effects among multiple reputations in one market context. It develops a framework in which the direction and magnitude of a reputation’s effect depend on attribute specificity and audience relevance. Empirically, it shows that analyst reputation has the strongest effect on shareholder reactions and can reduce the influence of CEO reputation, while firm reputation is less consistent in this setting.

**Practical Implication**
The findings imply that star analysts can move markets more strongly than non-star analysts when they issue recommendation changes. The authors suggest that markets may function more effectively if influential analysts are distributed more evenly across firm sizes and types. They also caution investors when reading analyst research about firms not led by star CEOs, because these firms appear to receive less analyst scrutiny.

**Limitations**
The authors identify the U.S.-specific sample as a limitation, noting that generalizability to other equity-market contexts is unclear. They also treat recommendation changes in isolation, even though clustered downgrades or upgrades may reinforce or damage CEO reputation nonlinearly. A further limitation is that reputations come from different certification sources, and the CAR models explain limited incremental variance despite practically meaningful valuation effects.

**Future Research**
Future research could examine how and when other types of reputation influence one another. The authors also suggest comparing reputational overlap in settings where the same body provides certification, such as relay CEO successions.

**APA 7th Citation**
Boivie, S., Graffin, S. D., & Gentry, R. J. (2016). Understanding the direction, magnitude, and joint effects of reputation when multiple actors’ reputations collide. *Academy of Management Journal*, 59(1), 188-206. https://doi.org/10.5465/amj.2014.0521
