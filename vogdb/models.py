from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

"""
"model" refers to classes and instances that interact with the database.
A model is equivalent to a database table e.g. VOG_profile table and it contains all the same attributes
"""


class VOG_profile(Base):
    # mysql table name
    __tablename__ = "VOG_profile"

    id = Column('VOG_ID', String, primary_key=True, index=True)
    protein_count = Column('ProteinCount', Integer)
    species_count = Column('SpeciesCount', Integer)
    function = Column('FunctionalCategory', String)
    consensus_function = Column('Consensus_func_description', String(100))
    genomes_in_group = Column('GenomesInGroup', Integer)
    genomes_total_in_LCA = Column('GenomesTotal', Integer)
    ancestors = Column('Ancestors', String)
    h_stringency = Column('StringencyHigh', Boolean)
    m_stringency = Column('StringencyMedium', Boolean)
    l_stringency = Column('StringencyLow', Boolean)
    virus_specific = Column('VirusSpecific', Boolean)
    num_phages = Column('NumPhages', Integer)
    num_nonphages = Column('NumNonPhages', Integer)
    phages_nonphages = Column('PhageNonphage', String)
    proteins = Column('Proteins', String)


class Species_profile(Base):
    # mysql table name
    __tablename__ = "Species_profile"

    species_name = Column('SpeciesName', String)
    taxon_id = Column('TaxonID', Integer, primary_key=True, index=True)
    phage = Column('Phage', Boolean)
    source = Column('Source', String)
    version = Column('Version', Integer)
    protein_names = relationship("Protein_profile", back_populates="species_names")


class Protein_profile(Base):
    # mysql table name
    __tablename__ = "Protein_profile"

    id = Column('ProteinID', String, primary_key=True)
    vog_id = Column('VOG_ID', String)
    taxon_id = Column('TaxonID', Integer,  ForeignKey("Species_profile.TaxonID"), index=True)
    species_names = relationship("Species_profile", back_populates="protein_names")


class AA_seq(Base):
    # mysql table name
    __tablename__ = "AA_seq"

    id = Column('ID', String, primary_key=True)
    seq = Column('AAseq', String)


class NT_seq(Base):
    # mysql table name
    __tablename__ = "NT_seq"

    id = Column('ID', String, primary_key=True)
    seq = Column('NTseq', String)
