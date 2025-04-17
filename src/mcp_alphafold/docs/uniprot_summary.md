### `uniprot_summary_tool`

This tool fetches AlphaFold model predictions for a given UniProt residue range. The tool takes in a UniProt accession number (AC), entry name (ID), or CRC64 checksum and returns detailed information about the structure models available for the specified sequence range.

## Arguments
- **`qualifier`** (`str`):  
  UniProtKB accession number (AC), entry name (ID), or CRC64 checksum of the UniProt sequence (e.g., `'Q5VSL9'`).


### Example Input:
- **qualifier**: `Q5VSL9`

## Response Structure

The response includes detailed information about the UniProt entry and its associated AlphaFold models.

### Example Response:
```json
{
  "uniprot_entry": {
    "ac": "Q5VSL9",
    "id": "STRP1_HUMAN",
    "uniprot_checksum": "5F9BA1D4C7DE6925",
    "sequence_length": 837,
    "segment_start": 1,
    "segment_end": 837
  },
  "structures": [
    {
      "summary": {
        "model_identifier": "AF-Q5VSL9-F1",
        "model_category": "AB-INITIO",
        "model_url": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-model_v4.cif",
        "model_format": "MMCIF",
        "model_type": null,
        "model_page_url": "https://alphafold.ebi.ac.uk/entry/Q5VSL9",
        "provider": "AlphaFold DB",
        "number_of_conformers": null,
        "ensemble_sample_url": null,
        "ensemble_sample_format": null,
        "created": "2022-06-01",
        "sequence_identity": 1,
        "uniprot_start": 1,
        "uniprot_end": 837,
        "coverage": 1,
        "experimental_method": null,
        "resolution": null,
        "confidence_type": "pLDDT",
        "confidence_version": null,
        "confidence_avg_local_score": 80.82,
        "oligomeric_state": null,
        "preferred_assembly_id": null,
        "entities": [
          {
            "entity_type": "POLYMER",
            "entity_poly_type": "POLYPEPTIDE(L)",
            "identifier": "Q5VSL9",
            "identifier_category": "UNIPROT",
            "description": "Striatin-interacting protein 1",
            "chain_ids": [
              "A"
            ]
          }
        ]
      }
    }
  ]
}
```