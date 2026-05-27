---
id: amj-vol-67-no-4-wu-2023
title: "The Social Structure of Insiders and Outsiders: Toward a Network Community Perspective on Firm Performance"
authors:
  - "Wu, X."
  - "Adbi, A."
  - "Mahmood, I. P."
year: 2024
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2022.0925"
volume: 67
issue: 4
pages: "903-932"

source: "AMJ/vol-67-no-4"
pdf_path: "library/AMJ/vol-67-no-4/pdfs/Wu 2023 The Social Structure of Insiders and Outsiders Toward a Network Community Perspective on Firm Performance.pdf"
text_path: "library/AMJ/vol-67-no-4/text/Wu 2023 The Social Structure of Insiders and Outsiders Toward a Network Community Perspective on Firm Performance.txt"
ingested_at: "2026-05-06"
extraction_model: "claude-opus-4-7"
extraction_version: "v2"

paper_type: "empirical-quantitative"
keywords: ["network communities", "interorganizational relationships", "insiders and outsiders", "venture capital", "syndication networks", "institutional development", "clique percolation method"]
theory: ["network community perspective", "social network theory (connections, positions, cliques)", "institutional theory (Khanna & Palepu, 1997; North, 1990)", "structural folds (Vedres & Stark, 2010)", "structural holes (Burt, 1992)"]
topics: ["strategy-innovation", "social-capital-theory", "institutional-theory", "china"]
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "financial"
methods: "OLS regressions with firm and year fixed effects (standard errors clustered at firm level) on VC firm-year panel data; community detection via clique percolation method (CPM, k=4) over one-year and three-year trailing-window syndication networks; tests for inverted U-shape following Haans, Pieters, & He (2016); robustness via Arellano-Bond/system-GMM dynamic panels, coarsened exact matching, IPO-rate alternative DV, principal component composite of centrality measures, and outlier checks (winsorization, trimming)."
sample:
  industry: "Venture capital (VC) syndication networks; VC firms investing in 26,484 portfolio companies"
  country: "China"
  time_period: "VC investments 2003-2016; portfolio exits tracked through 2018"
  units: "VC firm-year observations (parent-firm level)"
  n: "15,767 firm-year observations from 8,245 unique domestic VC firms (10,609 firm-years from 3,087 firms in fixed-effects models)"

evidence:
  sample_n: "final data set thus contains 15,767 firm-year"
  sample_country: "longitudinal data on VC firms in China"
  sample_industry: "syndication networks in the Chinese venture"
  sample_time_period: "timespan of VC investments is from 2003 to 2016"
  theories_overview: "integrating social network and institutional perspectives"
  methods_overview: "The clique percolation method (CPM) is a recent"
  keywords_source: "network communities (membership in cohesive network structures)"
---

# The Social Structure of Insiders and Outsiders: Toward a Network Community Perspective on Firm Performance

**Abstract**
Management literature on how interorganizational relationships influence firm performance has emphasized the importance of connections, positions, and cliques. We advance this literature by examining how network communities (membership in cohesive network structures) shape the performance of venture capital (VC) firms. We propose that community insiders affiliated with at least one network community will outperform outsiders. We also explicate the conditions under which the advantages of network community affiliations are likely to be muted. Specifically, we argue for the potential diseconomies of network community affiliations and the possibility of a substitutive relationship between network communities and institutional development. Leveraging recent advances in community-detection technology and longitudinal data on VC firms in China, we find support for our theoretical arguments. Analysis of mechanisms underlying our theoretical arguments reveals that the value of community affiliations comes from indirect connections within network communities. By integrating social network and institutional perspectives, this study highlights not only the promises but also the limits of relying on network community affiliations.

**Research Question**
How do a focal firm's network community affiliations enhance firm performance, and what factors might accentuate or diminish the benefits of those affiliations? In particular, the paper asks whether community insiders outperform outsiders, whether multiple insiders face diseconomies, and how institutional development moderates these relationships.

**Mechanism Process**
- IV(s): Insider status (dummy = 1 if affiliated with at least one network community); Community affiliations (count of network communities a VC firm is affiliated with) and its squared term; Marketization index (institutional development at provincial level)
- DV(s): Exit rate (proportion of a VC's portfolio companies exiting via IPO or M&A); IPO rate as alternative
- Moderators: Marketization index (interacting with Insider, with Community affiliations, and with Community affiliations squared)
- Controls: Degree centrality, betweenness centrality, eigenvector centrality, Burt's network constraint, prior experience (cumulative invested capital), prior success (cumulative successful exits); firm and year fixed effects

The mechanism rests on the argument that network communities — overlapping clusters of densely interconnected firms detected via the clique percolation method — provide insiders with information-acquisition and resource-exchange advantages, especially through indirect connections (partners' partners) that supply third-party referrals, trust, and reciprocity. Multiple insiders enjoy familiar access to diverse resource bases but face attentional and inertial costs of maintaining many community affiliations, producing an inverted U-shape between community count and performance. Well-developed institutions substitute for community-based exchange by providing market intermediaries, dampening insider advantages and shifting the inverted-U apex to fewer affiliations. Mechanism tests reveal that the benefit comes from indirect rather than direct community ties.

**Theoretical Contribution**
The paper introduces a network community perspective on firm performance that complements existing connection, position, and clique perspectives by capturing intermediate-level cohesive structures with overlapping membership. It shows that connections and centrality alone are insufficient — being part of a community is what generates performance advantages — and that the benefits of network communities operate through indirect ties rather than direct syndication partners. By integrating social network and institutional perspectives, the study reveals a substitutive relationship between network communities and institutional development, identifying boundary conditions under which network-based advantages diminish.

**Practical Implication**
Managers should prioritize deepening connections that lead to network community affiliations rather than building superficial connections, while exercising caution about over-affiliating with multiple communities, which can cause information overload and conflicts of interest. With advances in community-detection technologies (e.g., CPM), managers can develop a broader understanding of their network landscape. Governments in less-developed institutional contexts can incentivize community outsiders to become insiders (e.g., through public sponsorship of certain industries) to foster more equitable economic growth.

**Limitations**
The study focuses on a single country (China), raising generalizability concerns, and the coinvestment partnerships in China tend to be short-lived, which may shift the relative importance of outsiders, insiders, and multiple insiders. The orientation and stability of partnerships may differ in other settings, and informal institutions are not directly modeled. Identification of network community boundaries depends on parametric choices (clique size k, trailing window n) that involve theoretical and methodological trade-offs.

**Future Research**
Future studies can explore the performance effects of network communities in more- versus less-developed economies, investigate how informal institutions interact with formal institutions and network communities, and examine network configurations that lead to the emergence and persistence of multiple insiders. Researchers can combine CPM with exponential random graph models or relational event models to study the coevolution of insiders and outsiders, and analyze how bridging ties operate within, outside, and across community boundaries.

**APA 7th Citation**
Wu, X., Adbi, A., & Mahmood, I. P. (2024). The social structure of insiders and outsiders: Toward a network community perspective on firm performance. *Academy of Management Journal*, 67(4), 903-932. https://doi.org/10.5465/amj.2022.0925
