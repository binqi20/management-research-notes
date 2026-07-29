---
id: amj-vol-65-no-6-burt-2022
title: "Bridge Supervision: Correlates of a Boss on the Far Side of a Structural Hole"
authors:
  - "Burt, Ronald S."
  - "Wang, Song"
year: 2022
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.0676"
volume: 65
issue: 6
pages: "1835-1863"

source: "AMJ/vol-65-no-6"
pdf_path: "library/AMJ/vol-65-no-6/pdfs/Burt 2022 Bridge Supervision Correlates of a Boss on the Far Side of a Structural Hole.pdf"
text_path: "library/AMJ/vol-65-no-6/text/Burt 2022 Bridge Supervision Correlates of a Boss on the Far Side of a Structural Hole.txt"
ingested_at: "2026-06-24"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-29"

paper_type: "empirical-quantitative"
keywords: ["bridge supervision", "structural holes", "network brokerage", "role segregation", "dyad networks", "manager performance", "network constraint"]
theory: ["structural holes / social capital theory (Burt, 1992, 2005)", "Bott hypothesis on conjugal role segregation (Bott, 1955, 1957/1971)", "network brokerage and good ideas (Burt, 2004)"]
topics: ["leadership-behavior", "social-capital-theory"]
unit_of_analysis: "individual"
level_of_theory: "meso"
dependent_variable_family: "mixed"
methods: "Logit and OLS regressions across 455 supply chain managers in a large American electronics firm, using personnel records and a name-generator/interpreter network survey; dyad networks assembled around each manager-boss pair; idea texts scored for emotion via LIWC."
sample:
  industry: "Supply chain organization of a large American electronics company (leader in its industry)"
  country: "United States (establishments across North America)"
  time_period: "Single cross-sectional online survey wave (data originally collected for Burt, 2004)"
  units: "Individual managers (analyzed within manager-boss dyad networks)"
  n: "455 survey respondents (of 673 managers invited; 68% response)"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "of whom 455 completed the survey (68%)."
  sample_country: "across North America. It is not one of the electronics"
  sample_industry: "supply chain managers in a large American electron"
  sample_time_period: "Our cross-sectional data do not indicate intensity or"
  theories_overview: "described as “role segregation” in Bott’s"
  methods_overview: "These are logit regressions estimated across 455 managers predicting who does not cite the boss as a discussion partner"
  keywords_source: "be associated with role segregation between manager"
  hypotheses_source: "Hypothesis 3. Manager performance is independent of bridge supervision"
  measures_overview: '"Mutual contacts" is the number of contacts mutual to manager and boss.'
  findings_overview: "Managers operating under bridge supervision exclude the boss from their work discussions and are conservative in expressing emotion."
---

# Bridge Supervision: Correlates of a Boss on the Far Side of a Structural Hole

**Abstract**
“Bridge supervision” occurs when the connection between manager and boss is a network bridge between separate social worlds. Improved communication technology has facilitated the use of bridge supervision, so manager and boss can easily interact by audio or onscreen as a pair of people disconnected from surrounding colleagues—but at what cost to the manager, or to effective management? We argue that bridge supervision affects the way in which managers play their role, but not how well the role is played. We find clear support for the argument in a traditional corporate hierarchy. Managers operating under bridge supervision exclude the boss from their work discussions and are conservative in expressing emotion. Behavioral correlates notwithstanding, compensation and good ideas have their familiar association with network brokerage independent of bridge versus embedded supervision. In sum, bridge supervision affects manager style, but not performance. We conclude this paper by discussing the implications of our findings for future research.

**Research Question**
How does "bridge supervision"—a supervisory relationship that spans a structural hole between the separate social worlds of manager and boss—relate to the way managers play their role (role segregation) and to how well they perform (compensation and the value of their ideas)?

**Hypotheses / Propositions**
- Hypothesis 1. The probability of role segregation decreases with the number of mutual contacts shared by manager and boss.
- Hypothesis 2. The probability of role segregation increases with the density of connections among a manager's exclusive contacts (colleagues connected to the manager but not to the manager's boss).
- Hypothesis 3. Manager performance is independent of bridge supervision, as indicated by a lack of manager–boss mutual contacts or dense connections among a manager's exclusive contacts.

Hypothesis 3 is stated explicitly as a null hypothesis: the authors say they do not intend to prove it, they simply expect it and want to be explicit about that expectation.

**Mechanism Process**
- IV(s): Bridge supervision, operationalized by two dimensions of the manager-boss dyad network—(a) number of mutual contacts shared by manager and boss, and (b) exclusive density (density among the manager's contacts not connected to the boss); summarized as a binary bridge-vs-embedded indicator.
- DV(s): Role segregation, indicated by (1) failure to cite the boss as a core discussion partner and (2) absence of emotion words (LIWC) in the manager's idea text; and manager performance, measured as z-score salary and z-score idea value.
- Mediators: None modeled (Hypothesis 3 is an explicit null: performance is independent of bridge supervision).
- Moderators: Network constraint (access to structural holes / brokerage), entered as a level and slope adjustment to separate brokerage from bridge supervision.

Drawing an analogy from Bott's classic network study of conjugal role segregation, the authors argue that when a manager and boss occupy separate, cohesive constituencies, social pressure for within-group conformity leads the manager to treat the boss as an outsider—excluding the boss from work talk and suppressing emotional display "on stage" with higher management. Yet because returns to brokerage flow from a manager's own network skills (processing and recombining diverse information), the performance advantages of structural holes persist independent of whether supervision is bridged or embedded. Logit models support Hypotheses 1 and 2 (the odds of not citing the boss are ~9.5x higher under bridge supervision; the odds of showing no emotion ~2x higher), while OLS models and F-tests fail to reject the null Hypothesis 3.

**Data & Measures**
A single study of the supply chain organization of a large American electronics company, combining company personnel records with an online network survey; all 673 managers in the study population were invited and 455 completed the survey (68%), and the 455 respondents do not differ significantly from the 218 nonrespondents in salary, business unit, geographic location, job rank, or demographic controls for age, race, gender, and education. The compensation, idea value, network constraint measure, and control variables are those used in Burt (2004). Performance DVs: z-score salary from company records at the time of the survey (−1.86 ≤ z-score salary ≤ 4.08); and z-score idea value, built from two executives — each leading one of the company's largest business units — who rated each unattributed idea for improving the supply chain on a 5-point scale in response to "How much value could be generated if the idea were well executed?", with ideas a judge dismissed scored 0, the resulting 0–5 ratings averaged per idea and then standardized (−1.43 ≤ z-score ≤ 2.05). Role-segregation DVs, both binary: (a) failure to cite the boss as a core discussion partner — two name generators (the person with whom the manager's idea was discussed, then "More generally, who are the people with whom you most often discuss supply chain issues?") recorded up to eight names, the boss was never named by title and was identified from personnel records, and 33% of managers did not cite their boss; and (b) absence of emotion words in the manager's idea text (texts of up to 2,000 characters, averaging 60 words) scored with Linguistic Inquiry and Word Count (LIWC), where four out of five managers used at least one emotion word, leaving 22% with none.

Bridge-supervision IVs: the number of contacts mutual to manager and boss (M = 3.18, SD = 2.79), and manager-exclusive density, the average strength of connection among the manager's contacts not connected directly to the boss, multiplied by 100 and set to zero for managers with no or only one exclusive contact (M = 18.36, SD = 25.78); a binary bridge-versus-embedded indicator (M = 0.40) summarizes both, defined by the shaded area of Figure 3 (zero mutual contacts, extended out to four mutual contacts for managers with nonzero exclusive density). Brokerage is controlled with Burt's (1992) network constraint index, computed here within the dyad network rather than the ego network, entered as log constraint (M = 3.51, SD = 0.44) and measured as a deviation from its mean in defining interaction terms. A supervision dyad network was assembled for each of the 455 respondents — respondent first, then the boss identified from company HR records with the supervision tie fixed at maximum strength, then contacts strongly connected to either — from survey data providing 5,010 observations of 4,139 relationships coded at five levels of connection strength (1.00, .86, .65, .50, .00). Of the 157 bosses supervising the 455 respondents, 94 responded to the survey, 40 did not, and 23 worked outside the supply chain organization and were not invited; two dummy variables distinguishing these cases were added as a robustness check for under-reported boss networks. Other controls are job rank, purchasing versus internal role, age, a minority dummy, bachelor and graduate education, high-tech and low-tech business-unit dummies, and two high-cost urban-area dummies; race, gender, and marital status were tested but were not significant predictors or slope adjustments. Estimation is logit for the two binary role-segregation outcomes (Table 2, Models 1–4) and ordinary least squares for z-score salary and z-score idea value (Table 4, Models 5–8), both with robust standard errors (Stata "robust"), plus F(2,440) tests of whether distinguishing bridge-supervised managers adds anything to the performance predictions. The design is cross-sectional and associational — the paper reports correlates of bridge supervision and notes that its cross-sectional data do not indicate intensity or duration — and no causal identification strategy is used.

**Key Findings**
Hypothesis 1 supported. In the logit predicting which managers exclude the boss from their core discussion partners (Table 2, Model 1), the number of manager–boss mutual contacts carries a negative coefficient (−0.60, −7.88 test statistic, p < .001): managers who exclude their boss have fewer mutual contacts with the boss. Hypothesis 2 supported. In the same model, exclusive density carries a positive coefficient (reported in the text as 1.91 with a 4.02 test statistic, p < .001; .019 with a .005 standard error in Table 2, where density is scaled by 100): managers who exclude their boss have more densely interconnected colleagues disconnected from the boss. Descriptively, 85% of managers under embedded supervision cite their boss versus 39% under bridge supervision, and with controls held constant and embedded supervision as reference the odds of not citing the boss are nine and a half times higher under bridge supervision (e^2.25 in Model 2 is 9.49). Network constraint is also negative in Model 1 (−2.22 coefficient, −5.27 test statistic, p < .001), meaning network brokers are likely to operate independently of their boss; but once bridge supervision is entered as a binary variable in Model 2, network constraint is no longer a predictor either directly (−0.26 coefficient, −0.70 test statistic, p = .49) or as a slope adjustment (−0.60 coefficient, −1.14 test statistic, p = .26), while bridge supervision is the key predictor (2.25 coefficient, 9.22 test statistic, p < .001). The emotion indicator is weaker: 18% of embedded-supervised managers use no emotion words versus 29% under bridge supervision, and the odds of not displaying emotion are twice as high under bridge supervision (e^.68 in Model 4 is 1.97). Model 3, with all three continuous network variables entered, shows emotion independent of all of them (pseudo R² = .06 versus .27 for Model 1); the association appears in Model 4, which adds level and slope adjustments for the binary bridge/embedded distinction — a significant level effect (.68, 2.71 test statistic, p = .007) and a significant slope adjustment for network constraint among bridge-supervised managers (1.30 coefficient, 2.13 test statistic, p = .03). Substantively, bridge-supervised managers in the most closed networks show no emotion 80–90% of the time, whereas bridge-supervised network brokers show emotion 80–100% of the time.

Hypothesis 3 supported in the sense that the null is not rejected. In the OLS models predicting z-score salary (Models 5, 6) and z-score idea value (Models 7, 8), all four F(2,440) tests fail to reject the null that distinguishing bridge-supervised managers adds nothing to the prediction (.49, .75, .91, and .27, with probabilities .61, .47, .40, and .76), and the bridge supervision coefficients are negligible (−0.04 for salary in Model 6; 0.06 for idea value in Model 8). The familiar brokerage association is intact and independent of supervision type: network constraint is negative for salary (−0.32 in Model 5, −0.41 in Model 6, p < .001) and for idea value (−0.51 in Model 7, −3.75 test statistic, p < .001), so managers with networks rich in structural holes earn more and propose ideas judged more valuable whether supervision is bridged or embedded. There is also no indirect route: adding a predictor distinguishing managers who cite the boss does not improve prediction (0.75 and −0.20 test statistics for Models 5 and 7, p > .56), and a predictor for expressing emotion is similarly negligible (−0.50 and 1.23 test statistics, p > .22). In the authors' summary, bridge supervision affects manager style, but not performance.

**Theoretical Contribution**
The study integrates dyad networks—the joint network around a pair tied by an obligatory relationship (manager-boss)—into research on the competitive advantage of a manager's network, a relation prior brokerage work had ignored. It introduces and operationalizes "bridge supervision," shows it has behavioral correlates (role segregation) yet leaves performance returns to brokerage intact, and thereby clears away a potential confound: predicting manager performance does not require expanding the ego network to the dyad network around manager and boss.

**Practical Implication**
Because bridge supervision affects manager style but not performance, organizations face no apparent performance cost in adopting the more flexible, less expensive bridge supervision (e.g., remote or arm's-length arrangements expanded by COVID-19). The choice between bridge and embedded supervision is a question of management style rather than effective management—though leaders should be aware that bridge-supervised managers exclude bosses from discussions and withhold emotion.

**Limitations**
The data have two deficiencies: limited breadth (only two manager behaviors—citing the boss and expressing emotion—are observed, with little information on affect or other Bott-hypothesis dimensions) and time (the data are a single cross-sectional moment, so cumulative or duration effects of bridge supervision on performance cannot be detected). The study population is a single traditional bureaucracy where manager and boss have known each other 7.6 years on average.

**Future Research**
Replication should test Hypotheses 1 and 2 with more diverse behavioral and affective indicators of role segregation, using the many existing populations with network and performance data. Longitudinal data could reveal cumulative/systemic effects, language divergence preceding exit, and whether bridge supervision develops managers as brokers. The origins of bridge supervision (boss vs. manager vs. organizational characteristics; geography, budget, span of control, intentional development) and its operation as a work-culture phenomenon (e.g., freelancers, regional managers) are promising leads.

**APA 7th Citation**
Burt, R. S., & Wang, S. (2022). Bridge supervision: Correlates of a boss on the far side of a structural hole. *Academy of Management Journal*, 65(6), 1835–1863. https://doi.org/10.5465/amj.2021.0676
