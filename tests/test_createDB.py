from unittest.mock import patch, Mock
from createDB import getAPI
import pytest
import requests

# for me to test: pytest tests/test_createDB.py -v

@pytest.fixture
def mock_response():  # making fake api to get wig products and prices
    mock = Mock()
    mock.raise_for_status.return_value = None  # pretend request succeeded
    # makes fake json return value and with extra details in variants to test that only get price in test later
    mock.json.return_value = {
        "products": [
            {
                "tags": ["silky", "straight"],
                "variants": [{
                    "price": "2000.00",
                    "sku": "ABC123",          # extra field
                    "inventory_quantity": 5,   # extra field
                    "weight": 200              # extra field
                }]
            }
        ] * 11
    }
    return mock

@patch("requests.get")  # use patch to ignore regular requests
def test_getapi_success(mock_get, mock_response):  # replace the request with our mock one
    mock_get.return_value = mock_response  # set the getApi requests to return our fake response
    result = getAPI()
    assert len(result) == 11
    assert result[0][0] == "silky, straight"  # description from tags
    assert result[0][1] == "$2000.00"  # price with $ prefix
    assert result[0][2] == "$1500.00"  # first ora price

@patch("requests.get")
def test_getapi_badresponse(mock_get):
    # using a bad api so the error is raise and an empty list is returned
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    result = getAPI()
    assert result == []  # should return empty list on error

@patch("requests.get")
def test_getapi_bad_json(mock_get):
    # simulates bad JSON data missing the products key
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"wrong_key": []}  # missing "products" causes KeyError
    result = getAPI()
    assert result == []  # KeyError except catches it and returns empty list
