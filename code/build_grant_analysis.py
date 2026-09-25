#!/usr/bin/env python3
"""Build the 2022-2025 ARC/NHMRC/MRFF AI + molecular/life-science analysis.

The classifier is intentionally simple and auditable.

Molecular/related life science:
  YES if a biological/life-science FoR matches OR an explicit molecular/biological text group matches.
  REVIEW for broader life-science text terms that do not meet the headline rule.
  Otherwise NO.

AI/ML:
  YES if an AI-related FoR matches or an explicit AI/ML term/named method matches.
  REVIEW for broader computational terms such as digital twins, predictive modelling,
  radiomics and automated image analysis, plus biological 'neural network' ambiguity.
  Otherwise NO.

Review-only records are not included in headline AI + molecular/life-science totals.
All exact dictionaries are exported to terms_and_for.xlsx.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

START_YEAR = 2022
END_YEAR = 2025

AI_EXPLICIT = {
    "artificial intelligence": ["artificial intelligence", "ai-enabled", "ai enabled", "ai-driven", "ai driven", "ai-based", "ai based", "ai-assisted", "ai assisted", "ai-accelerated", "ai accelerated", "ai-augmented", "ai augmented", "ai-powered", "ai powered", "ai-enhanced", "ai enhanced"],
    "machine learning": ["machine learning", "machine-learning"],
    "deep learning": ["deep learning", "deep-learning"],
    "federated learning": ["federated learning", "federated-learning"],
    "transfer learning": ["transfer learning", "transfer-learning"],
    "reinforcement learning": ["reinforcement learning", "reinforcement-learning"],
    "self-supervised learning": ["self-supervised learning", "self supervised learning"],
    "supervised/unsupervised learning": ["supervised learning", "supervised-learning", "unsupervised learning", "unsupervised-learning", "semi-supervised learning", "semi supervised learning"],
    "active/meta learning": ["active learning", "meta-learning", "meta learning", "few-shot learning", "zero-shot learning"],
    "representation learning": ["representation learning"],
    "foundation model": ["foundation model", "foundation models"],
    "large language model": ["large language model", "large language models"],
    "protein language model": ["protein language model", "protein language models"],
    "generative AI": ["generative ai", "generative artificial intelligence"],
    "neural network": ["neural network", "neural networks", "neural-network", "neural-networks"],
    "convolutional neural network": ["convolutional neural network", "convolutional neural networks"],
    "recurrent neural network": ["recurrent neural network", "recurrent neural networks"],
    "graph neural network": ["graph neural network", "graph neural networks"],
    "transformer model": ["transformer model", "transformer models", "transformer architecture", "transformer-based"],
    "natural language processing": ["natural language processing"],
    "computer vision": ["computer vision"],
    "random forest": ["random forest", "random forests"],
    "support vector machine": ["support vector machine", "support vector machines", "support vector classifier", "support vector classifiers"],
    "gradient boosting": ["gradient boosting", "gradient-boosting", "gradient boosted", "gradient-boosted"],
    "XGBoost": ["xgboost"],
    "LightGBM": ["lightgbm"],
    "CatBoost": ["catboost"],
    "autoencoder": ["autoencoder", "autoencoders"],
    "generative adversarial network": ["generative adversarial network", "generative adversarial networks"],
    "decision tree": ["decision tree", "decision trees"],
    "nearest neighbours": ["k-nearest neighbour", "k nearest neighbour", "nearest-neighbour classifier", "nearest neighbor classifier"],
    "multilayer perceptron": ["multilayer perceptron", "multi-layer perceptron"],
    "AlphaFold": ["alphafold"],
    "expert system": ["expert system", "expert systems"],
}

AI_REVIEW = {
    "digital twin": ["digital twin", "digital twins"],
    "predictive modelling": ["predictive modelling", "predictive modeling", "predictive model", "predictive models"],
    "prediction algorithm": ["prediction algorithm", "prediction algorithms", "predictive algorithm", "predictive algorithms"],
    "classification algorithm": ["classification algorithm", "classification algorithms"],
    "pattern recognition": ["pattern recognition"],
    "automated image analysis": ["automated image analysis", "automated imaging analysis"],
    "image segmentation": ["image segmentation", "automated segmentation"],
    "object detection": ["object detection"],
    "computational pathology": ["computational pathology"],
    "radiomics": ["radiomics"],
    "intelligent system": ["intelligent system", "intelligent systems"],
    "decision support": ["decision support system", "decision-support system", "clinical decision support"],
    "data-driven model": ["data-driven model", "data driven model", "data-driven modelling", "data driven modelling"],
    "automated detection": ["automated detection", "automated diagnosis", "automated classification", "automated recognition"],
    "Bayesian network": ["bayesian network", "bayesian networks"],
    "evolutionary computation": ["evolutionary computation", "swarm intelligence"],
    "knowledge graph": ["knowledge graph", "knowledge graphs"],
    "anomaly detection": ["anomaly detection"],
    "clustering": ["clustering algorithm", "clustering algorithms", "unsupervised clustering"],
    "generative model": ["generative model", "generative models"],
    "data mining": ["data mining"],
    "learning algorithm": ["learning algorithm", "learning algorithms"],
    "predictive analytics": ["predictive analytics"],
    "image analysis": ["image analysis", "imaging analysis"],
    "recognition": ["image recognition", "facial recognition", "speech recognition"],
    "computer-aided diagnosis": ["computer-aided diagnosis", "computer aided diagnosis"],
    "automated phenotyping": ["automated phenotyping", "high-throughput phenotyping"],
}

AI_FOR = [
    "artificial intelligence", "machine learning", "computer vision", "image processing",
    "natural language processing", "pattern recognition", "intelligent systems",
]

AI_ACRONYM_RE = re.compile(r"\b(AI|LLMs?|CNNs?|GNNs?|NLP|SVMs?|GANs?)\b")
AI_GENERIC_CENTRAL_RE = re.compile(
    r"(?:\b(?:use|using|uses|utilise|utilize|develop|developing|apply|applying|harness|integrate|"
    r"build|create|deploy|train|enable)\b.{0,80}\b(?:AI|artificial intelligence)\b)|"
    r"(?:\b(?:AI|artificial intelligence)\b.{0,50}\b(?:method|model|tool|system|platform|approach|"
    r"algorithm|analysis|diagnosis|prediction|design|screening)\b)",
    re.I,
)

MLS_EXPLICIT_TEXT = {
    "genomics": ["genomics", "genomic", "genome-wide", "whole genome", "whole-genome"],
    "genetics": ["genetics", "genetic", "polygenic", "gene expression", "gene regulatory", "gene regulation"],
    "transcriptomics": ["transcriptomics", "transcriptomic", "transcriptome"],
    "proteomics": ["proteomics", "proteomic", "proteome"],
    "metabolomics": ["metabolomics", "metabolomic", "metabolome"],
    "epigenetics": ["epigenetics", "epigenetic", "epigenomics", "epigenomic", "chromatin"],
    "single-cell": ["single-cell", "single cell"],
    "spatial omics": ["spatial transcriptomics", "spatial proteomics", "spatial genomics", "spatial omics"],
    "DNA/RNA": ["dna", "rna", "mrna", "mirna", "non-coding rna", "noncoding rna"],
    "sequencing": ["sequencing", "sequence data", "sequence analysis"],
    "CRISPR/gene editing": ["crispr", "gene editing", "genome editing"],
    "protein/peptide": ["protein", "proteins", "peptide", "peptides"],
    "enzyme": ["enzyme", "enzymes", "enzymatic"],
    "receptor": ["receptor", "receptors"],
    "antibody/antigen": ["antibody", "antibodies", "antigen", "antigens"],
    "immune molecules/cells": ["cytokine", "cytokines", "chemokine", "chemokines", "t-cell", "t cells", "b-cell", "b cells"],
    "microbiome": ["microbiome", "microbiomes", "microbiota"],
    "microbial/pathogen": ["bacteria", "bacterial", "bacterium", "virus", "viral", "viruses", "pathogen", "pathogens", "fungal", "fungi"],
    "organoid": ["organoid", "organoids"],
    "stem cell": ["stem cell", "stem cells"],
    "biomarker": ["biomarker", "biomarkers"],
    "molecular biology": ["molecular biology", "molecular mechanism", "molecular mechanisms", "molecular pathway", "molecular pathways", "molecular profiling"],
    "biochemistry": ["biochemistry", "biochemical"],
    "systems biology": ["systems biology"],
    "synthetic biology": ["synthetic biology"],
    "structural biology": ["structural biology", "protein structure", "protein structures"],
    "bioinformatics": ["bioinformatics", "computational biology"],
    "molecular diagnostics": ["molecular diagnostic", "molecular diagnostics"],
}

# Broader life-science terminology is retained as a review signal but is not
# sufficient by itself for the headline molecular/life-science classification.
MLS_REVIEW_TEXT = {
    "cell biology": ["cell biology", "cellular biology"],
    "cells": ["cells", "cellular"],
    "immunology": ["immunology", "immunological", "immune response", "immune system"],
    "physiology": ["physiology", "physiological"],
    "microbiology": ["microbiology", "microbiological"],
    "neuroscience": ["neuroscience", "neuroscientific", "neural circuit", "neural circuits"],
    "developmental biology": ["developmental biology", "embryonic", "embryogenesis"],
    "evolution": ["evolutionary biology", "evolutionary", "phylogeny", "phylogenetic"],
    "ecology": ["ecology", "ecological", "biodiversity", "ecosystem", "ecosystems"],
    "plant biology": ["plant biology", "plant physiology", "crop", "crops"],
    "animal biology": ["zoology", "animal biology", "livestock"],
    "marine biology": ["marine biology", "marine organism", "marine organisms"],
    "disease mechanism": ["disease mechanism", "disease mechanisms", "pathogenesis"],
    "molecular": ["molecular"],
}

MLS_FOR_DIRECT = [
    "biochemistry", "cell biology", "genetics", "genomics", "microbiology", "immunology",
    "biotechnology", "bioinformatics", "computational biology", "medical microbiology",
    "medical biochemistry", "metabolomics", "molecular medicine", "molecular biology",
    "medicinal and biomolecular chemistry", "biological sciences", "ecology",
    "evolutionary biology", "plant biology", "zoology", "animal science", "agricultur",
    "veterinary", "marine biology", "environmental biology", "physiology", "neuroscience",
    "neurosciences",
]

MLS_FOR_CLINICAL_CONTEXT = [
    "oncology", "carcinogenesis", "pathology", "pharmacology", "clinical science",
    "cardiovascular", "haematology", "hematology", "respiratory", "infectious", "endocrin",
    "reproductive medicine", "paediatrics", "pediatrics", "ophthalmology", "nutrition",
]

MLS_FALSE_CONTEXT = [
    "solar cell", "solar cells", "fuel cell", "fuel cells", "battery cell", "battery cells",
    "electrochemical cell", "electrochemical cells", "photovoltaic cell", "photovoltaic cells",
    "genetic algorithm", "genetic algorithms", "molecular dynamics", "molecular electronics",
    "molecular material", "molecular materials", "molecular beam", "molecular simulation",
]


def clean(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def norm_text(*values: object) -> str:
    text = " | ".join(clean(v) for v in values if clean(v))
    text = re.sub(r"[^a-z0-9+_-]+", " ", text.lower())
    return f" {re.sub(r'\s+', ' ', text).strip()} "


def term_hits(text: str, groups: dict[str, list[str]]) -> list[str]:
    out = []
    for label, terms in groups.items():
        if any(f" {t.strip()} " in text for t in terms):
            out.append(label)
    return out


def substring_hits(text: str, terms: list[str]) -> list[str]:
    return [t for t in terms if t in text]


def classify_ai(title: str, summary: str, keywords: str, for_text: str) -> dict[str, object]:
    raw = " | ".join(clean(v) for v in (title, summary, keywords) if clean(v))
    text = norm_text(title, summary, keywords)
    strong = term_hits(text, AI_EXPLICIT)
    review = term_hits(text, AI_REVIEW)
    for_hits = substring_hits(norm_text(for_text), AI_FOR)
    acronyms = sorted(set(AI_ACRONYM_RE.findall(raw)))
    if acronyms:
        strong.append("AI/ML acronym")

    if any(x in text for x in [" bioinformatics ", " computational biology "]) and any(
        x in text for x in [" predict", " classifier ", " classification ", " learning algorithm ", " data-driven ", " algorithm "]
    ):
        review.append("bioinformatics + predictive/algorithmic language")

    biological_neural = (
        strong == ["neural network"]
        and any(x in norm_text(for_text) for x in ["neuroscience", "neurosciences", "central nervous system"])
        and not any(x in text for x in ["machine learning", "deep learning", "algorithm", "classifier", "computational", "artificial intelligence"])
    )
    if biological_neural:
        strong = []
        review.append("neural network (biological ambiguity)")

    if for_hits or strong:
        status = "yes"
    elif review:
        status = "review"
    else:
        status = "no"

    reasons = [f"FoR:{x}" for x in for_hits] + [f"explicit:{x}" for x in strong] + [f"review:{x}" for x in review]
    return {
        "ai_status": status,
        "ai": status == "yes",
        "ai_candidate": status in {"yes", "review"},
        "ai_review_required": status == "review",
        "ai_for_hits": "; ".join(for_hits),
        "ai_explicit_hits": "; ".join(strong),
        "ai_review_hits": "; ".join(review),
        "ai_reason": "; ".join(reasons),
    }


def classify_mls(title: str, summary: str, keywords: str, for_text: str, broad_area: str) -> dict[str, object]:
    text = norm_text(title, summary, keywords)
    domain = norm_text(for_text, broad_area)
    explicit = term_hits(text, MLS_EXPLICIT_TEXT)
    review = term_hits(text, MLS_REVIEW_TEXT)
    for_hits = substring_hits(domain, MLS_FOR_DIRECT)
    clinical_hits = substring_hits(domain, MLS_FOR_CLINICAL_CONTEXT)
    false_hits = substring_hits(text, MLS_FALSE_CONTEXT)

    if false_hits:
        if any(x in text for x in [" genetic algorithm ", " genetic algorithms "]):
            explicit = [x for x in explicit if x != "genetics"]
        if any(x in text for x in [" molecular dynamics ", " molecular electronics ", " molecular material ", " molecular materials ", " molecular beam ", " molecular simulation "]):
            review = [x for x in review if x != "molecular"]
        if any(x in text for x in [" solar cell ", " fuel cell ", " battery cell ", " electrochemical cell ", " photovoltaic cell "]):
            review = [x for x in review if x != "cells"]

    if for_hits or explicit:
        status = "yes"
    elif review:
        status = "review"
    else:
        status = "no"

    reasons = [f"FoR:{x}" for x in for_hits] + [f"explicit:{x}" for x in explicit] + [f"review:{x}" for x in review]
    if clinical_hits:
        reasons += [f"clinical-context:{x}" for x in clinical_hits]
    if false_hits:
        reasons += [f"false-positive-guard:{x}" for x in false_hits]

    return {
        "mls_status": status,
        "molecular_life_science": status == "yes",
        "mls_review_required": status == "review",
        "mls_for_hits": "; ".join(for_hits),
        "mls_explicit_hits": "; ".join(explicit),
        "mls_review_hits": "; ".join(review),
        "mls_clinical_context_hits": "; ".join(clinical_hits),
        "mls_false_context_hits": "; ".join(false_hits),
        "mls_reason": "; ".join(reasons),
    }


def normalise_arc(path: Path) -> pd.DataFrame:
    x = pd.read_csv(path, low_memory=False)
    out = pd.DataFrame({
        "source": "ARC",
        "source_record_id": x["code"].fillna(""),
        "source_locator": x["code"].fillna(""),
        "analysis_include": ~x["grant-status"].fillna("").eq("Declined"),
        "analysis_year": pd.to_numeric(x["funding-commencement-year"], errors="coerce").astype("Int64"),
        "analysis_year_basis": "funding commencement year",
        "scheme": x["scheme-name"].fillna(""),
        "institution": x["current-admin-organisation"].fillna(x["announcement-admin-organisation"]).fillna(""),
        "award_value": pd.to_numeric(x["announced-funding-amount"], errors="coerce"),
        "status": x["grant-status"].fillna(""),
        "title": x["grant-summary"].fillna("").str.split(". ", n=1, regex=False).str[0],
        "summary": x["grant-summary"].fillna(""),
        "keywords": "",
        "for_text": x["primary-field-of-research"].fillna(""),
        "broad_area": "",
        "supplementary_text": x["national-interest-test-statement"].fillna(""),
    })
    return out


def normalise_nhmrc(path: Path) -> pd.DataFrame:
    x = pd.read_csv(path, low_memory=False)
    return pd.DataFrame({
        "source": "NHMRC",
        "source_record_id": x["award_record_id"].fillna(""),
        "source_locator": x["source_file"].fillna("") + ":" + x["source_row"].fillna("").astype(str),
        "analysis_include": x["analysis_include"].astype(str).str.lower().eq("true"),
        "analysis_year": pd.to_numeric(x["source_year"], errors="coerce").astype("Int64"),
        "analysis_year_basis": "published application-round/source year",
        "scheme": x["funding_scheme"].fillna(""),
        "institution": x["administering_institution"].fillna(""),
        "award_value": pd.to_numeric(x["total_amount_awarded"], errors="coerce"),
        "status": "",
        "title": x["title"].fillna(""),
        "summary": x["description"].fillna(""),
        "keywords": x["research_keywords"].fillna("") + " | " + x["health_keywords"].fillna(""),
        "for_text": x["fields_of_research"].fillna("") + " | " + x["for_category"].fillna(""),
        "broad_area": x["broad_research_area"].fillna(""),
        "supplementary_text": x["grant_opportunity"].fillna("") + " | " + x["sub_type"].fillna(""),
    })


def normalise_mrff(path: Path) -> pd.DataFrame:
    x = pd.read_excel(path, sheet_name="Grants List")
    x = x[x["Project Name"].notna()].copy()
    start = pd.to_datetime(x["Contract Start Date"], errors="coerce")
    return pd.DataFrame({
        "source": "MRFF",
        "source_record_id": x["Grant ID"].fillna(""),
        "source_locator": "Grants List row " + (x.index + 2).astype(str),
        "analysis_include": True,
        "analysis_year": start.dt.year.astype("Int64"),
        "analysis_year_basis": "contract start year",
        "scheme": x["Grant Opportunity"].fillna(""),
        "institution": x["Organisation"].fillna(""),
        "award_value": pd.to_numeric(x["Total Grant Value"], errors="coerce"),
        "status": "",
        "title": x["Project Name"].fillna(""),
        "summary": x["Project Summary"].fillna(""),
        "keywords": "",
        "for_text": x["Field(s) of Research\n(DIVISION / Group / Field)"].fillna(""),
        "broad_area": x["Broad Research Area"].fillna(""),
        "supplementary_text": x["MRFF Initiative"].fillna(""),
    })


def classify_frame(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in df[["title", "summary", "keywords", "for_text", "broad_area"]].itertuples(index=False, name=None):
        rows.append({**classify_mls(*r), **classify_ai(r[0], r[1], r[2], r[3])})
    out = pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
    out["ai_mls"] = out["ai"] & out["molecular_life_science"]
    out["review_status"] = "auto_classified"
    out.loc[out["ai_review_required"] & out["mls_review_required"], "review_status"] = "AI and MLS review required"
    out.loc[out["ai_review_required"] & ~out["mls_review_required"], "review_status"] = "AI review required"
    out.loc[~out["ai_review_required"] & out["mls_review_required"], "review_status"] = "MLS review required"
    out["manual_ai_decision"] = ""
    out["manual_mls_decision"] = ""
    out["review_notes"] = ""
    return out


def safe_div(num: float, den: float) -> float:
    return float(num / den) if pd.notna(num) and pd.notna(den) and den != 0 else 0.0


def summary_rows(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sources = ["ARC", "NHMRC", "MRFF", "COMBINED"]
    years = list(range(START_YEAR, END_YEAR + 1)) + ["2022-2025"]
    for source in sources:
        source_data = data if source == "COMBINED" else data[data["source"] == source]
        for year in years:
            g = source_data if year == "2022-2025" else source_data[source_data["analysis_year"] == year]
            ai = g[g["ai"]]
            mls = g[g["molecular_life_science"]]
            both = g[g["ai_mls"]]
            total_count = len(g)
            total_funding = g["award_value"].sum(min_count=1)
            ai_count, mls_count, both_count = len(ai), len(mls), len(both)
            ai_funding = ai["award_value"].sum(min_count=1)
            mls_funding = mls["award_value"].sum(min_count=1)
            both_funding = both["award_value"].sum(min_count=1)
            headline = safe_div(both_funding, ai_funding) if source == "ARC" else (safe_div(both_funding, total_funding) if source in {"NHMRC", "MRFF"} else float("nan"))
            rows.append({
                "source": source,
                "year": year,
                "total_grant_count": total_count,
                "total_funding": total_funding,
                "ai_grant_count": ai_count,
                "ai_funding": ai_funding,
                "mls_grant_count": mls_count,
                "mls_funding": mls_funding,
                "ai_mls_grant_count": both_count,
                "ai_mls_funding": both_funding,
                "ai_mls_share_all_grants": safe_div(both_count, total_count),
                "ai_mls_share_ai_grants": safe_div(both_count, ai_count),
                "ai_mls_share_mls_grants": safe_div(both_count, mls_count),
                "ai_mls_share_all_funding": safe_div(both_funding, total_funding),
                "ai_mls_share_ai_funding": safe_div(both_funding, ai_funding),
                "ai_mls_share_mls_funding": safe_div(both_funding, mls_funding),
                "ai_share_all_funding": safe_div(ai_funding, total_funding),
                "mls_share_all_funding": safe_div(mls_funding, total_funding),
                "headline_funding_proportion": headline,
                "headline_denominator": "AI funding" if source == "ARC" else ("all funding" if source in {"NHMRC", "MRFF"} else "not defined for combined"),
                "review_required_count": int((g["review_status"] != "auto_classified").sum()),
            })
    return pd.DataFrame(rows)

def build_terms_table() -> dict[str, pd.DataFrame]:
    def groups_df(groups: dict[str, list[str]], role: str) -> pd.DataFrame:
        return pd.DataFrame([
            {"group": group, "term": term, "role": role}
            for group, terms in groups.items() for term in terms
        ])

    sheets = {
        "AI explicit terms": groups_df(AI_EXPLICIT, "Counts as AI unless an explicit ambiguity rule applies"),
        "AI review terms": groups_df(AI_REVIEW, "Retrieval/review only; not counted as AI until adjudicated"),
        "AI FoR": pd.DataFrame({"FoR text substring": AI_FOR, "role": "Counts as AI"}),
        "AI acronyms": pd.DataFrame({"exact uppercase token": ["AI", "LLM", "LLMs", "CNN", "CNNs", "GNN", "GNNs", "NLP", "SVM", "SVMs", "GAN", "GANs"], "role": "Counts as explicit AI/ML evidence"}),
        "AI combined review rule": pd.DataFrame({"component": ["domain term", "domain term", "secondary term", "secondary term", "secondary term", "secondary term", "secondary term", "secondary term"], "term": ["bioinformatics", "computational biology", "predict*", "classifier", "classification", "learning algorithm", "data-driven", "algorithm"], "role": ["Requires one secondary term", "Requires one secondary term", "With either domain term -> review", "With either domain term -> review", "With either domain term -> review", "With either domain term -> review", "With either domain term -> review", "With either domain term -> review"]}),
        "MLS explicit terms": groups_df(MLS_EXPLICIT_TEXT, "Counts as molecular/related life science"),
        "MLS review terms": groups_df(MLS_REVIEW_TEXT, "Broader life-science retrieval/review signal; not counted by itself"),
        "MLS FoR": pd.DataFrame({"FoR text substring": MLS_FOR_DIRECT, "role": "Counts as molecular/related life science"}),
        "Clinical FoR context": pd.DataFrame({"FoR text substring": MLS_FOR_CLINICAL_CONTEXT, "role": "Context only; does not classify by itself"}),
        "False-positive guards": pd.DataFrame({"term": MLS_FALSE_CONTEXT, "role": "Prevents generic genetic/molecular/cell wording from creating obvious non-life-science matches"}),
    }
    return sheets


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def style_workbook(path: Path, freeze: bool = True) -> None:
    wb = load_workbook(path)
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        if ws.max_row >= 1:
            for c in ws[1]:
                c.font = Font(name="Arial", bold=True, color="FFFFFF")
                c.fill = PatternFill("solid", fgColor="1F4E78")
                c.alignment = Alignment(vertical="center", wrap_text=True)
            if freeze:
                ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
        if ws.max_row <= 1000:
            for row in ws.iter_rows(min_row=2):
                for c in row:
                    c.font = Font(name="Arial", size=10)
                    c.alignment = Alignment(vertical="top", wrap_text=True)
        for col in range(1, ws.max_column + 1):
            header = str(ws.cell(1, col).value or "")
            width = 16
            if header in {"title", "summary", "keywords", "for_text", "mls_reason", "ai_reason", "review_notes"}:
                width = 45
            elif header in {"source_record_id", "source_locator", "scheme", "institution"}:
                width = 28
            elif "funding" in header or "award_value" in header:
                width = 18
            ws.column_dimensions[get_column_letter(col)].width = min(width, 55)
    wb.save(path)


def write_summary_workbook(path: Path, classified: pd.DataFrame) -> None:
    aggregate = summary_rows(classified)
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    headers = [
        "source", "year", "total_grant_count", "total_funding", "ai_grant_count", "ai_funding",
        "mls_grant_count", "mls_funding", "ai_mls_grant_count", "ai_mls_funding",
        "AI+MLS % all grants", "AI+MLS % AI grants", "AI+MLS % MLS grants",
        "AI+MLS % all funding", "AI+MLS % AI funding", "AI+MLS % MLS funding",
        "AI % all funding", "MLS % all funding", "headline funding proportion", "headline denominator",
        "review_required_count",
    ]
    ws.append(headers)

    agg_ws = wb.create_sheet("Aggregates")
    aggregate_cols = [
        "source", "year", "total_grant_count", "total_funding", "ai_grant_count", "ai_funding",
        "mls_grant_count", "mls_funding", "ai_mls_grant_count", "ai_mls_funding", "review_required_count",
    ]
    agg_ws.append(aggregate_cols)
    for row in aggregate[aggregate_cols].itertuples(index=False, name=None):
        agg_ws.append(list(row))

    for i, row in enumerate(aggregate.itertuples(index=False), start=2):
        ws.append([row.source, row.year])
        # Link base counts/dollars to the hidden aggregate sheet, then derive all proportions with formulas.
        for c in range(3, 11):
            ws.cell(i, c, f"=Aggregates!{get_column_letter(c)}{i}")
        ws.cell(i, 11, f"=IFERROR(I{i}/C{i},0)")
        ws.cell(i, 12, f"=IFERROR(I{i}/E{i},0)")
        ws.cell(i, 13, f"=IFERROR(I{i}/G{i},0)")
        ws.cell(i, 14, f"=IFERROR(J{i}/D{i},0)")
        ws.cell(i, 15, f"=IFERROR(J{i}/F{i},0)")
        ws.cell(i, 16, f"=IFERROR(J{i}/H{i},0)")
        ws.cell(i, 17, f"=IFERROR(F{i}/D{i},0)")
        ws.cell(i, 18, f"=IFERROR(H{i}/D{i},0)")
        ws.cell(i, 19, f'=IF(A{i}="COMBINED","",IF(A{i}="ARC",O{i},N{i}))')
        ws.cell(i, 20, row.headline_denominator)
        ws.cell(i, 21, f"=Aggregates!K{i}")

    headline = wb.create_sheet("Headline", 0)
    headline.append(["source", "year", "AI+MLS grant count", "AI+MLS funding", "headline denominator", "denominator funding", "headline funding proportion"])
    summary_row = 2
    for _, row in aggregate.iterrows():
        if row["source"] == "COMBINED":
            summary_row += 1
            continue
        out_r = headline.max_row + 1
        headline.cell(out_r, 1, f"=Summary!A{summary_row}")
        headline.cell(out_r, 2, f"=Summary!B{summary_row}")
        headline.cell(out_r, 3, f"=Summary!I{summary_row}")
        headline.cell(out_r, 4, f"=Summary!J{summary_row}")
        headline.cell(out_r, 5, row["headline_denominator"])
        headline.cell(out_r, 6, f"=Summary!F{summary_row}" if row["source"] == "ARC" else f"=Summary!D{summary_row}")
        headline.cell(out_r, 7, f"=Summary!S{summary_row}")
        summary_row += 1

    notes = wb.create_sheet("Notes")
    notes.append(["Item", "Definition"])
    for item, definition in [
        ("Period", "2022-2025 inclusive."),
        ("ARC headline proportion", "AI + molecular/life-science funding divided by all ARC AI funding."),
        ("NHMRC/MRFF headline proportion", "AI + molecular/life-science funding divided by all grant funding for that funder."),
        ("AI review records", "Review-only AI candidates are excluded from headline AI totals unless manually adjudicated and the analysis is rerun."),
        ("MLS review records", "Records with one generic biological signal in a clinical FoR are flagged for review and excluded from headline molecular/life-science totals."),
        ("ARC year", "Funding commencement year."),
        ("NHMRC year", "Published application-round/source year."),
        ("MRFF year", "Contract start year."),
        ("Aggregates sheet", "Hidden sheet containing the pandas-generated yearly counts and dollar totals. Visible proportions are Excel formulas."),
    ]:
        notes.append([item, definition])

    agg_ws.sheet_state = "hidden"
    wb.save(path)
    style_workbook(path)
    wb = load_workbook(path)
    ws = wb["Summary"]
    for r in range(2, ws.max_row + 1):
        for c in [4, 6, 8, 10]:
            ws.cell(r, c).number_format = '$#,##0;[Red]($#,##0);-'
        for c in range(11, 20):
            ws.cell(r, c).number_format = '0.0%'
    headline = wb["Headline"]
    for sheet in [headline, ws]:
        sheet.page_setup.orientation = "landscape"
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0
        sheet.sheet_properties.pageSetUpPr.fitToPage = True
    for r in range(2, headline.max_row + 1):
        headline.cell(r, 4).number_format = '$#,##0;[Red]($#,##0);-'
        headline.cell(r, 6).number_format = '$#,##0;[Red]($#,##0);-'
        headline.cell(r, 7).number_format = '0.0%'
    wb.save(path)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arc", type=Path, required=True)
    ap.add_argument("--nhmrc", type=Path, required=True)
    ap.add_argument("--mrff", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    frames = [normalise_arc(args.arc), normalise_nhmrc(args.nhmrc), normalise_mrff(args.mrff)]
    classified = classify_frame(pd.concat(frames, ignore_index=True))
    classified = classified[
        classified["analysis_include"]
        & classified["analysis_year"].between(START_YEAR, END_YEAR, inclusive="both")
    ].copy()
    classified = classified.sort_values(["source", "analysis_year", "source_record_id"]).reset_index(drop=True)

    # Flat, machine-readable files.
    classified.to_csv(args.outdir / "all_grants_classified_2022_2025.csv", index=False)
    summary = summary_rows(classified)
    summary.to_csv(args.outdir / "summary_results_2022_2025.csv", index=False)

    # Classified grant workbook.
    grants_xlsx = args.outdir / "all_grants_classified_2022_2025.xlsx"
    with pd.ExcelWriter(grants_xlsx, engine="openpyxl") as writer:
        classified.to_excel(writer, sheet_name="All grants", index=False)
        classified[classified["review_status"] != "auto_classified"].to_excel(writer, sheet_name="Review queue", index=False)
    style_workbook(grants_xlsx)

    # Separate review queue for convenient hand review.
    review = classified[classified["review_status"] != "auto_classified"].copy()
    review_xlsx = args.outdir / "review_queue_2022_2025.xlsx"
    with pd.ExcelWriter(review_xlsx, engine="openpyxl") as writer:
        review.to_excel(writer, sheet_name="Review queue", index=False)
    style_workbook(review_xlsx)

    # Exact term/FoR dictionary workbook.
    terms_xlsx = args.outdir / "terms_and_for_2022_2025.xlsx"
    with pd.ExcelWriter(terms_xlsx, engine="openpyxl") as writer:
        for sheet, table in build_terms_table().items():
            table.to_excel(writer, sheet_name=sheet[:31], index=False)
    style_workbook(terms_xlsx)

    # Summary workbook with formula-driven proportions from a hidden classified-data sheet.
    write_summary_workbook(args.outdir / "summary_results_2022_2025.xlsx", classified)

    # Review-stratified validation sample including negatives to detect missed candidates.
    validation_parts = []
    for source in ["ARC", "NHMRC", "MRFF"]:
        d = classified[classified["source"] == source]
        strata = {
            "AI+MLS positive": d[d["ai_mls"]],
            "AI review": d[d["ai_status"] == "review"],
            "MLS review": d[d["mls_status"] == "review"],
            "AI yes / MLS no": d[d["ai"] & ~d["molecular_life_science"]],
            "MLS yes / AI no": d[d["molecular_life_science"] & ~d["ai"]],
            "negative": d[(d["ai_status"] == "no") & (d["mls_status"] == "no")],
        }
        for stratum, pool in strata.items():
            if len(pool):
                s = pool.sample(min(15, len(pool)), random_state=42).copy()
                s.insert(0, "validation_stratum", stratum)
                validation_parts.append(s)
    validation = pd.concat(validation_parts, ignore_index=True)
    validation.to_excel(args.outdir / "validation_sample_2022_2025.xlsx", index=False)
    style_workbook(args.outdir / "validation_sample_2022_2025.xlsx")

    manifest = pd.DataFrame([
        {"source": "ARC", "filename": args.arc.name, "sha256": sha256(args.arc), "bytes": args.arc.stat().st_size, "year_field": "funding-commencement-year", "funding_field": "announced-funding-amount"},
        {"source": "NHMRC", "filename": args.nhmrc.name, "sha256": sha256(args.nhmrc), "bytes": args.nhmrc.stat().st_size, "year_field": "source_year", "funding_field": "total_amount_awarded"},
        {"source": "MRFF", "filename": args.mrff.name, "sha256": sha256(args.mrff), "bytes": args.mrff.stat().st_size, "year_field": "Contract Start Date -> year", "funding_field": "Total Grant Value"},
    ])
    manifest.to_csv(args.outdir / "source_manifest.csv", index=False)

    print(summary.to_string(index=False))
    print("\nClassification counts:")
    print(classified.groupby(["source", "ai_status", "mls_status"]).size().to_string())


if __name__ == "__main__":
    main()
