import os
import string
import random

import pytest
import sys
from fastapi.testclient import TestClient
import pandas as pd
from sqlalchemy.orm import sessionmaker
from os import path
sys.path.append('../tests')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from tests import generate_test_db
sys.path.append('../vogdb')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from vogdb.database import Base
from vogdb.main import api, get_db
from httpx import AsyncClient
import time

""" Tests for vogdb.main.py
Test naming convention
test_MethodName_ExpectedBehavior_StateUnderTest:
e.g. test_isAdult_False_AgeLessThan18

test prefix is important for in order for the pytest to recognize it as test function. 
If there is no "test" prefix, pytest will not execute this test function.
"""



@pytest.fixture(scope="session")
def get_test_client():
    # connect to test database
    engine = generate_test_db.connect_to_database()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # create the database
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    api.dependency_overrides[get_db] = override_get_db
    client = TestClient(api)
    return client


#------------------------
# vSummary/vog
#------------------------

def test_vsummaryVog_vogProfiles_ids(get_test_client):
    client = get_test_client
    params = {"id": ["VOG00001", "VOG00002", "VOG00234", "VOG03456"]}
    response = client.get(url="/vsummary/vog/", params=params)
    expected = ["VOG00001", "VOG00002", "VOG00234", "VOG03456"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate

    assert data["id"].to_list() == expected

def test_vsummaryVog_vogProfileFieldNames_ids(get_test_client):
    client = get_test_client
    params = {"id": ["VOG00001", "VOG00002", "VOG00234", "VOG03456"]}
    response = client.get(url="/vsummary/vog/", params=params)
    expected = ['id', 'protein_count', 'species_count', 'function',
       'consensus_function', 'genomes_in_group', 'genomes_total_in_LCA',
       'ancestors', 'h_stringency', 'm_stringency', 'l_stringency',
       'proteins']

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    assert list(data.keys()) == expected

# ToDo test field types

def test_vsummaryVog_isIdempotent_ids(get_test_client):
    client = get_test_client
    params = {"id": ["VOG00001", "VOG00002", "VOG00234", "VOG03456"]}

    response = client.get(url="/vsummary/vog/", params=params)
    expected_response = client.get(url="/vsummary/vog/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vsummaryVog_ResponseUnder500ms_ids(get_test_client):
    client = get_test_client
    params = {"id": ["VOG00001", "VOG00002", "VOG00234", "VOG03456"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vsummary/vog/", params=params)
    end = time.time()

    assert end-start <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vsummaryVog_ERROR422_integers(get_test_client):
    client = get_test_client
    params = {"id": [657567, 123, 124124, 1123]}
    response = client.get(url="/vsummary/vog/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummaryVog_ERROR404_randomString(get_test_client):
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vsummary/vog/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vsummaryVog_ERROR422_noParameter(get_test_client):
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vsummary/vog/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummaryVog_ERROR403_longParameter(get_test_client):
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vsummary/vog/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing


#------------------------
# vSummary/species
#------------------------

def test_vsummarySpecies_SpeciesProfiles_ids(get_test_client):
    client = get_test_client
    #taxon IDs are Integers
    params = {"taxon_id": [2713301, 2713308]}
    # params = {"taxon_id": ["2713301", "2713308"]}
    response = client.get(url="/vsummary/species/", params=params)
    expected = [2713301, 2713308]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate

    assert data["taxon_id"].to_list() == expected

def test_vsummarySpecies_speciesProfileFieldNames_ids(get_test_client):
    client = get_test_client
    #taxon IDs are Integers
    params = {"taxon_id": [2713301, 2713308]}
    response = client.get(url="/vsummary/species/", params=params)
    expected = ['species_name', 'taxon_id', 'phage', 'source',
       'version']

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    assert list(data.keys()) == expected

# ToDo test field types

def test_vsummarySpecies_isIdempotent_ids(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["2713301", "2713308"]}

    response = client.get(url="/vsummary/species/", params=params)
    expected_response = client.get(url="/vsummary/species/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vsummarySpecies_ResponseUnder500ms_ids(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["2713301", "2713308"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vsummary/species/", params=params)
    end = time.time()

    assert end-start <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

# but species IDS are integers
def test_vsummarySpecies_ERROR422_integers(get_test_client):
    client = get_test_client
    params = {"taxon_id": [657567, 123, 124124, 1123]}
    response = client.get(url="/vsummary/species/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummarySpecies_ERROR404_randomString(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["SOMETHING"]}
    response = client.get(url="/vsummary/species/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vsummarySpecies_ERROR422_noParameter(get_test_client):
    client = get_test_client
    params = {"taxon_id": None}
    response = client.get(url="/vsummary/species/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummarySpecies_ERROR403_longParameter(get_test_client):
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"taxon_id": long_string }
    response = client.get(url="/vsummary/species/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing

#------------------------
# vSummary/protein
#------------------------

def test_vsummaryProtein_ProteinProfiles_ids(get_test_client):
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vsummary/protein/", params=params)
    expected = ["11128.NP_150082.1", "2301601.YP_009812740.1"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate

    assert data["id"].to_list() == expected

def test_vsummaryProtein_proteinProfileFieldNames_ids(get_test_client):
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vsummary/protein/", params=params)
    expected = ['id', 'vog_id', 'taxon_id', 'species_name']

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    assert list(data.keys()) == expected

# ToDo test field types

def test_vsummaryProtein_isIdempotent_ids(get_test_client):
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    response = client.get(url="/vsummary/protein/", params=params)
    expected_response = client.get(url="/vsummary/protein/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vsummaryProtein_ResponseUnder500ms_ids(get_test_client):
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vsummary/protein/", params=params)
    end = time.time()

    assert end-start <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vsummaryProtein_ERROR422_integers(get_test_client):
    client = get_test_client
    params = {"id": [657567, 123, 124124, 1123]}
    response = client.get(url="/vsummary/protein/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummaryProtein_ERROR404_randomString(get_test_client):
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vsummary/protein/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vsummaryProtein_ERROR422_noParameter(get_test_client):
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vsummary/protein/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsummaryProtein_ERROR403_longParameter(get_test_client):
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vsummary/protein/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing



#------------------------
# vfetch/vog
#------------------------

# ToDo need to create extra test folder for hmm, mse stuff...
def test_vfetchVogHMM_HMMProfiles_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = ["VOG00234", "VOG00003"]

    data = response.json()

    for i in range(len(expected)):
        # searching vogid in first 50 characters
        assert any(expected[i] in hmm[0:50] for hmm in data)


def test_vfetchVogHMM_HMMFieldTypes_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = type(list())

    data = response.json()
    assert type(data) == expected


def test_vfetchVogHMM_isIdempotent_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}

    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected_response = client.get(url="/vfetch/vog/hmm/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vfetchVogHMM__ResponseUnder500ms_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    end = time.time()

    response_time = end-start
    assert response_time <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vfetchVogHMM_ERROR422_integers(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": [123132]}
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchVogHMM_ERROR404_randomString(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vfetchVogHMM_ERROR422_noParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchVogHMM_ERROR403_longParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vfetch/vog/hmm/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing


#------------------------
# vfetch/msa
#------------------------

# ToDo need to create extra test folder for hmm, mse stuff...

def test_vfetchVogMSA_MSAFieldTypes_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}
    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected = type(list())

    data = response.json()
    assert type(data) == expected


def test_vfetchVogMSA_isIdempotent_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}

    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected_response = client.get(url="/vfetch/vog/msa/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vfetchMSA_ResponseUnder500ms_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["VOG00234", "VOG00003"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vfetch/vog/msa/", params=params)
    end = time.time()

    response_time = end-start
    assert response_time <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vfetchVogMSA_ERROR422_integers(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": [123132]}
    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchVogMSA_ERROR404_randomString(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vfetchVogMSA_ERROR422_noParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchVogMSA_ERROR403_longParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vfetch/vog/msa/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing

#------------------------
# vfetch/protein/faa
#------------------------

# ToDo need to create extra test folder for hmm, mse stuff...
def test_vfetchProteinFAA_FAAProfiles_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected =["11128.NP_150082.1", "2301601.YP_009812740.1"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate

    assert data["id"].to_list() == expected

def test_vfetchProteinFAA_FAAFieldNames_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected = ["id", "seq"]

    data = response.json()
    print(data)
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    print(data)
    assert list(data.keys()) == expected


def test_vfetchProteinFAA_isIdempotent_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected_response = client.get(url="/vfetch/protein/faa/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vfetchProteinFAA_ResponseUnder500ms_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vfetch/protein/faa/", params=params)
    end = time.time()

    response_time = end-start
    assert response_time <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vfetchProteinFAA_ERROR422_integers(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": [123132]}
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchProteinFAA_ERROR404_randomString(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vfetchProteinFAA_ERROR422_noParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchProteinFAA_ERROR403_longParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vfetch/protein/faa/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing


#------------------------
# vfetch/protein/fna
#------------------------

# ToDo need to create extra test folder for hmm, mse stuff...
def test_vfetchProteinFNA_FNAProfiles_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected =["11128.NP_150082.1", "2301601.YP_009812740.1"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate

    assert data["id"].to_list() == expected

def test_vfetchProteinFNA_FNAFieldNames_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected = ["id", "seq"]

    data = response.json()
    print(data)
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    print(data)
    assert list(data.keys()) == expected


def test_vfetchProteinFNA_isIdempotent_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected_response = client.get(url="/vfetch/protein/fna/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vfetchProteinFNA_ResponseUnder500ms_ids(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["11128.NP_150082.1", "2301601.YP_009812740.1"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vfetch/protein/fna/", params=params)
    end = time.time()

    response_time = end-start
    assert response_time <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vfetchProteinFNA_ERROR422_integers(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": [123132]}
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchProteinFNA_ERROR404_randomString(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": ["SOMETHING"]}
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vfetchProteinFNA_ERROR422_noParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    params = {"id": None}
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vfetchProteinFNA_ERROR403_longParameter(get_test_client):
    os.chdir("../") #need to change because of the find_vogs_hmm_by_uid() data folder
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"id": long_string }
    response = client.get(url="/vfetch/protein/fna/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing


#------------------------
# vSearch/protein
#------------------------

def test_vsearchProtein_ProteinProfiles_TaxonIds(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["10295", "10298"]}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = ["10295", "10298"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    for response_id in data["id"].to_list():
        assert any(expected_val in response_id for expected_val in expected)


def test_vsearchProtein_ProteinProfiles_SpeciesIdAndTaxonId(get_test_client):
    client = get_test_client
    params = {"species_name": ["herpes"], "taxon_id": "10310"}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = ["10310"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    for response_id in data["id"].to_list():
        assert expected[0] in response_id

def test_vsearchProtein_ProteinProfiles_SpeciesIdAndTaxonIdAndVOGId(get_test_client):
    client = get_test_client
    params = {"species_name": ["lacto"], "taxon_id": "37105", "VOG_id":["VOG00001"]}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = ["37105"]

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    for response_id in data["id"].to_list():
        assert expected[0] in response_id

def test_vsearchProtein_proteinProfileFieldNames_ids(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["10295", "10298"]}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = ['taxon_id']

    data = response.json()
    data = pd.DataFrame.from_dict(data) # converting to df so its easier to validate
    assert list(data.keys()) == expected

# ToDo test field types

def test_vsearchProtein_isIdempotent_ids(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["10295", "10298"]}

    response = client.get(url="/vsearch/protein/", params=params)
    expected_response = client.get(url="/vsearch/protein/", params=params)

    response_data = response.json()
    expected_data = expected_response.json()

    assert response_data == expected_data


def test_vsearchProtein_ResponseUnder500ms_ids(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["10295", "10298"]}

    expected_time = 0.5
    start = time.time()
    response = client.get(url="/vsearch/protein/", params=params)
    end = time.time()

    assert end-start <= expected_time


#ToDo positiv + optional parameters e.g. sort, limit, skip...

def test_vsearchProtein_ERROR422_idIntegers(get_test_client):
    client = get_test_client
    params = {"taxon_id": [657567, 123, 124124, 1123]}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsearchProtein_ERROR404_randomString(get_test_client):
    client = get_test_client
    params = {"taxon_id": ["SOMETHING"]}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = 404

    assert response.status_code == expected


def test_vsearchProtein_ERROR422_noParameter(get_test_client):
    client = get_test_client
    params = {"taxon_id": None}
    response = client.get(url="/vsearch/protein/", params=params)
    expected = 422

    assert response.status_code == expected

def test_vsearchProtein_ERROR403_longParameter(get_test_client):
    client = get_test_client
    letters = string.ascii_lowercase
    long_string = [''.join(random.choice(letters) for i in range(10000))]
    params = {"taxon_id": long_string }
    response = client.get(url="/vsearch/protein/", params=params)
    expected = 403

    assert response.status_code == expected

# ToDo load testing










