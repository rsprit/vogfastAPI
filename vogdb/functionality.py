# from database.generate_db import ncbi
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from typing import Optional, Set, List
from fastapi import HTTPException
import tarfile
from ete3 import NCBITaxa

# ncbi = NCBITaxa()

"""
Here we define all the search methods that are used for extracting the data from the database
"""

"""
Very important Note: Here we specify what columns we want to get from our query: e.g. protein_id,..,species_name
In order that this result output is gonna pass through the Pydantic validation, two criteria need to be valid:
1. the attribute type values of the returned query object (in functionality.py)  (e.g. Species_profile.species_name)
 need to match the attribute type of the Pydantic response model (in this case schemas.Species_profile.species_name)
2. The names of the  attributes the returned query object also need to be exactly the same as in the Pydantic 
response model object, so we have in query object with attribute Protein_profile.species_name
so the pydantic response model (Protein_profile) needs to have the attribute name species_name as well

if those two criteria are not fulfilled, pydantic will throw an ValidationError

"""


def find_species_by_id(db: Session, ids: Optional[List[int]]):
    """
    This function returns the Species information based on the given species IDs
    """
    if ids:
        results = db.query(models.Species_profile).filter(models.Species_profile.taxon_id.in_(ids)).all()
        return results
    else:
        print("No ids given")


def get_species(db: Session,
                response_body,
                taxon_id: Optional[Set[int]],
                species_name: Optional[str],
                phage: Optional[bool],
                source: Optional[str],
                version: Optional[int]):
    """
    This function searches the Species based on the given query parameters
    """
    result = db.query(response_body)
    arguments = locals()
    filters = []

    for key, value in arguments.items():  # type: str, any
        if value is not None:
            if key == "taxon_id":
                filters.append(getattr(models.Species_profile, key).in_(value))

            if key == "species_name":
                value = "%" + value + "%"
                filters.append(getattr(models.Species_profile, key).like(value))

            if key == "phage":
                filters.append(getattr(models.Species_profile, key).is_(value))

            if key == "source":
                value = "%" + value + "%"
                filters.append(getattr(models.Species_profile, key).like(value))

            if key == "version":
                filters.append(getattr(models.Species_profile, key) == value)

    result = result.filter(*filters)
    return result.all()


def find_vogs_by_uid(db: Session, ids: Optional[List[str]]):
    """
    This function returns the VOG information based on the given VOG IDs
    """
    results = db.query(models.VOG_profile).filter(models.VOG_profile.id.in_(ids)).all()
    return results


def find_vogs_hmm_by_uid(uid):
    file_name = "./data/vog.hmm.tar.gz"
    tar = tarfile.open(file_name, "r:gz")
    vog_hmm_list = []
    if uid:
        for vog_id in uid:
            vog_hmm_list.append(vog_id.upper() + ".hmm")
    hmm_response = []
    for vog_hmm in vog_hmm_list:
        member = tar.getmember(vog_hmm)
        f = tar.extractfile(member)
        if f is not None:
            file = f.read()
            hmm_response.append(file)
    return hmm_response


def find_vogs_msa_by_uid(uid):
    file_name = "./data/vog.raw_algs.tar.gz"
    tar = tarfile.open(file_name, "r:gz")
    vog_msa_list = []
    if uid:
        for vog_id in uid:
            vog_msa_list.append(vog_id.upper() + ".msa")
    msa_response = []
    for vog_msa in vog_msa_list:
        member = tar.getmember(vog_msa)
        f = tar.extractfile(member)
        if f is not None:
            file = f.read()
            msa_response.append(file)
    return msa_response


def get_vogs(db: Session,
             response_body,
             id: Optional[Set[str]],
             pmin: Optional[int],
             pmax: Optional[int],
             smax: Optional[int],
             smin: Optional[int],
             function: Optional[Set[str]],
             consensus_function: Optional[Set[str]],
             mingLCA: Optional[int],
             maxgLCA: Optional[int],
             mingGLCA: Optional[int],
             maxgGLCA: Optional[int],
             ancestors: Optional[Set[str]],
             h_stringency: Optional[bool],
             m_stringency: Optional[bool],
             l_stringency: Optional[bool],
             virus_specific: Optional[bool],
             phages_nonphages: Optional[str],
             proteins: Optional[Set[str]],
             species: Optional[Set[str]],
             tax_id: Optional[Set[int]],
             inclusive: Optional[str] = 'i'
             ):
    """
    This function searches the VOG based on the given query parameters
    """
    if inclusive is not 'i' and inclusive is not 'u':
        raise HTTPException(status_code=404,
                            detail="The parameter for the Intersecion or Union search has to be 'i' or 'u'.")

    result = db.query(response_body)
    arguments = locals()
    filters = []

    for key, value in arguments.items():  # type: str, any
        if value is not None:
            if key == "id":
                filters.append(getattr(models.VOG_profile, key).in_(value))

            if key == "consensus_function":
                for fct_d in value:
                    d = "%" + fct_d + "%"
                    filters.append(getattr(models.VOG_profile, key).like(d))

            if key == "function":
                for fct_d in value:
                    d = "%" + fct_d + "%"
                    filters.append(getattr(models.VOG_profile, key).like(d))

            if key == "smax":
                filters.append(getattr(models.VOG_profile, "species_count") < value + 1)

            if key == "smin":
                filters.append(getattr(models.VOG_profile, "species_count") > value - 1)

            if key == "pmax":
                filters.append(getattr(models.VOG_profile, "protein_count") < value + 1)

            if key == "pmin":
                filters.append(getattr(models.VOG_profile, "protein_count") > value - 1)

            if key == "proteins":
                for protein in value:
                    p = "%" + protein + "%"
                    filters.append(getattr(models.VOG_profile, key).like(p))

            if key == "species":
                if inclusive == 'i':
                    # THIS IS THE INTERSECTION SEARCH:
                    vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(models.Species_profile). \
                        filter(models.Species_profile.species_name.in_(species)).group_by(
                        models.Protein_profile.vog_id). \
                        having(func.count(models.Species_profile.species_name) == len(species)).all()
                else:
                    # UNION SEARCH below:
                    vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(models.Species_profile). \
                        filter(models.Species_profile.species_name.in_(species)).group_by(
                        models.Protein_profile.vog_id).all()
                vog_ids = {id[0] for id in vog_ids}  # convert to set
                filters.append(getattr(models.VOG_profile, "id").in_(vog_ids))

            if key == "maxgLCA":
                filters.append(getattr(models.VOG_profile, "genomes_total") < value + 1)

            if key == "mingLCA":
                filters.append(getattr(models.VOG_profile, "genomes_total") > value - 1)

            if key == "maxgGLCA":
                filters.append(getattr(models.VOG_profile, "genomes_in_group") < value + 1)

            if key == "mingGLCA":
                filters.append(getattr(models.VOG_profile, "genomes_in_group") > value - 1)

            if key == "ancestors":
                for anc in value:
                    a = "%" + anc + "%"
                    filters.append(getattr(models.VOG_profile, key).like(a))

            if key == "h_stringency":
                filters.append(getattr(models.VOG_profile, key).is_(value))

            if key == "m_stringency":
                filters.append(getattr(models.VOG_profile, key).is_(value))

            if key == "l_stringency":
                filters.append(getattr(models.VOG_profile, key).is_(value))

            if key == "virus_specific":
                filters.append(getattr(models.VOG_profile, key).is_(value))

            if key == "phages_nonphages":
                val = "%" + value + "%"
                filters.append(getattr(models.VOG_profile, key).like(val))

            if key == "tax_id":
                ncbi = NCBITaxa()
                # ncbi.update_taxonomy_database()

                try:
                    id_list = []
                    if inclusive == 'u':
                        # UNION SEARCH:
                        for id in tax_id:
                            id_list.extend(
                                ncbi.get_descendant_taxa(id, collapse_subspecies=False, intermediate_nodes=True))
                            id_list.append(id)
                        vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(
                            models.Species_profile). \
                            filter(models.Species_profile.taxon_id.in_(id_list)).group_by(
                            models.Protein_profile.vog_id). \
                            filter(models.Species_profile.taxon_id.in_(id_list)).group_by(
                            models.Protein_profile.vog_id).all()
                        vog_ids = {id[0] for id in vog_ids}  # convert to set
                        filters.append(getattr(models.VOG_profile, "id").in_(vog_ids))
                        print("ID LIST")
                        print(id_list)
                    else:
                        # INTERSECTION SEARCH:
                        for id in tax_id:
                            id_list.extend(
                                ncbi.get_descendant_taxa(id, collapse_subspecies=False, intermediate_nodes=True))
                            id_list.append(id)
                            vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(
                                models.Species_profile). \
                                filter(models.Species_profile.taxon_id.in_(id_list)).group_by(
                                models.Protein_profile.vog_id). \
                                filter(models.Species_profile.taxon_id.in_(id_list)).group_by(
                                models.Protein_profile.vog_id).all()
                            vog_ids = {id[0] for id in vog_ids}  # convert to set
                            filters.append(getattr(models.VOG_profile, "id").in_(vog_ids))

                except ValueError:
                    raise HTTPException(status_code=404, detail="The provided taxonomy ID is invalid.")

    result = result.filter(*filters)
    return result.all()


def get_proteins(db: Session,
                 response_body,
                 species: Optional[Set[str]],
                 taxon_id: Optional[Set[int]],
                 vog_id: Optional[Set[str]]):
    """
    This function searches the VOG based on the given query parameters
    """
    result = db.query(response_body)
    arguments = locals()
    filters = []

    for key, value in arguments.items():  # type: str, any
        if value is not None:
            if key == "species":
                s_res = []
                for s in species:
                    search = "%" + s + "%"
                    res = db.query().with_entities(models.Protein_profile.id,
                                                   models.Protein_profile.vog_id,
                                                   models.Protein_profile.taxon_id,
                                                   models.Species_profile.species_name).join(models.Species_profile). \
                        filter(models.Species_profile.species_name.like(search)).all()
                    s_res.extend(res)
                s_res = {id[0] for id in s_res}  # convert to set
                filters.append(getattr(models.Protein_profile, "id").in_(s_res))

            if key == "taxon_id":
                filters.append(getattr(models.Protein_profile, key).in_(value))

            if key == "vog_id":
                filters.append(getattr(models.Protein_profile, key).in_(value))

    result = result.filter(*filters)
    return result.all()


def find_proteins_by_id(db: Session, pids: Optional[List[str]]):
    """
    This function returns the Protein information based on the given Protein IDs
    """
    results = db.query().with_entities(models.Protein_profile.id,
                                       models.Protein_profile.vog_id,
                                       models.Protein_profile.taxon_id,
                                       models.Species_profile.species_name).join(models.Species_profile). \
        filter(models.Protein_profile.id.in_(pids)).all()

    return results


def find_protein_faa_by_id(db: Session, id: Optional[List[str]]):
    results = db.query(models.AA_seq).filter(models.AA_seq.id.in_(id)).all()
    return results


def find_protein_fna_by_id(db: Session, pid):
    results = db.query().with_entities(models.NT_seq.id,
                                       models.NT_seq.seq).filter(models.NT_seq.id.in_(pid)).all()
    return results
