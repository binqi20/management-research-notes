---
id: amj-vol-67-no-6-oever-2024
title: "More than a Feeling: How Board Member Displays of Anger and Happiness Influence Strategic Decisions"
authors:
  - "van den Oever, Koen"
  - "Shropshire, Christine"
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.1075"
volume: 67
issue: 6
pages: "1525-1552"

source: "AMJ/vol-67-no-6"
pdf_path: "library/AMJ/vol-67-no-6/pdfs/Oever 2024 More than a Feeling How Board Member Displays of Anger and Happiness Influence Strategic Decisions.pdf"
text_path: "library/AMJ/vol-67-no-6/text/Oever 2024 More than a Feeling How Board Member Displays of Anger and Happiness Influence Strategic Decisions.txt"
ingested_at: "2026-05-05"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-12"

paper_type: "empirical-quantitative"
keywords:
  - "board of directors"
  - "displayed emotions"
  - "anger"
  - "happiness"
  - "nonverbal communication"
  - "strategic decision-making"
  - "focused influence"
  - "diffuse influence"
  - "scrutinizing governance"
  - "participative governance"
  - "peak emotional displays"
  - "duration of discussion"
theory:
  - "emotions as social information (EASI) model (Van Kleef, De Dreu & Manstead, 2010)"
  - "behavioral perspectives on corporate governance (Boivie et al., 2016, 2021)"
  - "strategic leadership system view (Luciano, Nahrgang & Shropshire, 2020)"
  - "scrutinizing vs. participative governance (public policy literature; Louwerse & Otjes, 2019)"
  - "peak-end rule / gestalt characteristics of experience (Ariely & Carmon, 2000)"
topics:
  - "board-of-directors"
  - "corporate-governance"
  - "emotions-at-work"
  - "leadership-behavior"
unit_of_analysis: "individual"
level_of_theory: "micro"
dependent_variable_family: "social"
methods: "Logit regression analyses on observational, video-coded data from 68 in-person board meeting recordings of four Dutch water management organizations; emotional displays measured at the static-image level using Microsoft Azure Face API (supervised machine learning of facial expressions across 145,370 individual frames), aggregated to peak (maximum) anger and happiness per director-agenda item; two dichotomous DVs (focused influence = top-manager promise/concession; diffuse influence = board majority approval of a change initiative); director-agenda item analytical level (n = 1,755 for focused, 1,666 for diffuse); robustness checks include control function approach with instrumental variables, causal sensitivity analyses (tipr; robustness of inference to replacement), supplemental analyses of early/late/duration peaks, sum-of-emotions, alternative negative emotions, and validation against human coders."
sample:
  industry: "Public water management (Dutch water authorities — fiduciary boards charged with territorial safety, water quantity and quality, and sewage treatment, with average annual budget of 146 million euros)"
  country: "Netherlands"
  time_period: "Not reported in paper"
  units: "Director-agenda item observations within board meetings (151 unique directors, 366 unique agenda items, 68 unique meetings across 4 organizations)"
  n: "1,755 director-agenda item observations (focused-influence model); 1,666 (diffuse-influence model); from 366 agenda items, 68 board meetings, 4 Dutch water management organizations, 151 unique directors"

evidence:
  sample_n: "sample includes 151 unique directors, 366 unique"
  sample_country: "four Dutch water management"
  sample_industry: "water authorities are financially independent as"
  sample_time_period: "Not reported in paper"
  theories_overview: "first theorize how anger can impact focused"
  methods_overview: "we adopted logit modeling"
  keywords_source: "displays of anger and happiness by board members"
  hypotheses_source: "Hypothesis 3a. Duration of the discussion will attenuate the relationship between peak displayed anger"
  measures_overview: "To measure diffuse influence, we coded a dummy"
  findings_overview: "(b 5 1.71, p 5 .05), in support of Hypothesis 2."
---

# More than a Feeling: How Board Member Displays of Anger and Happiness Influence Strategic Decisions

**Abstract**
To examine board members' influence in strategic decision-making, we consider the role of emotion displays during board meetings. We build a grounded model of how board members influence strategic decisions, which can occur directly from one director to a top manager or indirectly from one board member through the rest of the board. Drawing from the literature on nonverbal communication, we theorize that displays of anger and happiness by board members increase their focused or diffuse influence, respectively, over strategic decisions proposed by top management. We further hypothesize that the duration of the discussion moderates these main effects. Analyses on 366 agenda items from 68 board meetings of four Dutch water management organizations support our predictions that board member emotional displays indeed impact strategic decision outcomes via focused and diffuse influence processes. Our results also suggest that the duration of an agenda item's discussion attenuates the association between board members' displayed anger and their focused influence. These findings offer insights and new avenues for research in corporate governance, emotions, and communications, and have implications for our scholarly and practical understanding of how board members influence strategic decisions.

**Research Question**
How are board member displays of anger and happiness associated with influence on strategic decisions, and how does the duration of discussion of an agenda item moderate these emotion-influence relationships during board meetings?

**Hypotheses / Propositions**
- H1: Peak displayed anger by a board member is associated with a greater likelihood of focused influence (positive).
- H2: Peak displayed happiness by a board member is associated with a greater likelihood of diffuse influence (positive).
- H3a: Duration of the discussion attenuates (weakens) the association between peak displayed anger and focused influence (negative moderation).
- H3b: Duration of the discussion strengthens the association between peak displayed happiness and diffuse influence (positive moderation).

**Mechanism Process**
- IVs: Director peak displayed anger and director peak displayed happiness (maximum facial-expression intensity per director-agenda item, measured via Microsoft Azure Face API on 145,370 video frames).
- DVs: Focused influence (top manager makes promise/concession to amend proposed decision in response to a director) and diffuse influence (director-submitted change initiative receives board majority support).
- Moderator: Duration of discussion (sum of frames of speaking TMT and board members per agenda item).
- Controls: Board and TMT average and peak displayed anger/happiness; number of speaking board members; number of sponsors; director and board demographics (gender, political affiliation, stakeholder category, party leader, dominant coalition, seats, tenure, newcomer); board size, gender and ideological diversity, average meeting duration, meeting frequency, average tenure; organization and chairperson dummies.

Drawing on the EASI model, the paper argues that displayed emotions function as social information that triggers inferences about the emoter and the situation. Anger displays signal a need for change, convey dominance and determination, and push observers (especially less-powerful top managers) toward concession in dyadic, high-power-differential exchanges (scrutinizing governance), producing focused influence. Happiness displays signal cooperation and elicit appraisals of warmth, competence, and likeability, encouraging peer board members to support a change initiative through majority vote (participative governance), producing diffuse influence. Discussion duration weakens the anger-focused-influence link because additional stimuli crowd out the peak-anger signal as recollection fades and information-processing demands grow.

**Data & Measures**
Novel observational dataset of 68 complete videotaped in-person board meetings from four Dutch water management organizations (downloaded from the organizations' public webpages), converted into 145,370 individual static facial images. Emotions were coded with the Microsoft Azure Face API (supervised machine learning), which outputs intensity weights from 0 to 1.0 for each of eight facial expressions per image. Analyses are conducted at the director-agenda item level (n = 1,755 focused-influence model; n = 1,666 diffuse-influence model).
- IVs: Director peak displayed anger and director peak displayed happiness, each measured as the maximum Face API intensity of the respective emotion across a board member's images for an agenda item.
- DVs: Focused influence, a dummy coded 1 when the top manager responds to the director's statement with a promise or commitment to alter the proposal; diffuse influence, a dummy coded 1 when the director's change initiative receives board majority support.
- Moderator: Duration of discussion, the sum of the total frames of speaking TMT and board members per agenda item.
- Controls: board- and TMT-level average and peak displayed anger/happiness (to rule out emotional convergence and contagion), number of speaking board members, number of sponsors, director and board demographics, board size and diversity indices, meeting duration and frequency, tenure, and organization/chairperson dummies.
- Estimation and identification: logit (logistic) regression; endogeneity addressed with a control-function approach using directors' average displayed anger/happiness as instruments, alongside causal sensitivity analyses (robustness of inference to replacement; tipr). The design is observational and associational, with identification checks probing robustness to endogeneity and unmeasured confounders rather than establishing experimental causation.

**Key Findings**
- H1 supported (Model 2): director peak displayed anger is positively associated with focused influence (b = 1.43, p = .004); a one-SD increase in peak anger makes the odds of focused influence about 41% higher.
- H2 supported (Model 5): director peak displayed happiness is positively associated with diffuse influence (b = 1.71, p = .05); a one-SD increase in peak happiness makes the odds of diffuse influence about 94% higher.
- H3a supported (Model 3): the peak-anger by discussion-duration interaction is negative and significant (b < -0.01, p = .05); the anger-focused-influence association is stronger when the discussion is shorter.
- H3b not supported (Model 6): the peak-happiness by discussion-duration interaction is nonsignificant (b < 0.01, p = .19).

Discriminant pattern: peak anger did not produce diffuse influence and peak happiness did not produce focused influence; among other negative emotions, only contempt showed marginal focused-influence support (b = 2.21, p = .06). Robustness: effects were strongest for punctuated (peak) displays. With summed emotions, H3a held but H1 and H2 did not; excluding ambiguous influence cases, H1 and H2 held but H3a did not.

**Theoretical Contribution**
The paper opens the "black box" of boardroom interactions by theorizing two distinct paths to director influence over strategic decisions — focused (direct, dyadic, scrutinizing) and diffuse (board-wide, participative) — and links each to a different discrete emotion (anger vs. happiness) operating through different EASI mechanisms. By bridging behavioral corporate-governance research with social-psychology work on displayed emotions and EASI theory, the paper offers contextualized theory on when and how directors shape strategic decision outcomes, advances research on nonverbal communication in management, and surfaces novel implications for agency and resource-dependence views of board functioning by treating directors as heterogeneous in their persuasive ability.

**Practical Implication**
The study shows a director's focused influence is greatest when an anger display is intense and the discussion is short, whereas longer discussions attenuate that influence; happiness displays facilitate participative consensus while anger is more effective in pointed dyadic exchanges. Nonverbal behavior in the boardroom thus emerges as a meaningful, potentially manageable lever in strategic decision-making.

**Limitations**
The authors could only collect emotional-display data on the speaking director and top manager, not on observers' reactions, so influence as the theorized mechanism is not directly measured. They were unable to capture other forms of power (structural, prestige) or to identify moderating individual characteristics that would enrich the role of power; influence pathways outside the boardroom (coalition formation, committee work) are not observed. The Dutch water-management context, with larger boards and a formal change-initiative procedure, may not generalize to all corporate-board settings, although sensitivity analyses suggest results are robust to plausible unmeasured confounders.

**Future Research**
Future research should examine the strategic and intentional use of emotions by directors, the role of power (formal, structural, prestige, political capital) as a moderator of emotion-influence links, gendered or demographic patterns in scrutinizing versus participative governance, the efficacy of these governance mechanisms in other policymaking contexts, and combinations or sequences of multiple emotions (including contempt, which showed marginal focused-influence effects). Scholars are also encouraged to study the longer-term, repeated dynamics of director emotion regulation and how directors navigate the social complexity of board interactions over time.

**APA 7th Citation**
van den Oever, K., & Shropshire, C. (2024). More than a feeling: How board member displays of anger and happiness influence strategic decisions. *Academy of Management Journal*, 67(6), 1525-1552. https://doi.org/10.5465/amj.2022.1075
