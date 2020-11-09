from fastapi import FastAPI, Query
from typing import Optional, List, Set
from pydantic import BaseModel
from vogdb_api import Species, VOG, Protein, Gene
from functionality import Species_search

api = FastAPI()
data_path = "/files/home/sigi/Documents/fastAPI/data_202/vog.genes.all.fa"

@api.get("/")
async def root():
    return {"message": "Here is the Server :)"}


#Filtering for species
@api.get("/species", response_model=List[Species])
async def get_species(name: Optional[str] = None, id: Optional[int] = None, tax: Optional[str] = None, phage: Optional[bool] = None, source: Optional[str] = None):
	# need to write function to find species....
	result = Species_search.search(name=name, id=id, tax=tax, phage=phage, source=source)
	return result

# here all the filter options are listed
class Filter(BaseModel):
	sid: Optional[int] = None 
	sn: Optional[str] = None 
	tx: Optional[str] = None 
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
	vs: Optional[str] = None #high, medium, low stringency
	lca: Optional[str] = None

@api.post("/filter/")
async def create_filter(filter: Filter):
	print("filter")
	return filter
	



#@api.get("/vog_filtering/", response_model=List[VOG])


#@api.get("/species_filtering/", response_model=List[Species])

#@api.get("/protein_filtering/", response_model=List[Protein])
		
