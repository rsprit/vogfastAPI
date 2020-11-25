import pandas as pd
from .vogdb_api import VOG, Species
from Bio import SeqIO
import os
from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional, Set, List


"""
Here we define all the search methods that are used for extracting the data from the database
"""

def get_vogs1(db: Session, ids: Optional[List[str]]):
    results = db.query(models.VOG_profile).filter(models.VOG_profile.id.in_(ids)).all()
    return results

def get_proteins(db: Session, species: str):
    search = "%" + species + "%"

    #ToDo FIX This returns (Protein_profile: protein_id, vog_id, taxon_id, species_names(which is a whole SpeciesProfile, but we need only species_name attribute
    results = db.query(models.Protein_profile).join(models.Species_profile).filter(models.Species_profile.species_name.like(search)).all()

    # This is a "dirty" workaround to return the data in format that the schemas.Protein_profile wants it
    results_formated = [schemas.Protein_profile.parse_obj({"protein_id" : result.protein_id,
                                                 "vog_id": result.vog_id,
                                                 "taxon_id":result.taxon_id,
                                                 "species_names": result.species_names.species_name}) for result in results]
    return results_formated


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
            result = result[result.genomes_total > mingGLCA - 1]

        if maxgLCA is not None:
            result = result[result.genomes_total < maxgGLCA + 1]

        if mingGLCA is not None:
            result = result[result.ggenomes_in_group > mingGLCA - 1]

        if maxgGLCA is not None:
            result = result[result.genomes_in_group < maxgGLCA + 1]

        if ancestors is not None:
            for anc in ancestors:
                result = result[result.ancestors.apply(lambda x: anc.lower() in x.lower())]

        if h_stringency is not None:
            result = result[result.stringency_high == bool(h_stringency)]

        if m_stringency is not None:
            result = result[result.stringency_medium == bool(m_stringency)]

        if l_stringency is not None:
            result = result[result.stringency_low == bool(l_stringency)]

        if virus_spec is not None:
            if virus_spec:
                result = result[
                    ((result.stringency_high == True) |
                     (result.stringency_medium == True) |
                     (result.stringency_low == True))]
            else:
                result = result[
                    ((result.stringency_high == False) &
                     (result.stringency_medium == False) &
                     (result.stringency_low == False))]

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
