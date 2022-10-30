import requests
import pytest
from jsonschema import validate

base_url = 'https://api.openbrewerydb.org/breweries/'
brewery_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                }
            },
            "required": [
                "id",
                "name"
            ]
        }
    ]
}


def test_random():
    response = requests.get(base_url + 'random')
    data = response.json()
    try:
        validate(instance=data, schema=brewery_schema)
    except AttributeError:
        raise AttributeError(data)


def test_autocomplete():
    response = requests.get(base_url + 'autocomplete?query=dog')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 39


def test_list_default():
    response = requests.get(base_url)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 20


@pytest.mark.parametrize("test_input, expected", [
    (1, 1),
    (2, 2),
    (49, 49),
    (50, 50),
    (51, 50)
])
def test_list_per_rage(test_input, expected):
    response = requests.get(base_url + '?per_page=' + str(test_input))
    data = response.json()
    assert response.status_code == 200
    assert len(data) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("san_diego", "San Diego"),
    ("dallas", "Dallas"),
    ("new_york", "New York")
])
def test_search_by_city(test_input, expected):
    response = requests.get(base_url + '?by_city=' + str(test_input))
    data = response.json()
    assert response.status_code == 200
    assert len(data) <= 20
    for brewery in data:
        assert brewery["city"] == expected
