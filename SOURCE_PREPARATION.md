# Source preparation

The analysis runs directly from the merged ARC and NHMRC CSV files and the detailed MRFF grants workbook in `inputs/`.

`code/merge_arc_grants.py` and `code/merge_nhmrc_grants.py` are included for provenance and show how the merged ARC/NHMRC inputs were constructed from the original annual downloads. They are not required to reproduce the packaged analysis because the exact merged inputs are included.

The MRFF summary workbook is included as a reconciliation/supporting source but is not used for grant-level classification; the detailed MRFF grants workbook is the classification source.
