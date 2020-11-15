from fastapi import FastAPI, Query
from typing import Optional, List, Set
from pydantic import BaseModel


class Species(BaseModel):
    id: int
    name: str
    phage: bool
    source: str
# version: int


class VOG(BaseModel):
    name: str
    fct_category: Optional[str]
    protein_count: int
    species_count: int
    proteins: Set[str]
    species: Set[str]
    genes: Optional[Set[str]]
    description: Optional[str]
    ancestors: Optional[Set[str]]
    genomes_in_group: int
    genomes_total: int
    # virus_specific: int[3] #high, medium and low stringency
    stringency_high: Optional[bool]
    stringency_medium: Optional[bool]
    stringency_low: Optional[bool]


class Protein(BaseModel):
    id: str
    seq: str
    description: Optional[str] = None
    species: str


class Gene(BaseModel):
    id: str
    seq: str
