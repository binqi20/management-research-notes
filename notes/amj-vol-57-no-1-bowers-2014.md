---
id: amj-vol-57-no-1-bowers-2014
title: "Competitive Parity, Status Disparity, and Mutual Forbearance: Securities Analysts' Competition for Investor Attention"
authors:
  - "Bowers, A. H."
  - "Greve, H. R."
  - "Mitsuhashi, H."
  - "Baum, J. A. C."
year: 2014
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2011.0818"
volume: 57
issue: 1
pages: "38-62"

source: "AMJ/vol-57-no-1"
pdf_path: "library/AMJ/vol-57-no-1/pdfs/Bowers 2014 Competitive Parity, Status Disparity, and Mutual Forbearance Securities Analysts Competition for Investor Attention.pdf"
text_path: "library/AMJ/vol-57-no-1/text/Bowers 2014 Competitive Parity, Status Disparity, and Mutual Forbearance Securities Analysts Competition for Investor Attention.txt"
ingested_at: "2026-07-10"
extraction_model: "claude-fable-5"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["competitive parity", "status disparity", "multipoint contact", "mutual forbearance", "securities analysts", "investor attention", "Regulation Fair Disclosure", "bold earnings estimates"]
theory: ["mutual forbearance theory (Simmel, 1950; Barnett, 1993; Baum & Korn, 1996)", "status-based model of market competition (Podolny, 1993)"]
topics: ["competitive-strategy", "regulation"]
unit_of_analysis: "individual"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Natural experiment (enactment of Regulation Fair Disclosure); archival panel of analyst earnings estimates from Thomson IBES (1995-2007) merged with Institutional Investor rankings, SDC Platinum underwriting data, and CRSP; three-stage least squares (3SLS) fixed-effect simultaneous linear probability regressions of boldness and accuracy"
sample:
  industry: "Sell-side securities analysis (equity analysts at brokerage firms covering publicly traded companies)"
  country: "United States"
  time_period: "January 1, 1995 to December 31, 2007"
  units: "Analyst-stock earnings estimates"
  n: "1,229,872 estimates (473,649 by 4,784 analysts pre-Reg-FD; 756,223 by 6,670 analysts under Reg-FD)"

# Mandatory evidence anchors (v3 - Layer 1 faithfulness audit).
evidence:
  sample_n: "The final sample included 1,229,872 estimates"
  sample_country: "traded companies in the United States between"
  sample_industry: "In particular, we examine how securities analysts responded"
  sample_time_period: "1, 1995, and December 31, 2007"
  theories_overview: "Mutual forbearance theory provides an account"
  methods_overview: "using three-stage least squares (3SLS)"
  keywords_source: "market structures that affect competitive behavior: competitive parity, status disparity,"
  hypotheses_source: "Hypothesis 2. The effect stated in Hypothesis 1"
  measures_overview: "more than 1.5 standard deviations and 0 otherwise."
  findings_overview: "We also predict and find that high-status analysts forbear more strongly."
---

# Competitive Parity, Status Disparity, and Mutual Forbearance: Securities Analysts' Competition for Investor Attention

**Abstract**
Most studies of responses to change in competitive environments focus on competitor-specific adaptations. However, rivals are often acutely aware of one another, and this awareness should influence their competitive behavior. In this study, we focus on three market structures that affect competitive behavior: competitive parity, status disparity, and multipoint contact. In particular, we examine how securities analysts responded to a regulatory discontinuity, Regulation Fair Disclosure ("Reg-FD"), which promotes competitive parity by eliminating privileged access to proprietary firm information as a critical source of competitive advantage. We predict and find that Reg-FD activated mutual forbearance among analysts linked through multipoint contact. We also predict and find that high-status analysts forbear more strongly. Analysts' responses to heterogeneity in competitive advantage thus depend importantly on their competitive overlap and status, which has implications for both their behavior and the information they provide to investors.

**Research Question**
How do two dimensions of competitive relationships, multipoint contact and status, influence securities analysts' responses to a regulatory change (Regulation Fair Disclosure) that abruptly eliminates privileged access to firm information as a critical source of competitive advantage?

**Hypotheses / Propositions**
H1: An analyst's likelihood of issuing bold earnings estimates on a stock is lower if the analyst experiences high multipoint contact with other analysts.
H2: The effect stated in Hypothesis 1 is stronger under Reg-FD and may be exclusive to the period after its enactment.
H3: Analysts with Institutional Investor's ranking are less likely to issue bold estimates after Reg-FD.
H4: The effect stated in Hypothesis 1 is stronger for analysts with II (Institutional Investor) ranking.

**Mechanism Process**
- IV(s): Analyst multipoint contact (average proportional stock co-coverage overlap with the other analysts covering a focal stock, computed over 12-month moving windows updated quarterly); Reg-FD (competitive-parity shock; dummy coded 1 for dates after October 1, 2000); analyst status (recency-weighted sum of Institutional Investor All-Star listings since 1990).
- DV(s): Analyst positive boldness and analyst negative boldness (estimate more than 1.5 standard deviations above/below the consensus estimate); accurate positive/negative boldness (supplementary accuracy outcomes).
- Mediators: Not reported in paper
- Moderators: Reg-FD x analyst multipoint contact (H2); Reg-FD x analyst status (H3); analyst multipoint contact x analyst status (H4).

Bold earnings estimates are competitive actions that attract investor attention and threaten rival analysts. Multipoint contact through co-coverage of the same stocks lets analysts recognize their mutual interdependence, develop reciprocal dominance over separate spheres of influence, and convey mutual threats of retaliation, raising the cost of boldness and inducing forbearance. Forbearance presupposes competitive parity: before Reg-FD, analysts with privileged access to corporate information had little incentive to enter reciprocal dominance relationships, so multipoint contact should suppress boldness mainly after Reg-FD leveled access to material information. Because the distress of losing status exceeds the pleasure of gaining it, high-status (II-ranked) analysts forbear more strongly when multipoint contact permits it, stabilizing the existing status order.

**Data & Measures**
Data: Thomson IBES earnings estimates issued by all named sell-side analysts for publicly traded US companies between January 1, 1995 and December 31, 2007 (final sample 1,229,872 estimates), augmented with Institutional Investor All-Star rankings, SDC Platinum underwriting data, and CRSP stock data. DVs: analyst positive/negative boldness = dummy coded 1 when an estimate differs from the consensus (mean of all active estimates the day before the focal estimate) by more than 1.5 standard deviations above/below it; accurate positive/negative boldness = bold estimates closer to actual earnings than the consensus. IVs: multipoint contact = average proportional portfolio overlap between the focal analyst and the other analysts covering the focal stock; Reg-FD = dummy coded 1 for dates after October 1, 2000; analyst status = years listed as an Institutional Investor All-Star since 1990, weighted by recency. Identification: the enactment of Reg-FD is treated as a natural experiment satisfying the three conditions for causal inference; estimation uses three-stage least squares (3SLS) simultaneous linear probability regressions with analyst-stock dyad fixed effects and analyst, brokerage, and stock controls.

**Key Findings**
- H1 supported: coefficients for analyst multipoint contact are negative and significant for both positive boldness (-0.027, p < .001) and negative boldness (-0.018, p < .001) in Model 2, and as expected the effect is stronger for positive bold estimates.
- H2 supported: the Reg-FD x multipoint contact interactions are negative and significant (-0.006, p < .10 for positive boldness; -0.048, p < .001 for negative boldness). Prior to Reg-FD, analysts issued more negative bold estimates on high multipoint contact stocks (main effect +0.014, p < .001), showing a breakdown of forbearance under unequal information access; the sum of the main effect and the Reg-FD interaction is negative and significant.
- H3 supported: high-status analysts were more likely to issue bold estimates before Reg-FD but had the same likelihood as low-status analysts under Reg-FD (the sum of coefficients before and after is not significantly different from zero).
- H4 supported: the multipoint contact x analyst status interaction is negative and significant (-0.011, p < .001 for positive boldness; -0.004, p < .01 for negative boldness); in split-period regressions this interaction falls below standard significance levels for positive boldness under Reg-FD.
- Accuracy: pre-Reg-FD bold estimates display uncanny accuracy (above 0.8 for both directions); under Reg-FD accuracy drops to 0.395 (positive) and 0.251 (negative), far below the 0.5 coin-toss threshold, and multipoint contact increases the accuracy of bold estimates.

**Theoretical Contribution**
The study establishes competitive parity and status disparity as boundary conditions of mutual forbearance theory, making one theoretical premise explicit: equal footing. When some actors hold a substantial informational competitive advantage, structural conditions that would otherwise facilitate mutual forbearance do not foster it; indeed, multipoint contact sharpened certain competitive actions (negative bold estimates) when information was restricted, a full reversal of the result under public information circulation. The paper also extends multipoint contact research, which had treated actors as equal and ignored the social structure of markets, by showing that high-status actors are more willing to forbear in order to stabilize the status order, placing the work at the intersection of the mutual forbearance, competitive parity, and status research traditions.

**Practical Implication**
For the policy makers who drafted and passed Reg-FD, the findings show that a regulatory crackdown on one form of collusion (companies' private disclosure of information to preferred analysts) was effective in its own right but led to an increase in another form of collusion (mutual forbearance among analysts linked by multipoint contact). The rise in mutual forbearance suggests that market information may not be conveyed as directly or efficiently as actors focus on each other as sources of competitive advantage rather than individual skill, which has implications for the information analysts provide to investors.

**Limitations**
The authors cannot rule out quiet releases of material information after Reg-FD, although they found no evidence of such leaks in analysts' estimates and argue that consistently accurate estimates are visible and arouse suspicion. The Sargan test indicated that bold estimates were not fully exogenous in the accuracy regression, indicating potential bias in the accuracy (though not the boldness) regressions used for hypothesis testing. The trade-offs analysts make between attention gains and inaccuracy risk cannot be directly observed and are examined only indirectly through the accuracy models.

**Future Research**
The authors point to studying the effects of public information circulation on competition in other settings, such as safety-intensive industries (airlines, railroads, nuclear power plants) and industries subject to fair competition regulations, and to the reverse process, in which an industry characterized by relative homogeneity in competitive strength becomes more heterogeneous (e.g., through deregulation or transitions from dominant designs to technological ferment). They propose examining analysts' expansion and contraction of coverage (entry and exit behaviors) and alternative observable outcomes of multipoint contact such as the accuracy and timeliness of estimates. They also call for research into the microcognitive processes through which actors learn to compete under novel conditions.

**APA 7th Citation**
Bowers, A. H., Greve, H. R., Mitsuhashi, H., & Baum, J. A. C. (2014). Competitive parity, status disparity, and mutual forbearance: Securities analysts' competition for investor attention. *Academy of Management Journal*, 57(1), 38-62. https://doi.org/10.5465/amj.2011.0818
