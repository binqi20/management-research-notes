---
id: amj-vol-66-no-5-ross-2023
title: "Resource Idling and Capability Erosion"
authors:
  - "Ross, Jan-Michael"
  - "Li, Toby X."
  - "Hawk, Ashton"
  - "Reuer, Jeffrey J."
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2020.1050"
volume: 66
issue: 5
pages: "1334-1359"

source: "AMJ/vol-66-no-5"
pdf_path: "library/AMJ/vol-66-no-5/pdfs/Ross 2023 Resource Idling and Capability Erosion.pdf"
text_path: "library/AMJ/vol-66-no-5/text/Ross 2023 Resource Idling and Capability Erosion.txt"
ingested_at: "2026-05-20"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-quantitative"
keywords: ["resource idling", "capability erosion", "demand uncertainty", "sunk costs", "real options", "human capital", "automation"]
theory: ["resource-based view", "real options theory"]
topics: ["strategy-innovation", "competitive-strategy", "resource-based-view", "dynamic-capabilities"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Longitudinal archival panel of Texas oil drillers (Drillinginfo, RigData, Texas Railroad Commission, EIA). Firm capabilities estimated as residual intrinsic drilling speed from a project-level OLS first stage. H1 tested with firm fixed-effects regressions plus treatment-effect analysis (propensity score matching, inverse probability weighting, doubly robust estimation); H2-H4 tested with firm fixed-effects logit models of rig idling, standard errors clustered by firm."
sample:
  industry: "Onshore oil and gas drilling (drilling contractors operating rig fleets)"
  country: "United States (Texas)"
  time_period: "2001-2018 (18 years)"
  units: "Drillers, rigs; firm-year level (capability erosion) and rig-month level (idling decisions)"
  n: "102 drillers and 1,396 rigs; 301,536 rig-month observations in the idling logit models"

evidence:
  sample_n: "1,396 rigs with complete records of their activities"
  sample_country: "oil drilling contractors in Texas"
  sample_industry: "on oil and gas wells drilled using rigs in Texas over a"
  sample_time_period: "from 2001 to 2018"
  theories_overview: "Building on the resource-based view and real options theory, we argue that resource"
  methods_overview: "We estimate using the logit"
  keywords_source: "and a greater reliance on human capital as opposed"
  hypotheses_source: "Hypothesis 2. Demand uncertainty has a negative"
  measures_overview: "the driller “stacks” a given rig in month t by suspending its drilling operations"
  findings_overview: "greater proportion of rigs is associated with a decline"
---

# Resource Idling and Capability Erosion

**Abstract**
Why would some firms persist with continued operations when facing unfavorable economic conditions? Although prior studies have investigated the roles of uncertainty and sunk costs as sources of inertia, an unacknowledged type of sunk cost associated with temporary suspensions of operations is related to the erosion of existing capabilities. Building on the resource-based view and real options theory, we argue that resource idling contributes to capability erosion and that the anticipated capability loss motivates firms to refrain from idling their resources under demand uncertainty in the first place. The negative effects of uncertainty on resource idling are likely to be particularly strong for firms with superior capabilities and for those having a greater reliance on human capital. Using data on oil drilling contractors in Texas, the empirical evidence lends support to our theoretical arguments. Our insights suggest that resource idling shapes the development path of capabilities and risks jeopardizing firms' competitive advantages. The seemingly operational decision of temporarily idling resources can therefore be quite strategic for a firm, and "hysteresis," or inertia in continuing operations, can preserve firms' capabilities.

**Research Question**
Why would some firms persist with continued operations when facing unfavorable economic conditions? Specifically, how does anticipated capability erosion from temporarily idling resources function as a sunk cost that shapes firms' decisions to idle versus continue operations under demand uncertainty?

**Hypotheses / Propositions**
- H1: The extent of resource idling has a negative effect on a firm's capabilities (i.e., capability erosion).
- H2: Demand uncertainty has a negative impact on the likelihood of resource idling.
- H3: The negative impact of demand uncertainty on the likelihood of resource idling will be magnified for firms with superior capabilities.
- H4: The negative impact of demand uncertainty on the likelihood of resource idling will be magnified for resources with greater reliance on human capital (as opposed to automation).

**Mechanism Process**
- IV(s): Extent of resource idling (proportion of a driller's rigs "stacked" relative to its fleet); demand uncertainty (oil-price-driven exogenous volatility)
- DV(s): Firm capabilities / capability erosion (residual intrinsic drilling speed, firm-year level, H1); likelihood of resource idling (rig-month level, H2-H4)
- Mediators: Not modeled explicitly (capability erosion is the proposed sunk-cost channel linking idling to subsequent idling restraint)
- Moderators: Firm capabilities (H3); reliance on human capital vs. automation (H4)

The paper integrates the resource-based view with real options theory to argue that temporarily idling resources erodes existing capabilities through reduced utilization, organizational forgetting, layoffs, and the breaking of coordinated routines. Because this erosion is a sunk cost that cannot be costlessly reversed upon reactivation, forward-looking firms treat idling like outright exit and rationally persist ("hysteresis") under demand uncertainty rather than idle. The dissuading effect of uncertainty on idling is amplified for firms with superior capabilities (which face larger strategic sunk costs) and for firms reliant on human capital rather than automation (whose capabilities are more vulnerable to erosion). All four hypotheses receive empirical support.

**Data & Measures**
Archival panel data on Texas oil drilling assembled from Drillinginfo, RigData, the Texas Railroad Commission, and the U.S. Energy Information Administration, covering 102 drillers and 1,396 rigs from 2001 to 2018; the capability erosion analysis is at the firm-year level (n = 1,836) and the idling analysis at the rig-month level (n = 301,536). A driller's capabilities are measured as its intrinsic speed capability in drilling: a first-stage project-level OLS regresses the drilling rate for a given well (total well depth divided by drilling days) on well type, project size, contract type, field oil demand, and field and year dummies, and the residuals are standardized within each field-year subgroup and averaged to the firm-year. Extent of idling is the proportion of a driller's total rigs that are "stacked" relative to its fleet in year t; the rig-level dependent variable is a binary indicator equal to 1 if the driller stacks a given rig in month t by suspending its drilling operations and releasing the associated crew, and 0 otherwise. Demand uncertainty is the market forecast error from a GARCH model estimated on monthly U.S. oil demand for 2001-2018, that is, the absolute percentage difference between predicted and observed industry output; human capital reliance is a dummy equal to 1 if the focal rig is the traditional fully human-operated type and 0 if automated. Controls are grouped at the firm, environment, and rig levels (Table 1). H1 is estimated with firm fixed-effects regression, which the authors call identification by adjustment, with idling in year t lagged relative to capabilities in t + 1, and is complemented by treatment effect analysis, which they call identification by balancing, using propensity score matching, inverse probability weighting, and doubly robust estimation with drillers matched on size, age, number of clients, resource heterogeneity, technological sophistication, and human capital reliance. H2 to H4 are estimated with firm fixed-effects logit models of the binary idling decision, with standard errors clustered by firm. The authors note that idling decisions are not randomly assigned across firms, so identification rests on fixed effects, the lag structure, and balancing on observed covariates rather than on random or exogenous assignment.

**Key Findings**
All four hypotheses are supported. H1 is supported: the extent of resource idling in year t is negatively related to a driller's capabilities in year t + 1 (b = -10.122, p = .005; firm fixed effects, n = 1,836 firm-years), and the treatment effects analysis corroborates this, with drillers that idled at least one rig in year t showing lower capabilities in t + 1 than drillers that idled none (treatment-control differences of -1.619 under propensity score matching, -1.502 under inverse probability weighting, and -0.992 under doubly robust estimation; all p values below .02), a pattern that also holds using capabilities at t + 2. H2 is supported: demand uncertainty has a significant negative effect on the likelihood of idling a rig (b = -6.581, p = .008; rig-month logit, n = 301,536). H3 is supported: the interaction between demand uncertainty and firm capabilities is negative and significant (b = -0.002, p = .026), and the marginal effects plot shows the negative effect of uncertainty on idling is more pronounced for high-capability drillers. H4 is supported: the interaction between demand uncertainty and human capital reliance is negative and significant (b = -0.812, p = .039), with the negative effect of uncertainty on idling more pronounced for rigs relying on human capital than for automated rigs. Supplemental analyses find negative and significant coefficients for both partial ("warm stacking") and complete ("cold stacking") idling, with the larger coefficient and economic magnitude for complete idling, and an ordinal logit in which uncertainty reduces the degree of idling, an effect strengthened both by superior capabilities and by greater reliance on human capital.

**Theoretical Contribution**
The study introduces capability erosion as a previously unacknowledged form of sunk cost relevant to firms' investment decisions under uncertainty, thereby extending the resource-based view's attention from capability building toward the maturity stage of the capability lifecycle. By explicating how capability erosion operates as a sunk cost within a real options framework, it demonstrates a theoretical synergy between the resource-based view and real options theory and identifies a new, internally generated source of hysteresis. It also contributes to the resource reconfiguration literature by introducing temporary contraction as a reversible deviation from a current configuration.

**Practical Implication**
What seems to be an operational decision to navigate cyclical markets (idling resources) can be highly strategic, because it influences a firm's existing capabilities and its ability to benefit from future growth opportunities. Managers, especially at firms with superior capabilities or heavy reliance on human capital, should weigh anticipated capability erosion and reactivation costs against short-term cash-flow savings before idling resources in a downturn.

**Limitations**
The study is limited to a single industry with usage-specific resources and firms exposed to the same environmental shocks (oil price movements). The data cannot directly observe capability buildup in other value-chain activities (e.g., R&D) or other idling-related factors such as union contracts and labor relations dynamics. The authors note the context may be conservative, as predictions could be even stronger in more knowledge-intensive industries.

**Future Research**
Future work could examine resource idling in other cyclical industries (mining, aircraft, shipping), study different forms of idleness and erosion of newly built rather than established capabilities, and explore exogenous events offering varying managerial discretion (pandemics, disasters, political crises, wars). Researchers could also incorporate capabilities into real options analyses of hysteresis, develop more refined measures of automation and complementary knowledge assets, and study initiatives that curate resources and enhance recovery from erosion.

**APA 7th Citation**
Ross, J.-M., Li, T. X., Hawk, A., & Reuer, J. J. (2023). Resource idling and capability erosion. *Academy of Management Journal*, 66(5), 1334–1359. https://doi.org/10.5465/amj.2020.1050
