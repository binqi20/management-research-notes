---
id: amj-vol-69-no-3-cillo-2026
title: "Grow Old with Me: The Temporal Dynamics of Founder–Market Interactions in Capturing Market Attention"
authors:
  - "Cillo, P."
  - "Rubera, G."
year: 2026
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2023.0974"
volume: 69
issue: 3
pages: "455-477"
source: "AMJ/vol-69-no-3"
pdf_path: "library/AMJ/vol-69-no-3/pdfs/Cillo 2025 Grow Old with Me The Temporal Dynamics of Founder–Market Interactions in Capturing Market Attention.pdf"
text_path: "library/AMJ/vol-69-no-3/text/Cillo 2025 Grow Old with Me The Temporal Dynamics of Founder–Market Interactions in Capturing Market Attention.txt"
ingested_at: "2026-10-14"
extraction_model: "gpt-6-astra"
extraction_version: "v3"
paper_type: "empirical-quantitative"
keywords: ["entrepreneurial action", "market attention", "conceptual artifacts", "material artifacts", "founders leading the market discussion", "founders following the market discussion"]
theory: ["entrepreneurial action literature", "design view of entrepreneurship"]
topics: ["entrepreneurship", "marketing-strategy", "longitudinal"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Longitudinal observational study combining market-specific latent Dirichlet allocation, startup-specific vector autoregressive models and cumulative impulse response functions, and individual growth curve analysis with random intercepts and time slopes; Heckman two-stage correction for selection into the Twitter sample."
sample:
  industry: "Multiple industries, including business services, financial, manufacturing, and high-tech"
  country: "United States"
  time_period: "Startups founded in 2014–2015; founder and market tweets collected from one year before founding through 28 quarters afterward"
  units: "Startup-quarter observations, with repeated observations nested within startups"
  n: "1,529 startups and 25,655 startup-quarter observations in the main models; initial selection frame of 8,174 startups"
evidence:
  sample_n: "Number of startups                          1,529         1,529"
  sample_country: "U.S. startups founded in 2014 and 2015."
  sample_industry: "control for industry differences (business services,"
  sample_time_period: "one year before the startup founding up to 28 quarters"
  theories_overview: "entrepreneurial action literature and the design view of entrepreneurship"
  methods_overview: "growth curve analyses using a Stata xtmixed"
  keywords_source: "market attention"
  hypotheses_source: "Hypothesis 1a. There is a positive relationship between"
  measures_overview: "traffic to the startup’s website each quarter"
  findings_overview: "but this relationship weakens over time"
---

# Grow Old with Me: The Temporal Dynamics of Founder–Market Interactions in Capturing Market Attention

**Abstract**
How do founders attract and sustain market attention over time? While prior research often portrays founders as market-shaping agents, it has overlooked the reciprocal nature of founder–market interactions and how their effects evolve. Drawing on the entrepreneurial action literature and the design view of entrepreneurship, we develop a longitudinal framework that highlights the role of entrepreneurial artifacts—conceptual and material—in capturing market attention. We identify three theoretically relevant pathways to market attention: (1) founders leading the market discussion, (2) founders following the market discussion (both forms of conceptual artifacts), and (3) introducing new products (a material artifact). We argue that the effectiveness of each pathway changes over time. Using a sample of 1,529 U.S. startups founded in 2014–2015 and a novel combination of social media data, text analytics (LDA), and time-series methods (VAR), we find that leading the market discussion is most effective early on, while following becomes more beneficial as time progresses. New product introductions show a delayed but increasingly positive effect. Our study contributes to entrepreneurship research by offering a longitudinal view of how founders can attract and grow market attention through different artifacts, addressing calls for studies on founder–market interaction over time.

**Research Question**
How do founders attract and sustain market attention through leading market discussion, following market discussion, and introducing new products, and how do these relationships change as startups mature?

**Hypotheses / Propositions**
- H1a: Founders leading the market discussion more is positively associated with startup market attention at inception.
- H1b: The relationship between leading market discussion and market attention weakens over time, such that startups whose founders lead more eventually receive less attention than those whose founders lead less.
- H2a: Founders following the market discussion more is negatively associated with startup market attention at inception.
- H2b: The relationship between following market discussion and market attention becomes positive over time, such that startups whose founders follow more receive more attention than those whose founders follow less.
- H3a: Introducing more new products is positively associated with startup market attention at inception.
- H3b: The relationship between introducing new products and market attention strengthens over time, such that startups introducing more products receive more attention than those introducing fewer.

**Mechanism Process**
- IVs: Founders leading the market discussion; founders following the market discussion; introducing new products.
- DV: Startup market attention.
- Mediators: Not reported in paper.
- Moderator: Time since founding, measured in quarters.

Leading and following are conceptual artifacts: respectively, market discussion changes in response to founder discussion, or founder discussion changes in response to market discussion. Leading initially helps a startup stand out and become a cognitive referent, but later attempts to redirect discussion may conflict with established perceptions; following initially offers limited differentiation but later helps founders align with evolving market preferences. New products are material artifacts that communicate the startup’s offering and facilitate learning, refinement, and continued market engagement. These are the proposed explanations for the temporal relationships, rather than separately tested mediating pathways.

**Data & Measures**
The initial Crunchbase frame comprises 8,174 U.S. startups founded in 2014–2015 with founder names and founding dates. Requiring at least one founder to have a Twitter account at founding yields 1,529 startups, or 18.7% of the frame; Table 2 reports 25,655 startup-quarter observations. Founder and market tweets cover one year before founding through 28 quarters afterward. To identify each startup’s potential market, an author and research assistant select 10 exemplar accounts related to its offering; the market comprises users following at least four of these accounts.

Market-specific latent Dirichlet allocation models produce quarterly topic proportions for founders and their markets. The authors transform these proportions to log odds and estimate startup-specific vector autoregressive models with two lags, including topics as exogenous variables and using data available through each focal quarter. Leading is the cumulative change in market discussion following a permanent 10-percentage-point increase in founder discussion five quarters earlier; following reverses the direction, measuring the cumulative change in founder discussion after the corresponding increase in market discussion. New product introductions are counted from Crunchbase news titles and excerpts, including refinements to existing products and counting multiple articles about the same product once. Market attention is logged quarterly organic website traffic from Semrush, representing visits through unpaid search results.

Individual growth curve models estimated with Stata xtmixed use repeated observations nested within startups, random intercepts and time slopes, grand-mean-centered variables, and the founding quarter coded as zero. The focal predictors interact with time, so their simple coefficients concern initial attention. Controls include organic and paid keyword search volumes, founder tweet counts, startup Twitter mentions and their sentiment, offering creativity, founding-team size and sex composition, founders’ entrepreneurial industry experience and education, market attractiveness, competitor counts, and industry and founding-state fixed effects. A first-stage probit estimates Twitter-account selection using founding-city tweets in the three months before founding divided by city population as the exclusion variable, alongside founder characteristics and founding month-year and industry effects; its inverse Mills ratio enters the growth model. The study estimates longitudinal associations rather than randomized treatment effects.

**Key Findings**
- Table 2, Model 2 supports H1a: leading is positively associated with initial attention (b = 2.971, p < .001). Its interaction with time is negative (b = −0.140, p < .001), which the authors interpret as supporting H1b. Their Johnson–Neyman analysis reports a positive association for the first 14 quarters and no significant association afterward; the hypothesized later disadvantage is therefore not demonstrated as a significant negative association.
- H2a and H2b receive support: following is negatively associated with initial attention (b = −7.393, p < .001), with a positive time interaction (b = 0.879, p < .001). The association is negative for the first five quarters, nonsignificant through quarter 11, and positive from quarter 12 onward.
- H3a is not supported: introducing new products has no significant initial association (b = −0.106, p > .05). The positive time interaction supports H3b (b = 0.020, p < .001); the authors report a positive association only after 10 quarters.
- The authors report similar results with organic plus paid traffic, an unstructured covariance matrix, omission of the inverse Mills ratio, and alternative exemplar accounts for 350 randomly selected startups. Alternative cumulative impulse-response horizons qualify robustness: the following coefficient is only “partially significant” at four quarters and is also an exception to significance at six quarters. Appendix C’s model without time interactions estimates average associations over time, not effects at inception: leading is positive (b = 1.958, p < .001), following is nonsignificant (b = −0.062), and new products are positive (b = 0.166, p < .001).

**Theoretical Contribution**
The paper integrates entrepreneurial action and the design view of entrepreneurship into a longitudinal account of how conceptual and material artifacts help founders capture market attention. It identifies temporal boundary conditions for market influence, emphasizing a shift from leading conversations toward listening and adaptation as startups mature. The framework advances a contingent, reciprocal account of opportunity actualization rather than locating success entirely in founder characteristics or conditions at founding.

**Practical Implication**
The authors suggest that founders use exemplar accounts to identify potential customers, then read their followers’ posts or engage them in conversation to understand market interests. Founders should recognize the changing usefulness of communication strategies: lead with novel ideas early, then listen and respond to evolving preferences, while continuing to introduce products whose attention benefits may emerge later.

**Limitations**
The analysis concentrates on consumers and separates leading from following, although founders may pursue both simultaneously; it examines their consequences rather than antecedents. It does not capture other paid advertising, such as social media advertisements, or third-party influences such as endorsers and investors. Broad thematic shifts do not capture individual conversations, and market-specific topic models prevent systematic comparisons of content-specific shifts across startups.

**Future Research**
The authors propose examining industry conditions, including the ephemerality of consumer preferences, that affect when the relationships emerge, and extending the framework to suppliers and investors. They also propose studying hybrid or sequential combinations of leading and following and whether antecedents such as empathy, perspective-taking, or lucky projection produce different outcomes. Further work could examine conversation-level dynamics, including strategic silence and attention diversion, or focus on a single industry to investigate how communication around specific topics relates to attention over time.

**APA 7th Citation**
Cillo, P., & Rubera, G. (2026). Grow old with me: The temporal dynamics of founder–market interactions in capturing market attention. *Academy of Management Journal, 69*(3), 455–477. https://doi.org/10.5465/amj.2023.0974
