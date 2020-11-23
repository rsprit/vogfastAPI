from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from Bio import Entrez
import numpy as np

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

df = pd.read_csv(data_path + "vog.annotations.tsv", sep='\t')
df = df.rename(columns={"#GroupName": "VOG_ID"})
vog_fun_desc = df.iloc[:, 4].str.split(" ").str[1:].str.join(" ")  # trimming consensus functional description
df_selected = df.iloc[:, [0, 1, 2, 3]]
df_selected.insert(4, "Consensus_func_description", vog_fun_desc)

# create a table in the database
df_selected.to_sql(name='VOG_profile', con=engine,
                   if_exists='replace', index=False, chunksize=1000)

with engine.connect() as con:
    con.execute('ALTER TABLE `VOG_profile` ADD PRIMARY KEY (`VOG_ID`(767));')  # add primary key
    con.execute('ALTER TABLE VOG_profile  MODIFY  VOG_ID char(30) NOT NULL; ')  # convert text to char
    con.execute('ALTER TABLE VOG_profile  MODIFY  FunctionalCategory char(30) NOT NULL; ')
    con.execute('ALTER TABLE VOG_profile  MODIFY  Consensus_func_description char(100) NOT NULL; ')
    con.execute('CREATE UNIQUE INDEX VOG_profile_index ON VOG_profile (VOG_ID, FunctionalCategory);')  # create index
    con.execute('CREATE INDEX VOG_profile_index2 ON VOG_profile (Consensus_func_description);')  # create index

print('VOG_table successfuly created!')

# ---------------------
# Protein_table generation
# ----------------------
# extract proteins for each VOG
protein_list_df = pd.read_csv(data_path + "vog.members.tsv", sep='\t').iloc[:, [0, 4]]

# subsetting (only for testing purposes)
protein_list_df = protein_list_df.loc[np.random.choice(protein_list_df.index, 100, replace=False)]

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

# assign each protein its corresponding species by using NCBI entrez API
tax_ids = protein_list_df["TaxonID"]

Entrez.email = 'vinkopcelica27@gmail.com'  # Put your email here
handle = Entrez.efetch('taxonomy', id=tax_ids, rettype='xml')
response = Entrez.read(handle)

species_names = [entry.get('ScientificName') for entry in response]

# add species to the protein table
protein_list_df.insert(3, "Species_name", species_names)

# ToDo: use the same approach with Entrez to create protein names column


# create a protein table in the database
protein_list_df.to_sql(name='Protein_profile', con=engine,
                       if_exists='replace', index=False, chunksize=1000)

with engine.connect() as con:
    con.execute('ALTER TABLE `Protein_profile` ADD PRIMARY KEY (`ProteinID`(767));')
    con.execute('ALTER TABLE Protein_profile  MODIFY  ProteinID char(30) NOT NULL; ')
    con.execute('ALTER TABLE Protein_profile  MODIFY  TaxonID int(30) NOT NULL; ') #FOREIGN KEY for species...??
    con.execute('ALTER TABLE Protein_profile  MODIFY  VOG_ID char(30) NOT NULL; ')
    con.execute('ALTER TABLE Protein_profile  MODIFY  Species_name char(100) NOT NULL; ')
    con.execute('CREATE INDEX Protein_profile_by_species ON Protein_profile (Species_name);')
    con.execute('CREATE INDEX VOG_profile_index_by_protein ON Protein_profile (ProteinID);')

print('Protein_profile table successfully created!')

# ToDo creating other tables, modifying the existing tables, optimizing the structure
# ---------------------
# Species_table generation
# ----------------------
# extract Species information from the list
species_list_df = pd.read_csv(data_path + "vog.species.list",
                              sep='\t',
                              header=0,
                              names=['SpeciesName', 'TaxonID', 'Phage', 'Source', 'Version']) \
    .assign(Phage=lambda p: p.Phage == 'phage')
print(species_list_df)

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
