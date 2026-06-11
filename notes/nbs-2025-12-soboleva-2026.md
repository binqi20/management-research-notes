---
id: nbs-2025-12-soboleva-2026
title: "Agent-based insight into eco-choices: Simulating the fast fashion shift"
authors:
  - "Soboleva, Daria"
  - "Sánchez, Angel"
year: 2026
journal: "Ecological Economics"
doi: "https://doi.org/10.1016/j.ecolecon.2025.108824"
volume: 240
issue: null
pages: "108824"

source: "NBS/2025-12"
pdf_path: "library/NBS/2025-12/pdfs/Soboleva 2025 Agent-based insight into eco-choices Simulating the fast fashion shift.pdf"
text_path: "library/NBS/2025-12/text/Soboleva 2025 Agent-based insight into eco-choices Simulating the fast fashion shift.txt"
ingested_at: "2026-06-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["Fast fashion", "Agent-based modeling", "Demand", "Consumer behavior", "Environment", "Working conditions"]
theory: ["opinion dynamics (DeGroot, 1974; Friedkin–Johnsen)", "Bounded Confidence Model (Hegselmann and Ulrich, 2022)"]
topics: ["sustainable-consumption", "pro-environmental-behavior", "consumer-psychology", "europe"]
unit_of_analysis: "individual"
level_of_theory: "cross-level"
dependent_variable_family: "environmental"
methods: "Agent-based simulation in NetLogo 6.3.0; agents calibrated with a linear regression decision model estimated on survey data; scenario experiments vary peer-communication, social-media exposure/bias, and government-campaign parameters across non-polarized and polarized populations."
sample:
  industry: "Fast fashion / apparel consumption"
  country: "Spain"
  time_period: "Not reported in paper"
  units: "Simulated consumer agents (calibrated on Spanish survey respondents)"
  n: "1050 agents (calibrated on 1067 Spanish survey respondents)"

evidence:
  sample_n: "used for the linear regression. It is used to create 1050 agents."
  sample_country: "the demand for fast fashion, with a focus on Spain."
  sample_industry: "the demand for fast fashion"
  sample_time_period: "Not reported in paper"
  theories_overview: "choice of opinion updating mechanism is based on the foundational"
  methods_overview: "influences. To do so, we employ Agent-Based Modeling (ABM), which"
  keywords_source: "involved in choosing to buy fast fashion and the role of awareness regarding working conditions, environmental"
---

# Agent-based insight into eco-choices: Simulating the fast fashion shift

**Abstract**
the demand for fast fashion, with a focus on Spain. We explore the individual decision-making process involved in choosing to buy fast fashion and the role of awareness regarding working conditions, environmental consequences, and education on sustainable fashion in influencing consumer behavior. By employing Agent-Based Modeling, we investigate the factors influencing garment consumption patterns and how shifts in public opinion can be achieved through peer pressure, social media influence, and government interventions. Our study revealed that government interventions are pivotal, with the state's campaigns setting the overall tone for progress, although its success is conditioned by social media and polarization levels of the population. Importantly, the state does not need to adopt an extremely proactive stance or continue the campaigns indefinitely to achieve optimal results, as excessive interventions yield diminishing returns.

**Research Question**
How do awareness and education about sustainability shape individuals' decision-making regarding fast-fashion purchases, and how can peer pressure, social media, and government interventions shift public opinion toward more sustainable garment choices?

**Mechanism Process**
- Key constructs: agents' probability to purchase fast fashion, environmental concerns, working-conditions awareness, education on sustainable fashion, normative expectations, trust, access, shopping frequency.
- Decision model: a linear regression (R² = 0.37) on Spanish survey data calibrates each agent's purchase probability; environmental concerns and normative expectations are negatively but weakly associated, while shopping frequency dominates.
- Influence channels: peer interaction (DeGroot/Friedkin–Johnsen opinion dynamics; tolerance threshold for polarized agents), social-media feedback loops with bias, and "smart" re-election-seeking government campaigns with campaign-fatigue decay.
- Triggering conditions / moderators: population polarization level, communication (sharing) threshold δ, tolerance τ, social-media exposure σ and bias β, and government stance ζ.
- Emergent outcomes: population-level shifts in average concerns and fast-fashion purchase probability.

Individual micro-level agents update opinions through repeated weighted averaging over a small-world clique network, and these micro interactions aggregate to macro-level shifts in public opinion. Government campaigns set the overall tone for sustainable change, but their effectiveness is conditioned by initial polarization and prevailing social-media biases; beyond a point, additional intervention yields diminishing returns, and a slightly polarized population best sustains campaign effects after they are halted.

**Theoretical Contribution**
The study extends agent-based and opinion-dynamics modeling (DeGroot and Friedkin–Johnsen frameworks, with a bounded-confidence-style tolerance threshold) to the domain of sustainable fashion consumption, integrating peer, media, and state influence in one calibrated model. It theorizes that the well-documented attitude–behavior ("ethical purchasing") gap reflects an absence of societal pressure rather than insufficient concern, and that collective behavioral change depends on the broader population's receptiveness, not on highly concerned individuals or social media alone.

**Practical Implication**
Policymakers can shift consumption patterns through moderate, well-timed pro-sustainability campaigns rather than extreme or indefinite intervention, since excessive campaigning yields diminishing returns. Campaign design should account for population polarization and social-media bias; a slightly polarized population sustains effects longest, while educational efforts are needed to close the gap between concern and action.

**Limitations**
The model rests on simplifying assumptions: agents form ties randomly and cannot dissolve them, interactions are unilateral and equally weighted, and agents address one topic per time step, so model time does not map cleanly to real time and the lack of longitudinal data prevents validation. Susceptibilities are static and assigned independently, the government is assumed to know the population's average opinion, and the decision model is calibrated specifically to the Spanish market, limiting generalizability.

**Future Research**
Future work could let agents create and dissolve ties based on opinion differences to produce more realistic homophilous group formation, model bilateral and unequally weighted interactions, and allow susceptibility to change dynamically with usage and political alignment. Interconnecting the three susceptibility types and recalibrating the decision model with local data for other countries would extend applicability beyond Spain.

**APA 7th Citation**
Soboleva, D., & Sánchez, A. (2026). Agent-based insight into eco-choices: Simulating the fast fashion shift. *Ecological Economics*, 240, 108824. https://doi.org/10.1016/j.ecolecon.2025.108824
