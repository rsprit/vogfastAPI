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
    protein_count = Column('ProteinCount', Integer, index=False)
    species_count = Column('SpeciesCount', Integer, index=False)
    function = Column('FunctionalCategory', String, index=True)
    consensus_function = Column('Consensus_func_description', String(100), index=False)

class Protein_profile(Base):
    # mysql table name
    __tablename__ = "Protein_profile"

    protein_id = Column('ProteinID', String, index=True)
    vog_id = Column('VOG_ID', String, index=False)
    taxon_id = Column('TaxonID', Integer, index=False)
    species_name = Column('Species_name', String, primary_key=True)