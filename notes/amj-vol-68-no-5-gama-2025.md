---
id: amj-vol-68-no-5-gama-2025
title: "Cross-Sector Relational Realignments after an Institutional Crisis: Checking the Instrumentalization of Corporate-Nonprofit Partnerships"
authors:
  - "Gama, M. A. B."
  - "Gatignon, A."
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0677"
volume: 68
issue: 5
pages: "1031-1054"

source: "AMJ/vol-68-no-5"
pdf_path: "library/AMJ/vol-68-no-5/pdfs/Gama 2025 Cross-Sector Relational Realignments after an Institutional Crisis Checking the Instrumentalization of Corporate-Nonprofit Partnerships.pdf"
text_path: "library/AMJ/vol-68-no-5/text/Gama 2025 Cross-Sector Relational Realignments after an Institutional Crisis Checking the Instrumentalization of Corporate-Nonprofit Partnerships.txt"
ingested_at: "2026-07-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["corporate-nonprofit partnerships", "government corruption scandals", "nonmarket strategy", "institutional crisis", "corporate political influence", "nonprofit legitimacy", "instrumentalization"]
theory: ["nonmarket strategy", "stakeholder management", "institutional change", "organizational legitimacy"]
topics: ["corporate-political-activity", "nonprofit-management", "stakeholder-engagement", "corruption-bribery"]
unit_of_analysis: "dyad"
level_of_theory: "macro"
dependent_variable_family: "social"
methods: "Multilevel mixed-effects (MLM) logit panel regression with random effects for nonprofit type and firm fixed effects; robust standard errors clustered by nonprofit type. Eight-year (2010-2017) firm-nonprofit dyadic panel of Brazilian publicly listed firms and registered nonprofits, with partnerships coded from annual reports via Python NLP; associational before/after (Operation Carwash) design (difference-in-differences deemed unsuitable). 54 semi-structured interviews illustrate the mechanisms."
sample:
  industry: "Publicly listed nonfinancial firms across 20 industries and registered nonprofits of all social missions"
  country: "Brazil"
  time_period: "2010-2017 (four years before and after Operation Carwash, 2014)"
  units: "Firm-nonprofit dyad-years"
  n: "10,488,578 dyad-year observations (approx. 440 firms per year; 820,000 registered nonprofits; 6,067 nonprofits cited in annual reports)"

# Mandatory evidence anchors (v3 — Layer 1 faithfulness audit).
evidence:
  sample_n: "All models include 10,488,578 observations, 10 groups of nonprofit types, and firm-fixed effects"
  sample_country: "firms and registered nonprofits in Brazil"
  sample_industry: "440 firms per year from 20 different industries"
  sample_time_period: "from 2010 to 2017, covering four years before and"
  theories_overview: "Nonmarket strategy has typically treated firms"
  methods_overview: "mixed effect (MLM) logit panel regression with"
  keywords_source: "how government corruption scandals influence corporate-nonprofit partnerships by altering the institutional context"
  hypotheses_source: "Hypothesis 1. A corporate-nonprofit partnership is"
  measures_overview: "dummy variable named tainted directly"
  findings_overview: "nonprofit partnership occurring (b 5 3.57; p , .001)"
---

# Cross-Sector Relational Realignments after an Institutional Crisis: Checking the Instrumentalization of Corporate-Nonprofit Partnerships

**Abstract**
We examine how government corruption scandals influence corporate-nonprofit partnerships by altering the institutional context in ways that reshape the value of nonmarket relationships. We analyze these dynamics following Operation Carwash (2014) in Brazil, using comprehensive data on all publicly listed firms and registered nonprofits from 2010 to 2017. We find that partnerships became more common after the scandal's disclosure, as firms and nonprofits sought to collaborate on socioeconomic development. However, firms seen as directly or indirectly implicated in the scandal struggled to form partnerships due to risks to nonprofits' legitimacy. Moreover, nonprofits perceived as closely aligned with firms (i.e., trade associations) or the state (i.e., education and research nonprofits or those with political capital) were especially cautious about entering partnerships to avoid appearing complicit in advancing corporate political influence. Our findings thus "check" the instrumentalization of corporate-nonprofit partnerships in two ways: by examining how it unfolds after an institutional crisis and by revealing how nonprofits resist being used as vehicles for corporate reputational repair or political gain. We show that such crises can trigger a broader realignment of corporate partnerships with nonmarket actors, highlighting the need to study shifts across nonmarket sectors, and not just within them.

**Research Question**
How do revelations of government corruption scandals influence corporate-nonprofit partnerships by altering the institutional context and shifting the benefits and risks for both parties?

**Hypotheses / Propositions**
H1. A corporate-nonprofit partnership is more likely to emerge after the disclosure of a government corruption scandal.
H2. The positive effect of a government corruption scandal on the likelihood of a corporate-nonprofit partnership is weaker if the firm is directly (H2a) or indirectly (H2b) tainted by the scandal.
H3. The positive effect of a government corruption scandal on the likelihood of a corporate-nonprofit partnership is weaker for trade associations (H3a) and education and research (E&R) nonprofits (H3b) relative to other nonprofit missions.
H4. The positive effect of a government corruption scandal on the likelihood of a corporate-nonprofit partnership is weaker when the nonprofit has more political capital.

**Mechanism Process**
- IV(s): Post — a dummy for the period after Operation Carwash's 2014 disclosure (0 = 2010-2013; 1 = 2014-2017).
- DV(s): Corporate-nonprofit partnership — a dyadic dummy equal to 1 if firm i and nonprofit j collaborate in year t.
- Mediators: None statistically tested; the shift in joint benefits and legitimacy risks is theorized rather than formally mediated.
- Moderators: Firm directly tainted (H2a); firm indirectly tainted via state ownership (SOE) and political board ties (H2b); nonprofit is a trade association (H3a); nonprofit is an education and research (E&R) nonprofit (H3b); nonprofit political capital (H4).

A highly mediatized government corruption scandal erodes institutionalized trust in government and shifts perceived value toward nonprofits, raising the joint benefits of socioeconomic-development partnerships and making partnerships more likely overall. The same crisis, however, heightens legitimacy risks: nonprofits avoid firms tainted directly or indirectly (state ownership, politically connected boards) to protect their own legitimacy, and the nonprofits most exposed to accusations of enabling corporate political influence — trade associations, E&R nonprofits, and those with more political capital — become especially cautious, "checking" their own instrumentalization to preserve the appearance of disinterested public service.

**Data & Measures**
Setting/design: an eight-year (2010-2017) firm-nonprofit dyadic panel spanning four years before and after Operation Carwash (2014) in Brazil. DV: corporate-nonprofit partnership, coded 1/0 from firms' annual reports (and available corporate-foundation reports) using Python NLP over 3,524 corporate and 252 foundation reports; the candidate nonprofit set (6,067 nonprofits) was cross-checked against the IPEA database of ~820,000 registered nonprofits. IV: Post (2014-2017 = 1). Moderators: tainted directly (dummy for the eight directly implicated firms); SOE (>49.9% government ownership); political board ties (count of political positions from 39,452 board-member résumés); trade association and E&R nonprofit (IBGE classifications); nonprofit political capital (count of positive nonprofit-government ties extracted from 324,150 Factiva articles via Python NLP and a 60% LIWC cutoff). Firm-, nonprofit-, and dyad-level controls (fines, compliance communication/department, campaign and municipal donations, ROA, market-to-book, leverage, size, nonprofit board ties, government resources, geographic scope, collaborative experience, established relationship). Estimation: multilevel mixed-effects (MLM) logit panel regression with random effects for nonprofit type and firm fixed effects, robust standard errors clustered by nonprofit type, across 10,488,578 dyad-year observations. The design is associational (Operation Carwash affected all firms, leaving no clean control group, so difference-in-differences was rejected); 54 semi-structured interviews illustrate the mechanisms.

**Key Findings**
H1 is supported: the post-Operation Carwash period positively predicts partnership formation (b = 3.57, p < .001; margins ≈ +2.32%, roughly 246 additional partnerships). H2 is partially supported. H2a is supported: being directly tainted weakens the effect (tainted-directly × post b = -0.36, p < .01; ≈ 44.05% less likely, 51 fewer partnerships for the eight implicated firms). H2b is only partially supported, depending on the indirect-taint measure: state ownership weakens the effect (SOE × post b = -0.38, p < .001; ≈ 0.7% less likely, 14 fewer partnerships for the 21 SOEs), but political board ties × post is only b = -0.001, p < .1, which the authors state does not support the hypothesis. H3 is supported: the effect is weaker for trade associations (H3a: b = -0.55, p < .001; ≈ 19 fewer partnerships) and for E&R nonprofits (H3b: b = -0.45, p < .001; ≈ 8 fewer partnerships). H4 is supported: more nonprofit political capital weakens the effect (b = -1.22, p < .001; ≈ 14 fewer partnerships). Results hold across numerous robustness tests (alternative partnership coding, continuous scandal-intensity measures, alternative fixed-effects and estimation specifications, and sample restrictions).

**Theoretical Contribution**
The study advances a more dynamic view of nonmarket strategy and stakeholder management by showing that an institutional crisis triggers a realignment of firms' partnerships across nonmarket sectors — political and nonprofit arenas jointly, not just within each — so cross-sector ties must be theorized together. It "checks" the instrumentalization of corporate-nonprofit partnerships, revealing the limits of leveraging nonprofits for reputational repair or political influence (even for firms not directly implicated) and showing how nonprofits actively resist co-optation to protect their legitimacy. It integrates corporate political activity with corporate social responsibility and specifies the institutional and organizational contingencies (taint, sector proximity to firms or the state, political capital) that determine when using nonprofits for political influence backfires.

**Practical Implication**
The findings can help firms and nonprofits adapt more quickly — or act more proactively and intentionally — in crafting partnership strategies when such scandals occur, and help managers better understand the benefits and risks of nonmarket ties from different perspectives. They can also support policymakers and society in recognizing the sometimes opaque implications of firms' relationships with the nonprofit sector for government and public trust.

**Limitations**
The design observes only partnerships that could have formed (realized and counterfactual dyads), not whether a firm or nonprofit declined a potential partnership or the reasons for doing so, and it cannot directly observe which combinations of firm and nonprofit characteristics drove collaboration; identifying explicit empirical measures of the potential benefits and risks to both parties, and how these jointly evolve after a scandal, is untenable. In addition, the scale of Operation Carwash — implicating an unusually broad set of high-profile politicians and businesspeople — is rare, which limits generalizability.

**Future Research**
The authors call for a configurational approach to extend the theory; tests of generalizability to other, likely smaller-scale, corruption scandals and to other institutional changes that introduce political uncertainty and devalue corporate political ties (e.g., Taiwan's Sunflower Movement); and cross-country analyses as anti-government and anti-corporate sentiments rise globally. They also point to examining the longer-term sustainability of the observed effects (whether they persist if attitudes swing back toward indifference about corporate political influence) and how results might change if nonprofits themselves faced government opposition or allegations of financial misconduct.

**APA 7th Citation**
Gama, M. A. B., & Gatignon, A. (2025). Cross-sector relational realignments after an institutional crisis: Checking the instrumentalization of corporate-nonprofit partnerships. *Academy of Management Journal, 68*(5), 1031–1054. https://doi.org/10.5465/amj.2023.0677
