from enum import Enum
from pydantic import BaseModel, Field, RootModel
from typing import List, Optional


class AnnotationType(Enum):
    """Enum for annotation types"""
    MUTAGEN = "MUTAGEN"


class ConfidenceType(Enum):
    pLDDT = "pLDDT"
    QMEANDisCo = "QMEANDisCo"


class EnsembleSampleFormat(str, Enum):
    PDB = "PDB"
    MMCIF = "MMCIF"
    BCIF = "BCIF"


class IdentifierCategory(str, Enum):
    UNIPROT = "UNIPROT"
    RFAM = "RFAM"
    CCD = "CCD"
    SMILES = "SMILES"
    INCHI = "INCHI"
    INCHIKEY = "INCHIKEY"


class EntityType(str, Enum):
    BRANCHED = "BRANCHED"
    MACROLIDE = "MACROLIDE"
    NON_POLYMER = "NON-POLYMER"
    POLYMER = "POLYMER"
    WATER = "WATER"


class EntityPolyType(str, Enum):
    CYCLIC_PSEUDO_PEPTIDE = "CYCLIC-PSEUDO-PEPTIDE"
    PEPTIDE_NUCLEIC_ACID = "PEPTIDE NUCLEIC ACID"
    POLYDEOXYRIBONUCLEOTIDE = "POLYDEOXYRIBONUCLEOTIDE"
    POLYDEOXYRIBONUCLEOTIDE_POLYRIBONUCLEOTIDE_HYBRID = "POLYDEOXYRIBONUCLEOTIDE/POLYRIBONUCLEOTIDE HYBRID"
    POLYPEPTIDE_D = "POLYPEPTIDE(D)"
    POLYPEPTIDE_L = "POLYPEPTIDE(L)"
    POLYRIBONUCLEOTIDE = "POLYRIBONUCLEOTIDE"
    OTHER = "OTHER"


class Evidence(str, Enum):
    COMPUTATIONAL_PREDICTED = "COMPUTATIONAL/PREDICTED"


class ExperimentalMethod(str, Enum):
    ELECTRON_CRYSTALLOGRAPHY = "ELECTRON CRYSTALLOGRAPHY"
    ELECTRON_MICROSCOPY = "ELECTRON MICROSCOPY"
    EPR = "EPR"
    FIBER_DIFFRACTION = "FIBER DIFFRACTION"
    FLUORESCENCE_TRANSFER = "FLUORESCENCE TRANSFER"
    INFRARED_SPECTROSCOPY = "INFRARED SPECTROSCOPY"
    NEUTRON_DIFFRACTION = "NEUTRON DIFFRACTION"
    X_RAY_POWDER_DIFFRACTION = "X-RAY POWDER DIFFRACTION"
    SOLID_STATE_NMR = "SOLID-STATE NMR"
    SOLUTION_NMR = "SOLUTION NMR"
    X_RAY_SOLUTION_SCATTERING = "X-RAY SOLUTION SCATTERING"
    THEORETICAL_MODEL = "THEORETICAL MODEL"
    X_RAY_DIFFRACTION = "X-RAY DIFFRACTION"
    HYBRID = "HYBRID"


class ModelFormat(str, Enum):
    PDB = "PDB"
    MMCIF = "MMCIF"
    BCIF = "BCIF"


class ModelType(str, Enum):
    ATOMIC = "ATOMIC"
    DUMMY = "DUMMY"
    MIX = "MIX"


class OligomericState(str, Enum):
    MONOMER = "MONOMER"
    HOMODIMER = "HOMODIMER"
    HETERODIMER = "HETERODIMER"
    HOMO_OLIGOMER = "HOMO-OLIGOMER"
    HETERO_OLIGOMER = "HETERO-OLIGOMER"


class ModelCategory(str, Enum):
    EXPERIMENTALLY_DETERMINED = "EXPERIMENTALLY DETERMINED"
    TEMPLATE_BASED = "TEMPLATE-BASED"
    AB_INITIO = "AB-INITIO"
    CONFORMATIONAL_ENSEMBLE = "CONFORMATIONAL ENSEMBLE"


# AlphaFold Prediction Models
class EntrySummary(BaseModel):
    """Schema for AlphaFold prediction response"""
    entryId: str = Field(..., description="Unique identifier for the entry")
    gene: Optional[str] = Field(None, description="Gene associated with the entry")
    sequenceChecksum: Optional[str] = Field(None, description="Checksum of the sequence")
    sequenceVersionDate: Optional[str] = Field(None, description="Date of the sequence version")
    uniprotAccession: str = Field(..., description="UniProt accession number")
    uniprotId: str = Field(..., description="UniProt ID")
    uniprotDescription: str = Field(..., description="Description of the UniProt entry")
    taxId: int = Field(..., description="Taxonomy ID")
    organismScientificName: str = Field(..., description="Scientific name of the organism")
    uniprotStart: int = Field(..., description="Start position in UniProt")
    uniprotEnd: int = Field(..., description="End position in UniProt")
    uniprotSequence: str = Field(..., description="Sequence from UniProt")
    modelCreatedDate: str = Field(..., description="Date the model was created")
    latestVersion: int = Field(..., description="Current version of the model")
    allVersions: List[int] = Field(..., description="List of all versions for the model")
    bcifUrl: str = Field(..., description="URL for BCIF format")
    cifUrl: str = Field(..., description="URL for CIF format")
    pdbUrl: str = Field(..., description="URL for PDB format")
    paeImageUrl: str = Field(..., description="URL for PAE image")
    paeDocUrl: str = Field(..., description="URL for PAE documentation")
    amAnnotationsUrl: Optional[str] = Field(None, description="URL for AM annotations")
    amAnnotationsHg19Url: Optional[str] = Field(None, description="URL for AM annotations (Hg19)")
    amAnnotationsHg38Url: Optional[str] = Field(None, description="URL for AM annotations (Hg38)")
    isReviewed: Optional[bool] = Field(None, description="Indicates if the model is reviewed")
    isReferenceProteome: Optional[bool] = Field(None, description="Indicates if the model is part of the reference proteome")
    

class EntrySummaryResponse(RootModel):
    root: List[EntrySummary]


# UniProt Summary Models
class UniprotEntry(BaseModel):
    """Schema for UniProt entry in the response"""
    ac: str = Field(..., description="UniProt accession")
    id: Optional[str] = Field(None, description="UniProt identifier")
    uniprot_checksum: Optional[str] = Field(None, description="CRC64 checksum of the UniProt sequence")
    sequence_length: Optional[int] = Field(None, description="Length of the UniProt sequence")
    segment_start: Optional[int] = Field(None, description="1-indexed first residue of the UniProt sequence segment")
    segment_end: Optional[int] = Field(None, description="1-indexed last residue of the UniProt sequence segment")


class Entity(BaseModel):
    """Schema for entity in structure summary"""
    entity_type: EntityType = Field(..., description="Type of the entity")
    entity_poly_type: Optional[EntityPolyType] = Field(None, description="The type of the molecular entity; similar to _entity_poly.type in mmCIF")
    identifier: Optional[str] = Field(None, description="Identifier of the molecule")
    identifier_category: Optional[IdentifierCategory] = Field(None, description="Category of the identifier")
    description: str = Field(..., description="A textual label of the molecule")
    chain_ids: List[str] = Field(..., description="List of chain IDs associated with the entity")


class StructureSummary(BaseModel):
    """Schema for structure summary"""
    model_identifier: str = Field(..., description="Identifier of the model, such as PDB id")
    model_category: ModelCategory = Field(..., description="Category of the model")
    model_url: str = Field(..., description="URL of the model coordinates")
    model_format: ModelFormat = Field(..., description="Format of the model")
    model_type: Optional[ModelType] = Field(None, description="Defines if the coordinates are atomic-level or contains dummy atoms (e.g. SAXS models), or a mix of both (e.g. hybrid models)")
    model_page_url: Optional[str] = Field(None, description="URL of a web page of the data provider that show the model")
    provider: str = Field(..., description="Name of the model provider")
    number_of_conformers: Optional[float] = Field(None, description="The number of conformers in a conformational ensemble")
    ensemble_sample_url: Optional[str] = Field(None, description="URL of a sample of conformations from a conformational ensemble")
    ensemble_sample_format: Optional[EnsembleSampleFormat] = Field(None, description="File format of the sample coordinates, e.g. PDB.")
    created: str = Field(..., description="Date of release of model generation in the format of YYYY-MM-DD")
    sequence_identity: float = Field(..., description="Sequence identity in the range of [0,1] of the model to the UniProt sequence.")
    uniprot_start: int = Field(..., description="1-indexed first residue of the model according to UniProt sequence numbering")
    uniprot_end: int = Field(..., description="1-indexed last residue of the model according to UniProt sequence numbering")
    coverage: float = Field(..., description="Fraction in range of [0, 1] of the UniProt sequence covered by the model. This is calculated as (uniprot_end - uniprot_start + 1) / uniprot_sequence_length")
    experimental_method: Optional[ExperimentalMethod] = Field(None, description="Experimental method used to determine the structure, if applicable")
    resolution: Optional[float] = Field(None, description="The resolution of the model in Angstrom, if applicable")
    confidence_type: Optional[ConfidenceType] = Field(None, description="Type of the confidence measure. This is required for theoretical models.")
    confidence_version: Optional[str] = Field(None, description="Version of confidence measure software used to calculate quality. This is required for theoretical models.")
    confidence_avg_local_score: float = Field(..., description="Average of the confidence measures in the range of [0,1] for QMEANDisCo and [0,100] for pLDDT. Please contact 3D-Beacons developers if other estimates are to be added. This is required for theoretical models.")
    oligomeric_state: Optional[OligomericState] = Field(None, description="Oligomeric state of the model")
    preferred_assembly_id: Optional[str] = Field(None, description="Identifier of the preferred assembly in the model")
    entities: List[Entity] = Field(..., description="A list of molecular entities in the model")


class Structure(BaseModel):
    """Schema for structure in the response"""
    summary: StructureSummary


class UniprotSummaryResponse(BaseModel):
    """Schema for complete UniProt summary API response"""
    uniprot_entry: UniprotEntry = Field(..., description="UniProt entry data")
    structures: List[Structure] = Field(..., description="List of structures associated with the UniProt entry")


# Annotation Models
class Region(BaseModel):
    """Schema for annotation region"""
    start: int = Field(..., description="The first position of the sequence")
    end: int = Field(..., description="The last position of the sequence")
    annotation_value: Optional[List[float]] = Field(None, description="List of annotation scores")
    unit: Optional[str] = Field(None, description="Unit of measurement for annotation values")


class Annotation(BaseModel):
    """Schema for annotation"""
    type: AnnotationType = Field(..., description="Type of annotation (e.g., 'MUTAGEN')")
    description: str = Field(..., description="Description of the annotation")
    source_name: str = Field(..., description="Name of the source of the annotation")
    source_url: Optional[str] = Field(None, description="Optional URL to the source for more data")
    evidence: str = Field(..., description="Evidence type for the annotation")
    residues: Optional[List[int]] = Field(None, description="An array of residue indices")
    regions: Optional[List[Region]] = Field(None, description="Regions associated with the annotation")


class AnnotationResponse(BaseModel):
    """Schema for complete annotation response"""
    accession: str = Field(..., description="UniProt accession (e.g., 'Q5VSL9')")
    id: str = Field(..., description="UniProt ID (e.g., 'STRP1_HUMAN')")
    sequence: str = Field(..., description="Full protein sequence")
    annotation: List[Annotation] = Field(..., description="List of annotations")
