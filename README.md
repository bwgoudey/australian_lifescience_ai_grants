# Analysis of Australian AI and molecular life-science funding from NHMRC, MRFF and ARC grants

This package contains the complete reproducible analysis used to classify ARC, NHMRC and MRFF grants and analyses how Australian AI and molecular life-science have been funding in the past decade or so. 

## Main outputs

- `outputs/terms_and_for_2022_2025.xlsx` — exact AI/ML, molecular/life-science and FoR dictionaries used by the code.
- `outputs/all_grants_classified_2022_2025.xlsx` — all 8,292 included grants with source text, classification evidence and review status.
- `outputs/all_grants_classified_2022_2025.csv` — machine-readable equivalent.
- `outputs/summary_results_2022_2025.xlsx` — headline and complete yearly counts, dollar amounts and proportions. The visible proportion cells are formulas and the workbook has been recalculated/checked in LibreOffice.
- `outputs/summary_results_2022_2025.csv` — machine-readable summary including every proportion.
- `outputs/review_queue_2022_2025.xlsx` — all records requiring AI and/or molecular/life-science review.
- `outputs/validation_sample_2022_2025.xlsx` — stratified validation sample including negatives.

## Documentation

- `METHODOLOGY.md` — complete operational definitions, exact rule structure, denominators and limitations.
- `RESULTS.md` — compact headline and yearly results.
- `DATA_DICTIONARY.md` — classified-grant field definitions.
- `source_manifest.csv` — source filenames, SHA-256 hashes, year fields and funding fields.

## Code

`code/build_grant_analysis.py` contains the entire analysis. It uses pandas for ingestion, normalisation, classification and aggregation, and openpyxl only for workbook formatting/formulas.

To reproduce from the included source files:

```bash
bash code/run_analysis.sh
```

Python requirements are listed in `requirements.txt`.

## Scope

The analysis period is 2022–2025 inclusive. ARC uses funding commencement year, NHMRC uses source/application-round year, and MRFF uses contract start year. See `METHODOLOGY.md` before comparing annual figures across funders.

## Source preparation provenance

The exact merged inputs used for analysis are included under `inputs/`. `SOURCE_PREPARATION.md` and the two merge scripts document upstream ARC/NHMRC preparation; these are not needed to rerun the classification because the merged inputs are already packaged.

`run_analysis.sh` optionally opens/saves the summary workbook with LibreOffice when available so the Excel formula results are cached; this is not required for the CSV results or classifications.
