---
id: amj-vol-68-no-3-ploog-2024
title: "Rolling the Dice: Resolving Demand Uncertainty in Markets with Partial Network Effects"
authors:
  - "Ploog, J. N."
  - "Rietveld, J."
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0133"
volume: 68
issue: 3
pages: "598-619"

source: "AMJ/vol-68-no-3"
pdf_path: "library/AMJ/vol-68-no-3/pdfs/Ploog 2024 Rolling the Dice Resolving Demand Uncertainty in Markets with Partial Network Effects.pdf"
text_path: "library/AMJ/vol-68-no-3/text/Ploog 2024 Rolling the Dice Resolving Demand Uncertainty in Markets with Partial Network Effects.txt"
ingested_at: "2026-04-30"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-11"

paper_type: "empirical-quantitative"
keywords:
  - "network effects"
  - "partial network effects"
  - "demand uncertainty"
  - "diffusion of innovations"
  - "social features"
  - "product novelty"
  - "competition intensity"
theory:
  - "network effects theory"
  - "diffusion of innovations"
topics:
  - "innovation-management"
  - "competitive-strategy"
  - "consumer-psychology"
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "Endogenous treatment effects regression (linear endogenous treatment regression model) with heteroskedasticity-robust standard errors; Levene's test and heteroskedastic linear regression for variance comparison; coarsened exact matching (CEM) for robustness; instrumental variable (MtG events) in treatment equation."
sample:
  industry: "Global board games industry (nondigital tabletop games)"
  country: "Global (publishers from 77 countries)"
  time_period: "Board games released 2011-2017; data collected September 2020"
  units: "Board games (with and without collectible components)"
  n: "19,432 board games (225 with collectible components / CNGs)"

evidence:
  sample_n: "225 board games have collectible components"
  sample_country: "Publisher country dummies"
  sample_industry: "global board games industry, where board games"
  sample_time_period: "all board games released between 2011 and 2017"
  theories_overview: "literatures on network effects and the diffusion of innovations"
  methods_overview: "endogenous treatment effects model"
  keywords_source: "firms in markets with partial network effects"
  hypotheses_source: "Hypothesis 3a. Competition intensity negatively affects"
  measures_overview: "Second, we measure novelty by assessing a board"
  findings_overview: "The variance of owners for CNGs is 3.10 times"
---

# Rolling the Dice: Resolving Demand Uncertainty in Markets with Partial Network Effects

**Abstract**
It is commonly assumed that when markets are characterized by network effects, this universally affects all competing products. In reality, however, firms often have agency in terms of whether to incorporate social features that have the potential to generate network effects. When this is the case, markets are characterized by partial network effects—some products have network effects, whereas others compete on the basis of a standalone value proposition. In this study, we focus on the differences in demand uncertainty between network products and standalone products competing in such a market. We develop theory predicting how a product's social features interact with other known drivers of demand uncertainty to impact diffusion. We test our arguments in the global board games industry, where board games designed around the collection and trading of "collectible components" compete against traditional board games. Results show that network products exhibit greater variance in diffusion and that their diffusion is disproportionately affected by the degree of product novelty and the intensity and type of competition. Our findings contribute to the literatures on network effects and the diffusion of innovations.

**Research Question**
How does demand uncertainty differentially impact the diffusion of network products versus standalone products that compete in the same market? How do strategies to resolve consumers' perceived uncertainty affect the diffusion of network products compared to standalone products?

**Hypotheses / Propositions**
Baseline hypothesis. The diffusion of network products varies more widely than that of standalone products.
H1. Novelty negatively affects a product's diffusion, and this effect is more pronounced for network products than standalone products.
H2. Promoting early adoption positively affects a product's diffusion, and this effect is more pronounced for network products than standalone products.
H3a. Competition intensity negatively affects a product's diffusion, and this effect is more pronounced for network products than standalone products.
H3b. Competition from a hit product negatively affects a product's diffusion, and this effect is more pronounced for network products than standalone products.

**Mechanism Process**
- IV(s): Collectible components (network product dummy); Novelty (cosine distance of gameplay-mechanics vector); Kickstarter success (early-adoption promotion); Competition intensity (count of same-genre games released within +/- 3 months); Hit competition (presence of competitor with >=15% ownership share)
- DV(s): ln(Owners) two years after release (and variance of owners for baseline hypothesis)
- Mediators: Demand uncertainty (theoretical, not directly measured)
- Moderators: Collectible components moderates the effect of novelty, Kickstarter success, competition intensity, and hit competition on diffusion

Network products' value depends on attracting a large user base, generating greater consumer-perceived demand uncertainty than standalone products. The authors theorize that any factor amplifying (alleviating) demand uncertainty will disproportionately harm (help) the diffusion of network products. Empirically, novelty, competition intensity, and hit competition all interact negatively with collectible components on owners; the predicted positive effect of Kickstarter success on network products is reversed, which the authors attribute to a "chasm" between early adopters and mainstream consumers.

**Data & Measures**
Data are archival, drawn from Board Game Geek (collected September 2020), covering 19,432 board games released 2011-2017 (225 with collectible components / CNGs); Kickstarter backer and funding data were collected from Kaggle.com. Dependent variable: diffusion, measured as the natural log of the number of owners two years after release (for the baseline hypothesis, the variance of owners). Independent variables: collectible components (dummy = 1 if the game is a CNG); novelty (cosine distance between a game's 182-mechanic gameplay vector and the genre-matched market-average vector of games released in the prior five years); Kickstarter success (dummy = 1 if funded via a successful Kickstarter campaign); competition intensity (count of same-genre games released within +/- 3 months of the focal game, divided by its number of genres); hit competition (dummy = 1 if a competitor with >= 15% ownership share was released in the same six-month window). Controls include self-published, publisher experience, and ln(team size), plus publisher-country (77), genre (12), month-of-release (11), and year-of-release (6) fixed effects. Identification uses a linear endogenous treatment regression model to address the nonrandom assignment of collectible components (no natural experiment or exogenous shock is available), with MtG events (logged Magic the Gathering events in the publisher's country two years before launch) in the treatment equation; robustness uses coarsened exact matching (CEM).

**Key Findings**
The baseline hypothesis is supported: the variance of owners for CNGs is 3.10 times larger than that of standalone board games (p = .00), confirmed by both Levene's test and a heteroskedastic linear regression. H1 is supported: novelty's main effect is negative and significant (b = -0.35, p = .00), and its interaction with collectible components is also negative and significant (b = -0.60, p = .09); a 25% increase in novelty is associated with a 15.34% decline in owners for CNGs versus 7.33% for standalone games. H2 is not supported and in fact reverses: the main effect of Kickstarter success is positive and significant (b = 0.89, p = .00), but its interaction with collectible components is negative and significant (b = -1.17, p = .00) — opposite the predicted positive direction — so a successful Kickstarter campaign is associated with a 24.76% decrease in owners for CNGs while more than doubling owners for standalone games. H3a is supported: competition intensity's main effect (b = -0.0011, p = .00) and its interaction with collectible components (b = -0.0014, p = .01) are both negative and significant; 150 additional same-genre games within six months are associated with a 15.50% decline in owners for CNGs versus 9.65% for standalone games. H3b is supported: hit competition's main effect (b = -0.08, p = .07) and its interaction with collectible components (b = -0.81, p = .02) are both negative and significant; a hit competitor is associated with a 58.85% reduction in owners for CNGs versus 7.48% for standalone games. Results remain consistent under a coarsened-exact-matched, reweighted sample (3,863 observations).

**Theoretical Contribution**
The paper relaxes the universality assumption in the network effects literature by introducing markets with partial network effects, demonstrating that nonnetwork factors interact with social features to differentially shape diffusion of network versus standalone products. It also flips the diffusion of innovations literature's typical firm-side perspective on demand uncertainty toward the customer's perspective, showing that drivers of perceived uncertainty have disproportionately negative effects on network products' diffusion.

**Practical Implication**
Managers in markets with partial network effects should weigh whether and when to add social features by considering how product-market decisions (novelty, timing of release, competitive context) interact with social features to shape consumers' perceived uncertainty. Pairing network products with less novel designs and avoiding launches in highly competitive windows can mitigate downside diffusion risk; crowdfunding may not benefit network products and can dampen their diffusion.

**Limitations**
The study relies on archival data from a single, contextualized analog setting (Board Game Geek), which may not generalize to digital product markets. Demand uncertainty is not directly measured, nor is variation in early- versus late-adopter perceptions captured. Crowdfunding is the only frontloading mechanism considered; alternatives such as betas, preorders, crowdsourcing, and influencer partnerships are not examined.

**Future Research**
Future work should replicate findings in other industries—including digital product markets—and use laboratory experiments or demand-uncertainty questionnaires to measure perceived uncertainty more directly. Researchers could also study contexts with truly heterogeneous network effects, settings where firms add network value post-release, two- or multisided platform markets, and the dynamics of user engagement (versus mere adoption) in sustaining network effects.

**APA 7th Citation**
Ploog, J. N., & Rietveld, J. (2025). Rolling the dice: Resolving demand uncertainty in markets with partial network effects. *Academy of Management Journal*, 68(3), 598-619. https://doi.org/10.5465/amj.2023.0133
