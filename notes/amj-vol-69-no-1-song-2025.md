---
id: amj-vol-69-no-1-song-2025
title: "Anticipatory Impression Management for Potential Adverse Events: Positive Framing in the Wake of Short Seller Attacks on a Competitor"
authors:
  - "Song, R."
  - "Connelly, B. L."
  - "Ketchen, D. J., Jr."
  - "Shi, W."
year: 2026
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0914"
volume: 69
issue: 1
pages: "99-122"

source: "AMJ/vol-69-no-1"
pdf_path: "library/AMJ/vol-69-no-1/pdfs/Song 2025 Anticipatory Impression Management for Potential Adverse Events Positive Framing in the Wake of Short Seller Attacks on a Competitor.pdf"
text_path: "library/AMJ/vol-69-no-1/text/Song 2025 Anticipatory Impression Management for Potential Adverse Events Positive Framing in the Wake of Short Seller Attacks on a Competitor.txt"
ingested_at: "2026-07-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["anticipatory impression management", "positive framing", "short seller attacks", "earnings conference calls", "product-market similarity", "awareness-motivation-capability"]
theory: ["anticipatory impression management (Elsbach, Sutton, & Principe, 1998)", "awareness-motivation-capability framework (Chen, 1996)", "theory elaboration (Fisher & Aguinis, 2017)"]
topics: ["ceo-leadership", "competitive-strategy", "shareholder-activism"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "social"
methods: "Longitudinal panel; firm and year-quarter fixed-effects OLS regressions with interaction terms; difference-in-differences robustness check; content analysis of earnings-call transcripts using Loughran-McDonald sentiment dictionaries."
sample:
  industry: "Cross-industry; publicly listed U.S. firms whose direct competitor was attacked by a short seller (competitors identified via the Hoberg-Phillips TNIC-3 text-based network industry classification)"
  country: "United States"
  time_period: "2007-2022"
  units: "Firm-quarters (competitors of short-seller-attacked firms), nested in firms"
  n: "1,989 firms; 344 unique short attacks; 11,824 firm-quarter observations"

# Mandatory evidence anchors (v3 — Layer 1 faithfulness audit).
evidence:
  sample_n: "1,989 firms with a direct competitor attacked by a short seller"
  sample_country: "listed on the NASDAQ or New York Stock Exchange"
  sample_industry: "Not reported in paper"
  sample_time_period: "from 2007 through 2022"
  theories_overview: "Anticipatory impression management (AIM) provides a theoretical foundation"
  methods_overview: "We tested our hypotheses using firm fixed-effects"
  keywords_source: "CEO positive framing in earnings conference calls"
  hypotheses_source: "will be positively associated with CEO positive framing"
  measures_overview: "the cumulative abnormal returns (CAR) after a short"
  findings_overview: "positive framing (b 5 0.47, p , .05)"
---

# Anticipatory Impression Management for Potential Adverse Events: Positive Framing in the Wake of Short Seller Attacks on a Competitor

**Abstract**
Anticipatory impression management (AIM) provides a theoretical foundation for understanding the tactics organizations use to mitigate the potential adverse consequences of known upcoming events. We extend this theorizing to encompass potential upcoming events with known adverse consequences. We posit that a potential event is more likely to induce AIM to the extent that the firm is aware the event might occur, motivated to mitigate its potential consequences, and capable of engaging in tactics that could reduce the event’s likelihood. We test our theorizing in the scenario wherein a competitor has been attacked by a short seller, which raises the specter of a short seller attack on the focal firm. We contend that, following an attack on a competitor, chief executive officers use positive framing in earnings conference calls as an AIM tactic to deter short sellers. Examination of 1,989 firms with a direct competitor attacked by a short seller confirms our ideas. Our study thus extends the boundaries of theory on AIM and broadens research on short selling to encompass principles of attack prevention.

**Research Question**
Under what conditions does a firm engage in anticipatory impression management—specifically, CEOs' use of positive framing in earnings conference calls—in the wake of a short seller attack on a competitor, a potential event with known adverse consequences? Guided by Chen's (1996) awareness-motivation-capability logic, when is a firm more or less likely to use AIM before such a potential event occurs?

**Hypotheses / Propositions**
H1. Following a short seller attack on a competitor, CEO positive framing in earnings conference calls will be higher than it was prior to the attack.
H2. Following a short seller attack on a competitor, a firm's product-market similarity to the attacked firm will be positively associated with CEO positive framing in earnings conference calls.
H3. Following a short seller attack on a competitor, the magnitude of stock price decline at the attacked firm will be positively associated with CEO positive framing in earnings conference calls.
H4. Following a short seller attack on a competitor, a focal firm's recent (prior) stock price performance will be positively associated with CEO positive framing in earnings conference calls.

**Mechanism Process**
- IV(s): Short seller attack on a competitor (binary: 0 for the four quarters before the first attack on a competitor, 1 for the four quarters after)
- DV(s): CEO positive framing in earnings conference calls (positive minus negative words, scaled by speech length; Loughran-McDonald dictionaries)
- Mediators: Not reported in paper
- Moderators: Product-market similarity to the attacked firm (H2); magnitude of the attacked firm's stock price decline (H3); focal firm's prior stock price performance (H4)

Grounded in AIM theory and Chen's (1996) awareness-motivation-capability (AMC) framework, the study argues that a short seller attack on a competitor raises the specter of a similar attack on the focal firm. When a firm is aware the event might occur, motivated to prevent it, and capable of credibly framing positively, its CEO proactively uses positive framing in earnings calls to deter short sellers before an attack materializes. The paper elaborates AIM from known upcoming events with uncertain consequences to potential events with known adverse consequences, shifting uncertainty from the event's consequences to whether the event occurs.

**Data & Measures**
Short attack data came from Insightia (short-seller campaigns, 2007-2022); competitors of attacked firms were identified with the Hoberg-Phillips TNIC-3 text-based network industry classification; earnings-call transcripts came from Thomson Reuters StreetEvents and Capital IQ; stock and accounting data came from CRSP/Compustat. DV, positive framing: CEO positive words minus negative words (Loughran-McDonald 2011 dictionaries; 354 positive and 2,355 negative words), scaled by speech length, coded from the managerial-discussion section of the call. IV: a binary short-attack indicator (0 = four quarters pre-attack on a competitor, 1 = four quarters post). Moderators: product-market similarity (TNIC-3 product-similarity score combined with the two firms' relative market share, min-max normalized); stock price decline of the attacked firm (cumulative abnormal returns, CAR, over a three-day [-1, +1] window, using the absolute value of negative CAR); focal firm's prior performance (quarter-prior stock returns standardized by competitors). Estimation used firm and year-quarter fixed-effects OLS with the moderators entered as interactions with the IV; time-invariant controls were interacted with the IV; a difference-in-differences design served as a robustness check.

**Key Findings**
All four hypotheses were supported. H1: a short seller attack on a competitor has a positive and significant effect on CEO positive framing (β = 0.47, p < .05), corresponding to roughly a 21% increase in positive framing versus pre-attack calls (at zero moderator values). H2 supported: short attack × product-market similarity is positive and significant (β = 0.15, p < .01). H3 supported: short attack × stock price decline is positive and significant (β = 0.94, p < .01). H4 supported: short attack × prior performance is positive and significant (β = 0.23, p < .01), with the marginal effect becoming meaningful only above a threshold of prior performance (significant near the 15th percentile). Results were robust to difference-in-differences estimation. A post hoc analysis found that positive framing is negatively associated with the firm's subsequent short interest (β = -0.06, p < .01), suggesting positive framing can deter short selling.

**Theoretical Contribution**
The study elaborates AIM theory (Fisher & Aguinis's theory elaboration) by extending it from known upcoming events with potentially adverse consequences to potential events with known adverse consequences, thereby shifting the locus of uncertainty from the event's consequences to the event's occurrence. Using Chen's (1996) AMC framework as an organizing logic, it specifies the awareness, motivation, and capability conditions that initiate AIM before a potential event, and it extends AIM to an adversarial audience (short sellers) whom firms seek to deter rather than merely appease. A secondary contribution to short-selling research uncovers a previously overlooked spillover effect of short seller attacks on competitors of the attacked firm and theorizes the ex ante steps firms take in anticipation of short selling.

**Practical Implication**
Viewed from an oversight perspective, boards may encourage CEOs to engage in AIM (positive framing) to pre-empt volatility from anticipated disruptions, and could direct executives' attention to the AMC factors—how similar the attacked competitor is, how severe the attack was, and the firm's own vulnerabilities. More generally, because "good words are worth much, and cost little," firms may treat words as a low-cost first line of defense against short sellers and other hostile actors, though firms with very poor prior performance cannot credibly use positive language and thus lose this tool. The findings may also inform regulators, since short seller attacks that spill over to competitors can carry both corrective and disruptive effects across multiple firms.

**Limitations**
The authors could not fully account for the underlying reasons firms are susceptible to short seller attacks, though a supplementary test suggests spillover is more likely when a competitor is accused of product flaws than of accounting problems. The archival data did not permit direct assessment of the decision-making process that leads to AIM. The model's goodness-of-fit improved only marginally from the baseline to the full model, possibly reflecting nonlinearities or an excess of nonsignificant control variables. The study focuses on the potential for a short seller attack, whereas firms face many other events with negative consequences (e.g., investor activism, employee strikes, buyer demands).

**Future Research**
The authors call for combining actions with words to build a more comprehensive theory of AIM behavior, and for integrating AIM with theories such as protection motivation theory and threat rigidity theory to study long-term, over-time effects. They suggest exploring interorganizational nuances (including framing the potential event as a "selection decision" and drawing on signaling theory), testing the ideas with experimental or policy-capturing designs among CEOs and top executives, using case studies to examine how firms perceive antecedents of short seller attacks, and developing a "multiplex" version of AIM—combined with an attention-based view—that addresses multiple audiences and other threat contexts such as hostile takeovers, market entry, competitive dynamics, and labor disputes.

**APA 7th Citation**
Song, R., Connelly, B. L., Ketchen, D. J., Jr., & Shi, W. (2026). Anticipatory impression management for potential adverse events: Positive framing in the wake of short seller attacks on a competitor. *Academy of Management Journal, 69*(1), 99–122. https://doi.org/10.5465/amj.2023.0914
