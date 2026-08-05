---
id: amj-vol-62-no-3-kumar-2019
title: "Ego-Network Stability and Innovation in Alliances"
authors:
  - "Kumar, Pankaj"
  - "Zaheer, Akbar"
year: 2019
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2016.0819"
volume: 62
issue: 3
pages: "691-716"

source: "AMJ/vol-62-no-3"
pdf_path: "library/AMJ/vol-62-no-3/pdfs/Kumar 2019 Ego-Network Stability and Innovation in Alliances.pdf"
text_path: "library/AMJ/vol-62-no-3/text/Kumar 2019 Ego-Network Stability and Innovation in Alliances.txt"
ingested_at: "2026-06-29"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-08-05"

paper_type: "empirical-quantitative"
keywords: ["ego network configurations", "network closure", "structural holes", "ego-network stability", "innovation", "alliance portfolios", "geographic concentration", "biopharmaceutical firms"]
theory: ["social resource theory (Lin, 1982, 1990)", "network resource theory (Gulati, 2007)", "structural holes theory (Burt, 1992)", "network closure (Coleman, 1990)"]
topics: ["strategy-innovation", "innovation-management", "longitudinal", "north-america"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Empirical quantitative panel study of U.S. pharmaceutical firms' alliance ego networks. The authors construct annual alliance-network measures, measure innovation with citation-weighted patent counts net of self-citations, and estimate Poisson fixed-effects unconditional quasi-maximum likelihood models with firm and year fixed effects plus robustness tests."
sample:
  industry: "Pharmaceutical and biopharmaceutical firms, restricted to pharmaceutical-domain alliances and pharmaceutical patents."
  country: "United States"
  time_period: "1985-2005 for alliance/network observations, with patent data observed through 2010 to reduce right-censoring."
  units: "U.S. pharmaceutical firm-year observations for firms with at least two direct alliance ties."
  n: "198 U.S. pharmaceutical firms and 1,236 firm-year observations."

evidence:
  sample_n: "unbalanced panel of 198 U.S. pharmaceutical firms"
  sample_country: "198 U.S. pharmaceutical firms"
  sample_industry: "biopharmaceutical firms"
  sample_time_period: "from 1985 to 2005"
  theories_overview: "social resource theory"
  methods_overview: "Poisson fixed-effects"
  keywords_source: "firms’ ego network configurations—i.e., structural holes"
  hypotheses_source: "Hypothesis 1 states that network stability negatively"
  measures_overview: "network stability in year t2 is the percentage of ties"
  findings_overview: "Focal firms can limit the negative effects of ego-network stability on innovation by spanning structural holes in their alliance portfolios"
---

# Ego-Network Stability and Innovation in Alliances

**Abstract**
Much research has shown that firms’ ego network configurations—i.e., structural holes or network closure—help them achieve superior innovation outcomes. However, little is known about how the stability of the firm’s ego-network composition affects the firm’s innovation. In this paper, we investigate the outcomes of ego-network stability in an alliance context, arguing that stability actually reduces innovation for the focal firm. We further investigate two contingencies—namely, the structural holes the focal firm spans and the geographic concentration of its inventive activities—that moderate the detrimental innovation effects of ego network stability. Focal firms can limit the negative effects of ego-network stability on innovation by spanning structural holes in their alliance portfolios, whereas the negative effects are worsened when the focal firms’ inventive activities are geographically concentrated in a single country. We empirically test our hypotheses using 198 biopharmaceutical firms headquartered in the United States over a 21-year period from 1985 to 2005. Our results support our predictions.

**Research Question**
The paper asks how stability in a firm's alliance ego-network composition affects the focal firm's innovation performance. It also asks whether spanning structural holes mitigates the innovation penalty of stability and whether geographic concentration of inventive activities aggravates that penalty.

**Hypotheses / Propositions**
- H1: Greater ego-network stability of a focal firm is associated with reduced innovation performance for the focal firm.
- H2: The greater the spanning of structural holes by a focal firm, the less negative the relationship between ego-network stability and the focal firm's innovation performance.
- H3: The greater the geographic concentration of a focal firm's inventive activities, the more negative the relationship between ego-network stability and the focal firm's innovation performance.

**Mechanism Process**
- IV(s): Ego-network stability, defined as the percentage of alliance ties that stay the same from one year to the next.
- DV(s): Citation-weighted patent count net of self-citations.
- Mediators: Knowledge diversity, knowledge redundancy, and relational lock-in are theorized mechanisms but are not modeled as measured mediators.
- Moderators: Structural holes in the focal firm's alliance network; geographic concentration of the focal firm's inventive activities.

The mechanism is that repeated alliance partners initially provide useful social resources, but over time the knowledge accessible through the same partners becomes less diverse, more redundant, and more prone to lock-in. Because R&D alliances in fast-moving pharmaceutical contexts rely on changing knowledge requirements, stable partner composition can reduce the focal firm's exposure to novel recombinations. Structural holes soften this negative effect by giving the focal firm access to more diverse and less redundant partner information, whereas geographically concentrated inventive activity worsens it by limiting the firm's access to dispersed knowledge sources.

**Data & Measures**
Alliance data come from SDC Platinum, from which the authors selected all firms in the global pharmaceutical industry (SICs 2833 through 2836), both public and private, that participated in alliances announced from 1980 through 2005, augmented by an archival search of SEC-EDGAR, LexisNexis, Factiva, and Bloomberg. Because the majority of the alliances are open-ended, the authors hand-collected a deal database from SEC-EDGAR, LexisNexis, Factiva, Bloomberg Professional Terminal, Mergent Online, news and trade sources, and company websites, and applied a five-stage cascading search for alliance termination dates so that observed alliance durations, rather than the five-year rolling-window assumption used in prior work, determine when a tie exists. The network boundary requires each pharmaceutical firm to have an alliance with another pharmaceutical firm and each alliance itself to be in the pharmaceutical domain; subsidiaries, joint ventures, spinoffs (50% or more ownership), and business units are aggregated to the ultimate parent. Restricting attention to firms with at least two direct ties yields 208 U.S. firms and 1,379 firm-year observations; after matching to the patent data the final usable sample is an unbalanced panel of 198 U.S. pharmaceutical firms with 1,236 firm-year observations. Patent data were collected from the U.S. Patent and Trademarks Office, the NBER U.S. Patent Citations Data File, the Harvard U.S. Patent Inventor Database, and Kogan, Papanikolaou, Seru and Stoffman's (2012) dataset through November 2014 to reduce right-censoring bias, with the 2008 OTAF 283 concordance used to convert four-digit SIC codes into pharmaceutical technology classes; the last year of observation for the dependent variable is 2010, against a patent grant lag of roughly three to four years.
- DV: Citation-weighted patent count net of self-citations, computed as the sum over granted patents applied for in a five-year window (t + 1 to t + 5) of one plus the patent's total citations, net of self-citations.
- IV: Stability = 1 - Churn, where churn is (ties added + ties lost) divided by the firm's total number of unique ties during the period, so stability is the percentage of ties that stay the same from one year to the next; a firm entering the sample for the first time is assigned a stability score of 1.
- Moderator: Structural holes = 1 - the aggregate Burt (1992) constraint faced by the focal firm, using Zaheer and Bell's (2005) transformation, where a high score indicates exclusive access to alter firms.
- Moderator: Geographic concentration = a Herfindahl-Hirschman Index of the focal firm's inventive activities built from inventor country locations on its patents, where an index value of 1 indicates research concentrated in a single country; firms with missing inventor locations were assigned a score of 1.
- Controls: direct ties, indirect ties, technological opportunity, technological base (log), technological diversity of the focal firm and of its alliance partners, technological distance (cosine), industry similarity, partners' innovation value, equity alliances (% of total), cross-border participants (% of total), knowledge alliances (% of total), cumulative alliance experience, average age of alliances, an acquiror dummy, mergers and acquisitions stock (log), and status (Bonacich centrality).

Because the dependent variable is a nonnegative count and 15% of the count data are 0, the authors estimate a Poisson fixed-effects unconditional quasi-maximum likelihood model with firm and year fixed effects and cluster-robust standard errors, mean-centering Stability, Structural holes, and Geographic concentration to eliminate nonessential multicollinearity (mean VIF 7.72). The design is an observational firm-year panel rather than an experiment or quasi-experiment: the fixed-effects specification absorbs time-invariant unobserved firm heterogeneity in the predisposition to patent, and the authors separately run a control function approach for the Poisson fixed-effects estimator, instrumenting Structural holes with focal-firm innovation uncertainty (the standard deviation of a rolling five-year window of patent counts) and its product with Stability, to test whether Structural holes is endogenous.

**Key Findings**
Hypothesis 1 is supported. Stability has negative and significant coefficient estimates in Models 2, 3, 4, and 5 of Table 2 (Model 5: b = -0.29, p < .01), and the predicted-count plot shows that Stability has a negative, but diminishing, and significant (p < .05) impact on the predicted mean counts. At the mean, Stability reduces the conditional mean count of citation-weighted patents by 3.87 (p < .01), and the mean count reduces by 1.96 when Stability increases from the 10th to the 90th percentile (chi-square = 8.49; p < .01). Hypothesis 2 is, in the authors' own wording, largely supported: the interaction between Stability and Structural holes is positive and significant in Model 3 (b = 1.36, p < .01), but positive and only marginally significant in the fully specified Model 5 (b = 0.85, p < .10); the interaction plot shows the negative effect of stability on predicted patent counts is more detrimental to a focal firm with few structural holes than to one with many. Hypothesis 3 is supported: Models 4 and 5 show a negative and significant interaction between Stability and Geographic concentration (Model 4: b = -1.59; Model 5: b = -1.25; p < .05), and the effect of stability on predicted citation-weighted patent counts becomes more negative as the focal firm's network gets more highly geographically concentrated. Both moderators also carry significant main effects: Structural holes is positive and significant in Models 2 through 5 (p < .05; Model 5: b = 0.93), with a marginal effect at the sample mean of 12.43 citation-weighted patent counts net of self-citations (p < .05) and an increase of 4.63 as Structural holes moves from the 10th to the 90th percentile (chi-square = 5.27; p < .05), while Geographic concentration is negative and significant in Models 2 through 5 (p < .05; Model 5: b = -0.81), with a marginal effect at the sample mean of -10.84 (p < .05) and a decrease of 2.27 as it moves from the 10th to the 90th percentile (chi-square = 5.65; p < .05). All five Table 2 models are estimated on 1,236 firm-years and 198 firms.

The results are reported as robust to alternative dependent variables, including patents alone, citations alone (net of self-citations), and a 10-year forward-citation window, in which Stability again displays the expected negative relationship (b = -0.18, p < .05), the Stability by Structural holes interaction shows a positive effect (b = 0.99, p < .10), and the Stability by Geographic concentration interaction is consistent with the principal results (b = -1.36, p < .01). Coefficient estimates and their significance for the main variables of interest are essentially unchanged under a Poisson-gamma random-effects estimator (Model 6). In the conditionally correlated Poisson-gamma random-effects dynamic model (Model 7), the coefficient for Geographic concentration is not significant, though it is negative as hypothesized, while Structural holes (p < .05), Stability (p < .01), the interaction between Structural holes and Stability (p < .05), and the interaction between Geographic concentration and Stability (p < .10) have the same signs as in Model 5. The control function approach (Model 8) cannot reject the null hypothesis of exogeneity of Structural holes (robust Wald chi-square = 1.49; p = .22). A test of whether the stability-innovation relationship is quadratic does not reject linearity: the quadratic term is positive, indicating a possible U shape, but is not significant (p = .29), and the overall U-shape test is not significant (p = .33).

**Theoretical Contribution**
The paper adds a compositional lens to network research by showing that ego-network stability matters beyond the usual configuration lens of structural holes versus closure. It argues that network structures cannot be evaluated only by their degree of openness because the continuity or churn of the partner set can independently shape innovation outcomes.

It also extends social resource and network resource perspectives by emphasizing that the value of network resources depends on whether partners continue to provide nonredundant knowledge over time. The study therefore reframes stability, often treated as a foundation for social capital, as potentially detrimental in innovation-intensive alliance settings.

**Practical Implication**
Managers using alliances for innovation should monitor not only the number and structure of alliance ties but also whether the partner portfolio is becoming stale. The results imply that refreshing partners, spanning structural holes, and maintaining geographically dispersed inventive activity may help reduce the innovation costs of excessive network stability.

The paper also suggests that persistent open-ended alliances are not automatically beneficial for innovation. When alliance persistence is difficult to avoid, managers may be able to limit its negative consequences through more open ego-network structures and broader geographic access to knowledge.

**Limitations**
The empirical setting is the biopharmaceutical industry, so the authors expect the findings to generalize most clearly to industries where innovation is salient and alliances are used for innovation-related purposes. In industries where innovation is less critical or alliances serve other goals, network stability may not produce the same negative effects.

The authors also exclude isolates and pendants because stability and structural holes are not meaningfully defined for firms with zero or one alliance tie. In addition, the analysis treats relevant innovation knowledge as potentially coming from any alliance type, even though future work could distinguish upstream research alliances from downstream commercialization alliances.

**Future Research**
Future research could examine how ego-network stability affects innovation at other levels, including individual scientists, and could study the antecedents of ego-network stability itself. The authors also call for work on how local ego-network stability shapes global network properties such as small-worldliness, connectivity, and centrality.

Another opportunity is to classify alliance networks by value-chain activity and test whether stability has different innovation effects in upstream versus downstream relationships. Future studies could also examine the trade-off between the cost of changing network partners and the declining innovation value of stable partner portfolios.

**APA 7th Citation**
Kumar, P., & Zaheer, A. (2019). Ego-network stability and innovation in alliances. *Academy of Management Journal*, 62(3), 691-716. https://doi.org/10.5465/amj.2016.0819
