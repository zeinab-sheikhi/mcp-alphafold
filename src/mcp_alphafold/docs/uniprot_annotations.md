This tool retrieves all annotations for a specified UniProt residue range. It allows querying by the UniProt accession and the annotation type (e.g., MUTAGEN for AlphaMissense).

## Arguments

- **`qualifier`** (`str`):
  UniProt accession (e.g., `'Q5VSL9'`).

- **`annotation_type`** (`str`):
  Type of annotation (e.g., `'MUTAGEN'` for AlphaMissense).

### Example Input:
- **qualifier**: `Q5VSL9`
- **annotation_type**: `MUTAGEN`

## Response Structure

The response includes detailed information about the UniProt entry and its associated annotations.

### Example Output:

```json
{
  "accession": "Q5VSL9",
  "id": "STRP1_HUMAN",
  "sequence": "MEPAVGGPGPLIVNNKQPQPPPPPPPAAAQPPPGAPRAAAGLLPGGKAREFNRNQRKDSEGYSESPDLEFEYADTDKWAAELSELYSYTEGPEFLMNRKCFEEDFRIHVTDKKWTELDTNQHRTHAMRLLDGLEVTAREKRLKVARAILYVAQGTFGECSSEAEVQSWMRYNIFLLLEVGTFNALVELLNMEIDNSAACSSAVRKPAISLADSTDLRVLLNIMYLIVETVHQECEGDKAEWRTMRQTFRAELGSPLYNNEPFAIMLFGMVTKFCSGHAPHFPMKKVLLLLWKTVLCTLGGFEELQSMKAEKRSILGLPPLPEDSIKVIRNMRAASPPASASDLIEQQQKRGRREHKALIKQDNLDAFNERDPYKADDSREEEEENDDDNSLEGETFPLERDEVMPPPLQHPQTDRLTCPKGLPWAPKVREKDIEMFLESSRSKFIGYTLGSDTNTVVGLPRPIHESIKTLKQHKYTSIAEVQAQMEEEYLRSPLSGGEEEVEQVPAETLYQGLLPSLPQYMIALLKILLAAAPTSKAKTDSINILADVLPEEMPTTVLQSMKLGVDVNRHKEVIVKAISAVLLLLLKHFKLNHVYQFEYMAQHLVFANCIPLILKFFNQNIMSYITAKNSISVLDYPHCVVHELPELTAESLEAGDSNQFCWRNLFSCINLLRILNKLTKWKHSRTMMLVVFKSAPILKRALKVKQAMMQLYVLKLLKVQTKYLGRQWRKSNMKTMSAIYQKVRHRLNDDWAYGNDLDARPWDFQAEECALRANIERFNARRYDRAHSNPDFLPVDNCLQSVLGQRVDLPEDFQMNYDLWLEREVFSKPISWEELLQ",
  "annotation": [
    {
      "type": "MUTAGEN",
      "description": "AM score",
      "source_name": "AFDB",
      "source_url": "https://alphafold.ebi.ac.uk/files/AF-Q5VSL9-F1-aa-substitutions.csv",
      "evidence": "COMPUTATIONAL/PREDICTED",
      "residues": [1, 2, 3, ...],
      "regions": [
        {
          "start": 1,
          "end": 837,
          "annotation_value": [0.3234, 0.3281, ...],
          "unit": null
        }
      ]
    }
  ]
}
