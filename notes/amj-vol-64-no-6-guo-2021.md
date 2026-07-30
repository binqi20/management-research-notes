---
id: amj-vol-64-no-6-guo-2021
title: "The Impact of Executive Verbal Communication on the Convergence of Investors’ Opinions"
authors:
  - "Guo, W."
  - "Sengul, M."
  - "Yu, T."
year: 2021
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2019.0711"
volume: 64
issue: 6
pages: "1763-1792"

source: "AMJ/vol-64-no-6"
pdf_path: "library/AMJ/vol-64-no-6/pdfs/Guo 2021 The Impact of Executive Verbal Communication on the Convergence of Investors’ Opinions.pdf"
text_path: "library/AMJ/vol-64-no-6/text/Guo 2021 The Impact of Executive Verbal Communication on the Convergence of Investors’ Opinions.txt"
ingested_at: "2026-06-26"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["executive verbal communication", "investor opinion convergence", "content newness", "composition simplicity", "delivery unscriptedness", "earnings uncertainty", "sense-giving"]
theory: ["corporate communication literature", "sense-giving literature"]
topics: ["corporate-governance", "ceo-leadership", "financial-reporting", "quantitative-methods"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Fixed-effects regressions using second-by-second intraday stock trading data around earnings-call Q&A sessions; investor opinion convergence is measured as the change in bid-ask spread from the pre-event period to the event period, and communication attributes are measured with natural language processing and readability metrics."
sample:
  industry: "Firms operating across 237 four-digit Standard Industrial Classification industries."
  country: "Firms listed on the former American Stock Exchange, Nasdaq, and New York Stock Exchange."
  time_period: "Conference calls between January 1, 2005 and May 31, 2012."
  units: "Earnings conference call observations for publicly listed firms."
  n: "10,415 conference calls of 847 publicly listed firms."

evidence:
  sample_n: "10,415 conference calls of 847 publicly listed firms"
  sample_country: "firms listed on the former American Stock Exchange"
  sample_industry: "Standard Industrial Classification (SIC) industries."
  sample_time_period: "1, 2005, and May 31, 2012"
  theories_overview: "Building on the corporate communication and sense-giving literatures"
  methods_overview: "speaker and year-quarter fixed effects."
  keywords_source: "content newness, composition simplicity, and delivery unscriptedness"
  hypotheses_source: "we hypothesize that the newness, simplicity, and unscriptedness of executive verbal communication are all positively associated with investor opinion convergence"
  measures_overview: "the difference in the bid–ask spread between these"
  findings_overview: "delivery unscriptedness (p , .01) were positive and"
---

# The Impact of Executive Verbal Communication on the Convergence of Investors’ Opinions

**Abstract**
This paper studies the influence of executive verbal communication on the convergence of investors’ opinions, defined as reduction of differences in investors’ valuations. Building on the corporate communication and sense-giving literatures, we argue that executive verbal communication impacts investor opinion convergence through its influence not only on disclosure of new information, but also on the comprehensibility and credibility of the information conveyed. Accordingly, we hypothesize that the newness, simplicity, and unscriptedness of executive verbal communication are all positively associated with investor opinion convergence. We also argue that the effect of executive communication on investor opinion convergence will be amplified when investors have a greater demand for information as would be the case for those firms with higher earnings uncertainty. Using a unique research design and second-by-second intraday stock trading data from 10,415 conference calls of 847 publicly listed firms between 2005 and 2012, we found strong support for our predictions.

**Research Question**
How do the content, composition, and delivery of executive verbal communication during earnings-call Q&A sessions influence the convergence of investors' opinions? The paper also asks whether earnings uncertainty strengthens the relationships between communication newness, simplicity, unscriptedness, and investor opinion convergence.

**Hypotheses / Propositions**
Hypothesis 1. The level of content newness in executive communication is positively associated with investor opinion convergence.
Hypothesis 2. The level of composition simplicity in executive communication is positively associated with investor opinion convergence.
Hypothesis 3. The level of delivery unscriptedness in executive communication is positively associated with investor opinion convergence.
Hypothesis 4. The higher the focal firm's earnings uncertainty, the stronger the positive relationship between the level of (a) content newness, (b) composition simplicity, and (c) delivery unscriptedness in executive communication and investor opinion convergence.

**Mechanism Process**
- IV(s): Content newness, composition simplicity, and delivery unscriptedness in executives' verbal responses during the Q&A portion of earnings conference calls.
- DV(s): Investor opinion convergence, measured as the reduction in bid-ask spread from the pre-event period to the event period around the conference-call Q&A.
- Mediators: Not directly tested; the paper theorizes disclosure of new information, perceived comprehensibility, and perceived credibility as mechanisms.
- Moderators: Earnings uncertainty, measured primarily by the book-to-market ratio, with robustness checks using alternative uncertainty measures.

The paper argues that executive verbal communication narrows differences in investors' valuations by helping investors make sense of firm information. Content newness reduces information gaps, composition simplicity makes information easier to process and more credible, and delivery unscriptedness signals openness and makes communication more conversational and comprehensible. Regression results show positive associations between all three communication attributes and investor opinion convergence, and these associations are stronger when firms face higher earnings uncertainty.

**Data & Measures**
Single quantitative study on 10,415 earnings conference calls held by 847 firms listed on the former American Stock Exchange, Nasdaq, and NYSE between January 1, 2005 and May 31, 2012, assembled from five sources: per-second intraday stock trading data from the NYSE Trade and Quote (TAQ) database; historical trading data from the Center for Research in Security Prices (CRSP); conference-call transcripts from Refinitiv's Company Events Coverage database (formerly Thomson Reuters StreetEvents); annual and quarterly financial data from Compustat; and quarterly earnings and analysts' consensus forecasts from I/B/E/S. Retained calls were held between 11 a.m. and 2 p.m. EST, no more than two days but at least 90 minutes after the earnings announcement, and calls in which neither the management discussion (MD) nor the Q&A exceeded 200 words were dropped. The per-second data amount to roughly 110 million seconds of trading.
- DV, investor opinion convergence: the pre-event period bid-ask spread minus the event period bid-ask spread, where each spread is the average per-second difference between the best ask and best bid divided by the ask-bid midpoint, multiplied by 100. The pre-event period runs from 90 minutes to 15 minutes before the scheduled call start; the event period begins 20 minutes after the scheduled start (the typical Q&A start time) and ends 100 minutes later. A positive value indicates that investors' opinions converged.
- IV, content newness: the similarity between the content words executives used in the MD and in the Q&A, computed as the dot product of content-word count vectors with each word pair weighted by its Word2Vec text-embedding semantic similarity (embeddings from about 100 billion words of Google News data) rather than by plain cosine similarity, then reverse-coded and adjusted for document length following Lee (2016). Reported convergent validity: r = .10, p < .001, with the number of analyst questions in the Q&A.
- IV, composition simplicity: the Fog index of the Q&A, which combines average sentence length with the number of words of three or more syllables, reverse-coded by subtracting it from 24 (the sample maximum plus 1). The sample mean Fog index was 15.42 (SD 1.93).
- IV, delivery unscriptedness: one minus the cosine similarity of function-word count vectors for the MD and Q&A documents, adjusted for document length following Lee (2016). Q&A unscriptedness ranged from 4% to 44% in the sample, with a mean of 16%.
- Moderator, earnings uncertainty: the book-to-market ratio, calculated as the book value of shareholders' equity at the end of the most recent quarter before the call divided by the market value of outstanding shares at the end of that quarter (mean .63, SD .47). Four alternatives were used in robustness tests: analysts' forecast dispersion, debt-to-equity ratio, income volatility, and return volatility.
- Controls: firm size (logged number of employees), firm slack (current ratio), firm performance (ROA), negative and positive earnings surprise (entered separately, each the absolute deviation of reported quarterly earnings from analysts' median consensus scaled by stock price), pre-announcement spread, return volatility (SD of monthly returns over the prior 12 months), share turnover (average daily trading volume over the prior 12 months), analyst coverage (logged number of covering analysts), call length (logged Q&A word count), and call tenor (positive emotion words divided by all emotion words, using LIWC).

The three independent variables are standardized, and the models are regressions with speaker fixed effects (the executive who spoke the most words on a given call) and year-quarter fixed effects, with robust standard errors clustered by firm. The design is associational rather than experimental or quasi-experimental: the authors argue that intraday data and the pre-event versus event comparison limit confounding from the earnings announcement and other same-day events, but they do not claim a causal identification strategy for the communication attributes themselves. Omitted-variable and endogeneity concerns are instead addressed with impact threshold of a confounding variable (ITCV) tests, a two-stage Heckman model for selection into the 11 a.m. to 2 p.m. window, a two-stage model instrumenting content newness with whether a general counsel is among the firm's top-five highest paid executives, and a two-stage model instrumenting delivery unscriptedness with the number of security-related class action lawsuits in the firm's four-digit SIC industry in the prior year.

**Key Findings**
All four hypotheses are supported in the main models.
- H1 supported: content newness is positively and significantly associated with investor opinion convergence (coefficient = .115, SE = .057, p < .05, Model 2).
- H2 supported: composition simplicity is positively and significantly associated with convergence (coefficient = .017, SE = .008, p < .05, Model 2).
- H3 supported: delivery unscriptedness is positively and significantly associated with convergence (coefficient = .022, SE = .008, p < .01, Model 2).
- Economic significance, holding other variables at their means: convergence was 11.5% higher for Q&A sessions one standard deviation above rather than below the mean on content newness, 14.0% higher on composition simplicity, and 18.2% higher on delivery unscriptedness. For an average firm with a pre-call spread of $.216 per share, these correspond to differences of $.026, $.031, and $.040 per share.
- H4 supported: the interaction with earnings uncertainty is positive and significant for content newness (coefficient = .268, p < .05, Model 3), composition simplicity (coefficient = .030, p < .01, Model 4), and delivery unscriptedness (coefficient = .027, p < .01, Model 5). Simple slope tests show that when earnings uncertainty is high all three attributes significantly predict convergence (content newness = .19, p < .05; composition simplicity = .08, p < .001; delivery unscriptedness = .06, p < .001), whereas when earnings uncertainty is low the effects of simplicity and unscriptedness are only marginally significant (p < .10) and the effect of content newness is not significant.
- H4 support is partial across alternative moderator measures: substituting analysts' forecast dispersion, debt-to-equity ratio, income volatility, or return volatility for the book-to-market ratio, the interaction with content newness was significant only when return volatility was used, while the interactions with composition simplicity and delivery unscriptedness stayed positive and significant regardless of which alternative was used.
- Supplementary tests of interdependence among the three attributes (Table 4): the composition simplicity by delivery unscriptedness interaction is positive and highly significant (p = .004), the content newness interactions with simplicity (p = .526) and with unscriptedness (p = .877) are not significant, and the three-way interaction is negative and significant only at the 10% level (p = .088). The authors read this as simplicity and unscriptedness being complements while content newness operates independently of them.
- Control-variable results: earnings uncertainty, return volatility, negative earnings surprise, and pre-announcement spread are positively and significantly related to convergence, whereas firm size, firm slack, share turnover, and analyst coverage are negatively and significantly related to it; positive earnings surprise is positive but not significant.
- The two-stage models preserve the direction of the main results: instrumented content newness remains positively and significantly related to convergence (p < .05), as does instrumented delivery unscriptedness (p < .05), and the Heckman selection term was not significant (p = .73).

**Theoretical Contribution**
The paper contributes to corporate communication research by examining content, composition, and delivery together and by adding delivery unscriptedness to work that had emphasized written or content-based communication. It extends sense-giving theory by arguing that executive communication affects financial-market audiences not only through impression management but also through the comprehensibility, credibility, and information value of what executives say. It also introduces investor opinion convergence as a strategy-relevant outcome and uses intraday trading data to isolate investor reactions to executive communication more precisely.

**Practical Implication**
The paper offers no practical-implications section. Its findings indicate that providing new information, using simpler language, and responding in a less scripted manner are associated with greater investor opinion convergence, especially when earnings uncertainty is high — against a baseline in which, per the National Investor Relations Institute survey the paper cites, most companies script answers to potential questions. The paper also notes a tradeoff: less scripted communication may increase information value and perceived credibility, but it can also raise the risk of mistakes or unpolished delivery.

**Limitations**
The study is constrained by data availability because it uses conference-call transcripts, which allow the authors to study unscriptedness but not other delivery attributes such as voice volume, pitch, pauses, inflection, facial expression, eye contact, or hand gestures. The analysis focuses on investors and, in supplementary analyses, analysts, so the effects on other external constituents such as journalists and regulators are not tested. Investor opinion convergence is proxied by bid-ask spread, which captures aggregated agreement rather than direct individual investor opinions.

**Future Research**
Future research could examine other verbal and nonverbal delivery attributes using audio or audiovisual data. Additional work could test whether executive verbal communication shapes the perceptions of other stakeholder groups with different information demands. The paper also encourages research using alternative measures of investor opinion convergence, including experiments, simulations, social-media data, or direct measures of individual investors' valuations.

**APA 7th Citation**
Guo, W., Sengul, M., & Yu, T. (2021). The impact of executive verbal communication on the convergence of investors’ opinions. *Academy of Management Journal*, 64(6), 1763-1792. https://doi.org/10.5465/amj.2019.0711
