---
id: amj-vol-66-no-2-lee-2023
title: "The Role of Attribution in Learning from Performance Feedback: Behavioral Perspective on the Choice between Alliances and Acquisitions"
authors:
  - "Lee, Jaemin"
  - "Lee, Joon Mahn"
  - "Kim, Ji-Yub (Jay)"
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2019.1293"
volume: 66
issue: 2
pages: "578-603"

source: "AMJ/vol-66-no-2"
pdf_path: "library/AMJ/vol-66-no-2/pdfs/Lee 2023 The Role of Attribution in Learning from Performance Feedback Behavioral Perspective on the Choice between Alliances and Acquisitions.pdf"
text_path: "library/AMJ/vol-66-no-2/text/Lee 2023 The Role of Attribution in Learning from Performance Feedback Behavioral Perspective on the Choice between Alliances and Acquisitions.txt"
ingested_at: "2026-05-23"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-quantitative"
keywords: ["performance feedback", "attribution", "self-serving attribution", "alliances", "acquisitions", "governance mode choice", "aspiration level", "diffusion of responsibility"]
theory: ["performance feedback theory / behavioral theory of the firm (Cyert & March, 1963; Greve, 2003b)", "attribution theory (Weiner, 1979, 1986; Sedikides & Alicke, 2012)", "self-serving attribution (Mezulis et al., 2004; Shepperd et al., 2008)"]
topics: ["mergers-acquisitions", "behavioral-theory-of-the-firm", "attribution-theory", "north-america"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Event-history (survival) analysis estimating the hazard rate of a firm switching from an alliance to an acquisition, using a Cox model with firm fixed effects and standard errors clustered on firms; alliance performance measured by cumulative abnormal returns (CAR) relative to a social aspiration level via a spline; robustness via linear probability, conditional logit/multinomial logit, alternative aspiration levels, and alternative samples."
sample:
  industry: "Cross-industry; equity alliances/joint ventures and acquisitions by large U.S. corporations (SDC Joint Ventures and Alliances and Mergers and Acquisitions databases; COMPUSTAT/CRSP)"
  country: "United States (Fortune 500 firms)"
  time_period: "1994–2017 (with 1989–1993 used to measure prior experience)"
  units: "Firm-quarter observations (firms whose most recent transaction was an alliance, at risk of switching to an acquisition)"
  n: "13,535 firm-quarter observations (39,570 before filtering); 4,017 alliance-to-acquisition switches; models estimated on n = 26,005"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "sample of 13,535 firm-quarter observations; 4,017"
  sample_country: "completed by Fortune 500 firms"
  sample_industry: "Our sample consists of acquisitions and alliances"
  sample_time_period: "between 1994 and 2017"
  theories_overview: "we develop a theory of attribution in learning from performance feedback by integrating attribution and performance feedback theory."
  methods_overview: "were estimated using the Cox"
  keywords_source: "cognitive biases, such as self"
  hypotheses_source: "Hypothesis 2a. When alliance performance is below the aspiration level, the more experienced the alli"
  measures_overview: "Number of alliance partners. Alliance partner number represents the total number of partners that"
  findings_overview: "in the number of partners in an alliance decreased the likelihood that a firm would turn to an acquisi"
---

# The Role of Attribution in Learning from Performance Feedback: Behavioral Perspective on the Choice between Alliances and Acquisitions

**Abstract**
The causal attribution of performance has not been explicitly considered in the performance feedback literature, despite its potential value in learning from prior performance. In this study, we develop a theory concerning the attribution in learning from performance feedback and explore how the attribution of past alliance performance can influence a firm's choice between future acquisitions and alliances. We also examine the mechanisms by which attribution manifests by exploring how three theoretical factors, known to influence attribution, can moderate the relationship—the diffusion of responsibility, the perceived capability of partners, and the ambiguity of performance information. We find strong evidence supporting our predictions. This study contributes to the performance feedback literature by integrating attribution with performance feedback theory. It also extends research on corporate strategy by providing a behavioral account of the choice between acquisitions and alliances.

**Research Question**
How does the causal attribution of past alliance performance influence a firm's subsequent choice between acquisitions and alliances, and how do three attribution-relevant factors—the diffusion of responsibility, the perceived capability of partners, and the ambiguity of performance information—moderate the effect of alliance performance feedback on that choice?

**Hypotheses / Propositions**
- Baseline Hypothesis 1a. When a firm's alliance performance is below its aspiration level for alliances, the lower the alliance performance, the more likely the firm will subsequently make an acquisition (predicted sign on ALL < ASP: negative).
- Baseline Hypothesis 1b. When a firm's alliance performance is above its aspiration level for alliances, the higher the alliance performance, the less likely the firm will subsequently make an acquisition (predicted sign on ALL > ASP: negative).
- Hypothesis 1a. When alliance performance is below the aspiration level, the larger the number of alliance partners, the less likely a decrease in alliance performance will increase the likelihood of subsequently making an acquisition (predicted interaction sign: positive).
- Hypothesis 1b. When alliance performance is above the aspiration level, the larger the number of alliance partners, the less likely an increase in alliance performance will decrease the likelihood of subsequently making an acquisition (predicted interaction sign: positive).
- Hypothesis 2a. When alliance performance is below the aspiration level, the more experienced the alliance partner(s) with alliances, the more likely a decrease in alliance performance will increase the likelihood of subsequently making an acquisition (predicted interaction sign: negative).
- Hypothesis 2b. When alliance performance is above the aspiration level, the more experienced the alliance partner(s) is with alliances, the less likely an increase in alliance performance will decrease the likelihood of subsequently making an acquisition (predicted interaction sign: positive).
- Hypothesis 3a. When alliance performance is below the aspiration level, the higher the variability in alliance performance, the less likely a decrease in alliance performance will increase the likelihood of subsequently making an acquisition (predicted interaction sign: positive).
- Hypothesis 3b. When alliance performance is above the aspiration level, the higher the variability in alliance performance, the more likely an increase in alliance performance will decrease the likelihood of subsequently making an acquisition (predicted interaction sign: negative).
- The paper also states an explicit asymmetry expectation: the number of alliance partners is predicted to increase self-serving bias when alliance performance is below the aspiration level but to decrease it when performance is above the aspiration level, whereas partner alliance experience and alliance performance variability are predicted to produce symmetrical effects for success and failure.

**Mechanism Process**
- IV(s): Alliance performance relative to the social aspiration level, split into performance below aspiration (ALL < ASP) and above aspiration (ALL > ASP), measured by cumulative abnormal returns (CAR).
- DV(s): Likelihood (hazard rate) of a firm switching from an alliance to a subsequent acquisition.
- Mediators: None tested directly; self-serving attribution is the theorized but unobserved cognitive process, inferred through the moderators.
- Moderators: Number of alliance partners (diffusion of responsibility); partner alliance experience (perceived capability of partners); alliance performance variability (ambiguity of performance information).

The paper integrates attribution theory into the four-step performance feedback process (evaluation, attribution, search, change). Because managers make self-serving attributions, poor alliance performance attributed to external causes "may not deter managers from making alliances again, nor encourage them in searching for an alternative to alliances to the same degree as when attributed to internal causes," weakening the baseline below-aspiration prediction; conversely, crediting themselves for successful alliances leads managers to believe they will succeed again, which decreases their search for alternatives and reinforces the baseline above-aspiration prediction that stronger performance makes a subsequent acquisition less likely. The three moderators shift how strongly self-serving attribution manifests: more partners and higher performance variability amplify external attribution of failure (weakening the push toward acquisitions), while highly capable partners make blaming them less credible (strengthening the push toward acquisitions after failure).

**Data & Measures**
- Data sources: firms listed on the 1994 Fortune 500 list; their alliances (including alliances made by their subsidiaries, because alliance and acquisition decisions are typically made by headquarters) from the SDC Joint Ventures and Alliances database, and their acquisitions from the SDC Mergers and Acquisitions database, for deals announced and completed between 1994 and 2017. The 1989-1993 window supplies prior alliance and acquisition experience, and the study period starts in 1994 because SDC is known to be unreliable prior to 1989. Duplicate deal entries were eliminated and announcement dates were verified against major business news outlets such as Financial Times and Bloomberg News; SDC and news dates matched for about 77% of alliances, and news dates took precedence where they disagreed. Main analyses include only equity alliances and joint ventures, excluding nonequity forms such as licensing and manufacturing arrangements, marketing agreements, and research collaborations. Quarterly demographic and financial data on sample firms and alliance partners come from the COMPUSTAT/CRSP merged database.
- DV: the unobserved hazard rate for a firm that used an alliance at t to change to an acquisition at t+1, coded 1 if the first event the firm made at t+1 was an acquisition and 0 otherwise; the estimation sample is restricted to firm-quarter observations in which the firm's most recent transaction was an alliance (so the firm is at risk of switching governance mode).
- IV (alliance performance): cumulative abnormal returns (CAR) around the alliance announcement, measured over a [-1, +1] event window, with normal returns from the market model estimated on the CRSP value-weighted index over a 100-day period ending 10 days before the event. CAR was chosen because stock market reaction is regarded as salient performance feedback by managers and because its short window avoids the confounding that accounting measures suffer.
- IV (performance feedback): alliance performance relative to a social aspiration level, measured as the average CAR of every alliance made by all other firms (not only Fortune 500 firms) in the same industry, defined by the 2-digit SIC code of the firm's primary industry, during the year prior to the focal alliance. A spline splits performance into ALL < ASP (focal CAR minus the aspiration level when CAR falls below it, 0 otherwise) and ALL > ASP (focal CAR minus the aspiration level when CAR exceeds it, 0 otherwise). Where a firm made more than one alliance in a quarter, the last alliance's performance was used. The social aspiration specification was chosen partly because it gave the best model fit relative to historical and weighted aspiration levels.
- Moderator (diffusion of responsibility): alliance partner number, the total number of partners that participated in the focal alliance.
- Moderator (perceived capability of partners): partner alliance experience, the average of the total number of alliances completed by each partner during the five-year period prior to the focal alliance.
- Moderator (ambiguity of performance information): alliance performance variability, the standard deviation of the performance of all the alliances the firm made during the five-year period prior to the focal alliance.
- Controls (Table 3): alliance experience and acquisition experience (numbers of prior alliances and acquisitions completed in the previous five years), alliance performance variability and acquisition performance variability, partners' alliance experience, alliance partner number, firm performance (return on equity), divestiture experience (number of divestitures completed in the previous five years), financial slack (equity-to-debt ratio), unabsorbed slack (working capital to total sales), absorbed slack (selling, general, and administrative expenses to sales), diversification (number of different SIC codes reported), average past acquisition performance (average CAR of all acquisitions the firm made in the previous five years), partner firm performance (average return on equity of the alliance partners in the focal firm's alliances over the previous five years), and industry alliance density and industry acquisition density (numbers of alliances and acquisitions in the focal firm's industry over the previous five years).
- Estimation and identification: hazard rates were estimated with the Cox model, with firm identifiers included to control for potential heterogeneity and robust standard errors clustered on firms; Table 3 reports n = 26,005 and states that all models include firm fixed effects. The design is associational, not quasi-experimental: the paper names no instrumental-variable, difference-in-differences, regression-discontinuity, natural-experiment, or randomized strategy, and instead supports inference through a comprehensive control set, firm-level heterogeneity controls, a Schoenfeld-residuals test that found no violation of the proportional-hazards assumption, and a discussion of sample-induced endogeneity (all sample firms made both alliances and acquisitions during the study period). Multicollinearity was assessed via variance inflation factors, the highest being 3.7.

**Key Findings**
- Both baseline hypotheses were supported. The coefficients on ALL < ASP and ALL > ASP are negative and statistically significant in Models 2-5 (Model 2: ALL < ASP = -.055; ALL > ASP = -.094), so alliance performance further below the aspiration level raised, and performance further above it lowered, the hazard of subsequently making an acquisition. Model 2 implies that a decrease in alliance performance below aspiration of one dollar per share increases the likelihood of subsequently making an acquisition by 5.35%.
- Hypothesis 1a supported: the interaction of ALL < ASP with alliance partner number is positive and statistically significant (.008, Model 3), so a larger number of partners weakened the push from alliance failure toward acquisition.
- Hypothesis 1b supported: the interaction of ALL > ASP with alliance partner number is positive and statistically significant (.012, Model 3), so a larger number of partners weakened the extent to which alliance success deterred acquisition. Table 4, Panel A shows the marginal effects of both ALL < ASP and ALL > ASP are smallest at the high level of alliance partner number.
- Hypothesis 2a supported: the interaction of ALL < ASP with partner alliance experience is negative and statistically significant (-.003, Model 4), so more experienced (more capable) partners strengthened the push from alliance failure toward acquisition.
- Hypothesis 2b supported: the interaction of ALL > ASP with partner alliance experience is positive and statistically significant (.003, Model 4), so more experienced partners weakened the extent to which alliance success deterred acquisition. Table 4, Panel B shows the marginal effect of ALL < ASP is greatest, and that of ALL > ASP smallest, at the high level of partners' alliance experience.
- Hypothesis 3a supported: the interaction of ALL < ASP with alliance performance variability is positive and statistically significant (.253, Model 5), so more variable prior alliance performance weakened the push from alliance failure toward acquisition.
- Hypothesis 3b supported: the interaction of ALL > ASP with alliance performance variability is negative and statistically significant (-.433, Model 5), so more variable prior alliance performance amplified the negative relationship between above-aspiration performance and subsequent acquisition. Table 4, Panel C shows the marginal effect of ALL < ASP is smallest, and that of ALL > ASP greatest, at the high level of variability.
- Reported effect magnitudes from the interaction plots: below the aspiration level, a decrease in alliance performance from the mean to two standard deviations below the mean increased the multiplier of the hazard rate of making an acquisition by 24.65% at a low alliance partner number but by only 0.003% at a high one; above the aspiration level, an increase of two standard deviations decreased the multiplier by 48.60% at a low partner number versus 11.26% at a high one. For partner alliance experience, the same below-aspiration decrease produced a 50.11% increase in the hazard multiplier at a high level of partner alliance experience versus only 5.69% at a low level.
- The authors summarize the moderator results as follows: a larger number of alliance partners decreased the likelihood that a firm would turn to an acquisition when the alliance failed, but a successful alliance was more likely to prompt a change to an acquisition as the number of partners increased; firms were more likely to turn to an acquisition after a failed alliance when partners were experienced (perceived as highly capable) than when they were inexperienced, while a successful alliance was less likely to trigger a change to an acquisition when partners were inexperienced than when they were experienced; and highly variable past alliance performance made firms less likely to switch to an acquisition after both failed and successful alliances.
- The authors caution that the kinked baseline curve on its own - the coefficient on ALL > ASP being significantly smaller (more negative) than that on ALL < ASP - cannot be taken as evidence of self-serving attribution, because other behavioral processes such as organizational inertia or threat rigidity could produce similar results; the three moderator tests are what tease out the attribution mechanism. A supplementary test that used the partners' strongest past alliance performance as the aspiration level found no significant interaction between that expectation-based performance feedback measure and the partners' perceived capability, which the authors read as ruling out an expectation-based alternative explanation for Hypothesis 2b.
- Results were robust across a linear probability model with firm fixed effects, a multinomial logistic estimation conditioned on firms, and a logistic estimation conditioned on firms; historical and weighted aspiration levels; samples that include nonequity alliances or minority acquisitions; quarterly return on assets in place of CAR; five alternative CAR event windows; alternative four-, seven-, and ten-year windows for the moderator measures; an alternative dependent variable based on the last rather than the first event in a quarter; dropping quarters in which firms made more than one alliance; dropping observations with no alliance or acquisition in the focal quarter; and alternative methods for handling tied failure events.

**Theoretical Contribution**
The study is the first to explicitly integrate the attribution process into performance feedback theory, showing that a firm's response to prior performance is significantly shaped by how managers attribute that performance and arguing that core predictions of performance feedback theory may require revision. By identifying three attribution-influencing moderators, it uncovers the theoretical mechanisms by which attribution operates and helps explain enduring inconsistent findings on whether failure triggers strategic change. It also extends corporate strategy research by providing the first behavioral account of the alliance-versus-acquisition choice, departing from economic and agency perspectives.

**Practical Implication**
Governance-mode decisions (alliances vs. acquisitions) are not purely rational or opportunistic but can be distorted by managerial heuristics and biases such as self-serving attribution. Managers and stakeholders should be aware that conditions enabling blame-shifting—many alliance partners, highly variable performance histories, or weakly capable partners—can suppress learning from alliance failure, so that failed alliances "could barely facilitate strategic change when the conditions promoting self-attribution were present."

**Limitations**
The study examines only the choice between acquisitions and alliances and cannot observe internal development (organic growth), which typically goes unannounced. Its performance measure (CAR), though most suitable here, may not generalize to other metrics. The theory focuses on the focal firm's attribution and does not integrate the partner firm's view, and although results are robust across alternative aspiration-level specifications, slack resources may also influence how attributions are formed.

**Future Research**
Future work could study settings where organic growth or other performance metrics can be reliably measured and tightly linked to specific actions, more fully integrate a partner's view "using appropriate methods," examine how attribution processes differ across alternative aspiration-level specifications, and explore how attribution and slack search jointly shape other types of organizational change such as managerial succession or foreign-market entry mode.

**APA 7th Citation**
Lee, J., Lee, J. M., & Kim, J.-Y. (J.). (2023). The role of attribution in learning from performance feedback: Behavioral perspective on the choice between alliances and acquisitions. *Academy of Management Journal*, 66(2), 578–603. https://doi.org/10.5465/amj.2019.1293
