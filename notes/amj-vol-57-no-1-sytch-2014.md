---
id: amj-vol-57-no-1-sytch-2014
title: "Exploring the Locus of Invention: The Dynamics of Network Communities and Firms' Invention Productivity"
authors:
  - "Sytch, M."
  - "Tatarynowicz, A."
year: 2014
journal: "Academy of Management Journal"
doi: "https://doi.org/10.5465/amj.2011.0655"
volume: 57
issue: 1
pages: "249-279"

source: "AMJ/vol-57-no-1"
pdf_path: "library/AMJ/vol-57-no-1/pdfs/Sytch 2014 Exploring the Locus of Invention The Dynamics of Network Communities and Firms Invention Productivity.pdf"
text_path: "library/AMJ/vol-57-no-1/text/Sytch 2014 Exploring the Locus of Invention The Dynamics of Network Communities and Firms Invention Productivity.txt"
ingested_at: "2026-07-10"
extraction_model: "claude-fable-5"
extraction_version: "v3"

paper_type: "empirical-quantitative"
keywords: ["network communities", "invention productivity", "membership turnover", "interorganizational partnerships", "knowledge heterogeneity"]
theory: ["network community perspective", "ego network perspective (Burt, 1992; Ahuja, 2000)", "global network perspective (Schilling & Phelps, 2007; Uzzi & Spiro, 2005)"]
topics: ["innovation-management", "longitudinal"]
unit_of_analysis: "firm"
level_of_theory: "cross-level"
dependent_variable_family: "financial"
methods: "Longitudinal network panel; Girvan-Newman community detection on yearly alliance networks; negative binomial regression with conditional firm-level fixed effects; three-level Poisson models with random intercepts and random coefficients"
sample:
  industry: "Global computer industry (technology alliances; about 60% manufacturing, 30% services, 10% embedded systems)"
  country: "Global (multi-country interorganizational partnership network)"
  time_period: "Partnership data 1981-2001; yearly networks 1985-2001; patents filed 1986-2002"
  units: "Firm-year observations"
  n: "918 firm-year observations across 192 unique computer firms (720 firm-years in fixed-effects estimation; 410 firms in the full network sample)"

# Mandatory evidence anchors (v3 - Layer 1 faithfulness audit).
evidence:
  sample_n: "included 918 firm-year observations across 192"
  sample_country: "global computer industry from 1981 to 2001"
  sample_industry: "we use the evolving community structure of the network of interorganizational partnerships in the global computer industry"
  sample_time_period: "computer industry over 1981–2001 to predict firms’ patenting rates"
  theories_overview: "Departing from prior research analyzing the implications of social structure for actors’ outcomes by applying either an ego network or a global network perspective"
  methods_overview: "negative binomial models with firm-level fixed"
  keywords_source: "we examine how the membership dynamics of a network community affect the invention productivity of member firms"
  hypotheses_source: "Hypothesis 1. The turnover of community"
  measures_overview: "number of patents a focal firm applied for in year"
  findings_overview: "Our findings suggest, first, that a firm reaps the greatest invention benefits in a network community with moderate levels of membership turnover"
---

# Exploring the Locus of Invention: The Dynamics of Network Communities and Firms' Invention Productivity

**Abstract**
Departing from prior research analyzing the implications of social structure for actors’ outcomes by applying either an ego network or a global network perspective, this study examines the implications of network communities for the invention productivity of firms. Network communities represent dense and nonoverlapping structural groups of actors in a social system. A network community lens helps identify new ways to study firms’ access to diverse knowledge inputs in a dynamic system of interorganizational relationships. Specifically, we examine how the membership dynamics of a network community affect the invention productivity of member firms by either enabling or constraining access to broad, diverse knowledge inputs. Our findings suggest, first, that a firm reaps the greatest invention benefits in a network community with moderate levels of membership turnover. Second, a firm attains the greatest invention productivity when its own rate of movement across different network communities is moderate. Third, we find that community members located in the core of their network community can benefit more from membership dynamics and prior community affiliations than those on its periphery. In empirical analyses, we use the evolving community structure of the network of interorganizational partnerships in the global computer industry over 1981–2001 to predict firms’ patenting rates.

**Research Question**
How do the membership dynamics of network communities (the turnover of community members and a firm's own rate of movement across different communities) affect the invention productivity of member firms, and how do these effects vary with a firm's core/periphery location in its community and with global network reach?

**Hypotheses / Propositions**
H1: The turnover of community members in a firm's network community has an inverted U-shaped effect on the firm's invention productivity; the firm attains the highest invention productivity at a moderate rate of membership turnover.
H2: A firm's movement across different network communities has an inverted U-shaped effect on the firm's invention productivity; the firm attains the highest invention productivity if it moves across network communities at a moderate rate.
H3a: The inverted curvilinear relationship between membership turnover and invention productivity is moderated by the firm's core/periphery location in the community; a core firm benefits more from a moderate rate of membership turnover than a peripheral firm.
H3b: The inverted curvilinear relationship between a firm's movement across network communities and invention productivity is moderated by the firm's core/periphery location in the communities it encounters; a firm occupying a core position benefits more from a moderate rate of movement than a firm occupying peripheral positions.
H4a: The membership turnover relationship is moderated by global network reach; the positive effect of a moderate rate of membership turnover is weaker at higher levels of global network reach.
H4b: The movement relationship is moderated by global network reach; the positive effect of a moderate rate of movement is weaker at higher levels of global network reach.

**Mechanism Process**
- IV(s): Community membership turnover (year-on-year change in the member composition of the firm's network community); prior community affiliations (the firm's movement across different network communities); both specified with linear and squared terms.
- DV(s): Firm invention productivity, measured as the count of successful patent applications in year t+1.
- Mediators: None specified.
- Moderators: Within-community coreness (the firm's core/periphery location); global network reach (average network reach between any two firms, and its firm-history average).

Network communities are dense, nonoverlapping structural groups whose internal connectivity homogenizes knowledge within community boundaries while sparse between-community connectivity preserves knowledge heterogeneity across them. Membership dynamics update the knowledge base that is locally accessible to member firms: moderate membership turnover opens up and updates a community's knowledge base without imposing the trust, collaboration, and stability costs of excessive turnover, and moderate movement across communities gives a firm direct exposure to diverse knowledge inputs while avoiding integration costs, permanent newcomer status, and an incoherent collaborative profile. Core positions in a community provide broader and quicker access to the community's updated knowledge base, so core firms are expected to capture more of these benefits.

**Data & Measures**
Data: interorganizational technology partnerships in the global computer industry, 1981-2001, from the MERIT-CATI database; 410 unique computer firms; yearly networks reconstructed for 1985-2001 (17 annual observations, partnership duration set to five years). The effective sample included 918 firm-year observations across 192 unique computer firms; the conditional fixed-effects estimation truncated this by about 20 percent to 720 firm-year observations because firms that never patented were eliminated. DV: number of patents in t+1, the count of a firm's eventually approved patent applications from the NBER database of US patents, category 2 "computers & communications" (143,500 patents). IVs: membership turnover, measured as the inverse of community overlap across contiguous years; prior community affiliations, the number of distinct communities the firm belonged to before t, excluding the current community. Moderators: within-community coreness (Borgatti and Everett continuous core/periphery model, including its firm-history average) and global network reach (average inverted network distance, including its firm-history average). Communities were identified each year with the Girvan and Newman (2002) modularity-maximization method (average modularity 0.63). Estimation: negative binomial regression with conditional firm-level fixed effects plus three-level Poisson models with random intercepts and random coefficients; controls include headcount, net income, return on assets, R&D spending, ego network measures, and community characteristics. The design is an observational longitudinal panel; firm-level fixed effects are used to eliminate unobserved heterogeneity in firms' propensity to patent, and no experimental identification is claimed.

**Key Findings**
H1 supported: membership turnover has an inverted U-shaped effect on invention productivity (inflection at 47 percent turnover); a member of a moderately dynamic community (retaining about 55 percent of its members year to year) files 19.5 percent more patents than a member of a static community and 4.2 percent more than a member of a highly dynamic one. H2 supported: movement across communities has an inverted U-shaped effect (inflection at five prior community affiliations); a firm with about five prior affiliations files approximately twice as many patents as a firm with none and about 50 percent more than a firm with nine. H3a consistently supported: the positive effect of moderate turnover is amplified for core firms, who file about 5 percent more patents than peripheral members of a moderately dynamic community. H3b only partially supported: the interaction is not supported in the partial models but is supported in the fully specified models, with the inflection point shifting from five to three prior communities for core firms. H4a and H4b not supported: the negative binomial models show null interaction effects and the multilevel Poisson models yield estimates opposite to expectations. Supplementary analyses indicate that two firms in the same community are on average twice as likely to cite each other's patents as outsiders' patents, and that community dynamics are substantially driven by the behaviors of other firms rather than the focal firm's own new alliance formation.

**Theoretical Contribution**
The study advances a network community perspective as a third lens, beyond the ego network and global network perspectives, on how social structure shapes firms' invention: community boundaries demarcate homogeneous knowledge inputs, and the membership dynamics of communities have fundamental implications for firms' invention outcomes, casting doubt on the conclusion that only ego networks matter for actor outcomes. It contributes to research on network dynamics by identifying membership dynamics as an influential dimension of network change and by showing that community dynamics are significantly driven by other firms' behaviors rather than a firm's own pursuits, suggesting constrained individual agency over network positions. It also shows that ego network properties interact with features of network communities, a step toward a more integrative, multilevel approach to the relationship between network structures and actors' behaviors and outcomes.

**Practical Implication**
For firms in interorganizational partnership networks such as the computer industry studied here, the results imply that invention productivity is greatest in moderately dynamic network communities and at a moderate rate of movement across communities, and that firms located in community cores capture more of these benefits than peripheral members. The authors frame this as a tension between deep integration and search across only a few network communities as a core member versus a quick scan and peripheral entry into numerous network communities, and note that network communities tend to allow rich firms and firms in their cores to get even richer.

**Limitations**
The authors note that their theory and results are tailored to sparsely connected interorganizational systems in which network communities do not overlap, and that the network community lens is of limited applicability where a global network resembles a random network or displays a strong core/periphery structure; its use is contingent on a robust community structure being present. In addition, the conditional fixed-effects estimator eliminated firms that never patented during the 17-year window, truncating the sample by about 20 percent, a limitation addressed with alternative full-sample models in robustness tests.

**Future Research**
The authors propose extending the analysis to systems with overlapping network communities and to actors who are members of more than one community at a time, and applying the network community lens to a broader range of industrial, national, and institutional systems, including economies organized around business groups. They also suggest that ego network studies attend to whether an ego's alters sit in the same or different communities; that research explore how network communities form and evolve in industrial districts and regional economies; that industry analyses combine network communities of collaborators with groups of rivals, adding a cognitive lens on executives' and influential third parties' (such as financial analysts') perceptions of collaboration and rivalry; and that future work more systematically analyze how firm-level attributes interact with community membership dynamics.

**APA 7th Citation**
Sytch, M., & Tatarynowicz, A. (2014). Exploring the locus of invention: The dynamics of network communities and firms' invention productivity. *Academy of Management Journal*, 57(1), 249-279. https://doi.org/10.5465/amj.2011.0655
