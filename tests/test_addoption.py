import requests


def test_url_status(input_url, expected_status_code):
    response = requests.get(input_url)
    assert response.status_code == expected_status_code
