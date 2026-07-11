---
id: amj-vol-68-no-3-br-ndle-2024
title: "Crossing Technological Boundaries: Brokerage and the Emergence of Innovation Networks"
authors:
  - "Brändle, L."
  - "Berger, E. S. C."
  - "Howard, M. D."
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0439"
volume: 68
issue: 3
pages: "620-647"

source: "AMJ/vol-68-no-3"
pdf_path: "library/AMJ/vol-68-no-3/pdfs/Brändle 2024 Crossing Technological Boundaries Brokerage and the Emergence of Innovation Networks.pdf"
text_path: "library/AMJ/vol-68-no-3/text/Brändle 2024 Crossing Technological Boundaries Brokerage and the Emergence of Innovation Networks.txt"
ingested_at: "2026-04-30"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-11"

paper_type: "empirical-mixed"
keywords: ["brokerage", "tertius iungens", "tertius gaudens", "triadic closure", "multiplex technology closure", "innovation networks", "emergent technology", "incumbent technology", "monoclonal antibodies", "small molecules", "R&D alliances", "stochastic actor-oriented models"]
theory: ["tertius iungens (Obstfeld)", "tertius gaudens (Simmel)", "structural holes / brokerage theory (Burt)", "Gould and Fernandez brokerage roles", "triadic closure / network dynamics theory", "knowledge brokering"]
topics: ["innovation-management", "ecosystems-platforms", "dynamic-capabilities"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Mixed-methods design, dominantly quantitative. Quantitative core: longitudinal stochastic actor-oriented models (SAOMs) estimated in RSiena on a multivariate two-network panel (mAbs and small-molecule R&D alliance networks) of 453 cancer-therapy firms over 2004-2020 (17 yearly waves), modeling tie formation as the dependent variable with directed ties from client to R&D firm; tests of within-network uniplex closure (GWDSP), cross-network multiplex closure (WW->X), and a 'jumpWWClosure' term capturing mAbs-expertise asymmetric boundary-spanning closure; goodness-of-fit via sienaGOF (Mahalanobis distance) on indegree, outdegree, and triad-census distributions; rare-events logistic regression (King & Zeng 2001) on a 1.18M dyad-year panel as robustness; sienaCompositionChange to handle entry/exit; controls drawn from BioSciDB, USPTO patent records (CPC codes), FDA approvals, geocoded headquarters distance. Qualitative supplement: 14 in-depth interviews with scientists, big-pharma managers, biotech start-ups, regulators, and industry experts (9 informing context/hypotheses; 5 post-results sensemaking)."
sample:
  industry: "Biopharmaceutical / cancer therapy R&D alliances; specifically incumbent small-molecule (chemistry-based) and emergent monoclonal-antibody (mAbs) targeted-therapy technologies, with related modalities such as gene therapy"
  country: "Not reported in paper"
  time_period: "2004-2020 (17-year network observation window); 14 interviews with industry experts conducted around the study"
  units: "Interfirm directed R&D alliance ties (client to R&D firm) constituting two co-evolving technology networks (mAbs emergent and small-molecule incumbent)"
  n: "453 firms; alliance counts grow from 45 mAbs/50 small-molecule ties in 2004 to peaks of 131 mAbs (2016) and 106 small-molecule (2015); 1.18 million dyad-year observations in robustness logistic regression; 14 expert interviews"

evidence:
  sample_n: "Note: Total sample nodes: 453."
  sample_country: "Not reported in paper"
  sample_industry: "in the cancer therapy industry, all experts concurred"
  sample_time_period: "during the study period of 2004 to 2020"
  theories_overview: "(i.e., tertius iungens), they might have competitive incentives to prevent such connections (i.e., tertius gaudens)."
  methods_overview: "stochastic actor-oriented modeling by examining the"
  keywords_source: "different technology networks (i.e., multiplex technology closure)."
  hypotheses_source: "Hypothesis 2. Two firms are more likely to form an emerging technology alliance if they share a common"
  measures_overview: "In our networks, ties point from the client"
  findings_overview: "coefficient that is positive and significant (b 5 2.209,"
---

# Crossing Technological Boundaries: Brokerage and the Emergence of Innovation Networks

**Abstract**
Firms face elevated levels of uncertainty in collaborations focused on new technologies. While third parties may foster such collaborations by reducing technological and relational uncertainties (i.e., tertius iungens), they might have competitive incentives to prevent such connections (i.e., tertius gaudens). Building on this theoretical tension, this study investigates how brokerage and incumbent technology network structure shape emergent technology networks. We argue that organizations in the position of knowledge brokers tend to facilitate tie formation between partners to help mitigate uncertainty in an emergent technology, yet this tendency is reversed when keeping the separation between partners allows them to secure competitively advantageous positions. We collect longitudinal data on research and development collaborations in the cancer therapy industry, and conduct in-depth interviews with scientists and industry experts. We test our theoretical framework through stochastic actor-oriented modeling by examining the emergence of technology networks after the technological breakthrough of monoclonal antibodies for cancer therapy. Our findings indicate that over time, the role of brokers in fostering or preventing triadic closure across technologies significantly impacts the structure of emergent technology networks.

**Research Question**
Under what circumstances do brokers within and across technology networks facilitate or inhibit collaboration between their unconnected partners?

**Hypotheses / Propositions**
H1. Two firms are more likely to form an emerging (mAbs) technology alliance if they share a common third-party collaborator in the network of emerging technology alliances (within-network uniplex closure; positive).
H2. Two firms are more likely to form an emerging technology alliance if they share a common third-party collaborator in the network of incumbent (small-molecule) technology alliances (cross-network multiplex closure; positive).
H3. Two firms are less likely to form an emerging technology alliance if they share a common third-party collaborator in the network of incumbent technology alliances when only one of them has demonstrable expertise in the emergent technology (asymmetric boundary-spanning closure; negative — tertius gaudens dominates).

**Mechanism Process**
- IV(s): (1) Within-network uniplex closure — operationalized as a geometrically weighted dyad-wise shared partner term (GWDSP) capturing whether two firms share a common third-party collaborator within the emergent (mAbs) technology network; (2) Cross-network multiplex closure — a WW->X RSiena term capturing whether two firms share a common third party in the incumbent (small-molecule) technology network; (3) mAbs-expertise boundary-spanning closure — a "jumpWWClosure" term capturing the same multiplex configuration when the alter (R&D firm) has prior mAbs patents but the focal (client) firm does not.
- DV(s): Directed tie formation between client and R&D firm in the emergent mAbs alliance network (primary), with simultaneous tie formation in the small-molecule network as a co-dependent network in the multivariate SAOM.
- Mediators: Not formally modeled; the theorized mechanisms are uncertainty mitigation (favoring tertius iungens) and broker control of unique knowledge access (favoring tertius gaudens).
- Moderators: Asymmetry in firms' mAbs patent expertise (the boundary-spanning closure term itself functions as an interaction conditioning multiplex closure on knowledge asymmetry); controls for technology similarity, geographic distance, FDA stage 3 alliances, university ties, focal/alter patenting stocks and inventor counts.

The mechanism rests on the tertius iungens vs. tertius gaudens tension. In uniplex emergent-technology triads, brokers' competitive incentives are weak (all parties already operate in the same technology network), so the dominant logic is uncertainty mitigation: brokers introduce their unconnected emergent-technology partners to one another, fostering triadic closure (H1 supported, b=0.153, p<.05). In multiplex triads — where the broker mediates incumbent-technology ties between two firms that may form an emergent-technology tie — brokers in symmetrically informed dyads still favor closure because cross-technology referrals reduce relational and technological uncertainty (H2 supported, b=2.209, p<.05). However, when one alter has unique mAbs expertise and the other does not, the broker occupies a competitively attractive boundary-spanning position; the tertius gaudens logic dominates and brokers actively block the closure that would expose their information advantage (H3 supported, b=-126.659, p<.001). Findings replicate in rare-events logistic regression on 1.18M dyad-years.

**Data & Measures**
Data source: R&D alliances in cancer therapy from BioSciDB, a peer-reviewed biopharmaceutical alliance database; directed ties run from the client firm (seeking technology) to the R&D firm (providing it). Monoclonal-antibody (emergent) deals were isolated where "monoclonals" appears in the database's technologies field and were independently verified by two life-science scientists; small-molecule (incumbent) deals were identified analogously. Firm attributes were drawn from USPTO patents (Cooperative Patent Classification codes), FDA approvals and Stage-3 trial alliances, and geocoded headquarters. Final sample: 453 firms, 2004-2020 (17 yearly waves).
- DV: directed tie formation in the emergent mAbs alliance network, modeled jointly with small-molecule (incumbent) tie formation as a simultaneous dependent network in a multivariate stochastic actor-oriented model (SAOM) estimated in RSiena.
- IV, H1 (Within-Network Uniplex Closure): a geometrically weighted dyad-wise shared-partner (GWDSP) term for a shared third party within the mAbs network.
- IV, H2 (Cross-Network Multiplex Closure): a "WW->X" term for a shared third party in the incumbent small-molecule network.
- IV, H3 (mAbs Expertise Boundary-Spanning Closure): a "jumpWWClosure" term equal to multiplex closure conditional on the alter (R&D firm) holding prior mAbs patents while the focal (client) firm does not.
- Controls: indegree popularity, outdegree activity, alter/focal patents, knowledge quality (forward citations), number of inventors, FDA drug approvals, FDA Stage-3 alliances, university ties, mAbs patents, focal-alter similarity in mAbs, technology similarity (Euclidean distance between patent-class vectors) and its square, great-circle geographic distance, technology age, and small-molecule multiplexity.

Identification is associational network-dynamics modeling, not a causal experiment: SAOMs relax the tie-independence assumption and sienaCompositionChange accommodates firm entry and exit; fit is assessed via sienaGOF (Mahalanobis distance) on indegree, outdegree, and triad-census distributions. Robustness uses rare-events logistic regression (King & Zeng, 2001) on a 1.18-million dyad-year panel. A qualitative supplement of 14 expert interviews (9 informing context and hypotheses; 5 post-results sensemaking) contextualizes the mechanisms.

**Key Findings**
All three hypotheses are supported in the primary emergent (mAbs) network and replicate in the rare-events logistic-regression robustness models:
- H1 (within-network uniplex closure) supported: positive and significant in the mAbs network (b = 0.153, p < .05; SAOM Model 2) and replicated in the logit robustness test (b = 6.905, p < .001; Model 5). In the incumbent small-molecule network the same uniplex term was only marginally significant (p = .055).
- H2 (cross-network multiplex closure) supported: positive and significant in the mAbs network (b = 2.209, p < .05; SAOM Model 3), replicated in the logit (b = 1.121, p < .01; Model 6). The analogous multiplex term did not converge in the small-molecule network (an alternative XW->X term was non-significant), so no multiplex-closure tendency was found for the incumbent network.
- H3 (mAbs-expertise boundary-spanning closure) supported: negative and highly significant in the mAbs network (b = -126.659, p < .001; SAOM Model 3), replicated in the logit (b = -1.336, p < .001; Model 6) — when only the alter holds mAbs expertise, the broker blocks the emergent-technology tie (tertius gaudens). A parallel negative boundary-spanning effect also held for small-molecule tie formation (b = -14.957, p < .001).

SAOM goodness-of-fit was acceptable (indegree p = .147, outdegree p = .086, triad census p = .158).

**Theoretical Contribution**
The paper introduces multiplex technology closure — transitive collaborations spanning incumbent and emergent technology networks — as a new triadic concept that resolves the tertius iungens vs. tertius gaudens tension by jointly considering tie multiplexity and nodal expertise asymmetry. It contributes to (1) collaborative innovation theory by showing that the incumbent technology network exerts a paramount influence on the structure of emergent technology networks; (2) network dynamics research by modeling cross-network influences with simultaneously dependent networks; and (3) brokerage and triadic-closure theory by extending Shipilov and Li's (2012) multiplexity framework to triadic structures defined by technology focus and by demonstrating that brokers actively prevent closure to defend unique access to emergent-technology expertise.

**Practical Implication**
For pharmaceutical and biotech managers, the findings imply that established small-molecule incumbents can leverage existing collaborator triads to access emergent biological technologies such as mAbs, but should anticipate that intermediaries with unique mAbs expertise are unlikely to broker direct introductions. New entrants holding scarce emergent-technology expertise face strategic choices about whether to retain their boundary-spanning rents or grant access. For alliance designers and innovation policymakers, multiplex collaborative architectures across technologies are a central lever for accelerating cross-boundary innovation in domains where competing technologies coexist (e.g., antibody-drug conjugates).

**Limitations**
First, the empirical focus on the joint evolution of two networks (mAbs and small molecules) rather than full coevolution constrains inferences about two-way feedback. Second, generalizability beyond cancer therapy is uncertain because technological trajectories differ across industries; the findings may not transfer to settings with strong dominant designs or to breakthroughs (e.g., CRISPR-Cas) that establish a single dominant technology. Third, the study draws network boundaries based on the technological focus of relationships, leaving open the question of how a technology-community approach defined through relational distance would yield different patterns.

**Future Research**
The authors call for studies that (1) model true coevolution of multiple networks with two-way interdependencies, (2) examine how broker dynamics change when emergent technologies become new dominant standards (e.g., CRISPR-Cas), (3) investigate cyclical phases of technology emergence and their effects on cross-network broker behavior, and (4) explore multiplex technology closure within and across innovation communities defined by relational distance, asking how broker separation strategies play out across community boundaries.

**APA 7th Citation**
Brändle, L., Berger, E. S. C., & Howard, M. D. (2025). Crossing technological boundaries: Brokerage and the emergence of innovation networks. *Academy of Management Journal*, 68(3), 620-647. https://doi.org/10.5465/amj.2023.0439
