import cerberus
import requests
import re
import pytest
from jsonschema import validate

base_url = 'https://dog.ceo/api/'
image_pattern = re.compile(r"https://images\.dog\.ceo/breeds/\S+/(\S|_)+\.\w+")


@pytest.mark.parametrize('count', [1, 3, 15, 50])
def test_get_random(count):
    response = requests.get(base_url + 'breeds/image/random/' + str(count))
    data = response.json()
    matched = 0
    for row in data['message']:
        matched += len(image_pattern.findall(row))
    assert response.status_code == 200
    try:
        assert data['status'] == 'success'
    except AssertionError:
        raise AssertionError(data)
    try:
        assert matched == count
    except AssertionError:
        raise AssertionError(data['message'])


def test_get_all_breeds():
    all_breeds_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "message": {
                "type": "object"
            },
            "status": {
                "type": "string"
            }
        },
        "required": [
            "message",
            "status"
        ]
    }
    response = requests.get(base_url + 'breeds/list/all')
    data = response.json()
    assert response.status_code == 200
    try:
        assert data['status'] == 'success'
    except AssertionError:
        raise AssertionError(data)
    try:
        validate(instance=data, schema=all_breeds_schema)
    except AttributeError:
        raise AttributeError(data)


def test_by_breed():
    by_breed_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "message": {
                "type": "array"
            },
            "status": {
                "type": "string"
            }
        },
        "required": [
            "message",
            "status"
        ]
    }
    valid = cerberus.Validator
    response = requests.get(base_url + 'breed/hound/images')
    data = response.json()
    assert response.status_code == 200
    try:
        assert data['status'] == 'success'
    except AssertionError:
        raise AssertionError(data)
    try:
        validate(instance=data, schema=by_breed_schema)
    except AttributeError:
        raise AttributeError(data)


def test_all_images_of_sub_breed():
    response = requests.get(base_url + 'breed/hound/afghan/images')
    data = response.json()
    matched = 0
    for row in data['message']:
        matched += len(re.findall(r"https://images\.dog\.ceo/breeds/hound-afghan/(\S|_)+\.\w+", row))
    assert response.status_code == 200
    try:
        assert data['status'] == 'success'
    except AssertionError:
        raise AssertionError(data)
    try:
        assert matched == len(data['message'])
    except AssertionError:
        raise AssertionError(data['message'])


@pytest.mark.parametrize("test_input, expected",
                         [('hound', 7),
                          ('bulldog', 3),
                          ('bullterrier', 1),
                          ('australian', 1),
                          ('buhund', 1)])
def test_sub_breeds(test_input, expected):
    response = requests.get(base_url + 'breed/' + test_input + '/list')
    data = response.json()
    subs = list(data['message'])
    assert response.status_code == 200
    try:
        assert data['status'] == 'success'
    except AssertionError:
        raise AssertionError(data)
    try:
        assert len(subs) == expected
    except AssertionError:
        raise AssertionError(subs)
