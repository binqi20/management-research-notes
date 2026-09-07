---
id: amj-vol-58-no-3-piezunka-2015
title: "Distant Search, Narrow Attention: How Crowding Alters Organizations’ Filtering of Suggestions in Crowdsourcing"
authors:
  - "Piezunka, H."
  - "Dahlander, L."
year: 2015
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2012.0458"
volume: 58
issue: 3
pages: "856-880"

source: "AMJ/vol-58-no-3"
pdf_path: "library/AMJ/vol-58-no-3/pdfs/Piezunka 2015 Distant Search, Narrow Attention How Crowding Alters Organizations’ Filtering of Suggestions in Crowdsourcing.pdf"
text_path: "library/AMJ/vol-58-no-3/text/Piezunka 2015 Distant Search, Narrow Attention How Crowding Alters Organizations’ Filtering of Suggestions in Crowdsourcing.txt"
ingested_at: "2026-07-06"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "gpt-6-astra"
augmented_at: "2026-09-07"

paper_type: "empirical-quantitative"
keywords: ["distant search", "crowding", "organizational attention", "distant knowledge", "crowdsourcing"]
theory: ["attention-based view (Ocasio, 1997)", "distant search", "crowdsourcing as solution to distant search"]
topics: ["strategy-innovation", "innovation-management", "quantitative-methods"]
unit_of_analysis: "organization"
level_of_theory: "meso"
dependent_variable_family: "na"
methods: "Longitudinal Cox proportional hazard models on weekly suggestion-level risk-set records, using proprietary crowdsourcing-platform data, text-analysis measures of content distance, network measures of structural distance, contributor-history measures of personal distance, and Huber-White clustered standard errors at the individual level."
sample:
  industry: "Organizations using a website-embedded suggestion tool across different industries, with the clientele dominated by web companies."
  country: "Software company located on the west coast of the United States; most customer organizations were located in America and Western Europe."
  time_period: "November 2007-June 2011."
  units: "Crowdsourced suggestions submitted by external contributors to organizations, observed as weekly risk-set records until selection or censoring."
  n: "105,127 suggestions submitted to 922 organizations; 10,629 selected suggestions over 5,039,413 weekly observations."

evidence:
  sample_n: "922 organizations responded to 105,127 crowdsourced suggestions"
  sample_country: "west coast of the United States"
  sample_industry: "web companies"
  sample_time_period: "between November 2007 and June 2011"
  theories_overview: "attention-based view (Ocasio, 1997)"
  methods_overview: "We used the Cox proportional hazard models"
  keywords_source: "attention, search, and crowdsourcing"
  hypotheses_source: "(b) amplified by an increase in crowding."
  measures_overview: "Weighted degree centrality in the one-mode"
  findings_overview: "does not amplify the effect of personal distance"
---

# Distant Search, Narrow Attention: How Crowding Alters Organizations’ Filtering of Suggestions in Crowdsourcing

**Abstract**
In their search for innovation, organizations often invite suggestions from external contributors. Soliciting suggestions is a form of distant search, since it allows organizations to tap into knowledge that may not reside within their organizational boundaries. Organizations engaging in distant search often face a large pool of suggestions, an outcome we refer to as crowding. When crowding occurs, organizations, given a limited attention span, can attend to only a subset of suggestions. Our core argument is that crowding narrows the attention of organizations; that is, despite organizations’ efforts to reach out to external contributors and access suggestions that capture distant knowledge, they are more likely to pay attention to suggestions that are familiar, not distant. We test our theory with a unique longitudinal dataset that captures how 922 organizations responded to 105,127 crowdsourced suggestions from external contributors. After distinguishing between three different dimensions of distance (content, structural, and personal), we find that (a) all three types of distance have independent negative effects on the likelihood of attention, (b) crowding amplifies these negative effects, and (c) there are differences among the effects’ magnitudes. We elaborate on the broader implications of these findings for the literatures on attention, search, and crowdsourcing.

**Research Question**
The paper asks whether organizations that solicit suggestions from external contributors in order to access distant knowledge actually pay attention to suggestions that are distant. It also asks whether crowding makes organizations more or less likely to attend to distant knowledge during suggestion filtering.

**Hypotheses / Propositions**
- H1: The effect of content distance on organizations’ attention is (a) negative and (b) amplified by an increase in crowding.
- H2: The effect of structural distance on organizations’ attention is (a) negative and (b) amplified by an increase in crowding.
- H3: The effect of personal distance on organizations’ attention is (a) negative and (b) amplified by an increase in crowding.

**Mechanism Process**
- IV(s): Content distance, structural distance, personal distance, crowding, and the interactions between crowding and each distance dimension.
- DV(s): Organizational attention to a suggestion, operationalized as whether the organization assigned the suggestion the status "selected."
- Mediators: Not reported in paper.
- Moderators: Crowding moderates the effects of content distance and structural distance on organizational attention; the personal-distance interaction is weaker and loses significance in the full model.

The mechanism is an attention-filtering process under bounded organizational attention. When crowding increases, organizations simplify and rationalize filtering, which steers attention toward suggestions that are familiar in content, structurally connected to other supported suggestions, or submitted by contributors with prior attention from the organization. The evidence most strongly supports crowding as amplifying the negative effects of content and structural distance, while personal distance has a negative main effect but less robust moderation by crowding.

**Data & Measures**
The longitudinal, observational dataset came from a private software company providing a website-embedded suggestion tool, supplemented with organization characteristics from ZoomInfo and CrunchBase. After removing spam, blank and non-English suggestions, organizations’ own submissions, and organizations without matched characteristics, the main sample comprised 105,127 suggestions to 922 organizations between November 2007 and June 2011. Table 3 reports 10,629 selection events and 5,039,413 weekly risk-set observations. Attention was the weekly indicator that an organization assigned a suggestion “selected” status; suggestions entered at submission and exited at selection, with pending suggestions right censored. Crowding was the number of suggestions awaiting a status change in the organization’s community in week t.

Content distance used word-frequency and inverse-frequency weighting, cosine similarities, and a row sum multiplied by −1; Table 1 specifies comparison with previously accepted suggestions. Structural distance was weighted degree centrality in the one-mode projection of the contributor-vote network, normalized by community size and multiplied by −1. Personal distance used a contributor’s prior suggestions multiplied by −1, but the paper gives inconsistent definitions: the Methods text specifies previously implemented suggestions, whereas Table 1 specifies previously selected or rejected suggestions. Cox proportional hazard models with time-varying weekly covariates and Huber–White standard errors clustered by individual estimated associations with selection timing. Controls covered suggestion length and its square, suggestion and comment sentiments, vote share, comment count, contributor tenure and anonymity, and organization characteristics. Continuous-variable coefficients were standardized.

**Key Findings**
Table 3 supports H1a, H2a, and H3a: all three distance measures were negatively associated with attention. In the full Model 10, content, structural, and personal distance coefficients were −0.0797, −0.7013, and −0.3414, respectively (all p < .01). H1b and H2b were supported: crowding interacted negatively with content distance (b = −0.0367, p < .01) and structural distance (b = −0.8506, p < .01). The reported structural-distance illustration translates a one-standard-deviation increase into a 50% lower selection hazard at mean crowding and a 79% lower hazard at crowding one standard deviation above the mean. As a baseline result, a one-standard-deviation increase in crowding corresponded to a 33% lower selection hazard in Model 2.

H3b was not supported in the full model: the personal-distance interaction was negative and significant in Model 9 (b = −0.1694, p < .05) but nonsignificant in Model 10 (b = −0.1216). Table 4 shows that this moderation result varied across robustness checks: the median-split crowding interaction was significant (b = −0.2573, p < .01), the model without controls was marginal (b = −0.1465, p < .10), and the web-company subsample was nonsignificant (b = −0.1168). Content- and structural-distance main effects and moderation remained negative and significant in these checks.

**Theoretical Contribution**
The paper contributes to attention research by showing that crowding changes what organizations attend to, not only how much attention any single suggestion receives. It contributes to search research by separating access to distant knowledge from attention to distant knowledge, showing that organizations may collect distant suggestions but filter them out when the pool becomes crowded. It also contributes to crowdsourcing research by shifting attention from the solicitation stage to the filtering stage and by distinguishing content, structural, and personal distance empirically.

**Practical Implication**
Organizations using crowdsourcing should not assume that larger suggestion pools automatically improve innovation search. Managers may need to constrain the generation of alternatives, design filters that deliberately preserve distant suggestions, and establish criteria or ratios that prevent familiar suggestions from crowding out more distant ones. They can also begin by examining suggestions from contributors from whom the organization has not previously heard.

**Limitations**
The authors state that their theory depends on settings in which all suggestions and ideas are visible to the organization and to external contributors. It also depends on social mechanisms that allow external contributors to vote, comment, or refine suggestions; a simple suggestion box without these mechanisms would not provide the same relationship cues for filtering suggestions.

**Future Research**
Future research could examine how crowding affects organizations' relationships with ignored or rejected contributors, including whether disappointed contributors publicly harm organizational reputation or future search efforts.

**APA 7th Citation**
Piezunka, H., & Dahlander, L. (2015). Distant search, narrow attention: How crowding alters organizations’ filtering of suggestions in crowdsourcing. *Academy of Management Journal*, 58(3), 856-880. https://doi.org/10.5465/amj.2012.0458
