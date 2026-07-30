---
id: amj-vol-65-no-5-awate-2022
title: "A Trojan Horse Inside the Gates? Knowledge Spillovers During Patent Litigation"
authors:
  - "Awate, Kiran S."
  - "Makhija, Mona V."
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2018.1181"
volume: 65
issue: 5
pages: "1747-1769"

source: "AMJ/vol-65-no-5"
pdf_path: "library/AMJ/vol-65-no-5/pdfs/Awate 2022 A Trojan Horse Inside the Gates Knowledge Spillovers During Patent Litigation.pdf"
text_path: "library/AMJ/vol-65-no-5/text/Awate 2022 A Trojan Horse Inside the Gates Knowledge Spillovers During Patent Litigation.txt"
ingested_at: "2026-06-24"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-30"

paper_type: "empirical-quantitative"
keywords: ["patent litigation", "knowledge spillovers", "appropriability regime", "innovation", "organizational learning", "knowledge recency", "knowledge heterogeneity", "patent scope"]
theory: ["recombinant search / knowledge recombination view of innovation (Fleming, 2001; Katila & Ahuja, 2002; Fleming & Sorenson, 2004)", "appropriability regimes (Teece, 1986; Cohen, Nelson, & Walsh, 2000)", "organizational and vicarious learning (Hamel, 1991; Makhija & Ganesh, 1997; Posen & Chen, 2013)"]
topics: ["innovation-management", "competitive-strategy", "north-america", "longitudinal"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Longitudinal observational study of an unbalanced firm-therapeutic class-year panel. Conditional fixed-effects (Poisson) count models for novel drug approvals, with firm, therapeutic-class, and year fixed effects. Coarsened exact matching (CEM) addresses selection; two-stage Heckman models and an alternate citation-count DV provide robustness checks."
sample:
  industry: "U.S. pharmaceutical industry (domestic and foreign firms operating in the U.S. market, covered in Pharmaprojects); patents span 14 therapeutic classes"
  country: "United States"
  time_period: "1998 to 2015"
  units: "Firm-therapeutic class-year observations (accused vs. non-litigated pharmaceutical firms)"
  n: "22,486 firm-therapeutic-class-year observations for 169 firms (60 with a litigation event, 109 without); >3,000 patent litigation cases; CEM sample 4,705 observations / 359 firms"

evidence:
  sample_n: "consisted of 22,486 firm-thera"
  sample_country: "foreign pharmaceutical firms operating in the U.S."
  sample_industry: "U.S. pharmaceutical industry, in which firms expend"
  sample_time_period: "period 1998 to 2015"
  theories_overview: "An innovation comes about through recombining"
  methods_overview: "Poisson fixed-effects model well-suited"
  keywords_source: "knowledge may unintentionally spill over"
  hypotheses_source: "Hypothesis 1. Accused firms will have higher subsequent novel innovation output than firms not accused"
  measures_overview: "number of a firm’s novel drugs in a given therapeutic"
  findings_overview: "litigation event is positive and highly significant"
---

# A Trojan Horse Inside the Gates? Knowledge Spillovers During Patent Litigation

**Abstract**
While patent litigation is an important appropriability mechanism for protecting firms’ proprietary knowledge, through the litigation process, valuable knowledge may unintentionally spill over from firms defending their patents to those they accuse of patent infringement. We examine whether such spillover subsequently enhances the innovation of accused firms by analyzing over 3,000 patent litigation cases from 1998 through 2015 in the U.S. pharmaceutical industry. We find that firms accused of infringement have higher levels of innovation following litigation relative to other similar firms. Furthermore, litigation of patents that build on recent and heterogeneous knowledge and are characterized by greater scope more strongly enhance the accused firms’ subsequent innovation. These findings support the argument that patent litigation can facilitate knowledge spillovers.

**Research Question**
Does the knowledge that a patent-holding firm is compelled to disclose during patent infringement litigation spill over to the accused firm and enhance its subsequent novel innovation? And do attributes of the litigated patent's knowledge—its recency, heterogeneity, and scope—strengthen this effect?

**Hypotheses / Propositions**
- H1: Accused firms will have higher subsequent novel innovation output than firms not accused of patent infringement (positive).
- H2: The more recent the knowledge in the litigated patent, the higher an accused firm's subsequent novel innovation output over firms not accused of patent infringement (positive).
- H3: The more heterogeneous the litigated patent knowledge, the higher the subsequent novel innovation output of accused firms over firms not accused of patent infringement (positive).
- H4: The greater the scope of the litigated patent, the higher the accused firm's subsequent innovation output over firms not accused of patent infringement (positive).

**Mechanism Process**
- IV(s): Litigation event (accused-firm dummy); and, for the spillover-value hypotheses, knowledge recency, knowledge heterogeneity (entropy of secondary therapeutic classes), and knowledge scope (log number of patent claims) of the litigated patent
- DV(s): Accused firm's novel innovation output (count of novel FDA-approved drugs in a therapeutic class subsequent to litigation); robustness DV = citations of the litigated patent in the accused firm's subsequent patents
- Mediators: None formally modeled — knowledge spillover during litigation is the unobserved theorized channel between the litigation event and innovation
- Moderators: Knowledge recency, heterogeneity, and scope function as factors that increase the value of the spillover (modeled as direct effects on novel innovation, not interaction terms)

The argument rests on the recombinant view of innovation: novel inventions arise from recombining knowledge components, but the path to successful recombination is largely tacit and invisible in the patent itself. Litigation's disclosure rules (discovery, depositions, expert testimony) force the patent-holding firm to reveal procedural knowledge, rejected hypotheses, and causal linkages beyond the patent, creating unusually close colocation and proprietary spillovers to an accused firm that—operating in the same technological space—has both the intent and capacity to learn from them and apply them to its own subsequent innovation.

**Data & Measures**
Single-study observational panel. Sources combined: Pharmaprojects (domestic and foreign pharmaceutical firms operating in the U.S. market), COMPUSTAT via Wharton Research Data Services (financials), the USPTO (patents), Recombinant Capital (alliances), Westlaw (patent litigation cases), and the FDA (drug approvals). The original Pharmaprojects draw was 444 public and private firms — 132 that had undergone a litigation event and 312 that had not; after dropping firms lacking financial and other data for the full window, the main-analysis sample is 22,486 firm-therapeutic-class-year observations for 169 firms (60 with a litigation event, 109 without) over 1998 to 2015, an unbalanced panel across 14 therapeutic classes.
- DV: firm's novel innovation output = count of firm i's novel FDA-approved drugs in therapeutic class j in year t (novel = new molecular entities, or new combinations of existing entities offering significantly better treatment or much lower side effects; generics excluded). Sensitivity DV: number of citations of the litigated patent in the accused firm's subsequent patents.
- IV — litigation event: dummy coded 1 if focal firm i is accused of infringing a patent in therapeutic class j in year t − 5, and 0 otherwise. A rolling window of one to eight years was used to select the lag; five years yielded the strongest litigation-event coefficient.
- IV — knowledge recency: Heeley and Jacobson's (2008) formula applied to patents litigated against firm i in class j at t − 5, based on the gap between a focal patent's grant date and those of the patents it cites, benchmarked against the technology-class mean and standard deviation; only cited patents in the top 10th percentile of recency are included, so newer technological inputs score more positively.
- IV — knowledge heterogeneity: entropy index over the distribution of secondary therapeutic classes (k = 1, …, 13) recorded in Pharmaprojects for the patents litigated at t − 5; higher when more therapeutic classes are associated with the litigated patents.
- IV — knowledge scope: log of the number of claims in the litigated patents for firm i in therapeutic class j at t − 5.
- Controls (firm i, year t): prior novel drug approvals in the class over the prior five years, number of patents, R&D intensity, logged firm revenue (size proxy), logged firm age, active technology areas, research in different geography, codevelopment and licensing alliances in the last five years, merger-and-acquisition flag, patents filed in the firm's country of origin, co-occurring litigation, and other litigation as plaintiff.

Estimation in the paper's own terms: a Poisson fixed-effects model for the count DV, with firm fixed effects, 14 therapeutic-class dummies, and year dummies; the authors follow guidance to cluster standard errors at the firm (the highest level of aggregation) and report similar results with two-way clustering at firm and therapeutic-class levels. Selection is addressed with coarsened exact matching (CEM) on revenue, R&D intensity, patent output, and age, followed by a conditional fixed-effects Poisson model on the matched cross-section of 4,705 observations and 359 firms (66 with litigation events / 2,318 observations; 293 without / 2,387 observations). Endogeneity is addressed with a two-stage Heckman (1979) model whose first stage predicts subclass overlap between the accused firm's prior patents and the litigated patent, using the total number of subclasses in the accused firm's patents as the exclusion restriction. The design remains an observational panel: the theorized spillover channel is never directly measured, and identification rests on matching, fixed effects, and selection correction rather than on an experiment or exogenous shock.

**Key Findings**
- H1 supported. In the CEM matched sample (Table 2b) the litigation-event treatment variable has a positive and significant effect on accused firms' novel innovation outcomes (b = 0.369, p < .05). In the main analysis (Table 3, model 2) the litigation-event coefficient is positive and highly significant (b = 0.461, p < .001); the authors read this magnitude as litigation increasing the odds of an accused firm's novel drug discovery by 18%. They state that the CEM and main analyses together strongly confirm Hypothesis 1.
- H2 supported. Knowledge recency is positive and significant in both models 3 and 6 (b = 2.610, p < .05; b = 2.002, p < .05); a one-standard-deviation increase raises the odds of the accused firm's novel drug discovery by 7%.
- H3 supported. Knowledge heterogeneity is significant in both models 4 and 6 (b = 0.291, p < .05; b = 0.223, p < .05); a one-standard-deviation increase raises the odds of novel drug discovery by 14%.
- H4 supported. Knowledge scope is positive and significant in both models 5 and 6 (b = 0.091, p < .001; b = 0.080, p < .001); a one-standard-deviation increase raises the odds of novel drug discovery by 17%.
- Controls: three are statistically significant across models — prior drug approvals and licensing alliances raise subsequent innovation, while the number of active technology areas has a negative effect, which the authors read as specialization mattering for the ability to learn from spillovers. Remaining controls are not statistically significant, possibly because some are highly correlated with other controls.
- Robustness: with the alternate DV (citations of the litigated patent in the accused firm's subsequent patents, Table 4), results for the explanatory variables remain consistent with the main analysis, confirming all four hypotheses. In the two-stage Heckman models, the exclusion restriction is significantly associated with the first-stage outcome (p < .001) and the significant, negative inverse Mills ratio in the Table 6 second-stage models indicates the possibility of endogeneity; even so, the explanatory-variable results remain similar and provide additional support for the four hypotheses.

**Theoretical Contribution**
The study reveals an unforeseen, paradoxical consequence of a core appropriability mechanism: patent litigation, whose purpose is to curtail spillovers and protect proprietary knowledge, can itself generate valuable knowledge spillovers that strengthen a competitor. It is the first to demonstrate that litigation-driven spillovers enhance accused firms' novel innovation, and it sheds light on the micro-mechanisms (disclosure of recent, heterogeneous, and broad-scope knowledge) through which such learning occurs, highlighting the "double-edged sword" and the limits of strong appropriability regimes.

**Practical Implication**
Patent-holding firms should recognize that litigation entails a trade-off: defending the most valuable patents requires divulging additional proprietary, often procedural, knowledge that can strengthen rivals, so the litigation decision should weigh this risk of unintended spillover. The findings also raise—without endorsing—the strategic question of whether an accused firm's ability to learn from spillovers could help offset the costs of being litigated.

**Limitations**
The analysis holds technological class constant, and the authors note that specific disease areas or baseline technologies may have stronger effects on the hypothesized relationships; and the study assumes the patent-holding firm unintentionally spills knowledge during litigation, an assumption the authors invite subsequent research to reexamine.

**Future Research**
Future work could examine litigation involving contested patents of both firms (so spillovers accrue to each party), whether litigation outcomes (winning vs. losing) shape learning, and the trajectory of subsequent innovation in litigated versus non-litigated domains. Scholars could also study weaker-appropriability-regime industries, take a longitudinal view of whether patent-holding firms learn to limit spillovers over time, and revisit the assumption that disclosure is unintentional.

**APA 7th Citation**
Awate, K. S., & Makhija, M. V. (2022). A Trojan horse inside the gates? Knowledge spillovers during patent litigation. *Academy of Management Journal*, 65(5), 1747–1769. https://doi.org/10.5465/amj.2018.1181
