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
extraction_version: "v2"

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
---

# When Do Outside CEOs Underperform? From a CEO-Centric to a Stakeholder-Centric Perspective of Post-Succession Performance

**Abstract**
How does the appointment of an outside CEO affect the hiring firm's performance? Prior research has reported that outside CEOs tend to underperform compared to inside CEOs, with high performance variance. Extending CEO-centric perspectives, we predict that experiential learning enhances post-succession performance, while negative transfer learning undermines it. We then offer a novel, stakeholder-centric theoretical perspective, conjecturing that stakeholders' negative sentiment toward the CEO appointment undermines post-succession performance. We further conjecture that outside CEOs are less effective in leveraging their executive experience and suffer more from negative transfer and negative sentiment when compared to inside CEOs, who can leverage their familiarity and social embeddedness in the firm, which explains why outside CEOs may underperform. Analyzing the appointments of CEOs in U.S. public firms, we find that counter to expectations, the length and breadth of their executive experience do not explain either post-succession performance or the performance differences between outside CEOs and inside CEOs. Rather, the misfit between CEOs' corporate backgrounds and their firms' characteristics and the negative sentiment surrounding their appointments explain performance differences and the underperformance of outside CEOs. Accordingly, our study directs attention to the important yet previously understudied reactions of stakeholders to CEO appointments.

**Research Question**
Why do outside CEOs underperform relative to inside CEOs, and what drives the substantial heterogeneity in firm performance following CEO appointments? The paper asks whether established CEO-centric explanations (executive experience, corporate fit) or a newly proposed stakeholder-centric explanation (stakeholders' negative sentiment toward the appointment) better account for post-succession performance differences.

**Mechanism Process**
- IV(s): CEO experience length; CEO experience breadth; corporate misfit (incongruence between the CEO's prior corporate background and the appointing firm's age, size, and industry); negative stakeholder sentiment (textual analysis of media coverage around the appointment)
- DV(s): Post-succession firm performance (average industry-adjusted ROA over the three years following appointment)
- Moderators: Outside CEO (dummy = 1 if hired from outside the firm), which is hypothesized to strengthen the negative effects of corporate misfit (H4) and negative sentiment (H6) and weaken the positive effects of experience (H2)
- Mediators: None formally tested (mechanisms are theorized, not statistically mediated)

The authors juxtapose three theoretical mechanisms. From experiential learning theory, longer and broader executive experience should improve decision-making, but inside CEOs leverage familiarity and social embeddedness to convert experience into performance more effectively than outsiders. From negative transfer learning, corporate misfit leads CEOs to misapply "recipes" from dissimilar firms, harming performance—more so for outsiders who cannot diagnose contextual differences. From social cognition (negativity bias), stakeholders' negative sentiment toward an appointment escalates from scrutiny to withdrawn support, organizational resistance, and reputational damage, depressing performance—again more acutely for outsiders who lack embedded ties. Empirically, experience effects are null, while corporate misfit and negative sentiment significantly reduce performance and are amplified for outside CEOs.

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
