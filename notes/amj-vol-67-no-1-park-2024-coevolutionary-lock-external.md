---
id: amj-vol-67-no-1-park-2024-coevolutionary-lock-external
title: "Coevolutionary Lock-In in External Search"
authors:
  - "Park, Sanghyun"
  - "Piezunka, Henning"
  - "Dahlander, Linus"
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0710"
volume: 67
issue: 1
pages: "262-288"

source: "AMJ/vol-67-no-1"
pdf_path: "library/AMJ/vol-67-no-1/pdfs/Park 2024 Coevolutionary Lock-In in External Search.pdf"
text_path: "library/AMJ/vol-67-no-1/text/Park 2024 Coevolutionary Lock-In in External Search.txt"
ingested_at: "2026-05-12"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-14"

paper_type: "empirical-quantitative"
keywords: ["external search", "crowdsourcing", "coevolutionary lock-in", "selection consistency", "idea variety", "self-selection", "self-adjustment", "open innovation"]
theory: ["coevolutionary lock-in (Burgelman, 2002; Levinthal & Myatt, 1994)", "vicarious learning and signaling in open search (Piezunka & Dahlander, 2015, 2019)", "microfoundations of organization-individual interaction (Felin, Foss, & Ployhart, 2015)"]
topics: ["innovation-management", "ecosystems-platforms", "competitive-strategy", "signaling-theory"]
unit_of_analysis: "organization"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Longitudinal panel analysis of crowd-period observations from a U.S. crowdsourcing software vendor; fixed effects regressions with crowd-level fixed effects and clustered standard errors predict log-transformed idea variety; idea (dis)similarity measured via bag-of-words cosine distance with NLTK/scikit-learn preprocessing, with Doc2Vec word-embedding robustness check; supplementary OLS and contributor-fixed-effects models test individual-level self-selection and self-adjustment mechanisms."
sample:
  industry: "Crowdsourcing initiatives (suggestion-box style) hosted on the websites of organizations using a U.S. cloud-based crowdsourcing software vendor"
  country: "United States (software vendor; client organizations span the vendor's user base)"
  time_period: "November 2007 to March 2018 (panel periods of eight weeks each)"
  units: "Crowd-period (each crowd is an organization's open call for ideas)"
  n: "1,218 organizations, 1,435 crowds, 1.44 million ideas from 1.07 million contributors, yielding 11,296 crowd-period observations"

evidence:
  sample_n: "includes 1,218 organizations with 1,435 crowds that"
  sample_country: "the dataset in collaboration with a U.S.-based com"
  sample_industry: "the crowdsourcing efforts of 1,218 dis"
  sample_time_period: "November 2007 and March 2018)."
  theories_overview: "use the prior selection as a signal to infer what kind"
  methods_overview: "We thus adopt a fixed effects model that can"
  keywords_source: "selection consistency reduces idea variety. These"
  hypotheses_source: "organizations with greater selection consistency receive future ideas with lower"
  measures_overview: "To measure the (dis)similarity of ideas, we use"
  findings_overview: "idea variety in the subsequent period decreases by"
---

# Coevolutionary Lock-In in External Search

**Abstract**
While external search allows organizations to source diverse ideas from people outside the organization, it often generates a narrow set of nondiverse ideas. We theorize that this stems from an interplay between organizations' idea selection and the external generation of ideas: an organization selects ideas shared by external contributors, and the external contributors, who strive to see their ideas selected, use the prior selection to infer what kind of ideas the organization is looking for, and to respond. Contributors whose ideas are misaligned with the organization's selection tend to stop submitting ideas (i.e., self-selection) or adjust the ideas they submit so that they correspond (i.e., self-adjustment), resulting in a less diverse pool of ideas. Our central hypothesis is that the more consistent organizations are in their selection, the stronger the coevolutionary lock-in: organizations with greater selection consistency receive future ideas with lower content variety. We find support for these predictions by combining large-scale network analysis and natural language processing across a large number of organizations that use crowdsourcing. Our findings suggest a reconceptualization of external search as a two-way street: organizations are not simply passive receivers of ideas but send signals that shape the pool of ideas that externals share.

**Research Question**
How does an organization's consistency in selecting which crowdsourced ideas to implement shape the variety of ideas that external contributors subsequently submit, and what features of the external-contributor network moderate this coevolutionary process?

**Hypotheses / Propositions**
H1: Greater selection consistency by organizations results in reduced future idea variety (a negative main effect of selection consistency on idea variety).
H2a: Greater churn among external contributors dampens the decreasing effect that selection consistency has on idea variety (a positive, effect-weakening moderation), tested separately for newcomer inflow (Churn Newcomer) and established-contributor departure (Churn Departure).
H2b: Greater cohesion among external contributors amplifies the decreasing effect that selection consistency has on idea variety (a negative, effect-strengthening moderation).

**Mechanism Process**
- IV(s): Selection consistency (lagged, t−1) — average cosine similarity of all pairs of ideas selected by the organization in a crowd-period
- DV(s): Idea variety (t) — log of the average cosine dissimilarity across pairs of newly submitted ideas in the focal crowd-period
- Mediators (individual-level micro-mechanisms): self-selection (contributors whose ideas are distant from selected ones stop submitting) and self-adjustment (contributors modify subsequent submissions toward the selected solution space)
- Moderators: churn-newcomer (proportion of contributors who are newcomers in the period), churn-departure (proportion of established contributors who leave), and cohesion (log-density of the contributor–commenter network, lagged)
- Controls: crowd fixed effects, age of crowd, number of active contributors (t and t−1), idea length, degree of idea clustering, share of selected ideas, employee suggestions, number and length of organizational responses, number of votes, alignment between contributor votes and organizational selections

The mechanism is a positive feedback loop on the crowd: when an organization repeatedly selects similar ideas, external contributors infer a narrow taste from that signal, and adapt either by exiting (self-selection) or by submitting closer-to-selected ideas (self-adjustment). The pool of ideas the organization next sees therefore narrows in content variety, which in turn constrains future selection and reinforces the cycle. The effect is stronger when contributors have been exposed to (and socialized into) the signal — i.e., low churn and high network cohesion — and weaker when newcomers arrive or established contributors leave.

**Data & Measures**
- Data: a longitudinal dataset built with a U.S.-based vendor of cloud-based crowdsourcing ("suggestion box") software: 1,218 organizations, 1,435 crowds, and 1.44 million ideas from 1.07 million contributors, with time-stamped events from November 2007 to March 2018 transformed into eight-week crowd-period panels (11,296 crowd-period observations).
- Idea variety (DV, period t): log of the average cosine dissimilarity across all pairs of newly submitted ideas in a crowd-period, computed from bag-of-words vectors after stopword removal and stemming in Python (nltk, sklearn).
- Selection consistency (IV, lagged t−1): the average cosine similarity of all pairs of ideas the organization selected in a crowd-period, entered lagged to address reverse causality.
- Moderators: Churn Newcomer (proportion of contributors who are newcomers), Churn Departure (departing established contributors relative to active established contributors), and Cohesion (log density of the lagged contributor–commenter network, measured with NetworkX).
- Estimation: crowd fixed-effects regressions with standard errors clustered at the crowd level, adopted to absorb time-invariant unobserved heterogeneity; the design is associational (the authors describe the evidence as correlational and use lagged predictors for reverse causality rather than a causal-identification strategy). Robustness uses a Doc2Vec word-embedding distance; the individual-level self-selection mechanism is tested with pooled OLS (DV: propensity to contribute again) and self-adjustment with contributor fixed effects (DV: distance from the closest selected idea).

**Key Findings**
- H1 supported: selection consistency is negatively associated with next-period idea variety (Model 2: b = −0.024, p < .01); a 1 SD increase in selection consistency lowers subsequent idea variety by about 0.13 SD.
- H2a supported for both churn components (positive interactions that weaken the main effect): selection consistency × Churn Newcomer (Model 3: b = 0.058; Model 6: b = 0.038, p < .01) and selection consistency × Churn Departure (Model 4: b = 0.043; Model 6: b = 0.034, p < .01).
- H2b supported: cohesion negatively moderates the effect, strengthening the coevolutionary lock-in (Model 5: b = −0.018; Model 6: b = −0.015, p < .01).
- Micro-mechanisms: distance from selected ideas is negatively related to the propensity to contribute again (self-selection), and a contributor's number of prior contributions is negatively related to a new idea's distance from selected ideas (self-adjustment); both effects are strengthened under more consistent selection.
- Supplementary and robustness: a reverse loop also holds, with lower idea variety raising later selection consistency (Table 4, Model 2: b = −1.370; a 1 SD drop in idea variety raises selection consistency by 0.25 SD); the Churn Departure moderation turns nonsignificant at lower idea-count cutoffs, while H1, the newcomer moderation, and H2b remain supported.

**Theoretical Contribution**
The paper recasts external search as a two-way street: organizations not only absorb ideas from externals but also shape, through their selection signals, the very pool of ideas they will later receive. It identifies a coevolutionary lock-in mechanism that explains why open and crowdsourced search — typically framed as broadening — can over time converge to the same narrow solution space as internal search. By specifying self-selection and self-adjustment as the individual-level micro-foundations of this crowd-level convergence and by tying their strength to structural network properties (churn, cohesion), the study bridges micro and macro accounts of how organizations and external contributors jointly produce the information environment for organizational learning.

**Practical Implication**
Managers who want sustained idea variety should treat selection policy as a deliberate design lever rather than a neutral filter. Introducing some ambiguity or noise into selection (less perfectly consistent choices) preserves the perceived openness of the search and keeps contributors exploring broadly; concentrating selection accelerates fit but narrows the solution space, possibly irreversibly. Managers can also dampen lock-in by limiting visibility or interactions among external contributors when broad search is the goal, and should expect the fit-versus-variety trade-off to favor consistency in static environments and ambiguity in dynamic or breakthrough-seeking contexts.

**Limitations**
The evidence is correlational and may be subject to time-varying unobserved confounders despite crowd fixed effects. The individual-level analysis is restricted to contributors who submitted at least one idea, so it likely underestimates the true magnitude of self-selection by missing observers who never submit. The data also do not permit assessment of the performance consequences of coevolutionary lock-in, leaving the welfare implications of the fit-variety trade-off open.

**Future Research**
Field or lab experiments that manipulate selection policy could establish causal effects of selection consistency on idea variety. The authors call for studies of whether the coevolutionary process emerges across other forms of external search — alliances, hackathons, open innovation, informal networks — where contributors' costs of nonselection and incentives to align differ from crowdsourcing.

**APA 7th Citation**
Park, S., Piezunka, H., & Dahlander, L. (2024). Coevolutionary lock-in in external search. *Academy of Management Journal*, 67(1), 262–288. https://doi.org/10.5465/amj.2022.0710
