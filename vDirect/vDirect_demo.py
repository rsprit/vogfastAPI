import sys
from os import path
import pandas as pd

sys.path.append('../vogdb')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from vogdb import schemas, main

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    import requests
except ImportError:  # Python 2
    from urllib import urlencode
    from urllib2 import urlopen

base_url = 'http://127.0.0.1:8000/'


def vfetch(return_object="hmm", **params):
    """Yield the response of a query."""
    _valid_params = list(main.fetch_vog.__code__.co_varnames)

    # First make some basic checks.
    if return_object not in ["hmm", "msa"]:
        # return_object does not compare equal to any enum value:
        raise ValueError("Invalid return object " + str(return_object))

    for k in params:
        assert k in _valid_params, 'Unknown parameter: %s' % k

    url = base_url + 'vfetch/vog/{0}?'.format(return_object)

    r = requests.get(url=url, params=params)
    response = r.json()

    return response


def vsummary(return_object="vog", format="json", **params):
    """Yield the response (vog/species/protein summary of a query."""

    # First make some basic checks.
    if return_object not in ["vog", "species", "protein"]:
        # return_object does not compare equal to any enum value:
        raise ValueError("Invalid return object " + str(return_object))

    _valid_params = []
    if return_object == "vog":
        _valid_params = list(main.get_summary_vog.__code__.co_varnames)
    elif return_object == "species":
        _valid_params = list(main.get_summary_species.__code__.co_varnames)
    elif return_object == "protein":
        # ToDo for protein summary
        return "Not yet implemented"

    _valid_formats = ["json", "dataframe"]

    for k in params:
        assert k in _valid_params, 'Unknown parameter: %s' % k

    url = base_url + 'vsummary/{0}?'.format(return_object)

    # API GET request
    r = requests.get(url=url, params=params)
    response = r.json()

    # formatting
    if format == "dataframe":
        response = pd.DataFrame.from_dict(response)
    elif format == "csv":
        df = pd.DataFrame.from_dict(response)
        response = df.to_csv()
    return response

def vsummary(return_object="vog", format="json", **params):
    """Yield the response (vog/species/protein summary of a query."""

    # First make some basic checks.
    if return_object not in ["vog", "species", "protein"]:
        # return_object does not compare equal to any enum value:
        raise ValueError("Invalid return object " + str(return_object))

    _valid_params = []
    if return_object == "vog":
        _valid_params = list(main.get_summary_vog.__code__.co_varnames)
    elif return_object == "species":
        _valid_params = list(main.get_summary_species.__code__.co_varnames)
    elif return_object == "protein":
        #ToDo for protein summary
        return "Not yet implemented"

    _valid_formats = ["json", "dataframe"]

    for k in params:
        assert k in _valid_params, 'Unknown parameter: %s' % k

    url = base_url + 'vsummary/{0}?'.format(return_object)

    # API GET request
    r = requests.get(url=url, params=params)
    response = r.json()

    # formatting
    if format == "dataframe":
        response = pd.DataFrame.from_dict(response)
    elif format == "csv":
        df = pd.DataFrame.from_dict(response)
        response = df.to_csv()
    return response


def vsearch(return_object="vog", format="json", **params):
    """Yield the response (vog/species/protein summary of a query."""

    # First make some basic checks.
    if return_object not in ["vog", "species", "protein"]:
        # return_object does not compare equal to any enum value:
        raise ValueError("Invalid return object " + str(return_object))

    _valid_params = []
    if return_object == "vog":
        _valid_params = list(main.search_vog.__code__.co_varnames)
    elif return_object == "species":
        _valid_params = list(main.search_species.__code__.co_varnames)
    elif return_object == "protein":
        _valid_params = list(main.search_protein.__code__.co_varnames)
    else:
        raise ValueError("No return object given")

    _valid_formats = ["json", "dataframe"]

    for k in params:
        assert k in _valid_params, 'Unknown parameter: %s' % k

    url = base_url + 'vsearch/{0}?'.format(return_object)

    # API GET request
    r = requests.get(url=url, params=params)
    response = r.json()

    # formatting
    if format == "dataframe":
        response = pd.DataFrame.from_dict(response)
    elif format == "csv":
        df = pd.DataFrame.from_dict(response)
        response = df.to_csv()
    return response



# function to save hmm vFetch response objects (for now just hmm, mse)
def save_object(object, output_path="./test.txt"):
    """Saves the response object to output path"""

    with open(output_path, 'a') as file:
        for document in object:
            file.write(document)





print(vsummary(return_object="species", format="json", taxon_id=["2599843"]))