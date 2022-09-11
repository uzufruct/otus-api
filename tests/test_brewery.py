import cerberus
import requests
import re
import pytest

base_url = 'https://api.openbrewerydb.org/breweries/'
brewery_schema = {
    'type': 'list',
    'required': True,
    'schema': {
        "id": {'type': 'string', 'nullable': True},
        "name": {'type': 'string', 'nullable': True},
        "brewery_type": {'type': 'string', 'nullable': True},
        "street": {'type': 'string', 'nullable': True},
        "address_2": {'type': 'string', 'nullable': True},
        "address_3": {'type': 'string', 'nullable': True},
        "city": {'type': 'string', 'nullable': True},
        "state": {'type': 'string', 'nullable': True},
        "county_province": {'type': 'string', 'nullable': True},
        "postal_code": {'type': 'string', 'nullable': True},
        "country": {'type': 'string', 'nullable': True},
        "longitude": {'type': 'string', 'nullable': True},
        "latitude": {'type': 'string', 'nullable': True},
        "phone": {'type': 'string', 'nullable': True},
        "website_url": {'type': 'string', 'nullable': True},
        "updated_at": {'type': 'string', 'nullable': True},
        "created_at": {'type': 'string', 'nullable': True}
    }
}


@pytest.mark.skip()
def test_random():
    response = requests.get(base_url + 'random')
    data = response.json()
    v = cerberus.Validator()
    try:
        assert v.validate(data, brewery_schema)
    except TypeError:
        raise TypeError(data)


def test_autocomplete():
    response = requests.get(base_url + 'autocomplete?query=dog')
    data = response.json()
    pattern_id = re.compile(r"(\w|-)*dog(\w|-)*")
    # pattern_name = re.compile(r"(\w|-)*dog(\w|-)*")
    matched = 0
    for result in data:
        matched += len(pattern_id.findall(result['id']))
    assert response.status_code == 200
    assert matched == len(data)


