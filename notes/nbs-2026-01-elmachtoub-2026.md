---
id: nbs-2026-01-elmachtoub-2026
title: "Fair Fares for Vehicle Sharing Systems"
authors:
  - "Elmachtoub, Adam N."
  - "Kim, Hyemi"
year: 2026
journal: "Operations Research"
doi: "https://doi.org/10.1287/opre.2024.1043"
volume: null
issue: null
pages: null

source: "NBS/2026-01"
pdf_path: "library/NBS/2026-01/pdfs/Elmachtoub 2026 Fair Fares for Vehicle Sharing Systems.pdf"
text_path: "library/NBS/2026-01/text/Elmachtoub 2026 Fair Fares for Vehicle Sharing Systems.txt"
ingested_at: "2026-06-13"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["fairness", "price discrimination", "vehicle sharing systems"]
theory: ["price fairness and access fairness (Cohen, Elmachtoub, & Lei, 2022)", "queueing-network pricing models for shared vehicle systems (Waserhole & Jost, 2016; Banerjee et al., 2022; Benjaafar & Shen, 2023)"]
topics: ["pricing", "ecosystems-platforms", "public-policy", "north-america"]
unit_of_analysis: "market"
level_of_theory: "macro"
dependent_variable_family: "mixed"
methods: "Analytical operations-research study: a stylized two-node queueing-network pricing model (linear and exponential demand, with extensions for nonzero travel time, repositioning, and multiple units) yielding closed-form solutions and propositions; a convex-relaxation heuristic with provable approximation bounds for the general N-node network; and a real-data case study fitting logistic demand and solving the fair-pricing program with Ipopt/Pyomo."
sample:
  industry: "Vehicle sharing / ride-hailing transportation (Yellow Taxi, Green Taxi, and High-Volume For-Hire Vehicles such as Uber and Lyft)"
  country: "United States (Manhattan, New York City)"
  time_period: "Trips with pick-up times 7 a.m.–9 a.m. on March 3, 2023 (a 6 p.m.–8 p.m. window analyzed in the Online Appendix)"
  units: "Trips between Manhattan neighborhoods (63 taxi zones aggregated into N = 10 neighborhoods)"
  n: "K = 1548 vehicles (estimated); market sizes per node-pair from total Yellow/Green/Uber/Lyft trips in the window"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "We estimate the total number of units as K � 1548 by"
  sample_country: "such as Uber and Lyft, within New York City"
  sample_industry: "We focus on 63 taxi zones within Manhattan"
  sample_time_period: "trips with pick-up times between 7 a.m. and 9 a.m. on"
  theories_overview: "We consider two notions of fairness corresponding to price and access. Price fairness is a measure of how"
  methods_overview: "we employ a convex relaxation technique that is asymptotically optimal with access fairness constraints. Lastly, we conduct a case study"
  keywords_source: "Keywords: fairness • price discrimination • vehicle sharing systems"
---

# Fair Fares for Vehicle Sharing Systems

**Abstract**
To address the more general network pricing problem, we employ a convex relaxation technique that is asymptotically optimal with access fairness constraints. Lastly, we conduct a case study using real-world data of a vehicle sharing system operating in New York City. We analyze the tradeoff between fairness and various metrics, including revenue, consumer surplus, and social welfare, based on the fairness criteria we define.

**Research Question**
How does imposing price fairness or access fairness on a revenue-maximizing vehicle-sharing platform affect platform revenue, consumer surplus, and social welfare across locations, and how should platforms and regulators set fair fares to minimize the inequalities users experience by location?

**Mechanism Process**
- Decision variable (platform): origin–destination prices `p = {p_ij}` set to maximize steady-state revenue `R(p)` over a connected network of `N` nodes and `K` vehicles, subject to fairness constraints parameterized by `α ∈ [0,1]`.
- Fairness constraints (IV/treatment): *price fairness* (bounding the gap between max and min normalized prices) and *access fairness* (bounding the gap between max and min fractions of fulfilled requests, where access = availability `Π_i` × affordability `q_ij`), each in trip-based and origin-based forms.
- Outcomes (DVs): platform revenue, normalized consumer surplus `S(p)`, and social welfare `W(p) = R(p) + S(p)`.
- Key operational mechanism: vehicle availability is endogenous to prices through a steady-state flow-balance condition, so fair prices must also keep flow balanced across nodes.
- Moderators / boundary conditions: demand shape (linear vs. exponential), number of vehicles `K`, travel time, and the option to reposition vehicles.

The central mechanism is that prices in a shared-vehicle system govern not only affordability but also the spatial availability of vehicles via flow balance. A little price fairness can be win-win-win, reallocating a vehicle toward the lower-valuation node and raising surplus at both locations and overall welfare under some market scenarios. Access fairness, by contrast, forces availability at both nodes to move together and can only be satisfied by raising prices everywhere, so it always reduces consumer surplus at both locations and social welfare—perfect access fairness shuts the system down entirely. Repositioning can partly relax this "everyone worse-off" tendency by letting one location gain while another loses.

**Theoretical Contribution**
The paper extends fairness-constrained pricing (Cohen et al., 2022) from an infinite-supply monopolist to a finite-supply network where availability is endogenous, showing that the operational coupling between prices and vehicle flow produces regimes—and a uniformly harmful access-fairness result—that do not arise under unlimited resources. It formalizes price and access fairness for shared-vehicle networks, proves an impossibility of simultaneous perfect price and access fairness, and supplies a convex relaxation for access fairness with an asymptotically optimal approximation guarantee.

**Practical Implication**
Platforms and regulators are advised to favor price fairness over access fairness: a small amount of price fairness can raise welfare and surplus, whereas access fairness, though well intentioned, makes all parties worse off. The Manhattan case study shows how to quantify, by neighborhood, which areas gain or lose and how much revenue must be sacrificed for a given fairness level (e.g., origin-based access fairness retains ~80% of revenue and ~56% of surplus at full fairness).

**Limitations**
The theoretical results rely on a stylized two-node, single-unit model with specific demand families, and several general-network claims are obtained via a convex relaxation rather than exact solution. The case study cannot directly observe valuations or rejected trips, so demand functions are approximated from observed prices via a random-utility argument, and the analysis covers limited time windows in a single city.

**Future Research**
The authors suggest studying platforms that maximize social welfare rather than revenue, exploring alternative rider-side fairness notions (e.g., surplus-based) and driver-side fairness criteria, and investigating the legal and ethical implications of the proposed fairness measures.

**APA 7th Citation**
Elmachtoub, A. N., & Kim, H. (2026). Fair fares for vehicle sharing systems. *Operations Research*. https://doi.org/10.1287/opre.2024.1043
