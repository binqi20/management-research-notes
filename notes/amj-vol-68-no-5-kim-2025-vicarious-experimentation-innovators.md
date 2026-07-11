---
id: amj-vol-68-no-5-kim-2025-vicarious-experimentation-innovators
title: "Vicarious Experimentation: Do Innovators Learn by Being Imitated?"
authors:
  - "Kim, S."
  - "Posen, H. E."
  - "Ganco, M."
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.1122"
volume: 68
issue: 5
pages: "1108-1129"

source: "AMJ/vol-68-no-5"
pdf_path: "library/AMJ/vol-68-no-5/pdfs/Kim 2025 Vicarious Experimentation Do Innovators Learn by Being Imitated.pdf"
text_path: "library/AMJ/vol-68-no-5/text/Kim 2025 Vicarious Experimentation Do Innovators Learn by Being Imitated.txt"
ingested_at: "2026-07-11"
extraction_model: "claude-opus-4-8"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["vicarious experimentation", "learning by being imitated", "imitation", "vicarious learning", "causal ambiguity", "strategic experimentation", "organizational learning", "video game industry"]
theory: ["vicarious experimentation (novel construct)", "strategic experimentation (Felin & Zenger, 2009; Gans et al., 2019; Ries, 2011)", "vicarious learning (Argote & Miron-Spektor, 2011; Haunschild & Miner, 1997)", "organizational learning (March, 1991; Levinthal & March, 1993)", "knowledge spillovers (Cohen & Levinthal, 1989)", "absorptive capacity (Cohen & Levinthal, 1990)", "causal ambiguity (Lippman & Rumelt, 1982; Rivkin, 2000)"]
topics: ["innovation-management", "competitive-strategy", "absorptive-capacity"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Quantitative observational study of 438 original-sequel video-game dyads; OLS regression with genre, publisher, and sequel-release-year fixed effects and robust standard errors; interaction terms test two moderators; robustness checks include Oster (2019) unobservable-selection bounds, Heckman selection correction, two-stage least squares, and alternative measures/specifications."
sample:
  industry: "Console video game industry (PlayStation 2 games across 28 genres)"
  country: "Not reported in paper"
  time_period: "2000-2013 (PS2 console lifespan)"
  units: "Original-sequel game dyads (innovator firms' game series)"
  n: "438 original-sequel game pairs (drawn from 3,051 PS2 games)"

# Mandatory evidence anchors (v3 — Layer 1 faithfulness audit).
evidence:
  sample_n: "a dataset of 438 dyads of original and subsequent"
  sample_country: "Not reported in paper"
  sample_industry: "We built a dataset of 3,051 PlayStation 2 (PS2) games"
  sample_time_period: "long lifespan (2000–2013), making it easier to track"
  theories_overview: "This concept extends the logic of strategic experimentation by highlighting"
  methods_overview: "The results of the ordinary least squares (OLS)"
  keywords_source: "it takes the form of vicarious experimentation, where an imitator’s near-clone"
  hypotheses_source: "Hypothesis 2. The positive relationship between the"
  measures_overview: "sequel game with the average critics’ rating scores"
  findings_overview: "quality of the sequel game (Model 2: b 5 0.17, p , .01;"
---

# Vicarious Experimentation: Do Innovators Learn by Being Imitated?

**Abstract**
Strategy scholars conventionally view imitation as a one-way knowledge transfer from an innovating firm to an imitating firm. We propose that being imitated also serves as a source of learning for the innovator. An innovator learns by being imitated—observing the imitator’s choices and outcomes and comparing them to its own. A key challenge in such learning, and in vicarious learning more broadly, is causal ambiguity in identifying the factors that drive observed performance outcomes. We theorize that an innovator’s learning by being imitated is particularly effective in overcoming causal ambiguity when it takes the form of vicarious experimentation, where an imitator’s near-clone of the innovator’s product functions as a quasi-experimental treatment from which the innovator can learn. This concept extends the logic of strategic experimentation by highlighting how firms can learn from experiments they do not control. We test our theory in the video game industry, demonstrating that vicarious experimentation enhances the quality of the innovator’s next-generation product and offering support for the theorized boundary conditions under which this effect holds.

**Research Question**
How and what can innovators learn from being imitated? The paper asks whether an innovator's product being near-cloned by imitators functions as a source of quasi-experimental learning that improves the quality of its next-generation product, and identifies the boundary conditions under which this effect holds.

**Hypotheses / Propositions**
H1. The extent of vicarious experimentation is positively related to the quality of the next generation of the innovator's original product (controlling for the quality of the original product).
H2. The positive relationship between the extent of vicarious experimentation and the quality of the innovator's next-generation product is stronger if the imitators have higher prominence in the market.
H3. The positive relationship between the extent of vicarious experimentation and the quality of the innovator's next-generation product is weaker if the innovator's tacit knowledge is disrupted by changes in the product development unit.

**Mechanism Process**
- IV(s): Extent of vicarious experimentation — aggregated peripheral-feature variation across imitators' near-clones of the innovator's original game (core features held constant)
- DV(s): Quality of the innovator's next-generation (sequel) game (critics' ratings, 0–100)
- Mediators: Not reported in paper
- Moderators: Imitator market prominence (H2, strengthens the effect); loss of tacit product-specific knowledge via a change in the development unit (H3, weakens the effect)

Being imitated supplies the innovator with a set of quasi-experiments it does not run itself: an imitator's near-clone holds the original's core features fixed while varying peripheral features, so the innovator's original acts as the control and the near-clone as the treatment. By observing these peripheral variations and their market feedback, the innovator can reduce causal ambiguity and infer which feature changes improve performance, then retain, add, or delete features in its sequel. The learning is amplified when imitators are prominent — their products generate more visible, comprehensive, and reliable observational data — and it depends on the innovator retaining the tacit, product-specific knowledge (a form of absorptive capacity) needed to interpret and integrate the insights; disrupting the development unit erodes that knowledge and dampens the benefit.

**Data & Measures**
- Data: 438 original-sequel game dyads drawn from a base of 3,051 PS2 games (2000–2013, 28 genres), combining MobyGames, Metacritic, and IGDB; near-clones are later games that retain the original's core features (released between the original and the sequel). An additional 5,449 games on other consoles (e.g., Wii, Xbox) support cross-platform-imitation tests.
- DV — sequel quality: average critics' rating scores (0–100) from MobyGames and Metacritic.
- IV — vicarious experimentation: aggregated angular separation (Jaffe, 1986) of IGDB game-keyword vectors between each near-clone and the original (peripheral-feature variation with core features fixed), summed over the near-clone pool.
- Moderator — imitator prominence: average of imitator firms' market shares in the focal genre in year y–1 (with entropy-based, award-winning, and average-clone-sales alternatives).
- Moderator — loss of tacit knowledge: dummy = 1 if the game development unit changed between original and sequel (with developer-retention alternatives).
- Controls: quality and sales of the original game, years since the original, generation in the series, genre concentration (HHI), genre popularity, development-team size (plus an imputation dummy), and average game-feature popularity; genre (28), publisher (46), and sequel-release-year (10) fixed effects.
- Identification: associational OLS with robust standard errors; the authors state the results do not establish strict causality and instead bound unobservable selection (Oster, 2019), apply Heckman correction and two-stage least squares, and run alternative-explanation tests.

**Key Findings**
- H1 supported: vicarious experimentation is positively associated with sequel quality (Model 2: b = 0.17, p < .01; Model 3: b = 0.16, p < .01); a 1.0 SD increase in vicarious experimentation corresponds to roughly a 0.1 SD improvement in sequel quality in the main-effects model.
- H2 supported: the vicarious experimentation × imitator prominence interaction is positive and significant (Model 4: b = 0.04, p < .05) — the learning effect is driven by prominent imitators.
- H3 supported: the vicarious experimentation × loss-of-tacit-knowledge (development-unit change) interaction is negative and significant (Model 4: b = -0.29, p < .05) — the benefit disappears when the development studio changes.
- In the fully specified Model 4 the main effect of vicarious experimentation is not significant (b = 0.019, ns), confirming that imitator prominence and tacit-knowledge retention act as boundary conditions rather than the effect operating unconditionally; for prominent (top-20%) imitators with an unchanged development unit, a 1.0 SD increase corresponds to about a 0.3 SD increase in sequel quality.
- Robustness: results hold under alternative IV measures (imitation counts, unique feature bundles), alternative prominence measures (entropy of market shares, award-winning status, average clone sales), Oster (2019) bounds (δ = 76.05), Heckman selection correction, two-stage least squares, feature-removal-only cases, and cross-platform-imitation checks, although some alternative specifications weaken slightly.

**Theoretical Contribution**
The paper introduces "vicarious experimentation" as a novel mechanism, reframing being imitated not as mere knowledge leakage but as a source of targeted, causal, and actionable learning for the innovator. It positions the construct at the intersection of vicarious learning and learning from one's own experimentation — the innovator's original is the control and the imitator's near-clone is the treatment — thereby extending the strategy-as-experimentation perspective to experiments the focal firm does not control and specifying causal-ambiguity-based boundary conditions (near-clonal peripheral variation, imitator prominence, and tacit-knowledge retention). In doing so it foregrounds innovator agency in imitation research, which has traditionally cast innovators as passive parties whose knowledge is expropriated.

**Practical Implication**
From a managerial perspective, the study suggests firms may need to change their mindset about being imitated: rather than dismissing imitators as copycats with little to offer, innovators can study imitators' near-clones as opportunities to learn and improve their next-generation products. It also highlights the managerial importance of internal organizational factors — particularly retaining the tacit, product-specific knowledge of the original development team — because organizational changes that disrupt the development unit can inhibit the ability to learn from vicarious experimentation.

**Limitations**
The authors note that the interplay between competition and imitation is complex and not fully isolated, so the extent of competition may still shape how innovators learn from vicarious experiments. They do not fully examine the broader set of mechanisms (e.g., shifts in customer perceptions, competitive responses from rivals, and recombined knowledge spillovers) through which being imitated can affect an innovator, and they do not resolve whether being imitated benefits the innovator or the imitator more. Finally, the results do not establish strict causality — finding instruments or natural experiments for imitation remains difficult — so the design relies on extensive controls, unobservable-selection analysis (Oster, 2019), and tests ruling out alternative explanations.

**Future Research**
The authors call for research that disentangles imitation and competitive dynamics in more detail, and that develops a more comprehensive framework for how the interdependent mechanisms of being imitated jointly shape an innovator's outcomes over time. They encourage further work to explore causal relationships in imitation, and to weave together the strategy-as-experimentation, entrepreneurial-decision-making, Carnegie-tradition, and quasi-experimentation perspectives on which vicarious experimentation draws.

**APA 7th Citation**
Kim, S., Posen, H. E., & Ganco, M. (2025). Vicarious experimentation: Do innovators learn by being imitated? *Academy of Management Journal, 68*(5), 1108–1129. https://doi.org/10.5465/amj.2022.1122
