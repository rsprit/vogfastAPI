from pydantic import BaseModel
from typing import Optional, Set, List

"""
 Here we define the "schemas" i.e. specify what the output response should look like (which columns to select)
"""

"""
Very important Note: Here we specify what columns we want to return to the client
Pydantic models bridges with SQLAlchemy models.
In order that we connect Pydantic with SQLAlchemy, two criteria need to be valid:
1. the attribute type values of the returned query object (in functionality.py)  (e.g. Species_profile.species_name)
 need to match the attribute type of the Pydantic response model (in this case schemas.Species_profile.species_name)
2. The names of the  attributes the returned query object also need to be exactly the same as in the Pydantic 
response model object, so we have in query object with attribute Protein_profile.species_name
so the pydantic response model (Protein_profile) needs to have the attribute name species_name as well

if those two criteria are not fulfilled, pydantic will throw an ValidationError
"""

class VOG_UID(BaseModel):
    id: str

    class Config:
        orm_mode = True

class VOG_profile(BaseModel):
    id: str
    protein_count: int
    species_count: int
    function: str
    consensus_function: str
    genomes_in_group: int
    genomes_total_in_LCA: int
    ancestors: str = None
    h_stringency: bool
    m_stringency: bool
    l_stringency: bool
    proteins: str

    class Config:
        orm_mode = True


class Species_profile(BaseModel):
    taxon_id = int
    species_name = str
    phage = str
    source = str
    version = int

    class Config:
        orm_mode = True


class Protein_profile(BaseModel):
    protein_id: str
    vog_id: str
    taxon_id: int
    species_name: str

    class Config:
        orm_mode = True


# here all the filter options are listed
class Filter(BaseModel):
    sid: Optional[Set[int]] = None
    sn: Optional[Set[str]] = None
    # tx: Optional[str] = None
    p: Optional[bool] = None
    src: Optional[str] = None
    gmin: Optional[int] = None
    gmax: Optional[int] = None
    pmin: Optional[int] = None
    pmax: Optional[int] = None
    fc: Optional[str] = None
    pid: Optional[str] = None
    gn: Optional[str] = None
    fct: Optional[str] = None
    lca: Optional[str] = None
    vs: Optional[bool] = None  # high, medium, or low stringency
    h_stringency: Optional[bool] = None
    m_stringency: Optional[bool] = None
    l_stringency: Optional[bool] = None
