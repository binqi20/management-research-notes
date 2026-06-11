---
id: nbs-2025-12-guidolin-2026
title: "The pricing of biodiversity risk in commodity markets"
authors:
  - "Guidolin, Massimo"
  - "Pedio, Manuela"
year: 2026
journal: "Review of Finance"
doi: "https://doi.org/10.1093/rof/rfaf068"
volume: 30
issue: 1
pages: "351-389"

source: "NBS/2025-12"
pdf_path: "library/NBS/2025-12/pdfs/Guidolin 2026 The pricing of biodiversity risk in commodity markets.pdf"
text_path: "library/NBS/2025-12/text/Guidolin 2026 The pricing of biodiversity risk in commodity markets.txt"
ingested_at: "2026-06-09"
extraction_model: "claude-opus-4-8"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["biodiversity risk", "transition risk", "commodity returns", "biodiversity premium"]
theory: ["commodity production / convenience-yield model (Gorton, Hayashi & Rouwenhorst, 2012; Yang, 2013)", "characteristic-based asset pricing (Bolton & Kacperczyk, 2021, 2023; Brennan, Chordia & Subrahmanyam, 1998)", "transition risk vs. physical risk framework"]
topics: ["biodiversity", "sustainable-finance", "asset-pricing"]
unit_of_analysis: "market"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Characteristic-based asset pricing on a panel of internationally traded commodities; panel regressions of monthly spot/futures excess returns on the intensity of species loss with month-year and commodity fixed effects, standard errors double-clustered at month-year and commodity level; risk-adjusted returns from a seven-factor commodity model; an event study around the Kunming Declaration (with a Paris Agreement placebo); and beta-sorted tercile portfolios on exposure to an aggregate biodiversity loss index (PC of LPI and RLI)."
sample:
  industry: "Globally traded agricultural commodities (baseline 23 spot, 10 futures, e.g., cocoa, coffee, palm oil, sugar), expanded to 56 commodities including non-agricultural in the aggregate analysis"
  country: "Global (worldwide-aggregated commodity production and prices)"
  time_period: "2005-2022 (main analysis)"
  units: "Commodity-month observations"
  n: "23 agricultural commodities (spot) and 10 (futures) in baseline; 56 commodities in the aggregate-shock analysis"

evidence:
  sample_n: "twentythree commodity spot price series available from the IMF and with ten futures price series"
  sample_country: "we simply aggregate across different countries."
  sample_industry: "we leverage the availability of biodiversity footprint data for a broad set of agricultural commodities"
  sample_time_period: "our main analysis spans from 2005 to 2022, which is the sample"
  theories_overview: "the commodity production model presented in Section 5, which extends Gorton Hayashi and Rouwenhorst (2012) and Yang (2013)"
  methods_overview: "we employ a characteristic-based asset pricing framework to test whether biodiversity-related transition"
  keywords_source: "Keywords: biodiversity risk; transition risk; commodity returns; biodiversity premium."
---

# The pricing of biodiversity risk in commodity markets

**Abstract**
This article provides empirical evidence that biodiversity-related transition risk is priced in global commodity markets, with particular emphasis on agricultural commodities. Using intensity-based metrics of species loss per harvested land unit, we obtain empirical evidence that commodities with higher biodiversity footprints earn significant risk premia, after controlling for commodity-specific factors. An event study around the Kunming Declaration further shows that commodities associated with greater biodiversity risk experienced negative abnormal returns following the declaration. In an aggregate-level analysis, we additionally find that commodities with higher sensitivity (beta) to biodiversity shocks earn significantly higher excess returns, reinforcing the presence of a biodiversity­related risk premium across global commodity markets. Our findings suggest that investors are increasingly internalizing the biodiversity-related risks at the commodity-asset level. The findings can be rationalized by a commodity production model, which we outline in Section 5.

**Research Question**
The paper examines whether commodities with higher biodiversity footprints — reflected in species loss intensity and land-use impact — earn systematically different returns, consistent with investors pricing in the financial implications of nature-related regulatory and societal responses (i.e., biodiversity transition risk).

**Mechanism Process**
- IV(s): Intensity of species loss (predicted species committed to extinction per 10,000 km² of harvested land, lagged); for the event study, a Post × HighIntensitySpeciesLoss interaction around the Kunming Declaration; for the aggregate analysis, commodity beta to an aggregate biodiversity loss index (BLI, first PC of LPI and RLI).
- DV(s): Monthly commodity excess returns (spot and futures), raw and risk-adjusted; tercile-portfolio excess returns and seven-factor alphas.
- Mediators: None modeled (the convenience-yield channel is theorized, not estimated).
- Moderators: Sub-period (pre- vs. post-2015); financialization (GSCI membership); spot vs. futures market.

Higher biodiversity-footprint commodities face elevated transition risk because regulatory shifts, import bans, due-diligence rules, and changing investor/consumer preferences can penalize biodiversity-harming production; rational investors therefore demand a risk premium, so prices are bid down on adverse news to allow higher subsequent expected returns. The baseline panel finds a premium of roughly 20-60 basis points per month per ten additional species lost per 10,000 km², concentrated after 2015 and robust to emissions and deforestation controls. The Kunming-Declaration event study and the BLI beta-sorted long-short portfolio (annualized alpha ~5.4%) corroborate that this transition-risk premium operates at both the individual-commodity and aggregate-market levels; a Section 5 production model shows why the premium appears in spot but is washed out of futures returns via a risk-driven convenience-yield adjustment.

**Theoretical Contribution**
The paper extends the emerging literature on the financial materiality of biodiversity loss from equities to commodity markets, a domain where nature-related risks are immediate, physical, and directly measurable, and shows that investors price biodiversity transition risk at the asset level even absent firm-level disclosure. It develops a commodity production model (extending Gorton, Hayashi & Rouwenhorst, 2012 and Yang, 2013) in which expected spot returns decompose into a basis premium, a storage-cost volatility premium, and a biodiversity-intensity premium, and explains why the biodiversity premium does not survive in futures returns.

**Practical Implication**
The findings imply that investors can use commodities' intensity-of-species-loss footprints to anticipate biodiversity-related repricing, and that a high-beta-minus-low-beta commodity portfolio can hedge short-run aggregate biodiversity shocks. For policymakers, intensity-based species-loss metrics (rather than raw deforestation or emissions) better identify the commodities most exposed to the regulatory measures that constitute transition risk.

**Limitations**
The intensity-of-species-loss measure, being the output of a cSAR land-use model, captures habitat degradation from anthropogenic land use but not the effects of chemicals, invasive species, water consumption, habitat fragmentation, or species endemism, and is subject to measurement error (attenuation bias). The futures-market null result rests on a small sample of futures with correspondingly low test power, and the Commodity Footprints data cover only agricultural commodities.

**Future Research**
Future work could extend the analysis to non-agricultural commodities (metals, fossil fuels) as broader biodiversity data become available; enrich the footprint measure with multi-dimensional biodiversity data capturing taxonomic, functional, and geographic variation; and test whether markets differentiate among sub-components of biodiversity loss (species abundance, genetic diversity, ecosystem degradation) using emerging sources and taxonomies such as ENCORE, the IUCN Red List, and NatureDep.

**APA 7th Citation**
Guidolin, M., & Pedio, M. (2026). The pricing of biodiversity risk in commodity markets. *Review of Finance*, 30(1), 351-389. https://doi.org/10.1093/rof/rfaf068
