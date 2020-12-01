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
    genomes_total = Column('GenomesTotal', Integer)
    ancestors = Column('Ancestors', String)
    stringency_high = Column('StringencyHigh', Boolean)
    stringency_medium = Column('StringencyMedium', Boolean)
    stringency_low = Column('StringencyLow', Boolean)
    proteins = Column('Proteins', String)


class Species_profile(Base):
    # mysql table name
    __tablename__ = "Species_profile"

    taxon_id = Column('TaxonID', Integer, primary_key=True, index=True)
    species_name = Column('SpeciesName', String)
    phage = Column('Phage', Boolean)
    source = Column('Source', String)
    version = Column('Version', Integer)
    protein_names = relationship("Protein_profile", back_populates="species_names")


class Protein_profile(Base):
    # mysql table name
    __tablename__ = "Protein_profile"

    protein_id = Column('ProteinID', String,primary_key=True)
    vog_id = Column('VOG_ID', String)
    taxon_id = Column('TaxonID', Integer,  ForeignKey("Species_profile.TaxonID"), index=True)
    species_names = relationship("Species_profile", back_populates="protein_names")
