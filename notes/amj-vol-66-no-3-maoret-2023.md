---
id: amj-vol-66-no-3-maoret-2023
title: "On the Status Shocks of Tournament Rituals: How Ritual Enactment Affects Productivity, Input Provision, and Performance"
authors:
  - "Maoret, Massimo"
  - "Marchesini, Giacomo"
  - "Ertug, Gokhan"
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2020.0585"
volume: 66
issue: 3
pages: "926-952"

source: "AMJ/vol-66-no-3"
pdf_path: "library/AMJ/vol-66-no-3/pdfs/Maoret 2023 On the Status Shocks of Tournament Rituals How Ritual Enactment Affects Productivity, Input Provision, and Performance.pdf"
text_path: "library/AMJ/vol-66-no-3/text/Maoret 2023 On the Status Shocks of Tournament Rituals How Ritual Enactment Affects Productivity, Input Provision, and Performance.txt"
ingested_at: "2026-05-23"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-quantitative"
keywords: ["status shocks", "tournament rituals", "ritual enactment", "emotional energy"]
theory: ["interaction ritual theory (Collins, 2004)", "status / signaling theory"]
topics: ["organizational-behavior-hrm", "signaling-theory"]
unit_of_analysis: "individual"
level_of_theory: "micro"
dependent_variable_family: "social"
methods: "Quantitative causal-inference design using difference-in-differences (DID) with player, season, player-by-season, and game fixed effects, plus a regression discontinuity design (RDD) and coarsened exact matching as robustness checks; standard errors clustered by player-by-season."
sample:
  industry: "Professional sports (men's professional basketball, NBA)"
  country: "United States (NBA; league also includes one Canadian franchise)"
  time_period: "1983/84 to 2016/17 NBA seasons"
  units: "Player-game observations; treatment = All-Star Game participants, control = 'Almost All-Stars'"
  n: "33,507 game-level observations from 1,676 player-seasons (734 treatment, 942 control)"

evidence:
  sample_n: "a sample of 1,676 player-seasons (734 in the treatment and 942 in the control group)"
  sample_country: "data from the National Basketball Association"
  sample_industry: "the ASG in professional"
  sample_time_period: "from the 1983/84 to the"
  theories_overview: "We leverage sociological work on interaction rituals"
  methods_overview: "We employ difference-in-differences and regression discontinuity designs on game-level data from the National Basketball Association"
  keywords_source: "we theorize that, when status shocks include a ritualistic conferment of social prestige—such as in the case of “tournament rituals”"
  hypotheses_source: "lead to higher productivity (Hypothesis 1)"
  measures_overview: "We use Minutes Played as a measure of inputs"
  findings_overview: "the ASG has a positive effect on Touches per Minute"
---

# On the Status Shocks of Tournament Rituals: How Ritual Enactment Affects Productivity, Input Provision, and Performance

**Abstract**
We propose a novel process through which status shocks may enhance performance. Specifically, we theorize that, when status shocks include a ritualistic conferment of social prestige—such as in the case of “tournament rituals”—participating in that ritual enactment may increase tournament winners’ productivity and improve the inputs they receive, thereby improving their overall performance. We also consider the duration of that performance improvement, finding a decay that is consistent with our theorized mechanisms that are based on emotional energy. Our study shows that status shocks may carry not only informational value, as signals of quality, but also symbolic and social value that change the behavior of individuals who receive these shocks and of the input providers with whom they interact. We employ difference-in-differences and regression discontinuity designs on game-level data from the National Basketball Association to provide causal evidence for our hypotheses.

**Research Question**
Beyond the well-established informational "signaling" pathway, is there another process through which a status shock causally affects winners' subsequent performance? The authors ask whether participating in the ritualistic conferment of a status-boosting award ("ritual enactment") increases tournament winners' productivity and the inputs they receive, and how durable that effect is.

**Hypotheses / Propositions**
- H1: All else equal, participating in the ritualistic conferment of prestige will cause an increase in the productivity of tournament ritual winners (predicted positive).
- H2: All else equal, participating in the ritualistic conferment of prestige will cause tournament ritual winners to have an advantage in the inputs they receive (predicted positive).
- H3a: All else equal, participating in the ritualistic conferment of prestige will cause an increase in tournament ritual winners' overall performance (predicted positive).
- H3b: The positive effect of participating in the ritualistic conferment of prestige on tournament ritual winners' overall performance will decrease over time (predicted negative time trend).

H1 and H2 are the two proximal consequences the paper attributes to the emotional-energy boost generated by ritual enactment; H3a is their aggregate performance consequence and H3b its predicted decay.

**Mechanism Process**
- IV(s): Participation in the ritual enactment (the All-Star Game), operationalized as the interaction Participation in the ASG × Post ASG; exposure measured as minutes played in the ASG.
- DV(s): Player productivity (NBA Efficiency Rating per Minute and over Usage), inputs received (Minutes Played from coaches; Touches per Minute and Usage Rate from teammates), and overall performance (NBA Efficiency Rating).
- Mediators: "Emotional energy" (EE) — a boost to confidence, enthusiasm, and initiative — theorized but not directly measured (proxied via in-ritual exposure/minutes).
- Moderators: Time since the ritual (passage of games post-ASG), which decays the performance boost.

Drawing on Collins's (2004) interaction ritual theory, the authors argue that physically enacting a prestige-conferring ritual charges winners with emotional energy, which raises their drive to convert inputs into outputs (productivity) and, by creating an EE gap relative to non-participating input providers, attracts greater deference and resources (more touches/usage) from teammates. Because EE is transitory, the performance gain decays over subsequent games. The NBA setting separates ritual enactment from signaling because the All-Star announcement and the game occur weeks apart and coaches/teammates already have little uncertainty about player quality.

**Data & Measures**
Longitudinal sample of NBA players' game-level performance from the 1983/84 to the 2016/17 seasons, a range chosen because game-level data are incomplete before 1983/84 and the All-Star selection process changed substantially after 2016/17. All performance, roster, demographic, and ASG voting/participation data come from Basketball-Reference.com. The estimation window is 20 games per player-season: the 10 games before and the 10 games after the ASG. Treatment group = the 24 players selected to participate in the ASG each season (starters or reserves), restricted to those with nonzero ASG playing time. Control group = "Almost All-Stars," players ranked in the top 10 of fan voting who were not selected to participate. Final sample = 1,676 player-seasons (734 treatment, 942 control; 424 unique players) and 33,507 game-level observations.
- IV: the interaction Participation in the ASG x Post ASG. Participation in the ASG is a dummy coded 1 for treatment-group players in the focal season; Post ASG is a dummy coded 1 for games played after the ASG in that season.
- DV, overall performance (H3a/H3b): NBA Efficiency Rating, the composite the NBA officially uses to assess a player's performance in each game, computed as Points + Rebounds + Steals + Assists + Blocked Shots - Turnovers - Missed Shots.
- DV, productivity (H1): NBA Efficiency Rating per Minute Played and NBA Efficiency Rating over Usage, both constructed as ratios of overall performance to the level of input received.
- DV, inputs received (H2): Minutes Played for inputs from coaches; Touches per Minute and Usage Rate for inputs from teammates. Touches is an official NBA statistic aggregating the actions a player can take while possessing the ball (pass, shoot, draw a foul, commit a turnover), used because actual passes received are available only from 2013/14 onward; the two correlate at r = .91. Touches is scaled by minutes played to keep teammate inputs orthogonal to the coach's input. Usage Rate is the percentage of offensive plays that involve the focal player.
- Mediator: emotional energy is not measured. Its proxy is in-ritual exposure, tested as Post ASG x Number of minutes played in the ASG, with that variable set to 0 for control-group players.
- Controls: NBA Experience, Tenure with Team, Ln(1 + Number of Previous ASG Selections) as the player's status stock, PER in Previous Season as underlying quality, Game Won, Home Game, Progressive Game Number, and Participation in the ASG x Progressive Game Number to absorb differential trends across the two groups. Age is excluded because it correlates with NBA Experience at r = .91.

The paper claims causal identification and names its strategies explicitly. The main design is difference-in-differences (Bertrand, Duflo, & Mullainathan, 2004) with player, season, and game fixed effects, plus a stricter specification that replaces the player and season fixed effects with Player x Season fixed effects; robust standard errors are clustered by Player x Season. H3b is tested with a spline regression that splits Progressive Game Number into pre-ASG and post-ASG segments, each interacted with the treatment dummy. Supporting identification checks are a placebo DID that substitutes the All-Star announcement date for the ASG date (to separate ritual enactment from signaling), alternative control groups including all other players, coarsened exact matching, a "41st chair" comparison of Almost All-Stars against all other players, and a regression discontinuity design around the fan-voting cutoff using Relative Votes from Threshold with second-order polynomials fitted separately on each side of the cutoff.

**Key Findings**
H1 supported. Participation in the ASG x Post ASG is positive and significant for NBA Efficiency Rating per Minute (b = 0.034, p < .001, Model 2) and unchanged under the stricter Player x Season fixed effects (b = 0.034, p < .001, Model 3); for the alternative productivity measure, NBA Efficiency Rating over Usage, the coefficient is 0.043, p < .01 (Models 4 and 5). After the ASG the baseline treatment-control gap is amplified by 117% in NBA Efficiency Rating per Minute (from 0.029 to 0.063) and by 123% in NBA Efficiency Rating over Usage (from 0.035 to 0.078), which the authors translate into a 15% and a 12% increase relative to the within-season standard deviation of productivity.

H2 supported for teammate-provided inputs but not for coach-provided playing time. The coefficient on Participation in the ASG x Post ASG for Minutes Played is statistically nonsignificant (b = 0.079, p = .783, Model 6, confirmed in Model 7), so ASG participants do not seem to receive more playing time from coaches. Teammate inputs do increase: Touches per Minute (b = 0.069, p < .001, Models 8 and 9, with the treatment-control difference amplified by 147%, from 0.047 to 0.116) and Usage Rate (b = 0.668, p < .01, Model 10), corresponding to a 19% and a 13% increase in within-season standard-deviation terms. In the discussion the authors read the coach null as an indication that occupying a higher position in a formal structure such as an organizational hierarchy might shield certain individuals from the influence of ritual enactment.

H3a supported. Participation in the ASG x Post ASG is positive and significant for overall NBA Efficiency Rating (b = 1.314, p < .001, Model 11, which includes Player x Season and game fixed effects).

H3b supported. In the spline specification the post-ASG boost (b = 1.375, p < .001, Model 12) declines by approximately 0.15 after every game: Participation in the ASG x Progressive Game Number post ASG is negative and significant (b = -0.15, p < .001), while the corresponding pre-ASG trend is not significant (b = -0.03, p = .45), so the decay is specific to the post-ritual window. Plotted in five-game bins, the effect is positive and statistically significant for the first five games after the ASG (b = 0.915, p = .003); the 5-to-10-game bin is smaller and not statistically significant, and the downward trend continues in the 10-15 and 15-20 bins, which the authors describe as a halo effect of limited duration.

Mechanism and robustness evidence. Consistent with the emotional-energy account, Post ASG x Number of minutes played in the ASG is positive and significant (b = 0.06, p < .001), so the performance boost is amplified by a player's exposure during the ritual. The placebo DID that uses the All-Star announcement date instead of the ASG date produces no statistically significant changes in productivity, inputs received, or overall performance, which the authors treat as ruling out signaling as a credible alternative explanation. The RDD confirms a discontinuity at the voting cutoff: All-Stars just above it have an NBA Efficiency Rating 3.91 points higher across the 10 games after the ASG than players who barely missed selection (p < .001, Model A-1), and the result holds across four progressively narrower intervals (b = 3.45, p < .01 in the narrowest, Model A-4). Comparing Almost All-Stars with all other players who did not make the top 10 yields no statistically significant difference, supporting the assumed "41st chair effect," and the main results also hold with all other players as the control group and under coarsened exact matching.

**Theoretical Contribution**
The paper's primary contribution is introducing "ritual enactment" as a novel, symbolic/social process—distinct from informational signaling—through which status shocks causally affect performance. It shows status shocks affect not just audiences' perception of output quality but the production of output itself (input acquisition and the transformation of inputs into outputs), and it distinguishes status "shocks" from self-reinforcing status "stocks," demonstrating that the ritual-enactment advantage is of limited duration.

**Practical Implication**
Managers can use ceremonial, prestige-conferring events (not merely announcing winners or paying incentives) to generate motivational and performative boosts among employees, and could organize smaller-scale tournament-ritual-like events within teams or organizations. Because such events may reallocate resources via shifting deference, managers should monitor whether the resulting distribution stays fair and effective for organizational goals.

**Limitations**
The authors cannot measure emotional energy directly, so EE is inferred rather than observed (they provide indirect support via in-ritual exposure). Because the chosen input providers (coaches and teammates) have low uncertainty about player quality, the design isolates ritual enactment but precludes a direct comparison of the magnitude and duration of signaling versus ritual enactment within the same setting.

**Future Research**
Future work could compare the relative magnitude and duration of signaling versus ritual enactment in settings where audiences hold quality uncertainty, examine how formal/informal social structures (e.g., hierarchy, ideology) condition ritual-enactment effects, and study the interaction between status stocks and status shocks. Scholars could also investigate which ritual characteristics (formal vs. informal, public vs. private, field-level vs. organizational) and individual differences amplify or dampen the effect, and whether the framework extends to rituals routinely enacted within organizations.

**APA 7th Citation**
Maoret, M., Marchesini, G., & Ertug, G. (2023). On the status shocks of tournament rituals: How ritual enactment affects productivity, input provision, and performance. *Academy of Management Journal*, 66(3), 926–952. https://doi.org/10.5465/amj.2020.0585
