
from .functionality import *
from .database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Query
from .schemas import VOG_profile, Protein_profile, VOG_UID, Species_ID, Species_profile, ProteinID, AA_seq, NT_seq
# from .schemas import *
from . import models
import logging

api = FastAPI()

# uncomment when we have a domain
# redirected_app = HTTPToHTTPSRedirectMiddleware(api, host="example_domain.com")


# Dependency. Connect to the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api.get("/")
async def root():
    return {"message": "Welcome to VOGDB-API"}


@api.get("/vsearch/species/",
         response_model=List[Species_ID])
def search_species(db: Session = Depends(get_db),
                   ids: Optional[Set[int]] = Query(None),
                   name: Optional[str] = None,
                   phage: Optional[bool] = None,
                   source: Optional[str] = None,
                   version: Optional[int] = None):
    """
    This functions searches a database and returns a list of species IDs for records in that database
    which meet the search criteria.
    :return:
    """
    species = get_species(db, models.Species_profile.taxon_id, ids, name, phage, source, version)

    if not species:
        raise HTTPException(status_code=404, detail="No Species match the search criteria.")
    return species


@api.get("/vsummary/species/",
         response_model=List[Species_profile])
async def get_summary_species(taxon_id: Optional[List[int]] = Query(None), db: Session = Depends(get_db)):
    """
    This function returns Species summaries for a list of taxon ids
    :param taxon_id: Taxon ID
    :param db: database session dependency
    :return: Species summary
    """
    logging.info("GET request vsummary/Species")
    logging.debug("Recieved a vsummary/species request with parameters: taxon_id = {0}".format(taxon_id))
    species_summary = find_species_by_id(db, taxon_id)


    if not species_summary:
        raise HTTPException(status_code=404, detail="No matching Species found")

    return species_summary


@api.get("/vsearch/vog/",
         response_model=List[VOG_UID])
def search_vog(db: Session = Depends(get_db),
               id: Optional[Set[str]] = Query(None),
               pmin: Optional[int] = None,
               pmax: Optional[int] = None,
               smax: Optional[int] = None,
               smin: Optional[int] = None,
               functional_category: Optional[Set[str]] = Query(None),
               consensus_function: Optional[Set[str]] = Query(None),
               mingLCA: Optional[int] = None,
               maxgLCA: Optional[int] = None,
               mingGLCA: Optional[int] = None,
               maxgGLCA: Optional[int] = None,
               ancestors: Optional[Set[str]] = Query(None),
               h_stringency: Optional[bool] = None,
               m_stringency: Optional[bool] = None,
               l_stringency: Optional[bool] = None,
               virus_specific: Optional[bool] = None,
               phages_nonphages: Optional[str] = None,
               proteins: Optional[Set[str]] = Query(None),
               species: Optional[Set[str]] = Query(None),
               tax_id: Optional[Set[int]] = Query(None),
               inclusive: Optional[str] = 'a'
               ):
    """
    This functions searches a database and returns a list of vog unique identifiers (UIDs) for records in that database
    which meet the search criteria.
    :return:
    """

    vogs = get_vogs(db, models.VOG_profile.id, id, pmin, pmax, smax, smin, functional_category, consensus_function,
                    mingLCA, maxgLCA, mingGLCA, maxgGLCA,
                    ancestors, h_stringency, m_stringency, l_stringency, virus_specific, phages_nonphages, proteins,
                    species, tax_id, inclusive)
    if not vogs:
        raise HTTPException(status_code=404, detail="No VOGs match the search criteria.")
    return vogs


@api.get("/vsummary/vog/",
         response_model=List[VOG_profile])
async def get_summary_vog(id: List[str] = Query(None), db: Session = Depends(get_db)):
    """
    This function returns vog summaries for a list of unique identifiers (UIDs)
    :param id: VOGID
    :param db: database session dependency
    :return: vog summary
    """

    vog_summary = find_vogs_by_uid(db, id)
    print(type(vog_summary))
    print(type(vog_summary[0]))
    if not vog_summary:
        raise HTTPException(status_code=404, detail="No matching VOGs found")

    return vog_summary


@api.get("/vsearch/protein/",
         response_model=List[ProteinID])
async def search_protein(db: Session = Depends(get_db),
                         species_name: Optional[Set[str]] = Query(None),
                         taxon_id: Optional[Set[int]] = Query(None),
                         VOG_id: Optional[Set[str]] = Query(None)):
    proteins = get_proteins(db, models.Protein_profile.id, species_name, taxon_id, VOG_id)
    if not proteins:
        raise HTTPException(status_code=404, detail="No matching Proteins found")

    return proteins


@api.get("/vsummary/protein/",
         response_model=List[Protein_profile])
async def get_summary_protein(id: List[str] = Query(None), db: Session = Depends(get_db)):
    """
    This function returns protein summaries for a list of Protein identifiers (pids)
    :param id: proteinID
    :param db: database session dependency
    :return: protein summary
    """

    protein_summary = find_proteins_by_id(db, id)

    if not protein_summary:
        raise HTTPException(status_code=404, detail="No matching Proteins found")

    return protein_summary


@api.get("/vfetch/vog/hmm")
async def fetch_vog(id: List[str] = Query(None)):
    """
    This function returns vog data for a list of unique identifiers (UIDs)
    :param id: VOGID
    :param db: database session dependency
    :return: vog data (HMM profile)
    """
    vog_hmm = find_vogs_hmm_by_uid(id)
    return vog_hmm


@api.get("/vfetch/vog/msa")
async def fetch_vog(id: List[str] = Query(None)):
    """
    This function returns vog data for a list of unique identifiers (UIDs)
    :param id: VOGID
    :param db: database session dependency
    :return: vog data (HMM profile)
    """
    vog_hmm = find_vogs_msa_by_uid(id)
    return vog_hmm


@api.get("/vfetch/protein/faa",
         response_model=List[AA_seq])
async def fetch_protein_faa(db: Session = Depends(get_db), id: List[str] = Query(None)):
    """
    This function returns Amino acid sequences for the proteins specified by the protein IDs
    :param id: ProteinID
    :param db: database session dependency
    :return: Amino acid sequences for the proteins
    """
    protein_faa = find_protein_faa_by_id(db, id)
    if not protein_faa:
        raise HTTPException(status_code=404, detail="No matching Proteins found")

    return protein_faa

@api.get("/vfetch/protein/fna",
         response_model=List[NT_seq])
async def fetch_protein_fna(db: Session = Depends(get_db), id: List[str] = Query(None)):
    """
    This function returns Nucleotide sequences for the genes specified by the protein IDs
    :param id: ProteinID
    :param db: database session dependency
    :return: Nucleotide sequences for the proteins
    """
    protein_fna = find_protein_fna_by_id(db, id)
    if not protein_fna:
        raise HTTPException(status_code=404, detail="No matching Proteins found")
    return protein_fna
