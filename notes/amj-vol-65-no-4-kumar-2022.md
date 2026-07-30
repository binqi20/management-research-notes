---
id: amj-vol-65-no-4-kumar-2022
title: "Network Stability: The Role of Geography and Brokerage Structure Inequity"
authors:
  - "Kumar, Pankaj"
  - "Zaheer, Akbar"
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2020.0903"
volume: 65
issue: 4
pages: "1139-1168"

source: "AMJ/vol-65-no-4"
pdf_path: "library/AMJ/vol-65-no-4/pdfs/Kumar 2022 Network Stability The Role of Geography and Brokerage Structure Inequity.pdf"
text_path: "library/AMJ/vol-65-no-4/text/Kumar 2022 Network Stability The Role of Geography and Brokerage Structure Inequity.txt"
ingested_at: "2026-06-23"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["brokerage stability", "structural holes", "structural inequity", "knowledge recombination", "geographic distance", "interfirm alliances", "network decay"]
theory: ["structural hole theory (Burt, 1992)", "equity theory / inequity aversion (Fehr & Schmidt, 1999; Cook & Emerson, 1978)", "cognitive categorization of rivals (Porac et al., 1995)"]
topics: ["competitive-strategy", "ecosystems-platforms", "social-capital-theory"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "na"
methods: "Discrete-time survival analysis of non-repeated events (brokerage triad decay) using a complementary log-log estimator on a 21-year unbalanced panel; robustness via Weibull, frailty, PPML with high-dimensional fixed effects, and two-stage Heckman selection corrections."
sample:
  industry: "Global biopharmaceutical industry (SICs 2833-2836)"
  country: "Global (firms geocoded by latitude/longitude worldwide)"
  time_period: "1985-2005"
  units: "Brokerage alliance triads (broker-alter-alter); 14,829 unique triads"
  n: "53,377 triad-year observations, 260 broker firms and 517 alter firms"

evidence:
  sample_n: "260 broker and 517 alter firms in the global biopharmaceutical"
  sample_country: "260 broker and 517 alter firms in the global biopharmaceutical"
  sample_industry: "global biopharmaceutical industry set"
  sample_time_period: "517 alter firms from 1985 to 2005."
  theories_overview: "structurally induced “inequity” in opportunity"
  methods_overview: "complementary log-log discrete time survival model"
  keywords_source: "brokerage structures persist or decay"
  hypotheses_source: "Hypothesis 1 (H1). Conditional on its formation, a"
  measures_overview: "coded brokerage inequity deriving from a triad as 0 if"
  findings_overview: "knowledge recombination opportunity is positive and significant (p , 0.01)"
---

# Network Stability: The Role of Geography and Brokerage Structure Inequity

**Abstract**
While the outcomes of brokerage have been extensively investigated, the issue of when and why brokerage structures persist or decay has attracted relatively little research interest. Taking the perspective of the disconnected firms to whom the broker is tied, the "alters," we argue that structurally induced "inequity" in opportunity, or the broker's potential recombination of a larger share of alters' knowledge than vice versa, exerts a destabilizing effect on brokerage persistence. Furthermore, geographic distance, via its role in the cognitive classification of rivals, enhances alters' tolerance for inequity and contingently weakens the destabilizing effect of structural inequity in knowledge recombination opportunity that benefits the broker. Specifically, we postulate about the sociocognitive prismatic nature of geography in that geographic distance makes it less likely that alter firms see the broker as a rival and are hence less sensitive to inequity. We test our hypotheses with 260 broker and 517 alter firms in the global biopharmaceutical industry from 1985 to 2005, yielding 53,377 triad-year observations using a complementary log-log discrete time survival estimator. Our results support the hypotheses, highlighting the interplay between structural inequity and geographic distance in explaining brokerage decay.

**Research Question**
How does brokerage structure inequity affect the stability of brokerage triads, and how does geographic distance contingently influence the effects of structural inequity on the stability of brokerage triads?

**Hypotheses / Propositions**
- H1: Conditional on its formation, a brokerage triad is more likely to decay, and therefore exhibit less stability, in the presence of brokerage structure inequity in knowledge recombination opportunities (positive effect of inequity on the decay hazard).
- H2: Conditional on its formation, a brokerage triad is less likely to decay, and therefore exhibit greater stability, when a broker firm with knowledge recombination opportunities is geographically distant from its two alter firms than when the broker firm with knowledge recombination opportunities is geographically proximate to them (negative interaction: distance weakens the destabilizing effect of inequity).

**Mechanism Process**
- IV(s): Brokerage structure inequity in knowledge recombination opportunity (the broker's disproportionate ability to recombine a larger share of alters' knowledge than vice versa, coded 0-3 from cross-citation patterns).
- DV(s): Brokerage triad decay/instability (hazard of the triad ceasing to be a stable open structural hole).
- Moderators: Broker-alter geographic distance (great-circle distance in thousand miles).
- Controls: Alter-alter and broker-alter knowledge/status/size/patent differences, past ties, ease of recombination, same-country and same-SIC dyads, broker's lack of constraint; broker, broker-industry, and broker-country fixed effects.

Alters perceive the structural inequity in knowledge recombination opportunity favoring the broker as an unfair "cost," which provides motivation to terminate the tie and thereby destabilizes the brokerage triad (H1, supported: hazard ratio 1.12). Geographic distance operates as a sociocognitive prism: when the broker is geographically distant, alters are less likely to cognitively categorize it as a rival and become more tolerant of inequity, attenuating the destabilizing effect and prolonging brokerage (H2, supported: negative interaction).

**Data & Measures**
Single-study observational panel; the paper reports one dataset and no separate studies. Alliances were drawn from the Thomson Reuters SDC Platinum database (public and private firms with at least one alliance announced between 1980 and 2005 in the global pharmaceutical industry, SICs 2833-2836), supplemented with Factiva, LexisNexis, SEC-EDGAR, Bloomberg Professional Terminal, Mergent Online, trade magazines, news services, and company websites; alliance end dates were hand-collected through a five-stage search strategy. Patent-based measures use Kogan, Papanikolaou, Seru, and Stoffman's (2012) patent data set, Lai and colleagues' (2011) Harvard patent data set, Hall, Jaffe, and Trajtenberg's (2001) NBER patent citations data set, and USPTO patent and citation data. Firm latitudes and longitudes were retrieved from exact addresses via the Google Geocoding API, with manual coding where the API returned only country-level coordinates. The final sample with complete information on the independent variables is 14,829 unique brokerage triads and 53,377 triad-year observations involving 260 broker firms and 517 alter firms from 1985 to 2005, described in the Table 1 note as a 21-year unbalanced panel; the Table 2 estimation sample is 53,093 observations.
- DV: Decay, a dummy coded 0 in the triad's first observed year and in each subsequent year the triad reappears with no change in composition or relationships, and 1 for the year in which the triad status quo changes and brokerage decays. The paper reports that the estimation sample has 85.97% decay cases (12,749 events), which motivates the asymmetric complementary log-log link.
- IV: Brokerage structure inequity in knowledge recombination opportunity, a triad-level index running from 0 to 3, built in two steps from patent cross-citations over a rolling five-year window up to year t. Step 1 assigns 1 to each broker-alter dyad in which the broker's citations to the alter, normalized by the broker's total citations net of self-citations, exceed the alter's correspondingly normalized citations to the broker (adapting Mowery, Oxley, and Silverman's 1996 cross-citation rate measure), and 0 otherwise. Step 2 assigns 1 if the broker cited both alter firms in a single patent. The final measure sums the two steps: 0 when the broker neither out-recombines either alter nor recombines both alters' knowledge, and 3 when it out-recombines both alters and also recombines their knowledge in a single patent.
- Moderator: Broker-alter geographic distance (in thousand miles), the great-circle distance from the spherical law of cosines (earth radius R = 3,956.54 miles) between the broker's and each alter's alliance-relevant location at time t, averaged across the two broker-alter distances and divided by 1,000.
- Controls: alter-alter past ties, alter-alter knowledge difference (Jaccard coefficient over pharmaceutical patent subclasses), alter-alter status difference (normalized Bonacich centralities), and alter-alter geographic distance; broker-alter differences in past ties, status, knowledge, self-knowledge use, foreign-knowledge use, scientific linkage, patent quality, patent claims, multiple-partner alliances, alliance stability, alliance scope, and size (employees); ease of recombination of complementary technological niches; number of same-country dyads and number of same-SIC dyads (each 0 to 3); and the broker's lack of constraint (Burt's 1992 constraint measure with Zaheer and Bell's 2005 transformation).

Estimation in the paper's own terms: a discrete-time survival model for non-repeated events with a complementary log-log link, chosen because survival time is observed only in yearly intervals, multiple terminations occur within a year, and the outcome distribution is highly skewed; the specification includes survival time period dummies, country and industry dummies, and broker fixed effects, with cluster-robust standard errors and two-tailed tests. The design is associational rather than experimental, with no randomization or exogenous shock. Endogeneity concerns are addressed by lagging all independent variables and controls by one year to reduce simultaneity; by broker, broker-industry, and broker-country fixed effects; by a frailty specification with a normally distributed random error; and by two Heckman-style two-stage corrections using Lee's (1983) generalized inverse Mills ratio, one for self-selection into the broker position (excluded instruments: broker incidence, and social and historical aspiration-based innovativeness) and one for self-selection into geographic distance (excluded instrument: the average alliance distance spanned by all other firms in the focal firm's state, or country for non-U.S. firms, in year t). Nonindependence is handled with cluster-specific fixed effects, multiway clustering, and a Poisson pseudo-maximum likelihood estimator with multiway high-dimensional fixed effects.

**Key Findings**
Single study and single estimation sample; both hypotheses are supported in the full model (Model 3 of Table 2).
- H1 supported. The coefficient on Brokerage structure inequity in knowledge recombination opportunity is positive and significant (b = 0.11, SE = 0.03, p < .01). The corresponding hazard ratio is 1.12: the hazard of brokerage decay is 12.01% higher when inequity increases by one unit from zero, with broker-alter geographic distance at zero and other variables held constant. Structural inequity therefore destabilizes brokerage.
- H2 supported. The interaction between Brokerage structure inequity in knowledge recombination opportunity and Broker-alter geographic distance is negative and significant (b = -0.03, SE = 0.01, p < .01), with a multiplicative interaction of 0.97, meaning the hazard ratio for inequity at a broker-alter distance one unit (1,000 miles) higher is 0.97 times the hazard ratio at zero distance. Figure 2 shows that the positive effect of inequity on the hazard of decay is less detrimental for brokerage with high broker-alter geographic distance than for brokerage with low distance, so distance attenuates rather than reverses the destabilizing effect.
- Geographic distance also has a negative and significant main effect (b = -0.04, SE = 0.01, p < .01), hazard ratio 0.96, which the paper glosses as the hazard of decay being 0.96 times lower, or 3.64% lower, per additional 1,000 miles from zero when inequity is zero; distance thus enhances stability across its observed range.
- Robustness. The results hold under a Weibull estimator (Model 4) and a frailty specification (Model 5); under two-stage selection corrections for the broker position (Model 6, n = 40,478) and for geographic distance (Model 7, n = 53,093); and under a Poisson pseudo-maximum likelihood estimator, including five-way fixed effects (Model 9) and two-way dyadic fixed effects with three-way clustering (Model 10). An alternative continuous inequity measure and mean-centering the main predictors left the findings unchanged. When both selection corrections are included together the results still hold, though the coefficient on the geography selection correction becomes insignificant. The Altonji, Elder, and Taber (2005) ratio is 2.24, which the authors read as making it unlikely that unobservables explain the geographic-distance effect on brokerage decay.
- Post hoc evidence on alter agency: a one-standard-deviation increase in the probability of brokerage decay attributable to the interplay of inequity and geography raises the likelihood of an alter increasing its structural hole spanning by 3.5%, which the authors interpret as a possible broker-substitution effect. They also note that when the broker is at the losing end of the recombination asymmetry, that is, when inequity is zero or close to zero, brokerage persists.

**Theoretical Contribution**
The paper extends structural hole theory by shifting from a broker-centric to an altercentric account of network persistence, locating the source of brokerage decay in alters' perceived structural inequity in knowledge recombination opportunity rather than alter-alter rivalry. Alongside existing theorizing about the "shadow of others," which emphasizes common alters in the persistence of network structures, the paper highlights the distinct influence of the "shadow of the broker" on alters in explaining network stability. It further introduces geography as a sociocognitive moderator, showing that spatial distance heterogeneously alters alters' tolerance for inequity through rival categorization, thereby integrating the spatial embeddedness of ties into theories of network evolution and decay.

**Practical Implication**
Broker firms seeking to sustain advantageous brokerage positions are better off forming spatially distant ties and using frequent communication and procedurally fair alliance-management policies to manage geographically proximate, more rivalrous relationships. Alter-firm managers who wish to strengthen their bargaining position should make their distant collaborations more visible internally to stay alert to brokerage benefits they may be ceding.

**Limitations**
Brokerage in a knowledge-intensive industry may differ in degree from non-knowledge-based contexts, potentially weakening the theorizing there. The study captures "what opportunity a broker has" but data limitations preclude directly testing "how the broker behaves," and the authors cannot observe precisely which triad partner initiated termination, relying instead on theorized and post hoc proxies for alter agency.

**Future Research**
Future work could test the broker-behavior boundary condition, explore how structurally equivalent alters or status- and proximity-based reference groups shape inequity perceptions and referent-discrepancy effects, and examine different decay outcomes (tie disintegration, disintermediation, closure) to distinguish their antecedents and consequences.

**APA 7th Citation**
Kumar, P., & Zaheer, A. (2022). Network stability: The role of geography and brokerage structure inequity. *Academy of Management Journal*, 65(4), 1139-1168. https://doi.org/10.5465/amj.2020.0903
