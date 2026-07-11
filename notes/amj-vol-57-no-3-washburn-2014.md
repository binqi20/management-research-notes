---
id: amj-vol-57-no-3-washburn-2014
title: "Managers and Analysts: An Examination of Mutual Influence"
authors:
  - "Washburn, M."
  - "Bromiley, P."
year: 2014
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2011.0420"
volume: 57
issue: 3
pages: "849-868"

source: "AMJ/vol-57-no-3"
pdf_path: "library/AMJ/vol-57-no-3/pdfs/Washburn 2014 Managers and Analysts An Examination of Mutual Influence.pdf"
text_path: "library/AMJ/vol-57-no-3/text/Washburn 2014 Managers and Analysts An Examination of Mutual Influence.txt"
ingested_at: "2026-07-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["impression management", "securities analysts", "forecast guidance", "conference calls", "press releases", "earnings per share"]
theory: ["impression management (Elsbach, 2003; Pfarrer, Pollock, & Rindova, 2010; Rindova, Williamson, Petkova, & Sever, 2005)", "information intermediaries and the social construction of reputation (Rindova, Pollock, & Hayward, 2006; Bitektine, 2011)", "information asymmetry and signaling in manager-analyst exchange (Sanders & Carpenter, 2003; Basdeo et al., 2006)"]
topics: ["financial-reporting", "corporate-governance"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "social"
methods: "Longitudinal firm-quarter panel of large US firms (S&P 500 as of January 2002, excluding financials). Simultaneous-equation models of three impression management activities: probit with firm dummies and endogeneity corrections for forecast guidance; two-stage least squares with firm fixed effects and robust standard errors for (log) press releases and conference calls; 50-dataset multiple imputation for missing press-release data. Change in analysts' subsequent forecasts modeled with firm fixed-effects regression interacting each activity with above-target and below-target."
sample:
  industry: "Large publicly traded firms across industries (S&P 500 as of January 2002), excluding financial-industry firms (SIC 5999-7000) and unclassified firms (SIC 9999)"
  country: "United States"
  time_period: "January 2002 - December 2007"
  units: "firm-quarters"
  n: "116 firms in the hand-collected press-release subsample; roughly 2,300-2,447 firm-quarters for hand-collected data and about 7,000-7,400 firm-quarters for the archival variables"

# Mandatory evidence anchors (v3 — Layer 1 faithfulness audit).
evidence:
  sample_n: "consisted of 116 firms"
  sample_country: "data on large US firms"
  sample_industry: "We excluded firms from the financial"
  sample_time_period: "We began our sample in January of 2002 and ended in December 2007"
  theories_overview: "We draw on the impression management literature to offer hypotheses"
  methods_overview: "We test this dyadic representation of impression management activities using a longitudinal panel of large firms"
  keywords_source: "issuing forecast guidance, having conference calls with analysts, and issuing press releases"
  hypotheses_source: "Hypothesis 1. The extent earnings diverge"
  measures_overview: "taken to equal unity if the firm provided point"
  findings_overview: "supports Hypothesis 1 for firms with performance"
---

# Managers and Analysts: An Examination of Mutual Influence

**Abstract**
Securities analysts' predictions of firms' earnings per share constitute important performance targets for those firms. Firm managers attempt to both influence analysts' targets and achieve the targets. We draw on the impression management literature to offer hypotheses regarding how a firm's performance relative to prior targets influences the impression management activities of issuing forecast guidance, having conference calls with analysts, and issuing press releases. We also consider the influence of these impression management activities on subsequent analysts' targets. We test this dyadic representation of impression management activities using a longitudinal panel of large firms. Findings suggest managers take a variety of actions that vary with firm performance, and that some of those actions influence subsequent analyst targets under some conditions.

**Research Question**
How does a firm's performance relative to prior analyst earnings-per-share targets influence managers' impression management activities — issuing forecast guidance, holding conference calls, and issuing press releases — and how do those activities in turn influence analysts' subsequent forecasts, given that managers and analysts engage in a recursive, dyadic process in which neither party fully controls the outcome?

**Hypotheses / Propositions**
H1: The extent earnings diverge above or below analyst forecasts decreases the likelihood managers issue forecast guidance.
H2a: The extent that earnings diverge (above or below) analyst forecasts increases the number of press releases that managers subsequently issue.
H2b: The divergence of earnings from analyst forecasts has a larger influence on the number of press releases when earnings are below rather than above analyst forecasts.
H3a: The extent that earnings diverge (above or below) analyst forecasts positively influences the number of conference calls that managers subsequently undertake.
H3b: The divergence of earnings from analyst forecasts has a larger influence on the number of conference calls when earnings are below rather than above analyst forecasts.
H4: For firms with earnings significantly above analyst targets, forecast guidance, press releases, and conference calls negatively influence the change in subsequent analyst forecasts.
H5: For firms with earnings significantly below analyst targets, forecast guidance, press releases, and conference calls negatively influence the change in subsequent analyst forecasts.

**Mechanism Process**
- IV(s): above target and below target — the amount by which announced EPS exceeds (above target) or falls short of (below target) the last analyst consensus forecast
- DV(s): three impression management activities — forecast guidance (binary), press releases (natural log of the count), and conference calls (count); and, in the second model, the change in analysts' subsequent EPS forecasts
- Mediators: Not reported in paper — the three activities are dependent variables in the first-stage models and become explanatory variables in the second-stage forecast-change model, forming a recursive dyadic process rather than a tested mediation chain
- Moderators: the direction of divergence (below target vs. above target) as an asymmetry (H2b, H3b); above target and below target moderate how each impression management activity affects the change in analyst forecasts (H4, H5 interaction terms)

Drawing on impression management theory, the paper models a recursive, dyadic process: analysts set EPS targets, firms report performance relative to those targets, and managers respond with impression management activities whose intensity varies with the magnitude and direction of the performance-target divergence; these activities then feed back into analysts' subsequent forecast revisions. Larger deviations — especially shortfalls below target — heighten a firm's need to explain itself and so raise press releases and conference calls, whereas divergence in either direction discourages forecast guidance because guidance puts managers' reputations as accurate, competent forecasters at risk. Because neither party fully controls the process, the authors use the language of "influence" rather than direct causal control.

**Data & Measures**
Data sources: analyst quarterly EPS forecasts from I/B/E/S; forecast guidance from the First Call database; conference calls from the BestCalls database; financial data from Compustat Fundamentals Quarterly; institutional ownership from Thomson Reuters CDA/Spectrum (13F); press-release counts hand-collected from Lexis Nexis and verified against Hoover's Pro Online. Key dependent measures: forecast guidance = 1 if the firm provided point or interval estimate forecasts or made a material statement about an existing analyst forecast, else 0 (about 44% of firm-quarters); conference calls = count of management-analyst calls (values 0-17); press releases = natural log of the total number of press releases per period (mean 37, maximum 1,794). Independent variables of theoretical interest: above target = announced EPS minus the analyst consensus forecast when earnings exceeded the forecast (else 0); below target = consensus forecast minus announced EPS when the forecast exceeded earnings (else 0); differences greater than $1 were excluded. Second-model outcome: forecast change = mean analyst EPS forecast for quarter t generated in quarter t-1 minus the mean forecast for quarter t generated in quarter t-2. Controls: analyst consensus (SD of prior-period forecasts), fourth-quarter effect, change in and number of analyst forecasts, earnings management (deferred component of income tax expense scaled by quarterly assets), firm size (log market capitalization), and transient / quasi-indexer / dedicated institutional ownership. Estimation and identification: firm dummies / fixed effects with corrections for endogeneity among the three activities (probit for forecast guidance; two-stage least squares with robust standard errors for press releases and conference calls; fixed-effects regression for forecast change), plus 50-dataset multiple imputation for missing press-release data and Cook's D / dbeta outlier trimming. The design is an observational panel; the authors deliberately use "influence" language, noting the lack of direct control (associational, not an experimental identification strategy).

**Key Findings**
Managers' impression management activities varied systematically with performance relative to analyst targets. H1 was strongly supported: divergence both above target (b = -2.72, p < .001) and below target (b = -3.14, p < .001) reduced the likelihood of issuing forecast guidance. H2a was supported: divergence increased press releases for both above target (b = 0.40, p < .01) and below target (b = 0.55, p < .01). H2b was not supported: the below-target parameter exceeded the above-target parameter, but the difference just missed significance (χ²(1) = 2.48, p = .12). H3a was partially supported: divergence increased conference calls for below target (b = 0.505, p < .01) but not for above target (b = -0.039, n.s.). H3b was supported: the below-target influence on conference calls was significantly greater than the above-target influence across all 50 imputed datasets. H4 and H5 (effects of the activities on subsequent forecast revisions) were only partially supported, and only through conference calls: conference calls significantly reduced (smoothed) the increase in subsequent forecasts for firms with performance well above or well below target (negative interactions with above target and below target, significant in most windows). Forecast guidance had no significant effect on forecast change (H4/H5 not supported for forecast guidance). Contrary to H4/H5, press releases most strongly and negatively influenced forecast change when performance was near the target, becoming insignificant at extreme divergence.

**Theoretical Contribution**
The paper extends impression management theory from a predominantly one-directional view — firms projecting impressions onto passive audiences — to a two-way, continuing process of mutual influence in which managers and analysts each react to the other and neither fully controls the outcome. It advances a relational view of how stakeholders negotiate the value of socially constructed assets such as legitimacy, reputation, and status, and shows that the medium of transmission itself conveys information: how messages are communicated, not only their content, shapes their reception. Empirically, it demonstrates that firms' impression management activities vary systematically with performance relative to analyst targets and that some activities — notably conference calls — shape subsequent analyst forecasts under extreme performance.

**Practical Implication**
Managers may manage impressions more effectively if they systematically adapt their communication behavior — the choice among forecast guidance, press releases, and conference calls — to their firm's performance relative to analyst targets and to the target audience.

**Limitations**
The analysis examined only the media and channels of impression management, not the specific content of managers' messages. It lacked direct measures of analysts' sensitivity to influence, so the modest effects on forecast revision may reflect variation in the content or intent of the activities, variation in analysts' ability to discount them, or problems in the study's ancillary theoretical assumptions. By focusing solely on the manager-analyst relation, the study de-emphasized analysts' indirect influence on firms' access to external resources and the role of other intermediaries such as journalists and outside directors. The study also stops short of a normative analysis of whether managers should attempt to influence forecasts.

**Future Research**
The authors call for examining how the influence of firms' messages changes as those messages move through networks of intermediaries (for example, journalists and other analysts) to provide a more complete representation of managerial impression management. They also call for a normative analysis of whether managers should attempt to influence forecasts — one that allows for divergence between managers' and the firm's motivations, and that considers whether impression management activities systematically bias analyst forecasts and how such biases affect the firm.

**APA 7th Citation**
Washburn, M., & Bromiley, P. (2014). Managers and analysts: An examination of mutual influence. *Academy of Management Journal*, *57*(3), 849-868. https://doi.org/10.5465/amj.2011.0420
