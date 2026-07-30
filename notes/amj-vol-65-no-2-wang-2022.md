---
id: amj-vol-65-no-2-wang-2022
title: "The Past Is Prologue? Venture-Capital Syndicates’ Collaborative Experience and Start-Up Exits"
authors:
  - "Wang, Dan"
  - "Cox Pahnke, Emily"
  - "McDonald, Rory M."
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2019.1312"
volume: 65
issue: 2
pages: "371-402"

source: "AMJ/vol-65-no-2"
pdf_path: "library/AMJ/vol-65-no-2/pdfs/Wang 2022 The Past Is Prologue Venture-Capital Syndicates’ Collaborative Experience and Start-Up Exits.pdf"
text_path: "library/AMJ/vol-65-no-2/text/Wang 2022 The Past Is Prologue Venture-Capital Syndicates’ Collaborative Experience and Start-Up Exits.txt"
ingested_at: "2026-06-23"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["relational embeddedness", "venture-capital syndicates", "interorganizational collaboration", "start-up exits", "acquisition", "initial public offering", "focused success", "broadcast success"]
theory: ["relational embeddedness / paradox of embeddedness (Granovetter, 1985; Uzzi, 1997)", "social capital theory", "interorganizational networks"]
topics: ["entrepreneurship", "social-capital-theory", "mergers-acquisitions", "north-america"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Longitudinal observational study of Crunchbase data; competing-risks proportional-hazards (Cox-type) models of time-to-exit, with Heckman selection correction (inverse Mills ratio) and inverse-probability-of-treatment weighting (IPTW) to address endogeneity; supplemented by linear regression of acquisition-target market-segment similarity."
sample:
  industry: "Technology-sector start-ups across 444 Crunchbase market segments (e.g., software, enterprise software, analytics, e-commerce, mobile, clean technology, semiconductors) backed by venture-capital and angel investors"
  country: "United States"
  time_period: "1982 to July 2014"
  units: "VC-backed start-ups (and their first-round VC syndicates)"
  n: "10,879 U.S.-based VC-backed start-ups"

evidence:
  sample_n: "Of the 10,879 U.S.-based VC-backed start-ups"
  sample_country: "Because the United States is the primary context"
  sample_industry: "enterprise software, analytics, e-commerce, mobile, clean"
  sample_time_period: "between 1982 and July 2014"
  theories_overview: "the so-called paradox of embeddedness,"
  methods_overview: "we use Cox proportional hazards"
  keywords_source: "more likely to exit by acquisition (which we call a"
  hypotheses_source: "Hypothesis 2. A start-up is more likely to exit via IPO"
  measures_overview: "We measure VC joint collaboration experience by"
  findings_overview: "with less prior experience among the group of VCs, a jointly funded start-up is more likely to exit by initial public offering"
---

# The Past Is Prologue? Venture-Capital Syndicates’ Collaborative Experience and Start-Up Exits

**Abstract**
Past research has produced contradictory insights into how prior collaboration between organizations—their relational embeddedness—impacts collective collaborative performance. We theorize that the effect of relational embeddedness on collaborative success is contingent on the type of success under consideration, and we develop a typology of two kinds of success. We test our hypotheses using data from Crunchbase on a sample of almost 11,000 U.S. start-ups backed by venture-capital (VC) firms, using the VCs’ previous collaborative experience to predict the type of success that the start-ups will experience. Our findings indicate that as prior collaborative experience within a group of VCs increases, a jointly funded start-up is more likely to exit by acquisition (which we call a focused success); with less prior experience among the group of VCs, a jointly funded start-up is more likely to exit by initial public offering (a broadcast success). Our results deepen understanding of the connections between organizational performance and collaboration networks, contributing to entrepreneurship research on the role of investors in technology ventures.

**Research Question**
When do prior collaborations between organizations breed collaborative success? Specifically, how does the relational embeddedness of a start-up's first-round VC syndicate—the extent to which its members have previously coinvested together—shape whether the start-up achieves a "focused" success (acquisition) versus a "broadcast" success (IPO)?

**Hypotheses / Propositions**
- H1: A start-up is more likely to exit via acquisition if its VC investors have higher levels of relational embeddedness.
- H2: A start-up is more likely to exit via IPO if its VC investors have lower levels of relational embeddedness.

No third hypothesis is stated in the paper's text; the closure/failure models are introduced as additional analysis, although the table reporting them is headed "Hypothesis 3."

**Mechanism Process**
- IV(s): VC joint collaboration experience (relational embeddedness of the first-round VC syndicate, operationalized via a Newman (2001) tie-strength weighting of prior coinvestments); also decomposed into acquisition-specific and IPO-specific joint experience.
- DV(s): Type of start-up exit — acquisition exit (focused success), IPO exit (broadcast success), and, in additional analyses, closure/failure; modeled as competing-risks hazards.
- Mediators: None formally tested; theorized intervening processes are common interpretive schema, coordination efficiency, and knowledge diversity (argued, not directly measured).
- Moderators: Market-segment diversity of the VCs' other portfolio investments (the "best-of-both-worlds" interaction for IPO exits); exit-type-specific prior collaborative experience as a boundary condition.

The authors argue that higher relational embeddedness among a syndicate's VCs builds shared interpretive schema, trust, and coordination efficiencies that channel specialized, tacit knowledge into the start-up, positioning it for an acquisition—a focused success appraised by domain-specific experts. Lower embeddedness exposes the start-up to more diverse, nonredundant knowledge and broader social ties, encouraging strategies that appeal to multiple market segments and thus an IPO—a broadcast success determined by diverse appraisers and requiring complex coordination. The same diversity that aids broadcast success, however, can impair coordination, which is why less-embedded syndicates are also associated with higher start-up failure.

**Data & Measures**
- Design and data source: a single longitudinal observational study built from Crunchbase, a crowd-curated database launched in 2007 whose contributions are vetted by Crunchbase staff and triangulated against press releases, SEC filings, VentureSource and CB Insights; the authors supplemented it with hand-collected acquisition and IPO data checked against other sources. The raw extract covers 71,624 rounds of funding involving 42,027 new ventures and 20,142 investors between 1982 and July 2014.
- Analytic sample: restricted to U.S.-based start-ups (the primary context of Crunchbase's data collection) that received first-round funding from at least one VC firm and for which the locations of the firm and its VC investors are available; after dropping cases with missing data on the explanatory variables, the final analyzable sample is 10,879 start-ups. Within that sample, 1,689 (15.5%) experienced an acquisition exit, 317 (2.9%) an IPO exit, and 2,388 (21.9%) failed. The hazard models are estimated on start-up-day spells: n = 1,377,404 in the unweighted specifications and n = 1,453,668 under IPTW (n = 1,371,658 for the weighted closure model).
- Dependent variables: time from the first VC funding round to (a) an acquisition exit (focused success), (b) an IPO exit (broadcast success), and (c) closure/failure such as bankruptcy. Mean time-to-exit is 1,658 days (4.5 years, SD 1,409 days) for start-ups that went public, 1,237 days (3.4 years, SD 827 days) for those acquired, and 1,218 days (3.3 years) for those that failed. All 1,689 acquisition exits were screened against news reports and press releases using success criteria drawn from prior research (asset sales counted as unsuccessful; transaction value versus capital raised); 8.5% (144 of 1,689) were classified as possible "masked failures" and the main models were re-estimated dropping or recoding them.
- Independent variable — VC joint collaboration experience: the relational embeddedness of the start-up's first-round VC syndicate only (first-round investors are used because they bear the most risk and are most likely to guide the trajectory). A coinvestment tie exists when two of those VCs coinvested in at least one other firm within the five years prior to a given date. Tie strength follows Newman's (2001) weighting of one-mode projections of two-mode networks: S(A,B) is the sum of 1/(N_i - 1) across the m companies in which A and B coinvested before the focal firm, where N_i is investee i's total number of investors; the firm-level value C_j is the sum of those weights across all coinvestment dyads among start-up j's investors. Mean 2.153 (SD 13.565) at the first funding round and 8.747 (SD 39.781) at the final date of observation; the variable is standardized before estimation, so hazard coefficients are per standard deviation.
- Exit-type-specific independent variables: acquisition-specific joint experience (C_j,ACQ, computed over only those prior coinvestees that were eventually acquired) divided by total joint experience C_j, and IPO-specific joint experience (C_j,IPO) divided by C_j; the division is used to reduce artificial correlation and multicollinearity.
- Supplementary dependent variable (start-up strategy test): the Jaccard similarity between the focal start-up's set of market segments and the market segments of the firms it acquired, estimated by linear regression on the 1,692 sample start-ups that made at least one acquisition after their first VC round (R-squared = .206, Table 7).
- Controls: first-funding-year dummies; state dummies for the 10 states covering 92% of the sample; market-segment dummies for the 20 largest of 444 Crunchbase-created segments; the start-up's number of market segments, total number of VCs, years since founding, years between founding and first round, and number of funding rounds; total quarterly U.S. acquisitions and IPOs as "hot market" controls; and, at syndicate level, average VC centrality (lagged), average number of the VCs' other portfolio firms (lagged), the proportion of investors who are angels (lagged), the proportions of the VCs' other portfolio firms that went public, were acquired or failed (lagged), the proportion of VCs with other portfolio firms in the start-up's own market segment, and the market-segment diversity of the VCs' other portfolio firms (a Herfindahl-based index, 1 minus the sum of squared segment shares, scaled 0 to 1).
- Estimation and identification: competing-risks proportional-hazards models estimated separately for each exit type with the other two events treated as right-censored, following Katila and Shane (2005); the proportional-hazards assumption was checked by plotting Schoenfeld residuals. Selection is addressed twice over. First, a Heckman-style correction using Hallen's (2008) method: each real firm-syndicate pair is matched with 10 randomly chosen start-ups not funded by that syndicate to create simulated pairs, a first-stage probit on 84,027 start-up-syndicate pairs predicts whether a pair is real (instrument: average geographic distance between a start-up and its VC investors, where a one-standard-deviation decrease in distance raises the odds of investment by 43%, p < .001, and the first-stage F-statistic is 16.52), and the resulting inverse Mills ratio enters every hazard model. Second, inverse-probability-of-treatment weighting treats VCs' prior collaboration as a continuous treatment, with stabilized weights from GLM numerator and denominator models (n = 1,460,973) using seven blocks of mostly lagged confounders. The design remains observational: the paper states that the exclusion restriction for its instrument cannot be explicitly tested, urges readers to interpret the results cautiously, and presents IPTW as constructing a pseudo-population in which the measured confounders no longer predict selection into treatment.

**Key Findings**
- H1 supported. Each one-standard-deviation increase in the first-round syndicate's joint collaboration experience raises the hazard of an acquisition exit by 6% (exp(0.054) = 1.055; b = 0.054, 95% CI [0.028, 0.080], p = 0.013; Table 5, Model 1). The effect persists with a similar magnitude when confounders are added (b = 0.050, CI [0.018, 0.082], p = 0.016; Model 2) and under IPTW estimation (b = 0.042, p = 0.015; Model 3).
- H2 supported. A one-standard-deviation decrease in joint collaboration experience raises the hazard of an IPO exit by 37% (hazard ratio 1.373; b = -0.317, CI [-0.611, -0.023], p = 0.016; Table 5, Model 4). The effect is robust to including confounders (b = -0.297, p = 0.012; Model 5), though the authors note its strength diminishes noticeably under the treatment weights (b = -0.209, CI [-0.561, -0.033], p = 0.018; Model 6). It holds while controlling for the market-segment diversity of the syndicate's other investments, which the authors read as evidence that the nonredundant knowledge brought by VCs without prior collaborative experience outweighs the knowledge diversity captured in segment-specific expertise.
- Failure, examined as additional analysis rather than a stated hypothesis. Less shared collaborative experience significantly increases the hazard of closure: a one-standard-deviation reduction more than doubles it (hazard ratio 2.144; b = -0.763, CI [-1.201, -0.325], p = 0.000; Table 6, Model 1), and the coefficient stays negative with confounders (b = -0.693) and under IPTW (b = -0.580). Supplemental analysis shows time-to-failure is shorter for start-ups funded by less embedded VCs. The authors treat this as an unexpected trade-off: lower embeddedness raises the chances of an IPO but also of failure before any successful equity exit.
- Strategy evidence consistent with the theorized mechanism. Among the 1,692 start-ups that made acquisitions, greater VC prior collaboration is positively associated with the market-segment similarity between the focal start-up and the firms it acquires (b = 0.023, CI [0.003, 0.043], p = 0.009; Table 7), indicating that start-ups backed by more embedded syndicates concentrate on their existing segments rather than branching out.
- Boundary condition: exit-type-specific experience. A one-standard-deviation increase in acquisition-specific joint experience raises the hazard of being acquired by 4% (exp(0.038) = 1.039; b = 0.038, CI [0.012, 0.064], p = 0.001; Table 8, Model 1), an effect that is almost identical under IPTW (b = 0.038, CI [0.010, 0.066], p = 0.003; Model 3) but weakens to non-significance when confounders are included without weighting (b = 0.012, CI [-0.034, 0.058], p = 0.298; Model 2) — so this particular effect is only partially robust across specifications. A one-standard-deviation increase in IPO-specific joint experience raises the hazard of an IPO exit by 12% (exp(0.110) = 1.116; b = 0.110, CI [0.022, 0.198], p = 0.006; Table 8, Model 4), largely holding in magnitude with confounders (b = 0.085, CI [0.011, 0.159], p = 0.010; Model 5) and treatment weights (b = 0.111; Model 6). Cross-wise, IPO-specific experience is consistently negatively related to the hazard of an acquisition exit, and acquisition-specific experience consistently negatively related to the hazard of an IPO exit — the benefit of a syndicate's collaborative experience is conditional on its matching the exit type the start-up seeks.
- "Best-of-both-worlds" moderation, in unreported models. Interacting VC joint experience with the market-segment diversity of the VCs' other investments yielded evidence of the best-of-both-worlds effect for IPO exits (greater joint experience aiding coordination while diverse prior investment experience supplies breadth), but no evidence of an interaction effect for acquisition exits, which the authors attribute to acquisitions being appraised mainly by industry insiders and so not requiring diverse market experience.
- Descriptive pattern and robustness. Acquired firms' first-round VCs had greater average joint collaborative experience (mean 2.95) than those of firms that went public (mean 1.20) or failed (mean 2.36). Among VCs in the top quartile of syndicate relational embeddedness 4.0% of portfolio start-ups went public, and among those in the lowest quartile 12.6% were acquired, which the authors read as evidence that whether a VC prefers high- or low-embeddedness syndicates does not by itself reveal an ex ante exit preference. Results were not substantially altered by adding a quadratic term (no improvement in model fit for either outcome), by omitting firms whose VCs' shared collaborative values exceeded the 95th percentile, by including later-round VC investors, by coinvestment windows ranging from two to 10 years, by analyzing only the subsample of firms that received their first round of funding prior to 2007, or by dropping or recoding the 144 possible masked-failure acquisitions.

**Theoretical Contribution**
The paper offers a resolution to the "paradox of embeddedness" by reframing it as a contingency on the type of collective success: rather than embeddedness being uniformly beneficial or harmful, higher embeddedness promotes focused successes while lower embeddedness promotes broadcast successes. It introduces a typology of focused versus broadcast success distinguished by their appraisers, complexity, and prominence, and extends entrepreneurship research by treating investors' prior collaborative experience—and the distinction between exit pathways—as an underappreciated driver of start-up outcomes rather than collapsing exits into a single performance variable.

**Practical Implication**
Founders can read a prospective VC's relational embeddedness (its history of coinvestment partners and exit types) as a signal of the likely path ahead: highly embedded, acquisition-oriented syndicates suit founders aiming to be acquired, whereas a more diverse, less-embedded investor set better supports an IPO ambition—though at higher risk of failure. VCs seeking more IPO "home runs" might deliberately diversify their coinvestors, while those seeking steady acquisition returns might embed in a stable network of like-minded co-investors.

**Limitations**
The measure of collaborative experience captures only first-round investors, omitting later-round investors who also shape trajectories. The study cannot observe how VC partners and founders reach consensus on which exit to pursue, nor does it measure the financial value (acquisition premiums, IPO pricing) created by exited firms. As a macro-level study, it theorizes cognitive mechanisms (identity, coordination, shared interpretive schema) that are not directly observed in the data, and the exclusion restriction for its instrument cannot be explicitly tested.

**Future Research**
Future work could measure ultimate financial returns using acquisition premiums and IPO pricing as outcomes, and examine settings where different types of success are tightly coupled or nonexclusive (e.g., dissertation-committee placements, critical-acclaim-plus-box-office collaborations) rather than mutually exclusive. Micro-level experimental research could better isolate how cognitive factors such as identity and shared schema drive different kinds of success, and further studies could probe how network structure interacts with informational context across diverse appraisal environments.

**APA 7th Citation**
Wang, D., Cox Pahnke, E., & McDonald, R. M. (2022). The past is prologue? Venture-capital syndicates’ collaborative experience and start-up exits. *Academy of Management Journal*, 65(2), 371–402. https://doi.org/10.5465/amj.2019.1312
