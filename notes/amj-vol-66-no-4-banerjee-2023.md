---
id: amj-vol-66-no-4-banerjee-2023
title: "“Distinctive from What? And for Whom?” Deep Learning-Based Product Distinctiveness, Social Structure, and Third-Party Certifications"
authors:
  - "Banerjee, Mitali"
  - "Cole, Benjamin M."
  - "Ingram, Paul"
year: 2023
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2021.0175"
volume: 66
issue: 4
pages: "1016-1041"

source: "AMJ/vol-66-no-4"
pdf_path: "library/AMJ/vol-66-no-4/pdfs/Banerjee 2023 “Distinctive from What And for Whom” Deep Learning-Based Product Distinctiveness, Social Structure, and Third-Party Certifications.pdf"
text_path: "library/AMJ/vol-66-no-4/text/Banerjee 2023 “Distinctive from What And for Whom” Deep Learning-Based Product Distinctiveness, Social Structure, and Third-Party Certifications.txt"
ingested_at: "2026-05-20"
extraction_model: "claude-opus-4-7"
extraction_version: "v3"
augmented_model: "claude-opus-5"
augmented_at: "2026-07-28"

paper_type: "empirical-quantitative"
keywords: ["product distinctiveness", "third-party certifications", "social structure", "optimal distinctiveness", "supply-side and demand-side status", "deep learning", "reference points"]
theory: ["optimal distinctiveness theory (Deephouse, 1999; Zhao et al., 2017)", "social structure / status theory (Zuckerman, 2017; Podolny, 1993)", "reference-point and categorization perspectives (Bourdieu, 1983; Cattani et al., 2014)"]
topics: ["strategy-innovation", "social-capital-theory", "historical"]
unit_of_analysis: "individual"
level_of_theory: "meso"
dependent_variable_family: "social"
methods: "Longitudinal panel of artist-years; convolutional neural network (CaffeNet/AlexNet) extracts 4,096-dimensional feature vectors of artworks, with cosine distance to three reference points (prior competitors, current competitors, past self); negative binomial regression (NBREG, Stata MP 15.1) with robust standard errors, artist and year fixed effects, one-year lags, and supply-/demand-side status moderators."
sample:
  industry: "Fine art (modern-art painting and drawing); third-party certification via galleries and salons"
  country: "Europe (works/exhibitions catalogued in the Database of Modern Exhibitions)"
  time_period: "1905–1916"
  units: "Artists (artist-year observations); 12,193 artworks analyzed"
  n: "153 artists"

# Mandatory evidence anchors (v2 — Layer 1 faithfulness audit).
evidence:
  sample_n: "This yielded a final sample of 153 artists."
  sample_country: "coexhibitions in Europe"
  sample_industry: "context of the art industry"
  sample_time_period: "European artists between 1905 and 1916"
  theories_overview: "two distinct pulls of social structure"
  methods_overview: "model (NBREG in Stata version MP 15.1) with robust"
  keywords_source: "supply-side artist-to-artist networks"
  hypotheses_source: "an inverted U-shaped relationship to their distinctiveness from their past self."
  measures_overview: "a count of the number of exhibition opportunities"
  findings_overview: "We find support for Hypothesis 1 (p , .001) and"
---

# “Distinctive from What? And for Whom?” Deep Learning-Based Product Distinctiveness, Social Structure, and Third-Party Certifications

**Abstract**
How do producers’ distinctiveness and social structure influence third-party certifications? We argue that producers compete against prior and current competitors, and against their past selves. In the context of 153 artists active during a key period of the emergence of modern art (1905–1916), we utilize a convolutional neural network used in computer vision to extract feature vectors of artworks, and measure quantitative distance of these artists’ works from canonical reference points. We find that artists are rewarded for distinctiveness from prior and current competitors and their past selves (up to a point). However, artists’ autonomy to differentiate themselves depends on their position in the social structure, which we divide into supply-side artist-to-artist networks, and demand-side artist-to-gallerist networks. Artists with high or low supply-side status receive higher rewards for distinctiveness from current competitors than do artists with middle supply-side status. Artists with higher demand-side status receive higher rewards for distinctiveness from their own past, but lower rewards for distinctiveness from current competitors. These results show that peers strive to constrain each other to conform to positions of gravity within product space, and that market audiences deploy either higher or lower constraints on a producer’s identity depending on the reference point.

**Research Question**
How do a producer's distinctiveness and its position in social structure jointly shape the third-party certifications it receives? The paper centers on two questions: distinctive compared to what reference point (prior competitors, current competitors, or one's own past), and for whom — i.e., how supply-side (peer) and demand-side (audience) status moderate the rewards to distinctiveness.

**Hypotheses / Propositions**
- Hypothesis 1. Artists experience more exhibition opportunities if their work is distinctive when compared to prior competitors (predicted positive).
- Hypothesis 2. Artists experience more exhibition opportunities if their work is distinctive when compared to current competitors (predicted positive).
- Hypothesis 3. Artists experience fewer exhibition opportunities as a function of their distinctiveness from current competitors to the extent they are in the middle of, as opposed to low or high in, the status hierarchy derived from the peer network (predicted U-shaped moderation by supply-side peer-network status).
- Hypothesis 4. Artists experience more exhibition opportunities as a function of their distinctiveness from current competitors to the extent that they are higher in market status (predicted positive moderation by demand-side market status).
- Hypothesis 5. Artists' exhibition opportunities have an inverted U-shaped relationship to their distinctiveness from their past self.
- Hypothesis 5a. The distinctiveness from one's past self is positively moderated by an artist's market status.

**Mechanism Process**
- IV(s): Distinctiveness from prior competitors (19th-century art); distinctiveness from current competitors (peers); distinctiveness from past self — each a cosine distance between CNN-derived feature vectors.
- DV(s): Third-party certifications, operationalized as count of exhibition opportunities and count of unique exhibition cities per artist-year.
- Mediators: None modeled.
- Moderators: Supply-side peer-network status (eigenvector centrality in the coexhibition peer network); demand-side market status (status of exhibition venues).

The paper theorizes that distinctiveness from each reference point is rewarded by certifiers up to a point, but a producer's autonomy to differentiate is constrained by two "pulls" of social structure. Supply-side peer pressure to conform is non-monotonic: high- and low-status artists are rewarded for distinctiveness from current competitors, while middle-status artists are penalized (a U-shaped pattern). Demand-side market status is theorized to license distinctiveness from one's own past and, in Hypothesis 4, to reward distinctiveness from current competitors as well; the latter interaction instead emerged with "the opposite directionality than predicted," which the authors rationalize post hoc as high-status producers risking alienation of the peers and audiences on whom their legitimacy depends.

**Data & Measures**
- Sample construction: 361 modern artists born before 1900 listed in the Benezit Dictionary of Artists (2016) under a set of modern-art movements, intersected with the 13,301 artists catalogued in the Database of Modern Exhibitions (DoME) and with the Getty Research Institute's Union List of Artist Names, yielding 153 artists.
- Artwork corpus: 12,193 artworks with known creation years, hand-collected per artist from the Artstor collection and supplemented via Google image search, TinEye, and AskArt; plus a reference corpus of the first 2,000 19th-century images returned by Artstor.
- Feature extraction: CaffeNet (AlexNet architecture) convolutional neural network pretrained on 1,034,908 nonart ImageNet images; input is a 224 × 224 matrix of RGB pixels, output a 4,096-dimensional feature vector per artwork.
- DV (third-party certifications): count of exhibition opportunities afforded to each artist per year, 1905–1916, from DoME; alternative DV is the count of unique cities in which those exhibitions took place.
- IVs: distinctiveness from prior competitors = the artist-year average cosine distance of the artist's works from the 2,000 19th-century works; distinctiveness from current competitors = average cosine distance from the works created one year earlier by the artist's coexhibition alters (a moving one-year window); distinctiveness from past self = average cosine distance from the artist's own works created five to 15 years earlier. Where an artist produced no work in a given year, the most recent prior year's work is used.
- Moderators: supply-side peer-network status = eigenvector centrality in the cumulative artist-to-artist coexhibition network; demand-side market status = the artist's exhibitions in previous years weighted by each venue's eigenvector centrality in the valued venue × venue network.
- Controls: career age; peer-network brokerage (1 minus the local clustering coefficient); artist and year fixed effects.
- Estimation: negative binomial regression (NBREG, Stata MP 15.1) with robust standard errors, all independent variables lagged one year, and one-tailed tests for the hypotheses; 1,694 artist-year observations in the controls-only model and 1,683 in every model containing the distinctiveness measures.

The design is an observational longitudinal panel and the paper claims no causal-identification strategy: artist and year fixed effects are described only as controlling for historical influences and stable artist attributes, so the estimates are associational. Seven robustness checks are reported — dropping artist-years with no artwork by the artist; an alternative 19th-century corpus of 9,923 representational works from the Louvre's Departement des Peintures; peer-network ties restricted to the last three years; dropping the quadratic interaction term; degree-centrality and betweenness-centrality versions of market status; and adding a lagged DV — which the authors describe as leaving the results broadly robust.

**Key Findings**
- Main effects (Table 2, DV = exhibition count; Model 5, the fully nested main-effects model): support for Hypothesis 1 (p < .001) and for Hypothesis 2 (p < .10), so distinctiveness from prior competitors and from current competitors each predict more exhibitions. Hypothesis 5 receives only partial support in this model (p < .05 on the linear term, not significant on the squared term); the authors read Model 5 as showing a monotonic rather than inverted-U benefit of diverging from one's past self.
- Supply-side moderation (Model 6): Hypothesis 3 is supported. The interaction of distinctiveness from current competitors with peer-network status is negative (p < .10) and the interaction with peer-network status squared is positive (p < .01) — a U-shape in which middle-status artists gain the fewest exhibition opportunities from distinctiveness from peers — and the adjusted Wald test is significant (p < .01).
- Demand-side moderation of distinctiveness from current competitors (Model 7): Hypothesis 4 is not supported, since neither the interaction coefficient nor the adjusted Wald test is significant.
- Demand-side moderation of distinctiveness from past self (Model 8): the Hypothesis 5a interaction is positive and highly significant (p < .001), as is the adjusted Wald test (p < .001).
- Fully nested model with all interactions (Model 9, Table 2): Hypothesis 1 (p < .001), Hypothesis 3 (p < .10 and p < .001), Hypothesis 5 (p < .01 and p < .01) and Hypothesis 5a (p < .001) are supported, with the predicted inverted U for distinctiveness from past self emerging once market status is in the model. Hypothesis 2 falls just out of significance, so support for it depends on the model specification. Hypothesis 4 is significant in the direction opposite to that predicted (coefficient = −3.37, p < .001): higher market status lowers rather than raises the reward for distinctiveness from current competitors.
- Alternative DV (Table 3, unique exhibition cities): results overlap substantially with Table 2 in significance and directionality, with two differences in Model 9, both on the peer-status variable. The simple effect of peer-network status shows the same U-shaped curvilinear directionality but its first term loses significance, and that loss carries over to the first interaction term with distinctiveness from current competitors, whose predicted curvilinear directionality is otherwise unchanged.
- Marginal effects: for distinctiveness from prior competitors, artists at the median are predicted to have 2.05 exhibitions, versus 1.88 at the 25th percentile and 2.17 at the 75th percentile.

**Theoretical Contribution**
The study refines optimal-distinctiveness and status research by specifying which reference point matters and for whom, and by being the first (to the authors' knowledge) to empirically test Zuckerman's (2017) distinction between supply-side and demand-side conformity pressures. It also advances method and theory in aesthetic/sensorial markets by using a deep-learning measure of whole-product distinctiveness that does not rely on predefined categories, making previously unfalsifiable arguments (e.g., Bourdieu, 1983) empirically testable.

**Practical Implication**
Innovators competing for certifications should choose their referent for differentiation strategically given their status: high-market-status producers are better off differentiating from their own past work, while those without such status (e.g., new entrants) benefit more from differentiating from current competitors, and middle-status peers are better off converging closer to their contemporaries.

**Limitations**
Not reported in paper

**Future Research**
The authors note the framework and deep-learning approach can be extended beyond fine art to other visually driven industries (fashion, architecture, advertising) and, via tools for sound and text, to music, film, and publishing; distance can also be computed to any theoretically interesting reference point (e.g., a particular movement or artist), and image- and text-recognition techniques could be combined to study how distinctiveness across modalities jointly affects certification.

**APA 7th Citation**
Banerjee, M., Cole, B. M., & Ingram, P. (2023). “Distinctive from what? And for whom?” Deep learning-based product distinctiveness, social structure, and third-party certifications. *Academy of Management Journal*, 66(4), 1016–1041. https://doi.org/10.5465/amj.2021.0175
