---
id: nbs-2026-02-blanco-espeleta-2026
title: "Supporting repairability analysis through graph-based visualisation"
authors:
  - "Blanco-Espeleta, E."
  - "Pérez-Belis, V."
  - "Bovea, M. D."
year: 2026
journal: "Journal of Industrial Ecology"
doi: "https://doi.org/10.1007/s44498-026-00031-1"
volume: null
issue: null
pages: null

source: "NBS/2026-02"
pdf_path: "library/NBS/2026-02/pdfs/Blanco-Espeleta 2026 Supporting repairability analysis through graph-based visualisation.pdf"
text_path: "library/NBS/2026-02/text/Blanco-Espeleta 2026 Supporting repairability analysis through graph-based visualisation.txt"
ingested_at: "2026-04-14"
extraction_model: "claude-opus-4-6"
extraction_version: "v1"

paper_type: "empirical-quantitative"
keywords:
  - "Circular economy"
  - "EN 45554"
  - "Repair Index"
  - "Graph-based modelling"
  - "Network metrics"
  - "Industrial ecology"
theory:
  - "graph theory"
  - "network analysis"
topics:
  - "circular-economy"
  - "sustainable-materials"
  - "innovation-management"
unit_of_analysis: "firm"
level_of_theory: "meso"
dependent_variable_family: "environmental"
methods: "Three-stage methodology combining (I) input data structuring via an EN 45554-based Repair Matrix, (II) graph visualisation in Gephi using the ForceAtlas2 layout and (III) analytical output based on network metrics (degree, modularity, eccentricity, betweenness centrality) plus a novel graph-based Repair Index; demonstrated through an in-depth single-product case study."
sample:
  industry: "Small household appliances (capsule coffee machines)"
  country: "Not reported in paper"
  time_period: "Not reported in paper"
  units: "Product (capsule coffee machine) modelled as a graph of components and connections"
  n: "1 product case study"
---

# Supporting repairability analysis through graph-based visualisation

**Abstract**
Repairability is a key aspect of circular economy strategies, contributing to product longevity and resource efficiency. However, existing assessment methods often provide limited insight into product architecture and rarely combine visual and quantitative analysis. This study proposes a graph-based modelling approach for repairability assessment that integrates network metrics with structural visualisation. Building on EN 45554, an EN 45554-based Repair Matrix (RM) is used to assign repair-related attributes to product components and their connections. These attributes are represented as nodes and edges within a network, enabling both visual exploration and quantitative analysis of product architecture. A three-stage methodology is developed: (i) input data structuring, (ii) graph visualisation using Gephi software and (iii) analytical output. In addition, a novel graph-based Repair Index (RI) is introduced to quantify repairability at the system level. The approach is demonstrated through an in-depth case study of a capsule coffee machine. The results show that graph metrics such as degree, modularity, eccentricity and betweenness centrality effectively reveal structural complexity, accessibility constraints and critical components. The proposed method offers a conceptually scalable and interpretable framework that supports designfor-repair strategies by highlighting component dependencies and optimising disassembly logic. Overall, this work contributes to the development of more repairable and sustainable product architectures, supporting circular economy objectives.

**Research Question**
The main objective of the study is to assess the potential of graph-based modelling and network metrics as tools for evaluating product repairability, including identifying the required input data, the most relevant graph tools and metrics, appropriate visualisation strategies, and a new graph-based metric to quantify repairability at the network level.

**Mechanism Process**
- IV(s): Product architecture attributes derived from the EN 45554-based Repair Matrix (disassembly sequence/time, fastener type, required tools, working environment, skill level, spare-part availability, information availability, cost)
- DV(s): Structural repairability of the product, operationalised as a graph-based Repair Index (RI) and network metrics (degree, modularity, eccentricity, betweenness centrality, average path length)
- Mediators: Network structure of components and connections (nodes and edges) modelled in Gephi
- Moderators: Not reported in paper

The authors argue that repairability is driven not only by component-level attributes but by the structural configuration of the product's architecture. By encoding EN 45554-based Repair Matrix scores as node and edge attributes in a graph and applying the ForceAtlas2 layout in Gephi, the methodology makes visible how connectivity, accessibility and sequencing shape repair effort. Network metrics such as degree, modularity, eccentricity and betweenness centrality then translate this structure into quantitative indicators of complexity, accessibility constraints and critical components, which are aggregated into a novel graph-based Repair Index that summarises system-level repairability.

**Theoretical Contribution**
The study advances repairability assessment by integrating analysis, visualisation and parametrisation of repair-related information within a single graph-theoretic framework, addressing the gap left by conventional scoring matrices and static diagrams that do not preserve architectural logic. It introduces a novel graph-based Repair Index tailored to repairability, combining EN 45554-based parameters with network metrics so that accessibility, sequencing and part centrality are directly embedded in the assessment. In doing so, it contributes a conceptually scalable and interpretable methodology that links product architecture to circular-economy objectives of repairability and sustainability.

**Practical Implication**
Designers, policymakers and manufacturers can use the graph-based methodology as a decision-support tool to identify high-priority parts that should be redesigned to reduce dependency, improve accessibility or enhance modularity. By combining macro-level graph insights with micro-level node analysis and visual ranking, the approach provides actionable guidance for design-for-repair strategies and supports compliance with ecodesign and Right-to-Repair regulations such as Regulation (EU) 2024/1781.

**Limitations**
The work is an exploratory investigation tested through an in-depth case study on a single product configuration (a capsule coffee machine), so the immediate generalisation of the results is limited. The current implementation relies on expert-based scoring from the EN 45554-based Repair Matrix, whose weights may vary depending on the experts consulted, and Gephi is a general-purpose tool that does not interpret product structures or handle hierarchical assemblies, with modelling and data entry still performed manually.

**Future Research**
Future work will apply the approach to additional product models and categories to assess its versatility and generalisability, and will conduct systematic sensitivity and uncertainty analyses to examine how alternative weighting schemes influence the indicators. Empirical validation in collaboration with repair centres and manufacturers is planned to compare model-derived indicators (disassembly paths, repair effort, graph-based RI) with real-world repair times, frequencies and outcomes. The authors also plan to automate data integration and graph generation by linking the EN 45554-based Repair Matrix and the graph-based model directly to CAD environments, using machine learning to assist in the automatic identification and classification of components and connections.

**APA 7th Citation**
Blanco-Espeleta, E., Pérez-Belis, V., & Bovea, M. D. (2026). Supporting repairability analysis through graph-based visualisation. *Journal of Industrial Ecology*. https://doi.org/10.1007/s44498-026-00031-1
