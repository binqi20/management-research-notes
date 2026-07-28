---
id: amj-vol-66-no-5-engel-2023
title: "Signaling Diversity Debt: Startup Gender Composition and the Gender Gap in Joiners’ Interest"
authors:
  - "Engel, Yuval"
  - "Lewis, Trey"
  - "Cardon, Melissa S."
  - "Hentschel, Tanja"
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.1197"
volume: 66
issue: 5
pages: "1469-1500"

source: "AMJ/vol-66-no-5"
pdf_path: "library/AMJ/vol-66-no-5/pdfs/Engel 2023 Signaling Diversity Debt Startup Gender Composition and the Gender Gap in Joiners’ Interest.pdf"
text_path: "library/AMJ/vol-66-no-5/text/Engel 2023 Signaling Diversity Debt Startup Gender Composition and the Gender Gap in Joiners’ Interest.txt"
ingested_at: "2026-05-20"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-mixed"
keywords: ["diversity debt", "joiners", "startup gender composition", "lack of fit", "tokenism", "identity threat concerns", "gender gap in interest"]
theory: ["lack of fit model (Heilman, 1983, 2012)", "tokenism (Kanter, 1977a, 1977b)", "identity threat (Kroeper et al., 2022; Murphy et al., 2007)", "signaling of employer information (Cable & Turban, 2001)"]
topics: ["gender-in-organizations", "entrepreneurship", "signaling-theory", "europe"]
unit_of_analysis: "individual"
level_of_theory: "micro"
dependent_variable_family: "social"
methods: "Two studies. Study 1: field data from a job-matching mobile app; linear probability models (LPM) with robust standard errors clustered by job advertisement and job seeker, plus job-level fixed effects. Study 2: preregistered 2x2 (job seeker gender x diversity debt signal) between-subjects online experiment with mediation analysis (bootstrapped indirect effects)."
sample:
  industry: "Tech/startup employers; jobs dominated by IT/engineering (39%) and marketing (21%) in Study 1; a simulated 'ScaleIT' startup profile in Study 2"
  country: "Netherlands (Study 1 field data); United States (Study 2 experiment)"
  time_period: "Platform activity 2015–2017 (Study 1)"
  units: "Study 1: job seekers' interest decisions on job advertisements. Study 2: individual experiment participants (joiners)"
  n: "Study 1: 522,451 decisions by 8,340 job seekers across 1,978 job ads from 311 startups. Study 2: 597 participants"

evidence:
  sample_n: "522,451 decisions made by 8,340 job seekers"
  sample_country: "reside in the United States"
  sample_industry: "the sample is dominated by IT and engi"
  sample_time_period: "activity between 2015 and 2017"
  theories_overview: "the lack of fit model (Heilman, 1983) with"
  methods_overview: "robust standard errors clustered"
  keywords_source: "Women are underrepresented in startups"
  hypotheses_source: "The proportion of women in a startup is positively associated with interest for women joiners"
  measures_overview: "measured using a scale by Kroeper et al. (2022)"
  findings_overview: "finding the hypothesized gender gap and showing that women, but not men, are sensitive to information about organizational gender composition"
---

# Signaling Diversity Debt: Startup Gender Composition and the Gender Gap in Joiners’ Interest

**Abstract**
Women are underrepresented in startups, but research on “joiners”—nonfounder employees attracted to startup work—offers limited explanations for why such underrepresentation occurs and how it persists. We argue that, even among joiners, women are less interested than men in applying for startup jobs and that this gender gap is associated with differential reactions to information about the gender composition of prospective employers. We analyze unique field data obtained from a job-matching mobile-application platform for startups, finding the hypothesized gender gap and showing that women, but not men, are sensitive to information about organizational gender composition, especially for startups signaling “diversity debt”—that is, no or only a token representation of women. A preregistered experiment further reveals that women’s identity threat concerns mediate these effects. Gender disparities in startups are reproduced in a vicious cycle as existing underrepresentation deters women from applying. Our findings have implications for research and practice concerning joiners, the underrepresentation of women in entrepreneurship, and startups’ ability to shape the gender composition of their applicant pools.

**Research Question**
Why are women underrepresented among startup "joiners" (nonfounder employees), and how does information about a startup's existing gender composition—especially signals of "diversity debt"—shape the gender gap in joiners' interest in applying?

**Hypotheses / Propositions**
H1: There is a gender gap in interest for startup jobs such that, all else equal, women joiners are less interested in applying than men joiners.
H2: Startup gender composition information moderates the gender gap in joiners' interest in applying; the proportion of women in a startup is positively associated with interest for women joiners while men joiners remain unaffected.
H3: Startup gender composition information moderates the indirect effect of joiner gender on interest in applying through identity threat concerns; when the proportion of women in a startup indicates diversity debt (vs. no diversity debt), identity threat concerns are triggered for women joiners but not for men joiners, and identity threat concerns are in turn negatively associated with joiners' interest (for both men and women).

**Mechanism Process**
- IV(s): Job seeker gender (woman vs. man); startup gender composition signal (proportion of women; in Study 2, a diversity debt signal of 5% women vs. no-diversity-debt 40% women)
- DV(s): Interest in applying for a startup job (binary swipe decision in Study 1; application intentions in Study 2)
- Mediators: Women's identity threat concerns
- Moderators: Startup gender composition information (the proportion of women / diversity debt signal moderates the gender gap and the indirect effect)

Drawing on the lack of fit model, the paper argues that the masculine gender-typing of startups leads women joiners to form more negative fit expectations and lower interest than men (H1). Job seekers update these expectations using organizational gender composition as a signal, so a higher proportion of women raises women's (but not men's) interest (H2). At the extreme—when a skewed composition signals diversity debt (token representation)—tokenism logic predicts it triggers identity threat concerns in women, which mediate the link to lower interest, reproducing underrepresentation in a self-reinforcing vicious cycle (H3).

**Data & Measures**
Study 1 uses proprietary archival data from a job-matching mobile application for tech startups (platform activity 2015-2017; 97% of jobs posted in the Netherlands), covering 522,451 decisions by 8,340 job seekers on 1,978 job advertisements from 311 startups. DV: interest in applying, a binary variable capturing whether a job seeker pressed the "tick" (= 1) or the "cross" (= 0) on a viewed advertisement. IV: job seeker gender, coded algorithmically from first names using the genderize.io API with an 85% probability threshold (0 = man, 1 = woman). Moderator: company gender composition, the proportion of women employees that startups were required to report on every advertisement, scaled 0 (0% women) to 1 (100% women). Controls include a woman (co)founder, gender composition in the company background photo, industry gender composition, company size and age, average employee age, prior external investment, job title, job level, job commitment, net share of feminine wording, job seeker work experience, skills fit, language fit, weeks from posting to rating, and calendar year. Estimation: linear probability models with robust standard errors clustered simultaneously by job advertisement and job seeker, plus fixed effects models holding time-invariant job advertisement and job seeker characteristics constant, with a logit specification as a robustness check. Study 1 is observational, and the authors note that the control variables are unlikely to have a causal interpretation themselves; the mechanism is instead tested experimentally in Study 2. Study 2 is a preregistered 2 (job seeker gender: men, women; self-reported) x 2 (startup gender composition signal: diversity debt, no diversity debt; randomly assigned) between-subjects experiment with 597 Prolific participants residing in the United States, pre-screened for openness to startup employment. The manipulation varied only the gender composition line on an otherwise identical fictitious "ScaleIT" employer profile: 95% men/5% women versus 60% men/40% women. Primary DV: application intentions, Highhouse et al.'s (2003) 5-item scale (alpha = .89), with application decision and behavioral interest as binary secondary measures. Mediator: identity threat concerns, six items from Kroeper et al. (2022) rated 1 "not at all" to 5 "an extreme amount" (alpha = .95); anticipated fairness (alpha = .92) and perceived startup viability (alpha = .88) were measured as alternative mediators. Analysis: two-way ANOVAs plus a moderated mediation model with percentile bootstrapped 95% confidence intervals from 5,000 resamples.

**Key Findings**
Study 1 supports H1 and H2. For H1, holding other factors constant, the probability of expressing interest in applying is about 3% lower for women than for men (Table 3, Model 2: b = -0.03, SE = 0.01), which the authors call sizeable against the 17% baseline interest rate. For H2, the interaction between job seeker gender and the proportional representation of women is positive and significant (b = 0.04, SE = 0.01, p < .001) and survives a fixed effects specification; the slope linking women's representation to interest is positive and significant for women (b = 0.05, SE = 0.01, p < .001) but not for men (b = 0.01, SE = 0.01, p = .612). Marginal effects show the gender gap reaching about 4% at 0-20% women and closing to statistical insignificance as representation approaches about 60% women. In exploratory robustness checks the quadratic term is not significant (no curvilinear effect), but using Kanter's categories women's predicted probability of interest is 12% when startups show 0-15% women versus 17% (15-35%), 15% (35-50%), and 17% (50-100%), and threshold analysis places a tipping point near 30% women; the authors flag these as exploratory and draw no strong conclusions. The H1 gap and the H2 moderation do not significantly vary between masculine, feminine, and gender-neutral industries. Study 2 supports H3 and replicates the moderation. Gender interacted significantly with the composition signal on identity threat concerns, F(1, 593) = 48.65, p < .001, partial eta-squared = .08, and on application intentions, F(1, 593) = 8.00, p = .005, partial eta-squared = .01. Under the diversity debt signal women reported higher identity threat concerns (M = 3.37, SD = 1.23 vs. M = 2.14, SD = 0.83; p < .001, d = 1.18) and lower application intentions (M = 3.18, SD = 1.05 vs. M = 3.81, SD = 0.63; p < .001, d = 0.74). Men showed no significant difference in identity threat concerns across conditions (M = 1.91, SD = 0.83 vs. M = 1.69, SD = 0.59; d = 0.29); their application intentions did differ significantly (M = 3.65, SD = 0.80 vs. M = 3.92, SD = 0.64; d = 0.37), a difference the paper describes as substantially smaller than the one observed for women. The negative indirect effect of job seeker gender on application intentions via identity threat concerns was significant in both conditions (no diversity debt: b = -0.18, SE = 0.04, 95% CI [-0.26, -0.11]; diversity debt: b = -0.60, SE = 0.07, 95% CI [-0.75, -0.46]) and significantly more negative under the diversity debt signal (index of moderated mediation = -0.42, SE = 0.07, 95% CI [-0.56, -0.29]), so Hypothesis 3 is supported. Parallel models show the indirect effects via anticipated fairness and perceived startup viability are not conditional on the gender composition signal.

**Theoretical Contribution**
The paper integrates a gender lens into research on "joiners," bringing together the lack of fit model, tokenism, and identity threat to explain the self-reinforcing role of organizational gender composition in women's startup underrepresentation. It extends the prior focus on founder–employee gender congruence by showing that organization-level gender composition—a signal of past hiring behavior—is a meaningful informational cue, and positions women's identity threat concerns as the primary mechanism linking diversity debt signals to lower interest, thereby reconciling mixed prior evidence on supply- and demand-side drivers of gender sorting.

**Practical Implication**
Startups have an active role in shaping their own recruitment pipelines rather than attributing women's underrepresentation to a "pipeline problem." Because signaling diversity debt deters women through identity threat concerns, firms could counteract it with "identity safe cues"—for example, sincere text that explicitly recognizes the current lack of gender diversity alongside a concrete commitment to change, rather than generic diversity statements that can backfire.

**Limitations**
Study 1 captures only initial expressions of interest, not whether applicants and companies reached a final employment agreement, and the reported gender composition was holistic (not broken down by job level) and of unverified accuracy. The Study 2 diversity debt manipulation (5% women) was deliberately strong, raising a possible (though mitigated) risk of demand effects.

**Future Research**
Future work could test "identity safe cues" and other interventions to break diversity debt's self-reinforcing cycle, examine whether hiring women early indirectly improves later recruitment of women via signaling, and jointly study the perspectives of job seekers and startups (e.g., given evidence that startups prefer to hire male employees).

**APA 7th Citation**
Engel, Y., Lewis, T., Cardon, M. S., & Hentschel, T. (2023). Signaling diversity debt: Startup gender composition and the gender gap in joiners' interest. *Academy of Management Journal*, 66(5), 1469–1500. https://doi.org/10.5465/amj.2021.1197
