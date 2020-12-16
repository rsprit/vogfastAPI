import pytest
import sys
from os import path

sys.path.append('./')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from API_requests import *


""" Tests for API_requests.py
Test naming convention
test_MethodName_ExpectedBehavior_StateUnderTest:
e.g. test_isAdult_False_AgeLessThan18

test prefix is important for in order for the pytest to recognize it as test function. 
If there is no "test" prefix, pytest will not execute this test function.
"""


def test_vsearch_vogIds_allParameters():
    response = vsearch(return_object='vog',
                       format="dataframe",
                       id=[],
                       pmin=23,
                       pmax=100,
                       smin=1,
                       smax=50,
                       functional_category=["XrXs"],
                       l_stringency = True,
                       mingGLCA = 4,
                       phages_nonphages="phages_only")

    expected = ["VOG01473", "VOG02138"]
    assert response["id"].to_list() == expected


def test_vsearch_speciesIds_allParameters():
    response = vsearch(return_object="species",
                       format="dataframe",
                       ids = [],
                       name=["corona"],
                       phage= False,
                       source="NCBI Refseq",
                       version="201")

    expected = [11128, 290028, 1335626, 1384461, 2569586]
    assert response["taxon_id"].to_list() == expected


def test_vsearch_proteinIds_allParameters():
    response = vsearch(return_object="protein",
                       format="dataframe",
                       species_name = ["corona"],
                       taxon_id = [11128, 290028, 1335626, 1384461, 2569586],
                       VOG_id = ["VOG05566"])

    expected = ["11128.NP_150082.1"]
    assert response["id"].to_list() == expected


def test_vsummary_vogIds_twoVogIds():
    response = vsummary(return_object='vog', format="dataframe", id=['VOG00001', 'VOG00002'])

    expected = ['VOG00001', 'VOG00002']
    assert response["id"].to_list() == expected



def test_vsummary_speciesIds_twoTaxonIds():
    response = vsummary(return_object='species', format="dataframe", taxon_id=['2713308', '2591111'])

    expected = [2591111, 2713308]
    assert response["taxon_id"].to_list() == expected


def test_vsummary_proteinIds_twoProteinIds():
    response = vsummary(return_object="protein", format="dataframe", id=["11128.NP_150082.1"])
    expected = ['11128.NP_150082.1']
    print(response)
    assert response["id"].to_list() == expected
