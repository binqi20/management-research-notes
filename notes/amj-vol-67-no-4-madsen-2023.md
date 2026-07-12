---
id: amj-vol-67-no-4-madsen-2023
title: "Change at Last, but When Does Change Last? Preserving Attentional Engagement around Past Failures and Their Lessons"
authors:
  - "Madsen, P. M."
  - "Desai, V."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0391"
volume: 67
issue: 4
pages: "933-955"

source: "AMJ/vol-67-no-4"
pdf_path: "library/AMJ/vol-67-no-4/pdfs/Madsen 2023 Change at Last, but When Does Change Last Preserving Attentional Engagement around Past Failures and Their Lessons.pdf"
text_path: "library/AMJ/vol-67-no-4/text/Madsen 2023 Change at Last, but When Does Change Last Preserving Attentional Engagement around Past Failures and Their Lessons.txt"
ingested_at: "2026-05-06"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords: ["attention-based view", "attentional engagement", "vigilance", "organizational learning", "knowledge depreciation", "failure complexity", "culpability", "routine relatedness"]
theory: ["attention-based view (Ocasio, 1997, 2011; Nicolini & Korica, 2021)", "organizational learning theory (Argote et al., 2021; Levitt & March, 1988)"]
topics: ["organizational-behavior-hrm", "strategy-innovation", "methods-theory"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "social"
methods: "Fixed-effects maximum likelihood nonlinear regression on an unbalanced firm-year panel of all U.S. coal mining firms (1988-2021), estimating depreciation parameters (lambda) for accident experience using the feNmlm function in R; learning-curve specification with firm and year fixed effects."
sample:
  industry: "U.S. coal mining"
  country: "United States"
  time_period: "1988-2021 (data 1983-2021; first five years dropped to construct lags)"
  units: "firm-years"
  n: "28,304 firm-year observations from 5,869 firms"

evidence:
  sample_n: "mining industry, using a sample of all 5,869 firms"
  sample_country: "all firms that operated U.S. coal mines"
  sample_industry: "serious coal mining accidents"
  sample_time_period: "from 1983 to 2021. In this"
  theories_overview: "attention-based view (ABV), and specifically on"
  methods_overview: "fixed effect maximum likelihood"
  keywords_source: "attentional engagement and vigilance"
  hypotheses_source: "Hypothesis 1. Knowledge gleaned from a firm"
  measures_overview: "Negligence is rated on a 5-point scale"
  findings_overview: "This result supports Hypothesis 2."
---

# Change at Last, but When Does Change Last? Preserving Attentional Engagement around Past Failures and Their Lessons

**Abstract**
Although failures and other experiences can capture attention and motivate organizations to learn and improve, this knowledge is not always retained over time, leaving some organizations dangerously prone to repeat the same mistakes repeatedly. We adapt theory on the attention-based view—and specifically on attentional engagement and vigilance—to shed new light on this process. While prior research has examined how competing events may draw attention away, our theory leads us to consider the circumstances that will motivate employees to maintain attention on learning from failure that has already occurred. Our framework examines the conditions that preserve attention to past failures by increasing the perception that related issues exist elsewhere, serving as continuing reminders of or cues about the failure when attention begins to drift away. We find support for related hypotheses involving a failure's complexity, the firm's culpability, and the ongoing use of routines related to those involved in the failure. Our findings contribute to the attention-based view by developing theory about attentional engagement and vigilance and by emphasizing the conditions that can keep attention focused on, rather drawn away from, past failure. We also contribute to efforts to examine knowledge depreciation and forgetting in more depth in organizational learning theory.

**Research Question**
What characteristics of past organizational failures preserve managerial and employee attention over time, such that the knowledge derived from those failures depreciates more slowly? Why does knowledge from some failures persist longer in organizational structures, routines, and memories than knowledge from others?

**Hypotheses / Propositions**
- H1. Knowledge gleaned from a firm's past experience with more complex failures depreciates more slowly than knowledge from less complex failures, such that past complex failures are more closely associated with current performance.
- H2. Knowledge derived from a firm's past experience with more culpable failures depreciates more slowly than knowledge from less culpable failures, such that past culpable failures are more closely associated with current performance.
- H3. Knowledge gained through a firm's past failures involving routines more closely related to the firm's dominant routines depreciates more slowly than knowledge from failures with less-related routines, such that those past failures are more closely associated with current performance.

**Mechanism Process**
- IV(s): High failure complexity, high firm culpability, and high routine relatedness (each as time-varying indicators of past serious accident experience over years t-1 through t-5), interacted with summed accident experience.
- DV(s): Logged days lost to accidents (negative measure of mine safety performance); modeled jointly with knowledge depreciation parameter lambda for each experience type.
- Mediators: Sustained attentional engagement / vigilance to past failures (theorized, not directly measured).
- Moderators: Inherent in the design — complexity, culpability, and routine-relatedness moderate the rate at which prior accident experience depreciates.

The authors adapt the attention-based view to argue that failure characteristics that surface associations with other organizational routines repeatedly draw collective attention back to the failed area. Complex failures expose interconnections across diverse routines; culpable failures spread blame and scrutiny that diffuse to other domains; failures involving routines related to the firm's dominant routines remain salient through everyday work. These three forms of association preserve attentional engagement, slow knowledge depreciation, and extend the performance benefits of prior learning.

**Data & Measures**
- Data: annual observations of all firms that operated U.S. coal mines from 1983 to 2021, drawn from three Mine Safety and Health Administration (MSHA) databases — the Production Employment database (employment and productivity), the accident/injury/illness database (accidents, injuries, fatalities), and the mine inspection database (accident causes and firm culpability).
- DV: a logged count of employee days lost to injury (MSHA's required safety-performance index; a fatal injury is assigned 6,000 lost work days and a permanent disability between 5 and 4,500), used as a negative measure of mine safety performance.
- IV (all accident experience): annual counts of fatalities and permanent disabilities from "serious" accidents (those causing at least one fatality or permanent disability) in each prior year t-1 through t-5.
- Complexity (moderator): an entropy-based index of the heterogeneity of an accident's causes across MSHA's 21 accident-cause categories, dichotomized at the median into a "high complexity" indicator.
- Culpability (moderator): the average MSHA-inspector negligence rating for a firm's serious accidents (rated 1 = no negligence to 5 = reckless), dichotomized at the median into a "high culpability" indicator.
- Routine relatedness (moderator): an indicator that an accident occurred in a mine of the same type (surface vs. underground) as the majority of the firm's mines, dichotomized into a "high routine relatedness" indicator.
- Identification: each "high" indicator is multiplied by all accident experience so a separate knowledge-depreciation parameter (lambda) is estimated for high- versus low-X experience, via fixed-effects (firm and year) nonlinear maximum likelihood estimation. The authors describe the models as estimating the relationship between accumulated failure experience and subsequent performance, and characterize the design as correlational rather than causal.

**Key Findings**
- All three hypotheses were supported. A higher depreciation parameter (lambda, the share of knowledge retained from year to year) indicates slower depreciation.
- H1 supported: the depreciation parameter for high-complexity accident experience (0.82) is significantly larger than for low-complexity experience (0.22) (Wald test, p < .001) — knowledge from more complex failures depreciates more slowly.
- H2 supported: the high-culpability depreciation parameter (0.69) is significantly larger than the low-culpability parameter (0.15) (Wald test, p < .01).
- H3 supported: the high routine-relatedness depreciation parameter (0.96) is significantly larger than the low-relatedness parameter (0.57) (Wald test, p < .05).
- In the full model (Model 6), all three hypotheses continue to be supported; the "all accident" experience (low in complexity, culpability, and routine relatedness) is no longer significantly different from zero.

**Theoretical Contribution**
The paper develops theory about attentional engagement and vigilance within the attention-based view, specifying characteristics of past failures that pull attention back rather than allowing it to drift away. It contributes to organizational learning theory by showing that knowledge gleaned from different types of failures depreciates at different rates—answering Argote et al.'s (2021) call for theory about heterogeneity in retention rates—and by linking the ABV more tightly to the temporality of organizational memory.

**Practical Implication**
Managers can extend the lifespan of lessons learned from failures by conducting thorough investigations that surface causal complexity rather than simplifying causal stories, by openly engaging with the firm's culpability rather than externalizing blame, and by explicitly demonstrating how routines involved in past failures relate to dominant routines used elsewhere in the firm. Formal "lessons learned" programs (e.g., NASA's) illustrate this practice.

**Limitations**
The findings concern failure experience and may not generalize to nonfailure (success) experiences. The failures studied are coal mine accidents, so other types of organizational failures may show different depreciation patterns. The authors could not observe firm financial performance (most are not public), the analysis is correlational rather than causal, and learning and depreciation are inferred from experience-performance associations rather than directly observed in routines.

**Future Research**
Future work should apply the theory and the novel feNmlm-based depreciation estimation method to other forms of experience and to other types of organizational failures. The authors encourage examination of additional experiential and organizational factors that may influence depreciation rates.

**APA 7th Citation**
Madsen, P. M., & Desai, V. (2024). Change at last, but when does change last? Preserving attentional engagement around past failures and their lessons. *Academy of Management Journal*, 67(4), 933-955. https://doi.org/10.5465/amj.2022.0391
