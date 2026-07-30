---
id: amj-vol-65-no-5-keil-2022
title: "When Do Outside CEOs Underperform? From a CEO-Centric to a Stakeholder-Centric Perspective of Post-Succession Performance"
authors:
  - "Keil, Thomas"
  - "Lavie, Dovev"
  - "Pavicevic, Stevo"
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2018.1087"
volume: 65
issue: 5
pages: "1424-1449"

source: "AMJ/vol-65-no-5"
pdf_path: "library/AMJ/vol-65-no-5/pdfs/Keil 2022 When Do Outside CEOs Underperform From a CEO-Centric to a Stakeholder-Centric Perspective of Post-Succession Performance.pdf"
text_path: "library/AMJ/vol-65-no-5/text/Keil 2022 When Do Outside CEOs Underperform From a CEO-Centric to a Stakeholder-Centric Perspective of Post-Succession Performance.txt"
ingested_at: "2026-06-24"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["CEO succession", "outside CEO", "post-succession performance", "stakeholder sentiment", "negative transfer learning", "corporate misfit", "executive experience"]
theory: ["experiential learning theory (Kolb, 1984; Quinones, Ford, & Teachout, 1995)", "negative transfer learning (Ellis, 1965; Dokko, Wilk, & Rothbard, 2009)", "social cognition / negativity bias (Fiske & Taylor, 1991; Rozin & Royzman, 2001)", "stakeholder theory (Dorobantu, Henisz, & Nartey, 2017)"]
topics: ["ceo-leadership", "upper-echelons-theory", "stakeholder-theory"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Archival panel study of CEO appointments; two-stage Heckman-style selection (first-stage probit predicting succession) with second-stage generalized least squares (GLS) regression, clustered robust standard errors at the firm level, year fixed effects, and inverse Mills ratio control; Python-based textual sentiment analysis of press coverage (Harvard IV-4 dictionary) to construct the negative sentiment measure."
sample:
  industry: "S&P 500 and S&P 400 MidCap publicly traded firms spanning 55 two-digit SIC industries"
  country: "United States"
  time_period: "2001-2014"
  units: "CEO appointment events (882 firms; 318 outside-CEO and 957 inside-CEO appointments)"
  n: "1,275 CEO appointments"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "Our final sample included 1,275 appointments in"
  sample_country: "Analyzing the appointments of CEOs in U.S. public firms"
  sample_industry: "882 firms in 55 two-digit SICs, including 318"
  sample_time_period: "2001–2014 in Compustat"
  theories_overview: "drawing from social cognition"
  methods_overview: "ized least squares (GLS) regression with clustered"
  keywords_source: "we introduce a novel stakeholder-centric"
  hypotheses_source: "Hypothesis 3. The greater the misfit between a CEO’s"
  measures_overview: "We measured performance with return on assets"
  findings_overview: "negative sentiment surrounding their appointments explain performance differences and the underperformance of outside CEOs"
---

# When Do Outside CEOs Underperform? From a CEO-Centric to a Stakeholder-Centric Perspective of Post-Succession Performance

**Abstract**
How does the appointment of an outside CEO affect the hiring firm's performance? Prior research has reported that outside CEOs tend to underperform compared to inside CEOs, with high performance variance. Extending CEO-centric perspectives, we predict that experiential learning enhances post-succession performance, while negative transfer learning undermines it. We then offer a novel, stakeholder-centric theoretical perspective, conjecturing that stakeholders' negative sentiment toward the CEO appointment undermines post-succession performance. We further conjecture that outside CEOs are less effective in leveraging their executive experience and suffer more from negative transfer and negative sentiment when compared to inside CEOs, who can leverage their familiarity and social embeddedness in the firm, which explains why outside CEOs may underperform. Analyzing the appointments of CEOs in U.S. public firms, we find that counter to expectations, the length and breadth of their executive experience do not explain either post-succession performance or the performance differences between outside CEOs and inside CEOs. Rather, the misfit between CEOs' corporate backgrounds and their firms' characteristics and the negative sentiment surrounding their appointments explain performance differences and the underperformance of outside CEOs. Accordingly, our study directs attention to the important yet previously understudied reactions of stakeholders to CEO appointments.

**Research Question**
Why do outside CEOs underperform relative to inside CEOs, and what drives the substantial heterogeneity in firm performance following CEO appointments? The paper asks whether established CEO-centric explanations (executive experience, corporate fit) or a newly proposed stakeholder-centric explanation (stakeholders' negative sentiment toward the appointment) better account for post-succession performance differences.

**Hypotheses / Propositions**
- H1a: The greater the length of executive experience of a newly appointed CEO, the better the appointing firm's subsequent performance (positive).
- H1b: The greater the breadth of executive experience of a newly appointed CEO, the better the appointing firm's subsequent performance (positive).
- H2: The positive association between the appointing firm's post-appointment performance and the CEO's (a) length and (b) breadth of executive experience will be weaker for an outside CEO appointment than for an inside CEO appointment (negative moderation by outsider status).
- H3: The greater the misfit between a CEO's prior corporate background and the appointing firm's organizational characteristics, the worse the firm's performance becomes following the CEO appointment (negative).
- H4: Following a CEO appointment, the negative performance effect associated with corporate misfit will be stronger for an outside CEO appointment than for an inside CEO appointment (negative moderation).
- H5: The greater the stakeholders' negative sentiment concerning the appointment of a CEO, the worse the appointing firm's performance following the appointment (negative).
- H6: The negative association between stakeholders' negative sentiment concerning the appointment of a CEO and the appointing firm's post-appointment performance will be stronger for an outside CEO appointment than for an inside CEO appointment (negative moderation).

**Mechanism Process**
- IV(s): CEO experience length; CEO experience breadth; corporate misfit (incongruence between the CEO's prior corporate background and the appointing firm's age, size, and industry); negative stakeholder sentiment (textual analysis of media coverage around the appointment)
- DV(s): Post-succession firm performance (average industry-adjusted ROA over the three years following appointment)
- Moderators: Outside CEO (dummy = 1 if hired from outside the firm), which is hypothesized to strengthen the negative effects of corporate misfit (H4) and negative sentiment (H6) and weaken the positive effects of experience (H2)
- Mediators: None formally tested (mechanisms are theorized, not statistically mediated)

The authors juxtapose three theoretical mechanisms. From experiential learning theory, longer and broader executive experience should improve decision-making, but inside CEOs leverage familiarity and social embeddedness to convert experience into performance more effectively than outsiders. From negative transfer learning, corporate misfit leads CEOs to misapply "recipes" from dissimilar firms, harming performance—more so for outsiders who cannot diagnose contextual differences. From social cognition (negativity bias), stakeholders' negative sentiment toward an appointment escalates from scrutiny to withdrawn support, organizational resistance, and reputational damage, depressing performance—again more acutely for outsiders who lack embedded ties. Empirically, experience effects are null, while corporate misfit and negative sentiment significantly reduce performance and are amplified for outside CEOs.

**Data & Measures**
Single archival study (no multi-study design). Data: all CEO appointments in S&P 500 and S&P 400 MidCap publicly traded U.S.-based firms during 2001-2014, identified in Compustat's ExecuComp and then verified against firms' annual reports and press items; the final sample is 1,275 appointments in 882 firms across 55 two-digit SICs, comprising 318 outside-CEO and 957 inside-CEO appointments. Interim appointments, merger-driven appointments, CEO tenures shorter than a year, appointments with no press items, unverifiable career histories, and appointments with missing career-firm data were excluded. CEO career histories came from BoardEx, validated against ExecuComp, Bloomberg, Forbes, annual reports and proxy statements via Edgar, press items via LexisNexis, and corporate websites; financial data came from Compustat and Orbis (missing values from Edgar); founding dates from SEC filings, press items, corporate websites, Bloomberg, and Funding Universe.

- DV — Post-Succession Firm Performance: average industry-adjusted ROA over the first three years following the appointment (the median ROA of firms in the firm's primary two-digit SIC is subtracted from the firm's own ROA each year, then averaged across the three years).
- IV — CEO Experience Length: accumulated number of months spent in executive positions prior to the appointment (mean 181.54).
- IV — CEO Experience Breadth: number of firms in which the CEO had held executive positions prior to the appointment (mean 2.07).
- IV — Corporate Misfit: three 0-1 normalized indicators comparing the appointing firm with each firm in the CEO's executive career history — industry (graded four-digit SIC match), size (absolute log difference in employees), and age (absolute log difference in years since founding) — each weighted by the proportion of the CEO's career length spent in that firm/industry, then averaged (mean 0.21).
- IV — Negative Sentiment: Python textual-analysis algorithm over 27,092 LexisNexis press items (average 21 per appointment) published from three months before to three months after the announced appointment; counts of Harvard IV-4 negative-dictionary words appearing within a 10-word distance of the CEO's name, divided by the number of press items for that appointment (mean 0.94).
- Moderator — Outside CEO: dummy coded 1 if the newly appointed CEO was not employed by the firm prior to the appointment, 0 otherwise (mean 0.25).
- Controls: firm size, firm age, pre-succession firm performance, firm type (S&P 500 vs. MidCap), board size, board independence, TMT-CEO similarity, post-succession TMT change, CEO education, CEO duality, predecessor CEO founder, predecessor CEO dismissal, industry munificence, and year fixed effects.

Identification is associational rather than experimental. To address the non-randomness of succession, the authors pool firm-year observations (including firm-years without appointments) and estimate a first-stage probit predicting CEO succession with firm-clustered standard errors (n = 13,279 firm-years; Table A2), using the predecessor CEO's age and the industry's rate of CEO succession as exclusion restrictions, and carry the inverse Mills ratio into the second stage as the control "l CEO Succession". Second-stage hypothesis tests use generalized least squares (GLS) with clustered robust standard errors at the firm level and year fixed effects; maximum VIF is 2.18. Endogeneity in the decision to hire an outsider is separately addressed with a control function approach — a firm-clustered first-stage probit predicting an outside-CEO appointment, using the industry rate of outside-CEO appointments and the availability of an internal CEO candidate as exclusion restrictions, whose residuals are added as a control.

**Key Findings**
Results are from the full model (Model 10, Table 2; n = 1,275, standardized coefficients, two-tailed tests).

- H1a not supported: CEO experience length is negative and nonsignificant (β = -0.03, ns).
- H1b not supported: CEO experience breadth is negative and nonsignificant (β = -0.04, ns) in the full model.
- H2a not supported ("gained no support"): CEO experience length × Outside CEO is positive and nonsignificant (β = 0.02, ns).
- H2b not supported as predicted: rather than a weaker positive effect for outsiders, the authors report a marginally stronger negative effect for outside CEOs (β = -0.11, p < .10), and conclude that while breadth is "marginally more detrimental to outside CEOs," it "is not the main cause of this performance difference."
- H3 supported: corporate misfit negatively affects post-succession performance (β = -0.06, p < .05); a one-standard-deviation increase in misfit reduces post-succession performance by 1.6%.
- H4 supported: Corporate Misfit × Outside CEO is negative (β = -0.22, p < .001); a one-standard-deviation increase in misfit produces an extra 5.6% performance decline for outside CEOs relative to inside CEOs.
- H5 supported: negative sentiment undermines post-succession performance (β = -0.10, p < .001); a one-standard-deviation increase is associated with a 2.6% decline. The authors note this effect is more significant than that of corporate misfit and suggest negative sentiment may be the primary cause of post-succession performance heterogeneity.
- H6 supported: Negative Sentiment × Outside CEO is negative (β = -0.12, p < .05); negative sentiment leads to an extra 3.1% performance decline for outside CEOs relative to inside CEOs.
- With all predictors included, the Outside CEO main effect turns positive (β = 0.22, p < .001), which the authors read as evidence that the model effectively accounts for the disadvantages of outside CEOs.

Robustness: results hold with a one-year lag and with a five-year industry-adjusted ROA window, and with return on sales, but not with return on investment; market-based performance measures mostly yielded no effects. Narrowly defined C-suite-only or CEO-only experience measures also produced no significant performance effects. Decomposing corporate misfit, the age and industry components are more significant than the size component; measuring corporate fit as the inverse of misfit left results intact other than the coefficient sign change. Alternative word distances of 8 and 12 words gave consistent sentiment results, and a composite index adding analyst, director/executive (insider stock sales), and employee (Glassdoor) sentiment left the findings intact. Firm, board, and TMT size restrain the negative-sentiment effect (board size drives this result), whereas board independence does not mitigate it, and firm reputation proxies (firm age, S&P 500 affiliation) show non-significant moderation. The control function approach for outsider selection produced consistent findings.

**Theoretical Contribution**
The study's primary contribution is introducing a stakeholder-centric theoretical perspective to CEO succession—conceptualizing stakeholders' negative sentiment as a socio-cognitive bias that is a previously overlooked yet powerful driver of post-succession performance and of inside-versus-outside performance differences. Its secondary contribution extends CEO-centric perspectives by importing negative transfer learning into the succession domain to theorize "corporate misfit" between a CEO's background and the firm's characteristics, showing misfit harms all CEOs but more so outsiders. Together, juxtaposing multiple lenses reveals that experience—long the dominant explanation—does not explain performance heterogeneity, whereas misfit and sentiment do.

**Practical Implication**
Boards are advised that appointing an outside CEO can pay off regardless of the length or breadth of the candidate's experience, as long as the outsider's corporate background fits the firm's industry, age, and size and stakeholders' negative sentiment is mitigated. Boards should treat the succession process and stakeholder reactions as mattering at least as much as selection criteria, proactively managing stakeholder integration and sentiment for incoming CEOs.

**Limitations**
Reliance on archival data prevented observing the actual post-appointment decisions CEOs make, and the keyword-based sentiment measure could not isolate when sentiment was tied to objective CEO skills (though experience and fit were controlled). The inferred negative-sentiment measure captures sentiment level but not its origin, and the methods could not trace the temporal dynamics of how sentiment evolves after appointment.

**Future Research**
Future work could use surveys to identify the origins of negative sentiment and qualitative methods to study its temporal dynamics and the proposed micro-mechanisms (scrutiny, deprived support, resistance, reputational damage). Scholars might examine counteractions (e.g., image management, public relations) that CEOs and boards can take to mitigate sentiment, identify additional boundary conditions, use task-based rather than time-based experience measures, and extend the experience/misfit logic to other TMT members.

**APA 7th Citation**
Keil, T., Lavie, D., & Pavicevic, S. (2022). When do outside CEOs underperform? From a CEO-centric to a stakeholder-centric perspective of post-succession performance. *Academy of Management Journal*, 65(5), 1424–1449. https://doi.org/10.5465/amj.2018.1087
