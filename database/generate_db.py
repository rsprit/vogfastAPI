
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from Bio import Entrez
import numpy as np
import os
from sqlalchemy import VARCHAR
from sqlalchemy.dialects.mysql import LONGTEXT

"""
Here we create our VOGDB and create all the tables that we are going to use
Note: you may need to change the path of the data folder and your MYSQL credentials
"""
data_path = "../data/"

# MySQL database connection
username = "root"
password = "password"
server = "localhost"
database = "VOGDB"
SQLALCHEMY_DATABASE_URL = ("mysql+pymysql://{0}:{1}@{2}/{3}").format(username, password, server, database)


# Create an engine object.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()


# ---------------------
# VOG_table generation
# ----------------------
members = pd.read_csv(os.path.join(data_path, 'vog.members.tsv.gz'), compression='gzip',
                      sep='\t',
                      header=0,
                      names=['VOG_ID', 'ProteinCount', 'SpeciesCount', 'FunctionalCategory', 'Proteins'],
                      usecols=['VOG_ID', 'ProteinCount', 'SpeciesCount', 'FunctionalCategory', 'Proteins'],
                      index_col='VOG_ID')

annotations = pd.read_csv(os.path.join(data_path, 'vog.annotations.tsv.gz'), compression='gzip',
                          sep='\t',
                          header=0,
                          names=['VOG_ID', 'ProteinCount', 'SpeciesCount', 'FunctionalCategory', 'Consensus_func_description'],
                          usecols=['VOG_ID', 'Consensus_func_description'],
                          index_col='VOG_ID')

lca = pd.read_csv(os.path.join(data_path, 'vog.lca.tsv.gz'), compression='gzip',
                  sep='\t',
                  header=0,
                  names=['VOG_ID', 'GenomesInGroup', 'GenomesTotal', 'Ancestors'],
                  index_col='VOG_ID')

virusonly = pd.read_csv(os.path.join(data_path, 'vog.virusonly.tsv.gz'), compression='gzip',
                        sep='\t',
                        header=0,
                        names=['VOG_ID', 'StringencyHigh', 'StringencyMedium', 'StringencyLow'],
                        dtype={'StringencyHigh': bool, 'StringencyMedium': bool, 'StringencyLow': bool},
                        index_col='VOG_ID')

dfr = members.join(annotations).join(lca).join(virusonly)

# create a table in the database
dfr.to_sql(name='VOG_profile', con=engine, if_exists='replace', index=True,
           dtype={'VOG_ID': VARCHAR(dfr.index.get_level_values('VOG_ID').str.len().max()), 'Proteins': LONGTEXT},
           chunksize=1000)

with engine.connect() as con:
    con.execute('ALTER TABLE VOG_profile ADD PRIMARY KEY (`VOG_ID`(8)); ')  # add primary key
    con.execute('ALTER TABLE VOG_profile  MODIFY  VOG_ID char(30) NOT NULL; ')  # convert text to char
    con.execute('ALTER TABLE VOG_profile  MODIFY  FunctionalCategory char(30) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  Consensus_func_description char(100) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  ProteinCount int(255) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  SpeciesCount int(255) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  GenomesInGroup int(255) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  GenomesTotal int(255) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  Ancestors TEXT; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  StringencyHigh bool NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  StringencyMedium bool NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  StringencyLow bool NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  Proteins LONGTEXT; ')
    con.execute('CREATE UNIQUE INDEX VOG_profile_index ON VOG_profile (VOG_ID, FunctionalCategory);')  # create index
    # con.execute('CREATE INDEX VOG_profile_index2 ON VOG_profile (Consensus_func_description);')  # create index
    #con.execute('ALTER TABLE VOG_profile  ADD FOREIGN KEY (TaxonID) REFERENCES Species_profile(TaxonID); ')
# ToDo: add foreign keys to link to proteins, and species lists.
print('VOG_table successfully created!')


# ---------------------
# Species_table generation
# ----------------------
# extract Species information from the list
species_list_df = pd.read_csv(data_path + "vog.species.list",
                              sep='\t',
                              header=0,
                              names=['SpeciesName', 'TaxonID', 'Phage', 'Source', 'Version']) \
    .assign(Phage=lambda p: p.Phage == 'phage')

# create a species table in the database
species_list_df.to_sql(name='Species_profile', con=engine, if_exists='replace', index=False, chunksize=1000)

with engine.connect() as con:
    con.execute('ALTER TABLE `Species_profile` ADD PRIMARY KEY (`TaxonID`);')
    con.execute('ALTER TABLE Species_profile  MODIFY  SpeciesName char(100) NOT NULL; ')
    con.execute('ALTER TABLE Species_profile  MODIFY  TaxonID int(255) NOT NULL; ')
    con.execute('ALTER TABLE Species_profile  MODIFY  Phage bool NOT NULL; ')
    con.execute('ALTER TABLE Species_profile  MODIFY  Source char(100) NOT NULL; ')
    con.execute('ALTER TABLE Species_profile  MODIFY  Version int(255) NOT NULL; ')

# ToDo add foreign key to connect tax_id in protein_profile and species_profile? create index?

print('Species_profile table successfully created!')


#---------------------
# Protein_table generation
#----------------------

# extract proteins for each VOG
protein_list_df = pd.read_csv(data_path + "vog.members.tsv.gz", compression='gzip', sep='\t').iloc[:, [0,4]]

protein_list_df = protein_list_df.rename(columns={"#GroupName": "VOG_ID", "ProteinIDs": "ProteinID"})


# assign each protein a vog
protein_list_df = (protein_list_df["ProteinID"].str.split(",").apply(lambda x: pd.Series(x))
                   .stack()
                   .reset_index(level=1, drop=True)
                   .to_frame("ProteinID")
                   .join(protein_list_df[["VOG_ID"]], how="left")
                   )

# separate protein and taxonID into separate columns
protein_list_df["TaxonID"] = protein_list_df["ProteinID"].str.split(".").str[0]
protein_list_df["ProteinID"] = protein_list_df["ProteinID"].str.split(".").str[1:3].str.join(".")

# create a protein table in the database
protein_list_df.to_sql(name='Protein_profile', con=engine, if_exists='replace', index=False, chunksize=1000)

with engine.connect() as con:
    con.execute('ALTER TABLE Protein_profile  MODIFY  ProteinID char(30) NOT NULL; ')
    con.execute('ALTER TABLE Protein_profile  MODIFY  TaxonID int(30) NOT NULL; ')
    con.execute('ALTER TABLE Protein_profile  MODIFY  VOG_ID char(30) NOT NULL; ')
    con.execute('CREATE INDEX Protein_profile_by_species ON Protein_profile (Species_name);')
    con.execute('CREATE INDEX VOG_profile_index_by_protein ON Protein_profile (ProteinID);')
    # add foreign key
    con.execute('ALTER TABLE Protein_profile  ADD FOREIGN KEY (TaxonID) REFERENCES Species_profile(TaxonID); ')
    con.execute('ALTER TABLE Protein_profile  ADD FOREIGN KEY (VOG_ID) REFERENCES VOG_profile(VOG_ID); ')

print('Protein_profile table successfully created!')


#ToDo creating other tables, modifying the existing tables, optimizing the structure
