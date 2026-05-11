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
extraction_model: "claude-opus-4-6"
extraction_version: "v2"

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
---

# Coevolutionary Lock-In in External Search

**Abstract**
While external search allows organizations to source diverse ideas from people outside the organization, it often generates a narrow set of nondiverse ideas. We theorize that this stems from an interplay between organizations' idea selection and the external generation of ideas: an organization selects ideas shared by external contributors, and the external contributors, who strive to see their ideas selected, use the prior selection to infer what kind of ideas the organization is looking for, and to respond. Contributors whose ideas are misaligned with the organization's selection tend to stop submitting ideas (i.e., self-selection) or adjust the ideas they submit so that they correspond (i.e., self-adjustment), resulting in a less diverse pool of ideas. Our central hypothesis is that the more consistent organizations are in their selection, the stronger the coevolutionary lock-in: organizations with greater selection consistency receive future ideas with lower content variety. We find support for these predictions by combining large-scale network analysis and natural language processing across a large number of organizations that use crowdsourcing. Our findings suggest a reconceptualization of external search as a two-way street: organizations are not simply passive receivers of ideas but send signals that shape the pool of ideas that externals share.

**Research Question**
How does an organization's consistency in selecting which crowdsourced ideas to implement shape the variety of ideas that external contributors subsequently submit, and what features of the external-contributor network moderate this coevolutionary process?

**Mechanism Process**
- IV(s): Selection consistency (lagged, t−1) — average cosine similarity of all pairs of ideas selected by the organization in a crowd-period
- DV(s): Idea variety (t) — log of the average cosine dissimilarity across pairs of newly submitted ideas in the focal crowd-period
- Mediators (individual-level micro-mechanisms): self-selection (contributors whose ideas are distant from selected ones stop submitting) and self-adjustment (contributors modify subsequent submissions toward the selected solution space)
- Moderators: churn-newcomer (proportion of contributors who are newcomers in the period), churn-departure (proportion of established contributors who leave), and cohesion (log-density of the contributor–commenter network, lagged)
- Controls: crowd fixed effects, age of crowd, number of active contributors (t and t−1), idea length, degree of idea clustering, share of selected ideas, employee suggestions, number and length of organizational responses, number of votes, alignment between contributor votes and organizational selections

The mechanism is a positive feedback loop on the crowd: when an organization repeatedly selects similar ideas, external contributors infer a narrow taste from that signal, and adapt either by exiting (self-selection) or by submitting closer-to-selected ideas (self-adjustment). The pool of ideas the organization next sees therefore narrows in content variety, which in turn constrains future selection and reinforces the cycle. The effect is stronger when contributors have been exposed to (and socialized into) the signal — i.e., low churn and high network cohesion — and weaker when newcomers arrive or established contributors leave.

**Theoretical Contribution**
The paper recasts external search as a two-way street: organizations not only absorb ideas from externals but also shape, through their selection signals, the very pool of ideas they will later receive. It identifies a coevolutionary lock-in mechanism that explains why open and crowdsourced search — typically framed as broadening — can over time converge to the same narrow solution space as internal search. By specifying self-selection and self-adjustment as the individual-level micro-foundations of this crowd-level convergence and by tying their strength to structural network properties (churn, cohesion), the study bridges micro and macro accounts of how organizations and external contributors jointly produce the information environment for organizational learning.

**Practical Implication**
Managers who want sustained idea variety should treat selection policy as a deliberate design lever rather than a neutral filter. Introducing some ambiguity or noise into selection (less perfectly consistent choices) preserves the perceived openness of the search and keeps contributors exploring broadly; concentrating selection accelerates fit but narrows the solution space, possibly irreversibly. Managers can also dampen lock-in by limiting visibility or interactions among external contributors when broad search is the goal, and should expect the fit-versus-variety trade-off to favor consistency in static environments and ambiguity in dynamic or breakthrough-seeking contexts.

**Limitations**
The evidence is correlational and may be subject to time-varying unobserved confounders despite crowd fixed effects. The individual-level analysis is restricted to contributors who submitted at least one idea, so it likely underestimates the true magnitude of self-selection by missing observers who never submit. The data also do not permit assessment of the performance consequences of coevolutionary lock-in, leaving the welfare implications of the fit-variety trade-off open.

**Future Research**
Field or lab experiments that manipulate selection policy could establish causal effects of selection consistency on idea variety. The authors call for studies of whether the coevolutionary process emerges across other forms of external search — alliances, hackathons, open innovation, informal networks — where contributors' costs of nonselection and incentives to align differ from crowdsourcing. Further work could also examine how performance feedback, payoff asymmetries, and contributor incentives shape the strength and reversibility of lock-in.

**APA 7th Citation**
Park, S., Piezunka, H., & Dahlander, L. (2024). Coevolutionary lock-in in external search. *Academy of Management Journal*, 67(1), 262–288. https://doi.org/10.5465/amj.2022.0710
