---
id: amj-vol-67-no-2-li-2024
title: "Before Birth: How Provisional Spaces Shape the Localized Emergence of New Organizational Forms"
authors:
  - "Li, Ying"
  - "Khessina, Olga M."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0897"
volume: 67
issue: 2
pages: "494-525"

source: "AMJ/vol-67-no-2"
pdf_path: "library/AMJ/vol-67-no-2/pdfs/Li 2023 Before Birth How Provisional Spaces Shape the Localized Emergence of New Organizational Forms.pdf"
text_path: "library/AMJ/vol-67-no-2/text/Li 2023 Before Birth How Provisional Spaces Shape the Localized Emergence of New Organizational Forms.txt"
ingested_at: "2026-05-10"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords:
  - "provisional spaces"
  - "organizational form emergence"
  - "prebirth stage"
  - "proto-form"
  - "spatiotemporal context"
  - "geographic communities"
  - "localized opportunity structure"
  - "organizational ecology"
  - "movie theaters"
  - "nickelodeon"
theory:
  - "organizational form emergence and ecology (Hannan & Freeman, 1977; Hannan, Polos, & Carroll, 2007; Carroll & Hannan, 2000)"
  - "density dependence and legitimation (Hannan & Carroll, 1992; Hsu & Hannan, 2005)"
  - "spaces in organizational change (Cartel, Boxenbaum, & Aggeri, 2019; Furnari, 2014; Taylor & Spicer, 2007)"
  - "categorization and proto-forms (Polos, Hannan, & Carroll, 2002; McKendrick, Jaffee, Carroll, & Khessina, 2003)"
  - "highbrow/lowbrow cultural distinction (Bourdieu, 1984; DiMaggio, 1992)"
topics:
  - "entrepreneurship"
  - "new-venture-creation"
  - "strategy-innovation"
  - "historical"
unit_of_analysis: "market"
level_of_theory: "macro"
dependent_variable_family: "na"
methods: "Continuous-time event-history analysis using piecewise-exponential hazard rate models of a community's first founding of a movie theater (any form, nickelodeon-only, or movie house/palace-only). Independent variables are time-discounted (25% per year) cumulative counts of community-specific provisional spaces (all, highbrow, lowbrow), lagged by one year. Models include controls for population, median income, education, foreign-born share, professional workers, dwelling density, university and recreational presence, average movie runtime, annual film supply, and neighboring-community organizational density. Estimated by maximum likelihood in Stata (stpiece) on a split-spell file of year-long intervals; robust standard errors via Huber–White sandwich estimator clustered by community. Robustness checks include alternative discount rates, discrete-time event-history equivalents, and a placebo test on trade schools."
sample:
  industry: "Historical movie exhibition (movie-showing venues — provisional spaces such as opera houses, concert halls, penny arcades, dime museums, burlesque houses, dance halls, airdomes, storefronts; and dedicated movie theaters — nickelodeons, movie houses, movie palaces)"
  country: "United States — Chicago, Illinois (75 officially designated community areas)"
  time_period: "1896–1927 (from the year movie projectors were introduced in the U.S. market through the beginning of the Hollywood Golden Age triggered by sound films)"
  units: "75 Chicago community areas (community-year observations in a continuous-time event-history split-spell file); the venue population covers 927 movie-showing venues comprising 286 provisional spaces and 641 dedicated movie theaters (453 nickelodeons, 166 movie houses, 22 movie palaces)"
  n: "75 communities (events: 49 communities experienced a first nickelodeon founding, 46 a first movie house or palace, 24 experienced neither); 927 movie-showing venues underlie the independent and control variables"

evidence:
  sample_n: "n of all movie-showing venues 5 927, n of dedicated movie theaters 5 641 (n of nickelodeons 5 453"
  sample_country: "that existed in Chicago, Illinois, between 1896, the"
  sample_industry: "Using archival data on all movie-showing venues in Chicago communities, 1896–1927"
  sample_time_period: "year when movie projectors were introduced to the"
  theories_overview: "For example, the density dependence model reveals"
  methods_overview: "of piecewise-exponential hazard rate models of a"
  keywords_source: "theater forms: nickelodeon, movie house, and movie palace. We advance scholarship on"
  hypotheses_source: "Hypothesis 1. The higher the cumulative number of"
  measures_overview: "measure the instantaneous rate of a community"
  findings_overview: "founding of its first nickelodeon increases by 24.7%."
---

# Before Birth: How Provisional Spaces Shape the Localized Emergence of New Organizational Forms

**Abstract**
The literature on evolution of organizational forms has remained largely silent on where the first organizational instance of a new form comes from, treating it as either a given or an outcome of random variation. We challenge this agnostic assumption by putting the first organizational founding into a specific spatiotemporal context and revealing the role of provisional spaces, defined as small-scale, easily accessible settings where market pioneers temporarily experiment with applications of an innovation before dedicated organizations emerge. We theorize that provisional spaces disseminate necessary information about an innovation and enable potential entrepreneurs to envision a new template for organizing. Therefore, geographic communities with a higher number of provisional spaces are more likely to host the first organization embodying a new form sooner than others. Using archival data on all movie-showing venues in Chicago communities, 1896–1927, we find empirical support for our theorizing. Community variance in volume and types of provisional spaces for movie projectors, such as opera houses and penny arcades, led to community-level differences in the emergence of distinct movie theater forms: nickelodeon, movie house, and movie palace. We advance scholarship on organizational form emergence by uncovering the role of provisional spaces in shaping localized opportunity structures.

**Research Question**
How do prebirth dynamics — that is, market pioneers' experimentation with an innovation in preexisting "provisional spaces" — affect the emergence patterns of the first organizational instances of a new form across geographic communities? In particular, where and when does the first organization dedicated to exploiting an innovation appear, and which type of new form arises locally?

**Hypotheses / Propositions**
- H1 (positive): The higher the cumulative number of provisional spaces in a geographic community, the higher the probability that the community founds its first dedicated organization — the first movie theater of any form.
- H2 (positive / accelerating): The higher the number of provisional spaces that perceptually cluster into a specific proto-form, the sooner the community experiences its first venture founding embodying a form with features similar to that proto-form (highbrow spaces → movie house/palace; lowbrow spaces → nickelodeon).
- H3 (negative / delaying): The higher the number of provisional spaces that cluster into a specific proto-form, the later the community experiences its first founding embodying a form with features dissimilar from that proto-form (e.g., lowbrow spaces delay the highbrow movie house/palace; highbrow spaces delay the lowbrow nickelodeon).

**Mechanism Process**
- IV(s): Cumulative number of provisional spaces in a community (all types; highbrow; lowbrow), discounted 25% per year and lagged one year.
- DV(s): Community-level instantaneous founding rate of (a) the first dedicated movie theater of any form, (b) the first nickelodeon (lowbrow form), and (c) the first movie house or palace (highbrow form), 1896–1927.
- Mediators: Not formally tested as variables; the theorized cognitive mechanism is the emergence of a community-specific "proto-form" — a provisional template for organizing — perceived by potential entrepreneurs.
- Moderators: The same-type alignment between provisional space (lowbrow vs. highbrow) and the form being founded; the paper predicts that mismatched provisional spaces (e.g., highbrow spaces vis-à-vis nickelodeons) delay rather than accelerate same-community emergence.

The proposed mechanism is that, during the prebirth stage between an innovation's creation and the founding of the first dedicated organization, market pioneers experiment in small-scale, accessible preexisting venues. This experimentation disseminates community-specific knowledge about possible applications and gives rise to a proto-form that potential founders use as a template. Where lowbrow (or highbrow) provisional spaces accumulate, potential founders perceive a corresponding proto-form, accelerating emergence of a same-form dedicated organization (nickelodeon, or movie house/palace) and slowing the dissimilar one. Localized opportunity structure thus arises endogenously from the ecology of provisional spaces within a place.

**Data & Measures**
- Data: Archival population of 927 movie-showing venues (286 provisional spaces; 641 dedicated movie theaters = 453 nickelodeons, 166 movie houses, 22 movie palaces) across 75 officially designated Chicago community areas, 1896–1927. Venue and cultural-status data come from directories, movie-theater histories, IMDb, and the Chicago Tribune Display Ad section (used to date the earliest movie showings); community demographics come from the Local Community Fact Book, U.S. Census, and Encyclopedia of Chicago. Highbrow vs. lowbrow status was coded with a Theater Historical Society of America archivist from show type, ticket price, architecture, and operating philosophy.
- DV: Community's instantaneous founding rate (hazard) of its first movie theater, modeled separately for (a) any form (H1), (b) the lowbrow nickelodeon, and (c) the highbrow movie house or palace (H2/H3); communities with no founding by 1927 are right-censored.
- IV: Community-specific cumulative count of provisional spaces from 1896 to year t — all spaces (H1), highbrow, and lowbrow (H2/H3) — discounted 25% per year and lagged one year to avoid simultaneity.
- Controls (lagged one year): log human population, normalized community median income, % with at least a high-school degree, % foreign-born, dwelling density, university dummy, % professional workers, recreational-reputation dummy, average movie runtime, number of films released, and neighboring communities' density of the emerging form.
- Estimation / identification: continuous-time event-history analysis with piecewise-exponential hazard models estimated by maximum likelihood (Stata stpiece) on a split-spell file, with robust Huber–White standard errors clustered by community. The design is associational/archival — the authors describe the relationships as correlational, not causal — and inference is supported by a placebo test (provisional spaces should not predict trade-school emergence) plus robustness checks using alternative discount rates and discrete-time complementary log-log models. No formal mediation is tested; the proto-form is the theorized, unmeasured cognitive mechanism.

**Key Findings**
- H1 corroborated: the cumulative number of all provisional spaces significantly increases the founding rate of the first movie theater of any form (Model 4.2, b = 0.601, robust SE = 0.248); moving the count from 0 to its mean raises the founding probability by 30.3%.
- H2 supported in both same-form tests: highbrow provisional spaces significantly increase the first movie house/palace founding rate (Model 4.4, b = 1.085, SE = 0.372; +38.5% at the mean), and lowbrow provisional spaces significantly increase the first nickelodeon founding rate (Model 4.6, b = 1.578, SE = 0.394; +24.7% at the mean).
- H3 only partially corroborated (asymmetric): as predicted, lowbrow provisional spaces significantly delay the first highbrow movie house/palace (Model 4.4, b = −0.877, SE = 0.323; founding rate −11.6% at the mean), but highbrow provisional spaces have no significant effect on the first lowbrow nickelodeon (Model 4.6, b = 0.385, SE = 0.290, n.s.). The authors state: "Considered together, Hypotheses 1 and 2 are strongly supported. Hypothesis 3 is partially corroborated."
- Robustness: results hold under alternative discount rates and discrete-time event-history models, and a placebo analysis finds that provisional spaces do not predict the emergence of trade schools.

**Theoretical Contribution**
The paper develops a predictive theory of provisional spaces that situates the first organizational instantiation of a new form in a concrete spatiotemporal context, displacing the prevailing "genetics view" that treats the first organization as random variation. It introduces the concept of a proto-form to link prebirth experimentation to community-specific categorization processes, and articulates an ecological perspective on spaces that connects place-level form emergence to populations of small accessible settings within a community.

**Practical Implication**
Managers should recognize that experimenting with novel technology in their existing organizations can seed dedicated competitors that later substitute for them. Entrepreneurs can locate opportunities to found new organizational forms by attending to which preexisting community organizations are experimenting with a novel technology. Policy-makers can accelerate localized emergence of desired new forms by subsidizing, publicizing, and diversifying provisional spaces within their communities.

**Limitations**
The empirical setting is an organizational form that emerged successfully, so generalizability to forms that gestated but failed to materialize is uncertain. The archival design lacks exogenous shocks or matched comparisons, so the documented relationships between provisional spaces and first foundings are correlational rather than causal. The historical, single-city scope (Chicago) and reliance on directories and newspaper advertisements may also miss provisional spaces that left no archival trace.

**Future Research**
Researchers should study contemporary prebirth dynamics ethnographically (e.g., via Technology Transfer Offices) to observe how managers and would-be founders perceive proto-forms in real time. Internet-era data sources — online forums, review sites, discussion boards, and the Wayback Machine — can extend the framework to digitally-mediated emergence. Future work could also examine how factors such as inventor fame, infrastructure, and innovation aesthetics moderate the prebirth-to-emergence link, and explore non-U.S. contexts where culturally distinct provisional spaces (e.g., tea houses, stock exchanges) seeded early film exhibition.

**APA 7th Citation**
Li, Y., & Khessina, O. M. (2024). Before birth: How provisional spaces shape the localized emergence of new organizational forms. *Academy of Management Journal*, 67(2), 494–525. https://doi.org/10.5465/amj.2022.0897
