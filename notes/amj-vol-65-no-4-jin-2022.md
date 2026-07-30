---
id: amj-vol-65-no-4-jin-2022
title: "The Use of Strategic Noise in Reactive Impression Management: How Do Market Reactions Matter?"
authors:
  - "Jin, Jing"
  - "Li, Haiyang"
  - "Hoskisson, Robert E."
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2018.1054"
volume: 65
issue: 4
pages: "1303-1326"

source: "AMJ/vol-65-no-4"
pdf_path: "library/AMJ/vol-65-no-4/pdfs/Jin 2022 The Use of Strategic Noise in Reactive Impression Management How Do Market Reactions Matter.pdf"
text_path: "library/AMJ/vol-65-no-4/text/Jin 2022 The Use of Strategic Noise in Reactive Impression Management How Do Market Reactions Matter.txt"
ingested_at: "2026-06-23"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["strategic noise", "reactive impression management", "expectancy violations theory", "mergers and acquisitions", "cumulative abnormal return", "stock market reaction"]
theory: ["expectancy violations theory (Burgoon, 1993, 2016)", "strategic noise / impression management literature (Graffin et al., 2011, 2016)"]
topics: ["mergers-acquisitions", "organizational-identity"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "social"
methods: "Archival event study; zero-inflated negative binomial regressions of reactive positive and negative strategic-noise counts on the magnitude (absolute CAR[-1,0]) and direction of the M&A stock-market reaction, with firm-clustered robust standard errors and year dummies; negative binomial models as robustness checks."
sample:
  industry: "Mergers and acquisitions (acquiring firms) across industries, drawn from the SDC M&A database"
  country: "Not reported in paper"
  time_period: "2001 to 2015"
  units: "M&A deals (acquiring-firm announcements as focal events)"
  n: "7,575 M&A deals (3,746 with negative and 3,829 with positive stock market reactions)"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "Our sample has 7,575 observations, including"
  sample_country: "Not reported in paper"
  sample_industry: "The initial sample for this study included all M&A"
  sample_time_period: "from 2001 to 2015"
  theories_overview: "Expectancy violations theory suggests that in social"
  methods_overview: "we adopted zero-inflated negative"
  keywords_source: "may intercede in the process of reactive impression management."
  hypotheses_source: "the market reaction (i.e., its absolute value) is positively related to the amount of reactive negative"
  measures_overview: "we measured strategic noise as the count of strategic"
  findings_overview: "42.172; p 5 0.015), supporting Hypothesis 1b."
---

# The Use of Strategic Noise in Reactive Impression Management: How Do Market Reactions Matter?

**Abstract**
Management scholars have argued and demonstrated that firms use strategic noise as an anticipatory form of impression management to minimize the effect of a potential negative reaction to an event of interest. In this study, we contribute to the impression management literature by exploring how both positive and negative strategic noise may intercede in the process of reactive impression management. We argue that in reactive impression management, since firms already know the initial market reaction to a focal event, they can “strategically” release subsequent positive or negative strategic noise depending upon the direction and magnitude of the initial market reaction to the focal event. Using a sample of 7,575 mergers and acquisitions from 2001 to 2015 that represent our focal events, we find strong evidence to support our arguments.

**Research Question**
How do firms use positive and negative strategic noise for *reactive* impression management once the initial stock market reaction to a focal event has become publicly known? Specifically, how do the direction (positive vs. negative) and magnitude (absolute value) of that market reaction shape the amount of reactive positive and negative strategic noise a firm subsequently releases?

**Hypotheses / Propositions**
- H1a: Following a negative stock market reaction to an M&A announcement, the magnitude of the market reaction (i.e., its absolute value) is negatively related to the amount of reactive positive strategic noise released by the acquiring firms.
- H1b: Following a negative stock market reaction to an M&A announcement, the magnitude of the market reaction (i.e., its absolute value) is positively related to the amount of reactive negative strategic noise released by the acquiring firms.
- H2a: Following a positive stock market reaction to an M&A announcement, the magnitude of the market reaction is negatively related to the amount of reactive positive strategic noise released by the acquiring firms.
- H2b: Following a positive stock market reaction to an M&A announcement, the magnitude of the market reaction is positively related to the amount of reactive negative strategic noise released by the acquiring firms.

**Mechanism Process**
- IV(s): Magnitude of the stock market reaction to an M&A announcement (absolute value of CAR[-1,0]); direction of the reaction (positive vs. negative), used to split the sample and tested jointly as a positive-reaction dummy.
- DV(s): Count of reactive positive strategic noise releases and count of reactive negative strategic noise releases (firm-controlled, event-unrelated news on Day +1 after the M&A announcement).
- Mediators: None modeled.
- Moderators: The direction of the reaction conditions the magnitude effect (the same hypotheses are developed separately for the negative-reaction and positive-reaction subsamples, yielding the Reactive Offsetting, Big-Bath, Amplifying, and Hiding effects).

Drawing on expectancy violations theory, the authors argue that the publicly observed market reaction signals the direction and magnitude of stakeholders' expectancy violation, which firms then exploit. When the reaction is negative but small, firms release more positive strategic noise to offset and possibly flip the violation (H1a); when the negative reaction is substantial, offsetting is futile, so firms disgorge negative news together to convert it into a negative expectancy confirmation and seed future positive surprises ("big bath," H1b). When the reaction is positive but small, firms amplify it with positive noise (H2a); when it is substantial, firms "hide" unrelated negative news under the positive reaction to avoid creating separate future negative violations (H2b). All four hypotheses are supported.

**Data & Measures**
- Design and sample construction: a single archival event study of acquiring firms. The initial sample was all M&A announcements recorded in the SDC M&A database from 2001 to 2015, restricted to deals in which the acquiring firm held less than 50% of the target at announcement and achieved a majority shareholding through the acquisition, and to SDC records coded as an acquisition of assets, an acquisition of majority interests, or a merger. First M&A announcement dates were cross-checked against Capital IQ, which includes all news released by firms; after eliminating observations with missing data, 23,005 observations remained. The analysed sample is 7,575 observations, comprising 3,746 M&As with negative stock market reactions and 3,829 deals with positive stock market reactions.
- Data sources: SDC (deal characteristics), Capital IQ (news verification), CRSP (daily stock returns), COMPUSTAT (other financial information), ExecuComp (executive information), and the Corporate Library (governance data). Firm reputation was taken from Fortune's "Most Admired Companies" rankings for years after 2006 and the Wall Street Journal/Harris Interactive "Corporate Reputation" list for years before 2006.
- DVs (event counts): strategic noise was coded as present when three criteria were met at the time of an M&A — the firm announced a confounding event within one day (the [-1, +1] day window) of the M&A announcement, the event was completely under the control of the firm, and the event was not intended to clarify or be causally related to the M&A (examples: changes in dividend rates, key executives or directors, and earnings). Releases were then classified by content as positive or negative; ambiguous releases were resolved with additional information (earnings above estimates coded positive, estimate confirmations neutral, decreases negative). Reactive positive strategic noise is the count of positive strategic noise items released on Day +1 (used to test H1a and H2a); reactive negative strategic noise is the count of negative items released on Day +1 (H1b and H2b). A density measure (confounding events in the [-1, +1] window divided by 3 days) was used only for the Table 2 validity check.
- Coding reliability: a research assistant independently classified a random 10% of each news type as positive, negative, or neutral. ICC(2, 1) ranged from 0.77 to 0.85 and ICC(2, k) from 0.87 to 0.92, all above the 0.60 benchmark.
- IV: cumulative abnormal return CAR[-1, 0], the sum of daily abnormal returns relative to the market portfolio, with the market-model parameters estimated over a 250-day window running from 295 to 45 days before the focal acquisition. For H1a and H1b the authors use the absolute value of the negative CAR[-1, 0]. A supplementary pooled analysis instead constructs two variables to separate sign from size: magnitude of CAR[-1, 0] (its absolute value) and a positive market reaction dummy (1 when CAR[-1, 0] is positive, 0 when negative).
- Controls. Acquirer-related: firm size (logarithm-transformed sales), lagged ROA, diversification (entropy method), debt ratio, and firm reputation (1 if the firm appeared among the top 25 on the relevant reputation list in a given year, 0 otherwise). Deal-related: baseline positive and baseline negative confounding rates computed over the three months before the deal (Day -121 to Day -30, divided by 91 days), acquisition size (natural log of transaction value), stock percentage, similar acquisition experience (same four-digit SIC targets in the prior three years), a cross-border dummy, a Friday-announcement dummy, an earnings call within [-1, +1] dummy, and competitor M&As within [-1, +1]. Governance-related: CEO tenure, CEO total compensation, board size, and independent outside director ratio. Environment-related: environmental dynamism (five-year industry sales growth-rate variability, lagged one year). Year dummies are included in all models.
- Estimation: a goodness-of-fit test after Poisson regression indicated overdispersion, and the count DVs contained excessive zeros, so hypotheses were tested with zero-inflated negative binomial regressions with standard errors clustered at the firm level, specifying the baseline positive-negative confounding rate as the factor predicting whether strategic noise was zero. Negative binomial regressions were run as a robustness check and the results remained the same. The design is archival and associational: the paper names no causal identification strategy and states its predictions as relationships between the observed market reaction and subsequently released noise.

**Key Findings**
- H1a supported. In the negative-reaction subsample (3,746 observations), the coefficient on the magnitude of the negative market reaction predicting reactive positive strategic noise is significantly negative (b = -20.160; p = 0.011; Table 3, Model 2).
- H1b supported. In the same subsample, the coefficient on the magnitude of the negative market reaction predicting reactive negative strategic noise is significantly positive (b = 42.172; p = 0.015; Table 3, Model 4). Taken together, the authors read H1a and H1b as showing that after a negative reaction, the more significant that reaction, the less positive but the more negative strategic noise the firm releases.
- H2a supported. In the positive-reaction subsample (3,829 observations), the coefficient on CAR[-1, 0] predicting reactive positive strategic noise is significantly negative (b = -12.504, p = 0.019; Table 4, Model 2).
- H2b supported. In the same subsample, the coefficient on CAR[-1, 0] predicting reactive negative strategic noise is significantly positive (b = 44.290, p < 0.001; Table 4, Model 4). The authors illustrate the combined H2a/H2b pattern: when the CAR moves from 0.01 to 0.02, the firm will release 12% less positive strategic noise and 56% more negative strategic noise.
- Direction adds to magnitude. In the pooled supplementary models (Table 5, 7,575 observations), firms receiving a positive stock market reaction released significantly more negative strategic noise than those receiving a negative reaction (b = 0.711, p = 0.034), but there was no significant difference in positive strategic noise release between the two groups (b = 0.059, n.s.).
- Firms appear unable to anticipate the reaction. In the same table, the positive stock market reaction coefficient is insignificant in both anticipatory strategic noise models (Models 3 and 4), which the authors interpret as evidence that firms cannot predict the stock market reaction ex ante.
- Baseline validation of the noise assumption. 38.03% (8,748 of 23,005) of acquisitions had at least one confounding event within the Day -1 to Day +1 window; average strategic noise density was 21.7% against baseline confounding rates of 11.9% (prior three months), 11.7% (prior six months), and 11.4% (prior year), with paired t-tests of 46.57, 47.21, and 48.64 respectively (all p < 0.001) and 95% confidence bounds on the differences entirely above zero.
- Supplementary robustness. Other M&A-related factors are significantly associated with strategic noise in the three-day window (acquisition size b = 0.223, p < 0.001; stock percentage b = 0.003, p = 0.001; acquisition experience b = 0.022, p = 0.003; Table 6, 7,890 observations), which the authors treat as evidence that the M&A is the focal event rather than the noise. Only 5.8% (1,337 of 23,005) of M&A announcements coincided with earnings calls, and an unreported analysis excluding dividend and new-product releases left the results unchanged. An unreported test of whether market reactions influence the release of *inconsistent* strategic noise returned insignificant results. All estimates are associational.

**Theoretical Contribution**
The study extends the strategic-noise and impression-management literatures—previously focused almost exclusively on *anticipatory* IM—by being the first to systematically theorize and demonstrate strategic noise as a *reactive* IM tactic. By integrating expectancy violations theory, it shows that positive and negative strategic noise play distinct roles that depend jointly on the direction and magnitude of an already-realized expectancy violation, revealing that the offsetting role of positive noise is limited in reactive IM and that firms may deploy both anticipatory-style (big-bath, hiding) motives reactively when violations are substantial.

**Practical Implication**
For executives releasing news around M&A announcements, the magnitude of the market reaction matters more than its direction in shaping effective reactive IM. Firms can dampen the strategic effect of negative events by using the hiding effect (under a significant positive reaction) or the big-bath effect (under a significant negative reaction), and should attend to the absolute size of the expectancy violation rather than assuming, as executives tend to, that positive and negative violations call for categorically different responses.

**Limitations**
The study treats each news release independently and does not model relationships or consistency among different pieces of news (or between the noise and the M&A itself). The same news type may be positive for one firm or audience and negative for another, introducing classification ambiguity. The authors also do not test whether firms following the proposed IM strategies actually achieve better short- or long-term outcomes (e.g., media sentiment, deal completion).

**Future Research**
Future work could examine whether inconsistency between confounding events and the focal decision affects IM effectiveness, whether the same news is interpreted differently across firms and audience groups, and whether firms adhering to these strategies outperform deviators on outcomes such as media-coverage sentiment, M&A completion likelihood, and deal duration. Researchers could also explore how industry/competitive spillovers shape a focal firm's choice of positive versus negative strategic noise.

**APA 7th Citation**
Jin, J., Li, H., & Hoskisson, R. E. (2022). The use of strategic noise in reactive impression management: How do market reactions matter? *Academy of Management Journal*, 65(4), 1303–1326. https://doi.org/10.5465/amj.2018.1054
