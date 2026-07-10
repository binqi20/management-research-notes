---
id: amj-vol-57-no-1-funk-2014
title: "Making the Most of Where You Are: Geography, Networks, and Innovation in Organizations"
authors:
  - "Funk, R. J."
year: 2014
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2012.0585"
volume: 57
issue: 1
pages: "193-222"

source: "AMJ/vol-57-no-1"
pdf_path: "library/AMJ/vol-57-no-1/pdfs/Funk 2014 Making the Most of Where You Are Geography, Networks, and Innovation in Organizations.pdf"
text_path: "library/AMJ/vol-57-no-1/text/Funk 2014 Making the Most of Where You Are Geography, Networks, and Innovation in Organizations.txt"
ingested_at: "2026-07-10"
extraction_model: "claude-fable-5"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["geographic proximity", "knowledge spillovers", "intraorganizational networks", "cohesion", "inefficiency", "innovative performance"]
theory: ["theories of geography and innovation / localized knowledge spillovers (Audretsch & Feldman, 1996; Bathelt, Malmberg, & Maskell, 2004)", "social network theory: brokerage and cohesion (Burt, 2004; Coleman, 1988; Obstfeld, 2005; Lazer & Friedman, 2007)", "community social capital (Coleman, 1988; Lin, 1999; Putnam, 2000)"]
topics: ["innovation-management", "social-capital-theory", "north-america", "longitudinal"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Longitudinal firm-year panel; intraorganizational inventor networks from patent co-inventorship data; conditional fixed-effects quasi-maximum-likelihood Poisson regression with robust standard errors, random-effects Poisson with bootstrapped standard errors, probit selection model (inverse Mills ratio), and robustness checks (alternative lags, Burt's constraint, pre-1990 non-relocating subsample, Box-Cox OLS)."
sample:
  industry: "Nanotechnology (firms engaged in commercial nanotechnology R&D)"
  country: "United States"
  time_period: "1990-2004"
  units: "Firms (firm-year observations; networks and outcomes measured at each firm's main research facility)"
  n: "454 firms; 2,760 firm-year observations"

# Mandatory evidence anchors (v3 - Layer 1 faithfulness audit).
evidence:
  sample_n: "I collected longitudinal data on 454 firms that"
  sample_country: "454 US companies active in nanotechnology R&D"
  sample_industry: "companies active in nanotechnology R&D between 1990 and 2004"
  sample_time_period: "active in nanotechnology R&D between 1990 and 2004"
  theories_overview: "My approach extends theories of geography and innovation"
  methods_overview: "The estimates presented in models 1–7 are derived from conditional fixed-effects quasi-maximum-likelihood Poisson specification with robust standard errors"
  keywords_source: "such effects are moderated by intraorganizational network structures"
  hypotheses_source: "Hypothesis 1. Increases in proximity to other"
  measures_overview: "Count of citations to nanotechnology patents, applied for by inventors at"
  findings_overview: "as proximity to industry peers decreases—and knowledge spillovers become less common—inefficient networks are beneficial because they create and sustain diversity internally"
---

# Making the Most of Where You Are: Geography, Networks, and Innovation in Organizations

**Abstract**
Drawing on insights from macro- and microlevel research, I develop and test a theory of how the makeup of firms’ local environments influences their ability to generate innovations. I propose that although geographic proximity to industry peers can enhance performance, such effects are moderated by intraorganizational network structures. Data on collaborations among inventors and the geographic locations of 454 US companies active in nanotechnology R&D between 1990 and 2004 are used to show that as proximity to industry peers decreases—and knowledge spillovers become less common—inefficient networks are beneficial because they create and sustain diversity internally. For firms with high proximity, more cohesive network structures that facilitate information processing are desirable.

**Research Question**
How does the makeup of firms' local environments influence their ability to generate innovations? Specifically, the paper theorizes and tests whether the innovative-performance benefits of geographic proximity to companies performing related R&D are moderated by the structure of intraorganizational collaboration networks among a firm's inventors.

**Hypotheses / Propositions**
H1: Increases in proximity to other companies that perform related R&D are positively associated with a firm's innovative performance.
H2a: As proximity to companies that perform related R&D increases, a firm has greater innovative performance if the cohesiveness of its intraorganizational collaboration network also increases.
H2b: As proximity to companies that perform related R&D decreases, a firm has greater innovative performance if the inefficiency of its intraorganizational collaboration network increases.

**Mechanism Process**
- IV(s): Firm proximity (patent-weighted local density of other nanotechnology firms around a firm's main research facility)
- DV(s): Innovative performance: patent impact (citation-weighted count of nanotechnology patents applied for at t + 1 and t + 2) and new combinations (count of such patents bridging previously uncombined technology subclasses)
- Mediators: None modeled
- Moderators: Intraorganizational inventor network structure: cohesion (scaled clustering coefficient) and inefficiency (scaled average path length)

Geographic proximity to industry peers increases access to localized knowledge spillovers (through monitoring competitors, chance encounters, informal networks, and shared local institutions), supplying the diverse knowledge that fuels novel recombination but also raising the volume of information firms must internalize, adapt, and use. Cohesive intraorganizational networks promote frequent communication, trust, and joint problem solving, so they help highly proximate firms process large volumes of complex spillover knowledge, while local interaction offsets the knowledge-stagnation risks of dense ties. Inefficient networks, which have low connectivity and diffuse information slowly, preserve diverse ideas internally, create brokerage opportunities, and facilitate parallel problem solving, thereby compensating geographically isolated firms for their diminished access to spillovers. Innovative performance is therefore greatest when the structure of a firm's inventor network fits its geographic milieu.

**Data & Measures**
Longitudinal panel of 454 US firms engaged in nanotechnology R&D, 1990-2004 (2,760 firm-year observations after firm entry and exit). Intraorganizational networks are built from co-inventorship ties formed when two or more of a firm's employees work on a patent together (a unipartite projection of the inventor-patent bipartite network from the Patent Network Dataverse; ties dropped after five years), restricted to each firm's main research facility, whose annually updated location was hand-collected from SEC filings, archived company websites, press releases, and trade publications. DVs: impact = citation-weighted sum of nanotechnology patents applied for at t + 1 and t + 2 (five-year citation window); new combinations = count of such patents first combining a previously uncombined set of USPTO subclasses. IV: firm proximity = inverse-distance-weighted measure across all other sample firms, weighted by their logged annual nanotechnology patent counts. Moderators: cohesion = the network clustering coefficient scaled by that of a simulated random network with an identical bipartite degree distribution; inefficiency = average path length within connected components scaled by the random-network expectation. Estimation is associational: conditional fixed-effects quasi-maximum-likelihood Poisson models with robust standard errors plus random-effects Poisson models with bootstrapped standard errors, with a first-stage probit selection model supplying an inverse Mills ratio; fixed effects, the lag structure, and extensive controls (e.g., local university ties, local inventor hires, distant inventors, patent stocks) are used to alleviate endogeneity concerns, supported by robustness checks (pre-1990 non-relocating facilities, one-year lags, Burt's constraint, unweighted proximity, Box-Cox OLS).

**Key Findings**
In sum, all three hypotheses receive strong support. H1 supported: firm proximity has a positive and significant effect on both patent impact and new combinations (models 2 and 10). H2a supported: the cohesion x firm proximity interaction is positive and significant for both dependent variables (0.01, p < .01, models 6 and 14); as proximity to other nanotechnology firms increases, more cohesive inventor networks lead to greater innovative performance. For high-proximity firms, a two-standard-deviation increase above mean cohesion predicts increases of 25 percent in impact and 28 percent in new combinations, whereas for low-proximity firms the same increase predicts declines of 8 and 6 percent. H2b supported: the inefficiency x firm proximity interaction is negative and significant (-0.01; p < .05 for impact, p < .01 for new combinations), meaning that as proximity decreases, inefficient networks become beneficial; firms with much lower proximity see a 22 percent increase in impact and a 29 percent increase in new combinations for a two-standard-deviation increase in inefficiency. An unhypothesized finding is that firms combining high proximity with very cohesive networks have the greatest absolute performance; the main effect of inefficiency is positive and significant for both innovation measures.

**Theoretical Contribution**
The study advances theories of geography and innovation by showing that the benefits firms derive from their local environments are moderated by the structure of collaboration networks among their employees, accounting both for how highly proximate firms filter and process large volumes of spillover knowledge and for how geographically isolated firms create and sustain diversity internally. It contributes to network theory by examining contingencies in the overall (global) structure of relations rather than ego networks, showing that ego-level insights favoring increased connectivity do not translate cleanly to the global level, where less connectivity can be advantageous for groups that seek diverse ideas but have limited exposure to external knowledge. The finding that less connected networks can improve collective innovation also pushes community social capital research, and ecological and institutional work on local community effects, toward a more nuanced, contingency-based perspective.

**Practical Implication**
Managers seeking to stimulate innovation should consider structuring teams in ways that limit overall ties among their R&D employees when those employees have little exposure to new knowledge from peers at proximate organizations, for example by creating formal units housing separate project teams or skunk-works separations; by contrast, managers operating in settings proximate to industry peers should increase cohesion among R&D employees, for example through frequent meetings that bring together employees from diverse projects for collective problem solving. For entrepreneurs or managers choosing a location for a new venture or relocating an existing one, the findings help evaluate the trade-offs of different kinds of locations, and closely monitoring patterns of collaboration among employees might attenuate some of the innovation disadvantages of isolation.

**Limitations**
The proximity measure is based on distance to other firms, whereas universities, nonprofit research institutes, and government laboratories active in nanotechnology may also provide spillover benefits, and for some firms distance to a key partner could matter more than overall proximity. In addition, models that derive network and innovation data from archival sources like patents miss collaborative ties and innovations that leave no paper trail and do not account for informal contributions, a problem the author mitigates by studying a field in which patenting is commonplace.

**Future Research**
The paper calls for more nuanced measures of regional composition to better understand the effects of geography and intraorganizational ties; for alternative data on intraorganizational ties and performance, such as scientific publications or surveys, including better documentation of employees' interpersonal connections outside the organization and the human resource practices that facilitate or constrain the persistence of those ties; and for systematic research explaining the success of geographically isolated firms. It also urges research on how intraorganizational collaboration patterns shape the geographic diffusion of knowledge and regional economies, and on identifying the applicability of different network contingencies across ego and global levels of analysis.

**APA 7th Citation**
Funk, R. J. (2014). Making the most of where you are: Geography, networks, and innovation in organizations. *Academy of Management Journal*, 57(1), 193–222. https://doi.org/10.5465/amj.2012.0585
