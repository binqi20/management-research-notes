---
id: amj-vol-62-no-2-piezunka-2019
title: "Idea Rejected, Tie Formed: Organizations’ Feedback on Crowdsourced Ideas"
authors:
  - "Piezunka, Henning"
  - "Dahlander, Linus"
year: 2019
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2016.0703"
volume: 62
issue: 2
pages: "503-530"

source: "AMJ/vol-62-no-2"
pdf_path: "library/AMJ/vol-62-no-2/pdfs/Piezunka 2019 Idea Rejected, Tie Formed Organizations’ Feedback on Crowdsourced Ideas.pdf"
text_path: "library/AMJ/vol-62-no-2/text/Piezunka 2019 Idea Rejected, Tie Formed Organizations’ Feedback on Crowdsourced Ideas.txt"
ingested_at: "2026-06-29"
extraction_model: "gpt-5.5"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-08-05"

paper_type: "empirical-quantitative"
keywords: ["crowdsourcing ideas", "rejections", "newcomers", "continued interaction", "tie formation", "linguistic style", "feedback", "open innovation"]
theory: ["tie formation", "matching in relationship formation", "procedural justice", "feedback in creative processes"]
topics: ["strategy-innovation", "innovation-management", "ecosystems-platforms", "longitudinal"]
unit_of_analysis: "individual"
level_of_theory: "cross-level"
dependent_variable_family: "social"
methods: "Empirical quantitative study using large-scale longitudinal event data from virtual suggestion boxes. The authors estimate Cox proportional hazard models and discrete-time survival models with inverse probability of treatment weights, using large-scale text analysis of rejection explanations to measure content and linguistic-style matches."
sample:
  industry: "Organizations using cloud-based crowdsourcing suggestion-box software; specific industries are heterogeneous and not fully reported."
  country: "Data provider based on the West Coast of the United States; the paper does not fully report sampled organizations' countries."
  time_period: "From the software's launch in November 2007 through the end of the observation period in June 2013."
  units: "Newcomer-month observations of contributors' continued interaction with organizations after submitting first ideas."
  n: "70,159 organizations, 1,336,154 contributors, and 2.6 million ideas; survival analyses use 24,170,521 newcomer-month observations."

evidence:
  sample_n: "70,159 organizations that received ideas from 1,336,154 contributors"
  sample_country: "based on the West Coast of the United States"
  sample_industry: "virtual suggestion boxes"
  sample_time_period: "launch of the software in November 2007"
  theories_overview: "At the center of our reasoning are the relationships"
  methods_overview: "We use Cox proportional hazard models"
  keywords_source: "When organizations crowdsource ideas"
  hypotheses_source: "Hypothesis 1. An explicit rejection that only notifies a"
  measures_overview: "in the Linguistic Inquiry and Word Count (LIWC) 2015"
  findings_overview: "We find that receiving a rejection positively impacts newcomers’ willingness to submit ideas in future. This effect is stronger if the rejection includes an explanation"
---

# Idea Rejected, Tie Formed: Organizations’ Feedback on Crowdsourced Ideas

**Abstract**
When organizations crowdsource ideas, they select only a small share of the ideas that contributors submit for implementation. If a contributor submits an idea to an organization for the first time (i.e., is a newcomer), and the organization does not select the idea, this may negatively affect the newcomer’s relationship with the organization and willingness to submit ideas to the organization in future. We suggest that organizations can increase newcomers’ willingness to submit further ideas by providing a thus far understudied form of feedback: rejections. Though counterintuitive, we suggest that rejections encourage newcomers to bond with an organization. Rejections signal contributors that an organization is interested in receiving their ideas and developing relationships with them. To test our theory, we examine the crowdsourcing of 70,159 organizations that received ideas from 1,336,154 contributors. Using text analysis, we examine differences in how rejections are written to disentangle the mechanisms through which rejections affect contributors’ willingness to continue to interact with an organization. We find that receiving a rejection positively impacts newcomers’ willingness to submit ideas in future. This effect is stronger if the rejection includes an explanation and is particularly pronounced if the explanation matches the original idea in terms of linguistic style.

**Research Question**
The paper asks how organizations can increase newcomers' willingness to continue submitting ideas when their first crowdsourced ideas are not selected for implementation. It focuses on whether explicit rejections, explanations, and matches between an idea and the rejection explanation affect continued interaction.

**Hypotheses / Propositions**
- H1: An explicit rejection that only notifies a newcomer that a submitted idea has not been selected for implementation, but provides no additional explanation, increases the newcomer's willingness to continue to interact with the organization (i.e., to submit more ideas).
- H2: The positive effect (outlined in Hypothesis 1) of an explicit rejection on a newcomer's willingness to continue to interact with the organization (i.e., to submit more ideas) is stronger if the rejection includes an explanation.
- H3: The effect of an explicit rejection with an explanation (as proposed in Hypothesis 2) is stronger when the explanation indicates that the organization matches with the contributor in terms of content.
- H4: The effect of an explicit rejection with an explanation (as proposed in Hypothesis 2) is stronger when the explanation indicates that the organization matches with the contributor in terms of linguistic style.

**Mechanism Process**
- IV(s): First idea rejected without explanation; first idea rejected with explanation; match between the rejection explanation and the idea in informational content; match between the rejection explanation and the idea in linguistic style.
- DV(s): Continued interaction, measured as whether and when a newcomer submits a second idea to the same organization.
- Mediators: Perceived organizational interest, relationship development, procedural fairness, and perceived match are theorized mechanisms, but they are not directly estimated as mediators.
- Moderators: Explanation content match and linguistic-style match are modeled as conditions shaping the effect of rejection explanations; robustness checks also examine interactions with newcomer and organization activity.

The mechanism is that rejection can signal attention and relationship interest even when the substantive outcome is negative. A bare rejection reduces uncertainty that the organization is looking at submitted ideas, while an explained rejection signals greater time and effort by the organization. The key supported matching mechanism is linguistic rather than content-based: newcomers are more likely to return when the organization's explanation uses a style similar to the newcomer's original idea.

**Data & Measures**
The data come from a collaboration with a software-as-a-service company based on the West Coast of the United States whose software organizations use to collect and manage crowdsourced ideas through virtual suggestion boxes, where contributors submit ideas by completing the sentence "I suggest to you . . ." The collaboration gave the authors data on the crowdsourcing of 70,159 organizations that received 2.6 million ideas from 1,336,154 contributors between the launch of the software in November 2007 and the end of the observation period in June 2013. Cleaning proceeded in three steps: removing all ideas the software coded as spam and the contributors who submitted them, removing blank ideas, and restricting the analysis to ideas written in English so the content could be analyzed against an existing corpus of words. The unit of analysis is the newcomers' monthly activity; the dataset is split into monthly records, a newcomer enters the sample by posting a first idea, and the calendar month in which a newcomer is first observed is set as month zero, which allows the authors to account for right censoring because most newcomers submit only one idea.

The dependent variable, Continued interaction, captures whether a newcomer ever contributes a second idea to the organization and is coded as a dummy taking the value of 1 if newcomer i posts a second idea in calendar month t, where t is any calendar month following the newcomer's first entry. To assess the overarching (not hypothesized) effects, the authors create First idea rejected and First idea selected, dummies that switch from 0 to 1 in the month in which the newcomer's first idea is rejected or selected and retain that value thereafter; First idea selected aggregates status changes to "scheduled," "in work," or "implemented." Hypothesis 1 is tested with First idea rejected—without explanation, representing a rejection in which the organization simply changes the idea's status to rejected; Hypothesis 2 with First idea rejected—with explanation. Hypothesis 3 uses First idea rejected—explanation matches idea content, built with large-scale quantitative text analysis: nonalphabetical characters are removed, words are lowercased, stemmed to their root form, and stripped of stop words, and the remaining texts are transformed into word vectors following a bag-of-words approach, with the match computed as the cosine similarity of two binary vectors representing the unique terms occurring in the idea and the response. Hypothesis 4 uses First idea rejected—explanation matches idea style, following the approach of Goldberg et al. (2016): each text is classified into the subcategories captured in the Linguistic Inquiry and Word Count (LIWC) 2015 dictionary, a vector of the relative share of words in each category is created for each idea and each explanation, and the style match is the cosine similarity between the two vectors, so an idea and an explanation can match in style even without sharing individual words. In all comparisons the baseline is no response from the organization.

Controls enter at four levels. Organization level: cumulative ideas rejected by the organization and cumulative ideas selected in month t − 1, crowding (ideas at risk, i.e., not yet status-changed, in month t − 1), and age (months since the organization received its first idea). Newcomer level: anonymity, whether the newcomer is employed by the organization, and cumulative comments given, comments received, votes given, and votes received in month t − 1. Idea level: idea length (word count) and its square, plus LIWC-based linguistic-style controls for analytical thinking, clout, authenticity, tone, six-letter words, function words, pronouns, personal pronouns, cognitive processes, perceptive processes, and negation. Rejection level: rejection length, the same linguistic-style categories applied to the explanation itself (so that the match, rather than any particular style, is what is tested), whether the response has a prior duplicate, and whether the newcomer is named in the response. All continuous variables are standardized.

Estimation uses Cox proportional hazard models and discrete-time survival models with both time-invariant and time-varying covariates, with standard errors clustered at the newcomer level. The design is observational: the authors state that they do not have random assignment of which ideas organizations reject, and they address the resulting nonrandom selection of contributors into treatment groups with an inverse probability of treatment weighted (IPTW) approach, weighting newcomers by the inverse of the probability of becoming treated (rejected) and estimating the weighted models as discrete-time survival logistic regressions, since Cox models do not allow subject-specific weights. The authors also note that the sheer number of observations makes traditional significance tests nearly meaningless and therefore interpret effect sizes and replicate on smaller samples. Table 1 and Models 1-3 and 6 of Table 2 use 24,170,521 newcomer months from 1,336,154 newcomers; Models 4, 5, and 7 use 545,176 newcomer months from 31,475 newcomers, because the sample is constrained to those ideas that have been explicitly rejected with explanations. The robustness models in Table 3 use the full sample with interactions (1,336,154 newcomers; 24,170,521 newcomer months), an enhanced subsample of approximately 9% of the full sample constructed by matching organizational information from CrunchBase and ZoomInfo to add controls for organizational size, funding, U.S. location, and industry dummies (157,893 newcomers and 3,229,464 newcomer months in Models 2-3; 3,834 newcomers and 63,927 newcomer months in Model 4), and newcomer fixed-effects linear probability models (87,063 newcomers; 536,590 newcomer months).

**Key Findings**
Model 2 of Table 2 establishes the average effects against the baseline of no organizational response: First idea rejected is 0.860 (p < .01) and First idea selected is 1.013 (p < .01), and the authors note that the effect size of a rejection is smaller than that of a selection.

Hypothesis 1 is supported. In Model 3, First idea rejected—no explanation is 0.588 (p < .01); the authors describe the effect as both significant and economically meaningful, with a rejection without an explanation increasing the hazard that the newcomer will continue to interact by 80% (exp(.588)). Hypothesis 2 is supported. First idea rejected—with explanation is 0.890 (p < .01), increasing the hazard of continued interaction by 143% (exp(.890)); both coefficients are positive and significant, their 95% confidence intervals do not overlap, and a test of the equality of the coefficients shows that the effect of a rejection with an explanation is greater (143% vs. 80%, respectively).

Hypothesis 3 is refuted. In Model 5, First idea rejected—explanation matches idea content is −0.304 and insignificant; the authors conclude that the match between ideas and rejections in terms of content has no effect on continued interaction. Hypothesis 4 receives strong support. First idea rejected—explanation matches idea style is 0.508 (p < .01) in Model 5, and is described as highly significant and positive; conditional on receiving a rejection, a one standard-deviation increase in linguistic style similarity increases the hazard of continued interaction by 66%. Thus, while content matching (reusing words from the original idea) has no effect, style matching (adopting a similar linguistic style) has a clear positive effect. In supplementary analyses not reported in the paper, the interaction between content similarity and linguistic similarity is insignificant.

The discrete-time IPTW replications reproduce the same pattern: in Model 6, First idea rejected—no explanation is 0.703 (p < .01) and First idea rejected—with explanation is 0.934 (p < .01); in Model 7, the content match is −0.043 (insignificant) and the style match is 0.629 (p < .01). The authors note the similarity between the Cox and IPTW results as increasing their confidence.

The robustness checks in Table 3 add three qualifications. First, interactions with the main effect show positive interaction effects between a rejection of a newcomer's first idea and comments given (0.032, p < .01) and votes given (0.019, p < .10), while comments received (−0.008) and votes received (0.02) are insignificant; two organizational characteristics have negative interaction effects, ideas rejected by the organization (−0.021, p < .01) and crowding (−0.027, p < .10), implying that rejections have a weaker effect when competition is higher and when an organization has a history of rejecting ideas. Second, on the enhanced subsample the effects persist: First idea rejected is 0.470 (p < .01) in Model 2, and in Model 3 First idea rejected—with explanation is 0.523 (p < .05) and First idea rejected—no explanation is 0.298 (p < .05); in Model 4, the content match is −0.154 (insignificant) and the style match is 1.203 (p < .01), on a small sample of 3,834 newcomers who received rejections with explanations. Third, the newcomer fixed-effects linear probability models confirm the previous results and support the notion that the rejection or selection of a newcomer's first idea affects continued interaction even when accounting for unobserved time-invariant newcomer characteristics such as innate ability or personality.

Among the controls, the authors report that an organization's total number of ideas rejected and total number of ideas selected both positively affect newcomers' tendency to submit second ideas, crowding is positive, initiative age is negative, newcomer anonymity is negative, being employed by the organization is positive, and votes and comments both given and received are positive. Reusing a response an organization has used before has a positive effect, which the authors attribute to the organization devoting time and effort to develop a high-quality template, whereas using a newcomer's name in a rejection has no positive effect.

**Theoretical Contribution**
The paper contributes to tie-formation research by showing that failed initial interactions need not end an incipient relationship. Feedback from the contacted actor can help preserve the tie-formation process by signaling interest, appreciation, and match.

It also contributes to crowdsourcing and open innovation research by shifting attention from idea generation and selection to the management of rejected ideas. For feedback research, the study identifies relationship development as a function of feedback, not only task guidance or performance evaluation.

**Practical Implication**
Organizations that crowdsource ideas should not treat rejection as merely an administrative status update. Providing explicit rejections, especially with explanations written in a style that fits the contributor's own communication, can keep newcomers engaged after their first ideas are declined.

The findings also imply that silence is not neutral. If managers want future interaction, no feedback may waste relationship potential; if they want to suppress future interaction, the paper suggests that silence may be more effective than explicit rejection.

**Limitations**
The authors note that the findings may be bounded to settings where contributors face three possible responses: selection, rejection, or no feedback. The effects may differ in contexts where rejection is the only alternative to selection, where participation requires major effort, or where the rejected actor strongly identifies with the rejected contribution.

The study is observational, and organizations did not randomly assign rejection types to newcomers. Although the authors use inverse probability of treatment weighting, robustness checks, and fixed-effects analyses, they cannot rule out all unobserved heterogeneity or determine whether rejection is cost-beneficial for organizations overall.

**Future Research**
Future research could examine what makes a rejection helpful, including whether managers should give one reason or several reasons when rejecting complex proposals. It could also study whether and how managers deliberately adapt linguistic style when writing rejection explanations.

The authors also call for work on the antecedents and broader effects of rejections. Future studies could examine why managers avoid rejecting ideas, how rejections change contributors' later idea content or style, whether rejections affect other contributors' evaluations, and whether rejected contributors submit the same ideas elsewhere.

**APA 7th Citation**
Piezunka, H., & Dahlander, L. (2019). Idea rejected, tie formed: Organizations' feedback on crowdsourced ideas. *Academy of Management Journal*, 62(2), 503-530. https://doi.org/10.5465/amj.2016.0703
