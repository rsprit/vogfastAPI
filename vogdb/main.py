import sys

from fastapi import Query, HTTPException
from typing import Optional, Set, List
from .functionality import VogService, get_vogs1, get_proteins
from .database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from .schemas import VOG_profile, Protein_profile, Filter


api = FastAPI()
svc = VogService('data')

# Dependency. Connect to the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api.get("/")
async def root():
    return {"message": "Here is the root :)"}

#ToDo: include more filtering options
@api.get("/vog_profile1/", response_model=List[VOG_profile])
def read_users(ids: Optional[List[str]] = Query(None), db: Session = Depends(get_db)):
    """This function takes a list of VOGids and returns all the matching VOG_profiles
    """
    vogs = get_vogs1(db, ids )

    if vogs is None:
        raise HTTPException(status_code=404, detail="User not found")
    return vogs

#ToDO: include more filtering options
@api.get("/protein_profile1/", response_model=List[Protein_profile])
def read_users(species: str = Query(None), db: Session = Depends(get_db)):
    """This function takes only one species and returns all protein profiles associated with this species/family
    """

    proteins = get_proteins(db, species )
    if proteins is None:
        raise HTTPException(status_code=404, detail="User not found")
    return proteins



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
