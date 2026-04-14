---
id: nbs-2026-02-stefania-d-amico-2026
title: "The benchmark greenium"
authors:
  - "D’Amico, S."
  - "Klausmann, J."
  - "Pancost, N. A."
year: 2026
journal: "Journal of Financial Economics"
doi: "https://doi.org/10.1016/j.jfineco.2025.104217"
volume: 176
issue: null
pages: "104217"

source: "NBS/2026-02"
pdf_path: "library/NBS/2026-02/pdfs/Stefania D’Amico 2026 The benchmark greenium.pdf"
text_path: "library/NBS/2026-02/text/Stefania D’Amico 2026 The benchmark greenium.txt"
ingested_at: "2026-04-14"
extraction_model: "claude-opus-4-6"
extraction_version: "v1"

paper_type: "empirical-quantitative"
keywords:
  - "ESG"
  - "Green bonds"
  - "Dynamic no-arbitrage models"
theory:
  - "dynamic term structure model"
  - "no-arbitrage asset pricing"
  - "convenience yield theory"
  - "taste premium / green preferences"
topics:
  - "green-bonds"
  - "sustainable-finance"
  - "responsible-investing"
  - "climate-policy"
unit_of_analysis: "market"
level_of_theory: "macro"
dependent_variable_family: "financial"
methods: "Daily security-level dynamic term-structure model (DTSM) with an additional time-varying green factor, estimated via Bayesian/MCMC techniques to jointly price German federal green and conventional ('twin') sovereign bonds and extract a time-varying benchmark greenium purged of pecuniary and non-pecuniary non-environmental factors; complemented by regression analyses linking the estimated greenium to proxies of environmental concerns."
sample:
  industry: "Sovereign fixed-income markets (government bonds)"
  country: "Germany"
  time_period: "September 2020 through the sample end (data beginning with the first German green bund issuance in September 2020)"
  units: "German federal green bonds and their conventional 'twin' counterparts, plus the broader cross-section of outstanding German federal (Bund) securities"
  n: "Not reported in paper"
---

# The benchmark greenium

**Abstract**
While the green spread correlates with stock market prices, the conventional convenience yield, and temporary demand-supply imbalances, our greenium correlates only with proxies of environmental concerns.

**Research Question**
Is there a "taste" premium for green assets (a greenium) that stems solely from investors' environmental values rather than their cash-flow expectations, and if so, how large is it, how has it evolved over time, and how does it vary across investment horizons?

**Mechanism Process**
- IV(s): Investors' environmental preferences/climate concerns; relative supply and demand of green vs. conventional bonds; conventional convenience yield; broad market risk; bond maturity/horizon
- DV(s): Benchmark greenium (frictionless taste premium on risk-free green bonds); green spread; expected green returns
- Mediators: Latent common factors pricing German federal bonds plus a dedicated time-varying green factor in the DTSM
- Moderators: Horizon/term structure of the greenium; episodes of safe-haven flows and demand-supply imbalances affecting conventional twins

The authors extend a no-arbitrage dynamic term structure model to jointly price German federal green and conventional bonds by adding a green factor that affects only green securities. Because twin green and conventional Bunds have identical cash flows and default risk, any systematic yield differential must reflect non-cash-flow factors; the model decomposes these into pecuniary and non-pecuniary components and isolates the part driven solely by environmental concerns. The resulting benchmark greenium behaves as a convenience yield on green assets that varies with climate attitudes and perceived climate risk, generating a term structure of expected green returns that incorporates greenium risk and that can invert when short-horizon environmental concerns intensify relative to long-horizon ones.

**Theoretical Contribution**
The paper introduces a benchmark greenium — a frictionless, time-varying taste premium on risk-free green assets — and shows that the observable green spread is a noisy and potentially misleading proxy for it because it bundles the greenium with the conventional convenience yield, broad market risk, and temporary demand-supply imbalances. By embedding a dedicated green factor inside a dynamic no-arbitrage term structure model, the authors deliver the first horizon-dependent, time-varying estimate of the taste premium for green assets and of its associated risk premium, extending convenience-yield theory (Krishnamurthy and Vissing-Jorgensen; Nagel) from money-like assets to environmental assets. The framework generalizes to any convenience yield that affects one group of assets but not others and supplies a benchmark for pricing riskier green securities.

**Practical Implication**
Because the greenium is substantial, highly time-varying, and usually largest at shorter horizons (with an inverted term structure by early 2023), governments can capture a larger subsidy from climate-motivated investors by issuing shorter-term green bonds, passing the savings to taxpayers. The risk-free benchmark greenium also provides a reference price for riskier green assets, facilitating corporate green bond issuance and stimulating private funding for the green transition. Investors and portfolio managers should interpret green spreads cautiously, since they conflate environmental preferences with conventional convenience yields and market-risk shocks.

**Limitations**
The analysis is confined to the German sovereign 'twin' bond market, which offers an unusually clean setting but limits generalizability to other issuers, currencies, and credit-risky green bonds. The greenium is identified through a parametric DTSM whose assumptions about latent factor dynamics and the green factor specification may influence its estimated level and term structure.

**Future Research**
The framework could be applied to other convenience yields affecting distinct asset groups, and to riskier green securities (corporate green bonds, green sovereigns with default risk) once a benchmark greenium is available as a reference. Future work could also link time variation in the greenium more tightly to measurable climate policy shocks, investor flows, and climate-risk news, and extend the model to additional sovereign twin markets as more green bonds are issued.

**APA 7th Citation**
D’Amico, S., Klausmann, J., & Pancost, N. A. (2026). The benchmark greenium. *Journal of Financial Economics*, 176, 104217. https://doi.org/10.1016/j.jfineco.2025.104217
