---
id: amj-vol-59-no-2-weigelt-2016
title: "Competition, Regulatory Policy, and Firms’ Resource Investments: The Case of Renewable Energy Technologies"
authors:
  - "Weigelt, Carmen"
  - "Shittu, Ekundayo"
year: 2016
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2013.0661"
volume: 59
issue: 2
pages: "678-704"

source: "AMJ/vol-59-no-2"
pdf_path: "library/AMJ/vol-59-no-2/pdfs/Weigelt 2016 Competition, Regulatory Policy, and Firms’ Resource Investments The Case of Renewable Energy Technologies.pdf"
text_path: "library/AMJ/vol-59-no-2/text/Weigelt 2016 Competition, Regulatory Policy, and Firms’ Resource Investments The Case of Renewable Energy Technologies.txt"
ingested_at: "2026-07-04"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "gpt-6-astra"
augmented_at: "2026-09-05"

paper_type: "empirical-quantitative"
keywords: ["regulatory mandates", "competition", "new resource investments", "renewable energy investments", "resource-based view", "clean technologies"]
theory: ["resource-based view (RBV)", "institutional theory"]
topics: ["renewable-energy", "environmental-regulation", "resource-based-view", "institutional-theory"]
unit_of_analysis: "firm"
level_of_theory: "macro"
dependent_variable_family: "environmental"
methods: "Empirical quantitative panel study using annual data on U.S. electricity-generation firms from 1999 to 2010. The authors estimate random-effects Tobit models for the percentage of renewable electricity generation, random-effects Probit models for waste-to-energy, wind, and solar investment, split-sample tests by RPS presence, two-sample t-tests, and post-hoc two-stage random-effects Probit models for RPS policy likelihood."
sample:
  industry: "U.S. electricity generation segment, including private energy firms, investor-owned utilities, and government utilities"
  country: "United States"
  time_period: "1999-2010"
  units: "Firm-state-year observations for firms with operational electricity generation facilities"
  n: "1,542 firms and 10,518 firm-year observations"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "1542 firms"
  sample_country: "all power producers in the U.S."
  sample_industry: "the U.S. electricity industry"
  sample_time_period: "years 1999–2010"
  theories_overview: "Research grounded in the resource-based view"
  methods_overview: "Tobit using STATA"
  keywords_source: "regulatory mandates and competition"
  hypotheses_source: "Hypothesis 2—RPS dampens competitive effect"
  measures_overview: "its MW operational from renewable resources relative"
  findings_overview: "RPS X Competitors’ new resource investment               – significant"
---

# Competition, Regulatory Policy, and Firms’ Resource Investments: The Case of Renewable Energy Technologies

**Abstract**
We study the interplay between regulatory mandates and competition on a focal firm’s new resource investments. While prior literature has separately pointed to the influence of competition and regulatory policy on a focal firm’s resource decisions, less is known about how the policy effect interacts with the competitive effect. Studying how regulatory mandates moderate the effect of competition on a focal firm’s new resource investments, we show that resource redeployment is not simply a function of internal firm decisions but a response to external forces. We find that regulatory mandates dampen the effect of competitors’ new resource investments on a focal firm’s new resource investments. Distinguishing between different clean technology types, we show that this dampening effect is the stronger, the more distant the new resource is from incumbents’ old resource base, and the more established the mandate is. We test our hypotheses in the context of renewable energy investments in waste-to-energy, wind, and solar in the U.S. electricity industry. Our data comprise 1542 utilities and private energy firms and their renewable investments from 1999 to 2010.

**Research Question**
How does the presence and strength of regulatory mandates alter the effect of competitors’ new resource investments on a focal firm’s own renewable energy investments? The paper asks whether regulatory policy substitutes for or complements competitive signals when firms reconfigure resource portfolios toward clean technologies.

**Hypotheses / Propositions**
- H1: Competitors’ new resource investments have a positive effect on a focal firm’s subsequent new resource investment.
- H2: The presence of a regulatory mandate lowers the effect of competitors’ new resource investments on a focal firm’s subsequent new resource investment.
- H3: The more distant a new resource is from incumbent firms’ established resource base, the stronger regulatory mandates’ dampening of the competitive effect on a focal firm’s subsequent new resource investment.
- H4: The more established a regulatory mandate is, the more dampened the competitive effect on a focal firm’s new resource investment.

**Mechanism Process**
- IV(s): Competitors’ new resource investments in renewables, and separately in waste-to-energy, wind, and solar.
- DV(s): A focal firm’s subsequent renewable electricity generation investments; separate binary indicators for waste-to-energy, wind, and solar investment.
- Mediators: No mediation is hypothesized in the main model. A supplementary test of RPS mandates as a mediator of the competitive effect on new resource investment finds no support.
- Moderators: Presence of RPS regulatory mandates, yearly RPS goals, and renewable resource distance from incumbents’ established fossil-fuel resource base.

The mechanism is that competitors’ investments reduce uncertainty about the value, functioning, and strategic need for new renewable resources, prompting focal firms to invest. Regulatory mandates also reduce uncertainty, but because they are codified, enforceable, and apply to the focal firm and competitors alike, firms attend more to mandates than to competitive signals when mandates are present. This dampening effect is stronger for technologically distant resources such as wind and solar and, for some resource types, when RPS mandates are more established.

**Data & Measures**
The annual panel uses 1999–2010 data from the Platts Database of World Electric Power Producers, aggregated from generating units to firms within states. The main reporting tables contain 10,518 observations for 1,542 firms over 11 years; all independent variables are lagged one year. DSIRE supplies state RPS policy information, and EIA supplies state energy data. The main DV is operational MW from renewable resources divided by the focal firm’s total operational MW in the subsequent year; hydroelectric power is excluded. Separate binary DVs indicate whether the firm has invested in waste-to-energy, wind, or solar. Competitors’ investments are the state-level share of operational MW from renewables among competing private energy firms, investor-owned utilities, and government utilities, with corresponding shares calculated separately for each renewable type.

RPS presence is a state-year indicator; yearly RPS goals measure the minimum targeted renewable percentage and proxy how established the mandate is. Years with an RPS mandate is a control. Resource distance is examined by comparing waste-to-energy, which shares a combustion process with fossil technologies, against wind and solar. The main analyses estimate conditional associations using random-effects Tobit and Probit models, interactions, and splits by RPS presence; fixed-effects Generalized Least Squares (GLS) regressions provide a robustness check. Post-hoc two-stage models predict state RPS presence using state fuel prices as instruments, then use predicted RPS values in the firm investment models. These checks do not constitute a randomized or natural-experiment design.

**Key Findings**
- H1 is supported for all renewables combined (Table 2, Model 2: b = 0.274, p < .01), waste-to-energy (Table 3: b = 7.840, p < .01), and wind (Table 4: b = 18.579, p < .01). Solar is positive but nonsignificant in Table 5, Model 2 (b = 3.310); the authors report significance when the RPS presence and duration variables are omitted.
- H2 is supported for aggregate renewables: the interaction between RPS presence and competitors’ investments is negative (Table 2, Model 3: b = −0.299, p < .01). In the split samples, competitors’ investments are positively significant without RPS mandates (Model 4: b = 0.579, p < .01), but nonsignificant with mandates (Model 5: b = 0.120). The same split-sample significance pattern occurs for each renewable type.
- H3 receives support from the resource comparisons: the RPS interaction is negative and significant for wind (b = −28.451, p < .01) and solar (b = −339.74, p < .05), but nonsignificant for waste-to-energy (b = −2.589), which is closer to the established fossil resource base (Tables 3–5, Model 3).
- H4 is supported only for waste-to-energy (b = −110.56, p < .10) and solar (b = −133.555, p < .05). The interaction between yearly RPS goals and competitors’ investments is nonsignificant for aggregate renewables (b = 0.561) and wind (b = −234.93) in the RPS subsample (Tables 2–5, Model 6).

**Theoretical Contribution**
The paper extends the resource-based view by showing that resource portfolio reconfiguration is shaped by external regulatory and competitive forces, not only by internal resource endowments and capabilities. It specifies a substitution relationship between regulatory mandates and competitors’ resource investments and shows that this relationship varies across resource types by technological distance from incumbents’ existing resource base. The study also links RBV reasoning to institutional theory by showing how mandates can redirect managerial attention and resource redeployment.

**Practical Implication**
For policy makers, the findings imply that renewable energy mandates are especially influential when few competitors have already invested and when the targeted resource is technologically distant from incumbents’ existing resource base. The paper also suggests that stable, established mandates can make firms less reliant on competitors’ behavior as a guide for new clean technology investments. For managers, the findings indicate that resource investment decisions should account for how regulatory pressure can supersede competitive imitation as an external signal.

**Limitations**
The authors state that they control for electricity demand and retail market deregulation but do not explicitly study customer demand in deregulated markets where customers can choose electricity providers. They also note that the dichotomous RPS measure is crude, although they partially address policy variation with yearly RPS goals. The study is limited to the U.S. electricity industry, so the same policy-competition interaction may not generalize to other industries.

**Future Research**
The authors call for more fine-grained research on the structure of regulatory policies across states. They suggest testing the interplay between competition and regulatory policy in other industry contexts. They also identify opportunities to study value networks, vertical integration, transmission agreements, and firms’ nonmarket strategies in resource portfolio configuration.

**APA 7th Citation**
Weigelt, C., & Shittu, E. (2016). Competition, regulatory policy, and firms’ resource investments: The case of renewable energy technologies. *Academy of Management Journal*, 59(2), 678-704. https://doi.org/10.5465/amj.2013.0661
