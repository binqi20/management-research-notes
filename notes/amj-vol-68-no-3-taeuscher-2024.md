---
id: amj-vol-68-no-3-taeuscher-2024
title: "It Is Not the Whole Story: Toward a Broader Understanding of Entrepreneurial Ventures’ Symbolic Differentiation"
authors:
  - "Taeuscher, Karl"
  - "Lounsbury, Michael D."
year: 2025
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0581"
volume: 68
issue: 3
pages: "648-668"

source: "AMJ/vol-68-no-3"
pdf_path: "library/AMJ/vol-68-no-3/pdfs/Taeuscher 2024 It Is Not the Whole Story Toward a Broader Understanding of Entrepreneurial Ventures’ Symbolic Differentiation.pdf"
text_path: "library/AMJ/vol-68-no-3/text/Taeuscher 2024 It Is Not the Whole Story Toward a Broader Understanding of Entrepreneurial Ventures’ Symbolic Differentiation.txt"
ingested_at: "2026-04-30"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-4-8"
augmented_at: "2026-07-11"

paper_type: "empirical-quantitative"
keywords: ["entrepreneurial narratives", "narrative distinctiveness", "symbolic differentiation", "patents", "quality signals", "industry hotness", "cultural entrepreneurship"]
theory: ["cultural entrepreneurship theory", "signaling theory", "optimal distinctiveness"]
topics: ["entrepreneurship", "new-venture-creation", "competitive-strategy"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "social"
methods: "Multilevel random coefficient (hierarchical linear) modeling with random industry intercepts; topic modeling via latent Dirichlet allocation to construct narrative distinctiveness; coarsened exact matching as robustness check."
sample:
  industry: "All UK industries with venture activity (415 industries identified by five-digit SIC codes)"
  country: "United Kingdom"
  time_period: "Ventures incorporated between January 1, 2010 and December 31, 2021"
  units: "Entrepreneurial ventures (UK-headquartered private companies identified as 'ambitious' by Beauhurst)"
  n: "31,270 ventures"

evidence:
  sample_n: "we arrived at a regression sample of 31,270 ventures"
  sample_country: "31,270 UK-based ventures launched between 2010 and 2021"
  sample_industry: "select a primary five-digit SIC code"
  sample_time_period: "the United Kingdom between 2010 and 2021"
  theories_overview: "Building on cultural entrepreneurship theory"
  methods_overview: "use random coefficient modeling"
  keywords_source: "patent stocks and narrative distinctiveness"
  hypotheses_source: "Hypothesis 1a. In cold industries, there is a positive"
  measures_overview: "narrative distinctiveness as the sum of absolute"
  findings_overview: "substantially lower levels of narrative distinctiveness when situated in hot industries"
---

# It Is Not the Whole Story: Toward a Broader Understanding of Entrepreneurial Ventures’ Symbolic Differentiation

**Abstract**
Entrepreneurial ventures strategically communicate information about themselves to convey their distinctiveness and attract favorable audience attention. This study explores how the possession of quality-signaling resources, such as patents, influences the degree to which entrepreneurial ventures convey distinctiveness in their entrepreneurial narratives. Cultural entrepreneurship research spotlights such resources as the ingredients around which entrepreneurs construct distinctive narratives and proposes that resource-rich ventures will present themselves as particularly distinctive. Challenging this, we argue that ventures rich in quality-signaling resources—while ideally positioned to convey their distinctiveness—will likely forgo this symbolic differentiation opportunity under certain industry conditions due to a lack of external incentives. Our analysis of 31,270 UK-based ventures launched between 2010 and 2021 finds that, compared to patent-poor ventures, patent-rich ventures exhibit higher levels of narrative distinctiveness when situated in industries that receive little attention, but substantially lower levels of narrative distinctiveness when situated in hot industries that attract a lot of attention. In doing so, our study challenges the assumption that entrepreneurial ventures always aim to present themselves as distinctive as legitimately possible, delineates conditions under which this assumption is likely violated, and lays the groundwork for a broader research agenda on organizations’ substantive and symbolic differentiation.

**Research Question**
How does the possession of quality-signaling resources (specifically patents) shape the degree to which entrepreneurial ventures convey distinctiveness in their entrepreneurial narratives, and under what industry conditions do resource-rich ventures forgo opportunities for symbolic differentiation?

**Hypotheses / Propositions**
H1a. In cold industries, there is a positive relationship between entrepreneurial ventures' patent stocks and narrative distinctiveness (ventures with greater patent stocks convey higher distinctiveness).
H1b. In hot industries, there is a negative relationship between entrepreneurial ventures' patent stocks and narrative distinctiveness (ventures with greater patent stocks convey lower distinctiveness). Jointly, H1a and H1b predict that industry hotness negatively moderates the patent-stock/narrative-distinctiveness relationship.
H2a. In cold industries, the positive patent-stock/distinctiveness relationship is augmented (more positive) for patent stocks with a broader impact.
H2b. In hot industries, the negative patent-stock/distinctiveness relationship is augmented (more negative) for patent stocks with a broader impact.
H3. The patent-stock/narrative-distinctiveness relationship is contingent on industries' patent intensity, such that greater patent intensity attenuates (makes less negative) the negative relationship in hot industries.

**Mechanism Process**
- IV(s): Patent stock (log-transformed count of venture's patents); Patent breadth of impact (inverse Herfindahl of forward citation diversity)
- DV(s): Narrative distinctiveness (sum of absolute distances between venture's topic vector and prototypical industry narrative vector, derived via 60-topic LDA model)
- Moderators: Industry hotness (log of equity funding raised by UK ventures in the industry, 2017–2021); Industry patent intensity (log of total live patents across all UK companies in the industry)
- Mediators: Not directly tested (proposed mechanism is variation in entrepreneurs' external incentives for symbolic differentiation)

The central mechanism is that ventures rich in quality-signaling resources possess strong "narrative ingredients" but their motivation to deploy them depends on external incentives. In cold industries, ventures face high pressure to stand out, so patent-rich ventures leverage their resources to craft distinctive narratives. In hot industries, patent-rich ventures already attract favorable attention via their quality signals and—constrained by bounded rationality—lack incentives to invest in symbolic differentiation, sometimes deliberately emphasizing nondistinctive elements to position themselves as legitimate industry members. The moderation strengthens when patents have broad impact (more valuable signals) and when patents are rare in the industry (more discriminating signals).

**Data & Measures**
Data sources: ventures, their self-described entrepreneurial narratives, and industry-level equity-funding rounds come from Beauhurst (a tracker of UK "ambitious" companies); patent data come from Bureau van Dijk's Orbis IP database; five-digit SIC industry classification, employee counts, and industry density come from Companies House.
- Narrative distinctiveness (DV): sum of absolute distances between a venture's 60-topic latent Dirichlet allocation (LDA) narrative vector and its industry's mean (prototypical) topic vector, multiplied by 100.
- Patent stock (IV): natural logarithm (after adding 1) of the venture's number of patents; mean-centered.
- Industry hotness (moderator): natural logarithm (after adding 1) of total equity funding (pounds sterling) raised by UK ventures in the industry over 2017–2021.
- Patent breadth of impact: inverse Herfindahl index of the technology classes among the forward citations to a venture's patents; mean-centered.
- Industry patent intensity: natural logarithm (after adding 1) of total live patents held by all UK companies in the industry; mean-centered.
- Controls: venture age, venture size, accelerator, spinout, B2B, development stage, reputable VC, fundraising amount, crowdfunding, number of founders, founder-is-CEO, founder gender, narrative length, and industry density.

Estimation uses random coefficient (hierarchical linear) modeling with random industry intercepts, fit by maximum likelihood (Stata's mixed, mle command). The design is associational; coarsened exact matching is added as a robustness check to address unobservable differences between patenting and non-patenting ventures, but the authors state they cannot directly test the proposed motivational mechanism.

**Key Findings**
- H1a and H1b supported: the patent stock × industry hotness interaction is negative (b = -0.53, p < .001; Model 2). Simple-slope tests show patent stock is positively related to narrative distinctiveness in cold industries (-1 SD hotness: b = +1.47, p < .001) and negatively related in hot industries (+1 SD hotness: b = -1.14, p < .001); the relationship flips from positive to negative at about 0.13 SD above mean hotness. The paper reports "strong evidence in support of Hypotheses 1a and 1b."
- H2a and H2b supported: the moderating effect of industry hotness is nearly six times larger for patent breadth of impact than for raw patent stock, so the breadth-of-impact effect is significantly more positive in cold industries and more negative in hot industries.
- H3 supported in the main model: a positive three-way patent stock × industry hotness × patent intensity interaction (b = 0.25, p < .01; Model 4) indicates that higher industry patent intensity attenuates (makes less negative) the hot-industry moderation. Support for H3 is weaker outside the main model: coarsened-exact-matching models support Hypotheses 1a, 1b, 2a, and 2b, but the generalized-linear model (industry-clustered standard errors) and the smallest subsample models (Additional Materials Tables D3 and D4) return p-values above conventional thresholds, so the authors describe only "some" or "more limited" support for H3, whereas H1a, H1b, H2a, and H2b replicate consistently.

**Theoretical Contribution**
The study challenges cultural entrepreneurship theory's prevailing assumption that ventures always aim to present themselves as distinctive as legitimately possible, showing that resource-rich ventures may strategically forgo symbolic differentiation when external incentives are absent. It extends Lounsbury and Glynn's seminal model by introducing entrepreneurs' varying incentives for symbolic differentiation as a mechanism explaining heterogeneity in narrative distinctiveness, and contributes to organizational distinctiveness research by jointly considering firm-level (quality-signaling resources) and industry-level (industry hotness) factors.

**Practical Implication**
Entrepreneurs should recognize that whether to emphasize distinctiveness in venture narratives is contingent on industry conditions—in cold (low-attention) industries, emphasizing distinctiveness around resources like patents is beneficial, but in hot (high-attention) industries with rare patents, the symbolic emphasis matters less because the underlying quality signal already attracts attention. Resource providers evaluating ventures in hot industries should attend to substantive quality signals rather than narrative claims of distinctiveness alone.

**Limitations**
The authors only have access to ventures' narratives at one point in time, preventing analysis of how narratives evolve as patent stocks build up. They cannot directly test the proposed motivational mechanism because their data do not capture how individual entrepreneurs perceive their environment. Their models explain only a moderate share of variance (R² ≈ .26) in narrative distinctiveness, suggesting other unobserved factors shape narrative content.

**Future Research**
Future research could track narrative changes longitudinally as ventures accumulate patents, contextualize arguments to audience-specific differentiation by analyzing private documents like pitch decks, and explore how other quality-signaling resources (e.g., strategic alliances, founder experience) influence narrative distinctiveness. Microlevel process studies could also illuminate the cognitive and motivational processes underlying entrepreneurs' storytelling and symbolic differentiation efforts.

**APA 7th Citation**
Taeuscher, K., & Lounsbury, M. D. (2025). It is not the whole story: Toward a broader understanding of entrepreneurial ventures’ symbolic differentiation. *Academy of Management Journal*, 68(3), 648–668. https://doi.org/10.5465/amj.2023.0581
