from pydantic import BaseModel
from typing import Optional, Set, List


# Here we define the "schemas" i.e. specify what the output response should look like (which columns to select)


class VOG_profile(BaseModel):
    id: str
    protein_count: int
    species_count: int
    function: str
    consensus_function: str

    class Config:
        orm_mode = True


class Protein_profile(BaseModel):
    protein_id: str
    vog_id: str
    taxon_id: int
    species_name: str

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
