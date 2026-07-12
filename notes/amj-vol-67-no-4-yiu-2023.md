---
id: amj-vol-67-no-4-yiu-2023
title: "A Theory of Host Country Sentiments: An Illustration in Cross-Border Acquisitions"
authors:
  - "Yiu, D. W."
  - "Wan, W. P."
  - "Chen, K. X."
  - "Tian, X."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0239"
volume: 67
issue: 4
pages: "1024-1054"

source: "AMJ/vol-67-no-4"
pdf_path: "library/AMJ/vol-67-no-4/pdfs/Yiu 2023 A Theory of Host Country Sentiments An Illustration in Cross-Border Acquisitions.pdf"
text_path: "library/AMJ/vol-67-no-4/text/Yiu 2023 A Theory of Host Country Sentiments An Illustration in Cross-Border Acquisitions.txt"
ingested_at: "2026-05-06"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords: ["host country sentiments", "cross-border acquisitions", "sentiment dynamics", "sentiment analysis", "legitimacy", "emerging market firms"]
theory: ["theory of host country sentiments", "Durkheim's theory of collective effervescence", "ritual interactionist theory", "social constructionist theory", "sense-making theory", "institutional theory"]
topics: ["strategy-innovation", "mergers-acquisitions", "institutional-theory"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Logit regression analysis on 241 cross-border acquisition announcements; sentiment analysis using Stanford CoreNLP (lexicon-based Loughran-McDonald dictionary for deal sentiment, machine learning for acquirer and inward investment sentiment) on three corpora (9,533 + 30,120 + 9,741 documents); robustness checks include Heckman two-stage selection model, machine learning robustness test, shared corpora weighting, and impact threshold of confounding variable."
sample:
  industry: "Cross-border acquisitions across multiple industries (manufacturing, service, trade, financial, natural resources, high-tech, materials, telecommunications, hotel/real estate)"
  country: "United States (host country); China (home country)"
  time_period: "2013-2016"
  units: "Cross-border acquisition announcements by Chinese firms targeting U.S. firms"
  n: "241 acquisition announcements"

evidence:
  sample_n: "consists of 241 acquisi"
  sample_country: "Our study context is that of acquisitions by firms"
  sample_industry: "all acquisition attempts that targeted U.S. firms"
  sample_time_period: "announced by Chinese acquirers between 2013"
  theories_overview: "Synthesizing ritual interactionist"
  methods_overview: "we used logit regression analysis to test our"
  keywords_source: "We advocate the concept of \"host country"
  hypotheses_source: "Hypothesis 1. Host country sentiments toward (a) the"
  measures_overview: "country sentiments were measured as the polarity"
  findings_overview: "acquirer in Model 4 is positive and significant"
---

# A Theory of Host Country Sentiments: An Illustration in Cross-Border Acquisitions

**Abstract**
Capitalizing on massive sentiment diffusion and mobilization aided by mass media and social media nowadays, we introduce a general theory of host country sentiments to illuminate the granular, context-situated, and time dynamic power of social sentiments. We posit that host country is a value-laden context wherein a foreign entity's strategic action stimulates host country stakeholders' social sentiments and engagement in systems of discourses ("sentiment arousal"), mobilizes social sentiments toward the foreign entity ("sentiment competence"), and legitimizes social sentiments and the strategic action of the foreign entity ("sentiment resonance"). To test our theory, we employ a context of inward acquisitions by emerging market firms in an advanced economy, and postulate that host country sentiments toward objects of the inward acquisition (deal, acquirer, and inward investments from home country) will influence the likelihood of deal completion, an indication of host country legitimacy. We further highlight the patterns of host country sentiment dynamics, and showcase how sentiment volatility, wavelength, and augmentation exert heterogeneous effects on deal completion. Overall, we advocate a theory of host country sentiments in international management research that elucidates the interplay among host country sentiments, systems of social discourses, and multinational enterprise strategic outcomes in a host country.

**Research Question**
How do host country sentiments — socially constructed and collectively shared attitudes and emotional dispositions among host country stakeholders toward foreign entities — and their dynamics (volatility, wavelength, augmentation) influence the likelihood of cross-border acquisition deal completion?

**Hypotheses / Propositions**
- H1. Host country sentiments toward (a) the deal, (b) the acquirer, and (c) the inward investments from the home country are positively related to the likelihood of acquisition completion.
- H2. The higher the volatility of host country social sentiment toward (a) the deal, (b) the acquirer, and (c) the inward investments from the home country, the lower the likelihood of acquisition completion.
- H3. The shorter the wavelength of host country social sentiment toward (a) the deal, (b) the acquirer, and (c) the inward investments from the home country, the higher the likelihood of acquisition completion (wavelength predicted to be negatively related to completion).
- H4a. The sentiment augmentation effect between the acquirer and the deal is positively related to the likelihood of acquisition completion.
- H4b. The sentiment augmentation effect between the inward investments from the home country and the deal is positively related to the likelihood of acquisition completion.

**Mechanism Process**
- IV(s): Host country sentiments toward (a) deal, (b) acquirer, (c) inward investments from home country (China); sentiment dynamics (volatility, wavelength, augmentation) for each sentiment type
- DV(s): Acquisition completion (binary)
- Moderators: News coverage of the deal (post hoc analysis on sentiment volatility toward deal)
- Controls: Acquirer characteristics (size, public status, diversification, SOE status, acquisition experience, name with U.S. identity, subsidiary acquirer); target characteristics (public status, subsidiary); deal characteristics (same industry, minority ownership, financial acquisition); country-level variables (public opinion about China, political animosity toward China, frequency of inward acquisitions); year and industry dummies

The theory posits a three-stage mechanism: (1) sentiment arousal — a foreign entity's contentious strategic action in a value-laden host country stimulates stakeholders' sentiments and engagement in discourse; (2) sentiment competence — host country sentiments are mobilized via systems of discourses (mass and social media) underpinning rhythmic entrainment that gives rise to collective conscience; (3) sentiment resonance — host country stakeholders impose social judgment legitimizing or de-legitimizing the foreign entity's action. Sentiment dynamics (volatility, wavelength, augmentation) capture granular temporal patterns that exert heterogeneous effects on legitimation outcomes.

**Data & Measures**
- Data sources: Acquisition data from Thomson's SDC Platinum database (all attempts by Chinese acquirers targeting U.S. firms, 2013-2016). Host country sentiments were derived from three textual corpora scraped from news portals and platforms (e.g., Factiva, Bloomberg, Yahoo Finance, ThomsonONE, Seeking Alpha): deal (9,533 documents), acquirer (30,120 documents), and inward investments from China (9,741 documents).
- DV - Acquisition completion: binary, coded 1 if the deal was completed and 0 otherwise (66.4% of deals completed).
- IVs - Host country sentiments toward the deal, the acquirer, and inward investments from China: polarity scores (-1 to 1) from sentiment analysis using Stanford CoreNLP (lexicon-based Loughran-McDonald dictionary for the deal; machine-learning classifier for the acquirer and inward investments).
- Sentiment dynamics: volatility = standard deviation of differences in average sentiment values between adjoining time periods; wavelength = mean time distance between adjoining sentiment peaks; augmentation = cross-lag correlation between two sentiment types across adjoining periods.
- Controls: acquirer, target, deal, and country-level variables plus year and industry dummies (see Mechanism Process).
- Identification (in the paper's terms): logit regression on the dichotomous DV, with a Heckman two-stage selection model as a sample-selection check (the inverse Mills ratio was insignificant, so it was excluded from the main models) and a robustness-of-inference-to-replacement test for omitted-variable bias. The design is cross-sectional and associational rather than causal.

**Key Findings**
Support was heterogeneous across the eleven hypothesized effects (coefficients from the full model, Model 4; signs as reported by the paper).
- H1a supported: sentiments toward the deal positive and significant (b = 2.19, p < .05; average marginal effect 0.30, p < .05).
- H1b supported: sentiments toward the acquirer positive and significant (b = 6.06, p < .05).
- H1c supported: sentiments toward inward investments from China positive and significant (b = 6.35, p < .01).
- H2a NOT supported: contrary to the prediction, sentiment volatility toward the deal was positive and significant (b = 2.76, p < .01).
- H2b supported: sentiment volatility toward the acquirer negative and significant (b = -3.69, p < .05).
- H2c supported: sentiment volatility toward inward investments from China negative and significant (b = -22.09, p < .01).
- H3a supported: sentiment wavelength toward the deal negative and significant (b = -0.03, p < .01).
- H3b NOT supported: sentiment wavelength toward the acquirer insignificant.
- H3c supported: sentiment wavelength toward inward investments from China negative and significant (b = -0.40, p < .05).
- H4a NOT supported: sentiment augmentation between the acquirer and the deal positive but not significant.
- H4b supported: sentiment augmentation between inward investments from China and the deal positive and significant (b = 1.34, p < .01).

**Theoretical Contribution**
The paper introduces a novel general theory of host country sentiments that elevates sentiment-based social institutions in international and strategic management research. It synthesizes ritual interactionist, social constructionist, sense-making, and institutional perspectives by integrating situational, interactional, motivational, and cognitive elements of social sentiments. The conceptual differentiation of sentiment structures (deal, acquirer, inward investments) and sentiment dynamics (volatility, wavelength, augmentation) advances understanding of granular, time-dynamic effects of social sentiments on MNE legitimation outcomes.

**Practical Implication**
For acquirers from emerging markets like China, cross-border acquisitions easily turn into a public issue, and recognizing/managing the legitimacy of such acquisitions can make or break a planned deal. Firms contemplating acquisitions in developed economies should pay greater attention to host country sentiments, leverage sentiment analysis tools to monitor stakeholder discourse, and proactively manage stakeholders' social sentiments in systems of discourses facilitated by online media.

**Limitations**
The empirical context is limited to Chinese firm acquisitions of U.S. targets between 2013 and 2016, raising questions about generalizability to other country dyads with different bilateral relationships. The effects of host country sentiment volatility on deal completion produced inconclusive results requiring further investigation. Additionally, sentiment analysis relies on shared corpora that may have classification limitations, particularly for the dictionary approach where the subject of each sentence cannot be as easily identified.

**Future Research**
Future research can extend the theory using different country dyads (e.g., Korea, India as acquirers in the United States) to differentiate how host country sentiments affect inward acquisition outcomes from different home countries. The theory is generalizable to other salient inter-country events such as IPOs, foreign CEO appointments, MNE HR policies, and inter-country tensions. Future efforts can also investigate the inconclusive effects of host country sentiment volatility and explore cross-lag interactions between host country sentiment types.

**APA 7th Citation**
Yiu, D. W., Wan, W. P., Chen, K. X., & Tian, X. (2024). A theory of host country sentiments: An illustration in cross-border acquisitions. *Academy of Management Journal*, 67(4), 1024-1054. https://doi.org/10.5465/amj.2022.0239
