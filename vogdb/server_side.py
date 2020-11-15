from fastapi import FastAPI, Query
from typing import Optional, Set
from pydantic import BaseModel
from .functionality import VogService

api = FastAPI()
svc = VogService('data')


@api.get("/")
async def root():
    return {"message": "Here is the root :)"}


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


@api.get("/species")
async def get_species(name: Optional[Set[str]] = Query(None), id: Optional[Set[int]] = Query(None),
                      phage: Optional[bool] = None, source: Optional[str] = None):
    response = list(svc.species.search(name=name, ids=id, phage=phage, source=source))
    if not response:
        return {"message": "Nothing could be found for your search options."}
    return response


@api.get("/vog")
async def get_vogs(
        names: Optional[Set[str]] = Query(None), fct_description: Optional[Set[str]] = Query(None),
        fct_category: Optional[Set[str]] = Query(None), gmin: Optional[int] = None, gmax: Optional[int] = None,
        pmin: Optional[int] = None, pmax: Optional[int] = None, species: Optional[Set[str]] = Query(None),
        protein_names: Optional[Set[str]] = Query(None), mingLCA: Optional[int] = None, maxgLCA: Optional[int] = None,
        mingGLCA: Optional[int] = None, maxgGLCA: Optional[int] = None, ancestors: Optional[Set[str]] = Query(None),
        h_stringency: Optional[bool] = None, m_stringency: Optional[bool] = None, l_stringency: Optional[bool] = None,
        virus_spec: Optional[bool] = None):
    response = list(svc.groups.search(names=names, fct_description=fct_description, fct_category=fct_category,
                                      gmin=gmin, gmax=gmax, pmin=pmin, pmax=pmax, species=species,
                                      protein_names=protein_names, mingLCA=mingLCA, maxgLCA=maxgLCA, mingGLCA=mingGLCA,
                                      maxgGLCA=maxgGLCA, ancestors=ancestors, h_stringency=h_stringency,
                                      m_stringency=m_stringency, l_stringency=l_stringency, virus_spec=virus_spec))
    if not response:
        return {"message": "Nothing could be found for your search options."}
    return response


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
