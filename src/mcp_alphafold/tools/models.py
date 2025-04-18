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


class UniProtEvidence(BaseModel):
    evidenceCode: Optional[str]
    source: Optional[str]
    id: Optional[str]


class FullName(BaseModel):
    value: str
    evidences: Optional[List[UniProtEvidence]] = []


class RecommendedName(BaseModel):
    fullName: FullName


class AlternativeName(BaseModel):
    fullName: FullName


class ProteinDescription(BaseModel):
    recommendedName: Optional[RecommendedName]
    alternativeNames: Optional[List[AlternativeName]] = []
    flag: Optional[str]


class GeneName(BaseModel):
    value: str


class Gene(BaseModel):
    geneName: Optional[GeneName]


class Organism(BaseModel):
    scientificName: str


class CommentText(BaseModel):
    value: str
    evidences: Optional[List[UniProtEvidence]] = []


class Comment(BaseModel):
    commentType: str
    texts: List[CommentText]


class ExtraAttributes(BaseModel):
    uniParcId: Optional[str]


class UniProtEntryResponse(BaseModel):
    entryType: str
    primaryAccession: str
    proteinDescription: ProteinDescription
    comments: Optional[List[Comment]] = []
    features: Optional[List[dict]] = []
    extraAttributes: Optional[ExtraAttributes]


class UniProtSearchField(str, Enum):
    ABSORPTION = "absorption"
    ACCESSION = "accession"
    ANNOTATION_SCORE = "annotation_score"
    CC_ACTIVITY_REGULATION = "cc_activity_regulation"
    CC_ALLERGEN = "cc_allergen"
    CC_ALTERNATIVE_PRODUCTS = "cc_alternative_products"
    CC_BIOTECHNOLOGY = "cc_biotechnology"
    CC_CATALYTIC_ACTIVITY = "cc_catalytic_activity"
    CC_CAUTION = "cc_caution"
    CC_COFACTOR = "cc_cofactor"
    CC_DEVELOPMENTAL_STAGE = "cc_developmental_stage"
    CC_DISEASE = "cc_disease"
    CC_DISRUPTION_PHENOTYPE = "cc_disruption_phenotype"
    CC_DOMAIN = "cc_domain"
    CC_FUNCTION = "cc_function"
    CC_INDUCTION = "cc_induction"
    CC_INTERACTION = "cc_interaction"
    CC_MASS_SPECTROMETRY = "cc_mass_spectrometry"
    CC_MISCELLANEOUS = "cc_miscellaneous"
    CC_PATHWAY = "cc_pathway"
    CC_PHARMACEUTICAL = "cc_pharmaceutical"
    CC_POLYMORPHISM = "cc_polymorphism"
    CC_PTM = "cc_ptm"
    CC_RNA_EDITING = "cc_rna_editing"
    CC_SEQUENCE_CAUTION = "cc_sequence_caution"
    CC_SIMILARITY = "cc_similarity"
    CC_SUBCELLULAR_LOCATION = "cc_subcellular_location"
    CC_SUBUNIT = "cc_subunit"
    CC_TISSUE_SPECIFICITY = "cc_tissue_specificity"
    CC_TOXIC_DOSE = "cc_toxic_dose"
    COMMENT_COUNT = "comment_count"
    DATE_CREATED = "date_created"
    DATE_MODIFIED = "date_modified"
    DATE_SEQUENCE_MODIFIED = "date_sequence_modified"
    EC = "ec"
    ERROR_GMODEL_PRED = "error_gmodel_pred"
    FEATURE_COUNT = "feature_count"
    FRAGMENT = "fragment"
    FT_ACT_SITE = "ft_act_site"
    FT_BINDING = "ft_binding"
    FT_CARBOHYD = "ft_carbohyd"
    FT_CHAIN = "ft_chain"
    FT_COILED = "ft_coiled"
    FT_COMPBIAS = "ft_compbias"
    FT_CONFLICT = "ft_conflict"
    FT_CROSSLNK = "ft_crosslnk"
    FT_DISULFID = "ft_disulfid"
    FT_DNA_BIND = "ft_dna_bind"
    FT_DOMAIN = "ft_domain"
    FT_HELIX = "ft_helix"
    FT_INIT_MET = "ft_init_met"
    FT_INTRAMEM = "ft_intramem"
    FT_LIPID = "ft_lipid"
    FT_MOD_RES = "ft_mod_res"
    FT_MOTIF = "ft_motif"
    FT_MUTAGEN = "ft_mutagen"
    FT_NON_CONS = "ft_non_cons"
    FT_NON_STD = "ft_non_std"
    FT_NON_TER = "ft_non_ter"
    FT_PEPTIDE = "ft_peptide"
    FT_PROPEP = "ft_propep"
    FT_REGION = "ft_region"
    FT_REPEAT = "ft_repeat"
    FT_SIGNAL = "ft_signal"
    FT_SITE = "ft_site"
    FT_STRAND = "ft_strand"
    FT_TOPO_DOM = "ft_topo_dom"
    FT_TRANSIT = "ft_transit"
    FT_TRANSMEM = "ft_transmem"
    FT_TURN = "ft_turn"
    FT_UNSURE = "ft_unsure"
    FT_VAR_SEQ = "ft_var_seq"
    FT_VARIANT = "ft_variant"
    FT_ZN_FING = "ft_zn_fing"
    GENE_NAMES = "gene_names"
    GENE_OLN = "gene_oln"
    GENE_ORF = "gene_orf"
    GENE_PRIMARY = "gene_primary"
    GENE_SYNONYM = "gene_synonym"
    GO = "go"
    GO_C = "go_c"
    GO_F = "go_f"
    GO_ID = "go_id"
    GO_P = "go_p"
    ID = "id"
    KEYWORD = "keyword"
    KEYWORDID = "keywordid"
    KINETICS = "kinetics"
    LENGTH = "length"
    LINEAGE = "lineage"
    LINEAGE_IDS = "lineage_ids"
    LIT_DOI_ID = "lit_doi_id"
    LIT_PUBMED_ID = "lit_pubmed_id"
    MASS = "mass"
    ORGANELLE = "organelle"
    ORGANISM_ID = "organism_id"
    ORGANISM_NAME = "organism_name"
    PH_DEPENDENCE = "ph_dependence"
    PROTEIN_EXISTENCE = "protein_existence"
    PROTEIN_FAMILIES = "protein_families"
    PROTEIN_NAME = "protein_name"
    REDOX_POTENTIAL = "redox_potential"
    REVIEWED = "reviewed"
    RHEA = "rhea"
    SEQUENCE = "sequence"
    SEQUENCE_VERSION = "sequence_version"
    STRUCTURE_3D = "structure_3d"
    TEMP_DEPENDENCE = "temp_dependence"
    TOOLS = "tools"
    UNIPARC_ID = "uniparc_id"
    VERSION = "version"
    VIRUS_HOSTS = "virus_hosts"
    XREF_ABCD = "xref_abcd"
    XREF_AGR = "xref_agr"
    XREF_ALLERGOME = "xref_allergome"
    XREF_ALPHAFOLDDB = "xref_alphafolddb"
    XREF_ALZFORUM = "xref_alzforum"
    XREF_ANTIBODYPEDIA = "xref_antibodypedia"
    XREF_ANTIFAM = "xref_antifam"
    XREF_ARACHNOSERVER = "xref_arachnoserver"
    XREF_ARAPORT = "xref_araport"
    XREF_BGEE = "xref_bgee"
    XREF_BINDINGDB = "xref_bindingdb"
    XREF_BIOCYC = "xref_biocyc"
    XREF_BIOGRID = "xref_biogrid"
    XREF_BIOGRID_ORCS = "xref_biogrid-orcs"
    XREF_BIOMUTA = "xref_biomuta"
    XREF_BMRB = "xref_bmrb"
    XREF_BRENDA = "xref_brenda"
    XREF_CARBONYLDB = "xref_carbonyldb"
    XREF_CAZY = "xref_cazy"
    XREF_CCDS = "xref_ccds"
    XREF_CDD = "xref_cdd"
    XREF_CGD = "xref_cgd"
    XREF_CHEMBL = "xref_chembl"
    XREF_CHITARS = "xref_chitars"
    XREF_CLEANEX = "xref_cleanex"
    XREF_COLLECTF = "xref_collectf"
    XREF_COMPLEXPORTAL = "xref_complexportal"
    XREF_CONOSERVER = "xref_conoserver"
    XREF_CORUM = "xref_corum"
    XREF_CPTAC = "xref_cptac"
    XREF_CPTC = "xref_cptc"
    XREF_CTD = "xref_ctd"
    XREF_DBSNP = "xref_dbsnp"
    XREF_DEPOD = "xref_depod"
    XREF_DICTYBASE = "xref_dictybase"
    XREF_DIP = "xref_dip"
    XREF_DISGENET = "xref_disgenet"
    XREF_DISPROT = "xref_disprot"
    XREF_DMDM = "xref_dmdm"
    XREF_DNASU = "xref_dnasu"
    XREF_DRUGBANK = "xref_drugbank"
    XREF_DRUGCENTRAL = "xref_drugcentral"
    XREF_ECHOBASE = "xref_echobase"
    XREF_EGGNOG = "xref_eggnog"
    XREF_ELM = "xref_elm"
    XREF_EMBL = "xref_embl"
    XREF_EMDB = "xref_emdb"
    XREF_EMIND = "xref_emind"
    XREF_ENSEMBL = "xref_ensembl"
    XREF_ENSEMBLBACTERIA = "xref_ensemblbacteria"
    XREF_ENSEMBLFUNGI = "xref_ensemblfungi"
    XREF_ENSEMBLMETAZOA = "xref_ensemblmetazoa"
    XREF_ENSEMBLPLANTS = "xref_ensemblplants"
    XREF_ENSEMBLPROTISTS = "xref_ensemblprotists"
    XREF_ESTHER = "xref_esther"
    XREF_EUHCVDB = "xref_euhcvdb"
    XREF_EVOLUTIONARYTRACE = "xref_evolutionarytrace"
    XREF_EXPRESSIONATLAS = "xref_expressionatlas"
    XREF_FLYBASE = "xref_flybase"
    XREF_FUNFAM = "xref_funfam"
    XREF_GENE3D = "xref_gene3d"
    XREF_GENECARDS = "xref_genecards"
    XREF_GENEID = "xref_geneid"
    XREF_GENEREVIEWS = "xref_genereviews"
    XREF_GENERIF = "xref_generif"
    XREF_GENETREE = "xref_genetree"
    XREF_GENEWIKI = "xref_genewiki"
    XREF_GENOMERNAI = "xref_genomernai"
    XREF_GLYCONNECT = "xref_glyconnect"
    XREF_GLYCOSMOS = "xref_glycosmos"
    XREF_GLYGEN = "xref_glygen"
    XREF_GRAMENE = "xref_gramene"
    XREF_GUIDETOPHARMACOLOGY = "xref_guidetopharmacology"
    XREF_HAMAP = "xref_hamap"
    XREF_HGNC = "xref_hgnc"
    XREF_HOGENOM = "xref_hogenom"
    XREF_HPA = "xref_hpa"
    XREF_IC4R = "xref_ic4r"
    XREF_IDEAL = "xref_ideal"
    XREF_IMGT_GENE_DB = "xref_imgt_gene-db"
    XREF_INPARANOID = "xref_inparanoid"
    XREF_INTACT = "xref_intact"
    XREF_INTERPRO = "xref_interpro"
    XREF_IPTMNET = "xref_iptmnet"
    XREF_JAPONICUSDB = "xref_japonicusdb"
    XREF_JPOST = "xref_jpost"
    XREF_KEGG = "xref_kegg"
    XREF_LEGIOLIST = "xref_legiolist"
    XREF_LEPROMA = "xref_leproma"
    XREF_MAIZEGDB = "xref_maizegdb"
    XREF_MALACARDS = "xref_malacards"
    XREF_MANE_SELECT = "xref_mane-select"
    XREF_MASSIVE = "xref_massive"
    XREF_MEROPS = "xref_merops"
    XREF_METOSITE = "xref_metosite"
    XREF_MGI = "xref_mgi"
    XREF_MIM = "xref_mim"
    XREF_MINT = "xref_mint"
    XREF_MOONDB = "xref_moondb"
    XREF_MOONPROT = "xref_moonprot"
    XREF_NCBIFAM = "xref_ncbifam"
    XREF_NEXTPROT = "xref_nextprot"
    XREF_NIAGADS = "xref_niagads"
    XREF_OGP = "xref_ogp"
    XREF_OMA = "xref_oma"
    XREF_OPENTARGETS = "xref_opentargets"
    XREF_ORCID = "xref_orcid"
    XREF_ORPHANET = "xref_orphanet"
    XREF_ORTHODB = "xref_orthodb"
    XREF_PANTHER = "xref_panther"
    XREF_PATHWAYCOMMONS = "xref_pathwaycommons"
    XREF_PATRIC = "xref_patric"
    XREF_PAXDB = "xref_paxdb"
    XREF_PCDDB = "xref_pcddb"
    XREF_PDB = "xref_pdb"
    XREF_PDBSUM = "xref_pdbsum"
    XREF_PEPTIDEATLAS = "xref_peptideatlas"
    XREF_PEROXIBASE = "xref_peroxibase"
    XREF_PFAM = "xref_pfam"
    XREF_PGENN = "xref_pgenn"
    XREF_PHARMGKB = "xref_pharmgkb"
    XREF_PHAROS = "xref_pharos"
    XREF_PHI_BASE = "xref_phi-base"
    XREF_PHOSPHOSITEPLUS = "xref_phosphositeplus"
    XREF_PHYLOMEDB = "xref_phylomedb"
    XREF_PIR = "xref_pir"
    XREF_PIRSF = "xref_pirsf"
    XREF_PLANTREACTOME = "xref_plantreactome"
    XREF_POMBASE = "xref_pombase"
    XREF_PRIDE = "xref_pride"
    XREF_PRINTS = "xref_prints"
    XREF_PRO = "xref_pro"
    XREF_PROMEX = "xref_promex"
    XREF_PROSITE = "xref_prosite"
    XREF_PROTEOMES = "xref_proteomes"
    XREF_PROTEOMICSDB = "xref_proteomicsdb"
    XREF_PSEUDOCAP = "xref_pseudocap"
    XREF_PUBTATOR = "xref_pubtator"
    XREF_PUMBA = "xref_pumba"
    XREF_REACTOME = "xref_reactome"
    XREF_REBASE = "xref_rebase"
    XREF_REFSEQ = "xref_refseq"
    XREF_REPRODUCTION_2DPAGE = "xref_reproduction-2dpage"
    XREF_RGD = "xref_rgd"
    XREF_RNACT = "xref_rnact"
    XREF_SABIO_RK = "xref_sabio-rk"
    XREF_SASBDB = "xref_sasbdb"
    XREF_SFLD = "xref_sfld"
    XREF_SGD = "xref_sgd"
    XREF_SIGNALINK = "xref_signalink"
    XREF_SIGNOR = "xref_signor"
    XREF_SMART = "xref_smart"
    XREF_SMR = "xref_smr"
    XREF_STRING = "xref_string"
    XREF_SUPFAM = "xref_supfam"
    XREF_SWISSLIPIDS = "xref_swisslipids"
    XREF_SWISSPALM = "xref_swisspalm"
    XREF_TAIR = "xref_tair"
    XREF_TCDB = "xref_tcdb"
    XREF_TOPDOWNPROTEOMICS = "xref_topdownproteomics"
    XREF_TREEFAM = "xref_treefam"
    XREF_TUBERCULIST = "xref_tuberculist"
    XREF_UCSC = "xref_ucsc"
    XREF_UNICARBKB = "xref_unicarbkb"
    XREF_UNILECTIN = "xref_unilectin"
    XREF_UNIPATHWAY = "xref_unipathway"
    XREF_VECTORBASE = "xref_vectorbase"
    XREF_VEUPATHDB = "xref_veupathdb"
    XREF_VGNC = "xref_vgnc"
    XREF_WBPARASITE = "xref_wbparasite"
    XREF_WORMBASE = "xref_wormbase"
    XREF_XENBASE = "xref_xenbase"
    XREF_ZFIN = "xref_zfin"


class UniProtSearchParams(BaseModel):
    query: str = Field(..., description="Criteria to search UniProtKB. Advanced queries can be built with parentheses and conditionals such as AND, OR, and NOT. List of valid search fields.")
    fields: Optional[List[UniProtSearchField]] = Field(None, description="List of entry sections (fields) to be returned, separated by commas. List of valid fields.")
    sort: Optional[str] = Field(None, description="Specify field by which to sort results. List of valid sort fields.")
    includeIsoform: Optional[bool] = Field(False, description="Specify true to include isoforms, default is false.")
    size: Optional[int] = Field(5, ge=1, le=500, description="Specify the number of entries per page of results (Pagination size). Default is 25, max is 500.")
    
    class Config:
        use_enum_values = True
