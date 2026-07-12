---
id: amj-vol-67-no-6-harmon-2024
title: "Divergent Market Reactions to Abstract Language: A Multicountry Event Study of European Central Bank Communications"
authors:
  - "Harmon, D."
  - "Mariani, M."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0814"
volume: 67
issue: 6
pages: "1553-1576"

source: "AMJ/vol-67-no-6"
pdf_path: "library/AMJ/vol-67-no-6/pdfs/Harmon 2024 Divergent Market Reactions to Abstract Language A Multicountry Event Study of European Central Bank Communications.pdf"
text_path: "library/AMJ/vol-67-no-6/text/Harmon 2024 Divergent Market Reactions to Abstract Language A Multicountry Event Study of European Central Bank Communications.txt"
ingested_at: "2026-05-05"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords: ["language abstraction", "strategic communication", "core-periphery", "event study", "European Central Bank", "audience heterogeneity"]
theory: ["world systems theory", "linguistic category model", "strategic ambiguity"]
topics: ["finance-accounting", "governance-leadership", "europe"]
unit_of_analysis: "country"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Multicountry event study using OLS regression on cumulative abnormal returns (CAR) over a three-day window (t-1 to t+1) around ECB speech events. World market model adjusts country-level returns against the STOXX Euro 600. Models include year, weekday, speaker, location, and language family fixed effects with standard errors clustered at the speech level."
sample:
  industry: "Stock market indices in eurozone economies (monetary policy / central banking communications)"
  country: "11 eurozone countries (Austria, Belgium, France, Germany, Italy, Netherlands, Finland, Ireland, Portugal, Greece, Spain)"
  time_period: "June 19, 1998 to December 31, 2015"
  units: "Country-speech observations (eurozone country market reactions to ECB president speeches)"
  n: "5,709 country-speech observations from 548 ECB president speeches across 11 countries"

evidence:
  sample_n: "consisted of 548 speeches: 129 by Duisenberg, 315"
  sample_country: "in 11 eurozone countries react to the abstract language"
  sample_industry: "major stock market index of eurozone member"
  sample_time_period: "speeches delivered between June 19, 1998, and"
  theories_overview: "(LCM). Developed by Semin and Fiedler"
  methods_overview: "we used ordinary least squares (OLS) regression to"
  keywords_source: "speeches delivered by the European Central Bank president"
  hypotheses_source: "Hypothesis 2. The divergent reaction from market"
  measures_overview: "We measure market reaction by"
  findings_overview: "actors in peripheral countries react more negatively."
---

# Divergent Market Reactions to Abstract Language: A Multicountry Event Study of European Central Bank Communications

**Abstract**
Prominent leaders regularly communicate with multiple markets around the world, but we know little about the challenges that can arise when trying to effectively convey one's message in a global setting. In this paper, we develop a theory about how language abstraction—a dominant strategy used to create common ground among diverse audiences—can become problematic when used in a global environment where market actors have divergent interests. Employing a multicountry event study, we analyze how the stock markets in 11 eurozone countries react to the abstract language in public speeches delivered by the European Central Bank president. We find that abstract language, rather than creating common ground, produces divergent market reactions across core and peripheral countries, such that market actors in core countries react more favorably to abstract communication, while those in peripheral countries prefer concrete communication. We also show that this divergent reaction is stronger when the economic interests of the core and the periphery are made more salient. This study contributes new insights to research on strategic communication in market settings, expands our understanding of audience heterogeneity and market power, and highlights the growing challenges of communicating in a globalized society.

**Research Question**
How does the abstractness of a powerful leader's communication affect market reactions across countries that occupy different positions (core vs. periphery) within a globally interconnected economic system, and when do divergent reactions intensify?

**Hypotheses / Propositions**
H1. The abstractness of an ECB president's speech produces divergent reactions from market actors in core versus peripheral countries, such that higher speech abstraction leads to more positive (negative) reactions from core (peripheral) countries.
H2. The divergent reaction from core versus peripheral countries is stronger when the eurozone's economic outlook is more pessimistic.
H3. The divergent reaction from core versus peripheral countries is stronger when the ECB has recently taken monetary policy action.

**Mechanism Process**
- IV(s): Speech abstraction (linguistic category model score combining DAVs, IAVs, SVs, adjectives, nouns)
- DV(s): Market reaction (cumulative abnormal returns of country-level stock market index, t-1 to t+1)
- Moderators: Core-periphery position of the country (Campos & Macchiarelli dynamic measure); pessimistic economic outlook (LIWC-based tone of speech); recent monetary policy action (interest rate change within three months)
- Controls: Inflation, unemployment, debt/GDP, extant market returns, ECB communications, voting power, speech word count, complexity, future focus, uncertainty, vagueness, topic-model topics

Drawing on world-systems theory, the authors argue that core and peripheral country actors hold divergent interests—core actors trust the establishment and prefer the status quo, peripheral actors are suspicious of vague claims and prefer change. Because abstract language is hard to verify and conveys stability, core-country investors react favorably while peripheral-country investors react unfavorably. Salience-amplifying conditions (pessimistic outlook, recent policy action) make these divergent interests more visible and intensify the divergent reaction.

**Data & Measures**
Data: the full population of 548 English-language ECB president speeches (129 Duisenberg, 315 Trichet, 104 Draghi) delivered June 19, 1998 to December 31, 2015, linked to daily returns of the primary stock market index in each of 11 eurozone countries (5,709 country-speech observations).
- DV (market reaction): cumulative abnormal returns (CAR) of each country's primary stock index over a three-day window (t-1 to t+1), using Park's (2004) world market model with the STOXX Euro 600 as the superordinate index.
- IV (speech abstraction): linguistic category model (LCM) score weighting descriptive action verbs, interpretative action verbs, state verbs, adjectives, and nouns (Semin & Fiedler 1988; dictionaries from Johnson-Grey et al. 2020).
- Moderator (core-periphery): Campos & Macchiarelli (2016, 2021) dynamic score from 0 (core) to 100 (periphery), based on how symmetrically a country responds to demand/supply shocks.
- Moderator (pessimistic outlook): reversed LIWC positive-minus-negative "tone" of each speech.
- Moderator (policy action): dummy coded 1 if the speech fell within three months of an ECB interest-rate change.

Estimation is associational: OLS on CAR with year, weekday, speaker, location, and language-family fixed effects and standard errors clustered at the speech level. Robustness includes a 150-specification curve and Frank's (2000) impact-threshold test for omitted variables; no experimental or quasi-experimental identification is claimed.

**Key Findings**
All three hypotheses were supported. H1: the speech abstraction × core-periphery interaction was significant (p < .001, Model 3); core-country markets react more positively and peripheral-country markets more negatively as speech abstraction rises, with the predicted core and periphery values diverging significantly at one SD above (p = .024) and one SD below (p = .019) the abstraction mean. H2: the three-way abstraction × core-periphery × pessimistic-outlook interaction was significant (p = .033, Model 4), so divergence is stronger when the eurozone outlook is more pessimistic. H3: the three-way abstraction × core-periphery × policy-action interaction was significant (p = .041, Model 5), so divergence is stronger within three months of an ECB rate change. Both three-way interactions remain significant in the fully saturated model (Model 6). Results are robust across a 150-specification curve and a replication using all 19 eurozone countries (H1 p < .001; H2 p = .032; H3 p = .042).

**Theoretical Contribution**
The study extends research on strategic communication in market settings by demonstrating that the same leader message produces divergent reactions across countries within an economic system, identifying the core-periphery divide as an important contingency for audience heterogeneity. It reconciles mixed prior findings on abstract vs. concrete language by showing that audience interests, not language alone, drive reactions, and surfaces a less-visible dimension of market power embedded in everyday communications.

**Practical Implication**
Leaders of supranational institutions, multinational firms, and global initiatives should not assume that abstract or generalized language will build consensus across stakeholders in different countries. When audiences span a core-periphery divide, the same speech can inadvertently produce divergent reactions, especially during pessimistic periods or after major policy actions, leaving open a trade-off between broadly abstract framing and more concrete communication for peripheral audiences.

**Limitations**
All ECB presidents in the sample come from core countries, so the theory's prediction for a peripheral-country leader is not empirically tested. The empirical setting (the eurozone) is one canonical core-periphery system, and generalization to settings with weaker or different divergent interests warrants further work.

**Future Research**
Future research could examine settings where leaders themselves come from peripheral positions, or other audience contexts with core-periphery structures (urban/rural voters, central/peripheral employees, financial network cores). Scholars could also explore when abstract language produces convergence—conditions under which divergent interests are absent or non-salient—and study other communication strategies leaders use to manage globally heterogeneous audiences.

**APA 7th Citation**
Harmon, D., & Mariani, M. (2024). Divergent market reactions to abstract language: A multicountry event study of European Central Bank communications. *Academy of Management Journal*, 67(6), 1553-1576. https://doi.org/10.5465/amj.2022.0814
