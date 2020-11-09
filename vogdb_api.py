from fastapi import FastAPI, Query
from typing import Optional, List, Set
from pydantic import BaseModel


class Species(BaseModel):
	id: int
	name: str
	tax: str
	phage: bool
	source: str


class VOG(BaseModel):
	name: str
	functional_cat: str
	protein_count: int
	species_count: int
	proteins: Set[str]
	genes: Set[str]
	cons_fct_description: str
	#vius_specific: int[3] #high, medium and low stringency
	lca: str

class Protein(BaseModel):
	id: str
	seq: str
	description: Optional[str] = None
	species: str

class Gene(BaseModel):
	id: str
	seq: str




