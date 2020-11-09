from fastapi import FastAPI
from typing import Optional, List, Set
from pydantic import BaseModel
from vogdb.vogdb_api import Species
from vogdb.functionality import VogService, SpeciesService

api = FastAPI()
svc = VogService('data')
data_path = "/files/home/sigi/Documents/fastAPI/data_202/vog.genes.all.fa"


@api.get("/")
async def root():
    return {"message": "Here is the Server :)"}


# Filtering for species
@api.get("/species", response_model=List[Species])
async def get_species(name: Optional[Set[str]] = None, id: Optional[Set[int]] = None, phage: Optional[bool] = None,
                      source: Optional[str] = None):
    # need to write function to find species....
    result = SpeciesService.search(name=name, id=id, phage=phage, source=source)
    return result


# here all the filter options are listed
class Filter(BaseModel):
    sid: Optional[Set[int]] = None
    sn: Optional[Set[str]] = None
    #tx: Optional[str] = None
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
    vs: Optional[str] = None  # high, medium, low stringency
    lca: Optional[str] = None


@api.post("/filter/")
async def create_filter(paras: Filter):
    print("filter")
    #
    # finds aufrufen...
    return paras


searches = {
    "search1": {"sid": 1002724},
    "search2": {"sn": "India", "phage": True}
}

# @api.get("/vog_filtering/{Filter: paras}", response_model=List[VOG])


# @api.get("/species_filtering/", response_model=List[Species])

# @api.get("/protein_filtering/", response_model=List[Protein])
