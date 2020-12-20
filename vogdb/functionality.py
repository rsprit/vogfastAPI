import pandas as pd
# from database.generate_db import ncbi
from .vogdb_api import VOG, Species
from Bio import SeqIO
import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional, Set, List
from fastapi import Query, HTTPException
import tarfile
import gzip
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
             tax_id: Optional[int]
             ):
    """
    This function searches the VOG based on the given query parameters
    """

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
                vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(models.Species_profile). \
                    filter(models.Species_profile.species_name.in_(species)).group_by(models.Protein_profile.vog_id). \
                    having(func.count(models.Species_profile.species_name) == len(species)).all()
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
                try:
                    id_list = ncbi.get_descendant_taxa(tax_id, collapse_subspecies=False, intermediate_nodes=True)
                    id_list.append(tax_id)
                except ValueError:
                    raise HTTPException(status_code=404, detail="The provided taxonomy ID is invalid.")
                vog_ids = db.query().with_entities(models.Protein_profile.vog_id).join(models.Species_profile). \
                    filter(models.Species_profile.taxon_id.in_(id_list)).group_by(models.Protein_profile.vog_id).all()
                vog_ids = {id[0] for id in vog_ids}  # convert to set
                filters.append(getattr(models.VOG_profile, "id").in_(vog_ids))

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


def find_protein_faa_by_id(pid):
    file_name = "./data/vog.proteins.all.fa"
    # gunzip files???
    prots = SeqIO.index(file_name, 'fasta')
    result = []
    for p in pid:
        result.append(prots[p])
        # result.append(p + " " + prots[p]._seq._data)
    return result


def find_protein_fna_by_id(pid):
    # gunzip files???
    file_name = "./data/vog.genes.all.fa"
    #f = gunzip(file_name)
    genes = SeqIO.index(file_name, 'fasta')
    result = []
    for p in pid:
        result.append(genes[p])
    # with open("example.fasta", "w") as handle:
    #     for ele in result:
    #         SeqIO.write(ele.values(), handle, "fasta")
    return result



class SpeciesService:

    def __init__(self, filename):
        self._data = pd.read_csv(filename,
                                 sep='\t',
                                 header=0,
                                 names=['name', 'id', 'phage', 'source', 'version'],
                                 index_col='id') \
            .assign(phage=lambda p: p.phage == 'phage')

    def __getitem__(self, id):
        return Species(id=id, **self._data.loc[id])

    def search(self, ids=None, name=None, phage=None, source=None):
        result = self._data

        if ids is not None:
            for i in ids:
                yield Species(id=i, **self._data.loc[i])
            # if they ask for ID, everything else is ignored, bc ID is unique.
            return

        if phage is not None:
            result = result[result.phage == bool(phage)]

        if name is not None:
            for name in name:
                result = result[result.name.apply(lambda x: name.lower() in x.lower())]

        if source is not None:
            result = result[result.source.apply(lambda x: source.lower() in x.lower())]

        # return the result as generator object (more efficient than long list, and also iterable)
        for id, row in result.iterrows():
            yield Species(id=id, **row)


class GroupService:

    def __init__(self, directory):
        self._directory = directory

        members = pd.read_csv(os.path.join(directory, 'vog.members.tsv'),
                              sep='\t',
                              header=0,
                              names=['group', 'protein_count', 'species_count', 'fct_category', 'proteins'],
                              index_col='group')
        members = members.assign(
            proteins=members.proteins.apply(lambda s: frozenset(s.split(','))),
        )
        members = members.assign(
            species=members.proteins.apply(lambda s: frozenset(p.split('.')[0] for p in s))
        )

        annotations = pd.read_csv(os.path.join(directory, 'vog.annotations.tsv'),
                                  sep='\t',
                                  header=0,
                                  names=['group', 'protein_count', 'species_count', 'fct_category', 'description'],
                                  usecols=['group', 'description'],
                                  index_col='group')

        lca = pd.read_csv(os.path.join(directory, 'vog.lca.tsv'),
                          sep='\t',
                          header=0,
                          names=['group', 'genomes_in_group', 'genomes_total', 'ancestors'],
                          index_col='group')
        lca = lca.assign(
            ancestors=lca.ancestors.fillna('').apply(lambda s: s.split(';'))
        )

        virusonly = pd.read_csv(os.path.join(directory, 'vog.virusonly.tsv'),
                                sep='\t',
                                header=0,
                                names=['group', 'stringency_high', 'stringency_medium', 'stringency_low'],
                                dtype={'stringency_high': bool, 'stringency_medium': bool, 'stringency_low': bool},
                                index_col='group')

        self._data = members.join(annotations).join(lca).join(virusonly)

    def __getitem__(self, id):
        return VOG(name=id, **self._data.loc[id])

    def search(self, names=None, fct_description=None, fct_category=None, gmin=None, gmax=None,
               pmin=None, pmax=None, species=None, protein_names=None, mingLCA=None, maxgLCA=None,
               mingGLCA=None, maxgGLCA=None, ancestors=None, h_stringency=None, m_stringency=None, l_stringency=None,
               virus_spec=None):

        result = self._data

        if names is not None:
            result = result.loc[names]

        if fct_description is not None:
            for fct_d in fct_description:
                result = result[result.description.apply(lambda x: fct_d.lower() in x.lower())]

        if fct_category is not None:
            for fct_c in fct_category:
                result = result[result.fct_category.apply(lambda x: fct_c.lower() in x.lower())]

        if gmin is not None:
            result = result[result.species_count > gmin - 1]

        if gmax is not None:
            result = result[result.species_count < gmax + 1]

        if pmin is not None:
            result = result[result.protein_count > pmin - 1]

        if pmax is not None:
            result = result[result.protein_count < pmax + 1]

        if protein_names is not None:
            for protein in protein_names:
                result = result[result.proteins.apply(lambda x: protein in x)]

        if species is not None:
            for spec in species:
                result = result[result.species.apply(lambda x: spec in x)]

        if mingLCA is not None:
            result = result[result.genomes_total_in_LCA > mingLCA - 1]

        if maxgLCA is not None:
            result = result[result.genomes_total_in_LCA < maxgLCA + 1]

        if mingGLCA is not None:
            result = result[result.ggenomes_in_group > mingGLCA - 1]

        if maxgGLCA is not None:
            result = result[result.genomes_in_group < maxgGLCA + 1]

        if ancestors is not None:
            for anc in ancestors:
                result = result[result.ancestors.apply(lambda x: anc.lower() in x.lower())]

        if h_stringency is not None:
            result = result[result.h_stringency == bool(h_stringency)]

        if m_stringency is not None:
            result = result[result.m_stringency == bool(m_stringency)]

        if l_stringency is not None:
            result = result[result.l_stringency == bool(l_stringency)]

        if virus_spec is not None:
            if virus_spec:
                result = result[
                    ((result.h_stringency == True) |
                     (result.m_stringency == True) |
                     (result.l_stringency == True))]
            else:
                result = result[
                    ((result.h_stringency == False) &
                     (result.m_stringency == False) &
                     (result.l_stringency == False))]

        # return the result as generator object (more efficient than long list)
        for id, row in result.iterrows():
            yield VOG(name=id, **row)

    def proteins(self, id):
        filename = os.path.join(self._directory, 'faa', '{}.faa'.format(id))
        return SeqIO.parse(filename, 'fasta')


class VogService:

    def __init__(self, directory):
        self._directory = directory
        self._groups = None
        self._species = None
        self._proteins = None
        self._genes = None

    @property
    def species(self):
        if self._species is None:
            self._species = SpeciesService(os.path.join(self._directory, 'vog.species.list'))
        return self._species

    @property
    def proteins(self):
        if self._proteins is None:
            self._proteins = SeqIO.index(os.path.join(self._directory, 'vog.proteins.all.fa'), 'fasta')
        return self._proteins

    @property
    def genes(self):
        if self._genes is None:
            self._genes = SeqIO.index(os.path.join(self._directory, 'vog.genes.all.fa'), 'fasta')
        return self._genes

    @property
    def groups(self):
        if self._groups is None:
            self._groups = GroupService(self._directory)
        return self._groups
