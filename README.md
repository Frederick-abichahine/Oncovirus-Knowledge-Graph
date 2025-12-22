# Oncovirus Knowledge Graph
### _Knowledge Graphs Project_

---
## Frederick , FAC, Abi Chahine
> M.Sc. in Quantitative & Computational Biology, University of Trento, Italy
## Hala, HA, Alshaar
> M.Sc. in Quantitative & Computational Biology, University of Trento, Italy 

---

## **Note**  
> This README provides a **high-level overview** of the *Oncovirus Knowledge Graph* project.  
> For full methodological details, datasets, figures, and evaluations, please refer to the complete project report available in the repository.


## Index

1. [Introduction](#1-introduction)
2. [Purpose Definition](#2-purpose-definition)
3. [Information Gathering](#3-information-gathering)
4. [Schema and Ontologies](#4-schema-and-ontologies)
5. [Language Definition](#5-language-definition)
6. [Knowledge Definition](#6-knowledge-definition)
7. [Entity Definition](#7-entity-definition)
8. [Evaluation](#8-evaluation)
9. [Metadata Definition](#9-metadata-definition)
10. [Open Problems and Conclusion](#10-open-problems-and-conclusion)
11. [References](#11-references)

---

## 1. Introduction

Oncoviruses are viruses capable of inducing cancer development and are responsible for a significant fraction of human cancers. Notable examples include Human Papillomavirus (HPV), Hepatitis B and C viruses (HBV, HCV), and Epstein–Barr Virus (EBV).

Understanding molecular interactions between viral and host proteins, their effects on cellular pathways, and resulting phenotypes is essential for revealing oncogenic mechanisms and developing targeted therapies or vaccines [1][4].

However, existing knowledge is fragmented across heterogeneous sources (UniProt, KEGG, Reactome, scientific literature), making integration and unified querying difficult.

A **Knowledge Graph (KG)** enables semantic integration, reasoning, and hypothesis generation by linking viruses, proteins, pathways, phenotypes, cancers, and vaccines into a coherent structure [2].
This project constructs a comprehensive **Oncovirus Knowledge Graph** following the **ITELOS methodology** [3].

---

## 2. Purpose Definition

### 2.1 Informal Purpose

The purpose of this KG is to provide a unified and semantically rich representation of biological mechanisms through which viruses contribute to cancer development.

It integrates information on:

* Oncogenic viruses
* Viral and host proteins
* Cellular pathways
* Phenotypes
* Cancers
* Vaccines

The KG enables:

* Data integration
* Semantic reasoning
* Hypothesis generation
* Support for vaccine and therapeutic research

---

### 2.2 Domain of Interest

The domain encompasses **molecular, cellular, and clinical aspects of virus-induced cancers**, modeling how viruses manipulate host machinery to drive tumorigenesis.

#### 2.2.1 Space

* Focus on **human biological systems**
* Molecular and cellular host–virus interactions
* Tissue specificity (e.g., liver, cervix, lymphatic tissue)
* Viruses included:

  * HPV
  * HBV
  * HCV
  * EBV
  * HTLV-1

#### 2.2.2 Time

* From viral infection to cancer development
* Covers stages such as:

  * Viral entry
  * Integration
  * Latency
  * Immune evasion
  * Cellular transformation
* Literature timeframe: **2000–2025**

---

### 2.3 Scenarios

Example use cases:

* Identify virus–cancer associations
* Explore virus–host protein interactions
* Analyze disrupted cellular pathways
* Assess vaccine availability
* Perform phenotype-based discovery
* Compare oncogenic viruses

---

### 2.4 Personas

* **Dr. Elisa Marino** – Virologist
* **Dr. James Liu** – Computational Biologist
* **Dr. Maria Rossi** – Oncologist
* **Dr. Daniel Ortega** – Vaccine Researcher
* **Dr. Anna Becker** – Molecular Pathologist
* **Prof. Samuel Green** – Bioinformatics Educator
* **Dr. Rania Al-Hassan** – Data Scientist

---

### 2.5 Competency Questions (CQs)

* Which viruses cause which cancers?
* Which host proteins interact with viral proteins?
* Which pathways are disrupted?
* Are vaccines available?
* What viral phenotypes exist?
* Which viruses target a specific host protein?
* Which viral proteins disrupt specific pathways?

---

### 2.6 Concepts Identification

#### 2.6.1 Entity Types (ETypes)

| Entity Type       | Category   | Description              | Key Attributes                         |
| ----------------- | ---------- | ------------------------ | -------------------------------------- |
| Virus             | Core       | Oncogenic viruses        | virusCode, organismName, species, host |
| Cancer            | Core       | Virus-associated cancers | cancerID, cancerType, primarySite      |
| Vaccine           | Core       | Preventive vaccines      | vaccineID, vaccineName, description    |
| ViralProtein      | Common     | Viral proteins           | viralUniprotID, geneName               |
| HostProtein       | Common     | Human proteins           | hostUniprotID, geneName                |
| Pathway           | Common     | Biological pathways      | pathwayKeggID, pathwayName             |
| ProteinAnnotation | Contextual | Protein metadata         | function, localization                 |
| Phenotype         | Contextual | Viral traits             | phenotypeID, trait                     |

---

#### 2.6.2 Relationships

* Vaccine **targets** Virus
* Virus **causes** Cancer
* Virus **hasPhenotype** Phenotype
* Virus **encodes** ViralProtein
* ViralProtein **interactsWith** HostProtein
* HostProtein **hasAnnotation** ProteinAnnotation
* HostProtein **involvedIn** Pathway

---

### 2.7 ER Diagram

> **Figure 1:** ER diagram illustrating ETypes and relationships  
> *(See `/phase_1_purpose_definition/oncovirus_ER_diagram_light.png` in repository)*

---

### 2.8 Qualitative Evaluation

Minor refinements ensured alignment between purpose definition and ER structure without changing project scope.

---

## 3. Information Gathering

### 3.1 Data Sources

* **NCBI Virus** [5]
* **UniProt** [6]
* **IntAct** [7]
* **KEGG** [8]
* **ViralZone** [9]
* **WHO** [10]

These sources provide genomic, proteomic, interaction, pathway, and epidemiological data.

---

### 3.2 Data Preprocessing

* Automated Python pipelines
* Removed:

  * 2,360 incomplete records
  * 148 duplicates
* Final dataset:

  * 31 viral proteins
  * 759 host proteins
  * 2,272 pathways

#### Generated Files

| File                        | EType             |
| --------------------------- | ----------------- |
| virus_data.tsv              | Virus             |
| viral_protein_data.tsv      | ViralProtein      |
| host_protein_data.tsv       | HostProtein       |
| pathway_data.tsv            | Pathway           |
| vaccine_data.tsv            | Vaccine           |
| cancer_data.tsv             | Cancer            |
| virus_phenotype_data.tsv    | Phenotype         |
| protein_annotation_data.tsv | ProteinAnnotation |

---

### 3.3 Qualitative Evaluation

ER model remained valid; attributes and naming refined for biological clarity.

---

## 4. Schema and Ontologies

ETypes aligned where possible with:

* Human Disease Ontology
* Vaccine Ontology
* Pathway Ontology
* NCBO BioPortal resources

Custom schema used where no suitable ontology existed.

---

## 5. Language Definition

Formalization of concepts using:

* UKC
* NCBO BioPortal
* Custom OKG25 identifiers

### 5.1 Concept Identification

> **Table 3:** Language Resource Table  
> *(See full table in repository `/phase_3_language_definition/language_resource_table.xlsx` for readability)*

---

### 5.2 Language Teleontology

* Implemented in **Protégé**
* Exported as:

  ```
  oncovirus_KG_language_teleontology.owl
  ```

---

### 5.3 Qualitative Evaluation

* Removed inconsistent Pathway → Cancer relation
* Renamed properties for semantic clarity
* Preserved original purpose definition

---

## 6. Knowledge Definition

Formalized knowledge-level ontology with:

* Explicit IRIs
* Domain & range constraints
* Logical axioms

### 6.1–6.4 Highlights

* Root class: `Thing`
* 8 ETypes
* 8 object properties
* 29 data properties
* 261 total axioms

Ontology file:

```
oncovirus_KG_knowledge_teleontology.owl
```

---

## 7. Entity Definition

KG construction using **Karma**:

* Entity matching
* Entity identification
* Dataset-ontology mapping

### 7.1 Entity Identifiers

| Entity            | Identifier          |
| ----------------- | ------------------- |
| Virus             | virusCode           |
| Vaccine           | vaccineID           |
| Cancer            | cancerID            |
| Pathway           | pathwayKeggID       |
| Phenotype         | phenotypeID         |
| ViralProtein      | viralUniprotID      |
| HostProtein       | hostUniprotID       |
| ProteinAnnotation | proteinAnnotationID |

---

### 7.2 Visualization

* RDF imported into **GraphDB**
* Class and graph visualizations validated structure

---

## 8. Evaluation

### 8.1 Addressing CQs

Seven SPARQL queries executed in GraphDB successfully answered all CQs.

> Figures 12–18: SPARQL queries and results  
> *(See `/evaluation/sparql_CQ_queries.sparqlbook` in repository for all the queries used)*

---

### 8.2–8.5 Coverage & Connectivity

* High CQ coverage
* Strong schema–teleontology alignment
* Acceptable sparsity and connectivity metrics

---

## 9. Metadata Definition

Stored as `.xlsx`:

* `project_metadata.xlsx`
* `language_metadata.xlsx`
* `knowledge_metadata.xlsx`

Compatible with **LiveKnowledge** distribution.

---

## 10. Open Problems and Conclusion

This project successfully demonstrates the construction of an **Oncovirus Knowledge Graph** integrating molecular, clinical, and epidemiological data.

The KG:

* Answers all competency questions
* Is internally consistent
* Provides a scalable foundation for future expansion

Future work includes adding:

* More viruses
* Additional diseases
* Richer phenotypic and clinical annotations

---

## 11. References

[1]	“Oncovirus - an Overview | ScienceDirect Topics.” Www.sciencedirect.com, www.sciencedirect.com/topics/immunology-and-microbiology/oncovirus.

[2]	M. Kejriwal. Domain-Specific KG Construction. 1 Jan. 2019, www.researchgate.net/publication/332140558_Domain-specific_knowledge_graph_construction.

[3]	Giunchiglia, Fausto, et al. ITelos- Building Reusable KGs. 19 May 2021, www.researchgate.net/publication/351744853_iTelos-_Building_reusable_knowledge_graphs.

[4]	Xiao, Qing, et al. “Viral Oncogenesis in Cancer: From Mechanisms to Therapeutics.” Signal Transduction and Targeted Therapy, vol. 10, no. 1, 12 May 2025, www.nature.com/articles/s41392-025-02197-9, https://doi.org/10.1038/s41392-025-02197-9.

[5]	“NCBI Virus.” Www.ncbi.nlm.nih.gov, www.ncbi.nlm.nih.gov/labs/virus/vssi/#/.

[6]	“UniProt.” Uniprot, 2023, www.uniprot.org/.

[7]	“IntAct Portal.” Www.ebi.ac.uk, www.ebi.ac.uk/intact/home.

[8]	“KEGG: Kyoto Encyclopedia of Genes and Genomes.” Www.genome.jp, www.genome.jp/kegg/.

[9]	“ViralZone Root.” Expasy.org, 2020, viralzone.expasy.org/.

[10]	World Health Organization. “World Health Organization.” Who.int, World Health Organization, 2025, www.who.int/.

[11]	“Welcome to the NCBO BioPortal | NCBO BioPortal.” Bioontology.org, 2019, bioportal.bioontology.org/.

[12]	“UKC – Universal Knowledge Core – UKC.” Unitn.it, 2021, ukc.disi.unitn.it/. Accessed 11 Dec. 2025.

[13]	Center, Stanford. “Protégé.” Stanford.edu, 2019, protege.stanford.edu/.

[14]	 usc-isi-i2. “Home.” GitHub, 3 Oct. 2015, github.com/usc-isi-i2/Web-Karma/wiki. Accessed 11 Dec. 2025.

[15]	Datasets. (n.d.). LiveKnowledge. https://datascientiafoundation.github.io/LiveKnowledge/datasets

[16]	“GraphDB Downloads and Resources.” Ontotext.com, 2015, graphdb.ontotext.com/.

[17]	Schema.org. “Home - Schema.org.” Schema.org, 2019, schema.org/.

[18]	“Bioschemas - Live Deploys.” Bioschemas.org, 2022, bioschemas.org/developer/liveDeploys#heading3. Accessed 21 Dec. 2025.
