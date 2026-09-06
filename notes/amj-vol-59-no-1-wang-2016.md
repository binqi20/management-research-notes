---
id: amj-vol-59-no-1-wang-2016
title: "Protecting Market Identity: When and How Do Organizations Respond to Consumers’ Devaluations?"
authors:
  - "Wang, Tao"
  - "Wezel, Filippo Carlo"
  - "Forgues, Bernard"
year: 2016
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2014.0205"
volume: 59
issue: 1
pages: "135-162"

source: "AMJ/vol-59-no-1"
pdf_path: "library/AMJ/vol-59-no-1/pdfs/Wang 2016 Protecting Market Identity When and How Do Organizations Respond to Consumers’ Devaluations.pdf"
text_path: "library/AMJ/vol-59-no-1/text/Wang 2016 Protecting Market Identity When and How Do Organizations Respond to Consumers’ Devaluations.txt"
ingested_at: "2026-07-03"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "gpt-6-astra"
augmented_at: "2026-09-06"

paper_type: "empirical-quantitative"
keywords: ["market identity", "consumer devaluations", "expert evaluations", "public responses", "organizational reputation", "justification"]
theory: ["evaluation literature", "identity literature", "market identity literature", "organizational reputation"]
topics: ["organizational-identity", "theory-development", "strategy-innovation"]
unit_of_analysis: "organization"
level_of_theory: "macro"
dependent_variable_family: "social"
methods: "Empirical-quantitative study of TripAdvisor hotel reviews, using review-level logit models for public response occurrence and OLS models with Heckman correction for LIWC-coded justification in responses."
sample:
  industry: "Hotels and hospitality"
  country: "United Kingdom, focused on London hotels"
  time_period: "2002-2012"
  units: "TripAdvisor reviews, hotel-reviewer pairs, and public responses by London hoteliers"
  n: "209,950 reviews"

evidence:
  sample_n: "209,950 reviews"
  sample_country: "all hotels located in London"
  sample_industry: "hotel ratings section of TripAdvisor"
  sample_time_period: "period 2002–2012"
  theories_overview: "evaluation and identity literatures"
  methods_overview: "organized at the review level"
  keywords_source: "consumer evaluations that challenge their market identity"
  hypotheses_source: "devaluation, the higher the likelihood that the"
  measures_overview: "created by subtracting the consumers’ overall rating"
  findings_overview: "the longer the responses are, and the more causal,"
---

# Protecting Market Identity: When and How Do Organizations Respond to Consumers’ Devaluations?

**Abstract**
This article examines the conditions under which organizations publicly respond to unfavorable consumer evaluations that challenge their market identity. Because organizations’ market identities are certified by expert evaluations, consumers’ devaluations that challenge these expert evaluations represent an identity threat. However, organizations do not always react to consumers’ devaluations because of the risks associated with public responses. Hence, we first predict that organizations are more likely to respond to severe devaluations than to weaker ones; second, we propose that organizations, when faced with severe devaluations, are more likely to craft responses that justify their actions and behaviors. We further contend that, for any market identity under consideration, an organization’s reputation amplifies these relationships. Analyses of a dataset of London hoteliers’ responses to online reviews posted on TripAdvisor during the period 2002–2012 lend substantial support to our hypotheses.

**Research Question**
The paper asks when organizations publicly respond to consumer devaluations that challenge their market identity and how they craft those public responses. It examines whether the severity of devaluation and organizational reputation shape both the likelihood of response and the degree of justification used in the response.

**Hypotheses / Propositions**
- H1a: The more severe a consumer devaluation, the higher the likelihood that the affected organization will engage in a public response.
- H1b: The more severe a consumer devaluation, the more the affected organization will engage in justification, reflected in the rationalization and deflection used in its public response.
- H2a: For any given market identity, the better an organization’s reputation, the stronger the positive relationship between the extent of devaluation and the likelihood of its public response.
- H2b: For any given market identity, the better an organization’s reputation, the stronger the positive relationship between the extent of devaluation and the justification used in its public response.

**Mechanism Process**
- IV(s): Severity of consumer devaluation, measured as the gap between expert hotel-class ratings and consumers’ overall TripAdvisor ratings.
- DV(s): Occurrence of organizational public response; justification in public responses, captured through response length and LIWC categories for causal, insight, exclusive, and motion words.
- Mediators: Not reported in paper.
- Moderators: Organizational reputation, measured through TripAdvisor ranking, moderates the effects of devaluation on response occurrence and justification.

The mechanism is that expert evaluations certify market identity and set consumers’ expectations, so consumer ratings below expert ratings create an identity threat. As devaluation becomes more severe, the benefit of publicly defending the organization’s market identity outweighs the risks of drawing attention to complaints or appearing defensive. Reputation amplifies this sensitivity because highly ranked organizations have more to lose from devaluations, although the evidence for reputation’s effect on response style is limited and varies across justification measures.

**Data & Measures**
The observational dataset contains 209,950 TripAdvisor reviews of 596 London hotels, including 62,440 consumer devaluations and 33,286 reviews receiving public responses. Table 2 reports 209,818 observations in Models 1–2 and 209,194 in Models 3–4; Table 4 analyzes 33,286 responses, with 374 hotel and eight star-level clusters. Response occurrence is a binary indicator that an online review received a public reply. Devaluation equals the expert hotel-class rating minus the consumer’s overall rating when the latter is lower, and zero otherwise; both ratings range from one to five. Market identity is captured by hotel stars. Reputation is measured by log-transformed TripAdvisor ranking: smaller values indicate better reputation, and the measure does not vary over time.

Justification is measured with LIWC. Rationalizing efforts are proxied by log response word count and the percentages of causal and insight words; deflection efforts are proxied by the percentages of exclusive and motion words. The word-percentage outcomes are log-transformed in Table 4. Greater justification is expected to involve longer responses, more causal, insight, and exclusive words, and fewer motion words. Logit models in Stata 12 examine response occurrence; OLS models examine response style, incorporating a Heckman correction through the inverse Mills ratio for selection into responding. Models control for hotel and review characteristics, year and travel reason, and, in the focal within-class specifications, hotel stars; robust standard errors are clustered at hotel and star levels. These analyses estimate associations rather than experimentally identified effects.

Additional analyses examine changes in the average rating across the ten reviews before and ten reviews after a focal devaluation. They cover 62,440 devaluations involving 586 hotels, with Table 5 using all 62,440 events in Models 15–16 and the 10,911 devaluations receiving responses in Models 17–21.

**Key Findings**
H1a was supported: greater devaluation was associated with a higher likelihood of public response (Table 2, Model 3: b = 0.131, p < .001), equivalent to about 14% higher odds per unit of devaluation. H2a was supported: the devaluation × log ranking interaction was negative (Model 4: b = −0.234, p < .001); because lower ranking values represent better reputation, the association between devaluation and response likelihood was stronger among more reputable hotels.

H1b received substantial support. In Table 4’s models without interactions, devaluation was positively associated with log response length (b = 0.130), causal words (b = 0.167), insight words (b = 0.195), and exclusive words (b = 0.265), and negatively associated with motion words (b = −0.049); all p < .001. H2b received only limited support. The interaction with log ranking was negative for insight words (b = −0.041, p < .01) and marginal for response length (b = −0.032, p < .10), while interactions for causal and exclusive words were not significant. The motion-word interaction was also negative (b = −0.041, p < .05); the paper describes this pattern as the attenuation of lower-ranked hotels’ greater use of motion words as devaluation increases.

In the additional analyses of subsequent ratings, responding and longer responses were associated with attenuation of devaluation’s negative relationship with later evaluations (Table 5: devaluation × responding b = 0.015; devaluation × log response length b = 0.021; both p < .05). None of the corresponding interactions with the four word-category measures was significant. These observational results provide initial evidence about subsequent evaluations, without establishing causal benefits of responding.

**Theoretical Contribution**
The paper shifts identity-threat research from internal-external mismatches toward consumer challenges to expert-certified market identities. It contributes to market identity research by treating organizations as active defenders of market identity after evaluations occur, not only as passive subjects of third-party evaluations. It also extends research on ratings, rankings, and performativity by showing that public evaluations elicit organizational responses under specific conditions rather than automatically.

**Practical Implication**
Managers in service industries should monitor whether consumer evaluations devalue the organization relative to expert benchmarks, not only whether reviews are negative in absolute terms. When responding publicly, they should craft responses that credibly justify actions and address would-be customers’ interpretations, because response style can shape subsequent evaluations.

**Limitations**
The authors limit the conceptual development to consumer evaluations that are lower than expert evaluations, leaving over-evaluations and changes in expert ratings outside the scope. They also note that market identity may include persistent and malleable characteristics, but the study does not distinguish how responses differ across those characteristics. The study does not isolate the sources of disagreement between experts and consumers and focuses on one public-response channel without analyzing the full qualitative content of consumer reviews.

**Future Research**
Future research could examine what happens when consumers rate organizations more highly than experts or when expert ratings change without corresponding consumer updates. It could also distinguish responses to persistent versus malleable identity characteristics and analyze the qualitative content of consumer reviews to better understand why expert-consumer disagreements arise. Additional work combining online data, archival data, and interviews could test whether the findings generalize across response channels.

**APA 7th Citation**
Wang, T., Wezel, F. C., & Forgues, B. (2016). Protecting market identity: When and how do organizations respond to consumers’ devaluations? *Academy of Management Journal*, 59(1), 135-162. https://doi.org/10.5465/amj.2014.0205
