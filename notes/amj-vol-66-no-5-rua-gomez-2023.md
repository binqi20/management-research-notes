---
id: amj-vol-66-no-5-rua-gomez-2023
title: "Reaching for the Stars: How Gender Influences the Formation of High-Status Collaboration Ties"
authors:
  - "Rua-Gomez, Carla"
  - "Carnabuci, Gianluca"
  - "Goossen, Martin C."
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.0218"
volume: 66
issue: 5
pages: "1501-1528"

source: "AMJ/vol-66-no-5"
pdf_path: "library/AMJ/vol-66-no-5/pdfs/Rua-Gomez 2023 Reaching for the Stars How Gender Influences the Formation of High-Status Collaboration Ties.pdf"
text_path: "library/AMJ/vol-66-no-5/text/Rua-Gomez 2023 Reaching for the Stars How Gender Influences the Formation of High-Status Collaboration Ties.txt"
ingested_at: "2026-05-20"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-quantitative"
keywords: ["high-status connections", "collaboration ties", "gender", "geographic proximity", "network proximity", "third-party ties", "star scientists", "social capital"]
theory: ["status expectation theory (Foschi, 2000; Ridgeway & Smith-Lovin, 1999)", "social capital theory (Lin, 2002; Oldroyd & Morris, 2012)", "Blau's structural theory of proximity (Blau, 1952, 1977)"]
topics: ["gender-in-organizations", "teams-collaboration", "social-capital-theory"]
unit_of_analysis: "dyad"
level_of_theory: "cross-level"
dependent_variable_family: "social"
methods: "Binary logistic regression on a matched-sample, dyadic (star-nonstar-year) panel with firm and year fixed effects and standard errors clustered at the star-nonstar dyad level; nearest-neighbor matching of female to male nonstars on tenure, prior patents, and competence area."
sample:
  industry: "Pharmaceutical research and development (R&D) laboratories"
  country: "United States (American R&D departments of the 42 largest pharmaceutical companies)"
  time_period: "1985-2010"
  units: "Star-nonstar scientist dyad-years (first-time collaboration risk set)"
  n: "2.04 million female nonstar observations matched to an equal number of male nonstar observations"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "balanced sample of 2.04 million female nonstar obser"
  sample_country: "American laboratories of the 42 largest pharma"
  sample_industry: "pharmaceutical R&D labs are an exemplar case of a"
  sample_time_period: "pharmaceutical companies between 1985 and 2010"
  theories_overview: "theory, for example, posits that gender acts as a sta"
  methods_overview: "regression with firm and year fixed-effects to control"
  keywords_source: "structural factors—geographic and network proximity—affect men"
  hypotheses_source: "Hypothesis 1. Female nonstar scientists are less likely"
  measures_overview: "Female nonstar is a dummy variable for the gender"
  findings_overview: "women who are geographically colocated with a “star” colleague are less likely to form a tie with that colleague compared to male peers"
---

# Reaching for the Stars: How Gender Influences the Formation of High-Status Collaboration Ties

**Abstract**
Extant research has shown that it is harder for women than for men to form high-status connections in the workplace. Extending this line of research, we examine how two structural factors—geographic and network proximity—affect men's and women's chances of forming high-status connections. Using data on the formation of collaboration ties with star scientists within the research and development laboratories of the 42 largest pharmaceutical companies between 1985 and 2010, we show that women who are geographically colocated with a "star" colleague are less likely to form a tie with that colleague compared to male peers who are similarly colocated, and that this difference persists irrespective of the star's gender. Conversely, women benefit more than men do from network proximity, as indicated by the presence of common third-party ties, and this difference widens if the star colleague is also a woman. By illuminating how geographic and network proximity affect the chances of forming high-status connections differently for women than for men, our study goes beyond the notion that women have reduced access to workplace social capital and expands consideration to the structural factors that underpin—that is, amplify or reduce—that disadvantage.

**Research Question**
How do two structural factors—geographic proximity and network proximity—differently affect men's versus women's chances of forming high-status collaboration ties with star scientists, and how does the star colleague's own gender condition these effects?

**Hypotheses / Propositions**
- Baseline Hypothesis (i). Being geographically colocated with a star scientist increases a nonstar scientist's likelihood of forming a collaboration tie with that star scientist.
- Hypothesis 1. Female nonstar scientists are less likely than male nonstar scientists to form a collaboration tie with a star scientist with whom they are geographically colocated.
- Hypothesis 2a. The effect postulated by Hypothesis 1 is weaker if the star scientist is a woman.
- Hypothesis 2b (competing with 2a). The effect postulated by Hypothesis 1 is stronger if the star scientist is a woman.
- Baseline Hypothesis (ii). Having third-party ties in common with a star scientist increases a nonstar scientist's likelihood of forming a collaboration tie with that star scientist.
- Hypothesis 3. Female nonstar scientists are more likely than are male ones to form a collaboration tie with a star scientist with whom they share common third-party ties.
- Hypothesis 4a. The effect postulated by Hypothesis 3 is weaker if the star scientist is a woman.
- Hypothesis 4b (competing with 4a). The effect postulated by Hypothesis 3 is stronger if the star scientist is a woman.

**Mechanism Process**
- IV(s): Geographic colocation (star and nonstar in the same geographic/commuting cluster); third-party ties (a shared common collaborator with the star); nonstar gender (Female nonstar); and gender-dyad dummies (e.g., Female star–female nonstar)
- DV(s): First-time collaboration—formation of a new copatenting tie between a star and a nonstar scientist in the current year (~0.1% base rate)
- Mediators: Not modeled directly; the theorized pathway is the credibility of competence signals under gender stereotypes (face-to-face agency signaling vs. third-party endorsement)
- Moderators: Nonstar gender moderates both baseline effects (H1, H3); the star's gender further moderates these gender gaps (competing H2a/H2b for colocation; competing H4a/H4b for third-party ties)

Drawing on status expectation theory and Blau's structural argument about spatial proximity, the authors argue that colocation rewards stereotypically male agentic self-promotion, so women profit less than men from being geographically near a star (H1, supported). Network proximity instead lets a third party convey stereotype-congruent, person-specific endorsements that override gender bias, so women benefit more than men from third-party ties (H3, supported). Because female stars share female nonstars' minority status yet also face a "favoritism threat," the star's gender amplifies the network-proximity advantage for female nonstars while leaving the colocation disadvantage persistent regardless of star gender.

**Data & Measures**
- Data sources: European Patent Office (EPO) patent applications — both granted applications and failed ones — for the American R&D departments of the 42 largest pharmaceutical companies (all PhRMA members in 1985), with scientists traced through the inventor names appearing on firms' patent applications; Mergent WebReports for firm financial and operational data; U.S. Social Security Administration first-name records for scientist gender (96% matched, raised to 99.5% through manual searches of LinkedIn, public profiles and Google, with the residual 0.5% classified as male). A dozen field interviews with star and nonstar scientists informed the setting.
- DV — First-time collaboration: dyadic dichotomous variable set to 1 if the star and nonstar scientist collaborated for the first time in the current year, observed as coauthorship of a patent application.
- Star status: the 5% most productive R&D scientists within each firm, based on a five-year count of patent applications.
- IV — Geographic colocation: dichotomous, set to 1 if star and nonstar belong to the same geographic cluster, assigned by a "city clustering algorithm" run on the location data in each scientist's most recent patent application (median distance 12 miles for colocated dyads versus 725 miles for non-colocated ones).
- IV — Third-party ties: dichotomous, set to 1 if the star and nonstar had at least one collaborator within the firm in common, identified from patent applications filed during the five years before the current year.
- Gender variables: Female nonstar dummy; in some models, four star–nonstar gender-dyad dummies with Male star–male nonstar as the reference category.
- Controls: star tenure, star prior patents, star current projects, nonstar tenure, nonstar prior patents, potential star collaborators, and same competence area, plus firm and year dummies; skewed controls entered log-transformed.
- Identification (in the paper's terms): a matched-sample design using nearest-neighbor matching — each female nonstar–star–year observation matched to a male nonstar paired with the same star, firm and year, within a 5% range on tenure, prior patents and same competence area (matches found for 89% of female nonstars) — estimated with binary logistic regression carrying firm and year fixed effects and standard errors clustered at the star–nonstar dyad level (4,098,128 observations). The authors describe the study as nonexperimental and caution against interpreting the estimates as evidence of causality. Robustness checks include rare-event logistic regression, a Cox proportional hazards event-history model, dyad-level random effects, looser matching margins and the unmatched sample, alternative colocation and third-party-tie measures, and a replication on USPTO data.

**Key Findings**
Support is heterogeneous across the eight hypotheses; coefficients below are logit coefficients with signs as reported by the paper.
- Baseline Hypothesis (i) supported: geographic colocation raises the probability of forming a first-time tie (model 1: b = 1.756, p < .001) — in marginal terms, colocation increases that probability by nearly 5.8 times.
- Hypothesis 1 supported: the Geographic colocation × Female nonstar interaction is negative (model 4: b = −0.343, p < .001); colocation raises the tie probability 4.9 times for a female nonstar versus 6.8 times for a male nonstar.
- Hypotheses 2a and 2b both unsupported: a Wald test cannot reject equality between Male star–female nonstar × Geographic colocation (b = −0.324, p < .01) and Female star–female nonstar × Geographic colocation (b = −0.562, p < .01) in model 8 (χ² = 1.22, p = .270), so women's colocation disadvantage persists irrespective of the star's gender; the authors read this as the minority-status homophily and favoritism-threat mechanisms cancelling each other out.
- Baseline Hypothesis (ii) supported: common third-party ties raise the probability of forming a first-time tie (model 1: b = 2.369, p < .001) — by a factor of 10.6.
- Hypothesis 3 supported: the Third-party ties × Female nonstar interaction is positive (model 4: b = 0.294, p < .001); a third-party tie raises the likelihood of collaboration nine-fold for male nonstars but more than twelve-fold for female nonstars.
- Hypothesis 4b supported and Hypothesis 4a not: Female star–female nonstar × Third-party ties (b = 0.645, p < .001) is significantly larger than Male star–female nonstar × Third-party ties (b = 0.260, p < .001) in model 8 (Wald χ² = 6.52, p = .011), so third-party ties are especially beneficial for female nonstars when the star is also a woman — the paper estimates this catalyzing effect is over 50% larger with a female than a male star.
- Unhypothesized direct effect: female nonstar scientists are 10% less likely than their male peers to form ties with star scientists (model 1: b = −0.101, p < .01).
- Post hoc: splitting stars at median organizational tenure, Female star–female nonstar × Geographic colocation is negative and significant in the below-median-tenure subsample but positive and nonsignificant in the above-median-tenure subsample — colocation raises a female nonstar's chance of tying to a recently hired female star by a factor of 3.4 versus 6.1 for a long-tenured female star. The third-party effect is largest among female nonstars with few prior patents and those whose main competence area differs from the star's.

**Theoretical Contribution**
The paper moves beyond the established finding that women have reduced access to high-status social capital to specify the structural mechanisms that amplify or reduce that disadvantage, showing that men and women rely on different pathways (colocation vs. third-party ties) into high-status networks. It advances understanding of how status heterophily shapes tie formation by integrating social-psychological accounts of gender stereotyping into Blau's structural theory, and reframes the debate on high-status women from whether they help other women toward the conditions under which they do so.

**Practical Implication**
Organizations should pair sensitization to agency-stereotype bias in face-to-face settings with interventions that deliberately build third-party (sponsorship) ties between low-status women and high-status colleagues, since such ties are an especially powerful lever when women's competence is hard to signal. The increasing geographic dispersion of knowledge work may itself narrow the gender gap in high-status connections.

**Limitations**
The nonexperimental design precludes strong causal claims; proximity may follow rather than precede collaboration intentions, and matched nonstars may differ on unobserved dimensions. EPO patent data may miss collaborations that never result in a patent filing, risking false negatives in the tie-formation measure, and the study does not examine gendered differences in failed collaborations.

**Future Research**
The authors call for field or lab experiments to establish causation, studies of how the theorized effects change over time as the share of (star) women rises and organizations grow more geographically dispersed, and research on how virtual collaboration technologies and remote work shape men's and women's ability to signal competence and form high-status ties.

**APA 7th Citation**
Rua-Gomez, C., Carnabuci, G., & Goossen, M. C. (2023). Reaching for the stars: How gender influences the formation of high-status collaboration ties. *Academy of Management Journal*, 66(5), 1501–1528. https://doi.org/10.5465/amj.2021.0218
