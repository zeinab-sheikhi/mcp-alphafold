# `alpha_fold_prediction_tool`

This tool retrieves all available AlphaFold models for a specified UniProt accession. It allows querying by the UniProt accession or by the CRC64 checksum of the UniProt sequence.

## Arguments
- **`qualifier`** (`str`):
  UniProt accession (e.g., `'Q5VSL9'`).

- **`sequence_checksum`** (`str`, optional):
  CRC64 checksum of the UniProt sequence.

### Example Input:
- **qualifier**: `Q5VSL9`
- **sequence_checksum**: `5F9BA1D4C7DE6925`

## Response Structure

The response will be a list of objects, each containing detailed information about the available AlphaFold models.


### Example Output:

```json
[
  {
    "entryId": "AF-Q5VSL9-F1",
    "gene": "STRIP1",
    "sequenceChecksum": "5F9BA1D4C7DE6925",
    "sequenceVersionDate": "2004-12-07",
    "uniprotAccession": "Q5VSL9",
    "uniprotId": "STRP1_HUMAN",
    "uniprotDescription": "Striatin-interacting protein 1",
    "taxId": 9606,
    "organismScientificName": "Homo sapiens",
    "uniprotStart": 1,
    "uniprotEnd": 837,
    "uniprotSequence": "MEPAVGGPGPLIVNNKQPQPPPPPPPAAAQPPPGAPRAAAGLLPGGKAREFN...",
    "modelCreatedDate": "2022-06-01",
    "latestVersion": 4,
    "allVersions": [1, 2, 3, 4],
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-model_v4.bcif",
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-model_v4.cif",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-model_v4.pdb",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-predicted_aligned_error_v4.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-predicted_aligned_error_v4.json",
    "amAnnotationsUrl": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-aa-substitutions.csv",
    "amAnnotationsHg19Url": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-hg19.csv",
    "amAnnotationsHg38Url": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-hg38.csv",
    "isReviewed": true,
    "isReferenceProteome": true
  }
]
```
