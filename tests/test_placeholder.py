import requests
import pytest
from jsonschema import validate
import random

base_url = 'https://jsonplaceholder.typicode.com/'
posts_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "userId": {
                    "type": "integer"
                },
                "id": {
                    "type": "integer"
                },
                "title": {
                    "type": "string"
                },
                "body": {
                    "type": "string"
                }
            },
            "required": [
                "userId",
                "id",
                "title",
                "body"
            ]
        }
    ]
}


def test_get_comments_random():
    test_id = random.randint(1, 100)

    response_posts = requests.get(base_url + 'posts/' + str(test_id) + '/comments')
    data_posts = response_posts.json()

    response_comments = requests.get(base_url + 'comments?postId=' + str(test_id))
    data_comments = response_comments.json()

    assert response_comments.status_code == 200
    assert response_posts.status_code == 200
    assert data_posts == data_comments


def test_get_posts():
    response = requests.get(base_url + 'posts')
    data = response.json()
    assert response.status_code == 200
    try:
        validate(instance=data, schema=posts_schema)
    except AttributeError:
        raise AttributeError(data)


@pytest.mark.parametrize('test_input, expected', [
    ('title', 'foo'),
    ('body', 'sample text')
])
def test_patch_post(test_input, expected):
    response = requests.patch(base_url + 'posts/1', data={test_input: expected})
    data = response.json()
    assert response.status_code == 200
    assert data[test_input] == expected


def test_delete_post():
    test_id = random.randint(1, 100)
    response = requests.delete(base_url + 'posts/' + str(test_id))
    assert response.status_code == 200


@pytest.mark.parametrize('test_input, expected', [
    ({'title': 'foo1', 'body': 'bar1', 'userId': 1},
     {'id': 101, 'title': 'foo1', 'body': 'bar1', 'userId': '1'}),
    ({'title': 'fake User', 'body': 'bar1', 'userId': 50},
     {'id': 101, 'title': 'fake User', 'body': 'bar1', 'userId': '50'})
])
def test_post_post(test_input, expected):
    response = requests.post(base_url + 'posts', data=test_input)
    data = response.json()
    assert response.status_code == 201
    assert data == expected
