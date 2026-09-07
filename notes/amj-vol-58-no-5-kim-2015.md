---
id: amj-vol-58-no-5-kim-2015
title: "All Aspirations are not Created Equal: The Differential Effects of Historical and Social Aspirations on Acquisition Behavior"
authors:
  - "Kim, J.-Y. (J.)"
  - "Finkelstein, S."
  - "Haleblian, J. (J.)"
year: 2015
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2012.1102"
volume: 58
issue: 5
pages: "1361-1388"

source: "AMJ/vol-58-no-5"
pdf_path: "library/AMJ/vol-58-no-5/pdfs/Kim 2015 All Aspirations are not Created Equal The Differential Effects of Historical and Social Aspirations on Acquisition Behavior.pdf"
text_path: "library/AMJ/vol-58-no-5/text/Kim 2015 All Aspirations are not Created Equal The Differential Effects of Historical and Social Aspirations on Acquisition Behavior.txt"
ingested_at: "2026-07-06"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "gpt-6-astra"
augmented_at: "2026-09-07"

paper_type: "empirical-quantitative"
keywords: ["performance aspirations", "historical aspirations", "social aspirations", "performance feedback", "acquisition behavior", "acquisition performance variability", "U.S. commercial banking industry"]
theory: ["behavioral theory of the firm (Cyert & March, 1963)", "performance feedback theory", "aspiration-level theory"]
topics: ["strategy-innovation", "mergers-acquisitions", "behavioral-theory-of-the-firm", "quantitative-methods"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Empirical quantitative archival study using event history analysis and piecewise exponential models of repeat acquisitions; acquisition performance is measured with acquirer cumulative abnormal returns, split around historical and social aspiration levels, with interactions for prior acquisition performance variability."
sample:
  industry: "U.S. commercial banking industry; horizontal acquisitions among commercial banking institutions, including banks, thrifts, savings banks, and bank holding companies."
  country: "United States."
  time_period: "1988 to 2005."
  units: "Publicly traded commercial banking institutions, horizontal acquisitions, and yearly event-history spells."
  n: "3,010 acquisitions made by 642 publicly traded banks, transformed into 8,799 yearly spells."

evidence:
  sample_n: "3,010 acquisitions"
  sample_country: "U.S. commercial banking institutions"
  sample_industry: "commercial banking industry"
  sample_time_period: "between 1988 and 2005"
  theories_overview: "Building on the behavior theory of the firm"
  methods_overview: "We employed a piecewise exponential model"
  keywords_source: "historical and social aspirations"
  hypotheses_source: "making a subsequent acquisition is stronger"
  measures_overview: "the standard deviation of the acquirer market returns of"
  findings_overview: "results provide support for Hypothesis 2."
---

# All Aspirations are not Created Equal: The Differential Effects of Historical and Social Aspirations on Acquisition Behavior

**Abstract**
Research on performance aspirations has tended to assume that historical and social aspirations work in parallel and influence strategic behavior in a similar manner. We posit that these two distinct modes of performance comparison in fact lead to dissimilar firm behavior. We also explore how variability in prior acquisition performance influences the relationship between aspiration levels and subsequent strategic behavior. We examine our questions in the context of mergers and acquisitions within the U.S. commercial banking industry from 1988 to 2005. Consistent with our opening prediction, we find that firms’ acquisition behavior varies significantly depending on whether historical or social comparisons are used. We also find that high variability in the previous acquisition performance of a firm intensifies the relationship between acquisition performance relative to aspirations and the probability of the firm making acquisitions below historical and social aspirations, but attenuates the relationship above such aspirations.

**Research Question**
The paper asks whether historical and social aspiration levels produce different effects on firms' subsequent acquisition behavior. It also asks how variability in prior acquisition performance changes the relationship between acquisition performance relative to aspirations and the probability of making another acquisition.

**Hypotheses / Propositions**
- Baseline proposition: Acquisition performance relative to aspiration levels is positively related to the probability of a firm making a subsequent acquisition.
- H1: This positive relationship is weaker when acquisition performance is above the historical aspiration level than when it is below that level.
- H2: This positive relationship is stronger when acquisition performance is above the social aspiration level than when it is below that level.
- H3a: Below the aspiration level, the positive relationship between relative acquisition performance and the probability of a subsequent acquisition is stronger for firms with high acquisition performance variability than for those with low variability.
- H3b: Above the aspiration level, this positive relationship is weaker for firms with high acquisition performance variability than for those with low variability. H3a and H3b apply to both historical and social aspirations.

**Mechanism Process**
- IV(s): Acquirer market returns relative to historical aspiration levels; acquirer market returns relative to social aspiration levels; prior acquisition performance variability.
- DV(s): Hazard rate of making a subsequent acquisition.
- Mediators: Managerial interpretation of performance feedback, risk preferences, and search behavior are theorized processes, but no mediator is directly estimated.
- Moderators: Prior acquisition performance variability moderates the below-aspiration and above-aspiration performance-feedback relationships for both historical and social aspirations.

The mechanism is an interpretation-based performance feedback process. Historical aspirations compare current acquisition performance with the firm's own acquisition record, making capability assessments more internally grounded and encouraging caution when performance greatly exceeds prior standards. Social aspirations compare performance with other banks in the same core geographic market; because peer performance is more ambiguous, managers are more likely to interpret above-social-aspiration performance as evidence of their own capability and continue acquiring. High prior performance variability makes performance signals less reliable, intensifying acquisition persistence below aspirations but attenuating acquisition persistence above aspirations.

**Data & Measures**
The archival sample comprises 3,010 horizontal acquisitions by 642 publicly traded U.S. commercial banking institutions during 1988–2005, converted into 8,799 yearly spells. Acquisition records came from SNL Financial; stock market data came from the Center for Research in Securities Prices; financial and demographic data came from banking and regulatory databases. Banks entered the risk set with an acquisition; 220 banks exited through closure or acquisition or were right-censored without another acquisition by the study's end. The outcome is the hazard of a subsequent acquisition, using an acquisition event indicator and time at risk. Piecewise exponential event-history models treat acquisitions as repeatable events and include controls and year fixed effects; this is an associational design.

Acquirer market returns are cumulative abnormal returns (CARs) from one trading day before through one day after the acquisition announcement, capturing market feedback rather than realized acquisition gains. Historical aspirations are an exponentially weighted moving average of prior acquisition CARs, with a weighting parameter of 0.3. Social aspirations are the average acquisition market returns of other banks in the focal bank's core state market during the year before the focal acquisition; the core state supplies the largest amount of the bank's deposits. For each aspiration benchmark, separate below- and above-aspiration spline variables equal the focal CAR minus the benchmark on the relevant side and zero otherwise. The moderator is the standard deviation of market returns for all the bank's acquisitions since 1988 and before the focal acquisition. Historical aspirations and variability are set to zero when there is no prior acquisition record; a first-acquisition indicator controls for these observations.

**Key Findings**
The baseline prediction is supported in Table 2, Model 2: returns relative to both aspiration benchmarks are positively associated with subsequent acquisition rates. H1 is supported: the historical-aspiration slope is 7.47 below versus 1.01 above the benchmark (both p < .01); the marginal slope change in Model 2A is −6.46 (p < .01). H2 is supported: the social-aspiration slope is 5.83 below versus 8.70 above the benchmark (both p < .01), with a marginal increase of 2.87 (p < .05).

H3a and H3b are supported: performance variability strengthens the positive relationship below aspirations and weakens it above aspirations for both benchmarks. In the full Model 5, the historical below- and above-aspiration interaction coefficients are 57.76 (p < .05) and −35.60 (p < .01), respectively; the corresponding social-aspiration interactions are 134.13 and −85.33 (both p < .05). These are unstandardized coefficients. The below-social-aspiration main coefficient is nonsignificant in Models 4 and 5, which include its variability interaction. The proposed psychological processes were not directly tested.

**Theoretical Contribution**
The study extends behavioral theory of the firm and performance feedback research by showing that historical and social aspirations are not interchangeable reference points. It theorizes why aspiration sources differ in the information they encode and in the cognitive and organizational processes through which managers interpret them, and tests their differing associations with subsequent acquisition behavior. It also adds performance variability as a moderator of feedback-based learning, showing how variability can change whether managers treat performance shortfalls or successes as reliable signals for future acquisition behavior.

**Practical Implication**
The paper suggests that acquisition performance feedback can carry different meanings for managers. The same market reaction to a deal can motivate different future acquisition behavior depending on whether managers compare it with the firm's own history or with peer banks. The theory also suggests that highly variable prior deal performance can make both unusually good and unusually poor outcomes less diagnostic of underlying acquisition capability.

**Limitations**
The authors note that omitted variables may affect both acquisition performance and subsequent acquisition likelihood, even though they include extensive controls and year fixed effects. The study examines only horizontal acquisitions in U.S. commercial banking, so the findings may not hold for other acquisition types. It also proposes psychological processes such as self-enhancement and attention to variability but does not directly test those processes.

**Future Research**
Future research could examine when managers attend more to historical aspirations, social aspirations, absolute performance, relative performance, or performance variability. Studies could broaden the acquisition context beyond horizontal banking acquisitions and test whether the findings apply to different acquisition types. Laboratory studies could isolate the causal psychological processes linking aspiration feedback, performance variability, and subsequent strategic action, and future acquisition work could model aspirations and expectations together.

**APA 7th Citation**
Kim, J.-Y. (J.), Finkelstein, S., & Haleblian, J. (J.). (2015). All aspirations are not created equal: The differential effects of historical and social aspirations on acquisition behavior. *Academy of Management Journal*, 58(5), 1361-1388. https://doi.org/10.5465/amj.2012.1102
