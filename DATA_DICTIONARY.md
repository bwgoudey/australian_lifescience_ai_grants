# Classified-grants data dictionary

| Column | Meaning |
|---|---|
| `source` | ARC, NHMRC or MRFF. |
| `source_record_id` | Stable identifier used for the source record. |
| `source_locator` | Human-readable source locator. |
| `analysis_include` | Whether the source record is eligible for analysis before the 2022–2025 filter. |
| `analysis_year` | Year used for the analysis. |
| `analysis_year_basis` | Definition of the year for that funder. |
| `scheme` | Funding scheme or grant opportunity. |
| `institution` | Administering/recipient institution. |
| `award_value` | Nominal award value used in funding summaries. |
| `status` | Source grant status when available. |
| `title` | Normalised project/grant title. |
| `summary` | Project/grant summary used for classification. |
| `keywords` | Source keywords used for classification when available. |
| `for_text` | FoR text used for classification. |
| `broad_area` | Broad research area when available. |
| `supplementary_text` | Additional source context retained but not used by the simple classifier. |
| `mls_status` | yes/review/no molecular/related life-science classification. |
| `molecular_life_science` | Boolean headline molecular/life-science classification. |
| `mls_review_required` | Whether the MLS screen requires review. |
| `mls_for_hits` | Matching life-science FoR strings. |
| `mls_explicit_hits` | Matching explicit molecular/biological term groups. |
| `mls_review_hits` | Matching broader life-science review groups. |
| `mls_clinical_context_hits` | Matching clinical FoR context strings. |
| `mls_false_context_hits` | False-positive guard phrases encountered. |
| `mls_reason` | Semicolon-separated evidence for the MLS classification. |
| `ai_status` | yes/review/no AI classification. |
| `ai` | Boolean headline AI classification. |
| `ai_candidate` | True for yes or review AI records. |
| `ai_review_required` | Whether the AI screen requires review. |
| `ai_for_hits` | Matching AI FoR strings. |
| `ai_explicit_hits` | Matching explicit AI/ML term groups or acronym evidence. |
| `ai_review_hits` | Matching broader AI review groups. |
| `ai_reason` | Semicolon-separated evidence for the AI classification. |
| `ai_mls` | True when both headline AI and headline molecular/life-science classifications are true. |
| `review_status` | Combined review status. |
| `manual_ai_decision` | Blank field reserved for later human adjudication. |
| `manual_mls_decision` | Blank field reserved for later human adjudication. |
| `review_notes` | Blank field reserved for later human notes. |
