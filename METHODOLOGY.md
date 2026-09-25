# Methodology: AI and molecular/related life-science grants, 2022–2025

## Purpose

This analysis identifies grants that combine artificial intelligence or machine learning with molecular or related life-science research in ARC, NHMRC and MRFF grant data. The implementation is intentionally simple, auditable and reproducible rather than an attempt to construct a perfect scientific ontology.

Headline results use only records classified automatically as **yes** for both AI and molecular/related life science. Records matched only by broader review terms are retained in the review queue but are not included in headline totals.

## Source data and analysis year

The analysis uses the three files listed in `source_manifest.csv`.

- **ARC:** one record per included grant; `funding-commencement-year` is the analysis year; `announced-funding-amount` is the nominal award value. Records with `grant-status == Declined` are excluded.
- **NHMRC:** records with `analysis_include == true`; `source_year` is the analysis year; `total_amount_awarded` is the nominal award value. The year represents the published application-round/source year.
- **MRFF:** non-empty rows from the `Grants List` sheet; contract start year is the analysis year; `Total Grant Value` is the nominal award value.

Only records with analysis years **2022, 2023, 2024 or 2025** are retained.

## Fields used for classification

The same rule is applied to source-specific text fields after normalisation:

- **ARC:** `grant-summary` and `primary-field-of-research`. The first sentence of `grant-summary` is retained as a convenience title, but the full grant summary is searched. The National Interest Test statement is retained in the classified output as supplementary text but is not used by the simple classifier.
- **NHMRC:** grant title, description, research keywords, health keywords, `fields_of_research`, `for_category` and broad research area. Grant opportunity/sub-type is retained as supplementary text but is not used by the simple classifier.
- **MRFF:** Project Name, Project Summary, Field(s) of Research and Broad Research Area. MRFF Initiative is retained as supplementary text but is not used by the simple classifier.

This separation is intentional: funding scheme names and policy-facing supplementary text should not themselves cause a scientific classification.

## Text processing

Title, summary and keyword fields are lower-cased, punctuation is converted to spaces and repeated whitespace is collapsed. Search terms are matched as complete normalised phrases rather than arbitrary substrings. FoR rules use case-insensitive substring matching against the supplied FoR text. Upper-case AI/ML acronyms are detected separately.

## AI/ML classification

A grant is classified **AI = yes** when either:

1. its FoR contains one of the AI FoR strings below; or
2. its title, summary or keywords contain one of the explicit AI/ML terms or named methods below; or
3. its text contains one of the explicitly recognised upper-case acronyms below.

Broader computational terms are **review signals only**. They place the grant in the review queue but are not counted as AI in the headline analysis. A specific ambiguity rule demotes `neural network` to review when it appears to refer to a biological neural network in a neuroscience/CNS FoR and there is no other computational/AI evidence.

### AI/ML FoR strings

`artificial intelligence`, `machine learning`, `computer vision`, `image processing`, `natural language processing`, `pattern recognition`, `intelligent systems`

### AI/ML acronyms

`AI`, `LLM`, `LLMs`, `CNN`, `CNNs`, `GNN`, `GNNs`, `NLP`, `SVM`, `SVMs`, `GAN`, `GANs`.

### Explicit AI/ML terms and methods

- **artificial intelligence:** `artificial intelligence`; `ai-enabled`; `ai enabled`; `ai-driven`; `ai driven`; `ai-based`; `ai based`; `ai-assisted`; `ai assisted`; `ai-accelerated`; `ai accelerated`; `ai-augmented`; `ai augmented`; `ai-powered`; `ai powered`; `ai-enhanced`; `ai enhanced`
- **machine learning:** `machine learning`; `machine-learning`
- **deep learning:** `deep learning`; `deep-learning`
- **federated learning:** `federated learning`; `federated-learning`
- **transfer learning:** `transfer learning`; `transfer-learning`
- **reinforcement learning:** `reinforcement learning`; `reinforcement-learning`
- **self-supervised learning:** `self-supervised learning`; `self supervised learning`
- **supervised/unsupervised learning:** `supervised learning`; `supervised-learning`; `unsupervised learning`; `unsupervised-learning`; `semi-supervised learning`; `semi supervised learning`
- **active/meta learning:** `active learning`; `meta-learning`; `meta learning`; `few-shot learning`; `zero-shot learning`
- **representation learning:** `representation learning`
- **foundation model:** `foundation model`; `foundation models`
- **large language model:** `large language model`; `large language models`
- **protein language model:** `protein language model`; `protein language models`
- **generative AI:** `generative ai`; `generative artificial intelligence`
- **neural network:** `neural network`; `neural networks`; `neural-network`; `neural-networks`
- **convolutional neural network:** `convolutional neural network`; `convolutional neural networks`
- **recurrent neural network:** `recurrent neural network`; `recurrent neural networks`
- **graph neural network:** `graph neural network`; `graph neural networks`
- **transformer model:** `transformer model`; `transformer models`; `transformer architecture`; `transformer-based`
- **natural language processing:** `natural language processing`
- **computer vision:** `computer vision`
- **random forest:** `random forest`; `random forests`
- **support vector machine:** `support vector machine`; `support vector machines`; `support vector classifier`; `support vector classifiers`
- **gradient boosting:** `gradient boosting`; `gradient-boosting`; `gradient boosted`; `gradient-boosted`
- **XGBoost:** `xgboost`
- **LightGBM:** `lightgbm`
- **CatBoost:** `catboost`
- **autoencoder:** `autoencoder`; `autoencoders`
- **generative adversarial network:** `generative adversarial network`; `generative adversarial networks`
- **decision tree:** `decision tree`; `decision trees`
- **nearest neighbours:** `k-nearest neighbour`; `k nearest neighbour`; `nearest-neighbour classifier`; `nearest neighbor classifier`
- **multilayer perceptron:** `multilayer perceptron`; `multi-layer perceptron`
- **AlphaFold:** `alphafold`
- **expert system:** `expert system`; `expert systems`

### AI review-only terms

- **digital twin:** `digital twin`; `digital twins`
- **predictive modelling:** `predictive modelling`; `predictive modeling`; `predictive model`; `predictive models`
- **prediction algorithm:** `prediction algorithm`; `prediction algorithms`; `predictive algorithm`; `predictive algorithms`
- **classification algorithm:** `classification algorithm`; `classification algorithms`
- **pattern recognition:** `pattern recognition`
- **automated image analysis:** `automated image analysis`; `automated imaging analysis`
- **image segmentation:** `image segmentation`; `automated segmentation`
- **object detection:** `object detection`
- **computational pathology:** `computational pathology`
- **radiomics:** `radiomics`
- **intelligent system:** `intelligent system`; `intelligent systems`
- **decision support:** `decision support system`; `decision-support system`; `clinical decision support`
- **data-driven model:** `data-driven model`; `data driven model`; `data-driven modelling`; `data driven modelling`
- **automated detection:** `automated detection`; `automated diagnosis`; `automated classification`; `automated recognition`
- **Bayesian network:** `bayesian network`; `bayesian networks`
- **evolutionary computation:** `evolutionary computation`; `swarm intelligence`
- **knowledge graph:** `knowledge graph`; `knowledge graphs`
- **anomaly detection:** `anomaly detection`
- **clustering:** `clustering algorithm`; `clustering algorithms`; `unsupervised clustering`
- **generative model:** `generative model`; `generative models`
- **data mining:** `data mining`
- **learning algorithm:** `learning algorithm`; `learning algorithms`
- **predictive analytics:** `predictive analytics`
- **image analysis:** `image analysis`; `imaging analysis`
- **recognition:** `image recognition`; `facial recognition`; `speech recognition`
- **computer-aided diagnosis:** `computer-aided diagnosis`; `computer aided diagnosis`
- **automated phenotyping:** `automated phenotyping`; `high-throughput phenotyping`

### Additional AI review combination

`bioinformatics` or `computational biology` combined with predictive/algorithmic language (`predict*`, `classifier`, `classification`, `learning algorithm`, `data-driven`, or `algorithm`) is retained for review but not counted automatically as AI.

## Molecular and related life-science classification

A grant is classified **molecular/related life science = yes** when either:

1. its FoR contains one of the biological/life-science FoR strings below; or
2. its title, summary or keywords contain one of the explicit molecular/biological term groups below.

Broader life-science terms are retained as **review signals only** when they occur without an explicit term or qualifying FoR. This is intended to keep areas such as neuroscience, ecology and physiology discoverable without automatically including every grant that happens to mention a cell or a molecular concept. Clinical/medical FoRs are retained as context but do not classify a grant by themselves.

### Molecular/life-science FoR strings

`biochemistry`, `cell biology`, `genetics`, `genomics`, `microbiology`, `immunology`, `biotechnology`, `bioinformatics`, `computational biology`, `medical microbiology`, `medical biochemistry`, `metabolomics`, `molecular medicine`, `molecular biology`, `medicinal and biomolecular chemistry`, `biological sciences`, `ecology`, `evolutionary biology`, `plant biology`, `zoology`, `animal science`, `agricultur`, `veterinary`, `marine biology`, `environmental biology`, `physiology`, `neuroscience`, `neurosciences`

### Explicit molecular/biological terms

- **genomics:** `genomics`; `genomic`; `genome-wide`; `whole genome`; `whole-genome`
- **genetics:** `genetics`; `genetic`; `polygenic`; `gene expression`; `gene regulatory`; `gene regulation`
- **transcriptomics:** `transcriptomics`; `transcriptomic`; `transcriptome`
- **proteomics:** `proteomics`; `proteomic`; `proteome`
- **metabolomics:** `metabolomics`; `metabolomic`; `metabolome`
- **epigenetics:** `epigenetics`; `epigenetic`; `epigenomics`; `epigenomic`; `chromatin`
- **single-cell:** `single-cell`; `single cell`
- **spatial omics:** `spatial transcriptomics`; `spatial proteomics`; `spatial genomics`; `spatial omics`
- **DNA/RNA:** `dna`; `rna`; `mrna`; `mirna`; `non-coding rna`; `noncoding rna`
- **sequencing:** `sequencing`; `sequence data`; `sequence analysis`
- **CRISPR/gene editing:** `crispr`; `gene editing`; `genome editing`
- **protein/peptide:** `protein`; `proteins`; `peptide`; `peptides`
- **enzyme:** `enzyme`; `enzymes`; `enzymatic`
- **receptor:** `receptor`; `receptors`
- **antibody/antigen:** `antibody`; `antibodies`; `antigen`; `antigens`
- **immune molecules/cells:** `cytokine`; `cytokines`; `chemokine`; `chemokines`; `t-cell`; `t cells`; `b-cell`; `b cells`
- **microbiome:** `microbiome`; `microbiomes`; `microbiota`
- **microbial/pathogen:** `bacteria`; `bacterial`; `bacterium`; `virus`; `viral`; `viruses`; `pathogen`; `pathogens`; `fungal`; `fungi`
- **organoid:** `organoid`; `organoids`
- **stem cell:** `stem cell`; `stem cells`
- **biomarker:** `biomarker`; `biomarkers`
- **molecular biology:** `molecular biology`; `molecular mechanism`; `molecular mechanisms`; `molecular pathway`; `molecular pathways`; `molecular profiling`
- **biochemistry:** `biochemistry`; `biochemical`
- **systems biology:** `systems biology`
- **synthetic biology:** `synthetic biology`
- **structural biology:** `structural biology`; `protein structure`; `protein structures`
- **bioinformatics:** `bioinformatics`; `computational biology`
- **molecular diagnostics:** `molecular diagnostic`; `molecular diagnostics`

### Broader life-science review-only terms

- **cell biology:** `cell biology`; `cellular biology`
- **cells:** `cells`; `cellular`
- **immunology:** `immunology`; `immunological`; `immune response`; `immune system`
- **physiology:** `physiology`; `physiological`
- **microbiology:** `microbiology`; `microbiological`
- **neuroscience:** `neuroscience`; `neuroscientific`; `neural circuit`; `neural circuits`
- **developmental biology:** `developmental biology`; `embryonic`; `embryogenesis`
- **evolution:** `evolutionary biology`; `evolutionary`; `phylogeny`; `phylogenetic`
- **ecology:** `ecology`; `ecological`; `biodiversity`; `ecosystem`; `ecosystems`
- **plant biology:** `plant biology`; `plant physiology`; `crop`; `crops`
- **animal biology:** `zoology`; `animal biology`; `livestock`
- **marine biology:** `marine biology`; `marine organism`; `marine organisms`
- **disease mechanism:** `disease mechanism`; `disease mechanisms`; `pathogenesis`
- **molecular:** `molecular`

### Clinical FoR context strings

These are stored as contextual evidence only and do not classify a grant by themselves:

`oncology`, `carcinogenesis`, `pathology`, `pharmacology`, `clinical science`, `cardiovascular`, `haematology`, `hematology`, `respiratory`, `infectious`, `endocrin`, `reproductive medicine`, `paediatrics`, `pediatrics`, `ophthalmology`, `nutrition`

### False-positive guards

The following phrases prevent obvious non-life-science uses of otherwise relevant vocabulary from creating a match:

`solar cell`, `solar cells`, `fuel cell`, `fuel cells`, `battery cell`, `battery cells`, `electrochemical cell`, `electrochemical cells`, `photovoltaic cell`, `photovoltaic cells`, `genetic algorithm`, `genetic algorithms`, `molecular dynamics`, `molecular electronics`, `molecular material`, `molecular materials`, `molecular beam`, `molecular simulation`

In particular, `genetic algorithm` does not count as genetic life science, and `molecular dynamics`, `molecular electronics`, `molecular materials`, `molecular beam` and `molecular simulation` do not count solely because they contain `molecular`.

## Review status

Every record has `ai_status` and `mls_status` with values `yes`, `review` or `no`, plus a combined `review_status`.

- `auto_classified`: neither classifier requires review.
- `AI review required`: only the AI screen is ambiguous.
- `MLS review required`: only the molecular/life-science screen is ambiguous.
- `AI and MLS review required`: both are ambiguous.

The current headline analysis is deterministic: only `yes` classifications are counted. Review-only records are provided in `review_queue_2022_2025.xlsx` for later refinement and are not silently adjudicated.

## Funding summaries and denominators

For every funder and year, the summary contains raw counts and nominal award values for:

- all grants;
- AI grants;
- molecular/related life-science grants; and
- grants classified as both AI and molecular/related life science.

It also reports all three funding proportions discussed during development:

1. AI + molecular/life-science funding / **all funding**;
2. AI + molecular/life-science funding / **all AI funding**; and
3. AI + molecular/life-science funding / **all molecular/life-science funding**.

Equivalent grant-count proportions are also reported.

For the main presentation:

- **ARC headline:** AI + molecular/life-science funding as a percentage of **all ARC AI funding**.
- **NHMRC headline:** AI + molecular/life-science funding as a percentage of **all NHMRC funding**.
- **MRFF headline:** AI + molecular/life-science funding as a percentage of **all MRFF funding**.

These headline percentages have intentionally different denominators because ARC is a general research funder, while NHMRC and MRFF are health/medical research funders. They should not be interpreted as directly equivalent portfolio shares.

## Validation

`validation_sample_2022_2025.xlsx` contains a stratified sample from AI+MLS positives, AI review cases, MLS review cases, AI-positive/MLS-negative cases, MLS-positive/AI-negative cases and double negatives. It is intended for manual checking of precision and missed cases. The current results do not assume that this validation sample has already been manually adjudicated.

## Reproducibility

`build_grant_analysis.py` is the source of truth for the dictionaries, normalisation, classification and summary calculations. `terms_and_for_2022_2025.xlsx` is generated directly from the same dictionaries. `source_manifest.csv` records source-file SHA-256 hashes. Running `run_analysis.sh` against the packaged input files recreates the CSV and Excel outputs.

## Limitations

This is a lexical/FoR screen, not a semantic gold-standard classification. Explicit AI terminology can occasionally be incidental, and some AI work may be described without any listed term. Similarly, the molecular/life-science boundary is operational rather than ontological. The review and validation files are included so that these limitations can be quantified or corrected later without changing the basic pipeline.
