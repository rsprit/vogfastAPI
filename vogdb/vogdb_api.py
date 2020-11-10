from fastapi import FastAPI, Query
from typing import Optional, List, Set
from pydantic import BaseModel


class Species(BaseModel):
	id: int
	name: str
	phage: bool
	source: str
	#version: int


class VOG(BaseModel):
	name: str
	functional_cat: str
	protein_count: int
	species_count: int
	proteins: Set[str]
	genes: Set[str]
	cons_fct_description: str
	lca: str
	#virus_specific: int[3] #high, medium and low stringency
	h_stringency: bool
	m_stringency: bool
	l_stringency: bool

class Protein(BaseModel):
	id: str
	seq: str
	description: Optional[str] = None
	species: str

class Gene(BaseModel):
	id: str
	seq: str




