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
extraction_model: "claude-opus-4-6"
extraction_version: "v2"

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
---

# “Distinctive from What? And for Whom?” Deep Learning-Based Product Distinctiveness, Social Structure, and Third-Party Certifications

**Abstract**
How do producers’ distinctiveness and social structure influence third-party certifications? We argue that producers compete against prior and current competitors, and against their past selves. In the context of 153 artists active during a key period of the emergence of modern art (1905–1916), we utilize a convolutional neural network used in computer vision to extract feature vectors of artworks, and measure quantitative distance of these artists’ works from canonical reference points. We find that artists are rewarded for distinctiveness from prior and current competitors and their past selves (up to a point). However, artists’ autonomy to differentiate themselves depends on their position in the social structure, which we divide into supply-side artist-to-artist networks, and demand-side artist-to-gallerist networks. Artists with high or low supply-side status receive higher rewards for distinctiveness from current competitors than do artists with middle supply-side status. Artists with higher demand-side status receive higher rewards for distinctiveness from their own past, but lower rewards for distinctiveness from current competitors. These results show that peers strive to constrain each other to conform to positions of gravity within product space, and that market audiences deploy either higher or lower constraints on a producer’s identity depending on the reference point.

**Research Question**
How do a producer's distinctiveness and its position in social structure jointly shape the third-party certifications it receives? The paper centers on two questions: distinctive compared to what reference point (prior competitors, current competitors, or one's own past), and for whom — i.e., how supply-side (peer) and demand-side (audience) status moderate the rewards to distinctiveness.

**Mechanism Process**
- IV(s): Distinctiveness from prior competitors (19th-century art); distinctiveness from current competitors (peers); distinctiveness from past self — each a cosine distance between CNN-derived feature vectors.
- DV(s): Third-party certifications, operationalized as count of exhibition opportunities and count of unique exhibition cities per artist-year.
- Mediators: None modeled.
- Moderators: Supply-side peer-network status (eigenvector centrality in the coexhibition peer network); demand-side market status (status of exhibition venues).

The paper theorizes that distinctiveness from each reference point is rewarded by certifiers up to a point, but a producer's autonomy to differentiate is constrained by two "pulls" of social structure. Supply-side peer pressure to conform is non-monotonic: high- and low-status artists are rewarded for distinctiveness from current competitors, while middle-status artists are penalized (a U-shaped pattern). Demand-side market status licenses distinctiveness from one's own past yet penalizes distinctiveness from current competitors, because high-status producers risk alienating the peers and audiences on whom their legitimacy depends.

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
