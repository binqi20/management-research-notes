---
id: amj-vol-68-no-4-chung-2025
title: "Threading the Needle of Corporate Activism: How Firms Frame Their Stances on Polarizing Social Issues"
authors:
  - "Chung, Sung Hun (Brian)"
  - "Odziemkowska, Kate"
  - "Piazza, Alessandro"
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0237"
volume: 68
issue: 4
pages: "680-706"

source: "AMJ/vol-68-no-4"
pdf_path: "library/AMJ/vol-68-no-4/pdfs/Chung 2025 Threading the Needle of Corporate Activism How Firms Frame Their Stances on Polarizing Social Issues.pdf"
text_path: "library/AMJ/vol-68-no-4/text/Chung 2025 Threading the Needle of Corporate Activism How Firms Frame Their Stances on Polarizing Social Issues.txt"
ingested_at: "2026-04-18"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-11"

paper_type: "empirical-quantitative"
keywords: ["corporate activism", "strategic framing", "collective action frames", "individual action frames", "social arrangements", "issue settlement", "contestation", "LGBTQ rights", "same-sex marriage", "stakeholder alignment", "executive ideology", "advocacy organizations"]
theory: ["strategic framing theory", "collective action frame theory (Snow & Benford)", "institutional theory (Fligstein & McAdam contestation/settlement)", "upper echelons theory", "stakeholder theory", "social movement theory"]
topics: ["corporate-political-activity", "stakeholder-engagement", "lgbtq-inclusion", "north-america"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "social"
methods: "Stacked-cohort difference-in-differences panel regression on a firm-month panel of Fortune 500 companies' LGBTQ-related communications (1999-2019). Dependent variable is firms' relative use of collective action frames vs. individual action frames in press releases and tweets, computed from a dictionary of keywords built via human coding plus latent Dirichlet allocation (LDA) topic modeling. Treatment is a marriage-equality settlement (state legislative or judicial decision) in the firm's headquarters state, with cohorts constructed for each of the 36 distinct settlement events; control firms are Fortune 500 firms in states without a settlement during the cohort window. Models include firm, cohort, and month-year fixed effects, clustered standard errors at firm-cohort level, and a Heckman (1979) two-stage selection correction (first-stage probit instrumented by industry average elite-network size). Robustness checks include negative binomial counts, contemporaneous ideology measures, exclusion of CEO-attributed text, federal vs. state settlement decomposition, and annual-frequency models."
sample:
  industry: "Fortune 500 companies across all sectors (cross-industry); identification leverages two-digit SIC industry-level political-ideology measures"
  country: "United States (50 states; 36 state-level marriage-equality settlement events between 2004 Massachusetts and 2015 Obergefell v. Hodges)"
  time_period: "1999-2019 observation window (covering the 2004 Massachusetts settlement through the 2015 Obergefell decision plus four-year lead/lag)"
  units: "Firm-month observations of LGBTQ-related corporate press releases and corporate Twitter posts; dictionary-based frame measures"
  n: "152 Fortune 500 firms that spoke out on LGBTQ issues; 6,461 press releases and 6,450 tweets analyzed; 6,920 firm-month observations in main regression; first-stage probit on 619,047 firm-months from all Fortune 500 firms"

evidence:
  sample_n: "action) from 6,461 press releases and 6,450 tweets."
  sample_country: "to 2019, of which 152 spoke out on LGBTQ issues"
  sample_industry: "Fortune 500 companies' statements regarding LGBTQ"
  sample_time_period: "1999–2019, during which 36 distinct marriage equality"
  theories_overview: "According to upper echelons theory, the belief"
  methods_overview: "selection model (Heckman, 1979) estimated at the"
  keywords_source: "The collective action frame dictionary contains"
  hypotheses_source: "Following a judicial or legislative settlement of an issue, firms will rely more on collective"
  measures_overview: "where C is the number of collective action frame"
  findings_overview: "with all controls included (b 5 0.058, p 5 .004)"
---

# Threading the Needle of Corporate Activism: How Firms Frame Their Stances on Polarizing Social Issues

**Abstract**
Corporate activism, or the active involvement of business in contested social and political issues, presents strategic challenges for organizations. Despite the risks of stakeholder backlash, corporate activism is on the rise. We suggest that how firms speak out on polarizing social issues may help explain this quandary. Leveraging corporate press releases and Twitter accounts of Fortune 500 companies that spoke on LGBTQ issues between 1999 and 2019, as same-sex marriage progressively became legal across the United States, we find that prior to legalization in their home state, firms default to touting the economic merits of their track record on LGBTQ workplace issues, avoiding contentious debates. Once marriage equality is enacted, firms shift their speech toward activism, advocating for broader societal change. Further, the shift to activism is highly dependent on internal and external stakeholder preferences. Our findings point to an irony: corporate "activism" in pursuit of social change often takes place only after polarizing issues have been settled. This study contributes to the growing literature on corporate activism by shedding light on how firms strategically frame their communications to navigate the complex terrain of stakeholder expectations, and how these framing strategies are shaped by the evolving legal and institutional landscape.

**Research Question**
How do firms strategically frame their stances on polarizing social issues as institutional arrangements evolve from contested to settled, and how is the shift from individual action frames to collective action frames conditioned by the ideological alignment of internal and external stakeholders?

**Hypotheses / Propositions**
H1. Following a judicial or legislative settlement of an issue, firms will rely more on collective action frames (relative to individual action frames) in communicating their stance on the issue. (Positive main effect.)
H2. The board of directors' (BOD) and CEO's liberal political ideology will strengthen the relationship between issue settlements and firms' use of collective action frames posited in H1. (Positive moderation.)
H3. Industry-level conservative political orientation will weaken the relationship between issue settlements and firms' use of collective action frames posited in H1. (Negative moderation.)
H4. State-level conservative political ideology will weaken the relationship between issue settlements and firms' use of collective action frames posited in H1. (Negative moderation.)
H5. The presence of issue-aligned advocacy organizations in the firm's headquarter state will strengthen the relationship between issue settlements and firms' use of collective action frames posited in H1. (Positive moderation.)

**Mechanism Process**
- IV(s): Post-issue settlement — a binary indicator equal to 1 after a judicial or legislative marriage-equality decision in the firm's headquarters state (36 staggered state-level settlements, 2004-2015).
- DV(s): Firm's relative use of collective action frames vs. individual action frames in LGBTQ-related press releases and tweets, measured as C / (C + I), where C is the count of collective-action keywords and I is the count of individual-action keywords from a dictionary built via human coding plus LDA topic modeling.
- Mediators: Not formally modeled; the theorized mechanism is firms' strategic reading of reduced contestation/heightened legitimacy after settlement, which lowers backlash risk and makes injustice/prognostic/motivational collective-action frames safer to deploy.
- Moderators: (1) BOD and CEO liberal political ideology (positive interaction, H2); (2) industry-level conservative political ideology (negative interaction, H3); (3) state-level conservative political ideology (negative interaction, H4); (4) presence of two or more issue-aligned advocacy organizations in firm's headquarters state (positive interaction, H5).

Drawing on social movement theory's distinction between collective action frames (diagnostic, prognostic, motivational; injustice and moral outrage) and "individual action frames" (the authors' coinage for business/workplace framings tied to firm-level economic rationales), the paper argues that for-profit firms confronting contested social issues default to lower-risk individual action frames during contestation and only shift to collective action frames after a judicial or legislative settlement legitimizes a position and reduces stakeholder fault lines. Settlements operate by encoding authoritative signals of acceptable conduct and catalyzing attitudinal shifts, lowering the ex post backlash risk of injustice framings. The shift, however, is filtered through ideological alignment with key stakeholders: liberal executives, liberal industries, liberal states, and the presence of LGBTQ-aligned NGOs amplify the post-settlement shift to collective action frames, while conservative executives, industries, or state electorates suppress it.

**Data & Measures**
- Data corpus: all LGBTQ-related press releases (Business Wire and P.R. Newswire) and corporate Twitter/X posts of Fortune 500 companies, 1999-2019 — 6,461 press releases and 6,450 tweets. The first-stage selection model covers all Fortune 500 firms 1999-2019 (619,047 firm-months), of which 152 spoke out on LGBTQ issues; the main panel has 6,920 firm-month observations.
- DV (Firm's collective action frames): relative use C / (C + I), where C is the count of collective-action-frame words and I the count of individual-action-frame words in a firm's LGBTQ statements. Frame dictionaries were built by human coding of a subsample (2,143 tweets and 6,441 press-release titles) and refined with latent Dirichlet allocation (LDA) topic modeling.
- Treatment (Post-issue settlement): indicator equal to 1 once a judicial or legislative marriage-equality decision was enacted in the firm's headquarters state (36 staggered state settlements, 2004-2015).
- Moderators: (H2) BOD and CEO liberal ideology = directors' and CEO's donations to Democratic candidates divided by total donations (three-year average, five-year lag); (H3) industry-level conservatism = average Bonica (2013) campaign-finance CF scores of PACs at the two-digit SIC level (10-year lag, five-year moving average); (H4) state-level conservatism = average CF score of political candidates in the state; (H5) issue-aligned advocacy organizations = dummy equal to 1 if two or more such organizations operated in the firm's headquarters state.
- Controls: firm size (logged), ROA, HRC (Corporate Equality Index) rating, logged word count, Tweet channel, CEO-statement dummy, environmental munificence and complexity, state population, state poverty rate, state ethnic heterogeneity, CEO overconfidence, firm elite education, and firm elite network size.
- Identification: stacked-cohort difference-in-differences with firm, cohort, and month-year fixed effects and standard errors clustered at the firm-cohort level, plus a Heckman (1979) two-stage selection correction (first-stage probit instrumented by industry average elite network size). The design is quasi-experimental, leveraging the staggered timing of state settlements rather than random assignment.

**Key Findings**
- H1 (supported): following a marriage-equality settlement, treated firms shift toward collective action frames relative to control firms (model 1, p = .032; model 3 with full controls, b = 0.058, p = .004) — roughly a 6% increase, about one-quarter of the sample standard deviation.
- H2 (supported): BOD/CEO liberal ideology strengthens the post-settlement shift (model 4, p < .001). Very liberal executives (90th percentile) use ~18% more collective action frames than very conservative ones (10th percentile) (~70% of the SD); settlements have no significant effect when executives are conservative.
- H3 (supported): industry-level conservatism weakens the shift (model 5, p < .001); highly conservative industries (90th percentile) use ~19% fewer collective action frames post-settlement than liberal industries (10th percentile) (~three-quarters of the SD), with no significant settlement effect in conservative industries.
- H4 (supported): state-level conservatism weakens the shift (p < .001); highly conservative states (90th percentile) use ~18% fewer collective action frames than liberal states (10th percentile) (~70% of the SD).
- H5 (supported in isolation, attenuated in the full model): in its own model (model 6, p < .001), the presence of two or more issue-aligned advocacy organizations strengthens the shift (~15% more collective action frames, ~59% of the SD). In the full model (model 7), however, the advocacy-organization interaction becomes non-significant (p = .306) as its effect is absorbed by state-level ideology, while executive liberalism, industry conservatism, and state conservatism remain independently significant.
- Robustness: a negative-binomial count model corroborates H1 (firms in settlement states predicted to use 43 vs. 30 collective action words); results are unchanged when CEO-attributed text is excluded, and the significant shift holds for state-court or legislative settlements but not for federal-court decisions.

**Theoretical Contribution**
The paper extends institutional theory by showing how firms' rhetorical strategies — not just their structural or practice-level adoptions — reflect and adapt to evolving institutional contestation/settlement cycles, and it advances stakeholder theory by demonstrating that ideological alignment with multiple stakeholder layers (executives, industry peers, state electorates, NGOs) conditions how, not just whether, firms speak out. It also contributes to corporate-activism research by surfacing an irony: "true" activist (collective-action) framing predominantly emerges after social arrangements are already settled, suggesting that "corporate activism" is partly a misnomer — firms tend to enter the fray only after the battle has been won.

**Practical Implication**
For managers, the findings imply that signaling support during periods of active contestation is most safely done through individual action frames anchored in business and workplace rationales, while collective action frames carry meaningful backlash risk until institutional legitimacy is established. For activists, NGOs, and policymakers expecting corporations to be vanguards of change, the analysis cautions that corporate "activist" speech is largely a lagging, contingent response calibrated to executive, industry, and state-level ideology rather than a proactive driver of contested social change.

**Limitations**
The study is restricted to Fortune 500 firms, so smaller firms — which may employ different niche or product-market framing strategies — are not covered. The empirical setting (U.S. same-sex marriage legalization, 2004-2015) was an unusually clean and progressive trajectory of staggered settlements, raising questions about generalizability to settlements moving in conservative directions or settlements that diverge sharply from public opinion (e.g., Dobbs). Identification rests on settlements in the headquarters state, even though stakeholders (employees, customers) may reside elsewhere; constructs such as the motivational dimension of collective action frames partly overlap with prior issue-selling and symbolic-vs-substantive distinctions in management research.

**Future Research**
Future work could probe how stakeholder ideology shapes reactions to firms' framing choices and whether mixed framing produces less coherence or broader appeal across heterogeneous audiences. Researchers could examine settlements that go "against the grain" of public opinion, settlements moving in conservative directions, framing choices of small and private firms, and the welfare consequences of corporations' heavy reliance on individual action frames (business-case framings) for the beneficiaries of prosocial corporate initiatives.

**APA 7th Citation**
Chung, S. H. (B.), Odziemkowska, K., & Piazza, A. (2025). Threading the needle of corporate activism: How firms frame their stances on polarizing social issues. *Academy of Management Journal*, 68(4), 680-706. https://doi.org/10.5465/amj.2023.0237
