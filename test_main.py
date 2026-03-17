#!/usr/bin/env python
import json
import os

import pytest

import main

EMAIL = 'test@test.com'
PASSWORD = 'test'
SECRET = 'test_secret'


@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.JWT_SECRET = SECRET
    main.APP.config['TESTING'] = True

    with main.APP.test_client() as client:
        yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL, 'password': PASSWORD}
    response = client.post(
        '/auth',
        data=json.dumps(body),
        content_type='application/json',
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert 'token' in payload
    assert payload['token'] is not None


def test_contents(client):
    auth_response = client.post(
        '/auth',
        data=json.dumps({'email': EMAIL, 'password': PASSWORD}),
        content_type='application/json',
    )
    token = auth_response.get_json()['token']

    response = client.get('/contents', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['email'] == EMAIL
    assert 'exp' in payload
    assert 'nbf' in payload


def test_contents_requires_token(client):
    response = client.get('/contents')
    assert response.status_code == 401
